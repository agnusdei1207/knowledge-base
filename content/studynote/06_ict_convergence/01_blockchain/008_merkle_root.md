---
title: "8. 머클 루트 (Merkle Root) - 모든 트랜잭션 해시를 묶은 최종 해시값"
tags:
  - "ict_convergence"
---


# 08. 머클 루트 (Merkle Root)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 머클 루트는 해당 블록 내 모든 거래의 해시값을 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)([Merkle Tree](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)) 구조로 반복적으로 결합하여 도출한 단일 해시값으로, 블록 헤더에 저장되어 전체 거래 목록의-integrity를 대표하는 핵심 값이다.
> 2. **가치**: 머클 루트 하나의 해시값만으로 수천 건의 거래 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을효율적으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있으며, SPV(Simple Payment [Verification](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) 클라이언트의 거래 확인을 가능하게 하는 핵심 기반이다.
> 3. **융합**: 비트코인, 이더리움 등 모든 주요 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에서 활용되며, 머클 증명(Merkle Proof)과 결합하여 탈중앙화된 환경에서의 효율적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 가능하다.

---

## Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

### 개념의 정의

머클 루트(Merkle Root)는 특정 블록 내에 포함된 모든 거래([Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/))를 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)([Merkle Tree](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)) 구조로 처리하여 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 단일 해시값이다. 블록 헤더(Block Header)의 핵심 구성 요소 중 하나로, 이전 블록 해시(Previous Block Hash)와 함께 블록을유일하게 식별하는 역할을 한다. 머클 루트가 변경되면 이후 연결된 모든 블록의 참조가 끊어지므로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 핵심이 된다.

### 탄생 배경과 필요성

디지털 금융 시스템에서 거래 기록의변조 여부를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 것은 가장 중요한 과제이다. 그러나 블록 하나에 수천 건의 거래가 포함된 경우, 모든 거래를 직접 비교하여 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 것은막대한 계산 비용이 소요된다. 머클 루트는 이러한 문제의해결책으로, 단일 해시값(머클 루트)만으로 해당 블록 내 모든 거래의-integrity를 대표할 수 있게 하였다. 또한 특정 거래의 존재를 증명하는 머클 증명(Merkle Proof)을 활용하면, 전체 거래 목록 전체를 전송하지 않고도 거래의 유효성을 효율적으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있다.

### 💡 analogy

머클 루트는기업의 지문과 같다. 인간의 지문은 그 개인을유일하게 식별한다. 머클 루트도 특정 블록의 모든 거래를유일하게 식별한다. 만약 기업의 임직원이 한 명이라도변경되면(거래 내용 변경),해공사전체의조직구조가 바뀌게 되어 최종적으로는공사적"지문"(머클 루트)이 달라진다. 실제 지문처럼, 머클 루트도 한 문자라도 달라지면 다른 값이되어버린다.

### 배경 설명

머클 루트의 생성과정은 다음과 같다. 수선, 블록 내 각 거래에 SHA-256 해시 알고리즘을 적용하여취인 해시값(리프노드)을 얻는다.다음에,린り합う 두 리프노드를 결합(Concatenation)하고, 결합된 값에 SHA-256 해시를 적용하여 부모 노드를얻는다. 만약 리프노드의 수가기수인 경우, 마지막 리프노드를 복제하여짝을 맞춘다. 이 과정을근절점(머클 루트)에 도달할 때까지반복한다. 머클 루트는 리프노드(거래)의 총 수와 무관하게 항상 동일한 크기(32바이트, 256비트)를가진다. 거래 한 건이라도 내용이 바뀌면, 그 거래의 해시값이변わり,련쇄적에 머클 루트가 달라져서 조작사실이감지된다.

### 📢 비유 요약

머클 루트는전시회의 전시품 체크섬과 같다. 전시회에 hundred 점의 작품이 있다면, 한 점의 작품도 빠지거나 조작되면 전체 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)의 목록과 맞지 않게 되어문제가 발견된다. 그러나 실제 모든 작품을확인하는 대신, 전시회의개막전에각 팀별로작품 목록을 요약 제출하게 하고, 이를 다시위원회에서 종합하여최종 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)(머클 루트)를제작한다. 이후 누군가 작품을빠뜨리거나 바꿔치면, 관련 팀의 요약이 달라지고최종 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/)와 맞지 않아즉시 Discovery된다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 머클 루트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 과정 상세

