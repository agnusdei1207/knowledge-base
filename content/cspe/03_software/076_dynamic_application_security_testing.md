---
title: "동적 분석 DAST (Dynamic Application Security Testing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 76
---

# 📖 【암기용】 개념 완전 이해

> 목적: DAST를 처음 봐도 실행 중인 애플리케이션을 외부 공격자 관점에서 점검하는 방식으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: DAST(동적 애플리케이션 보안 테스트)는 **배포 전 스테이징 환경에 올려 실제로 가동 중인 웹·API 애플리케이션**을 대상으로, 로그인 이후 화면·세션·API 인가까지 포함해 HTTP 요청·응답을 주고받으며 취약점을 검증하는 **런타임 보안 테스트 운영 절차**다.
- **왜 필요한가**: 소스코드는 정상이어도, 로그인 이후에만 보이는 관리자 화면이나 세션 쿠키 속성, API 인가 로직은 실제로 로그인해서 움직여봐야 검증할 수 있다. DAST는 이 "인증된 사용자 시점"까지 포함해 배포를 허용할지 판단하는 운영 게이트로 쓰인다.
- **핵심 직관**: 코드 리뷰가 아니라 실제 매장에 손님(정상 사용자)과 도둑(공격자) 역할로 들어가 출입문·계산대·창고 잠금이 실제로 버티는지 현장에서 확인하는 것이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 런타임 보안 테스트 (Runtime Security Test) | 애플리케이션을 실제로 가동한 상태에서 수행하는 보안 검증 — DAST가 속한 상위 범주 | 도면 검토가 아니라 실제 건물 현장 점검 |
| 블랙박스 (Black-box) | 소스코드를 보지 않고 입력·출력 관찰만으로 판단하는 방식 | 내부 배선을 모른 채 스위치만 눌러보는 것 |
| 인증 크롤링 (Authenticated Crawling) | 테스트 계정으로 로그인 세션을 유지한 채 화면·API를 탐색하는 절차 | 방문증을 받아 건물 안쪽 사무실까지 둘러보는 것 |
| OpenAPI(Swagger) 명세 | API의 엔드포인트·파라미터를 기계가 읽을 수 있게 정리한 문서 | 건물의 방 배치도 — 이게 있어야 안 가본 방도 빠짐없이 찾는다 |
| 커버리지 (Coverage) | 전체 화면·API 중 실제로 스캔이 도달한 비율 | 전체 방 중 실제로 점검한 방의 비율 |
| False Negative (미탐) | 실제로 취약한데 스캐너가 찾아내지 못하는 것 | 창문이 열려 있는데 순찰 경로에서 빠져 못 본 것 |
| Staging Gate | DAST 결과에 따라 운영 배포를 허용·차단하는 배포 관문 | 최종 검수를 통과해야 여는 출고 게이트 |
| Rate Limit | 짧은 시간에 과도한 요청이 들어오는 것을 막는 서버 제한 | 한 사람이 문을 너무 빨리 여러 번 두드리면 막는 경비 규칙 |

## 깊이 이해

### 인증 크롤링이 별도로 필요한 이유 — 수치로 확인
로그인 없이 크롤링하면 회원가입·비회원 열람 화면만 보인다. 예를 들어 전체 API가 100개인 서비스에서 그중 80개가 로그인 후에만 호출되는 API라면, 인증 없이 스캔했을 때 커버리지는 20%에 그친다. 테스트 계정과 세션 유지 로직(쿠키, JWT 리프레시)을 스캐너에 심어 로그인 상태로 크롤링해야 나머지 80개 API가 스캔 대상에 들어온다. 실무에서 인증 크롤링 커버리지 목표를 80% 이상으로 잡는 이유가 여기 있다.

### OpenAPI 명세를 넣으면 커버리지가 왜 오르는가
현대 REST API는 화면에 링크로 드러나지 않는 파라미터(예: 정렬 옵션, 관리자 전용 쿼리 파라미터)가 많다. 크롤러가 화면 링크만 따라가면 실제 API의 일부만 발견하는데, 백엔드의 OpenAPI(Swagger) JSON을 스캐너에 직접 넣어주면 정의된 모든 엔드포인트·파라미터를 빠짐없이 인지하고 각각에 페이로드를 주입할 수 있다. 그 결과 화면 크롤링만으로는 10%대에 머물던 API 커버리지가 명세 기반 스캔에서는 90% 이상까지 오르는 것이 일반적이다.

