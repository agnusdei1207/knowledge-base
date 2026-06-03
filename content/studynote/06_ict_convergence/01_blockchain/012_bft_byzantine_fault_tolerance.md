+++
title = "12. 비잔틴 장애 허용 (BFT, Byzantine Fault Tolerance) - 1/3 미만의 악의적 노드가 있어도 정상 합의 보장"
description = "1/3 미만의 악의적 노드가 있어도 정상 합의를 보장하는 매커니즘"
date = 2024-05-18

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

# [비잔틴 장애 허용](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) ([BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/), Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 네트워크에서 일부 노드가 고장 나거나 악의적으로 거짓 정보를 전파하더라도, 전체 시스템이 올바른 상태로 합의할 수 있는 내성 메커니즘입니다.
> 2. **가치**: 신뢰할 수 없는 환경([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/))에서도 다수결 메시지 교환을 통해 [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)과 시스템 생존성을 유지합니다.
> 3. **융합**: 고전적인 크래시 장애 허용(CFT) 한계를 극복하고, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 생태계와 결합하여 고성능 기업용 원장([PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/), Tendermint)의 근간 기술로 작동합니다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[비잔틴 장애 허용](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) ([BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/), Byzantine [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경에서 네트워크 내에 '악의적인 의도를 가진 배신자 노드'가 존재하더라도 시스템 전체가 올바른 결론에 도달하도록 보장하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 원칙입니다. 이는 1982년 레슬리 램포트(Leslie Lamport)가 제안한 '비잔틴 장군의 문제(Byzantine Generals Problem)'에서 유래되었습니다.

전통적인 IT 인프라에서는 노드가 단순히 꺼지거나 응답하지 않는 충돌 장애(Crash Fault)만을 가정했습니다. 그러나 퍼블릭 네트워크나 [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 환경에서는 해킹당한 노드가 고의로 시스템을 교란하기 위해 A에게는 '공격', B에게는 '[후퇴](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/)'라는 서로 다른 거짓 메시지를 동시에 보낼 수 있습니다. 이처럼 노드가 멈추지 않고 적극적으로 거짓을 퍼뜨리는 상황을 '비잔틴 장애'라고 하며, BFT는 이러한 최악의 조건 속에서도 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 지키기 위해 필수적입니다.

비잔틴 장군의 문제와 거짓 메시지 전파 상황을 나타낸 도식입니다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">장군 1 (배신자)</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">장군 2</div></div>
<div class="kb-diagram-note">후퇴하라! (거짓말) 공격 전파 (진실)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">장군 3</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">장군 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">===&gt;</div><div class="kb-diagram-node">비잔틴 성 (목표)</div><div class="kb-diagram-note">&lt;===</div></div>
</div>
</div>


이 도식의 핵심은 배신자(장군 1)가 다른 장군들에게 서로 모순되는 지시를 내려 진영 전체의 행동을 분열시키려 한다는 점입니다. 만약 장군들이 마스터(장군 1)의 지시만 듣는다면 부대는 궤멸합니다. 이 상황을 타개하려면 장군 2, 3, 4가 서로 받은 메시지를 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)([P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) 교환)하여 배신자를 색출해내야 합니다. 실무 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서도 이처럼 노드 간 메시지 N:N [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)이 필수적이며, 이는 강력한 보안을 주지만 노드 수가 늘어날수록 통신 복잡도가 기하급수적으로 폭증하는 원인이 됩니다.

📢 **섹션 요약 비유**: 마치 여러 명의 탐정이 모여 범인을 추리할 때, 그중에 범인과 내통하여 계속 가짜 증거를 흘리는 스파이가 섞여 있어도, 서로의 증언을 끈질기게 대조하여 결국 진짜 범인을 찾아내는 과정과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

BFT를 달성하기 위한 가장 중요한 수학적 대원칙은 전체 노드의 수가 $N$이고, 악의적(비잔틴) 노드의 수가 $f$일 때, 네트워크가 정상적으로 합의하기 위해서는 반드시 **$N \ge 3f + 1$** 의 조건을 만족해야 한다는 것입니다. 즉, 배신자가 전체의 1/3 미만이어야만 시스템이 안전합니다.

| 구성 요소 | 역할 | 내부 동작 | 통신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | 비유 |
|:---|:---|:---|:---|:---|
| **Primary (리더)** | 합의 안건의 최초 제안 | 클라이언트 요청을 받아 시퀀스 번호 부여 후 전파 | Pre-prepare | 회의 주재자 |
| **Replica (복제본)** | 안건 수신 및 [P2P](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/916_p2p_peer_to_peer_networking_super_node_gnutella/) [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/) | 리더의 메시지를 다방면으로 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/) 투표 | Prepare / Commit | 회의 참석자 |
| **Quorum (정족수)** | 다수결 확정 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) | 전체 노드의 2/3 초과 동일 메시지 수신 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | Threshold 2f+1 | 의결 정족수 |
| <strong><a href="/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a> Change</strong> | 리더 교체 메커니즘 | 리더가 죽거나 배신자일 경우 새로운 리더 선출 | [Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) 기반 | 의장 탄핵 및 재선출 |
| <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/675_digital_signature_process_asymmetric_key/">Digital Signature</a></strong> | 메시지 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 증명 | 공개키 기반으로 누가 메시지를 보냈는지 위조 방지 | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) | 인감 도장 |

