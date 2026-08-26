---
sidebar:
  order: 15
  label: "015. SLO•SLI (Service Level Objective•Indicator)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "사이트 신뢰성 공학(SRE) 품질 지표 및 목표 거버넌스 : SLI 및 SLO (Google SRE & CUJ 기반)"
date: "2026-08-26T15:31:14+09:00"
tags:
  - "notes-evaluation"
weight: 15
extra:
  question_no: "015"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 50
  priority_note: "137회·138회 연속 출제, Google SRE(Site Reliability Engineering) 핵심 신뢰성 지표, 서비스 수준 지표(SLI: Service Level Indicator, SLI=Good Events / Valid Total Events), 서비스 수준 목표(SLO: Service Level Objective), 핵심 사용자 여정(CUJ: Critical User Journey), 이동 측정 창(Rolling Window), 다중 윈도우 다중 번레이트(Multi-Window Multi-Burn-Rate) 경보"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **서비스 수준 지표 및 목표(SLI & SLO / Google Site Reliability Engineering)**:
  - **SLI (Service Level Indicator)**: 서비스가 제공하는 품질의 수준을 사용자 관점에서 정량적으로 계측한 실측 비율 ($\text{SLI} = \frac{\text{Good Events (성공/정상 지연 이벤트 수)}}{\text{Valid Total Events (유효 전체 이벤트 수)}} \times 100\%$).
  - **SLO (Service Level Objective)**: 개발팀(Dev)과 운영팀(SRE)이 시스템의 안정성과 출시 속도의 균형을 맞추기 위해 내부적으로 합의한 정량적 목표 기준선 (예: "30일 이동 창 동안 결제 요청의 99.9%가 500ms 이내에 완료되어야 함").
- **인프라 중심 모니터링 및 주관적 품질 판단 결함(Host-centric & Subjective Reliability Defect)**: 서버 CPU 80% 가동률 같은 단순 하드웨어 지표에만 매몰되어 실제 사용자 결제 실패나 화면 멈춤을 조기에 감지하지 못하고, 개발팀의 신규 배포 요구와 운영팀의 변경 거부 간의 소모적 갈등을 유발하는 구조적 결함.

</details>

- 정의/개념: 데이터 기반의 신뢰성 거버넌스를 확립하기 위해 **핵심 사용자 여정(CUJ) 정의 $\rightarrow$ 좋은 이벤트(Good Events) 기준 수립 $\rightarrow$ 이동 측정 창(Rolling Window) 기반 SLI 산출 $\rightarrow$ 에러 예산($1-\text{SLO}$) 연계 내부 목표(SLO) 설정 $\rightarrow$ 번레이트(Burn Rate) 기반 배포 통제** 를 집행하는 **SRE 정량 품질 관리 체계**
- 배경/필요성: 100% 목표로는 **배포 속도·안정성** 균형 불가

#### 한줄 요약
- SLI는 사용자 관점의 품질 실측치이고, SLO는 에러 예산과 연계된 내부 엔지니어링 목표 기준선이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SLI/SLO 3대 핵심 설계 원칙**:
  - **사용자 중심주의 (User-Centric / CUJ)**: 백엔드 서버 상태가 아닌 실제 사용자가 겪는 체감 품질(성공률, 지연시간)을 측정.
  - **단순하고 명확한 이벤트 비율 (Good / Total)**: 모든 SLI를 $0\% \sim 100\%$ 범위의 백분율 비율 공식으로 통일.
  - **이동 측정 창 (Rolling Time Window)**: 고정된 월초~월말이 아닌 최근 7일, 28일, 30일간의 연속된 기간을 슬라이딩 윈도우로 평가.

</details>

- 성공·지연 준수 비율에 기반한 **SLI 수식화**
- SLO에서 허용 실패량을 구하는 **에러 예산**
- 급격·완만한 소진을 잡는 **다중 윈도우 번레이트**

