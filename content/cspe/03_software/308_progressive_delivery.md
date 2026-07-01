---
title: "프로그레시브 딜리버리 (Progressive Delivery)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 308
---

# 📖 【암기용】 개념 완전 이해

> 목적: 프로그레시브 딜리버리를 처음 봐도 배포 후 점진 공개와 자동 검증의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 새 버전을 사용자·트래픽 비율별로 단계 공개하고 지표 기준에 따라 확대·중단하는 전달 방식
- **왜 필요한가**: 전체 사용자에게 한 번에 배포하면 결함 발견 시 장애 범위가 커지므로 작은 비율에서 검증 후 확대해야 함
- **핵심 직관**: 신약 임상처럼 소수 대상에서 이상 반응을 확인하고 단계적으로 대상을 늘리는 방식임

## 깊이 이해
- **배경·문제의식**: CI/CD가 배포 빈도를 높였지만, 배포 성공이 사용자 품질을 보장하지는 않음. 새 버전은 오류율, 지연시간, 비즈니스 지표를 확인하며 점진 노출해야 함.
- **작동 원리**: Canary, Blue/Green, Feature Flag, Traffic Split을 사용해 1%, 5%, 25%, 50%, 100%로 확대함. 자동 분석이 SLO와 guardrail을 확인하고 실패 시 rollback함.
- **비유**: 새 교통 체계를 전 도시가 아니라 한 구역에서 먼저 시행하고 사고율과 통행 시간을 본 뒤 확대하는 방식임.
- **구체 예시**: 결제 서비스 v2를 5% 트래픽에 배포하고 30분간 5xx 0.1% 이하, p95 300ms 이하, 결제 성공률 감소 0.5%p 이내일 때 25%로 확대함.
- **흔한 오해·주의점**: Canary 배포만으로는 충분하지 않음. 지표 기준, 자동 중단, 관측성, 롤백 절차가 있어야 Progressive Delivery임.

## 연결 개념
- Canary Release: 소량 트래픽 대상 신규 버전 검증
- Feature Toggle: 기능 단위 공개 제어
- SLO: 확대·중단을 결정하는 품질 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. Progressive Delivery는 배포 전략 나열이 아니라 지표 기반 자동 확대·중단 판단으로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Progressive Delivery는 새 버전을 트래픽·사용자 비율별로 점진 노출하고 관측 지표로 확대·중단을 자동 결정하는 릴리스 방식이다.
> 2. **가치**: 배포와 공개를 분리해 장애 반경을 제한하고, SLO 기반으로 롤백 판단을 표준화한다.
> 3. **판단 포인트**: 트래픽 분할, 지표 수집, 자동 분석, 롤백 시간이 모두 설계되어야 단순 Canary와 구분된다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 릴리스 전략 이해 확인 | Canary, Blue/Green, Feature Flag, Traffic Split | Canary만 설명하고 자동 분석 누락 |
| 운영 품질 판단 확인 | 오류율, p95, 비즈니스 지표, SLO | 배포 성공률만 지표로 제시 |
| 자동화·롤백 역량 확인 | Analysis, Promotion, Rollback | 수동 승인만으로 마무리 |

> 요약: 이 문제는 새 버전을 어떻게 조금씩 노출하고 어떤 기준으로 중단할지 묻는다.

---

## Ⅰ. 개요 및 필요성

Progressive Delivery는 신규 버전을 단계적으로 공개하는 릴리스 방식이다. 전체 배포는 결함 발생 시 사용자 영향이 크며 원인 추적 시간이 길어짐. 트래픽 비율과 SLO 기준으로 자동 확대·중단해 장애 반경과 롤백 시간을 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Developer -> CI/CD -> Delivery Controller -> Traffic Router -> Stable/Canary -> Observability
  / Feature Flag
  / SLO Analysis
  / Rollback
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Delivery Controller | 배포 단계와 승격 정책 제어 | Argo Rollouts, Flagger |
| Traffic Router | 트래픽 비율 분할 | Ingress, Service Mesh |
| Observability | 오류·지연·비즈니스 지표 수집 | Prometheus, APM, 로그 |
| Feature Flag | 사용자·기능 단위 공개 | 코드 배포와 공개 분리 |

