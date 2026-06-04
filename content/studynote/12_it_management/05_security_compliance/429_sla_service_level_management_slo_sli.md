---
title: "429. SLA 서비스 수준 관리 SLO SLI (SLA Service Level Management SLO SLI)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SLI(Service Level Indicator, 서비스 수준 지표)·SLO(Service Level Objective, 서비스 수준 목표)·SLA(Service Level Agreement, 서비스 수준 합의)는 **측정 가능한 지표 -> 목표치 -> 외부 계약**으로 이어지는 신뢰성 공학적 3계층 구조이며, Google SRE에서 정형화된 Error Budget(에러 예산)이 이를 코드 변경 속도와 직접 연결한다.
> 2. **가치**: 정량적 가용성(예: 99.95% = 월 21.9분 장애 허용)을 통해 클라우드 SLA 시 **최대 30~100% 서비스 크레딧(SC)** 환급을 자동화하고, MTTR(평균 복구 시간)을 40% 이상 단축하며, CapEx/OpEx 대비 ROI를 사후 측정이 아닌 사전 보장 형태로 전환한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **"SLO를 얼마나 빡빡하게(SLO = 99.99% vs 99.9%)"**, **"SLI를 사용자 관점 vs 시스템 관점 중 어디에서"**, **"Error Budget을 Burn Rate로 어느 빈도로"** 측정하느냐이며, 이는 곧 인프라 비용 곡선과 직결된다(99.9% -> 99.99%만 해도 인프라 비용이 10배 이상 증가).

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 시스템이 **모놀리식 -> SOA -> 마이크로서비스 -> 클라우드 네이티브(K8s, MSA, Serverless)**로 진화함에 따라, 서비스 간 의존성 그래프가 1:N에서 N:M으로 폭증하면서 "시스템이 살아있는가"라는 단순 가용성 개념만으로는 비즈니스 임팩트를 표현할 수 없게 되었다. 전통적 ITIL 기반의 **인시던트 관리(MTTR, MTBF)** 중심 운영은 "장애 발생 후 사후 복구"에 머물렀고, AWS·GCP 같은 하이퍼스케일러가 99.99% 가용성을 표준화하면서 **"장애가 나기 전에 신뢰성을 정량적 계약으로 정의"**하는 SRE(Site Reliability Engineering) 패러다임이 등장했다. Google은 2016년 《Site Reliability Engineering》을 공개하며 SLI/SLO/Error Budget 체계를 코드와 동일하게 1급 시민(first-class citizen)으로 다루기 시작했다.

```text
  +------------------------------------------------------------------+
  |      SLA 관리 패러다임의 진화 (전통적 -> SRE 기반)               |
  +------------------------------------------------------------------+
  |                                                                  |
  |  [전통적 ITIL 운영]              [SRE 기반 SLA 관리]             |
  |  +---------------+              +-----------------------+        |
  |  | SLA 문서(Word)|              | SLI/SLO(SLO as Code) |        |
  |  | 분기별 보고   |              | Prometheus + Alert   |        |
  |  | 사후 분석     |              | Error Budget Burn    |        |
  |  | MTTR 추적     |              | Multi-Window/Multi-  |        |
  |  |               |              | Burn-Rate (MWMB)     |        |
  |  +-------+-------+              +-----+-------------+---+        |
  |          |                            |             |            |
  |          v                            v             v            |
  |  "장애 후 보고"               "신뢰성 = 제품 기능"             |
  |  정성적 (느낌)                정량적 (수치·예산·알림)           |
  |                                                                  |
  |  변화 트리거:                                                     |
  |   • 클라우드 SLA = 자동 환불 -> 정량화 불가피                     |
  |   • MSA -> N:M 의존성 -> 시스템 가용성 ≠ 사용자 경험              |
  |   • CD/데브옵스 -> 배포 빈도 ^ -> 안정성·속도 균형 필요           |
  +------------------------------------------------------------------+
```

핵심 필요성은 다음 3가지로 요약된다. 첫째, **계약적 책임(Accountability)**: CSP(Cloud Service Provider)의 가용성 99.9%는 고객사 SLO 99.95% 산정 시 직렬 가용성 공식 `1 - (1-0.999)(1-0.999)=99.9999%`처럼 합성 가용성을 계산해야 하고, 이를 위해선 SLI 정의가 필수다. 둘째, **비용 최적화**: 9가 두 개 추가될 때마다 인프라 비용은 기하급수적으로 증가하므로(예: 99.9% vs 99.99%, 3배~10배 DB 복제 비용), 비즈니스 임팩트가 낮은 워크로드는 낮은 SLO로 두는 **Tiered SLO 전략**이 필요하다. 셋째, **엔지니어링 문화**: Error Budget이 0이 되면 코드 변경을 동결(freeze)하는 규칙은, 운영팀과 개발팀 간 신뢰를 코드 레벨에서 자동화한다.