### 취약점 판별의 실제 예시
스테이징 환경의 주문 조회 API `/api/orders?id=1`에 작은따옴표 하나를 더한 `/api/orders?id=1'`을 보냈을 때, 정상이라면 400 에러나 빈 결과가 와야 한다. 그런데 응답 본문에 `SQL syntax error near ''''` 같은 DB 에러 메시지가 그대로 노출되거나, 정상 요청은 50ms인데 이 요청만 5초 넘게 걸린다면 SQL Injection 가능성으로 판정한다.

### 스테이징에서 반드시 데이터를 격리하는 이유
DAST는 실제 파괴적인 요청(글쓰기, 결제, 삭제 API 호출)까지 보낸다. 운영 DB를 그대로 쓰는 스테이징이라면 결제 API에 페이로드를 주입하는 순간 실제 결제가 발생하거나 실제 고객 데이터가 변조될 수 있다. 그래서 결제·메일 발송 같은 외부 연동은 mock 처리하고, 운영 데이터 복제를 금지하며, 스캔 후 rollback 가능한 시드 데이터로 되돌리는 절차가 필수다.

### False Negative가 생기는 대표 원인과 대응
- 인증 크롤링이 실패하면 보호된 API 전체가 스캔 대상에서 빠져 미탐이 급증한다 → 테스트 계정·시드 URL·OpenAPI 명세를 스캐너에 명시적으로 제공해야 한다.
- WAF나 Rate Limit이 스캐너의 대량 요청을 공격으로 오인해 차단하면, 그 이후 페이로드는 서버에 도달조차 못 하고 미탐으로 이어진다 → 스캐너 IP를 WAF 예외 목록에 등록한다.
- 스캔 시간이 부족해 중간에 잘리면 뒷부분 엔드포인트가 통째로 누락된다 → 위험도가 높은 엔드포인트부터 스캔하는 risk-based 순서 조정과 병렬 스캔으로 시간을 관리한다.

## 연결 개념
- SAST — 코드 내부 흐름을 보는 보완 테스트
- API Security Testing — OpenAPI 명세 기반 엔드포인트 점검
- Penetration Test — 수동 공격 시나리오 기반 심층 점검

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DAST는 실행 애플리케이션을 블랙박스 관점에서 공격해 인증, 세션, API, 배포 설정 관련 런타임 취약점을 검증하는 통제이다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DAST는 실행 중인 웹·API 서비스에 실제 HTTP 요청을 보내 취약 응답과 비정상 동작을 탐지하는 보안 테스트이다.
> 2. **가치**: staging gate에서 OWASP Top 10, 인증 크롤링, API scan을 수행해 배포 전 critical 취약점 0건을 목표로 함.
> 3. **판단 포인트**: 블랙박스 특성상 false negative가 있으므로 인증 설정, 스캔 범위, SAST·수동 점검 보완이 필수임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 보안 테스트 원리 확인 | running app, black-box, request/response 분석 | 소스 코드 분석인 SAST와 혼동 |
| 운영 적용 판단 확인 | auth crawling, API scan, staging gate | 로그인 필요 화면 스캔 누락 |
| 한계와 보완 이해 확인 | false negative, 스캔 범위, SAST 병행 | DAST만으로 전체 보안 검증 완료 주장 |

> 요약: 이 문제는 실행 환경 취약점 검증과 배포 게이트 운영을 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 실행 앱 블랙박스 보안 테스트
- 배경: 소스 코드 분석만으로는 런타임 설정, 인증 흐름, 세션 쿠키 속성, 서버 오류 노출 같은 실행 환경 결함을 확인하기 어렵다.
- 필요성: DAST는 staging 또는 pre-prod 환경에 SQLi, XSS, 인증 우회 페이로드를 전송해 배포 전 취약 동작을 차단한다.

---

## Ⅱ. 구조 및 구성요소