#### 한줄 요약
- 사용자 중심 CUJ 계측, Good/Total 백분율 공식, 이동 측정 창, 에러 예산 및 번레이트 연계를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SLI & SLO 4대 아키텍처 계층**:
  1. **CUJ Layer**: 핵심 사용자 여정(로그인, 상품 검색, 장바구니, 결제 승인) 식별.
  2. **SLI Specification Layer**: 좋은 이벤트(Good), 유효 이벤트(Valid Total), 측정 위치 정의.
  3. **Aggregation & Window Layer**: Prometheus/Datadog 기반 30일 이동 집계 윈도우.
  4. **Governance & Decision Layer**: 잔여 에러 예산 산출, 배포 동결(Freeze) 또는 롤아웃 승인.

</details>

```text
SLI·SLO 관리 체계
├─ CUJ Layer
├─ SLI Specification Layer
├─ Aggregation·Window Layer
└─ Governance·Decision Layer
```

선의 의미: 사용자 여정에서 SLI를 측정하고 30일 이동 창에서 SLO 목표 및 에러 예산과 대조하여 배포 여부를 제어하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **CUJ Layer** | 사용자 핵심 여정과 측정 우선순위 정의 |
| **SLI Specification Layer** | Good·Valid Total·측정 위치 명세 |
| **Aggregation·Window Layer** | 이동 창에서 SLI 집계 |
| **Governance·Decision Layer** | 에러 예산에 따라 배포 승인·동결 |

#### 한줄 요약
- CUJ 여정 정의, 가용성/지연시간 SLI 수식, SLO 목표치, 에러 예산 및 배포 거버넌스로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SLI/SLO 수립 및 운영 5단계 수명주기**:
  1. 핵심 사용자 여정(CUJ: 주문 결제) 및 측정 지점(API Gateway) 선정
  2. 좋은 이벤트 기준(HTTP 5xx 미발생 및 응답시간 300ms 이하) 명세화
  3. 최근 30일 이동 창 기반으로 실측 SLI 데이터베이스 집계
  4. 과거 데이터와 비즈니스 요구를 반영하여 SLO 목표치(99.9%) 확정
  5. 일일 에러 예산 소진율(Burn Rate)을 감시하여 배포 승인 또는 동결 집행

</details>

```text
1. [CUJ 식별 및 측정 지점 설정]
    ├─ 핵심 여정: 이커머스 장바구니 결제 API (`POST /api/v1/checkout`)
    └─ [측정 위치: 클라이언트 직전 로드밸런서(Ingress Gateway) 로그 채택]
            │
            ▼
2. [SLI 판정 공식 정의]
    ├─ 분모(Valid Total): 봇 및 정기 헬스체크를 제외한 실제 결제 요청 건수
    ├─ 분자(Good Events): HTTP 상태 코드 500 미만 AND 지연시간 300ms 이하
    └─ [공식: $\text{SLI} = \frac{\text{Good Events}}{\text{Valid Total}} \times 100\%$]
            │
            ▼
3. [SLO 목표치 및 에러 예산 수립]
    ├─ 30일간 총 유입 예상량: 1,000만 건
    ├─ 합의된 목표: $\text{SLO} = 99.9\%$ (30일 이동 윈도우)
    └─ [허용 에러 예산: $1,000만 \times 0.1\% = 10,000\text{건}$의 실패 허용]
            │
            ▼
4. [실시간 모니터링 및 번레이트 감시]
    ├─ Prometheus 메트릭 수집 ➔ 현재 30일 SLI = 99.94% (양호)
    ├─ 신규 결제 모듈 배포 후 1시간 만에 500 에러 2,000건 발생
    └─ [1시간 번레이트 $\text{Burn Rate} = 14.4\times$ 초과 ➔ 긴급 페이저(Pager) 알람 발송]
            │
            ▼
5. [에러 예산 정책 집행]
    ├─ 1시간 만에 월간 에러 예산의 20% 소진 ➔ 신규 배포 즉시 차단(Rollback)
    ├─ 긴급 롤백 완료 후 에러 발생률 0% 복귀
    └─ [다음 1주일간 신규 기능 개발을 중단하고 결제 예외 처리 리팩토링 스프린트 집행]
```

**동작 원리**

1. **CUJ 식별 및 측정 지점 설정**: 사용자 경계 선택
2. **SLI 판정 공식 정의**: Good·Valid Total 기준 명세
3. **SLO 목표치 및 에러 예산 수립**: 허용 실패량 확정
4. **실시간 모니터링 및 번레이트 감시**: 소진 속도 탐지
5. **에러 예산 정책 집행**: 잔여량에 따라 배포 승인·동결