- **📢 섹션 요약 비유**: SLA 관리는 **"자동차 보험 + 자동차 검사 + 운전 점수"**를 합친 것과 같다. 보험 계약(SLA)이 정량적 보상(환급)을 약속하고, 검사(SLI)가 수치를 측정하며, 운전 점수(Error Budget)가 마이너스면 즉시 면허 정지(배포 동결)되는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SRE의 신뢰성 관리 아키텍처는 **측정(Instrumentation) -> 수집(Collection) -> 분석(Analytics) -> 행동(Action)**의 4계층으로 구성된다. SLI는 ① 가용성(Availability), ② 지연 시간(Latency), ③ 처리량(Throughput), ④ 정확성(Correctness), ⑤ 내구성(Durability) 등 **사용자 접점(用户 접점, User Journey) 단위**로 정의되며, 일반적으로 **좋은 이벤트(good event) / 유효 이벤트(valid event)**의 비율로 표현된다. 예: `SLI = successful_requests / total_requests` 또는 `SLI = requests_under_300ms / total_requests`.

```text
  +------------------------------------------------------------------+
  |          SRE 신뢰성 관리 4계층 아키텍처 (End-to-End)              |
  +------------------------------------------------------------------+
  |                                                                  |
  |  [1] 측정 계층 (Instrumentation)                                 |
  |   +----------+  +----------+  +----------+  +----------+         |
  |   | App SDK  |  | LB/Proxy |  | K8s      |  | Sidecar  |         |
  |   |(OpenTel) |  |(Envoy)   |  |(cAdvisor)|  |(Istio)   |         |
  |   +-----+----+  +-----+----+  +-----+----+  +-----+----+         |
  |         |             |             |             |              |
  |         v             v             v             v              |
  |  [2] 수집 계층 (Collection)                                     |
  |   +----------+  +----------+  +----------+                       |
  |   |Prometheus|  |Fluentbit |  |Tempo/Jaeger|                     |
  |   |(Metrics) |  |(Logs)    |  |(Traces)   |                     |
  |   +-----+----+  +-----+----+  +-----+----+                       |
  |         +------+------+------+------+                            |
  |                v             v                                   |
  |  [3] 분석 계층 (Analytics)                                       |
  |   +-----------------+  +------------------+                      |
  |   | SLO Evaluator   |  | Burn-Rate Engine |                      |
  |   | (Sloth/Pyrra)   |  | (Multi-Window)   |                      |
  |   +--------+--------+  +--------+---------+                      |
  |            |                    |                                |
  |            v                    v                                |
  |  [4] 행동 계층 (Action)                                          |
  |   +--------------+  +--------------+  +--------------+           |
  |   | Alertmanager |  | Error Budget |  | CD Gate      |           |
  |   |(PagerDuty)   |  | Tracker      |  |(Argo Rollouts|           |
  |   |              |  |(GitLab)      |  |/SLO Block)   |           |
  |   +--------------+  +--------------+  +--------------+           |
  +------------------------------------------------------------------+
```

SLO 산정 시 가장 중요한 공식은 **Error Budget**이다. `Error Budget = 1 - SLO`, 즉 SLO가 99.9%라면 0.1%(=월 43.2분)가 허용 오차다. 이를 시간 윈도우(28일 롤링, 30일 캘린더 등)로 환산하면 1일 허용 오차 = 4.32분, 1시간 = 0.18분이 된다. Google SRE Workbook은 **Multi-Window Multi-Burn-Rate(MWMB)** 알림 전략을 권장하는데, 이는 ① 단기 빠른 알림(1시간 윈도우에서 14.4× 소비) + ② 중기 알림(6시간 윈도우에서 6× 소비) 2개 조합으로 페이저 피로 없이 빠르게 감지한다.

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SLI** (Service Level Indicator) | 사용자 관점의 정량적 측정값 | `good_events / valid_events` 비율; Ex: `http_requests_total{status!~"5.."} / http_requests_total`; 카디널리티 관리를 위해 Histogram Bucket(예: 50ms, 100ms, 300ms, 1s) 단위로 분포 측정 |
| **SLO** (Service Level Objective) | 내부 목표치(공식 선언) | OpenSLO/SLO Spec YAML로 선언; Sloth/Pyrra가 Prometheus Rule로 자동 변환; 예: `slo: 99.9 over 30d` + `burnrate: 14.4x over 1h` |
| **SLA** (Service Level Agreement) | 외부 고객과 계약, 미달 시 보상 | CSP 가용성(예: AWS EC2 99.99%, RDS Multi-AZ 99.95%) + 자체 SLA; 위반 시 SC(Service Credit, 통상 10~30% 환불) 자동 발급 |
| **Error Budget** | SLO 잔여 허용 오차의 화폐 단위 | `Budget = Window × (1 - SLO/100)`; 0이 되면 **기능 동결(Feature Freeze)** 정책 자동화(Argo CD Sync Window, OPA Gatekeeper) |
| **Burn-Rate Alert** | 예산 소진 속도 기반 알림 | MWMB: `(errors_now / allowed_errors) / window_size` ≥ 임계치 시 page; 예: 1h burnrate 14.4x -> 1일 만에 60% 예산 소진 예측 |
| **SLI/SLO Registry** | SLO 카탈로그 중앙 관리 | Backstage SLO Plugin, Nobl9, Datadog SLO Management; SLO를 코드로 관리(PR 리뷰, GitOps) |
| **Observability Backend** | 측정 데이터 저장·분석 | Prometheus + Cortex/Thanos(장기 저장), Grafana Mimir, VictoriaMetrics, Honeycomb, Lightstep |

