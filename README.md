# SK hynix DART Financial Analysis Agent

[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗%20대시보드%20바로가기-0753A6?style=for-the-badge&logo=github&logoColor=white)](https://HSC-Class02.github.io/SH_SKhynix/)

SK hynix (000660 / OpenDART corp_code `00164779`)의 DART 정기보고서 재무정보를 수집하고 성장성·수익성·현금흐름·재무안정성·자본효율을 분석하는 GitHub Actions 기반 agent입니다.

## 1. 자동화
- 대상 보고서: **사업보고서(Annual), 반기보고서(Half-year), 1분기보고서(Q1), 3분기보고서(Q3)**
- 수집 시작연도: **2010년**
- OpenDART `fnlttSinglAcntAll` API는 2015년부터 재무정보를 제공하므로 **2010–2014는 API 제공 전 기간으로 명시**하고, 2015년 이후를 자동 수집합니다.
- 매월 1일 **09:10 KST** 자동 업데이트
- 코드 변경 후 push trigger로 즉시 검증
- `DART_API_KEY`는 GitHub Actions Secret으로만 사용

## 2. 주요 재무 수치
**재무상태표**: 총자산, 유동자산, 현금및현금성자산, 매출채권, 재고자산, 총부채, 유동부채, 이자부차입금, 자본총계  
**손익계산서**: 매출액, 매출원가, 매출총이익, 판매비와관리비, 영업이익, 세전이익, 당기순이익, EBITDA  
**현금흐름표**: CFO, CFI, CFF, CAPEX, FCF  
**운전자본/부채**: 순차입금, DSO, DIO, CCC, 순차입금/EBITDA, 이자보상배율

## 3. 주요 재무비율
- 성장성: 매출증가율
- 수익성: Gross margin, Operating margin, Net margin, EBITDA margin
- 자본효율: ROA, ROE
- 유동성/안정성: Current ratio, Debt/Equity, Equity ratio, Debt dependency, Interest coverage
- 현금흐름: CFO/Net income, FCF
- 운전자본: DSO, DIO, CCC

분기 테이블은 DART 누적 손익·현금흐름에서 Q2/Q3/Q4를 standalone quarter로 역산하고, 재무상태표는 각 분기 말 잔액을 사용합니다.

## 4. Dashboard
[🔗 대시보드 바로가기](https://HSC-Class02.github.io/SH_SKhynix/)

상단에는 매출·영업이익 추이와 **Margins & Returns** 그래프를 배치하고, 하단에는 **Annual / Half-year / Quarterly** 3개 테이블과 국내 Peer Firms 표를 제공합니다.

## 5. 국내 Peer Firms
| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| Samsung Electronics | 005930 | 메모리/DRAM/NAND 직접 peer |
| DB HiTek | 000990 | 국내 반도체 제조/파운드리 peer |
| Hanmi Semiconductor | 042700 | HBM 패키징 장비 및 생태계 peer |
| SK Siltron | — | 반도체 웨이퍼/소재 value-chain peer, 비상장 |

Samsung Electronics는 SK hynix와 직접적인 국내 메모리 경쟁사이며, Hanmi Semiconductor는 HBM 패키징 장비를 통해 SK hynix 생태계와 연결됩니다. citeturn1search0turn1search4 DB HiTek은 국내 반도체 제조사로 별도의 foundry 중심 peer입니다. citeturn1search1

## 6. GitHub Pages
Repository → **Settings → Pages → Source: GitHub Actions**로 설정합니다.  
`pages.yml`이 `dashboard/`를 배포합니다.

## 7. API 인증키
`DART_API_KEY`를 코드나 README에 직접 입력하지 마세요. 설정 방법은 [docs/API_SETUP.md](docs/API_SETUP.md)를 참고하세요.

> 투자 판단 전 반드시 DART 원문 공시와 주석을 확인하세요.
