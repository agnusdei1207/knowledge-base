---
title: "카나리 배포·블루-그린 배포 (Canary Blue-Green Deployment)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 70
---

# 📖 【암기용】 개념 완전 이해

> 목적: 카나리 배포와 블루-그린 배포를 점진 출시와 병렬 환경 전환 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 운영 배포 위험을 줄이기 위한 점진 트래픽 전환과 병렬 환경 전환 기법
- **왜 필요한가**: 한 번에 전체 사용자에게 새 버전을 배포하면 결함 발생 시 영향 범위가 100%가 됨. 카나리와 블루-그린은 영향 범위를 제한하고 빠른 복귀 경로를 제공함.
- **핵심 직관**: 새 식당 메뉴를 일부 손님에게 먼저 내보거나, 같은 매장을 하나 더 준비해 문을 바꿔 여는 방식임.

## 깊이 이해
- **배경·문제의식**: 무중단 배포가 요구되는 서비스에서는 릴리스 실패가 매출과 SLA 위반으로 이어짐. 특히 DB 스키마, 캐시, 외부 API 변경은 롤백을 어렵게 만듦.
- **작동 원리**: 카나리는 새 버전에 1%, 5%, 25%, 50%, 100%처럼 트래픽을 단계적으로 보냄. 블루-그린은 Blue 운영 환경과 Green 신규 환경을 병렬로 두고 검증 후 라우팅을 전환함.
- **비유**: 카나리는 시식 코너 확대, 블루-그린은 대체 매장을 준비한 뒤 간판을 바꾸는 방식임.
- **구체 예시**: Kubernetes에서 Argo Rollouts가 5% 트래픽을 v2 pod로 보내고 p95 latency 300ms 이하, error rate 1% 이하일 때 다음 단계로 진행함.
- **흔한 오해·주의점**: 애플리케이션 롤백만 준비해도 충분하지 않음. DB migration은 expand-contract, backward compatibility, feature flag를 함께 설계해야 함.

## 연결 개념
- Progressive Delivery: 지표 기반 점진 배포와 자동 중단
- Feature Flag: 기능 노출을 코드 배포와 분리
- DB Migration: 롤백 가능한 스키마 변경 전략

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 카나리와 블루-그린은 배포 방식 이름보다 traffic shifting, metric gate, rollback, DB migration 호환성이 판단 핵심임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 카나리는 일부 트래픽부터 점진 전환하고, 블루-그린은 두 환경을 병렬 운영한 뒤 라우팅을 일괄 전환하는 배포 전략임.
> 2. **가치**: 장애 영향 범위를 1~5% 초기 사용자로 제한하거나 병렬 환경 복귀로 MTTR 10분 이하를 목표로 함.
> 3. **판단 포인트**: metric gate, 자동 rollback, 세션·캐시·DB 호환성, 비용을 비교해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 배포 전략 차이 확인 | canary traffic shifting vs blue-green switch | 무중단 배포로만 일반화 |
| 운영 위험 통제 확인 | rollback, metric gate, SLO | DB migration과 상태 저장 문제 누락 |
| 적용 기준 판단 확인 | 사용자 영향, 인프라 비용, 관측성 | 한 전략이 항상 우월하다고 단정 |

> 요약: 이 문제는 배포 전환 방식과 실패 시 복구 조건을 지표 기반으로 비교해야 한다.

---

## Ⅰ. 개요 및 필요성

카나리 배포와 블루-그린 배포는 운영 중 신규 버전을 배포할 때 장애 영향과 복구 시간을 줄이는 릴리스 전략이다. 전체 배포는 결함 발생 시 사용자 100%에 영향을 주므로 점진 전환 또는 병렬 환경 전환이 필요하다. 배포 성공 여부는 error rate, latency, rollback time으로 판단한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Traffic -> Router/Load Balancer
  / Canary: v1 95% / v2 5% -> Metric Gate -> Increase/Rollback
  / Blue-Green: Blue Active / Green Standby -> Switch -> Blue Rollback
DB/Cache/Session -> Compatibility Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Traffic Router | 트래픽 비율 또는 환경 전환 | Ingress, service mesh, LB |
| Metric Gate | 지연, 오류, 비즈니스 지표 판정 | p95, 5xx, conversion |
| Rollback Path | 이전 버전 또는 환경 복귀 | 10분 이하 목표 |
| Data Compatibility | DB, cache, session 호환 | expand-contract migration |

