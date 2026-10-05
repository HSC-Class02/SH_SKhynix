# OpenDART API 설정

1. [OpenDART](https://opendart.fss.or.kr/)에서 인증키를 발급합니다.
2. GitHub → **Settings → Secrets and variables → Actions → New repository secret**.
3. Secret 이름은 **`DART_API_KEY`** 로 입력합니다.
4. 값에는 발급받은 40자리 OpenDART 인증키를 입력합니다.
5. 기업코드는 SK hynix **`00164779`** 입니다.
6. Actions → **Update DART Financial Data** → Run workflow로 최초 실행을 테스트할 수 있습니다.

## 중요: 2010–2014년
OpenDART의 `fnlttSinglAcntAll` 개발가이드상 해당 API의 재무정보 제공은 2015년부터입니다. 따라서 이 프로젝트는 `START_YEAR=2010`을 유지하되 2010–2014를 **API 제공 전 기간**으로 기록합니다. 2015년 이후는 OpenDART API를 통해 자동 수집합니다.
