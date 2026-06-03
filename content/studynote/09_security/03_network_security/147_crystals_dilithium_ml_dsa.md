+++
title = "147. CRYSTALS-Dilithium (ML-DSA) — 격자 기반 디지털 서명"
date = 2026-04-19

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CRYSTALS-Dilithium(크리스탈스-딜리시움)은 격자(Lattice) 수학 문제의 어려움에 기반한 양자 내성(Post-[Quantum](/knowledge-base/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/), [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/)) 디지털 서명 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, NIST(National Institute of Standards and Technology)가 2024년 ML-DSA([Module](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) Lattice-Based [Digital Signature](/knowledge-base/studynote/03_network/13_network_security_basics/675_digital_signature_process_asymmetric_key/) [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/), FIPS 204)로 표준화했다.
> 2. **가치**: [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)([Quantum Computer](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/))가 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)·[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) 기반 기존 디지털 서명을 수초 내에 파괴할 수 있는 시대를 대비해, <strong>양자 공격에 안전한 디지털 서명 표준</strong>으로 인터넷·[PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/)([Public Key Infrastructure](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/)) 인프라를 미래 보호한다.
> 3. **판단 포인트**: Dilithium은 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)/[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) 대비 공개키·서명 크기가 크지만 서명 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 속도가 빠르고 구현이 단순하여, <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 1.3·<a href="/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/">코드 서명</a>·<a href="/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/">PKI</a> 인증서 대체</strong>의 1순위 후보다.

---

## Ⅰ. 개요 및 필요성

디지털 서명은 메시지의 무결성과 발신자 인증을 보장하는 암호 기술이다. 현재 인터넷 보안의 근간인 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)·[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/)(Elliptic Curve [Digital Signature](/knowledge-base/studynote/03_network/13_network_security_basics/675_digital_signature_process_asymmetric_key/) [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))는 소인수분해와 이산대수 문제의 어려움에 의존한다. 그러나 Shor [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 구현한 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)가 등장하면 이 두 문제 모두 다항 시간([Polynomial](/knowledge-base/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) Time)에 풀린다.

NIST는 2016년 [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 표준화 공모를 시작했고, CRYSTALS-Dilithium이 최종 선발되어 2024년 **FIPS 204(ML-DSA)** 로 발표됐다. 이는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)·[SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)·[코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/)·[PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) 인증서·스마트카드 전 영역에 영향을 미친다.

<strong>Dilithium 없으면(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/">PQC</a> 전환 없으면) 발생하는 위험</strong>:
- "지금 암호화, 나중에 해독(Harvest Now, Decrypt Later)" 공격 — 지금 수집한 암호문을 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/) 완성 후 해독
- 인터넷 [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) 기반 신뢰 체계 붕괴
- [HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/), [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/), [코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/), 전자 계약 등 전면 무력화

- **📢 섹션 요약 비유**: CRYSTALS-Dilithium은 <strong>'<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/">양자 컴퓨터</a>라는 만능 마스터키가 등장하기 전에 교체하는 새로운 자물쇠(디지털 서명 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>)'</strong> 입니다. 기존 자물쇠([RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)/[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/))는 양자 드릴로 1초 만에 열리지만, 격자 수학으로 만든 새 자물쇠는 양자 드릴도 뚫지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 격자(Lattice) 기반 보안의 기초



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">격자(Lattice) 수학 개념</div>
<div class="kb-diagram-note">격자: n차원 공간에서 기저 벡터의 정수 선형 결합으로 이루어진 점의 집합</div>
<div class="kb-diagram-note">기저 벡터</div>
<div class="kb-diagram-note">b1 = (1, 0) b2 = (0, 1)</div>
<div class="kb-diagram-note">격자 점: 모든 a·b1 + b·b2 (a, b ∈ 정수)</div>
<div class="kb-diagram-note">어려운 문제:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SVP (Shortest Vector Problem):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">격자에서 가장 짧은 벡터 찾기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 고차원일수록 고전+양자 컴퓨터도 어려움</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LWE (Learning With Errors):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">선형 방정식에 노이즈를 추가 → 역산 불가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ Dilithium의 보안 기반</div></div>
</div>
</div>



CRYSTALS-Dilithium은 <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a>-LWE(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a> <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a> With Errors)</strong> 와 <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a>-SIS(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a> Short Integer Solution)</strong> 문제의 어려움에 기반한다.

### 2. Dilithium 키·서명 크기 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 공개키 크기 | 서명 크기 | 보안 레벨 |
|:---|:---:|:---:|:---|
| [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)-2048 | 256 B | 256 B | 128-bit (양자에 취약) |
| [ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) [P-256](/knowledge-base/studynote/09_security/03_network_security/123_p_256/) | 64 B | 64 B | 128-bit (양자에 취약) |
| **Dilithium2 (ML-DSA-44)** | **1,312 B** | **2,420 B** | 128-bit (양자 내성) |
| **Dilithium3 (ML-DSA-65)** | **1,952 B** | **3,293 B** | 192-bit (양자 내성) |
| **Dilithium5 (ML-DSA-87)** | **2,592 B** | **4,595 B** | 256-bit (양자 내성) |

