---
title: "IPFS (InterPlanetary File System)"
date: "2026-05-01"
tags:
  - "studynote-ict-convergence"
weight: 55
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IPFS (InterPlanetary [File](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System)는 콘텐츠 주소 기반의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이다.
> 2. **가치**: CID (Content [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)), Merkle [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) ([Directed Acyclic Graph](/studynote/06_ict_convergence/03_cloud_infrastructure/255_apache_airflow_dag/)), [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) ([Peer-to-Peer](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/)) 구조로 위치가 아니라 내용으로 찾는다.
> 3. **판단 포인트**: 저장과 영속성은 자동이 아니다. pinning과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요하다.

---

## Ⅰ. 개요 및 필요성

IPFS는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 어디에 있는지가 아니라 어떤 내용인지로 찾는다. 그래서 링크가 바뀌어도 같은 콘텐츠를 추적할 수 있다.

[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장, 검열 [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/), 콘텐츠 배포에서 유용하다.

- **📢 섹션 요약 비유**: IPFS는 책장 위치 대신 책 내용의 지문으로 찾는 도서관이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 chunk로 쪼개지고, 각 chunk는 해시로 식별된다. 이 해시들이 Merkle DAG를 만들고, 최종적으로 CID가 생성된다.

```text
File -> Chunks -> Hashes -> Merkle DAG -> CID -> Retrieval
```

| 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| CID | 콘텐츠 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) | 해시 기반 |
| Merkle [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | 연결 구조 | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) |
| Node | 저장/전달 | [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 참여 |
| Pinning | 고정 저장 | 지속성 |

핵심은 위치 기반 주소가 아니라 내용 기반 주소라는 점이다. 같은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 같은 CID를 가지므로 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 쉽다.

- **📢 섹션 요약 비유**: IPFS는 주소가 아니라 지문으로 우편물을 찾는 시스템이다.

---

## Ⅲ. 비교 및 연결

IPFS는 HTTP와 다르다. HTTP는 위치 기반이고, IPFS는 내용 기반이다. 다만 IPFS도 캐시와 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 위해 게이트웨이와 pinning이 필요하다.

| 항목 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) | IPFS |
| :--- | :--- | :--- |
| 주소 | 위치 기반 | 콘텐츠 기반 |
| [무결성](/studynote/09_security/01_intro_principles/003_integrity/) | 별도 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 해시로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | 서버 의존 | [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) + pinning |

블록체인과 함께 쓰면 메타데이터나 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 더 강하게 보장할 수 있다.

- **📢 섹션 요약 비유**: HTTP는 집 주소, IPFS는 책 내용이 적힌 바코드다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 pinning [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 네트워크 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 게이트웨이, 업로드/다운로드 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 콘텐츠 수명 관리를 함께 봐야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 누가 계속 보관할 것인가?
2. CID를 어떻게 배포할 것인가?
3. [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)과 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 전략이 있는가?
4. 게이트웨이 장애 시 대안이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- IPFS를 그냥 영구 저장소로 오해하는 경우
- pinning 없이 데이터가 사라지는 경우
- 콘텐츠 주소와 메타데이터를 혼동하는 경우

기술사 관점에서는 IPFS가 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 공유성을 높이지만 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 반드시 필요하다는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: IPFS는 책을 여러 도서관에 복사해 두는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 서가다.

---

## Ⅴ. 기대효과 및 결론

IPFS는 콘텐츠 중심 배포와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 저장에 강하다. [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 링크와 공유가 쉬워진다.

정리하면, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 위치가 아닌 내용으로 찾는 것이 핵심이다.

- **📢 섹션 요약 비유**: IPFS는 이름이 아니라 얼굴로 친구를 찾는 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| CID | 콘텐츠 주소 |
| Merkle [DAG](/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 구조 |
| [P2P](/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 노드 |
| Pinning | 지속 저장 |
| Gateway | 접근 경로 |

### 📈 관련 키워드 및 발전 흐름도

```text
파일
    |
    v
해시 / CID
    |
    v
Merkle DAG
    |
    v
P2P 저장 / pinning
```

이 흐름은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장이 위치 기반에서 내용 기반으로 바뀌는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. IPFS는 책 제목이 아니라 책 내용으로 찾는 도서관이에요.
2. 같은 책은 같은 번호를 가져요.
3. 그래서 어디서 받아도 같은 책인지 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 552

<- **이전**: [54. DAO (Decentralized Autonomous Organization)](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)
**다음**: [56. 스마트 컨트랙트 보안 취약점 - 재진입 (Re-entrancy), 오버플로우/언더플로우, 권한 탈취](/studynote/06_ict_convergence/01_blockchain/056_smart_contract_vulnerability_reentrancy/) ->

---
