+++
title = "57. 재해 복구 (Disaster Recovery, DR) - BIA와 RTO/RPO 설계"
weight = 57
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[379_dr_architecture|재해 복구]]([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]])는 재난 이후 IT [[090_service_kubernetes_network_load_balancing|서비스]]와 [[001_dikw_pyramid|데이터]]를 얼마나 빨리, 얼마나 적게 잃고 되살릴지 정하는 [[658_ir_recovery|복구]] [[268_strategy_pattern|전략]]이다.
> 2. **가치**: [[212_bia_business_impact_analysis_rto_rpo_dr|BIA]] ([[212_bia_business_impact_analysis_rto_rpo_dr|Business Impact Analysis]])로 중요한 업무를 찾고, [[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]])와 [[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]])로 [[658_ir_recovery|복구]] 수준을 수치화한다.
> 3. **판단 포인트**: [[658_ir_recovery|복구]] 목표에 따라 Mirror, Hot, Warm, Cold site를 선택하고, 정기적인 [[658_ir_recovery|복구]] 훈련으로 실제 작동 여부를 [[395_verification_process_review|검증]]해야 한다.

---

## Ⅰ. 개요 및 필요성

DR은 BCP (Business Continuity Plan)의 일부이지만, 특히 정보시스템과 [[001_dikw_pyramid|데이터]] [[658_ir_recovery|복구]]에 초점을 맞춘다. 서버가 멈추고 [[001_dikw_pyramid|데이터]]가 날아간 뒤 어떻게 살아날지를 정하는 일이다.

[[555_backup_and_restore_strategy|백업]]만 있다고 끝나지 않는다. [[555_backup_and_restore_strategy|백업]]을 복원할 장소, 복원 시간, 복원 순서까지 준비해야 진짜 [[658_ir_recovery|복구]]가 된다.

- **📢 섹션 요약 비유**: DR은 불이 난 뒤 어디서 다시 가게를 열지 정해 두는 비상 [[658_ir_recovery|복구]] 지도다.

---

## Ⅱ. BIA와 [[176_rto_recovery_time_objective|RTO]]/[[177_rpo_recovery_point_objective|RPO]]

[[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 설계의 출발점은 [[212_bia_business_impact_analysis_rto_rpo_dr|BIA]] ([[212_bia_business_impact_analysis_rto_rpo_dr|Business Impact Analysis]])다. 어떤 업무가 먼저 살아야 하는지 정해야 [[658_ir_recovery|복구]] 순서가 정해진다.

```text
BIA
  ↓
핵심 업무 선정
  ↓
RTO / RPO 설정
  ↓
복구 사이트와 백업 전략 결정
```

- **[[176_rto_recovery_time_objective|RTO]]**는 [[090_service_kubernetes_network_load_balancing|서비스]]가 다시 켜져야 하는 최대 시간이다.
- **[[177_rpo_recovery_point_objective|RPO]]**는 허용 가능한 최대 [[001_dikw_pyramid|데이터]] 손실 시점이다.

이 두 값이 작을수록 [[658_ir_recovery|복구]] 비용은 급격히 올라간다.

- **📢 섹션 요약 비유**: 병원에서 "몇 시간 안에 수술해야 하는지"와 "얼마나 피를 잃어도 되는지"를 먼저 정하는 것과 같다.

---

## Ⅲ. [[658_ir_recovery|복구]] 센터의 유형

[[658_ir_recovery|복구]] 목표에 따라 사이트 수준이 달라진다.

- **[[178_mirror_site|Mirror Site]]**: 거의 실시간으로 주 센터와 동일하게 [[212_synchronization_mechanisms|동기화]]한다.
- **[[179_hot_site_dr|Hot Site]]**: 즉시 전환이 가능한 대기 센터다.
- **[[180_warm_site_dr|Warm Site]]**: 일부만 준비되어 있어 [[658_ir_recovery|복구]]에 시간이 더 걸린다.
- **[[181_cold_site_dr|Cold Site]]**: 기본 공간만 준비된 저비용 방식이다.

[[658_ir_recovery|복구]] 목표가 엄격할수록 비용이 커지지만, [[090_service_kubernetes_network_load_balancing|서비스]] 중단 위험은 줄어든다.

- **📢 섹션 요약 비유**: 예비 차를 완전히 시동 걸어 둔 상태로 둘지, 꺼 둔 채로 둘지는 돈과 급함의 차이다.

---

## Ⅳ. [[658_ir_recovery|복구]] 절차와 [[395_verification_process_review|검증]]

DR은 계획보다 실행과 [[395_verification_process_review|검증]]이 중요하다.

- [[555_backup_and_restore_strategy|백업]]과 [[016_replication_factor|복제]]를 구분한다.
- Failover와 Failback 절차를 정한다.
- [[658_ir_recovery|복구]] 후 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 [[396_validation|확인]]한다.
- 정기적으로 복원 테스트를 수행한다.

[[658_ir_recovery|복구]] 시나리오가 문서에만 있고 실제로 안 돌아가면 의미가 없다. 그래서 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 훈련은 필수다.

- **📢 섹션 요약 비유**: 운동회 전 연습을 해 보지 않으면, 진짜 달리기에서 넘어지기 쉽다.

---

## Ⅴ. 실무 설계와 BCP 비교

DR은 [[555_backup_and_restore_strategy|백업]]과 같은 말이 아니다. [[555_backup_and_restore_strategy|백업]]은 [[001_dikw_pyramid|데이터]]를 저장하는 행위이고, DR은 [[090_service_kubernetes_network_load_balancing|서비스]] 전체를 다시 살리는 [[268_strategy_pattern|전략]]이다.

실무에서는 다음을 함께 본다.

- 핵심 업무별 [[658_ir_recovery|복구]] 우선순위
- [[176_rto_recovery_time_objective|RTO]]/RPO에 맞는 사이트 선택
- [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]] 주기
- [[658_ir_recovery|복구]] 후 [[395_verification_process_review|검증]] 절차
- BCP 전체 문서와의 연계

이 기준이 맞아야 재난이 와도 핵심 [[090_service_kubernetes_network_load_balancing|서비스]]를 버틸 수 있다.

- **📢 섹션 요약 비유**: 물통만 준비하는 것과, 물통을 어디에 두고 누가 들고 갈지도 정해 두는 것은 다르다.

---

## 관련 개념 맵

```text
BIA
   ↓
RTO / RPO
   ↓
Mirror / Hot / Warm / Cold site
   ↓
복구 훈련 / 검증
```

---

## 관련 키워드 및 발전 흐름도

1. [[555_backup_and_restore_strategy|백업]] 중심 사고 → [[001_dikw_pyramid|데이터]] 저장에만 초점
2. [[212_bia_business_impact_analysis_rto_rpo_dr|BIA]] 도입 → 핵심 업무 우선순위화
3. [[176_rto_recovery_time_objective|RTO]]/[[177_rpo_recovery_point_objective|RPO]] 수치화 → [[658_ir_recovery|복구]] 목표 정량화
4. 사이트 계층화 → 비용과 [[658_ir_recovery|복구]] 속도의 균형
5. [[658_ir_recovery|복구]] 훈련과 자동화 → DR의 실전 운용 강화

---

## 어린이를 위한 3줄 비유 설명

[[379_dr_architecture|재해 복구]]는 가게가 무너지면 어디서 다시 열지 정하는 거예요.  
언제까지 다시 열어야 하는지, 얼마나 잃어도 되는지도 미리 정해요.  
그래야 진짜 위기 때 덜 당황해요.
