---
title: 55. IPFS (InterPlanetary File System)
date: '2026-05-01'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IPFS (InterPlanetary [[501_file_definition_logical_record|File]] System)는 콘텐츠 주소 기반의 [[136_variance|분산]] [[501_file_definition_logical_record|파일]] 시스템이다.
> 2. **가치**: CID (Content [[088_identifier_in_er_model|Identifier]]), Merkle [[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]]), [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] ([[916_p2p_peer_to_peer_networking_super_node_gnutella|Peer-to-Peer]]) 구조로 위치가 아니라 내용으로 찾는다.
> 3. **판단 포인트**: 저장과 영속성은 자동이 아니다. pinning과 [[016_replication_factor|복제]] [[164_policy|정책]]이 필요하다.

---

## Ⅰ. 개요 및 필요성

IPFS는 [[501_file_definition_logical_record|파일]]이 어디에 있는지가 아니라 어떤 내용인지로 찾는다. 그래서 링크가 바뀌어도 같은 콘텐츠를 추적할 수 있다.

[[136_variance|분산]] 저장, 검열 [[003_resistance|저항]], 콘텐츠 배포에서 유용하다.

- **📢 섹션 요약 비유**: IPFS는 책장 위치 대신 책 내용의 지문으로 찾는 도서관이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[501_file_definition_logical_record|파일]]은 chunk로 쪼개지고, 각 chunk는 해시로 식별된다. 이 해시들이 Merkle DAG를 만들고, 최종적으로 CID가 생성된다.

```text
File → Chunks → Hashes → Merkle DAG → CID → Retrieval
```

| 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| CID | 콘텐츠 [[289_identification_flags_fragmentation_offset|식별자]] | 해시 기반 |
| Merkle [[401_bayesian_network_dag_causality|DAG]] | 연결 구조 | [[003_integrity|무결성]] |
| Node | 저장/전달 | [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 참여 |
| Pinning | 고정 저장 | 지속성 |

핵심은 위치 기반 주소가 아니라 내용 기반 주소라는 점이다. 같은 [[501_file_definition_logical_record|파일]]은 같은 CID를 가지므로 [[003_integrity|무결성]] [[395_verification_process_review|검증]]이 쉽다.

- **📢 섹션 요약 비유**: IPFS는 주소가 아니라 지문으로 우편물을 찾는 시스템이다.

---

## Ⅲ. 비교 및 연결

IPFS는 HTTP와 다르다. HTTP는 위치 기반이고, IPFS는 내용 기반이다. 다만 IPFS도 캐시와 [[452_availability|가용성]]을 위해 게이트웨이와 pinning이 필요하다.

| 항목 | [[461_http_stateless_connection_oriented|HTTP]] | IPFS |
| :--- | :--- | :--- |
| 주소 | 위치 기반 | 콘텐츠 기반 |
| [[003_integrity|무결성]] | 별도 [[395_verification_process_review|검증]] | 해시로 [[395_verification_process_review|검증]] |
| [[452_availability|가용성]] | 서버 의존 | [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] + pinning |

블록체인과 함께 쓰면 메타데이터나 [[316_reference_pattern_nosql|참조]] [[003_integrity|무결성]]을 더 강하게 보장할 수 있다.

- **📢 섹션 요약 비유**: HTTP는 집 주소, IPFS는 책 내용이 적힌 바코드다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 pinning [[164_policy|정책]], 네트워크 [[136_variance|분산]], 게이트웨이, 업로드/다운로드 [[282_performance_tactics|성능]], 콘텐츠 수명 관리를 함께 봐야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. [[501_file_definition_logical_record|파일]]을 누가 계속 보관할 것인가?
2. CID를 어떻게 배포할 것인가?
3. [[452_availability|가용성]]과 [[016_replication_factor|복제]] 전략이 있는가?
4. 게이트웨이 장애 시 대안이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- IPFS를 그냥 영구 저장소로 오해하는 경우
- pinning 없이 데이터가 사라지는 경우
- 콘텐츠 주소와 메타데이터를 혼동하는 경우

기술사 관점에서는 IPFS가 [[136_variance|분산]] 저장의 [[003_integrity|무결성]]과 공유성을 높이지만 운영 [[164_policy|정책]]이 반드시 필요하다는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: IPFS는 책을 여러 도서관에 복사해 두는 [[136_variance|분산]] 서가다.

---

## Ⅴ. 기대효과 및 결론

IPFS는 콘텐츠 중심 배포와 [[136_variance|분산]] 저장에 강하다. [[395_verification_process_review|검증]] 가능한 링크와 공유가 쉬워진다.

정리하면, [[501_file_definition_logical_record|파일]]을 위치가 아닌 내용으로 찾는 것이 핵심이다.

- **📢 섹션 요약 비유**: IPFS는 이름이 아니라 얼굴로 친구를 찾는 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| CID | 콘텐츠 주소 |
| Merkle [[401_bayesian_network_dag_causality|DAG]] | [[003_integrity|무결성]] 구조 |
| [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] | [[136_variance|분산]] 노드 |
| Pinning | 지속 저장 |
| Gateway | 접근 경로 |

### 📈 관련 키워드 및 발전 흐름도

```text
파일
    │
    ▼
해시 / CID
    │
    ▼
Merkle DAG
    │
    ▼
P2P 저장 / pinning
```

이 흐름은 [[501_file_definition_logical_record|파일]] 저장이 위치 기반에서 내용 기반으로 바뀌는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. IPFS는 책 제목이 아니라 책 내용으로 찾는 도서관이에요.
2. 같은 책은 같은 번호를 가져요.
3. 그래서 어디서 받아도 같은 책인지 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 552

← **이전**: [[054_dao_decentralized_autonomous_organization|54. DAO (Decentralized Autonomous Organization)]]
**다음**: [[056_smart_contract_vulnerability_reentrancy|56. 스마트 컨트랙트 보안 취약점 - 재진입 (Re-entrancy), 오버플로우/언더플로우, 권한 탈취]] →

---