> 요약: 배포 구조는 라우팅, 지표 판정, 롤백 경로, 데이터 호환성을 함께 갖춰야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
신규 버전 배포 -> Smoke Test -> Traffic Shift/Switch
-> Metric Collect -> Gate Decision
-> Continue/Promote 또는 Rollback
-> DB Migration 후속 정리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | v2 배포와 smoke test 수행 | readiness 100% |
| 2 | 카나리 1~5% 또는 Green 환경 검증 | error rate 1% 이하 |
| 3 | p95 latency, 5xx, 핵심 KPI 수집 | p95 300ms 이하 |
| 4 | gate 통과 시 전환 확대 또는 switch | 단계별 승인 기록 |
| 5 | 실패 시 rollback, 성공 시 old 정리 | rollback 10분 이하 |

> 요약: 배포는 신규 버전 검증, 트래픽 전환, 지표 판정, 롤백 또는 승격 순서로 진행된다.

---

## Ⅳ. 특징

| 구분 | 카나리 배포 | 블루-그린 배포 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 전환 방식 | 1%, 5%, 25%, 100% 단계 증가 | Blue에서 Green으로 일괄 switch | 사용자 영향 범위 vs 복구 단순성 |
| 인프라 비용 | 기존 환경에 일부 v2 추가 | 전체 환경 2벌 필요 | 비용 약 2배 가능 |
| 검증 | 실제 사용자 일부 관측 | 전환 전 Green 검증 | telemetry와 synthetic test |
| 롤백 | 트래픽 비율 0%로 축소 | Blue로 라우팅 복귀 | DB 호환성 없으면 복구 제한 |

> 요약: 카나리는 영향 범위 제어에 유리하고 블루-그린은 환경 전환과 복귀가 단순하나 비용과 데이터 호환성 검토가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Rolling update | Canary/Blue-Green | SLO 99.9%, 무중단 요구 |
| 비용/성능 | 단일 환경 | 병렬 환경 또는 부분 트래픽 | 비용 2배 허용 여부 |
| 운영/위험 | 전체 영향 가능 | 영향 범위 제한, 즉시 복귀 | error budget 작은 서비스 |
| 데이터 | 단순 schema 변경 | backward compatible migration | DB 변경 포함 시 expand-contract |

> 요약: 선택 기준은 사용자 영향 허용치, 인프라 비용, 관측성 수준, DB 호환성이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지표 없는 전환 | 관측성 부재 | metric gate, alert 자동화 | p95, 5xx, KPI 수집률 100% |
| DB 롤백 실패 | 비호환 schema 변경 | expand-contract, dual write 검토 | backward test 100% |
| 세션 불일치 | 상태 저장 서버 | sticky session, external session store | session error 0건 |
| 비용 증가 | 환경 2벌 유지 | TTL, 자동 scale down | Green idle cost 추적 |

> 요약: 배포 리스크는 지표 부재, DB 비호환, 세션 상태, 비용이며 사전 검증과 자동 gate로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 오류율 | 5xx error rate 1% 이하 | APM, ingress metrics |
| 지연시간 | p95 latency 300ms 이하 | Prometheus, tracing |
| 복구 시간 | rollback 10분 이하 | deployment log |
| 데이터 호환 | backward compatibility 100% | migration test |

> 요약: 배포 성공은 오류율, 지연시간, 복구 시간, 데이터 호환성 기준을 모두 통과해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Argo Rollouts, Flagger, Istio를 사용해 5%, 25%, 50%, 100% 카나리 단계를 구성하고 error rate 1% 초과 시 자동 rollback을 설정함.
2. 블루-그린은 Green 환경 smoke test 후 DNS/LB switch를 수행하고 Blue 환경은 30분 보존해 rollback 10분 이하를 확보함.
3. DB 변경은 expand-contract, nullable column, dual-read 전략으로 backward compatibility를 보장하고 destructive migration은 배포 안정화 후 수행함.

**결론 (2줄):**
- 기술사 판단: 사용자 영향 최소화가 우선이면 카나리, 즉시 환경 복귀와 검증 환경 분리가 우선이면 블루-그린을 선택함.
- 향후 방향: 두 전략은 feature flag, SLO metric gate, progressive delivery와 결합해 자동 릴리스 의사결정으로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "카나리와 블루-그린 배포를 설명하시오" | 전환, 지표 수집, rollback 흐름 | traffic shifting과 parallel environment 비교 |
| 요구사항 명시형 | "비교하시오", "무중단 배포 방안을 제시하시오" | metric gate, DB migration, rollback 절차 | 선택 기준, 비용, 세션·데이터 리스크 |

> 요약: 설명형은 배포 원리를, 비교·방안형은 지표 gate와 데이터 호환성 중심으로 목차를 전환한다.
