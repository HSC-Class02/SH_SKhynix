# Architecture

OpenDART → Python collector → raw JSON / normalized CSV → analysis CSV → dashboard/data.js → GitHub Pages.

- `update-data.yml`: 매월 1일(KST 09:10) 자동 수집 + 변경분 commit.
- `pages.yml`: dashboard 변경 시 GitHub Pages 자동 배포.
- 분기 손익/현금흐름은 DART 누적값에서 Q2/Q3/Q4를 역산하여 standalone quarter로 구성합니다.
- 재무상태표 항목은 각 분기 말 잔액을 사용합니다.
