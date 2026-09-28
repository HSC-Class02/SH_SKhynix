# SK hynix DART Financial Analysis Agent

[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗%20대시보드%20바로가기-0753A6?style=for-the-badge&logo=github&logoColor=white)](https://HSC-Class02.github.io/SH_SKhynix/)

SK hynix(000660 / OpenDART corp_code `00164779`)의 2010년 이후 사업·반기·분기보고서 재무정보를 수집하고 주요 재무비율을 계산합니다.

## 자동화
매월 1일 `update-data.yml`이 실행되며 `DART_API_KEY` GitHub Secret을 사용합니다. 데이터 변경 시 commit되고 Pages가 배포됩니다.

## API Key
OpenDART에서 인증키를 발급한 후 Repository → Settings → Secrets and variables → Actions → New repository secret에서 `DART_API_KEY`를 등록하세요. API 키는 코드에 직접 넣지 않습니다.

## 주요 수치
매출액, 영업이익, 당기순이익, 총자산, 총부채, 총자본, 현금및현금성자산, 유동자산, 유동부채와 영업이익률, 순이익률, ROE, ROA, 유동비율, 부채비율을 제공합니다.

## Peer Firms
| 기업 | 비교 관점 |
|---|---|
| 삼성전자 | 메모리/반도체 |
| DB하이텍 | 파운드리 |
| SK실트론 | 반도체 웨이퍼 |
| 한미반도체 | 반도체 후공정 장비 |

## GitHub Pages
`Settings → Pages → Source: GitHub Actions`로 설정하세요.
Dashboard: https://HSC-Class02.github.io/SH_SKhynix/

투자 판단 전 원문 공시를 확인하세요.
