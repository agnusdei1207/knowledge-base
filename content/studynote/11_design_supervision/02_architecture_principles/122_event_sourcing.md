---
title: "Event Sourcing"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) ([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/))은 시스템의 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 저장하는 대신, 그 상태에 이르기까지의 모든 상태 변화 이벤트(event)를 영구적이고 순서가 보장된 추가 전용(append-only) 이벤트 스트림으로 저장하고, 이 이벤트들을 순서대로 재생(replay)하여 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 복원하는 패턴이다.
> 2. **가치**: 데이터의 전체 변경 이력이 이벤트로 보존되므로 완벽한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([audit trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/)), 특정 시점으로의 시간 여행(time travel), 이벤트 재생을 통한 새로운 읽기 모델 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 모두 가능해진다.
> 3. **판단 포인트**: [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화, [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 긴 이벤트 스트림의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이라는 세 가지 기술적 도전을 수반하므로, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적과 이력 관리가 핵심 요구사항인 금융·의료·법률 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 그 가치가 극대화된다.

---

## Ⅰ. 개요 및 필요성

전통적인 CRUD (Create, Read, Update, Delete) 방식에서는 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)만 저장하고 이전 상태는 덮어쓴다. 이 방식은 "지금 무엇인가"는 알 수 있지만 "어떻게 이 상태가 되었는가"는 알 수 없다. 금융 거래에서 현재 잔액은 알 수 있지만 어떤 입출금이 있었는지 알 수 없는 상황이 된다.

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 이 문제를 근본적으로 해결한다. 현재 잔액 대신 "100원 입금", "50원 출금", "200원 입금" 같은 이벤트들을 순서대로 저장한다. 현재 잔액(250원)은 이 이벤트들을 재생하여 계산한다. 어떤 시점의 잔액도 해당 시점까지의 이벤트를 재생하면 알 수 있다.

```text
+-------------------------------------------------------------+
|        이벤트 소싱 vs 전통 CRUD 저장 방식 비교              |
+-------------------------------------------------------------+
|  [전통 CRUD] - 현재 상태만 저장                              |
|  계좌 잔액: 250원 (이력 없음)                                |
|                                                             |
|  [이벤트 소싱] - 이벤트 스트림 저장                          |
|  이벤트 #1: AccountOpened(balance=0)  @2026-01-01           |
|  이벤트 #2: MoneyDeposited(amount=100) @2026-01-02          |
|  이벤트 #3: MoneyWithdrawn(amount=50)  @2026-01-03          |
|  이벤트 #4: MoneyDeposited(amount=200) @2026-01-04          |
|                                                             |
|  현재 상태 = 이벤트 #1~#4 순차 재생 -> 잔액 250원            |
+-------------------------------------------------------------+
```

이벤트는 append-only로만 저장된다. 한번 기록된 이벤트는 수정하거나 삭제하지 않는다. 이 불변성(immutability)이 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적의 신뢰성을 보장한다.

- **📢 섹션 요약 비유**: 회계 장부는 숫자를 지우고 고쳐 쓰지 않는다. 잘못된 금액은 반대 방향의 정정 분개를 추가한다. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 이 회계 원칙을 소프트웨어에 적용한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)의 핵심 구성 요소는 이벤트 스토어(Event Store), [애그리게이트](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)([Aggregate](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)), 프로젝션(Projection), [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)([Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/))이다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 이벤트 스토어 | 이벤트를 append-only로 영구 저장 | 불변성, 순서 보장, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| [애그리게이트](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) | 이벤트를 소비하여 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 계산 | 이벤트 적용(apply) 메서드 |
| 프로젝션 | 이벤트로부터 읽기 모델 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 읽기 모델과 결합 |
| [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) | 특정 시점 상태 저장으로 재생 최적화 | N번째 이벤트마다 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) |

```text
+-------------------------------------------------------------+
|      스냅샷을 통한 이벤트 재생 최적화                        |
+-------------------------------------------------------------+
|  이벤트 스트림:                                             |
|  E1 E2 E3 ... E500 [스냅샷] E501 E502 ... E750 [스냅샷] ... |
|                                                             |
|  현재 상태 복원 시:                                         |
|  가장 최근 스냅샷 로드 + 스냅샷 이후 이벤트만 재생          |
|  (전체 이벤트 재생 불필요 -> 성능 최적화)                    |
+-------------------------------------------------------------+
```

이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화가 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)의 핵심 기술 도전이다. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 정의한 이벤트 구조가 비즈니스 변화로 바뀌어야 할 때, 이미 저장된 이벤트를 변경할 수 없으므로 업캐스팅(upcasting) 기법으로 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 이벤트를 최신 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 변환하여 처리한다.

- **📢 섹션 요약 비유**: Git의 커밋 히스토리와 같다. 현재 코드 상태는 모든 커밋을 순서대로 적용한 결과다. 특정 커밋으로 되돌아가거나(time travel), 새로운 브랜치에서 다른 방향으로 실험(새 읽기 모델)할 수 있다.

---
## Ⅲ. 비교 및 연결

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)과 전통 CRUD의 선택은 "[현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)"와 "변화의 이력" 중 무엇이 핵심 자산인지에 따라 결정된다.

