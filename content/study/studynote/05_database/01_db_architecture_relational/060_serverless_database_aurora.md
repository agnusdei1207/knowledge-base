+++
weight = 60
title = "60. 서버리스 데이터베이스 (Serverless DB) - Amazon Aurora Serverless 등 자동 확장 아키텍처"
date = "2026-04-10"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[206_serverless_cold_start|서버리스]] DB는 컴퓨팅 자원을 미리 고정하지 않고 필요할 때만 늘리고 줄이는 자동 확장형 [[002_database_definition|데이터베이스]]다.
> 2. **가치**: 수요가 들쑥날쑥한 [[090_service_kubernetes_network_load_balancing|서비스]]에서 비용을 줄이고, [[249_scaling_normalization_standardization|스케일링]] 부담을 크게 낮춘다.
> 3. **판단 포인트**: 스토리지와 컴퓨팅 분리, [[264_proxy_pattern_surrogate_access_control|프록시]] 계층, [[559_serverless_cold_start_mitigation|콜드 스타트]]와 지속 트래픽 적합성을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 클라우드 DB는 CPU와 메모리 크기를 먼저 정해야 했다. 트래픽이 없을 때는 낭비가 크고, 갑자기 늘면 즉시 대응이 어렵다.

[[206_serverless_cold_start|서버리스]] DB는 이런 문제를 풀기 위해 컴퓨팅을 탄력적으로 붙였다 떼고, 스토리지는 별도로 유지한다. [[390_aurora_serverless_quorum_write|Aurora]] Serverless가 대표적이다.

- **📢 섹션 요약 비유**: 자동차를 사는 대신 필요한 시간에만 기사와 차를 부르는 [[090_service_kubernetes_network_load_balancing|서비스]] 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 [[293_storage_compute_separation|스토리지와 컴퓨팅의 분리]]다. [[001_dikw_pyramid|데이터]]는 안정적으로 저장하고, 실행 노드는 부하에 맞춰 자동 조절한다.

```text
App
  ↓
Proxy / Router
  ↓
Compute Node (scale up/down)
  ↓
Shared Storage
```

| 계층 | 역할 |
| :-- | :-- |
| [[264_proxy_pattern_surrogate_access_control|Proxy]]/Router | 연결 유지와 요청 분배 |
| Compute Node | SQL 실행과 [[191_transaction_concept_states|트랜잭션]] 처리 |
| Shared Storage | [[001_dikw_pyramid|데이터]] 영구 저장 |

접속이 줄면 컴퓨팅은 0에 가깝게 내려가고, 트래픽이 몰리면 빠르게 노드를 늘린다. 그래서 [[206_serverless_cold_start|서버리스]] DB는 불규칙한 워크로드에 적합하다.

- **📢 섹션 요약 비유**: 창고는 그대로 두고, 계산대 인원만 손님 수에 따라 늘리는 가게다.

---

## Ⅲ. 비교 및 연결

| 방식 | 장점 | 한계 |
| :-- | :-- | :-- |
| Provisioned DB | 예측 가능, 꾸준한 [[282_performance_tactics|성능]] | 과다 [[528_provisioning|프로비저닝]] 낭비 |
| [[206_serverless_cold_start|Serverless]] DB | 자동 확장, 비용 최적화 | [[559_serverless_cold_start_mitigation|콜드 스타트]], 변동성 |
| Self-managed DB | 세밀한 통제 | 운영 부담 큼 |

[[206_serverless_cold_start|서버리스]] DB는 [[129_spike_agile_technical_investigation|스파이크]]가 큰 [[090_service_kubernetes_network_load_balancing|서비스]], 테스트/개발, 비정기 업무에 강하다. 반대로 24시간 고부하가 계속되는 시스템은 기존 Provisioned DB가 더 나을 수 있다.

- **📢 섹션 요약 비유**: 항상 손님이 많은 식당에는 정규 직원이 낫고, 들쑥날쑥한 식당에는 파트타임이 낫다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[206_serverless_cold_start|서버리스]] DB를 고를 때는 "얼마나 자주, 얼마나 급하게 트래픽이 변하나"를 먼저 본다.

### [[435_checklist_based_testing|체크리스트]]

1. 트래픽 패턴이 예측 불가능한가?
2. 0에 가까운 유휴 비용이 중요한가?
3. [[559_serverless_cold_start_mitigation|콜드 스타트]]가 [[090_service_kubernetes_network_load_balancing|서비스]]에 치명적이지 않은가?
4. 커넥션 풀과 [[264_proxy_pattern_surrogate_access_control|프록시]] [[268_strategy_pattern|전략]]이 준비됐는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 꾸준한 초고부하 시스템에 [[206_serverless_cold_start|서버리스]]를 적용하는 설계
- [[249_scaling_normalization_standardization|스케일링]]은 자동인데 커넥션 관리는 수동인 설계
- 저장 비용보다 실행 [[015_지연_데이터_관점|지연]]을 더 크게 보는 설계

- **📢 섹션 요약 비유**: 문을 열고 닫는 사람이 자동이어도, 손님이 계속 꽉 차 있으면 결국 작은 가게는 버티기 어렵다.

---

## Ⅴ. 기대효과 및 결론

[[206_serverless_cold_start|서버리스]] DB는 비용과 확장성 문제를 동시에 줄인다. 특히 짧게 몰리는 트래픽에는 매우 유리하다.

하지만 모든 DB 문제를 해결하지는 않는다. 결국 [[090_service_kubernetes_network_load_balancing|서비스]] 패턴을 보고 [[206_serverless_cold_start|서버리스]]가 맞는지 선택해야 한다.

- **📢 섹션 요약 비유**: 풍선처럼 필요할 때만 커지는 창고지만, 항상 큰 창고가 필요한 곳도 있다.

---

## 관련 개념 맵

```text
트래픽 변동
   ↓
Serverless DB
   ↓
Compute / Storage 분리
   ↓
자동 확장 / 비용 최적화
```

---

## 관련 키워드 및 발전 흐름도

```text
Provisioned DB
   ↓
Auto Scaling DB
   ↓
Serverless DB
   ↓
Aurora Serverless
```

---

## 어린이를 위한 3줄 비유 설명

[[206_serverless_cold_start|서버리스]] DB는 손님이 올 때만 계산대를 늘리는 가게예요.  
손님이 없으면 계산대를 줄여서 돈을 아껴요.  
그래서 왔다 갔다 하는 손님이 많은 곳에 잘 맞아요.