3f+1 증명 구조와 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 합의의 내결함성([Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/)) 경계를 시각화한 상태도입니다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">── 전체 노드 수 N = 4 (장애 허용 f = 1)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">정상 노드 A</div><div class="kb-diagram-node">정상 노드 B</div><div class="kb-diagram-node">정상 노드 C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 진실 동의 (2개) ↑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 악의적 교란 (1개) ↓</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">배신 노드 f</div><div class="kb-diagram-note">=&gt; 거짓 메시지로 정족수 파괴 시도</div></div>
<div class="kb-diagram-note">* 정족수(Quorum) = 2f + 1 = 3표 필요</div>
<div class="kb-diagram-note">* 정상 노드 수(N-f) = 3개이므로, 배신자 1명을 무시하고 합의 가능</div>
</div>
</div>


이 구조의 핵심은 почему(왜) 2f+1이 아니라 3f+1이 필요한지를 직관적으로 보여주는 데 있습니다. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서는 네트워크 지연으로 인해 $f$개의 정상 노드가 응답하지 못할 수 있습니다. 가장 최악의 시나리오는 정상 노드 $f$개가 지연되고, 악성 노드 $f$개가 거짓말을 하는 경우입니다. 이때 응답한 노드는 전체 $N - f$개이고, 이 중 다수결을 차지하려면 절반을 초과해야 하므로 정상 응답이 악성 응답보다 많아야 합니다. 따라서 최악의 비동기 환경에서도 악의적 공격과 단순 네트워크 단절을 모두 이겨내려면 전체 노드가 3f+1개 이상이어야 합니다. 실무에서는 이러한 한계 때문에 노드 1개가 죽었을 때 견디려면 최소 4대의 서버를, 2대가 죽었을 때 견디려면 7대의 서버를 구축해야 하는 비용([TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/)) 증가를 감수해야 합니다.

📢 **섹션 요약 비유**: 회사에서 중요한 계약에 도장을 찍기 위해 임원 4명이 필요한데, 그중 1명이 산업 스파이라서 서류를 몰래 찢더라도, 나머지 3명의 임원이 서로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하여 계약을 정상 통과시키는 것과 같습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 합의 모델은 장애의 성격을 어떻게 규정하느냐에 따라 크래시 장애 허용(CFT)과 [비잔틴 장애 허용](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)([BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/))으로 나뉩니다.

CFT(Crash [Fault Tolerance](/knowledge-base/studynote/02_operating_system/11_exam_summary/800_system_architecture_fault_tolerance_dual/))와 BFT의 스펙을 비교한 매트릭스입니다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비교 항목</div><div class="kb-diagram-cell">CFT (Crash Fault)</div><div class="kb-diagram-cell">BFT (Byzantine Fault)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장애 유형</div><div class="kb-diagram-cell">서버 다운, 네트워크 끊김</div><div class="kb-diagram-cell">데이터 변조, 해킹, 거짓말</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">방어 공식</div><div class="kb-diagram-cell">N ≥ 2f + 1</div><div class="kb-diagram-cell">N ≥ 3f + 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">노드 신뢰</div><div class="kb-diagram-cell">내부망 (신뢰도 높음)</div><div class="kb-diagram-cell">외부망 (제로 트러스트)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대표 알고리즘</div><div class="kb-diagram-cell">Paxos, Raft</div><div class="kb-diagram-cell">PBFT, Tendermint</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">활용 도구</div><div class="kb-diagram-cell">Kafka, etcd, Zookeeper</div><div class="kb-diagram-cell">Hyperledger, 코스모스</div></div>
</div>
</div>