```
[거래 목록]
  |
  v
+------------------------------------------------------------------+
|  1단계: 각 거래의 해시값 계산 (SHA-256)                          |
|  TX1 --► H1 = SHA256(TX1)                                       |
|  TX2 --► H2 = SHA256(TX2)                                       |
|  TX3 --► H3 = SHA256(TX3)                                       |
|  TX4 --► H4 = SHA256(TX4)                                       |
+------------------------------------------------------------------+
  |
  v
+------------------------------------------------------------------+
|  2단계:隣接 해시값 결합 후 해시 (Level 1)                          |
|  H1 + H2 --► H12 = SHA256(H1 ∥ H2)                              |
|  H3 + H4 --► H34 = SHA256(H3 ∥ H4)                              |
+------------------------------------------------------------------+
  |
  v
+------------------------------------------------------------------+
|  3단계:상위 레벨 결합 후 해시 (Level 2)                           |
|  H12 + H34 --► H1234 = SHA256(H12 ∥ H34)                       |
|                        |                                         |
|                        v                                         |
|  [머클 루트 = H1234] (항상 32바이트)                             |
+------------------------------------------------------------------+
```

머클 루트의 핵심 특성은결정론적(Deterministic)이라는 점이다. 동일한 거래 목록으로부터 항상동일한 머클 루트가 생성된다. 이것은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 환경에서 모든 노드가 독립적으로 동일한 머클 루트를 계산하여 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있음을 의미한다.

### 머클 루트와 블록 헤더

```
+------------------------------------------------------------------+
|                      블록 헤더 (80바이트)                         |
+------------------------------------------------------------------+
|                                                                  |
|  버전 (4B)         | 이전 블록 해시 (32B) | 머클 루트 (32B)     |
|  ---------          ------------------   -------------          |
|  타임스탬프 (4B)    | 난이도 목표 (4B)    | 논스 (4B)          |
|                                                                  |
+------------------------------------------------------------------+
                          |
                          v
              +------------------------------+
              |  블록 헤더의 Double SHA-256   |
              |  = 블록 자체의 고유 해시값     |
              |  (블록을唯一하게 식별)        |
              +------------------------------+
```

머클 루트는 블록 헤더의 3번째 필드에 위치하며, 다른 필드([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/), 이전 블록 해시, 타임스탬프, 난이도, 논스)와 함께 블록 헤더 전체의 해시값(블록 해시)을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는inputs 중 하나이다. 따라서 거래 내용(TX)이 바뀌면 머클 루트가 바뀌고, 이것은 블록 헤더의 해시값도 바꿔버린다. 이것이 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의변조 방지의핵심 메커니즘이다.

### 📢 비유 요약

머클 루트와 블록 헤더의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는인질의수족의가와 같다. 수족(모든 거래)가 조금이라도동く와/과, 쇄(머클 루트)이 맞지 않게 되고, 전신의가(블록 해시)도 풀리게 되어 조작 사실이 드러난다. すべ고의취인이정합성보고ば, ロックも전신의가も정상에기능하는.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

### SPV(Simple Payment [Verification](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))에서의 활용

SPV 클라이언트(예: 모바일비특잡지갑)는 전체 블록을 다운로드하지 않고, 블록 헤더만 다운로드하여동작한다. 특정 거래가 이루어졌는지 확인하려면, SPV 클라이언트는 해당 거래의 머클 증명(Merkle Proof)을모든 블록을 저장한 전체 노드([Full Node](/studynote/06_ict_convergence/01_blockchain/083_full_node_complete_ledger/))에게 요청한다. 전체 노드는 해당 거래가 포함된 블록의 리프노드부터 머클 루트까지의형제 노드 해시값들을제공한다. SPV 클라이언트는이러한값으로 머클 루트을재계산하여, 자신이보유한 블록 헤더의 머클 루트와비교함으로써 거래의 존재를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.이방법에より, モバイル전포등リソース이/가한제된デバイス에서も, 효솔적な검정이가능과なる.

### 비트코인 코어(bitcoind)에서의 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 과정

비트코인 코어 등의_full node는 새로운 블록을 수신하면 다음과 같은 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 절차를たど린다. 수선 블록의 크기와 구조가 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 규칙에 맞는지 확인한다.다음에 블록 헤더의작업량증명(PoW)이 유효한지 확인한다. 그후, 블록 내 모든 거래를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고, 거래들로 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를 재구성하여얻은 머클 루트가 블록 헤더에 저장된 머클 루트와 일치하는지 확인한다. 이 중 하나라도 실패하면 블록은배척される.

### 이더리움에서의 머클 루트

이더리움은 비트코인과는다른 종류의 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를활용한다. 이더리움에서는 머클 패트리시아 트리(Merkle Patricia [Trie](/studynote/08_algorithm_stats/04_datastructure/066_trie/), MPT)를 사용하여, 계정 상태(Accounts [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)), 거래 영수증(Receipts), 거래 목록(Transactions) 등을 저장한다. MPT는 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/).prefix tree(Prefix Tree)와 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)의 특성을 결합한 것으로, 키-값 쌍을효율적으로 저장하고 검색할 수 있다.