### 3. Dilithium 서명 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">키 생성: (공개키 pk, 비밀키 sk) ← KeyGen()</div>
<div class="kb-diagram-note">sk: 랜덤 행렬 + 작은 다항식 벡터</div>
<div class="kb-diagram-note">pk: 행렬 A와 t = A·s1 + s2 (s1, s2 작은 벡터)</div>
<div class="kb-diagram-note">서명: σ ← Sign(sk, 메시지 M)</div>
<div class="kb-diagram-note">반복: 랜덤 y 생성 → w = A·y → c = H(pk, M, w) → z = y + c·s1</div>
<div class="kb-diagram-note">조건: z, r0 = w - c·s2 의 크기가 임계값 이내이면 서명 완성</div>
<div class="kb-diagram-note">검증: Verify(pk, M, σ)</div>
<div class="kb-diagram-note">z 크기 확인 + w' = A·z - c·t 재계산 → H(pk, M, w') == c?</div>
</div>
</div>



- **📢 섹션 요약 비유**: Dilithium 서명은 **'노이즈가 섞인 수학 퍼즐에 비밀열쇠로 도장 찍기'** 입니다. 도장(서명)을 찍으려면 비밀열쇠가 있어야 하고, 노이즈가 섞인 답이 올바른 범위 안에 들어오는지 확인합니다. [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)도 노이즈 퍼즐은 못 풀어냅니다.

---

## Ⅲ. 비교 및 연결

### [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 디지털 서명 후보군 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 기반 | 장점 | 단점 |
|:---|:---|:---|:---|
| **ML-DSA (Dilithium)** | 격자(Lattice) | 빠른 서명·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 구현 단순 | 큰 서명 크기 |
| <strong><a href="/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/">SLH-DSA</a> (<a href="/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/">SPHINCS</a>+)</strong> | [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) | 수학 가정 최소 (해시만 의존) | 매우 큰 서명 (수십 KB) |
| **FN-DSA (FALCON)** | 격자(NTRU) | 작은 서명 크기 | 구현 복잡([부채널 공격](/knowledge-base/studynote/02_operating_system/10_security/668_side_channel_attack_meltdown_spectre_kpti/) 취약) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/">ECDSA</a></strong> | 이산대수 | 작은 크기, 범용 지원 | 양자에 취약 |

### 연결 개념 흐름

[RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)/[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) 취약점([양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)) → [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 필요성 → NIST [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 표준화 → ML-DSA(Dilithium), [ML-KEM](/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/)(Kyber), [SLH-DSA](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/)([SPHINCS](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/)+) → 하이브리드 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)(기존+[PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 병행) → 완전 [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 전환

- **📢 섹션 요약 비유**: [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 서명 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택은 **'방탄 조끼 소재 선택'** 과 같습니다. ML-DSA(격자)는 무게(크기)는 좀 있지만 방탄 성능이 우수하고 착용이 쉽습니다. [SLH-DSA](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/)(해시)는 신뢰성은 최고지만 너무 무겁습니다. FALCON은 가볍지만 제조(구현)가 까다롭습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 의사결정 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 상황 | 권장 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 이유 |
|:---|:---|:---|
| [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 인증서·핸드셰이크 | ML-DSA (Dilithium3) | 속도·범용성 균형 |
| [코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/) (장기 유효성) | [SLH-DSA](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/) ([SPHINCS](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/)+) | 수학적 가정 최소 = 장기 신뢰 |
| 소형 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스 서명 | FALCON (FN-DSA) | 작은 크기 (리소스 제약) |
| 전환 기간 (현재~3년) | 하이브리드 ([ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) + ML-DSA) | [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 유지 |

### 기술사 시험 핵심 포인트

1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/">PQC</a>(<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">Post-Quantum Cryptography</a>)</strong>: [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/) 공격에 안전한 암호 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 총칭
2. **Harvest Now, Decrypt Later**: 현재의 암호문을 저장해 미래 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)로 해독하는 장기 공격
3. **ML-DSA = FIPS 204 = Dilithium**: 동일 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 세 가지 이름
4. **하이브리드 서명**: 전환 기간 중 [ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) + ML-DSA를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 서명·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/">PQC</a> 전환을 "<a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/">양자 컴퓨터</a> 완성 후"로 미루기</strong>: "지금 수확, 나중 해독" 공격은 현재 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다. 국가 기밀, 금융 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 지금 수집되어 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/) 완성 후 해독될 수 있다. 장기 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 <strong>지금 즉시 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/">PQC</a> 전환</strong>이 필요하다.

- **📢 섹션 요약 비유**: [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 전환 지연은 **'도둑이 지금 금고를 통째로 가져가고, 나중에 열쇠를 구하면 열겠다고 기다리는 상황'** 입니다. 금고(암호화된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 이미 도둑 손에 있고, [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)(열쇠)만 기다리면 됩니다. 지금 바꾸지 않으면 미래의 자신이 당합니다.

---

## Ⅴ. 기대효과 및 결론

CRYSTALS-Dilithium(ML-DSA)은 NIST가 공식 채택한 [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 디지털 서명 표준으로, 향후 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20년 내 인터넷 보안 인프라의 서명 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 기반을 교체하는 대규모 전환의 핵심이다.

**한계**: [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)·[ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/) 대비 공개키와 서명 크기가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~40배 크다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크 패킷 크기 증가, X.509 인증서 크기 증가, 메모리·[대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 제약 환경에서의 제한이 존재한다. 경량 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경에서는 FALCON이나 해시 기반 서명이 더 적합할 수 있다.

**미래 방향**: ① [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) RFC를 통한 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 확장 표준화, ② X.509 [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 인증서 프로파일 확정, ③ [HSM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/)([Hardware Security Module](/knowledge-base/studynote/09_security/03_network_security/157_hsm_hardware_security_module/))·[PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) 솔루션의 ML-DSA 지원 확산, ④ [양자 내성 암호](/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)([ML-KEM](/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/) + ML-DSA) 풀 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 전환.

ML-DSA는 "더 좋은 서명이 아니라, 살아남기 위한 필수 서명"이다 — 양자 시대를 대비한 인터넷 신뢰 체계의 재건이라는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: ML-DSA로의 전환은 **'내진 설계가 없는 건물에 내진 보강재를 추가하는 리노베이션'** 입니다. 지진([양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/))이 오기 전에 보강하지 않으면, 순식간에 무너집니다. 건물이 멀쩡해 보여도 내진 기준이 바뀌면 반드시 보강해야 합니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/">PQC</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">Post-Quantum Cryptography</a>)</strong> | Dilithium이 속한 [양자 내성 암호](/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| <strong><a href="/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/">ML-KEM</a> (CRYSTALS-Kyber)</strong> | [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 키 캡슐화 메커니즘; Dilithium(서명)과 함께 NIST [PQC](/knowledge-base/studynote/12_it_management/05_security_compliance/351_quantum_computing_pqc_transition/) 쌍둥이 표준 |
| **격자(Lattice) 암호** | SVP, LWE 등 수학 난제 기반; 현재 PQC의 주류 방향 |
| **FIPS 204** | NIST가 발행한 ML-DSA(Dilithium) 공식 표준 번호 |
| **Harvest Now, Decrypt Later** | 현재 암호문 수집 후 미래 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)로 해독하는 위협 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RSA / ECDSA (고전 암호 디지털 서명)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">양자 컴퓨터 위협 → Shor 알고리즘 → RSA/ECDSA 파괴 가능</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NIST PQC 표준화 공모 (2016~2024)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─► ML-DSA (Dilithium) — 격자 기반 서명</div><div class="kb-diagram-node">FIPS 204</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─► SLH-DSA (SPHINCS+) — 해시 기반 서명</div><div class="kb-diagram-node">FIPS 205</div></div>
<div class="kb-diagram-tree-item" style="--depth:2">FN-DSA (FALCON) — 격자(NTRU) 기반 서명</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">하이브리드 전환 (ECDSA + ML-DSA 병행)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">완전 PQC 전환 — TLS, PKI, 코드 서명, IoT</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 인터넷의 도장(디지털 서명)은 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)·ECDSA라는 자물쇠로 만들어졌는데, <strong><a href="/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/">양자 컴퓨터</a>가 등장하면 이 자물쇠를 1초 만에 열 수 있어요!</strong> 그래서 새로운 자물쇠가 필요해요.
2. CRYSTALS-Dilithium은 <strong>격자(Lattice)라는 수학 미로</strong>에 기반한 새 자물쇠예요. 이 미로는 [양자 컴퓨터](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)도 빠져나오지 못할 만큼 복잡하게 설계되어 있어요!
3. 크기가 기존보다 크지만(공개키·서명이 더 길지만), 미래에도 <strong>인터넷 도장의 신뢰를 지킬 수 있는 유일한 방법</strong>이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 200 / 1108

← **이전**: [146. ML-KEM (구 CRYSTALS-Kyber)](/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/)
**다음**: [148. FALCON — 격자 기반 서명, 짧은 서명](/knowledge-base/studynote/09_security/03_network_security/148_falcon_fn_dsa/) →

---