핵심 알고리즘: **Burn-Rate = (실제 오류율 / 허용 오류율)**. SLO 99.9%(30일)에서 1시간 burnrate 14.4×가 발생하면, 그 1시간 동안 발생한 오류가 정상 시 1시간 허용 오류의 14.4배라는 의미. 30일 예산 0.1% × 30일 × 24시간 = 0.1% × 720h = 0.72h 분량인데, 14.4× × 1h = 14.4h분이 단일 시간에 소진. 이는 곧 14.4h / 0.72h = 20% 예산을 1시간 만에 태운 것이므로 즉시 페이지 발송. SLO 99.99%에서는 1h burnrate 36×가 위험 임계치(2.4% 예산 소진)가 된다.

- **📢 섹션 요약 비유**: SLI는 **"체온계"**, SLO는 **"정상 체온 범위(36.5±0.5℃)"**, Error Budget는 **"오늘 허용되는 열 쏠림 횟수"**, Burn-Rate는 **"분당 열이 오르는 속도"**와 같다. 속도가 임계치 넘으면 바로 병원으로(페이지), 누적 허용량 다 쓰면 외출 금지(배포 동결).

---

## Ⅲ. 비교 및 연결

SLA/SLO/SLI는 서로 혼용되지만 명확한 책임 소재가 다르며, 동시에 ITIL/COBIT/ISO 20000 같은 거버넌스 프레임워크와 상호 보완 관계에 있다. 또한 SRE의 Error Budget은 전통적 Change Management(변경 관리) 위원회의 **"사람 기반 승인"**을 **"데이터 기반 자동 승인"**으로 대체한다.

| 구분 | SLA (Service Level Agreement) | SLO (Service Level Objective) | SLI (Service Level Indicator) |
| :--- | :--- | :--- | :--- |
| **대상** | 외부 고객(법적·상업적 계약) | 내부 엔지니어링(목표치) | 시스템·사용자 접점(측정값) |
| **책임** | 경영·법무·영업 | SRE·플랫폼팀 | 개발·운영 |
| **수치 예시** | "가용성 99.9% 미달 시 월 10% 환불" | "30일 롤링 99.9% SLO, 0.1% 에러 예산" | "HTTP 200 응답 / 전체 요청" |
| **위반 시** | Service Credit 환급, 손해배상 | Feature Freeze, Pager 에스컬레이션 | (자체로는 의미 없음) |
| **변경 빈도** | 분기~연 단위(계약 갱신) | 코드 PR 단위(점진적 조정) | 상시(실시간 측정) |
| **문서 형태** | PDF 계약서, MSA 부속서 | YAML/JSON(OpenSLO spec) | Prometheus/Grafana 대시보드 |
| **포함 관계** | SLO ≥ SLA (내부 목표 ≥ 외부 약속) | SLO ⊃ SLI (목표 ⊃ 지표) | SLI ⊂ SLO (지표가 목표의 근간) |

다른 프레임워크와의 연결: **ITIL 4**의 "Service Level Management" 프로세스는 SLO/SLI 개념을 포괄하지만, **Error Budget처럼 배포 속도와 직접 연결**시키지는 않는다. **ISO/IEC 20000**은 SLA 템플릿과 변경 관리 프로세스를 강조하지만 측정 자동화는 약하다. **COBIT 2019**의 EDM(평가, 지시, 모니터링) 계층은 SLO 리포팅을 거버넌스 측면에서 보완한다. **DevOps Research and Assessment(DORA) 4 Key Metrics**(배포 빈도, 리드 타임, 변경 실패율, 복구 시간)는 SLO를 코드 단위로 분해한 지표로 볼 수 있다. **AIOps** 도구(Datadog Watchdog, Dynatrace Davis, New Relic AI)는 SLI 이상 탐지를 머신러닝으로 자동화하여 수동 임계치 기반의 한계를 보완한다.

- **📢 섹션 요약 비유**: SLA는 **"손님에게 보여주는 메뉴판"**,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 429 / 800

<- **이전**: [428. 문제 관리 근본 원인 분석 RCA](/studynote/12_it_management/05_security_compliance/428_problem_management_root_cause_analysis/)
**다음**: [430. 지식 관리 KMS 조직 학습 체계](/studynote/12_it_management/05_security_compliance/430_knowledge_management_kms_learning_system/) ->

---