> 요약: Controller가 트래픽을 나누고 Observability 지표를 판단해 승격 또는 롤백을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
신규 버전 배포 -> 1% 노출 -> 지표 분석 -> 5% 확대 -> 지표 분석 -> 100% 승격 또는 롤백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Canary 버전 배포 | readiness, smoke test |
| 2 | 소량 트래픽 분배 | 1% 또는 내부 사용자 |
| 3 | 자동 분석 | 5xx, p95, error budget |
| 4 | 단계 확대 | 5%, 25%, 50%, 100% |
| 5 | 승격·롤백 | SLO 위반 시 5분 이내 rollback |

> 요약: Progressive Delivery는 소량 노출과 지표 분석을 반복하며 조건 충족 시 승격하고 위반 시 롤백한다.

---

## Ⅳ. 특징

| 구분 | 전통 배포 | Progressive Delivery | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 공개 범위 | 전체 즉시 공개 | 1%부터 단계 공개 | 장애 반경 제한 |
| 판단 기준 | 배포 성공 | SLO·비즈니스 지표 | 5xx 0.1%, p95 300ms |
| 롤백 | 수동 재배포 | 자동 rollback | MTTR 10분 이하 |
| 실험 | 별도 분석 | Flag·Canary 연계 | 전환율 변화 0.5%p |

> 요약: Progressive Delivery는 배포 완료보다 사용자 지표를 기준으로 릴리스 승격 여부를 판단한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Blue/Green | 즉시 전체 전환 | 단계별 트래픽 전환 | 사용자 영향 최소화 필요 |
| Canary | 소량 검증 | 자동 분석·승격 포함 | SLO 기반 자동화 필요 |
| Feature Flag | 기능 공개 제어 | 배포·트래픽·기능 통합 | 사용자군별 점진 공개 |

> 요약: Progressive Delivery는 Canary, Blue/Green, Feature Flag를 지표 기반 승격 절차로 묶는 상위 운영 방식이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 승격 | 지표 부족 | guardrail metric, 최소 관측 시간 | false promotion 건수 |
| 트래픽 불균형 | 세션 고정·캐시 영향 | consistent hashing, header routing | canary traffic 오차 1%p 이하 |
| 롤백 실패 | DB 변경 비호환 | backward compatible schema | rollback success rate |

> 요약: 지표 설계, 트래픽 분배, 스키마 호환성이 Progressive Delivery의 핵심 리스크이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 품질 | 5xx 0.1% 이하, p95 300ms 이하 | Prometheus, APM |
| 롤백 | 5분 이내 자동 rollback | CD 로그 |
| 트래픽 | 설정 비율 대비 오차 1%p 이하 | Ingress, mesh metric |

> 요약: 품질, 롤백 시간, 트래픽 분배 정확도가 릴리스 성공 기준이다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. Argo Rollouts 또는 Flagger로 1%, 5%, 25%, 50%, 100% 승격 단계를 정의하고 각 단계 최소 관측 시간을 30분으로 설정함.
2. 승격 조건은 5xx 0.1% 이하, p95 300ms 이하, 핵심 전환율 하락 0.5%p 이내로 정의함.
3. DB 변경은 expand-contract, backward compatible API, feature flag off 경로를 준비해 rollback success rate 100%를 목표로 함.

**결론 (2줄):**
- 기술사 판단: 사용자 영향이 큰 서비스와 배포 빈도가 높은 조직은 Progressive Delivery, 내부 배치성 서비스는 Blue/Green 또는 Rolling Update로 충분함.
- 향후 방향: 릴리스 판단은 SLO와 비즈니스 guardrail을 결합한 자동 분석, AIOps 기반 이상 탐지와 연결됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Progressive Delivery를 설명하시오" | 단계 노출·자동 분석 흐름 | 기존 배포 전략 대비 특징 |
| 요구사항 명시형 | "무중단 배포 방안을 제시하시오" | 트래픽 분할·SLO·롤백 절차 | 리스크와 자동 승격 기준 |

> 요약: 설명형은 릴리스 개념, 방안형은 SLO 기반 승격·중단 자동화를 중심으로 작성한다.