CFT 방식은 노드가 단순히 멈추는 물리적 장애만 가정하므로, 과반수(2f+1) 동의만 있으면 합의가 성립합니다. 통신 오버헤드가 적어 [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) 같은 클라우드 인프라의 내부 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)에 널리 쓰입니다. 반면 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 방식은 노드가 해킹당해 '살아 있으면서 거짓 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 뿌리는' 최악의 보안 위협을 막기 위해 훨씬 무거운 3f+1 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)을 수행합니다. 따라서 기업이 [프라이빗 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/020_private_blockchain/)을 구축할 때, 참여사가 모두 같은 계열사라면 가벼운 CFT([Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/))를 써도 되지만, 서로 이해관계가 다른 타 기업이 섞여 있다면 반드시 BFT를 적용하여 담합과 조작을 차단해야 합니다.

📢 **섹션 요약 비유**: CFT가 단순히 '결석한 학생'을 빼고 출석한 학생끼리 과제를 결정하는 것이라면, BFT는 결석자뿐만 아니라 일부러 '오답을 퍼뜨리는 분탕러 학생'까지 완벽하게 걸러내어 정답을 찾는 깐깐한 학급 회의와 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무 환경에서 순수 BFT를 대규모 퍼블릭 네트워크에 그대로 적용하는 것은 불가능에 가깝습니다. 메시지 교환량 때문입니다. 노드가 N개일 때 BFT의 통신 복잡도는 $O(N^2)$로 폭증합니다. 

따라서 실무 시스템 아키텍트는 다음의 장애 요소와 제약을 우회하기 위한 전략을 선택해야 합니다.

1. <strong>퍼블릭 <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a>의 딜레마 극복</strong>
   - 비트코인(PoW)은 BFT의 무거운 통신을 버리고, 해시 퍼즐이라는 물리적 장벽을 통해 확률적으로 비잔틴 장애를 허용하는 우회로를 택했습니다. 
   - 반면 이더리움이나 코스모스 같은 PoS 기반 최신 체인은 수만 개의 노드 중 소수의 위원회(Committee)만 무작위로 차출하여 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 투표를 진행하는 방식으로 확장성(Scalability) 병목을 해결합니다.

2. <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/020_private_blockchain/">프라이빗 블록체인</a> 노드 운영 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
   - 시스템 이중화를 명목으로 [프라이빗 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/020_private_blockchain/) 노드를 3대만 구성하는 것은 치명적 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)입니다. ($N=3$일 때, $f=0$ 즉 비잔틴 장애를 하나도 허용하지 못함). 비잔틴 방어를 위해서는 최소 4대(f=1)의 물리적으로 분리된 노드를 구성해야 합니다.

[BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 한계를 극복하기 위한 확장성 튜닝(위임 및 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/))의 의사결정 트리입니다.


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">네트워크 노드 수가 100개를 초과하는가?</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">(No, 100개 미만) --&gt; PBFT (Practical BFT) 원형 그대로 사용</div>
<div class="kb-diagram-note">(Hyperledger Fabric 등 컨소시엄망)</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">O(N^2) 통신 폭주로 네트워크 마비 위험</div></div>
<div class="kb-diagram-tree-item" style="--depth:6">해결책 A: DPoS (위임 지분 증명) - 21개 대표 노드만 BFT 수행</div>
<div class="kb-diagram-tree-item" style="--depth:6">해결책 B: Tendermint - 가십 프로토콜과 BFT 융합</div>
</div>
</div>


