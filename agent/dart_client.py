import requests
BASE="https://opendart.fss.or.kr/api"
class DartClient:
    def __init__(self,key):
        if not key: raise ValueError("DART_API_KEY is not set")
        self.key=key
    def get(self,path,params):
        p=dict(params); p["crtfc_key"]=self.key
        r=requests.get(BASE+path,params=p,timeout=60); r.raise_for_status(); return r.json()
    def financials(self,corp,year,code):
        return self.get("/fnlttSinglAcntAll.json",{"corp_code":corp,"bsns_year":year,"reprt_code":code,"fs_div":"CFS"})
