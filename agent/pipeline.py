import json
from datetime import date
from pathlib import Path
import pandas as pd
from .config import CORP_CODE, API_KEY, START_YEAR, END_YEAR, REPORT_CODES
from .dart_client import DartClient

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; RAW=DATA/"raw"; DASH=ROOT/"dashboard/data.js"
ALIASES={
"revenue":["매출액","수익(매출액)"],"cost_of_sales":["매출원가"],"gross_profit":["매출총이익"],
"operating_profit":["영업이익","영업이익(손실)"],"net_income":["당기순이익","당기순이익(손실)"],
"depreciation":["감가상각비","감가상각비와상각비","감가상각비 및 무형자산상각비"],
"total_assets":["자산총계"],"current_assets":["유동자산"],"cash":["현금및현금성자산","현금 및 현금성자산"],
"receivables":["매출채권","매출채권및기타채권"],"inventory":["재고자산"],"total_liabilities":["부채총계"],
"current_liabilities":["유동부채"],"debt":["단기차입금","단기차입금및유동성장기차입금","유동성장기부채","장기차입금","사채","리스부채","장기차입금및사채"],
"total_equity":["자본총계"],"ppe_purchase":["유형자산의 취득","유형자산 취득"],"intangibles_purchase":["무형자산의 취득","무형자산 취득"],
"cfo":["영업활동으로 인한 현금흐름","영업활동현금흐름"],"cfi":["투자활동으로 인한 현금흐름","투자활동현금흐름"],
"cff":["재무활동으로 인한 현금흐름","재무활동현금흐름"],"interest_expense":["이자비용","이자비용(금융비용)"]}
BAL={"total_assets","current_assets","cash","receivables","inventory","total_liabilities","current_liabilities","debt","total_equity"}
FLOW=set(ALIASES)-BAL

def n(v):
    s=str(v).strip().replace(",","") if v is not None else ""
    if s in ("","-","nan","None"): return None
    try: return float(s)
    except ValueError: return None

def extract(rows):
    matches={}
    for r in rows:
        name=str(r.get("account_nm","")).strip()
        for m,names in ALIASES.items():
            if any(name==x or x in name or name in x for x in names):
                matches.setdefault(m,[]).append(r)
    values={}; accounts={}
    for m,rs in matches.items():
        values[m]=sum(n(r.get("thstrm_amount")) or 0 for r in rs) if m in {"debt","ppe_purchase","intangibles_purchase"} else n(rs[0].get("thstrm_amount"))
        accounts[m]="; ".join(str(r.get("account_nm","")) for r in rs)
    return values,accounts

def fetch(client,year,code):
    x=client.financials(CORP_CODE,year,code,"CFS")
    if x.get("status")=="000": return x,"CFS"
    x=client.financials(CORP_CODE,year,code,"OFS")
    return x,"OFS"