| 비교 축 | A | B |
|:---|:---|:---|
| **저장 대상** | [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) (Latest [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) | 변화 이벤트 스트림 |
| **이력 추적** | 별도 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 테이블 필요 | 이벤트 자체가 이력 |
| **시간 여행** | 불가 (이전 상태 소실) | 이벤트 재생으로 가능 |
| **복잡도** | 단순 | 높음 |
| <strong>읽기 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 직접 조회 (빠름) | 프로젝션 필요 |

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) ([도메인 주도 설계](/studynote/12_it_management/05_security_compliance/310_architecture/))의 [애그리게이트](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)([Aggregate](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)) 패턴, CQRS와 삼위일체를 이룬다. [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) [애그리게이트](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/)가 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계를 정의하고, [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)이 상태 변화를 이벤트로 저장하며, CQRS가 읽기 모델을 분리한다.

- **📢 섹션 요약 비유**: 사진(CRUD)은 현재 모습만 담지만, 영상([이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/))은 모든 순간의 변화를 담는다. 사진으로는 어제 어디에 있었는지 알 수 없지만, 영상은 재생하면 알 수 있다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)의 실무 도입에서 가장 많이 간과하는 것은 [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) (General [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) Regulation, 일반 [개인정보보호](/studynote/09_security/16_data_privacy/803_privacy_law_comparison/) 규정) 등 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 삭제 요구와의 충돌이다. 이벤트가 append-only라 삭제가 불가능하므로, 암호화 삭제(cryptographic erasure) 기법으로 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)를 암호화하고 키만 삭제하는 방식을 사용한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 완벽한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([audit trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/))이 법적·비즈니스적으로 필요한가?
2. 과거 특정 시점의 상태 조회(time travel)가 요구사항인가?
3. 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 진화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 계획되어 있는가?
4. [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)으로 이벤트 재생 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 수용 가능한가?
5. [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 등 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 삭제 요구에 대한 암호화 삭제 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?

- **📢 섹션 요약 비유**: 의료 기록은 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)만 기록하지 않고 모든 진료 이력을 보존한다. 특정 날의 진료 내용을 다시 볼 수 있고, 이력으로 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 설명한다.

---

## Ⅴ. 기대효과 및 결론

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)을 적용하면 완벽한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적, 시간 여행, 이벤트 재생을 통한 버그 재현·재처리, 새로운 읽기 모델의 언제든지 추가가 가능해진다. 특히 금융·의료·법률처럼 이력 추적이 규정 요구사항인 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 추가 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 테이블 없이 이 요구사항을 자연스럽게 충족한다.

한계는 기술 복잡도와 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 학습 비용이다. 이벤트 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 설계, [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 프로젝션 관리, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 대응이 모두 추가 설계 고려사항이다. 조회 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(최종 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))도 감수해야 한다.

미래 방향으로는 ① [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 전용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)(EventStoreDB)의 성숙, ② [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)과 [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)의 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 공유 원칙 활용, ③ ML 모델 학습 데이터로 이벤트 스트림 활용이 주목받고 있다.

[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 "[현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)는 과거 모든 변화의 결과물"이라는 철학을 시스템 설계에 적용한 것으로, 변화의 이력이 핵심 자산인 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 가장 강력한 무기로 기억해야 한다.

- **📢 섹션 요약 비유**: 블랙박스는 현재 차량 상태가 아니라 사고 직전까지의 모든 이동 이력을 기록한다. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 소프트웨어 시스템의 블랙박스다.

---

### 📌 관련 개념 맵

[CRUD 이력 소실 문제] -> [이벤트 소싱] -> [애그리게이트] -> CQRS 읽기 모델] -> [감사 추적·시간 여행]

| 개념 | 연결 포인트 |
|:---|:---|
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 이벤트로부터 읽기 모델 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| [애그리게이트](/studynote/04_software_engineering/04_testing_quality/222_aggregate_ddd_transaction_consistency/) | 이벤트를 적용하여 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 유지하는 [DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) 개념 |
| [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) | 이벤트 재생 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 기법 |
| EventStoreDB | [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 전용 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) |

### 📈 관련 키워드 및 발전 흐름도

[CRUD 상태 덮어쓰기] -> [이벤트 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 패턴] -> [이벤트 소싱 패턴(그렉 영)] -> CQRS+[DDD](/studynote/12_it_management/05_security_compliance/310_architecture/) 결합] -> [EventStoreDB] -> [블록체인·ML 이벤트 스트림 활용]

### 👶 어린이를 위한 3줄 비유 설명

1. 저금통(현재 잔액)만 보면 돈을 얼마나 넣고 뺐는지 모르잖아요.
2. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)은 "100원 넣기", "50원 꺼내기" 같은 모든 기록을 순서대로 남기는 방법이에요.
3. 그러면 어느 날의 잔액도 기록을 되감아서 계산할 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 178 / 530

<- **이전**: [121. CQRS 패턴 (Command Query Responsibility Segregation)](/studynote/11_design_supervision/02_architecture_principles/121_cqrs_pattern/)
**다음**: [123. 마이크로서비스 아키텍처 (MSA, Microservices Architecture)](/studynote/11_design_supervision/02_architecture_principles/123_msa_microservices_architecture/) ->

---