### 📢 비유 요약

머클 루트의 실무 활용은중요 문서의 [DRM](/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/)(디지털 [저작권](/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/) 관리)과 같다. PDF [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 DRM을 적용하면, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용 중 일부가 바뀌면 DRM이 무효가 된다. 머클 루트도 마찬가지로, 거래 내용 중 일부가 바뀌면 머클 루트가 달라져서 해당 블록 전체가 무효 처리된다. 이를 통해변조된 거래가 포함된 블록은 네트워크에서자동적에배척된다.

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

### [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 테스트

머클 루트의품질test에서 가장 기본적인 것은 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이다. 측시 절차는다음과 같다. 수선 테스트용 거래 목록을수집한다. 다음에 동일한 거래 목록으로 두 번 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를 구축한다. 머클 루트가동일해야 한다. 3번목에 거래 중 하나를 조작(내용 변경)한다. 4번목에 조작된 거래 목록으로 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를 구축한다. 머클 루트가기존과 달라야 한다. 이 측시를 통해 머클 루트의결정론적성과 변조 민감도를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

### 머클 증명 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 테스트

머클 증명의올바른 작동을 측시하기 위해다음과 같은 절차를 따른다. 수선 유효한 머클 증명수거집을준비한다. 다음에 증명으로부터 머클 루트를재계산한다. 3번목에재계산된 머클 루트와 실제 블록의 머클 루트를 비교한다.동일하면 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 성공이다. 4번목에형제 노드의 해시값 중 하나라도 변경하면,재계산된 머클 루트가 달라져서 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이실패해야 한다.

### 경계 조건 테스트

머클 루트연산의경계 조건도 측시해야 한다. 리프노드가 1개만 있는 경우(트리의최소 크기), 리프노드가기수 개인 경우(형제 [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 처리), 리프노드가 2^n개보다많고 2^(n+1)개보다 적은 경우 등을 측시한다. 이러한 경계 조건에서 올바르게 머클 루트가 생성되는지를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

### 📢 비유 요약

머클 루트의품질test는은행 지폐 감정 자동화 시스템의テスト와/과らえるこ와/과가에서きる. 진짜 지폐를 넣으면「진짜」라는 결과가 나와야 하고, 위조 지폐(내용 변경)를 넣으면「위조」라는 결과가 나와야 한다. 또한 찢어진 지폐(경계 조건)도정しく처리되어야 한다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

### 이더리움 2.0과 Verkle 트리

이더리움의금후의アップグレード에서는 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를 대체할 Verkle 트리(Verkle Tree)의도입이검토되고 있다. Verkle 트리는 벡터 커밋먼트(Vector Commitment)를활용하여, 동일한 보안 수준을 유지하면서 머클 증명(Proof)의 크기를대폭으로 줄인다. 현재 이더리움의 머클 증명은심도에 따라 수십 개의 해시값을 함ん에서いる이/가, Verkle 트리의 증명은 수개의 Commitment치만으로 동일한 증명 기능을 выполняет다. 이것은 이더리움의 레이트 클라이언트( light [client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))의 efficiency를 크게 향상시킬 것으로 기대된다.

### 이중 지불공격과 머클 루트

이중 지불( Double Spending) 공격은 동일한 UTXO를 두 번 사용하는공격이다. 공격자는 유효한 거래와 함께 이를 은폐하기 위한 가짜 거래를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 일부 노드에만 전파하거나, 거래를 비례적으로 조작하여 머클 루트를개변하려고 시도할 수 있다. 그러나 네트워크의 다수 노드가 올바른 머클 루트를 계산하여 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하므로, 조작된 블록은배척된다.작업량증명(PoW)이나 지분증명(PoS) 등의 Consensus Algorithm과 머클 루트의 조합으로 이중 지불 공격은실질적으로방지된다.

### 📢 비유 요약

머클 루트의 발전은우체국추종 시스템의진화와 같다. 과거에는 소포마다전과정을수동으로기록하였다(전체 거래 목록 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)). 머클 루트는 각 중계소마다 해당 구간의 소포 목록 요약만을기록하면 되게 하였다(효율적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)). Verkle 트리는중계소의 수를더 줄이면서도잉연추적이 가능하게 하는 차세대 시스템이다.

### 결론

머클 루트는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 기술의근기를이루는 핵심 구성 요소이다. 단일 해시값으로 수천 건의 거래 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 대표할 수 있다는 단순하지만 강력한 개념은, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서의 효율적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이라는 과제를 해결하였다. SPV 클라이언트, 머클 증명 등ractical한응용의 기반이 되며, Verkle 트리 등 차세대 기술의 발전에도 핵심적인 영감을주고 있다. 머클 루트는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 네트워크의 불변성(Immutability)과 투명성(Transparency)을기술적으로단보하는 중요한 요소이다.