def collect():
    RAW.mkdir(parents=True,exist_ok=True); client=DartClient(API_KEY); raw=[]; reports=[]
    end=END_YEAR or date.today().year
    for y in range(START_YEAR,end+1):
        for code,label in REPORT_CODES.items():
            if y<2015:
                reports.append({"year":y,"report_code":code,"report":label,"status":"not_available_via_fnlttSinglAcntAll_before_2015","rcept_no":"","dart_url":""}); continue
            try:
                x,fs=fetch(client,y,code); status=x.get("status",""); rows=x.get("list",[]) if status=="000" else []
                (RAW/f"{y}_{label}.json").write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
                raw.extend([{**r,"_fs_div":fs} for r in rows])
                r=rows[0].get("rcept_no","") if rows else ""
                reports.append({"year":y,"report_code":code,"report":label,"status":status,"message":x.get("message",""),"rcept_no":r,"fs_div":fs,"dart_url":f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={r}" if r else ""})
            except Exception as e:
                reports.append({"year":y,"report_code":code,"report":label,"status":"error","message":str(e),"rcept_no":"","dart_url":""})
    return raw,reports

def normalize(raw):
    groups={}
    for r in raw: groups.setdefault((r.get("bsns_year"),r.get("reprt_code"),r.get("_fs_div","CFS")),[]).append(r)
    rows=[]
    for (y,code,fs),rs in groups.items():
        vals,accounts=extract(rs)
        for m,v in vals.items():
            if v is not None: rows.append({"year":int(y),"report_code":str(code),"report":REPORT_CODES.get(str(code),str(code)),"metric":m,"value":v,"account_nm":accounts[m],"fs_div":fs})
    return pd.DataFrame(rows)

def wide(df):
    return df.pivot_table(index=["year","report_code","report"],columns="metric",values="value",aggfunc="first").reset_index() if not df.empty else pd.DataFrame()

def analyze(df,ptype):
    if df.empty: return df
    df=df.copy()
    cols=["revenue","cost_of_sales","gross_profit","operating_profit","net_income","total_assets","total_equity","current_assets","current_liabilities","total_liabilities","cash","debt","cfo","cfi","cff","ppe_purchase","intangibles_purchase","depreciation","interest_expense","receivables","inventory"]
    for c in cols:
        if c not in df: df[c]=pd.NA
    if df["gross_profit"].isna().all(): df["gross_profit"]=df.revenue-df.cost_of_sales
    df["ebitda"]=df.operating_profit+df.depreciation.fillna(0)
    df["capex"]=-(df.ppe_purchase.fillna(0).abs()+df.intangibles_purchase.fillna(0).abs())
    df["fcf"]=df.cfo+df.capex; df["net_debt"]=df.debt-df.cash
    df["gross_margin"]=df.gross_profit/df.revenue; df["operating_margin"]=df.operating_profit/df.revenue
    df["net_margin"]=df.net_income/df.revenue; df["ebitda_margin"]=df.ebitda/df.revenue
    df=df.sort_values(["year","report_code"]).reset_index(drop=True)
    df["avg_assets"]=(df.total_assets+df.total_assets.shift())/2; df["avg_equity"]=(df.total_equity+df.total_equity.shift())/2
    df["roa"]=df.net_income/df.avg_assets; df["roe"]=df.net_income/df.avg_equity
    df["current_ratio"]=df.current_assets/df.current_liabilities; df["debt_to_equity"]=df.total_liabilities/df.total_equity
    df["equity_ratio"]=df.total_equity/df.total_assets; df["debt_dependency"]=df.debt/df.total_assets
    df["interest_coverage"]=df.operating_profit/df.interest_expense.abs(); df["net_debt_ebitda"]=df.net_debt/df.ebitda
    df["cfo_to_net_income"]=df.cfo/df.net_income
    days=365 if ptype=="annual" else 181 if ptype=="half-year" else 91
    df["dso"]=df.receivables/df.revenue*days; df["dio"]=df.inventory/df.cost_of_sales.abs()*days; df["ccc"]=df.dso+df.dio
    df["period_type"]=ptype
    return df

def quarters(a,h,q1,q3):
    out=[]; frames=[a,h,q1,q3]
    years=sorted(set().union(*[set(x.year.astype(int)) for x in frames if not x.empty])) if any(not x.empty for x in frames) else []
    for y in years:
        A=a[a.year==y]; H=h[h.year==y]; O=q1[q1.year==y]; N=q3[q3.year==y]
        A=A.iloc[0].to_dict() if not A.empty else {}; H=H.iloc[0].to_dict() if not H.empty else {}
        O=O.iloc[0].to_dict() if not O.empty else {}; N=N.iloc[0].to_dict() if not N.empty else {}
        for q,base,bs,prev in [(1,O,O,{}),(2,H,H,O),(3,N,N,H),(4,A,A,N)]:
            if not base: continue
            r=dict(base); r["quarter"]=f"Q{q}"; r["report"]="quarterly"
            for m in BAL: r[m]=bs.get(m)
            for m in FLOW: r[m]=base.get(m) if q==1 else (base.get(m)-prev.get(m) if base.get(m) is not None and prev.get(m) is not None else base.get(m))
            out.append(r)
    d=pd.DataFrame(out)
    if d.empty: return d
    d["qo"]=d.quarter.map({"Q1":1,"Q2":2,"Q3":3,"Q4":4}); d=d.sort_values(["year","qo"]).drop(columns="qo")
    return analyze(d,"quarterly")

def records(df):
    if df.empty: return []
    return json.loads(df.replace({float("inf"):None,float("-inf"):None}).to_json(orient="records",force_ascii=False))

def main():
    DATA.mkdir(exist_ok=True); raw,reports=collect()
    pd.DataFrame(reports).to_csv(DATA/"reports.csv",index=False,encoding="utf-8-sig")
    long=normalize(raw); long.to_csv(DATA/"financial_data_long.csv",index=False,encoding="utf-8-sig"); b=wide(long)
    a=analyze(b[b.report_code=="11011"].copy(),"annual") if not b.empty else pd.DataFrame()
    h=analyze(b[b.report_code=="11012"].copy(),"half-year") if not b.empty else pd.DataFrame()
    q1=b[b.report_code=="11013"].copy() if not b.empty else pd.DataFrame(); q3=b[b.report_code=="11014"].copy() if not b.empty else pd.DataFrame()
    q=quarters(a,h,q1,q3)
    for name,d in [("annual",a),("half_year",h),("quarterly",q)]: d.to_csv(DATA/f"{name}.csv",index=False,encoding="utf-8-sig")
    payload={"annual":records(a),"half_year":records(h),"quarterly":records(q),"updated_at":str(date.today()),"source":"OpenDART","start_year":START_YEAR,"api_note":"OpenDART fnlttSinglAcntAll provides financial statements from 2015 onward; 2010-2014 are retained as explicit unavailable periods."}
    DASH.write_text("window.FINANCIAL_DATA="+json.dumps(payload,ensure_ascii=False,separators=(",",":"))+";",encoding="utf-8")
    print(f"Generated annual={len(a)}, half={len(h)}, quarterly={len(q)}")

if __name__=="__main__":
    main()