```text
Running Web/API App -> Crawler / OpenAPI Import
  -> Auth Session -> Attack Payload Engine
  -> Response Analyzer -> Finding -> Staging Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Crawler | 화면·링크·폼 탐색 | SPA는 JS 렌더링 지원 필요 |
| Auth Handler | 로그인·토큰·세션 유지 | MFA, refresh token 처리 |
| Payload Engine | 공격 입력 생성 | XSS, SQLi, SSRF, path traversal |
| Response Analyzer | 오류·반사·지연 응답 분석 | evidence 기반 finding |
| Staging Gate | 배포 허용 여부 결정 | critical 0건, high 예외 승인 |

> 요약: DAST 구조는 실행 앱 탐색, 인증 유지, 공격 페이로드 전송, 응답 분석, 배포 게이트로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Deploy to Staging -> Seed URL / OpenAPI Spec
  -> Login Session -> Crawl / API Enumerate
  -> Attack Requests -> Analyze Evidence
  -> Block / Approve Release
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | staging 환경에 배포 후 scan target 등록 | 운영 데이터 미사용, 테스트 계정 사용 |
| 2 | 인증 세션 생성과 크롤링 수행 | authenticated coverage 80% 이상 |
| 3 | 웹·API 엔드포인트에 페이로드 전송 | rate limit, WAF 예외 범위 설정 |
| 4 | 응답 코드·본문·시간 기반 evidence 분석 | 재현 가능한 finding 확보 |
| 5 | 배포 승인·차단·예외 처리 | critical 0건, high 승인 기록 |

> 요약: DAST는 staging 배포 후 인증 크롤링과 공격 요청을 수행하고 evidence 기준으로 배포 허용 여부를 결정한다.

---

## Ⅳ. 특징

| 구분 | SAST | DAST | 정량 기준 |
|:---|:---|:---|:---|
| 분석 대상 | 코드·바이트코드 | 실행 앱·API | staging URL, OpenAPI |
| 관점 | 내부 경로 | 외부 공격자 관점 | black-box |
| 탐지 강점 | 코드 흐름 취약점 | 런타임·설정·인증 취약점 | OWASP Top 10 |
| 한계 | 오탐 가능 | 미탐 가능 | authenticated coverage |
| 적용 시점 | PR·CI | staging·pre-prod | release gate |

> 요약: DAST는 실행 환경 취약점 확인에 강점이 있으며 SAST와 결합할 때 탐지 범위가 넓어진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SAST는 내부 코드 분석 | DAST는 외부 요청 분석 | 런타임 설정 검증 시 DAST |
| 비용/성능 | 수동 모의해킹 | 자동 반복 스캔 | 릴리스마다 staging scan 필요 시 |
| 운영/위험 | 운영 직접 점검 | 격리 staging 점검 | 운영 데이터 영향 0건 필요 |
| API | 화면 크롤링 중심 | OpenAPI 기반 API scan | API 서비스는 명세 기반 병행 |

> 요약: DAST는 실행 환경과 인증 흐름 검증이 필요한 릴리스 게이트에 적합하며, 코드 결함은 SAST로 보완한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| false negative | 크롤링·인증 실패 | seed URL, OpenAPI, test account 제공 | authenticated coverage 80% 이상 |
| 테스트 장애 | 공격 페이로드로 데이터 변조 | staging 격리, mock payment, rollback seed | 데이터 오염 0건 |
| 스캔 장기화 | 엔드포인트 과다 | risk-based scan, parallel worker | scan time 60분 이하 |
| 오탐 논쟁 | evidence 불충분 | 재현 요청·응답 저장 | 재현율 90% 이상 |

> 요약: DAST 리스크는 인증 범위, 테스트 데이터 격리, 스캔 시간, evidence 재현성으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배포 차단 | critical 0건, high 승인 기록 100% | DAST report, release log |
| 탐색 범위 | authenticated coverage 80% 이상 | crawler coverage |
| API 점검 | OpenAPI endpoint coverage 90% 이상 | spec 대비 호출 결과 |
| 처리 시간 | staging scan 60분 이하 | CI/CD duration |

> 요약: DAST 성공 여부는 critical 차단, 인증 탐색 범위, API 커버리지, 스캔 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. OWASP ZAP, Burp Suite Enterprise, Arachni 등을 staging pipeline에 연결하고 release gate에서 critical 취약점 0건을 조건으로 설정함.
2. 테스트 계정, seed URL, OpenAPI 명세, JWT refresh 절차를 제공해 인증 화면과 API 커버리지를 80~90% 이상으로 유지함.
3. 운영 데이터 복제 금지, 결제·메일·외부 연동 mock 처리, rate limit 설정으로 스캔 중 부작용을 차단함.

**결론 (2줄):**
- 기술사 판단: 웹·API 런타임 취약점과 배포 설정 검증이 목적이면 DAST를 staging gate에 배치하고, 코드 흐름 결함은 SAST로 병행함.
- 향후 방향: DAST는 API 보안 테스트, IAST, 인증 자동화, CI/CD evidence 관리와 결합해 릴리스 보안 통제로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DAST를 설명하시오", "기술하시오" | 인증 크롤링, 공격 요청, evidence 분석 흐름 | SAST와 차이, black-box 특성 |
| 요구사항 명시형 | "보안 검증 방안을 제시하시오", "비교하시오" | staging gate, API scan, false negative 대응 | SAST·DAST 조합과 release 차단 기준 |

> 요약: 설명형은 실행 앱 공격 원리를, 방안형은 staging 게이트와 인증·API 커버리지 확보를 중심으로 전개한다.