---

## 핵심 인사이트 [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램 ([Concept](/studynote/14_data_engineering/02_math_mining/120_concept/) Map)

```
+------------------------------------------------------------------+
|                    머클 루트 생성 및 검증 원리                      |
+------------------------------------------------------------------+
|                                                                  |
|  [거래 목록]                                                      |
|  TX1, TX2, TX3, TX4, TX5, TX6, TX7, TX8                         |
|     |                                                   |
|     v                                                        |
|  [머클 트리 构建]                                                |
|                                                                  |
|      Level 0 (Leaf):    H1   H2   H3   H4   H5   H6   H7   H8   |
|                              |                                     |
|      Level 1:           H12        H34        H56        H78      |
|                              |                                     |
|      Level 2:           H1234                 H5678              |
|                              |                                     |
|      Level 3:                    머클 루트                          |
|                             (H12345678)                            |
|                             = 항상 32B                            |
|                                                                  |
+------------------------------------------------------------------+
|  검증 과정:                                                       |
|                                                                  |
|  [증명 대상 거래: TX5]                                            |
|  TX5의兄弟: H6 --► H56                                           |
|  H56의兄弟: H78 --► H5678                                        |
|  H5678의兄弟: H1234 --► 머클 루트                                 |
|                                                                  |
|  ✅ 증명된 머클 루트 == 실제 블록의 머클 루트 -> 거래 유효          |
|  ❌ 증명된 머클 루트 != 실제 블록의 머클 루트 -> 거래 위조/누락   |
+------------------------------------------------------------------+
|  핵심 특성:                                                       |
|  - 단일 해시값으로 N개 거래 무결성 代表                            |
|  - 거래 1개라도 변경 -> 머클 루트大幅 변경                          |
|  - SPV客户端는 전체 블록 없이 거래 검증 가능                       |
+------------------------------------------------------------------+
```


### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| <strong><a href="/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/">해시 함수</a> (<a href="/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/">Hash Function</a>)</strong> | SHA-256 기반으로 각 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)을 고정 길이 32바이트 지문으로 변환하는 핵심 연산 |
| **이진 해시 트리 (Binary Hash Tree)** | 거래 해시를 쌍으로 합쳐 단계적으로 올라가는 트리 구조로, 루트 한 개가 전체를 대표 |
| <strong>SPV (Simple Payment <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">Verification</a>)</strong> | 머클 증명 경로만으로 전체 블록 없이 특정 거래의 포함 여부를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 경량 클라이언트 기술 |
| **블록 헤더 (Block Header)** | 머클 루트를 포함한 80바이트 메타데이터로, [작업 증명](/studynote/06_ict_convergence/01_blockchain/014_pow_proof_of_work/)(PoW)의 해싱 대상이 되는 핵심 구조 |
| **Verkle 트리 (Verkle Tree)** | 이더리움 2.0에서 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)를 대체하여 증명 크기를 수십 배 줄이는 차세대 암호화 트리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[개별 트랜잭션 해시 (TX Hash)]
    |
    v
[머클 트리 (Merkle Tree) — 쌍 결합 해싱]
    |
    v
[머클 루트 (Merkle Root) — 단일 32바이트 지문]
    |
    v
[블록 헤더 (Block Header) — 머클 루트 삽입]
    |
    v
[SPV 경량 검증 (Simple Payment Verification)]
```

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에서 수천 개의 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 단일 해시 값으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하고 경량 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 가능하게 하는 머클 루트 기술 발전 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 머클 루트는 수천 장의 영수증을 <strong>딱 한 줄의 암호</strong>로 요약한 마법 도장이에요.
2. 누군가 영수증 한 장을 몰래 바꾸면 암호가 완전히 달라져서 바로 들키게 돼요.
3. 이 마법 도장 덕분에 가벼운 스마트폰도 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 전체를 내려받지 않고 내 거래가 진짜인지 확인할 수 있어요!

## 참고
- 모든 약어는 반드시 전체 명칭과 함께 표기
- 일어/중국어 절대 사용 금지
- 각 섹션 끝에 📢 요약 비유 반드시 추가
- 최소 800자/[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)
- [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)명: 01_, 02_, 03_... 형식 (2자리 숫자)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 8 / 552

<- **이전**: [7. 머클 트리 (Merkle Tree / Hash Tree) - 트랜잭션 무결성 검증을 위한 해시 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)
**다음**: [9. 해시 포인터 (Hash Pointer) - 데이터의 위치와 무결성 정보를 동시에 지님](/studynote/06_ict_convergence/01_blockchain/009_hash_pointer/) ->

---