이 흐름의 핵심은 노드 수가 증가할 때 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 겪는 치명적인 [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 문제를 어떻게 소프트웨어적으로 잘라내느냐([Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/))입니다. BFT는 안전성은 완벽하지만 브로드캐스트의 저주를 동반합니다. 실무에서는 거대한 네트워크의 모든 노드에게 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 권한을 주지 않고, 지분 투표(DPoS)를 통해 선출된 극소수의 대표자들 사이에서만 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 메시지 교환 체계를 가동시켜 TPS 성능과 합의 안전성이라는 두 마리 토끼를 잡습니다.

📢 **섹션 요약 비유**: 전 국민 5천만 명이 카카오톡으로 실시간 토론을 하면 서버가 터지므로, 선거를 통해 국회의원 300명만 뽑아서 여의도([BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 룸)에 모아놓고 고밀도 표결을 진행하게 하는 것과 같습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 컴퓨터 과학의 이론적 난제였던 BFT는, [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 기술과 만나면서 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 금융 시스템과 중앙은행 디지털 화폐([CBDC](/knowledge-base/studynote/06_ict_convergence/01_blockchain/061_cbdc_central_bank_digital_currency/))의 핵심 인프라로 자리 잡았습니다. 

| 정량적/정성적 효과 | 비고 및 발전 방향 |
|:---|:---|
| **블록 즉각 완결성 보장** | 분기(Fork)가 발생하지 않아 금융 결제에 적합 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">제로 트러스트</a> 실현</strong> | 타 기관의 노드를 믿지 않아도 시스템 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 유지 보장 |
| <strong>비동기 <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/">BFT</a> 발전</strong> | HoneyBadger [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 등 타이밍 가정 없는 차세대 합의 엔진 등장 |

미래의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경에서는 부분 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(Partial Synchrony) 가정을 넘어, 극도의 네트워크 마비 상태(비동기) 속에서도 합의를 멈추지 않는 Asynchronous [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)(aBFT) 연구가 가속화되고 있습니다. BFT는 신뢰가 부재한 디지털 세계에서 수학적으로 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 빚어내는 가장 견고한 방패입니다.

📢 **섹션 요약 비유**: 성벽을 지키는 경비병 중 일부가 뇌물을 먹고 성문을 열어주려 해도, 겹겹이 짜인 상호 감시 시스템([BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)) 덕분에 절대로 성문이 열리지 않는 난공불락의 요새를 구축하는 것과 같습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [PBFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) ([Practical BFT](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/)) | 이론적 BFT를 현실의 비동기 네트워크 환경에서 사용할 수 있도록 최적화한 실용 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- FLP 불가능성 정리 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 비잔틴 노드가 아닌 단순 크래시 장애 하나만 있어도 완벽한 합의를 보장할 수 없다는 이론
- 크래시 장애 허용 (CFT) | 비잔틴 장애와 달리 노드의 단순 중단 현상만을 허용 범위로 두는 내부망용 합의([Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) 등) 구조
- [분산 원장 기술](/knowledge-base/studynote/06_ict_convergence/01_blockchain/474_dlt_distributed_ledger_technology/) ([DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/)) | 중앙 집중형 DB 없이 [BFT](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/) 기반의 네트워크 다수결로 동일한 원장을 유지하는 체계
- 이중 지불 공격 (Double Spending) | 악의적 노드가 똑같은 자산을 여러 번 전송하려는 비잔틴 공격의 대표적 금융 사례

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">크래시 장애 허용 (CFT, Crash Fault Tolerance) — 단순 다운만 가정</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비잔틴 장애 허용 (BFT, Byzantine Fault Tolerance) — 악의적·임의 오류까지 고려</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">실용 BFT (PBFT, Practical Byzantine Fault Tolerance) — 합의 지연을 줄인 구현</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">임계값 서명 (Threshold Signature) — 다수 서명을 압축하는 최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">비동기 BFT (aBFT, Asynchronous BFT) — 시간 가정 없이도 합의</div></div>
</div>
</div>



이 흐름은 단순 다운만 다루는 CFT에서 출발해, 악의적 오류를 견디는 BFT와 PBFT를 거쳐 타이밍 가정을 없앤 aBFT로 진화하는 합의 체계의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 여러 명의 친구들이 모여서 숨바꼭질 술래를 정할 때, 그중에 일부러 게임을 망치려는 장난꾸러기 친구가 숨어있는 상황이에요.
2. **원리**: 장난꾸러기가 계속 거짓말을 해도, 진짜 진실을 말하는 친구들이 훨씬 더 많으면 그 거짓말을 무시하고 진짜 규칙을 지켜낼 수 있어요.
3. **효과**: 나쁜 마음을 먹은 해커가 네트워크에 몰래 들어와 컴퓨터를 고장 내거나 가짜 정보를 뿌려도, 전체 시스템은 절대 무너지지 않고 튼튼하게 돌아간답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 12 / 552

← **이전**: [11. 합의 알고리즘 (Consensus Algorithm) - 분산 노드 간 상태 일치 달성 매커니즘](/knowledge-base/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)
**다음**: [13. PBFT (Practical BFT) - 다수결 기반 상태 기계 복제 합의 (텐더민트, 하이퍼레저)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/013_pbft_practical_bft/) →

---
