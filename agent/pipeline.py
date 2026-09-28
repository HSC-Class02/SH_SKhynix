import json
from pathlib import Path
import pandas as pd
from .config import CORP_CODE,API_KEY,START_YEAR
from .dart_client import DartClient
CODES={"11011":"annual","11012":"half-year","11013":"quarterly-Q1","11014":"quarterly-Q3"}
KEYS={"매출액":"revenue","영업이익":"operating_profit","당기순이익":"net_income","자산총계":"total_assets","부채총계":"total_liabilities","자본총계":"total_equity","현금및현금성자산":"cash","유동자산":"current_assets","유동부채":"current_liabilities"}
def main():
    c=DartClient(API_KEY); rows=[]
    for y in range(START_YEAR,__import__("datetime").date.today().year+1):
        for code,label in CODES.items():
            try:
                x=c.financials(CORP_CODE,y,code)
                if x.get("status")!="000": continue
                Path("data").mkdir(exist_ok=True)
                Path(f"data/raw_{y}_{label}.json").write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
                rows+=x.get("list",[])
            except Exception as e: print("WARN",y,label,e)
    out=[]
    for r in rows:
        if r.get("account_nm") in KEYS:
            out.append({"year":r.get("bsns_year"),"report":r.get("reprt_code"),"metric":KEYS[r["account_nm"]],"amount":r.get("thstrm_amount")})
    df=pd.DataFrame(out)
    df.to_csv("data/financial_data.csv",index=False,encoding="utf-8-sig")
    p=df.pivot_table(index=["year","report"],columns="metric",values="amount",aggfunc="first").reset_index()
    for c in KEYS.values():
        if c not in p: p[c]=pd.NA
    p["operating_margin"]=p.operating_profit/p.revenue
    p["net_margin"]=p.net_income/p.revenue
    p["roe"]=p.net_income/p.total_equity
    p["roa"]=p.net_income/p.total_assets
    p["current_ratio"]=p.current_assets/p.current_liabilities
    p["debt_to_equity"]=p.total_liabilities/p.total_equity
    p.to_csv("data/analysis.csv",index=False,encoding="utf-8-sig")
    Path("dashboard/data.js").write_text("window.FINANCIAL_DATA="+p.to_json(orient="records",force_ascii=False)+";","utf-8")
if __name__=="__main__": main()