#### 한줄 요약
- CUJ 선정, SLI 수식 명세, SLO/에러 예산 수립, 번레이트 감시, 배포 제어 정책 집행 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **주요 SLI 지표 4대 유형 비교**:
  - 가용성 SLI (Availability): 요청 성공률 ($\frac{\text{Status} < 500}{\text{Total}}$).
  - 지연시간 SLI (Latency): 응답 시간 준수율 ($\frac{\text{Latency} \le T}{\text{Total}}$).
  - 품질 저하 SLI (Quality): 기능 저하(Graceful Degradation) 없는 완전 응답률.
  - 신선도 SLI (Freshness): 데이터 파이프라인의 실시간 동기화 지연 준수율.

</details>

| SLI 지표 유형 | Good Event 판정 기준 | 주요 측정 대상 시스템 | 핵심 사용자 경험 |
|:---|:---|:---|:---|
| **가용성 (Availability)**| HTTP 상태 코드가 5xx가 아닌 경우 | **웹 서버, API 게이트웨이, 결제 서버**| "서비스가 에러 없이 작동하는가?" |
| **지연시간 (Latency)** | 왕복 응답시간이 $T\text{ms}$ 이하인 경우 | **검색 엔진, 대화형 웹 화면, DB 쿼리**| "화면이 버벅거림 없이 빠른가?" |
| **처리율 (Throughput)** | 초당 처리 건수가 최소 기준 이상인 경우 | **비디오 스트리밍, 대용량 파일 다운로드**| "다운로드가 끊김 없이 전송되는가?" |
| **품질 (Quality)** | Fallback 응답이 아닌 온전한 데이터 반환 | **AI 추천 엔진, 개인화 배너 서버** | "임시 데이터가 아닌 정확한 결과인가?"|
| **신선도 (Freshness)** | 데이터 생성 후 DB 반영까지의 지연 $\le T$| **실시간 주가 파이프라인, 대시보드** | "지금 보는 데이터가 최신 정보인가?" |

#### 한줄 요약
- 가용성(성공률), 지연시간(응답 속도), 처리율(전송량), 품질(완전성), 신선도(최신성)로 분류된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SLI/SLO 실무 운영 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 클라이언트 유효성 검증 실패인 HTTP 4xx(400 Bad Request 등)를 에러로 합산하여 **사용자의 오입력으로 인해 SLO가 부당하게 위반되고 배포가 동결되는 결함 발생** | **분모는 전체 유효 요청으로 하되, 분자에서 4xx는 Good Event(서버 관점에서 정상 처리)로 분류하고 5xx 서버 에러만 Bad Event로 집계** | 사용자 오입력에 의한 지표 왜곡 100% 방지 |
| 단순 백엔드 WAS 서버 내부 로그만 측정하여 **앞단의 CDN 캐시 장애나 로드밸런서 SSL 핸드셰이크 지연을 전혀 감지하지 못하는 사각지대 발생** | **최종 사용자와 가장 가까운 Edge API Gateway 또는 RUM(Real User Monitoring) 브라우저 계측 지표를 최우선 SLI로 채택** | 실제 사용자 체감 품질 100% 반영 |
| SLO 목표치를 비현실적인 100%로 설정하여 **모든 에러 예산이 상시 0으로 유지되며 개발팀의 신규 기능 릴리스가 무기한 마비되는 경직성 발생** | **비즈니스 가치와 비용을 고려하여 현실적인 '포 나인(99.99%)' 이하로 목표를 수립하고, 에러 예산 정책을 팀 간 공식 협약으로 강제** | 개발 민첩성과 시스템 안정성의 완벽한 균형 달성 |

#### 한줄 요약
- 4xx 에러를 정상으로 분리하고, Edge Gateway에서 체감 품질을 측정하며, 현실적 SLO로 배포 유연성을 확보한다.

## Ⅶ. 결론

- **에러 예산**이 남으면 배포하고 소진되면 안정화 우선

#### 한줄 요약
- CUJ 기반의 SLI 실측과 에러 예산 연계 SLO 운영을 통해 개발 속도와 시스템 안정성의 균형을 완성한다.
