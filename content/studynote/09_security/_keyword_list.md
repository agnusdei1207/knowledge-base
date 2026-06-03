---
title: 09. 정보보안 키워드 목록
date: '2026-03-25'
tags:
- studynote-security
---
[[267_weight_bias_activation|weight]] = 9999

# 정보보안 (Information [[283_security_tactics|Security]]) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 보안 전 영역 기술사 수준 핵심 키워드
> ⚡ 기술사 보안 문제는 단순 지식이 아닌 **[[611_threat_modeling|위협 모델링]] → 아키텍처 설계 → 법적·제도적 대응**까지 통합 서술을 요구함

---

## 1. 정보보안 개론 / 원칙 — 67개

1. 정보보안 3요소 — CIA ([[002_confidentiality|기밀성]]·[[003_integrity|무결성]]·[[452_availability|가용성]])
2. [[002_confidentiality|기밀성]] ([[002_confidentiality|Confidentiality]]) — 암호화, 접근 제어, [[119_drm_data_reference_model_standard|DRM]], [[104_classification_analysis|분류]]
3. [[003_integrity|무결성]] ([[003_integrity|Integrity]]) — 해시, [[675_digital_signature_process_asymmetric_key|전자서명]], [[673_mac_message_authentication_code|MAC]], [[674_hmac_hash_based_mac_ipsec|HMAC]], [[112_checksum|체크섬]]
4. [[452_availability|가용성]] ([[452_availability|Availability]]) — HA 설계, [[483_raid_overview|RAID]], 부하 [[136_variance|분산]], DDoS 방어, [[085_sla|SLA]]
5. [[005_authenticity|인증성]] ([[005_authenticity|Authenticity]]) — 신원 [[396_validation|확인]], [[159_pki_public_key_infrastructure|PKI]], 디지털 서명, 메시지 [[303_authentication_authorization_patterns|인증]]
6. 부인방지 (Non-repudiation) — [[675_digital_signature_process_asymmetric_key|전자서명]], 타임스탬프, [[568_logs_distributed_logging_elk_fluentd|로그]], [[606_auditing_linux_auditd|감사]] 추적
7. 책임추적성 (Accountability) — [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]], [[606_auditing_linux_auditd|감사]] 기록, 사용자 행동 추적
8. [[803_privacy_law_comparison|개인정보보호]] 3요소 — [[002_confidentiality|기밀성]]·[[003_integrity|무결성]]·[[292_accessibility_kwcag_wcag|접근성]] ([[844_iso_27701_pims|ISO 27701]])
9. 정보보안 6요소 — CIA + [[005_authenticity|인증성]] + 부인방지 + 책임추적성
[[489_raid_10_hybrid|10]]. [[010_least_privilege|최소 권한 원칙]] (Principle of [[010_least_privilege|Least Privilege]]) — 필요 알 권리
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_separation_of_duties|직무 분리 원칙]] ([[011_separation_of_duties|Separation of Duties]]) — 4눈 원칙, [[136_variance|분산]] 통제
12. [[012_defense_in_depth|다단계 인증 원칙]] ([[012_defense_in_depth|Defense in Depth]]) — 심층 방어
13. [[013_need_to_know|알 필요성 원칙]] ([[013_need_to_know|Need-to-Know]]) — 정보 접근 제한
14. [[014_simplicity|단순 보안 원칙]] ([[014_simplicity|Simplicity]]) — 불필요한 복잡성 제거
15. [[015_open_design|공개 설계 원칙]] ([[015_open_design|Open Design]]) — 키 은닉，而非 算法 은닉
16. 실패 안전 원칙 ([[459_fail_safe|Fail-Safe]]) — 기본값 거부, 오류 시 [[298_safe_state|안전 상태]]
17. 완전한 중재 원칙 (Complete Mediation) — 모든 접근 경로 검사
18. 경제적 설계 원칙 (Economy of Mechanism) — 최소 구현
19. [[019_ai_emerging_tech|완전한 통제 원칙]] (Open Platform for [[283_security_tactics|Security]]) — 분리 [[571_protection_vs_security|보호]]
20. Least Common Mechanism — 메커니즘 공유 최소화
21. [[021_psychological_acceptability_principle|심리적 사용성 원칙]] ([[021_psychological_acceptability_principle|Psychological Acceptability]]) — 보안이 [[286_usability_tactics|사용성]]을 해치면 안 됨
22. 정보보안 [[164_policy|정책]] — 최고 경영진 승인, 문서화된 규칙
23. 정보보안 표준 — [[164_policy|정책]]實施 위한 구체적 기준
24. 정보보안 지침 — 표준 적용 방법론
25. 정보보안 절차 — 구체적 작업 지침
26. [[026_risk_management_process|위험 관리 프로세스]] — [[655_ir_detection_analysis|식별]]/분석/평가/대응/모니터링/보고
27. [[027_risk_identification|위험 식별]] ([[027_risk_identification|Risk Identification]]) — 자산·위협·취약점 목록화
28. [[028_quantitative_risk_analysis|정량적 위험 분석]] — [[032_ale_annual_loss_expectancy|ALE]] = ARO × SLE, [[450_mtbf|MTBF]], [[360_mttf|MTTF]], [[451_mttr|MTTR]]
29. [[029_qualitative_risk_analysis|정성적 위험 분석]] — High/Medium/Low 매트릭스
30. SLE (Single Loss Expectancy) — 단일 사고 예상 손실
31. ARO (Annual Rate of Occurrence) — 연간 발생 [[130_probability|확률]]
32. [[032_ale_annual_loss_expectancy|ALE]] (Annual Loss Expectancy) — 연간 예상 손실
33. [[033_risk_response_strategies|위험 대응 전략]] 4가지 — 회피/전가/완화/수용
34. 위험 회피 ([[034_risk_avoidance|Risk Avoidance]]) — 위험 원천 제거
35. [[051_risk_transfer|위험 전가]] ([[051_risk_transfer|Risk Transfer]]) — 보험, 외주, 계약 조항
36. [[052_risk_mitigation|위험 완화]] ([[036_risk_mitigation|Risk Mitigation]]) — 통제措施 도입으로 위험 감소
37. [[037_risk_acceptance|위험 수용]] ([[037_risk_acceptance|Risk Acceptance]]) —管理层 승인 하에
38. [[038_residual_risk|잔여 위험]] ([[038_residual_risk|Residual Risk]]) — 통제 후 남은 위험
39. 검출 위험 (Detected [[096_risk_non_risk_architecture_evaluation_flaws|Risk]]) vs 미검출 위험 (Undetected [[096_risk_non_risk_architecture_evaluation_flaws|Risk]])
40. [[040_inherited_risk|inherited Risk]] — [[040_inherited_risk|상속된 위험]]
41. [[302_security_architecture_design|보안 아키텍처]] — [[112_zachman_framework|Zachman Framework]] (6×6 매트릭스)
42. [[042_sabsa|SABSA]] (Sherwood Applied Business [[302_security_architecture_design|Security Architecture]]) — 수평×수직 매트릭스
43. [[043_osa|OSA]] ([[043_osa|Open Security Architecture]]) — [[302_security_architecture_design|보안 아키텍처]] 패턴 [[394_catalog_metadata|카탈로그]]
44. [[113_togaf|TOGAF]] ([[113_togaf|The Open Group]] [[319_architecture|Architecture]] Framework) — 아키텍처 개발 方法论
45. NIST [[017_csf|CSF]] 2.0 — Identify/Protect/Detect/Respond/Recover + Govern
46. [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) — "Never Trust, Always Verify", [[850_nist_sp_800_207|NIST SP 800-207]]
47. [[047_zta|ZTA]] ([[184_zero_trust_architecture|Zero Trust Architecture]]) — NIST 4단계 구현 로드맵
48. [[048_sdp|SDP]] (Software Defined Perimeter) —的软件 정의 경계
49. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] — 워크로드별 격리, 측면 이동 차단
50. East-West 트래픽 통제 — 내부 [[364_segmentation|세그멘테이션]]
51. North-South 트래픽 통제 — 경계 방어
52. 보안 통제 3가지 유형 — 관리적/기술적/물리적
53. [[053_preventive_controls|예방 통제]] ([[053_preventive_controls|Preventive Controls]]) — 사전 차단
54. [[054_detective_controls|탐지 통제]] ([[054_detective_controls|Detective Controls]]) — 이상 징후 발견
55. [[055_corrective_controls|교정 통제]] ([[055_corrective_controls|Corrective Controls]]) — 사고 후 [[658_ir_recovery|복구]]
56. [[056_deterrent_controls|억제 통제]] ([[056_deterrent_controls|Deterrent Controls]]) — 위협 행동 [[656_ir_containment|억제]]
57. 상실 통제 ([[057_compensating_controls|Compensating Controls]]) — 기존 통제 우회 조치
58. [[058_security_by_design|내재적 보안]] ([[058_security_by_design|Security by Design]]) — 설계 단계 보안 고려
59. [[059_bolt_on_security|사후 보안]] ([[059_bolt_on_security|Bolt-on Security]]) — 완성 후 보안 추가
60. [[060_privacy_by_design|Privacy by Design]] 7基本原则 — 사전 [[571_protection_vs_security|보호]], 기본값私密性 등
61. [[061_secure_by_default|Secure by Default]] — 기본적으로 안전한 기본값
62. [[190_secure_coding_guideline|Secure Coding]] — 안전한 소프트웨어 개발
63. [[611_threat_modeling|Threat Modeling]] — [[097_stride_convolutional_neural_network_downsampling|STRIDE]], DREAD, [[642_mitre_attack|MITRE ATT&CK]] 맵핑
64. DREAD 모델 — Damage/Reproducibility/Exploitability/Affected Users discoverability
65. [[097_stride_convolutional_neural_network_downsampling|STRIDE]] 모델 — [[598_spoofing|Spoofing]]/Tampering/Repudiation/Information Disclosure/[[599_dos_ddos_attack|DoS]]/Elevation
66. [[066_pasta_threat_modeling|PASTA]] ([[300_process|Process]] for Attack Simulation and Threat Analysis) — 7단계 [[611_threat_modeling|위협 모델링]]
67. [[067_attack_surface_analysis|Attack Surface Analysis]] — 공격 표면 관리

---

## 2. [[652_cryptography_concept_encryption_decryption|암호학]] 기초 — 42개

68. [[652_cryptography_concept_encryption_decryption|암호학]] ([[652_cryptography_concept_encryption_decryption|Cryptography]]) — [[002_confidentiality|기밀성]]·[[003_integrity|무결성]]·[[303_authentication_authorization_patterns|인증]]·부인방지 제공
69. 고전 암호 — 치환 암호, 전치 암호
70. 凯撒 암호 ([[070_caesar_cipher|Caesar Cipher]]) — 알파벳 3자리 이동
71. 단일 치환 암호 — 하나의 알파벳을 하나의 문자로 치환
72. [[072_vigenere_cipher|다중 치환 암호]] (Vigenère Cipher) — 키워드 기반 복수 치환
73. [[073_enigma|Enigma]] — 독일 제2차 세계대전 기계식 암호
74. 一次性密码本 ([[074_one_time_pad|One-Time Pad]]) — 정보 이론적으로 완벽한 안전성
75. 현대 [[652_cryptography_concept_encryption_decryption|암호학]] 기본 가정 — computationally infeasible
76. [[076_symmetric_encryption|대칭키 암호]] ([[076_symmetric_encryption|Symmetric Encryption]]) — 동일한 키로 암호화/복호화
77. [[077_asymmetric_encryption|비대칭키 암호]] ([[077_asymmetric_encryption|Asymmetric Encryption]]) — 공개키/비밀키 쌍
78. 하이브리드 암호 — 대칭+비대칭 결합 (키 교환+[[001_dikw_pyramid|데이터]] 암호화)
79. [[655_block_cipher_des_3des_feistel|블록 암호]] ([[655_block_cipher_des_3des_feistel|Block Cipher]]) — 고정 크기 블록 단위 암호화
80. [[654_stream_cipher_rc4_chacha20|스트림 암호]] ([[654_stream_cipher_rc4_chacha20|Stream Cipher]]) — [[073_bit|비트]]/[[074_byte|바이트]] 단위 실시간 암호화
81. [[081_rc4_stream_cipher|RC4]] — [[654_stream_cipher_rc4_chacha20|스트림 암호]], 취약점 발견으로 사용 중단 ([[580_wep_wired_equivalent_privacy_rc4|WEP]])
82. Salsa20/ChaCha20 — ARX 기반 [[654_stream_cipher_rc4_chacha20|스트림 암호]], [[694_thread_local_storage_tls|TLS]] 1.3
83. [[656_aes_advanced_encryption_standard_rijndael|AES]] ([[656_aes_advanced_encryption_standard_rijndael|Advanced Encryption Standard]]) — 128/192/256비트 키
84. [[656_aes_advanced_encryption_standard_rijndael|AES]] SPN 구조 — SubBytes/ShiftRows/MixColumns/AddRoundKey
85. [[656_aes_advanced_encryption_standard_rijndael|AES]] 키 [[208_schedule_history_transaction_execution_order|스케줄]] — 라운드 키 [[087_process_state_transition|생성]]
86. [[086_des_data_encryption_standard|DES]] ([[086_des_data_encryption_standard|Data Encryption Standard]]) — 56비트 키, 취약
87. [[087_3des|3DES]] ([[087_3des|Triple DES]]) — 168비트 (112비트 실효 강도)
88. [[655_block_cipher_des_3des_feistel|블록 암호]] 모드 — ECB/[[089_cbc_mode|CBC]]/CFB/OFB/[[090_ctr_mode|CTR]]
89. [[089_cbc_mode|CBC]] ([[089_cbc_mode|Cipher Block Chaining]]) — [[459_quic_fec_forward_error_correction|초기]]화 벡터([[288_version_ihl_tos_total_length|IV]]) 필요, 체인 의존성
90. [[090_ctr_mode|CTR]] ([[059_counter|Counter]]) — 난수 대신 [[059_counter|카운터]], [[430_index_fast_full_scan|병렬]] 처리 가능
91. [[659_gcm_galois_counter_mode_aead|GCM]] (Galois/[[059_counter|Counter]] Mode) — [[092_aead|AEAD]], [[303_authentication_authorization_patterns|인증]] 암호화
92. [[092_aead|AEAD]] (Authenticated Encryption with Associated [[001_dikw_pyramid|Data]]) — 암호화+[[303_authentication_authorization_patterns|인증]] 동시
93. [[093_cca|CCA]] ([[093_cca|Chosen Ciphertext Attack]]) — 암호문 공격 [[104_classification_analysis|분류]]
94. [[094_cpa|CPA]] (Chosen Plaintext Attack) — 평문 공격 [[104_classification_analysis|분류]]
95. [[095_ind_cpa|IND-CPA]] ([[095_ind_cpa|Indistinguishability under CPA]]) — [[652_cryptography_concept_encryption_decryption|암호학]]적 안전성 정의
96. IND-CCA2 — 강인한 [[652_cryptography_concept_encryption_decryption|암호학]]적 안전성
97. [[667_hash_function_integrity_one_way|해시 함수]] — 단방향성, 충돌 [[003_resistance|저항]]성, Preimage [[003_resistance|저항]]성
98. [[668_md5_hash_collision_vulnerability|MD5]] — 128비트 해시, 충돌 공격 실용화 ([[098_md5|1996]])
99. SHA-1 — 160비트, SHA-1 충돌 발견 (2017, SHAttered)
100. SHA-2 — SHA-224/256/384/512, 현재 표준
101. [[101_sha_3|SHA-3]] ([[101_sha_3|Keccak]]) — sponge construction, NIST 2015
102. BLAKE2/BLAKE3 — 채택성능 해시, [[656_aes_advanced_encryption_standard_rijndael|AES]] 대체
103. [[674_hmac_hash_based_mac_ipsec|HMAC]] (Hash-based [[673_mac_message_authentication_code|Message Authentication Code]]) — 키掺入 해시
104. [[104_nmac|NMAC]] ([[104_nmac|Nested MAC]])
105. [[105_cmac|CMAC]] ([[105_cmac|Cipher-based MAC]]) — [[655_block_cipher_des_3des_feistel|블록 암호]] 기반
106. [[106_gmac|GMAC]] ([[106_gmac|Galois MAC]]) — GCM의 [[303_authentication_authorization_patterns|인증]] 부분
107. [[107_rainbow_table|rainbow table]] — 사전 계산 [[067_hash_table|해시 테이블]], 역산 공격
108. [[671_password_hash_salt_pbkdf2_bcrypt_argon2|salt]] — [[563_hash_collision_chaining_linear_probing|해시 충돌]] 방지를 위한 난수 추가
109. [[109_key_stretching|키 스트레칭]] — PBKDF2, bcrypt, scrypt (메모리 하드)

---

## 3. [[652_cryptography_concept_encryption_decryption|암호학]] 심화 / [[159_pki_public_key_infrastructure|PKI]] — 52개

110. [[110_rsa|RSA]] — 소인수분해 문제 기반, 1977년 Rivest/Shamir/Adleman
111. [[110_rsa|RSA]] 키 [[087_process_state_transition|생성]] — 두 소수의 곱, 오일러 파이 함수
112. [[112_rsa_oaep|RSA-OAEP]] — 최적 [[077_asymmetric_encryption|asymmetric encryption]] [[098_padding_convolutional_neural_network_same_valid|padding]], CCA2 안전성
113. [[113_rsa_pss|RSA-PSS]] — [[130_probability|확률]]적 서명 방식, [[093_safe_scaled_agile_framework_art_pi|safe]] 서명
114. [[114_modulo_arithmetic|modulo 연산]] — [[110_rsa|RSA]] 핵심인 나머지 연산
115. Carmichael 수 — [[110_rsa|RSA]] 안전성 분석 관련
116. [[663_macos_ios_gcd_grand_central_dispatch|GCD]] ([[116_gcd_rsa|최대공약수]]) — [[110_rsa|RSA]] 키 [[087_process_state_transition|생성]]에서 사용
117. [[117_extended_euclidean_algorithm|확장 유클리드 알고리즘]] — [[192_module_independence|모듈]]로 역수 계산
118. [[124_crt|CRT]] (Chinese Remainder Theorem) — [[110_rsa|RSA]] 복호화 최적화
119. [[554_ecc_circuit|ECC]] ([[119_ecc_elliptic_curve_cryptography|Elliptic Curve Cryptography]]) — [[120_elliptic_curve_equation|타원곡선]] 이산 [[568_logs_distributed_logging_elk_fluentd|로그]] 문제
120. [[120_elliptic_curve_equation|타원곡선]] — y² = x³ + ax + b 꼴의 곡선
121. [[121_ecdlp|ECDLP]] (Elliptic Curve Discrete Log Problem) — [[554_ecc_circuit|ECC]] 안전성 기반
122. [[122_secp256k1|secp256k1]] — Bitcoin에서 사용되는 곡선
123. [[123_p_256|P-256]] ([[123_p_256|secp256r1]]) — NIST 권장 곡선
124. P-384 / P-521 — NIST 고강도 곡선
125. [[097_ecdsa_schnorr_signature_bitcoin|ECDSA]] ([[125_ecdsa|Elliptic Curve DSA]]) — [[554_ecc_circuit|ECC]] 기반 디지털 서명
126. EdDSA / Ed25519 — Edwards 곡선, 결정론적 서명
127. [[127_x25519|X25519]] — ECDH를 Edwards 곡선에서 구현
128. [[128_dh_diffie_hellman|DH]] (Diffie-Hellman) — 이산 [[568_logs_distributed_logging_elk_fluentd|로그]] 기반 키 교환
129. [[129_dhe_ephemeral_dh|DHE]] ([[129_dhe_ephemeral_dh|Ephemeral DH]]) — 임시 [[128_dh_diffie_hellman|DH]], [[139_pfs_perfect_forward_secrecy|전방 비밀성]](PFS) 제공
130. [[130_ecdh|ECDH]] — [[554_ecc_circuit|ECC]] 기반 효율적 키 교환
131. [[131_ecdhe_ephemeral_ecdh|ECDHE]] — Ephemeral [[130_ecdh|ECDH]], [[694_thread_local_storage_tls|TLS]] 1.3 기본
132. [[132_key_exchange_protocol_mitm|키교환 프로토콜]] — [[706_mitm_man_in_the_middle_hsts|중간자 공격]] 방지를 위한 상호 [[303_authentication_authorization_patterns|인증]]
133. [[937_hybrid_encryption|Hybrid Encryption]] — [[134_kem_key_encapsulation|KEM]]/[[135_dem_data_encapsulation|DEM]] 분리 구조 (ISO 18033-2)
134. [[134_kem_key_encapsulation|KEM]] ([[134_kem_key_encapsulation|Key Encapsulation Mechanism]]) — 키 포장
135. [[135_dem_data_encapsulation|DEM]] ([[135_dem_data_encapsulation|Data Encapsulation Mechanism]]) — [[001_dikw_pyramid|데이터]] 암호화
136. [[136_hkdf|HKDF]] ([[674_hmac_hash_based_mac_ipsec|HMAC]]-based [[505_password_storage_kdf_salt|Key Derivation Function]]) — RFC 5869
137. [[694_thread_local_storage_tls|TLS]] 1.3 핸드셰이크 — 1-RTT, 0-RTT, [[142_psk_pre_shared_key|PSK]]
138. [[092_aead|AEAD]] 요구 — [[694_thread_local_storage_tls|TLS]] 1.3은 [[092_aead|AEAD]] 암호만 허용
139. [[139_pfs_perfect_forward_secrecy|전방 비밀성]] (PFS) — 과거 [[140_session_key|세션 키]] 유출해도 과거 통신 [[571_protection_vs_security|보호]]
140. [[140_session_key|세션 키]] — 임시 [[160_session_controlling_terminal|세션]]용短期密钥
141. [[141_master_secret|마스터 시크릿]] — Pre-Master Secret에서 파생
142. [[142_psk_pre_shared_key|PSK]] (Pre-Shared [[067_db_key_uniqueness_minimality|Key]]) — 사전 공유 키
143. [[143_diffie_hellman_gruppen|Diffie-Hellman Gruppen]] — RFC 3526 소수 그룹
144. [[144_hkdf_tls_1_3|키 파생 함수]] — [[694_thread_local_storage_tls|TLS]] 1.3의 [[136_hkdf|HKDF]]-Extract/Expand
145. NIST [[351_quantum_computing_pqc_transition|PQC]] 표준화 — 2016년 시작, 2024년 4개 [[001_algorithm_definition|알고리즘]] 선정
146. CRYSTALS-Kyber — 격자 기반 [[134_kem_key_encapsulation|KEM]], NIST [[351_quantum_computing_pqc_transition|PQC]] 표준
147. [[147_crystals_dilithium_ml_dsa|CRYSTALS-Dilithium]] — 격자 기반 디지털 서명, NIST [[351_quantum_computing_pqc_transition|PQC]]
148. FALCON — 격자 기반 서명, 짧은 서명
149. [[149_sphincs_slh_dsa|SPHINCS]]+ — 해시 기반 서명, 양자 내성
150. BIKE / HQC / Classic McEliece — 코드 기반 [[351_quantum_computing_pqc_transition|PQC]]
151. [[236_quantum_computing_pqc|양자 컴퓨팅]] 위협 — Shor [[001_algorithm_definition|알고리즘]] ([[110_rsa|RSA]]/[[554_ecc_circuit|ECC]] 깨뜨림), [[986_grover_algorithm_impact|Grover]] ([[656_aes_advanced_encryption_standard_rijndael|AES]] 128→64)
152. "Harvest Now, Decrypt Later" — 양자 위협 대응 [[268_strategy_pattern|전략]]
153. .[[153_crypto_agility|crypto agility]] — [[001_algorithm_definition|알고리즘]] 교체 능력, [[351_quantum_computing_pqc_transition|PQC]] 이전 준비
154. 키 관리 생명주기 — [[087_process_state_transition|생성]]/분배/저장/사용/순환/폐기
155. [[155_key_destruction_crypto_shredding|키 폐기]] — 안전한 삭제, 키 재료 완전 소멸
156. [[156_key_rotation|키 순환]] — 정기적 키 교체, 유출 시 [[658_ir_recovery|복구]]력
157. [[475_hsm|HSM]] ([[157_hsm_hardware_security_module|Hardware Security Module]]) — 물리적 키 [[571_protection_vs_security|보호]]
158. [[476_tpm|TPM]] ([[476_tpm|Trusted Platform Module]]) — 플랫폼 키 저장, 원격 증명
159. [[159_pki_public_key_infrastructure|PKI]] ([[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]]) — 공개키 [[303_authentication_authorization_patterns|인증]]서 체계
160. [[089_contract_account_smart_contract|CA]] ([[160_ca_certification_authority|Certification Authority]]) — [[303_authentication_authorization_patterns|인증]]서 발급/관리
161. [[161_ra_registration_authority|RA]] ([[161_ra_registration_authority|Registration Authority]]) — [[303_authentication_authorization_patterns|인증]] 요청 [[395_verification_process_review|검증]]/승인

---

## 4. [[159_pki_public_key_infrastructure|PKI]] 심화 / [[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] — 49개

162. [[678_crl_certificate_revocation_list|CRL]] ([[678_crl_certificate_revocation_list|Certificate Revocation List]]) — 폐지 [[303_authentication_authorization_patterns|인증]]서 목록
163. [[679_ocsp_online_certificate_status_protocol|OCSP]] (Online Certificate Status [[295_protocol_field_tcp_udp_icmp|Protocol]]) — 실시간 [[303_authentication_authorization_patterns|인증]]서 상태 질의
164. [[679_ocsp_online_certificate_status_protocol|OCSP]] 스테이플링 — 서버가 [[679_ocsp_online_certificate_status_protocol|OCSP]] 응답 사전 가져옴
165. [[162_continuous_training_pipeline_model_retraining|CT]] ([[165_ct_certificate_transparency|Certificate Transparency]]) — [[303_authentication_authorization_patterns|인증]]서 발급 공개 [[568_logs_distributed_logging_elk_fluentd|로그]]
166. [[162_continuous_training_pipeline_model_retraining|CT]] [[568_logs_distributed_logging_elk_fluentd|로그]] 서버 — Google/Rustproof 등 다수 운영
167. [[167_sct_signed_certificate_timestamp|SCT]] ([[167_sct_signed_certificate_timestamp|Signed Certificate Timestamp]]) — [[162_continuous_training_pipeline_model_retraining|CT]] 증명
168. [[168_caa_certification_authority_authorization|CAA]] ([[168_caa_certification_authority_authorization|Certification Authority Authorization]]) — 허용된 [[089_contract_account_smart_contract|CA]] [[511_dns_hierarchical_distributed_architecture|DNS]] 레코드
169. PKCS#[[489_raid_10_hybrid|10]] — [[303_authentication_authorization_patterns|인증]]서 서명 요청 ([[169_pkcs10_csr|CSR]]) 형식
170. PKCS#7 / CMS — [[303_authentication_authorization_patterns|인증]]서 envelope 형식
171. PKCS#12 — [[303_authentication_authorization_patterns|인증]]서+개인키 보관 형식 (.pfx)
172. DER / PEM 인코딩 — [[303_authentication_authorization_patterns|인증]]서 인코딩 형식
173. X.509 v3 [[303_authentication_authorization_patterns|인증]]서 — Subject/Issuer/[[493_san_storage_area_network|SAN]]/[[067_db_key_uniqueness_minimality|Key]] Usage/NSC
174. [[493_san_storage_area_network|SAN]] ([[174_san_subject_alternative_name|Subject Alternative Name]]) — 다중 [[064_relation_domain|도메인]] [[303_authentication_authorization_patterns|인증]]서
175. [[175_wildcard_certificate|와일드카드 인증서]] — *.example.com
176. [[154_ev_earned_value|EV]] ([[176_ev_extended_validation_certificate|Extended Validation]]) [[303_authentication_authorization_patterns|인증]]서 — 엄격한 [[395_verification_process_review|검증]], 녹색 주소창
177. [[177_dv_domain_validation_certificate|DV]] ([[177_dv_domain_validation_certificate|Domain Validation]]) [[303_authentication_authorization_patterns|인증]]서 — [[064_relation_domain|도메인]] [[395_verification_process_review|검증]]만
178. [[178_ov_organization_validation_certificate|OV]] ([[178_ov_organization_validation_certificate|Organization Validation]]) — 조직 [[395_verification_process_review|검증]]
179. Self-signed [[303_authentication_authorization_patterns|인증]]서 — 자체 발급 [[303_authentication_authorization_patterns|인증]]서, 내부용
180. [[180_certificate_chain_of_trust|인증서 체인 검증]] — Root [[089_contract_account_smart_contract|CA]] → Intermediate [[089_contract_account_smart_contract|CA]] → End Entity
181. 브릿지 [[089_contract_account_smart_contract|CA]] ([[181_bridge_ca_cross_certification|Bridge CA]]) — 교차 [[303_authentication_authorization_patterns|인증]]
182. [[182_certificate_pinning_ssl_tls_security|인증서 핀닝]] —已知 [[303_authentication_authorization_patterns|인증]]서 목록 하드코딩
183. [[183_hpkp_http_public_key_pinning_deprecated|HPKP]] ([[461_http_stateless_connection_oriented|HTTP]] Public [[067_db_key_uniqueness_minimality|Key]] Pinning) — deprecated, 동적 핀닝 권장
184. Certificate Patrol / [[283_security_tactics|Security]]/Telemetry — Firefox 브라우저 핀닝
185. 동적 핀닝 — [[162_continuous_training_pipeline_model_retraining|CT]] [[568_logs_distributed_logging_elk_fluentd|로그]] 기반pins
186. [[186_ocsp_stapling_tls_handshake_optimization|Stapling of OCSP]] Response — [[694_thread_local_storage_tls|TLS]] 핸드셰이크 최적화
187. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] ([[187_mtls_mutual_tls_authentication|Mutual TLS]]) — 서버+클라이언트 상호 [[303_authentication_authorization_patterns|인증]]
188. [[188_code_signing_software_authentication|Code Signing]] — 소프트웨어 원산지 [[303_authentication_authorization_patterns|인증]]
189. [[189_authenticode_microsoft_code_signing|Authenticode]] — Microsoft [[188_code_signing_software_authentication|코드 서명]]
190. [[190_apple_developer_id_code_signing_notarization|Apple Developer ID]] — macOS/iOS 앱 서명
191. [[191_signature_timestamping_tsa|서명 타임스탬프]] —[[192_time_stamping_authority_rfc3161_non_repudiation|TSA]] ([[192_time_stamping_authority_rfc3161_non_repudiation|Time Stamping Authority]])
192. [[192_time_stamping_authority_rfc3161_non_repudiation|TSA]] ([[192_time_stamping_authority_rfc3161_non_repudiation|Time Stamping Authority]]) — RFC 3161, 부인방지
193. [[193_crl_distribution_point_cdp|CRL Distribution Point]] — [[678_crl_certificate_revocation_list|CRL]] 발급 위치
194. [[194_authority_information_access_aia_ocsp|Authority Information Access]] — [[679_ocsp_online_certificate_status_protocol|OCSP]] 응답자 위치
195. [[195_crl_scope_crlnumber_delta|CRL Scope]] — 전체/crlNumber 용도
196. [[196_delta_crl_efficiency_improvement|delta CRL]] —增量 [[678_crl_certificate_revocation_list|CRL]], 효율성 향상
197. [[197_ldh_limited_distribution_hypothesis|LDH]] ([[197_ldh_limited_distribution_hypothesis|Limited Distribution Hypothesis]]) — [[303_authentication_authorization_patterns|인증]]서 배포 모델
198. [[067_db_key_uniqueness_minimality|Key]] Usage 확장 — digitalSignature/keyEncipherment/codeSigning
199. [[199_extended_key_usage_eku_serverauth|Extended Key Usage]] — serverAuth/clientAuth/codeSigning/emailProtection
200. [[200_name_constraints_ca_issuance_limit|nameConstraints]] — CA가 발급 가능한 이름 공간 제한
201. [[201_basic_constraints_ca_path_length|Basic Constraints]] — [[089_contract_account_smart_contract|CA]] 여부, 경로 길이 제한
202. [[202_policy_mapping|정책 매핑]] — 상위 [[089_contract_account_smart_contract|CA]] [[164_policy|정책]]과 하위 [[089_contract_account_smart_contract|CA]] [[202_policy_mapping|정책 매핑]]
203. [[203_spc_signed_public_key_challenge|SPC]] (Signed Public [[067_db_key_uniqueness_minimality|Key]] Challenge) — [[188_code_signing_software_authentication|코드 서명]] blob
204. [[204_authenticode_timestamp_protocol|Authenticode Timestamp Protocol]] — RFC 3161 호환
205. [[205_kernel_mode_signing_dse|Kernel Mode Signing]] — Windows [[022_kernel_role|커널]] 드라이버 필수
206. [[206_uefi_secure_boot_verification|UEFI Secure Boot]] — 부팅 과정 [[188_code_signing_software_authentication|코드 서명]] [[395_verification_process_review|검증]]
207. [[496_dkim_domainkeys_identified_mail|DKIM]] ([[496_dkim_domainkeys_identified_mail|DomainKeys Identified Mail]]) — 이메일 발신자 [[303_authentication_authorization_patterns|인증]]
208. [[495_spf_sender_policy_framework|SPF]] ([[495_spf_sender_policy_framework|Sender Policy Framework]]) — 허용된 발신 서버 목록 ([[511_dns_hierarchical_distributed_architecture|DNS]] TXT)
209. [[497_dmarc_domain_based_message_authentication|DMARC]] ([[064_relation_domain|Domain]]-based Message Auth Reporting) — [[495_spf_sender_policy_framework|SPF]]+[[496_dkim_domainkeys_identified_mail|DKIM]] [[164_policy|정책]]
210. [[210_dane_dns_based_auth_tlsa|DANE]] ([[511_dns_hierarchical_distributed_architecture|DNS]]-Based Auth of Named Entities) — TLSA 레코드, [[303_authentication_authorization_patterns|인증]]서 고정

---

## 5. [[1117_network_security_zero_trust_policy|네트워크 보안]] — 55개

211. [[1117_network_security_zero_trust_policy|네트워크 보안]] 3대 영역 — 경계/[[364_segmentation|세그멘테이션]]/[[003_integrity|무결성]]
212. [[690_firewall_generation_evolution|방화벽]] — 네트워크 경계 접근 제어
213. [[213_packet_filtering_firewall|패킷 필터링 방화벽]] — 3-4층 헤더 기반 필터
214. [[214_stateful_inspection_firewall|상태 검사 방화벽]] ([[992_firewall_stateful_inspection|Stateful Inspection]]) — 연결 상태 추적
215. 애플리케이션 게이트웨이 ([[264_proxy_pattern_surrogate_access_control|Proxy]]) — 7층 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 검사
216. [[698_ngfw_next_generation_firewall|NGFW]] (Next-Generation [[690_firewall_generation_evolution|Firewall]]) — DPI, 사용자识别, 앱識別
217. [[217_firewall_topology_screened_subnet_dual_dmz|방화벽 토폴로지]] — 스크린 서브넷, 이중 [[219_demilitarized_zone_dmz_public_subnet|DMZ]]
218. [[218_bastion_host_dmz_security|bastion host]] — 경계 호스트, 공개 [[090_service_kubernetes_network_load_balancing|서비스]] 전용
219. [[219_demilitarized_zone_dmz_public_subnet|DMZ]] (Demilitarized Zone) — 비 Military Zone, 공개 구간
220. [[220_internal_firewall_segmentation|내부 방화벽]] ([[220_internal_firewall_segmentation|Internal Firewall]]) — 내부 [[364_segmentation|세그멘테이션]]
221. East-West 트래픽 — 수평 방향 통신, 내부 위협 통제
222. North-South 트래픽 — 경계 통과 통신
223. [[223_network_segmentation_vlan_vrf_isolation|네트워크 세그멘테이션]] — [[224_vlan_virtual_lan_broadcast_domain|VLAN]], [[371_vrf_virtual_routing_and_forwarding|VRF]], [[369_logic_bomb|논리]]적 격리
224. [[224_vlan_virtual_lan_broadcast_domain|VLAN]] ([[224_vlan_virtual_lan_broadcast_domain|Virtual LAN]]) — 브로드캐스트 [[064_relation_domain|도메인]] 분리
225. [[371_vrf_virtual_routing_and_forwarding|VRF]] (Virtual [[339_routing_overview_best_path_selection|Routing]] and Forwarding) — 경로 격리
226. [[700_nac_network_access_control|NAC]] ([[226_nac_network_access_control_ieee_802_1x|Network Access Control]]) — IEEE 802.[[584_802_1x_pnac_eap_radius|1X]], [[446_port_and_bus|포트]] 기반 접근 제어
227. [[229_eap_extensible_authentication_protocol|EAP]] ([[229_eap_extensible_authentication_protocol|Extensible Authentication Protocol]]) — 802.[[584_802_1x_pnac_eap_radius|1X]] [[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
228. [[228_eap_md5_vulnerable_authentication|EAP-MD5]] — 취약, 권장되지 않음
229. [[229_peap_protected_eap_tls_tunnel_authentication|PEAP]] ([[229_peap_protected_eap_tls_tunnel_authentication|Protected EAP]]) — TLS隧道保护 [[229_eap_extensible_authentication_protocol|EAP]]
230. [[230_eap_tls_mutual_authentication_pki|EAP-TLS]] — [[303_authentication_authorization_patterns|인증]]서 기반 상호 [[303_authentication_authorization_patterns|인증]]
231. [[231_mac_address_filtering_spoofing_vulnerability|MAC Address Filtering]] — 허가된 MAC만 허용
232. [[601_ids_ips_syscall_tracing|IDS]] ([[994_ids_ips_intrusion_detection_prevention_false_positive|Intrusion Detection System]]) — 오용 탐지/[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
233. [[601_ids_ips_syscall_tracing|IDS]] 배치 — in-band ([[601_ids_ips_syscall_tracing|IDS]]) vs out-of-band (tap/mirror)
234. [[695_ips_network_intrusion_prevention_system|IPS]] (Intrusion Prevention System) — 인라인 배치, 자동 차단
235. [[235_signature_based_detection_misuse_known_attacks|Signature-based detection]] —已知 공격 패턴 매칭
236. [[236_anomaly_based_detection_zero_day_false_positive|Anomaly-based detection]] —정상 프로파일과 비교
237. HIDS/HIPS — 호스트 기반 [[601_ids_ips_syscall_tracing|IDS]]/[[695_ips_network_intrusion_prevention_system|IPS]]
238. [[693_nids_network_intrusion_detection_system|NIDS]]/NIPS — 네트워크 기반 [[601_ids_ips_syscall_tracing|IDS]]/[[695_ips_network_intrusion_prevention_system|IPS]]
239. [[694_snort_suricata_misuse_anomaly_detection|Snort]] — [[191_oss_license_compliance|오픈소스]] [[693_nids_network_intrusion_detection_system|NIDS]]
240. [[240_suricata_multithreaded_nids_ids_ips_engine|Suricata]] — 멀티스레드 [[693_nids_network_intrusion_detection_system|NIDS]]
241. [[241_zeek_bro_network_traffic_metadata_analysis|Zeek]] (formerly Bro) — 네트워크 트래픽 분석
242. [[696_waf_web_application_firewall|WAF]] ([[242_waf_web_application_firewall_l7_protection|Web Application Firewall]]) — [[461_http_stateless_connection_oriented|HTTP]]/[[471_https_http_over_tls|HTTPS]] [[571_protection_vs_security|보호]]
243. OWASP Core Rule Set — [[696_waf_web_application_firewall|WAF]] 규칙 세트
244. [[244_virtual_patching_waf|Virtual Patching]] — 실제 패치 전 WAF로 취약점 우회
245. [[245_modsecurity_open_source_waf|ModSecurity]] — [[191_oss_license_compliance|오픈소스]] [[696_waf_web_application_firewall|WAF]] 엔진
246. [[542_api_gateway|API Gateway]] — [[014_api_posix|API]] 접근 제어,_RATE limiting, [[303_authentication_authorization_patterns|인증]]
247. [[542_api_gateway|API Gateway]] 기능 — [[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]]/[[456_caching|캐싱]]/로깅/변환
248. DDoS 공격 — 고의적 [[090_service_kubernetes_network_load_balancing|서비스]] 중단 공격
249. DDoS 3유형 — 볼류메트릭/[[295_protocol_field_tcp_udp_icmp|프로토콜]]/애플리케이션 계층
250. DDoS 방어 기법 — [[520_rate_limiting|Rate Limiting]], Anycast, [[721_drdos_scrubbing_center_mitigation|Scrubbing Center]]
251. [[251_bgp_blackhole|BGP Blackhole]] — DDoS 트래픽 경로黑洞
252. [[252_dns_amplification|DNS Amplification]] — [[511_dns_hierarchical_distributed_architecture|DNS]] [[298_qkv_attention|쿼리]] 증폭 공격
253. [[253_ntp_amplification|NTP Amplification]] — [[536_ntp_network_time_protocol_stratum|NTP]] 모노리스트 상태 [[298_qkv_attention|쿼리]] 증폭
254. [[254_memcached_amplification|memcached Amplification]] — [[406_udp_user_datagram_protocol_connectionless_fast|UDP]] [[446_port_and_bus|포트]] 11211 활용
255. [[255_syn_flood|SYN Flood]] — [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 半開 연결 점유
256. [[256_udp_flood|UDP Flood]] — 비효율적 [[295_protocol_field_tcp_udp_icmp|프로토콜]]滥用
257. [[257_http_flood|HTTP Flood]] — application layer DDoS
258. [[258_slowloris|Slowloris]] — [[461_http_stateless_connection_oriented|HTTP]] 헤더 미완성 전송으로 연결 점유
259. [[704_ip_spoofing_trust_injection|IP Spoofing]] — 출발지 IP 위조, BCP38 필수
260. [[260_urpf_unicast_rpf|uRPF]] (Unicast Reverse Path Forwarding) — [[598_spoofing|Spoofing]] 방지
261. [[991_arp_spoofing|ARP Spoofing]] — [[673_mac_message_authentication_code|MAC]] 주소 위조, 스위칭 환경에서도 가능
262. [[316_gratuitous_arp_g_arp_ip_conflict_cache_update|Gratuitous ARP]] — 정상 [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 응답 위조, MiTM 사전 준비
263. [[263_dhcp_spoofing|DHCP Spoofing]] — [[522_dhcp_dynamic_host_configuration_protocol|DHCP]] 서버 역할 사칭
264. [[976_dns_spoofing|DNS Spoofing]] — [[511_dns_hierarchical_distributed_architecture|DNS]] 응답 캐시 오염
265. [[265_dns_cache_poisoning|DNS Cache Poisoning]] — Kaminsky 공격, [[395_verification_process_review|검증]] 없는 응답

---

## 6. [[1117_network_security_zero_trust_policy|네트워크 보안]] 심화 — 55개

266. MITM (Man-in-the-Middle) 공격 — 통신 경로 가로채기
267. [[267_ssl_stripping|SSL Stripping]] — [[471_https_http_over_tls|HTTPS]]→[[461_http_stateless_connection_oriented|HTTP]] 강제 다운그레이드
268. [[268_hsts|HSTS]] ([[461_http_stateless_connection_oriented|HTTP]] Strict Transport [[283_security_tactics|Security]]) — [[471_https_http_over_tls|HTTPS]] 강제 사용
269. [[461_http_stateless_connection_oriented|HTTP]] Public [[067_db_key_uniqueness_minimality|Key]] Pinning — deprecated (2018)
270. [[270_cookie_hijacking|Cookie Hijacking]] — [[160_session_controlling_terminal|세션]] [[475_cookie_local_state|쿠키]] 탈취
271. [[707_session_hijacking_tcp_seq_cookie|세션 하이재킹]] — [[405_tcp_transmission_control_protocol_connection_oriented|TCP]] 시퀀스 넘버 예측
272. [[272_packet_sniffing|패킷 스니핑]] — 프로미스큐어스 모드 네트워크 인터페이스
273. [[273_session_fixation|세션 고정 공격]] ([[273_session_fixation|Session Fixation]]) — 공격자 [[160_session_controlling_terminal|세션]] ID 강제 [[009_config|설정]]
274. [[274_replay_attack|Replay Attack]] — 통신 [[701_sniffing_eavesdropping_promiscuous|도청]] 후 재전송
275. [[589_ipsec_offload|IPsec]] — 네트워크層 투명한 보안
276. [[589_ipsec_offload|IPsec]] 두 가지 [[295_protocol_field_tcp_udp_icmp|프로토콜]] — [[381_ah_authentication_header_integrity_auth|AH]] ([[303_authentication_authorization_patterns|인증]]만)/[[382_esp_encapsulating_security_payload_confidentiality|ESP]] (암호화+[[303_authentication_authorization_patterns|인증]])
277. [[589_ipsec_offload|IPsec]] 모드 — Transport 모드/Tunnel 모드
278. [[383_ike_isakmp_sa_security_association|IKE]] ([[383_ike_isakmp_sa_security_association|Internet Key Exchange]]) — 키 교환 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
279. [[279_ikev1|IKEv1]] Phase 1/2 — Main Mode/Aggressive Mode
280. [[280_ikev2|IKEv2]] — MOBIKE 지원, [[384_nat_t_ipsec_nat_traversal_udp_4500|NAT-T]] 자동 처리
281. [[384_nat_t_ipsec_nat_traversal_udp_4500|NAT-T]] ([[384_nat_t_ipsec_nat_traversal_udp_4500|NAT Traversal]]) — [[589_ipsec_offload|IPsec]] [[983_vpn_virtual_private_network|VPN]] [[307_nat_network_address_translation_router_principles|NAT]] 통과
282. [[379_l2tp_layer_2_tunneling_protocol|L2TP]]/[[589_ipsec_offload|IPsec]] — [[379_l2tp_layer_2_tunneling_protocol|L2TP]] 터널 + [[589_ipsec_offload|IPsec]] 암호화
283. [[283_ssl_vpn|SSL VPN]] — 브라우저 기반/클라이언트 설치형
284. [[284_openvpn|OpenVPN]] — [[191_oss_license_compliance|오픈소스]] [[283_ssl_vpn|SSL VPN]]
285. [[387_wireguard_vpn_modern_tunneling|WireGuard]] — modern [[983_vpn_virtual_private_network|VPN]], Linux [[022_kernel_role|커널]]에 통합
286. [[286_zerotier|ZeroTier]] — [[136_variance|분산]] [[983_vpn_virtual_private_network|VPN]], [[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]] 터널
287. [[287_tailscale|Tailscale]] — [[387_wireguard_vpn_modern_tunneling|WireGuard]] 기반 관리형 [[983_vpn_virtual_private_network|VPN]]
288. [[740_sase_secure_access_service_edge_sdwan_cloud|SASE]] (Secure Access [[090_service_kubernetes_network_load_balancing|Service]] Edge) — 네트워크+보안 통합
289. [[481_sse_server_sent_events|SSE]] ([[289_sse_security_service_edge|Security Service Edge]]) — SASE의 보안 요소
290. [[849_sd_wan_software_defined_wide_area_network|SD-WAN]] ([[290_sdwan_security|Software-Defined WAN]]) — WAN [[015_virtualization|가상화]]
291. [[849_sd_wan_software_defined_wide_area_network|SD-WAN]] 보안 — 암호화된 터널, 중앙 집중식 [[164_policy|정책]]
292. [[292_vpn_concentrator|VPN concentrator]] — 다수 [[983_vpn_virtual_private_network|VPN]] 연결 집약 장치
293. [[694_thread_local_storage_tls|TLS]]/SSL 취약점 역사 — [[294_poodle|POODLE]]/[[295_beast|BEAST]]/[[296_crime_attack|CRIME]]/ROGUE
294. [[294_poodle|POODLE]] ([[098_padding_convolutional_neural_network_same_valid|Padding]] [[188_pl_sql_t_sql_procedural|Oracle]] On Downgraded Legacy Encryption)
295. [[295_beast|BEAST]] (Browser Exploit Against SSL/[[694_thread_local_storage_tls|TLS]])
296. [[296_crime_attack|CRIME]] — [[694_thread_local_storage_tls|TLS]] [[347_compaction|압축]] [[481_side_channel_attack|사이드 채널 공격]]
297. [[297_heartbleed|HEARTBLEED]] — OpenSSL 하트비트 확장 메모리 유출
298. [[298_drown_attack|DROWN]] — SSLv2滥用による [[110_rsa|RSA]] 解読
299. [[299_logjam_attack|Logjam]] — DH_EXPORT 키 강제 사용, 512비트 그룹
300. [[300_freak_attack|FREAK]] — RSA_EXPORT 키 강제 사용
301. [[301_sweet32_attack|Sweet32]] — 64비트 [[655_block_cipher_des_3des_feistel|블록 암호]] Birthday 공격
302. [[694_thread_local_storage_tls|TLS]] 1.3 — 이전 [[288_version_ihl_tos_total_length|버전]]과의 [[344_compatibility_usability|호환성]] 제거, 빠른 핸드셰이크
303. [[694_thread_local_storage_tls|TLS]] 1.3 vs 1.2 차이 — 1-RTT 핸드셰이크, 0-RTT, PFS 의무
304. [[694_thread_local_storage_tls|TLS]] 密码套件 — TLS_AES_256_GCM_SHA384 등
305. cipher suite命名规则 — TLS_kex_AUTH
306. Perfect [[235_forward_backward_chaining|Forward]] Secrecy — 각 [[160_session_controlling_terminal|세션]]独立的密钥
307. [[538_ssh_vs_telnet_secure_remote|SSH]] ([[538_ssh_vs_telnet_secure_remote|Secure Shell]]) — 안전한 원격 접속
308. [[538_ssh_vs_telnet_secure_remote|SSH]] 키 기반 [[303_authentication_authorization_patterns|인증]] — 공개키/개인키 쌍
309. [[309_ssh_agent_forwarding|SSH Agent Forwarding]] — 로컬 에이전트를远程에 전달
310. [[485_sftp_ssh_file_transfer|SFTP]] — [[538_ssh_vs_telnet_secure_remote|SSH]] 기반 [[501_file_definition_logical_record|파일]] 전송
311. [[747_scp|SCP]] — [[538_ssh_vs_telnet_secure_remote|SSH]] 기반 [[501_file_definition_logical_record|파일]] 복사
312. [[312_ssh_tunnel|SSH Tunnel]]/[[264_proxy_pattern_surrogate_access_control|Proxy]] — SOCKS [[264_proxy_pattern_surrogate_access_control|프록시]]
313. [[313_known_hosts|Known Hosts]] — 서버 공개키 최초 수락/저장
314. [[538_ssh_vs_telnet_secure_remote|SSH]] 옵션 강화 — PasswordAuthentication no, PubkeyAuthentication yes
315. [[543_ldap_lightweight_directory_access_protocol|LDAP]] — [[506_directory_structure_symbol_table|디렉터리]] [[090_service_kubernetes_network_load_balancing|서비스]] 접근 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
316. [[316_ldaps|LDAPS]] ([[316_ldaps|LDAP over SSL]]) — [[446_port_and_bus|포트]] 636, [[543_ldap_lightweight_directory_access_protocol|LDAP]] 암호화
317. [[543_ldap_lightweight_directory_access_protocol|LDAP]] [[480_injection|인젝션]] — 특수 문자注入으로 [[303_authentication_authorization_patterns|인증]] 우회
318. [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] 캐시poisoning —静态 [[312_arp_address_resolution_protocol_ip_to_mac|ARP]] [[009_config|설정]]으로 MiTM
319. [[319_vlan_hopping|VLAN Hopping]] — [[238_switch_operation_principles|Switch]] [[598_spoofing|Spoofing]]/Double Tagging
320. [[260_bridge_pattern_abstraction_implementation|Bridge]] [[295_protocol_field_tcp_udp_icmp|Protocol]] [[001_dikw_pyramid|Data]] Unit ([[254_bpdu_bridge_protocol_data_unit|BPDU]]) — [[238_switch_operation_principles|스위치]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]

---

## 7. 시스템 보안 / 엔드포인트 — 55개

321. [[321_endpoint_security|엔드포인트 보안]] — 단말기에 대한 보안措施
322. [[322_epp|EPP]] ([[322_epp|Endpoint Protection Platform]]) — 통합 엔드포인트 [[571_protection_vs_security|보호]]
323. [[323_antivirus|AV]] ([[323_antivirus|Anti-Virus]]) — 시그니처 기반 악성코드 탐지
324. [[324_behavior_based_detection|행위 기반 탐지]] — 시그니처 없이 의심 행동 감지
325. [[325_edr|EDR]] (Endpoint [[961_deepfake_detection|Detection]] and Response) — 실시간 모니터링+응답
326. [[127_xdr_external_data_representation|XDR]] (Extended [[961_deepfake_detection|Detection]] and Response) — 멀티 플랫폼 [[325_correlation_analysis_pearson_spearman|상관 분석]]
327. [[327_mdr|MDR]] (Managed [[961_deepfake_detection|Detection]] and Response) — 관리형 탐지/응답
328. [[328_endpoint_protection_combo|엔드포인트 보호 조합]] — [[323_antivirus|AV]]+[[325_edr|EDR]]+NDR+[[613_ueba|UEBA]]
329. [[329_ttp|TTP]] (Tactics, Techniques, Procedures) — 공격자 행동 패턴
330. [[591_buffer_overflow|버퍼 오버플로우]] ([[591_buffer_overflow|Buffer Overflow]]) — 메모리 경계 초과
331. [[331_stack_buffer_overflow|스택 버퍼 오버플로우]] — 함수 복귀 주소 덮어쓰기
332. [[332_heap_buffer_overflow|힙 버퍼 오버플로우]] — 힙 메모리 오염
333. [[333_integer_overflow|정수 오버플로우]] ([[333_integer_overflow|Integer Overflow]]) — 정수 범위 초과
334. [[334_format_string_bug|Format String Bug]] — %x, %s 등 포맷 지시어 악용
335. [[335_nx_bit|NX bit]] (No-Execute) — 실행 가능 메모리 영역 분리
336. [[336_dep|DEP]] ([[336_dep|Data Execution Prevention]]) — NX를 OS 수준에서 구현
337. [[374_aslr|ASLR]] (Address Space Layout Randomization) — 주소 공간 난수화
338. [[338_pie|PIE]] ([[338_pie|Position Independent Executable]]) — EXE도 [[374_aslr|ASLR]]
339. [[339_stack_canary|Stack Canary]] — [[057_stack|스택]] 프레임 손상 탐지 [[475_cookie_local_state|쿠키]]
340. [[604_ssp|SSP]] ([[541_stack_smashing_protector|Stack Smashing Protector]]) — GCC의 [[057_stack|스택]] [[571_protection_vs_security|보호]]
341. [[341_relro|RELRO]] ([[341_relro|Relocation Read-Only]]) — GOT [[289_cqrs_db|쓰기]] [[571_protection_vs_security|보호]]
342. [[342_full_relro|Full RELRO]] — GOT 전체 읽기 전용
343. [[343_fortify_source|FORTIFY_SOURCE]] — _chk 함수로 버퍼 연산 대체
344. [[596_return_oriented_programming|ROP]] ([[596_return_oriented_programming|Return-Oriented Programming]]) — [[345_gadget_rop|가젯]] 체인, [[592_shellcode_injection|셸코드]] 없이 코드 실행
345. [[345_gadget_rop|가젯]] (Gadget) — Ret 명령으로 끝나는 코드 조각
346. [[346_jop|JOP]] ([[346_jop|Jump-Oriented Programming]]) — 함수 포인터Hijacking
347. [[347_cop|COP]] ([[347_cop|Call-Oriented Programming]]) — 호출 기반 [[345_gadget_rop|가젯]] 체인
348. Return-to-libc — libc 함수 직접 호출
349. [[349_heap_spray|Heap Spray]] — 힙 메모리에 [[592_shellcode_injection|셸코드]] 대량 배치
350. [[350_heap_feng_shui|Heap Feng Shui]] — 힙 레이아웃 조작
351. [[351_use_after_free|Use-After-Free]] — 해제된 메모리 재사용
352. [[352_double_free|Double Free]] — 이중 해제로 힙 손상
353. [[213_race_condition|Race Condition]] — [[273_toctou|TOCTOU]] (Time-of-Check-Time-of-Use)
354. [[281_deadlock_definition|Deadlock]] / [[315_livelock_vs_deadlock|Livelock]] — 자원 점유로 인한 교착/기아
355. [[355_toctou|Time-of-Check to Time-of-Use]] — [[501_file_definition_logical_record|파일]] 접근 races
356. [[356_privilege_escalation|권한 상승]] — [[356_privilege_escalation|Local Privilege Escalation]] (LPE)
357. [[022_kernel_role|커널]] [[356_privilege_escalation|privilege escalation]] — Dirty [[542_cow_file_system|COW]], EternalBlue
358. [[597_zero_day_exploit|Zero-Day]] — 패치되지 않은 취약점 利用
359. [[603_rootkit_syscall_hooking|루트킷]] ([[603_rootkit_syscall_hooking|Rootkit]]) — 시스템에潜伏하는 악성 코드 모음
360. [[360_kernel_rootkit|커널 루트킷]] — OS [[022_kernel_role|커널]] 레벨 설치
361. 사용자모드 [[603_rootkit_syscall_hooking|루트킷]] — 애플리케이션 레벨
362. [[362_bootkit|부트킷]] ([[362_bootkit|Bootkit]]) — 부팅 과정infecting
363. [[363_mbr_bootkit|MBR Bootkit]] — [[515_mbr_vs_gpt|Master Boot Record]] 감염
364. [[364_uefi_bootkit|UEFI Bootkit]] — [[706_uefi|UEFI]] [[032_firmware|펌웨어]] 수준 감염
365. [[608_secure_boot|Secure Boot]] 우회 — 서명 [[395_verification_process_review|검증]] 무력화
366. [[366_firmware_rootkit|Firmware Rootkit]] — BIOS/[[032_firmware|펌웨어]] 숨겨진 [[737_backdoor_c2_beacon_behavior_analysis|백도어]]
367. [[740_keylogger|키로거]] ([[740_keylogger|Keylogger]]) — 키입력 기록
368. [[737_backdoor_c2_beacon_behavior_analysis|백도어]] ([[727_backdoor|Backdoor]]) — 정상 [[303_authentication_authorization_patterns|인증]] 우회
369. [[369_logic_bomb|논리]]炸弾 ([[588_logic_bomb|Logic Bomb]]) — 특정 조건 충족 시 발동
370. [[726_trojan_horse|트로이목마]] ([[586_trojan_horse_wrapper|Trojan Horse]]) — 겉보기에 정상인 악성코드
371. [[730_ransomware|랜섬웨어]] ([[730_ransomware|Ransomware]]) — [[501_file_definition_logical_record|파일]] 암호화 후 몸값
372. [[731_cryptolocker|CryptoLocker]] / [[732_wannacry|WannaCry]] / [[734_ryuk|Ryuk]] — 주요 [[730_ransomware|랜섬웨어]] 변종
373. [[738_wiper|Wiper]] — [[001_dikw_pyramid|데이터]] 파괴 목적인 malware
374. [[374_apt|지능형 지속 위협]] ([[748_apt|APT]]) — 국가 수준 위협 행위자
375. [[375_fileless_malware|Fileless Malware]] — 메모리 내에서만 실행, [[501_file_definition_logical_record|파일]] 없는 공격

---

## 8. 시스템 보안 심화 — 40개

376. [[376_kernel_vulnerability|커널 취약점]] — 시스템 콜 인터페이스 악용
377. [[483_spectre|Spectre]]/[[482_meltdown|Meltdown]] — CPU 취약점 (推测執行 악용)
378. [[483_spectre|Spectre]] v1/v2 — Bounds Check Bypass/[[577_branch_target_injection|Branch Target Injection]]
379. [[482_meltdown|Meltdown]] — Rogue [[001_dikw_pyramid|Data]] Cache Load
380. [[764_mds|MDS]] ([[380_mds_attack|Microarchitectural Data Sampling]]) — CPU 내부 [[001_dikw_pyramid|데이터]] 샘플링
381. [[767_zombieload_attack|ZombieLoad]] / [[765_ridl_attack|RIDL]] — Load值的[[096_risk_non_risk_architecture_evaluation_flaws|리스크]]
382. [[382_swapgs|SWAPGS]] — [[418_gpu|GPU]] 취약점 악용
383. CPU 취약점缓解 — 마이크로코드 업데이트, OS 패치
384. [[032_firmware|펌웨어]] 보안 — [[206_uefi_secure_boot_verification|UEFI Secure Boot]]
385. [[919_measured_boot|Measured Boot]] — TPM利用, boot 측정값 기록
386. [[386_static_pcr|Static PCR]] — 부팅 과정 [[003_integrity|무결성]] 측정
387. [[387_dynamic_pcr|Dynamic PCR]] — late launch으로 동적 측정
388. [[388_intel_txt|Intel TXT]] ([[388_intel_txt|Trusted Execution Technology]]) — late launch
389. [[389_sgx|SGX]] ([[389_sgx|Software Guard Extensions]]) — [[390_enclave|enclave]] [[307_memory_protection|메모리 보호]]
390. [[390_enclave|enclave]] — SGX의加密 메모리 영역
391. [[391_amd_sev|AMD SEV]] ([[391_amd_sev|Secure Encrypted Virtualization]]) — [[598_vm_migration_nic|VM]] 암호화
392. SEV-ES — [[598_vm_migration_nic|VM]] [[057_register|레지스터]] [[272_state_pattern|state]] 암호화
393. [[393_memory_encryption_engine|Memory Encryption Engine]] — 하드웨어 [[796_memory_encryption|메모리 암호화]]
394. [[476_tpm|TPM]] 2.0 — 키 저장, 플랫폼 증명
395. [[476_tpm|TPM]] 기능 — PCR, EK, NV [[154_database_index_b_tree_search_optimization|Index]], Attestation
396. [[396_remote_attestation|remote attestation]] — [[396_remote_attestation|원격 플랫폼 증명]]
397. [[397_bitlocker_windows_fde|BitLocker]] — Windows FDE, [[476_tpm|TPM]]+N PIN/[[359_usb|USB]] 사용
398. [[398_filevault_macos_fde|FileVault]] — macOS FDE
399. [[399_luks_linux_unified_key_setup|LUKS]] — Linux Unified [[067_db_key_uniqueness_minimality|Key]] Setup, 디스크 암호화
400. [[400_veracrypt_cross_platform_disk_encryption|VeraCrypt]] — [[191_oss_license_compliance|오픈소스]] 암호화 도구
401. 全드라이브 암호화 (FDE) — OS 레벨 암호화
402. [[402_field_level_encryption|필드 레벨 암호화]] — DB 컬럼/필드별 암호화
403. [[403_tde_transparent_data_encryption|TDE]] ([[403_tde_transparent_data_encryption|Transparent Data Encryption]]) — DB 엔진 레벨 암호화
404. [[404_backup_encryption|백업 암호화]] — [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]도 암호화 필수
405. [[405_secure_erase|Secure Erase]] — [[327_ssd|SSD]] trim + 암호화 키 삭제
406. [[406_patch_management|패치 관리]] — [[407_cvss_scoring|CVSS]] 점수 기반 우선순위
407. [[407_cvss_scoring|CVSS]] (Common Vulnerability Scoring System) — 0~10점
408. [[407_cvss_scoring|CVSS]] 구성 — Base/Transient/Temporal/Global 벡터
409. [[409_cve_lifecycle|CVE]] (Common Vulnerabilities and Exposures) — 취약점 등록 번호
410. [[410_cwe_taxonomy|CWE]] ([[410_cwe_taxonomy|Common Weakness Enumeration]]) — 취약점 유형 [[104_classification_analysis|분류]]
411. [[411_cpe_inventory_mapping|CPE]] ([[411_cpe_inventory_mapping|Common Platform Enumeration]]) — 플랫폼 명칭
412. OVAL (Open Vulnerability and Assessment Language) — 취약점 검사 언어
413. 弱口令检测 — 기본パスワード/사전攻撃
414. 시스템 강화 — Hardening, 불필요 [[090_service_kubernetes_network_load_balancing|서비스]] 제거
415. CIS Benchmarks — Center for Internet [[283_security_tactics|Security]] 강화 가이드

---

## 9. 웹 / 애플리케이션 보안 — 60개

416. [[416_owasp_top_10|OWASP Top 10]] — 가장 위험한 웹 보안 취약점
417. A01. [[417_broken_access_control|취약한 접근 제어]] — [[418_idor|IDOR]], 권한 없는 기능 접근
418. [[418_idor|IDOR]] (Insecure [[176_direct_addressing|Direct]] Object [[316_reference_pattern_nosql|Reference]]) — 객체 참조Manipulation
419. [[419_path_traversal|경로 순회]] ([[419_path_traversal|Path Traversal]]) — ../../etc/passwd
420. [[420_directory_traversal|보편적 자원 순회]] ([[420_directory_traversal|Directory Traversal]]) — 경로 역추적
421. Local [[501_file_definition_logical_record|File]] Inclusion (LFI) —本地 [[501_file_definition_logical_record|파일]] 포함
422. Remote [[501_file_definition_logical_record|File]] Inclusion (RFI) — [[422_remote_file_inclusion_rfi|원격 파일 포함]]
423. [[423_access_control_bypass|접근 제어 회피]] — 메소드 제한 우회, [[450_cors_misconfiguration|CORS Misconfiguration]]
424. A02. [[479_cryptographic_failures|암호화 실패]] — 안전하지 않은 암호화 사용
425. [[425_hardcoded_credentials|하드코딩 자격증명]] — 소스코드 내 평문 비밀번호
426. 약한 [[694_thread_local_storage_tls|TLS]] [[288_version_ihl_tos_total_length|버전]] — [[694_thread_local_storage_tls|TLS]] 1.0/1.1 사용
427. [[182_certificate_pinning_ssl_tls_security|Certificate Pinning]] 우회 — Frida, Objection
428. A03. [[480_injection|인젝션]] — 입력값 [[395_verification_process_review|검증]] 부재로 인한 코드 실행
429. SQL [[480_injection|인젝션]] — [[002_database_definition|데이터베이스]] [[298_qkv_attention|쿼리]]Manipulation
430. [[430_error_based_sqli|Error-based SQL Injection]] — 오류 메시지 통한 정보 탈취
431. [[431_blind_sql_injection|Blind SQL Injection]] — [[369_logic_bomb|논리]]적 참/거짓 반응으로 정보 추출
432. Time-based [[431_blind_sql_injection|Blind SQL Injection]] — SLEEP() 함수로 반응 [[015_지연_데이터_관점|지연]]
433. [[433_orm_injection|ORM Injection]] — 객체-[[083_relationship_in_er_model|관계]] 매핑 프레임워크 공격
434. [[434_nosql_injection|NoSQL Injection]] — [[540_mongodb|MongoDB]] 등 문서DB 공격
435. [[435_os_command_injection|OS Command Injection]] — 서버 [[158_instruction|명령어]] 실행
436. [[317_ldap_injection|LDAP Injection]] — [[543_ldap_lightweight_directory_access_protocol|LDAP]] [[298_qkv_attention|쿼리]] 조작
437. [[437_xpath_injection|XPath Injection]] — XML [[001_dikw_pyramid|데이터]] 질의 조작
438. [[438_el_injection|Expression Language Injection]] — Spring/Struts EL 공격
439. [[439_ssti|Template Injection]] ([[439_ssti|SSTI]]) — 서버 사이드 템플릿 엔진 공격
440. A04. [[481_insecure_design|안전하지 않은 설계]] — [[611_threat_modeling|threat modeling]] 부재
441. [[441_missing_threat_modeling|위협 모델링 부재]] — 설계 단계 보안 평가 미실시
442. [[442_insecure_defaults|안전하지 않은 기본값]] — 기본 계정/비밀번호
443. [[443_excess_functionality|초과 기능]] — 불필요한 기능 활성화
444. A05. [[482_security_misconfiguration|보안 설정 오류]] — 잘못된 구성으로 인한 노출
445. 기본 계정 —厂商 제공 기본 비밀번호
446. 불필요 [[090_service_kubernetes_network_load_balancing|서비스]] — 사용 안 하는 [[090_service_kubernetes_network_load_balancing|서비스]] running
447. 오류 메시지 정보 유출 — 내부 경로/[[057_stack|스택]] 트레이스
448. [[448_missing_security_headers|Missing Security Headers]] — [[448_missing_security_headers|보안 헤더 미설정]]
449. Debug Mode — 개발용 모드 생산 환경 노출
450. [[450_cors_misconfiguration|CORS Misconfiguration]] — Access-Control-Allow-Origin: *
451. A06. 취약한 [[603_component_independent_deployment_unit|컴포넌트]] — 알려진 취약점 포함 [[336_library_vs_framework|라이브러리]]
452. [[452_log4shell|Log4Shell]] ([[452_log4shell|CVE-2021-44228]]) — Log4j RCE
453. [[453_sca|서드파티 라이브러리 취약점]] — npm/PyPI/RubyGems 의존성
454. A07. [[303_authentication_authorization_patterns|인증]] 실패 — 부적절한 [[303_authentication_authorization_patterns|인증]] 메커니즘
455. [[455_credential_stuffing|크리덴셜 스터핑]] — 유출 계정 재사용
456. [[456_brute_force|브루트포스]] — 무차별 대입 공격
457. [[457_password_spraying|패스워드 스프레이]] — 다양한 비밀번호 소량 시도
458. [[458_credential_pooling|크리덴셜 풀링]] — 자격증명 목록 활용
459. [[160_session_controlling_terminal|세션]] ID 노출 — URL, [[568_logs_distributed_logging_elk_fluentd|로그]], Referer 헤더
460. [[460_session_fixation|세션 고정]] — [[160_session_controlling_terminal|세션]] ID 고정 공격
461. A08. [[003_integrity|무결성]] 실패 — 소프트웨어 [[003_integrity|무결성]] [[395_verification_process_review|검증]] 부재
462. [[090_configuration_item|CI]]/CD 보안 — 파이프라인 침해, [[463_dependency_confusion|의존성 오염]]
463. [[463_dependency_confusion|의존성 오염]] ([[463_dependency_confusion|Dependency Confusion]]) — 비공개 패키지 덮어쓰기
464. [[464_insecure_signature_verification|잘못된 서명 검증]] — [[188_code_signing_software_authentication|코드 서명]] [[395_verification_process_review|검증]] 우회
465. A09. 로깅/모니터링 실패 — 증거 미보존
466. [[466_logging_blindness|Blindness]] — 공격 탐지 못 함
467. [[467_logging_without_alert|Logging Without Alert]] — [[568_logs_distributed_logging_elk_fluentd|로그]]만 기록, 알림 없음
468. A10. [[468_ssrf|SSRF]] — 서버 사이드 요청 위조
469. [[468_ssrf|SSRF]] [[012_metadata|메타데이터]] — 169.254.169.254 등 cloud [[012_metadata|metadata]]
470. [[726_xss_cross_site_scripting_types|XSS]] ([[470_xss|Cross-Site Scripting]]) —客户端 스크립트 삽입
471. 반사형 [[726_xss_cross_site_scripting_types|XSS]] — URL 파라미터 반영
472. 저장형 [[726_xss_cross_site_scripting_types|XSS]] — DB에 저장, 모든 사용자에게 발동
473. [[473_dom_xss|DOM-based XSS]] —客户端 JavaScript 변조
474. [[726_xss_cross_site_scripting_types|XSS]] 페이로드 — <script>alert(1)</script>, img onerror
475. [[475_csp|CSP]] ([[475_csp|Content Security Policy]]) — [[726_xss_cross_site_scripting_types|XSS]] 완화 헤더

---

## [[489_raid_10_hybrid|10]]. 웹 보안 심화 / [[014_api_posix|API]] 보안 — 50개

476. [[728_csrf_cross_site_request_forgery_concept|CSRF]] ([[728_csrf_cross_site_request_forgery_concept|Cross-Site Request Forgery]]) — 사용자의 의지와 무관한 요청
477. SameSite [[475_cookie_local_state|쿠키]] — [[728_csrf_cross_site_request_forgery_concept|CSRF]] 방어
478. [[478_csrf_token|CSRF Token]] — 난수 토큰 요구
479. 双重 Submit [[475_cookie_local_state|Cookie]] — [[475_cookie_local_state|쿠키]]+파라미터 대조
480. [[480_clickjacking|Clickjacking]] — 투명 iframe 덮기
481. X-Frame-Options — frame [[278_instruction_tuning|embedding]] 차단
482. [[482_frame_ancestors|frame-ancestors]] — [[475_csp|CSP]] [[288_version_ihl_tos_total_length|버전]]의 [[482_frame_ancestors|frame-ancestors]]
483. [[483_cors_preflight|CORS Preflight]] — OPTIONS 요청으로 사전 [[395_verification_process_review|검증]]
484. CORS 요청 흐름 — Origin 헤더 → 서버 허용/거부
485. [[485_owasp_zap|OWASP ZAP]] — 웹 취약점 스캐너
486. [[486_burp_suite|Burp Suite]] — 웹 [[264_proxy_pattern_surrogate_access_control|프록시]],渗透 테스트 도구
487. [[487_sqlmap|SQLMap]] — SQL [[480_injection|인젝션]] 자동화 도구
488. [[488_nikto|Nikto]] — 웹 서버 취약점 스캐너
489. [[489_httpoxy|httpoxy]] — CGI 환경변수 proxyManipulation
490. [[490_host_header_injection|Host Header Injection]] — X-Forwarded-Host [[395_verification_process_review|검증]] 우회
491. [[491_web_cache_deception|Web Cache Deception]] — 캐시poisoning
492. [[492_unicode_normalization|Unicode Normalization]] — нормализация 차이 공격
493. [[493_null_byte_injection|NULL Byte Injection]] — %00로 확장자 우회
494. [[494_null_byte_poisoning|Null Byte Poisoning]] — [[501_file_definition_logical_record|파일]]명 내 null 문자
495. [[495_oas_openapi_specification|OAS]] ([[495_oas_openapi_specification|OpenAPI Specification]]) — [[477_rest_api_architecture|REST API]] 표준
496. [[246_graphql_query_language_overfetching_solution|GraphQL]] 인트로스펙션 — [[014_api_posix|API]] [[005_schema|스키마]] 공개
497. [[497_graphql_dos|GraphQL DoS]] — depth/alias 제한 없으면 무한 [[298_qkv_attention|쿼리]]
498. [[477_rest_api_architecture|REST API]] 보안 — [[520_rate_limiting|Rate Limiting]], [[549_jwt_json_web_token|JWT]], [[674_hmac_hash_based_mac_ipsec|HMAC]]
499. [[499_api_versioning_security|API Versioning]] — [[014_api_posix|API]] [[288_version_ihl_tos_total_length|버전]] 관리와 보안
500. [[549_jwt_json_web_token|JWT]] ([[549_jwt_json_web_token|JSON Web Token]]) — [[239_stateless_redis|stateless]] [[303_authentication_authorization_patterns|인증]]
501. [[549_jwt_json_web_token|JWT]] 구조 — Header/Payload/Signature (JWS/JWE)
502. [[549_jwt_json_web_token|JWT]] [[310_alg_application_layer_gateway_nat_traversal|alg]]: none — 취약점, [[310_alg_application_layer_gateway_nat_traversal|alg]] [[395_verification_process_review|검증]] 필수
503. [[503_hs256_vs_rs256_jwt_signing|HS256 vs RS256]] — 대칭/비대칭 서명
504. [[549_jwt_json_web_token|JWT]] 유출 — XSS로 토큰 탈취
505. [[505_refresh_token|Refresh Token]] — [[505_refresh_token|액세스 토큰 재발급]]
506. OAuth 2.0 — 델리게이션 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
507. OAuth 2.0 4가지 Grant — [[509_authorization_models_rbac_abac|Authorization]] [[082_process_memory_structure|Code]]/[[509_pkce_public_client|PKCE]]/[[003_audit_stakeholders|Client]] Credentials/[[596_return_oriented_programming|ROP]]
508. [[508_authorization_code_grant|Authorization Code Grant]] —redirect_uri 기반
509. [[509_pkce_public_client|PKCE]] (Proof [[067_db_key_uniqueness_minimality|Key]] for [[082_process_memory_structure|Code]] Exchange) — public [[003_audit_stakeholders|client]] 보안
510. [[866_open_redirect|Open Redirect]] — OAuth redirect_uri 우회
511. [[511_token_leakage|Token Leakage]] — URL 내 토큰 노출
512. [[512_oauth_scope|Scope]] — OAuth 권한 범위
513. Access Token vs [[505_refresh_token|Refresh Token]] — 수명 차이
514. [[537_oidc_openid_connect|OIDC]] — OAuth 2.0之上的 신원 레이어
515. [[515_id_token_jwt|ID Token]] — OIDC의 사용자 신원 증명
516. [[515_id_token_jwt|ID Token]] vs Access Token — 용도 구분
517. [[517_oidc_discovery_document|Discovery Document]] — .well-known/openid-configuration
518. [[518_jwks_uri_endpoint|jwks_uri]] — [[343_json|JSON]] Web [[067_db_key_uniqueness_minimality|Key]] Set 엔드포인트
519. [[519_oidc_nonce|Nonce]] — [[274_replay_attack|replay attack]] 방지
520. [[520_rate_limiting|Rate Limiting]] — 요청 수 제한으로 [[599_dos_ddos_attack|DoS]] 방지
521. [[696_waf_web_application_firewall|WAF]] 규칙 — OWASP [[243_owasp_core_rule_set_crs_waf_anomaly_scoring|CRS]] 기반
522. [[245_modsecurity_open_source_waf|ModSecurity]] Core Rule Set — [[522_modsecurity_crs|generic 공격 탐지]]
523. [[523_http_request_smuggling_concept|HTTP Request Smuggling]] — front-end/back-end interpretation 차이
524. [[461_http_stateless_connection_oriented|HTTP]] Request走私 — CL.[[361_ospf_traffic_engineering_te|TE]], [[361_ospf_traffic_engineering_te|TE]].CL, H2.CL
525. [[525_http_response_smuggling|HTTP Response Smuggling]] — 응답 분할

---

## [[308_static_dynamic_nat_pat_port_address_translation|11]]. [[527_identity_management|신원 관리]] / 접근 제어 — 55개

526. [[526_iam|IAM]] (Identity and Access [[372_management|Management]]) — 신원+접근 통합 관리
527. [[527_identity_management|신원 관리]] — 사용자 lifecycle ([[528_provisioning|프로비저닝]]/수정/비활성화/삭제)
528. [[528_provisioning|Provisioning]] — 사용자 계정 자동 [[087_process_state_transition|생성]]
529. [[529_deprovisioning|Deprovisioning]] — 퇴직/이직 시 계정 즉시 삭제
530. Joiner/Mover/Leaver 프로세스 — 신원 lifecycle 관리
531. [[531_sso|SSO]] ([[531_sso|Single Sign-On]]) —一次登录，多アプリ access
532. SAML 2.0 — XML 기반 [[531_sso|SSO]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
533. [[533_saml_assertion|SAML Assertion]] — 신원 정보 포함 XML
534. SAML Request/Response — [[166_sp|SP]]-Initiated/[[536_idp_identity_provider|IdP]]-Initiated
535. [[166_sp|SP]] ([[535_sp_service_provider|Service Provider]]) — [[090_service_kubernetes_network_load_balancing|서비스]] 제공자
536. [[536_idp_identity_provider|IdP]] ([[536_idp_identity_provider|Identity Provider]]) — 신원 제공자
537. [[548_openid_connect|OpenID Connect]] — OAuth 2.0 기반 [[531_sso|SSO]]
538. [[538_oidc_discovery|OIDC Discovery]] — 자동 [[009_config|설정]] [[012_metadata|메타데이터]]
539. [[539_claims|Claims]] — OIDC의 사용자 [[082_attribute_types_er_model|속성]]
540. [[540_scope_oidc|OIDC Scope]] ([[540_scope_oidc|OpenID Connect Scope]]) — 요청하는 정보 범위 (openid/profile/email)
541. [[541_pkce_in_oidc|PKCE in OIDC]] — [[509_authorization_models_rbac_abac|Authorization]] [[082_process_memory_structure|Code]] [[571_protection_vs_security|보호]]
542. OAuth 2.0 vs [[537_oidc_openid_connect|OIDC]] — 델리게이션 vs [[303_authentication_authorization_patterns|인증]]
543. [[543_federation|Federation]] — 조직 간 신뢰 기반 ID 공유
544. [[544_trust_relationship|Trust Relationship]] — [[543_federation|federation]] 파트너 간 신뢰
545. [[545_edugain|eduGAIN]] — 학술 기관간 [[543_federation|federation]]
546. [[546_shibboleth|Shibboleth]] — SAML 기반 [[543_federation|federation]]
547. [[543_ldap_lightweight_directory_access_protocol|LDAP]] 기반 [[303_authentication_authorization_patterns|인증]]/조회 — [[506_directory_structure_symbol_table|디렉터리]] [[090_service_kubernetes_network_load_balancing|서비스]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
548. [[548_active_directory|Active Directory]] — Microsoft [[506_directory_structure_symbol_table|디렉터리]] [[090_service_kubernetes_network_load_balancing|서비스]]
549. Azure AD / Microsoft Entra ID — 클라우드 신원
550. [[550_azure_ad_connect|Azure AD Connect]] — [[061_on_premise_legacy_infrastructure|온프레미스]] AD 클라우드 연동
551. [[551_okta_idaas|Okta]] — [[309_saas|SaaS]] [[551_okta_idaas|IDaaS]]
552. [[552_mfa|MFA]] ([[552_mfa|Multi-Factor Authentication]]) — 다중 [[303_authentication_authorization_patterns|인증]]
553. [[553_knowledge_factor|지식 요인]] — 비밀번호, PIN
554. [[554_possession_factor|소유 요인]] — 토큰, 스마트폰, 스마트카드
555. [[555_inherence_factor|내재 요인]] — 지문, 홍채, 음성, 얼굴
556. [[556_location_factor|위치 요인]] — GPS, IP 기반 위치
557. [[557_behavioral_factor|행동 요인]] — 타이핑 패턴, 마우스 움직임
558. [[558_totp|TOTP]] ([[558_totp|Time-based OTP]]) — 30초마다 변경
559. [[559_hotp|HOTP]] ([[559_hotp|HMAC-based OTP]]) — [[059_counter|카운터]] 기반
560. [[560_push_notification|Push Notification]] — 모바일 푸시 알림
561. FIDO2 / WebAuthn —公开키 암호 기반 [[303_authentication_authorization_patterns|인증]]
562. [[562_passkey|Passkey]] — FIDO2 기반, 플랫폼 관리
563. [[562_passkey|Passkey]] 장점 — [[752_phishing|피싱]] [[003_resistance|저항]], 암호 불필요
564. [[564_pam|PAM]] ([[564_pam|Privileged Access Management]]) — [[565_privileged_accounts|특권 계정]] 관리
565. 特권 계정 — 관리자,root, [[275_iam_role_for_service_accounts|서비스 계정]]
566. [[566_session_recording|세션 레코딩]] — 특권 [[160_session_controlling_terminal|세션]] 녹화/[[606_auditing_linux_auditd|감사]]
567. [[567_vault|vault]] — 비밀번호 금고 (HashiCorp [[567_vault|Vault]])
568. [[568_jit_access|Just-In-Time]] Access — 필요 시만 일시적 권한
569. [[569_rbac|RBAC]] ([[569_rbac|Role-Based Access Control]]) — 역할 기반 권한
570. [[569_rbac|RBAC]] 1/2/3 —.flat/hierarchical/constrained
571. [[571_role_hierarchy|역할 계층]] — 상위 역할이 하위 권한 [[234_uml_class_relationships_generalization_dependency|상속]]
572. [[572_abac|ABAC]] ([[572_abac|Attribute-Based Access Control]]) — [[082_attribute_types_er_model|속성]] 기반
573. [[573_abac_attributes|속성 종류]] — subject/object/[[066_gitlab_flow_environment_branch_strategy|environment]]/action
574. [[574_xacml|XACML]] (eXtensible [[547_access_control_rwx|Access Control]] Markup Language) — [[572_abac|ABAC]] [[164_policy|정책]] 언어
575. [[575_rebac|ReBAC]] ([[575_rebac|Relationship-Based Access Control]]) — [[083_relationship_in_er_model|관계]] 기반
576. [[576_zanzibar|Zanzibar]] — Google의 권한 시스템
577. [[010_least_privilege|최소 권한 원칙]] — 필요한 최소 권한만 부여
578. [[578_sod_segregation_of_duties|직무 분리]] (SoD) —권한 [[136_variance|분산]]으로 부정행위 방지
579. [[579_accounting_auditing|어카운팅]] — 접근 기록, [[606_auditing_linux_auditd|감사]] 자료
580. [[580_access_review|접근 검토]] ([[580_access_review|Access Review]]) — 정기적 권한 재검토

---

## 12. 신원 보안 심화 / 위협 — 40개

581. [[581_authentication_server|인증 서버]] — [[583_kdc|KDC]], [[536_idp_identity_provider|IdP]], [[303_authentication_authorization_patterns|인증]] endpoints
582. [[545_kerberos_kdc_ticket_based_auth|Kerberos]] — 네트워크 [[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] (v5)
583. [[583_kdc|KDC]] ([[583_kdc|Key Distribution Center]]) — [[344_as_autonomous_system_asn|AS]]+[[585_tgs|TGS]] 통합
584. [[344_as_autonomous_system_asn|AS]] ([[584_as|Authentication Server]]) — [[459_quic_fec_forward_error_correction|초기]] [[303_authentication_authorization_patterns|인증]]
585. [[585_tgs|TGS]] ([[585_tgs|Ticket Granting Server]]) — 티켓 발급
586. [[586_tgt|TGT]] ([[586_tgt|Ticket Granting Ticket]]) — 장기 티켓
587. [[587_st|ST]] ([[587_st|Service Ticket]]) — 특정 [[090_service_kubernetes_network_load_balancing|서비스]]용 단기 티켓
588. [[545_kerberos_kdc_ticket_based_auth|Kerberos]] 상호 [[303_authentication_authorization_patterns|인증]] — [[003_audit_stakeholders|client]]+server mutual
589. [[589_silver_ticket|Silver Ticket]] — [[587_st|ST]] 위조 ([[275_iam_role_for_service_accounts|서비스 계정]] 키 사용)
590. [[590_golden_ticket|Golden Ticket]] — [[586_tgt|TGT]] 위조 (KRBTGT 키 사용)
591. [[591_ptt|Pass-the-Ticket]] — 메모리 내 티켓 재사용
592. [[592_pth|Pass-the-Hash]] — [[594_ntlm|NTLM]] 해시 재사용
593. [[593_bronze_attack|Kerberos Bronze Attack]] — [[707_asrep_roasting|AS-REP Roasting]]
594. [[594_ntlm|NTLM]] — Windows 네이티브 [[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
595. [[595_ntlm_hash|NTLM Hash]] — MD4(UTF-16LE(password))
596. [[596_ntlm_authentication|NTLM Authentication]] — 3-way handshake (質詢/응답)
597. [[597_lm_hash|LM Hash]] — [[086_des_data_encryption_standard|DES]] 기반, 취약한 레거시
598. [[598_ntlmv2|NTLMv2]] — [[674_hmac_hash_based_mac_ipsec|HMAC]]-[[668_md5_hash_collision_vulnerability|MD5]] 기반 강화 [[288_version_ihl_tos_total_length|버전]]
599. [[599_netntlm|NetNTLM]] — 네트워크 상에서만 사용되는 [[594_ntlm|NTLM]]
600. [[600_ms_chapv2|MS-CHAPv2]] — [[224_ppp_point_to_point_protocol|PPP]]/[[229_eap_extensible_authentication_protocol|EAP]] 내부의 [[594_ntlm|NTLM]] 변형
601. [[601_credential_dumping|Credential Dumping]] — LSASS 메모리/ [[705_sam_hive|SAM hive]] 추출
602. [[602_mimikatz|Mimikatz]] — 크리덴셜 추출 도구
603. [[603_wdigest|WDigest]] — 평문 비밀번호 [[456_caching|캐싱]] ([[235_registry_immutable_tag|레지스트리]] [[009_config|설정]])
604. [[604_ssp|SSP]] ([[604_ssp|Security Support Provider]]) — [[303_authentication_authorization_patterns|인증]] 공급자 DLL
605. Golden/[[589_silver_ticket|Silver Ticket]] [[605_golden_silver_ticket_mitigation|mitigation]] — KRBTGT 비밀번호 周월적 교체
606. Protected Users 그룹 — [[545_kerberos_kdc_ticket_based_auth|Kerberos]] 전용 [[303_authentication_authorization_patterns|인증]]
607. [[607_smart_card|Smart Card]] — [[303_authentication_authorization_patterns|인증]]서 기반 [[552_mfa|MFA]]
608. [[608_pkinit|PKINIT]] — Kerberos에서 공개키 [[303_authentication_authorization_patterns|인증]] 사용
609. [[609_remote_desktop_gateway|Remote Desktop Gateway]] — RDG, [[471_https_http_over_tls|HTTPS]] 기반 원격접속
610. Azure AD条件부 액세스 — [[164_policy|정책]] 기반 접근 제어
611. [[611_conditional_access_signals|조건부 액세스 신호]] — 사용자/위험/디바이스/위치
612. [[612_identity_protection|Identity Protection]] — Azure AD ID [[571_protection_vs_security|보호]]
613. [[613_ueba|UEBA]] (User Entity Behavior Analytics) — 행동 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
614. [[614_ad_hoc_identity|애드혹 identity]] — 임시/외부 사용자 관리
615. [[615_federated_identity|Federated Identity]] — SAML/[[537_oidc_openid_connect|OIDC]] 기반 연합
616. [[616_identity_bridge|Identity Bridge]] — AD FS, [[550_azure_ad_connect|Azure AD Connect]] [[543_federation|Federation]]
617. SCIM 2.0 — 자동 사용자 [[528_provisioning|프로비저닝]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
618. [[568_jit_access|JIT]] [[528_provisioning|프로비저닝]] — [[568_jit_access|Just-In-Time]], On-Demand [[528_provisioning|프로비저닝]]
619. [[619_id_governance_iga|ID Governance]] — 권한 [[303_authentication_authorization_patterns|인증]], 합성성 검토
620. [[620_privileged_identity_management_pim|Privileged Identity Management]] ([[430_pim|PIM]]) —Azure 특권 ID 관리

---

## 13. 보안 운영 (SecOps) — 60개

621. [[131_soc|SOC]] ([[855_soc_2|Security Operations Center]]) — 보안 관제 조직
622. [[131_soc|SOC]] 티어 — 티어 1(alert 분석)/2( approfondita調査)/3( [[689_threat_hunting|threat hunting]])
623. [[367_noc|NOC]] ([[623_noc|Network Operations Center]]) — 네트워크 모니터링
624. [[624_siem|SIEM]] ([[283_security_tactics|Security]] Information and [[074_event_management|Event Management]]) — [[568_logs_distributed_logging_elk_fluentd|로그]] 집적/[[325_correlation_analysis_pearson_spearman|상관 분석]]
625. [[624_siem|SIEM]] 구성 — 수집(Curator)/저장(Repository)/분석(Analyzer)/可视化(Dashboard)
626. [[626_log_collection|로그 수집]] — [[535_syslog_protocol_udp_514|syslog]], Windows Event Log, [[539_netflow_sflow_traffic_monitoring|NetFlow]], PCAP
627. Normalizzazione — 다양 [[568_logs_distributed_logging_elk_fluentd|로그]] 형식 [[093_normalization|정규화]]
628. [[325_correlation_analysis_pearson_spearman|상관 분석]] (Correlation) — 이벤트 간 [[083_relationship_in_er_model|관계]] 탐지
629. [[629_ueba_in_siem|UEBA in SIEM]] — 행동 분석 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]
630. [[630_splunk|Splunk]] — Enterprise [[624_siem|SIEM]]
631. [[631_elastic_siem|Elastic SIEM]] — [[302_cdc|Elasticsearch]] 기반
632. [[632_qradar|QRadar]] — IBM [[624_siem|SIEM]]
633. [[633_arcsight|ArcSight]] — HPE/Micro Focus [[624_siem|SIEM]]
634. [[634_graylog|Graylog]] — [[191_oss_license_compliance|오픈소스]] [[624_siem|SIEM]]
635. [[635_wazuh|Wazuh]] — [[191_oss_license_compliance|오픈소스]] [[624_siem|SIEM]]/[[325_edr|EDR]]
636. [[745_soar_security_orchestration_automation_response|SOAR]] ([[283_security_tactics|Security]] [[073_container_orchestration_tools|Orchestration]], Automation, Response) — 자동화 대응
637. [[637_playbook|플레이북]] — 시나리오별 자동 대응 절차
638. [[638_security_automation|보안 자동화]] — 반복 작업 자동화
639. [[746_ti_threat_intelligence_ioc_stix_taxii|Threat Intelligence]] — 위협 정보 공유
640. [[746_ti_threat_intelligence_ioc_stix_taxii|TI]] 4가지 유형 — [[268_strategy_pattern|전략]]/전술/운영/기술적
641. STIX/TAXII — 위협 정보 교환 표준
642. [[642_mitre_attack|MITRE ATT&CK]] — 공격자 전술/기법/절차DB
643. [[643_attack_matrix|ATT&CK Matrix]] — Pre-ATT&CK/Enterprise/Mobile
644. [[644_sub_techniques|Sub-techniques]] — 세분화된 공격 기법
645. [[199_cyber_kill_chain_mitre_attack|Cyber Kill Chain]] — Lockheed Martin 7단계
646. UNC/[[748_apt|APT]] 그룹 — [[748_apt|APT]] 집합 명칭 (MITRE)
647. [[647_diamond_model|Diamond Model]] — 공격 분석 4要素 모델
648. [[648_pyramid_of_pain|Pyramid of Pain]] — 위협 Inteligence 가치 계층
649. [[649_osint|OSINT]] ([[649_osint|Open Source Intelligence]]) — 공개 출처 위협 정보
650. [[409_cve_lifecycle|CVE]]/[[407_cvss_scoring|CVSS]] — 취약점 점수 체계
651. [[651_nvd|NVD]] ([[651_nvd|National Vulnerability Database]]) — NIST [[409_cve_lifecycle|CVE]] DB
652. [[652_incident_response_nist_800_61|인시던트 대응]] ([[165_ir|IR]]) — NIST 6단계
653. [[165_ir|IR]] 단계 — 준비/[[655_ir_detection_analysis|식별]]/[[656_ir_containment|억제]]/[[657_ir_eradication|근절]]/[[658_ir_recovery|복구]]/[[659_ir_lessons_learned|교훈]]
654. [[165_ir|IR]] 준비 — 대응 계획, 팀 구성, 교육
655. [[655_ir_detection_analysis|식별]] — 모니터링/알람→初步 분석
656. [[656_ir_containment|억제]] ([[656_ir_containment|Containment]]) — 단기([[195_isolation_concurrency_control|isolation]])/장기(정상运营 복귀)
657. [[657_ir_eradication|근절]] ([[657_ir_eradication|Eradication]]) — 감염 원인 제거
658. [[658_ir_recovery|복구]] — 시스템 정상화, 운영 재개
659. [[659_ir_lessons_learned|교훈]] ([[659_ir_lessons_learned|Lessons Learned]]) — 후속 조치, 보고서 작성
660. [[660_tabletop_exercise|tabletop exercise]] —桌上演習, 시나리오 기반 연습
661. [[661_dfir|DFIR]] (Digital Forensics and [[806_incident_response|Incident Response]]) — 디지털 포렌식+[[165_ir|IR]]
662. [[662_forensics_4_principles|포렌식 4원칙]] — 순수성/재현성/[[395_verification_process_review|검증]]/객관성
663. [[663_evidence_preservation|증거 보전]] —write blocker, [[003_integrity|integrity]] hashing
664. [[664_chain_of_custody|Chain of Custody]] — 증거 이동/처리 기록
665. [[665_memory_forensics|메모리 포렌식]] — Volatility, Rekall
666. [[666_ram_dump|RAM Dump]] — 물리 메모리 덤프
667. [[667_pagefile_hiberfil_analysis|페이지 파일 분석]] — pagefile.sys, hiberfil.sys
668. [[668_network_forensics|네트워크 포렌식]] — PCAP, [[539_netflow_sflow_traffic_monitoring|NetFlow]], [[511_dns_hierarchical_distributed_architecture|DNS]] [[568_logs_distributed_logging_elk_fluentd|로그]]
669. [[669_log_preservation|로그 보전]] — [[535_syslog_protocol_udp_514|syslog]], Windows Event, [[690_firewall_generation_evolution|Firewall]] [[568_logs_distributed_logging_elk_fluentd|로그]]
670. [[670_timeline_analysis|타임라인 분석]] — 이벤트 시간순 재구성
671. MFT 분석 — Windows NTFS [[012_metadata|메타데이터]]
672. [[672_registry_analysis|레지스트리 분석]] — NTUSER.DAT, SAM, [[283_security_tactics|SECURITY]] [[544_hive|hive]]
673. [[673_stealth_techniques|스텔스 기법]] — [[674_anti_forensics|anti-forensics]], [[568_logs_distributed_logging_elk_fluentd|로그]] 삭제
674. [[674_anti_forensics|anti-forensics]] — 증거 인멸/변조 기술
675. 脆弱点 スキャン — Nessus, OpenVAS, Qualys
676. [[676_penetration_testing|침투 테스트]] — 합법적 해킹 시뮬레이션
677. [[677_ptes|PTES]] — [[676_penetration_testing|Penetration Testing]] Execution Standard
678. [[678_owasp_testing_guide|OWASP Testing Guide]] — 웹 앱 테스트 가이드
679. [[679_osstmm|OSSTMM]] — 보안 테스트 방법론
680. [[680_bug_bounty|버그 바운티]] — 공개 취약점 보상 프로그램

---

## 14. 보안 운영 심화 / [[689_threat_hunting|위협 헌팅]] — 40개

681. [[681_red_team|레드팀]] — 적대적 관점, 실제 공격 시뮬레이션
682. [[682_blue_team|블루팀]] — 방어 관점, 탐지/대응
683. [[683_purple_team|퍼플팀]] — 레드+블루 협력
684. [[684_white_team|White Team]] — 시나리오 관리/심사
685. [[685_adversarial_simulation|적대적 시뮬레이션]] — [[681_red_team|Red Team]] vs [[683_purple_team|Purple Team]] exercises
686. [[686_assumed_breach|가정 침투]] ([[686_assumed_breach|Assumed Breach]]) — 내부 접근 가정
687. [[687_bas|BAS]] (Breach and Attack Simulation) — 자동화된 공격 시뮬레이션
688. [[683_purple_team|Purple Team]] — 공격/방어 협력, 탐지 규칙 개선
689. [[689_threat_hunting|위협 헌팅]] ([[689_threat_hunting|Threat Hunting]]) — 가설 기반 선제적 탐색
690. Huntington 가설 — "공격자는 이미 내부에 있다"
691. [[691_hunting_loop|Hunting Loop]] —가설/탐색/발견/정보 공유
692. [[692_mitre_engage|MITRE Engage]] — 방어적 사이버 [[268_strategy_pattern|전략]] 프레임워크
693. [[693_deception_technology|Deception Technology]] —蜜罐/蜜网/ [[696_canary_token|canary token]]
694. [[694_honey_pot|Honey Pot]] — 유인 시스템
695. [[695_honey_net|Honey Net]] — 유인 네트워크 세그먼트
696. [[696_canary_token|Canary Token]] — 조기 탐지용 경보
697. [[501_file_definition_logical_record|파일]] [[595_canary_stack_smashing_protector|canary]] — 조기 침해 탐지
698. 브라우저 [[595_canary_stack_smashing_protector|canary]] — [[160_session_controlling_terminal|세션]] 탈취 탐지
699. [[699_forensic_image|포렌식 이미지]] — [[769_architecture|DD]], FTK Imager
700. [[668_md5_hash_collision_vulnerability|MD5]]/SHA-256 해시 — 증거 [[003_integrity|무결성]] [[395_verification_process_review|검증]]
701. FTK / EnCase — 포렌식 도구
702. [[702_axiom|AXIOM]] — [[702_axiom|Magnet Forensics]] 포렌식
703. UAC绕过 — 사용자 계정 컨트롤 우回
704. LSASS 추출 — [[602_mimikatz|Mimikatz]], procdump
705. [[705_sam_hive|SAM hive]] 추출 — [[705_sam_hive|reg save]] HKLM\SAM
706. [[706_kerberoasting|Kerberoasting]] — SPN 요청 티켓 hash 추출
707. [[707_asrep_roasting|AS-REP Roasting]] — 사전 [[303_authentication_authorization_patterns|인증]] 미사용 계정 공격
708. [[708_dcsync|DCSync]] — DC에서 크리덴셜Replication 요청
709. NTDS.dit 추출 — DC [[002_database_definition|데이터베이스]] 직접 추출
710. [[710_bloodhound|BloodHound]] — AD 공격 경로 분석 도구
711. [[711_crackmapexec|CrackMapExec]] — 네트워크 크리덴셜 공격 도구
712. [[712_empire|Empire]] / PowerShell [[712_empire|Empire]] — 포스트-침투 프레임워크
713. [[747_cobalt_strike|Cobalt Strike]] — 상업용 [[676_penetration_testing|침투 테스트]] 도구
714. [[714_sliver|Sliver]] — [[191_oss_license_compliance|오픈소스]] [[746_c2|C2]] 프레임워크
715. [[715_caldera|Caldera]] — MITRE 자동화 [[685_adversarial_simulation|적대적 시뮬레이션]]
716. [[716_red_canary|Red Canary]] — [[325_edr|EDR]],威胁検出
717. [[717_osquery|osquery]] —Endpoint [[003_bigdata_7v|시각화]]/[[298_qkv_attention|쿼리]]
718. Sysmon — Windows 시스템 모니터링
719. [[241_zeek_bro_network_traffic_metadata_analysis|Zeek]] — 네트워크 트래픽 분석
720. YARA — 악성코드 패턴 규칙

---

## 15. 악성코드 / 공격 기법 — 60개

721. [[721_malware_classification|악성코드 분류]] — [[589_virus|바이러스]]/웜/[[726_trojan_horse|트로이목마]]/[[730_ransomware|랜섬웨어]]/[[739_spyware|스파이웨어]]/[[603_rootkit_syscall_hooking|루트킷]]
722. [[589_virus|바이러스]] ([[589_virus|Virus]]) — 정상 [[501_file_definition_logical_record|파일]]에感染, 자기 [[016_replication_factor|복제]]
723. 웹orm — 네트워크 통해 само[[016_replication_factor|복제]], 독립 실행
724. [[724_network_worm|네트워크 웜]] — 취약점 직접 침투 ([[082_process_memory_structure|Code]] Red, SQL Slammer)
725. [[725_email_worm|이메일 웜]] — 메일附件/링크 (ILOVEYOU)
726. [[726_trojan_horse|트로이목마]] — 겉보기에 정상, 실질적으로 악성
727. バックドア — 정상software伪装된 후면入口
728. [[728_dropper|드롭퍼]] ([[728_dropper|Dropper]]) — 다단계 [[729_downloader|Downloader]]
729. [[729_downloader|Downloader]] — 원격에서 추가 악성코드 가져옴
730. [[730_ransomware|랜섬웨어]] 공격 체인 — [[501_file_definition_logical_record|파일]] 암호화 후 몸값
731. [[731_cryptolocker|CryptoLocker]] — 2014년 대규모 [[730_ransomware|랜섬웨어]]
732. [[732_wannacry|WannaCry]] — 2017년 글로벌, EternalBlue 활용
733. [[733_notpetya|NotPetya]] — 2017년 Ukraine 전력网攻击
734. [[734_ryuk|Ryuk]] — 목표형 대규모 [[730_ransomware|랜섬웨어]]
735. 이중extortion — 암호화+[[001_dikw_pyramid|데이터]] 유출
736. [[736_raas|RaaS]] ([[730_ransomware|Ransomware]] [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) — [[730_ransomware|랜섬웨어]] 임대 [[090_service_kubernetes_network_load_balancing|서비스]]
737. [[737_locker|Locker]] — 화면 잠금형 [[730_ransomware|Ransomware]]
738. wipers — [[001_dikw_pyramid|데이터]] 파괴 목적
739. [[739_spyware|스파이웨어]] ([[739_spyware|Spyware]]) — 사용자 활동 감시
740. [[740_keylogger|키로거]] — 키入力 기록
741. 广告软件 ([[741_adware|Adware]]) — 강제 광고 표시
742. [[742_cryptominer|cryptominer]] — 시스템 자원 활용 암호화폐 채굴
743. [[743_bots|bots]] — 명령 制圧力 갖춘 감염 호스트
744. [[990_botnet_cnc|botnet]] — 다수의 [[743_bots|bots]] 집합
745. [[990_botnet_cnc|botnet]] 구조 — 중앙집중형 (C&C)/[[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]]
746. [[746_c2|C2]] ([[746_c2|Command and Control]]) — [[990_botnet_cnc|봇넷]] 지휘 통제
747. [[747_cobalt_strike|Cobalt Strike Beacon]] — [[676_penetration_testing|침투 테스트]]용 [[746_c2|C2]]
748. [[748_apt|APT]] ([[374_apt|Advanced Persistent Threat]]) — 국가/조직적 위협
749. [[748_apt|APT]] 그룹 — Lazarus(北한국), FIN7(범죄조직), APT29(러시아)
750. [[748_apt|APT]] 공격 단계 — 정찰/침투/내부정찰/横向移动/유지/[[001_dikw_pyramid|데이터]]반출
751. First [[751_initial_access|Initial Access]] — 최초 침투 수단
752. [[752_phishing|피싱]] ([[752_phishing|Phishing]]) — 가장 일반적인 침투 수단
753. [[753_spear_phishing|스피어 피싱]] ([[753_spear_phishing|Spear Phishing]]) — 목표 맞춤형
754. [[754_whaling|웨일링]] ([[754_whaling|Whaling]]) — 임원 대상 고대상 [[752_phishing|피싱]]
755. [[755_bec|BEC]] ([[755_bec|Business Email Compromise]]) — 경영자 사칭 금융 사기
756. [[756_smishing|스미싱]] ([[756_smishing|Smishing]]) — SMS 기반 [[752_phishing|피싱]]
757. [[757_vishing|비싱]] ([[757_vishing|Vishing]]) — 전화 기반 [[752_phishing|피싱]]
758. [[758_pretexting|사전조사]] ([[758_pretexting|Pretexting]]) — 거짓 상황 구성
759. [[759_tailgating|테일게이팅]] ([[759_tailgating|Tailgating]]) — 따라 들어가기
760. [[760_busybasing|버스딩]] ([[760_busybasing|Busybasing]]) —注意力转移
761. [[761_zero_day|제로데이]] — 공개되지 않은 취약점 利用
762. [[762_watering_hole|watering hole]] — 목표 집합 자주 방문 사이트 감염
763. [[763_drive_by_download|drive-by download]] — 악성 사이트 접근만으로 감염
764. 供应链攻击 — 소프트웨어 개발망 침해 (SolarWinds)
765. [[765_update_interception|업데이트 역추적]] ([[765_update_interception|Update Interception]]) — 자동更新 가로채기
766. 다형성 (Polymorphic) — 암호화된 코드,侦码 변경
767. 메타모픽 (Metamorphic) — 코드 자체 변환
768. [[768_armored_virus|armored virus]] —侦码 회피를 위한 [[571_protection_vs_security|보호]] 层
769. [[501_file_definition_logical_record|파일]]리스 (Fileless) — 메모리만 사용, [[501_file_definition_logical_record|파일]] 없는 공격
770. [[770_lolbins|LOLBins]] (Living Off the Land) — 정당한 도구 활용
771. PowerShell 공격 — 메모리 내 스크립트 실행
772. WMI 공격 — WMI 이벤트消费者 활용
773. JScript/VBScript 공격 — 스크립트 기반
774. [[774_registry_run_key|레지스트리 런키]] — 자동 실행 등록 정보
775. [[775_scheduled_task|예약 작업]] ([[775_scheduled_task|Scheduled Task]]) — 정기적 실행
776. [[090_service_kubernetes_network_load_balancing|서비스]] 등록 — Windows [[090_service_kubernetes_network_load_balancing|서비스]]로潜伏
777. [[511_dns_hierarchical_distributed_architecture|DNS]] [[377_tunneling_mechanism_overview|터널링]] — [[511_dns_hierarchical_distributed_architecture|DNS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 내 [[001_dikw_pyramid|데이터]] 반출
778. [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] [[377_tunneling_mechanism_overview|터널링]] — [[318_icmp_internet_control_message_protocol_diagnostics|ICMP]] 패킷 내 [[001_dikw_pyramid|데이터]] 운반
779. [[471_https_http_over_tls|HTTPS]] 역투명 relay — 내부망 통신 외부로
780. [[780_dynamic_proxy|동적 프록시]] — 감염 호스트를 Proxy로 활용

---

## 16. [[001_dikw_pyramid|데이터]] / [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]] — 55개

781. [[781_personal_information|개인정보]] ([[781_personal_information|Personal Information]]) — 재识别 가능 정보
782. [[782_sensitive_information|민감정보]] — 건강/범죄기록/유전정보/ biometric
783. [[783_pipa_korea|개인정보보호법]] (한국) — 수집/처리/提供/파기 원칙
784. [[784_privacy_3_principles|개인정보 3대 원칙]] — 수집 제한/목적 명확/보유 기간
785. [[174_privacy_impact_assessment|개인정보 영향평가]] ([[335_privacy_impact_assessment_pia_audit_linkage|PIA]]) — 고위험 처리前 평가
786. [[781_personal_information|개인정보]] [[501_file_definition_logical_record|파일]] 표준 [[571_protection_vs_security|protection]] 지침 — 한국 [[783_pipa_korea|개인정보보호법]] 시행규칙
787. 정보보호 管理체계 ([[171_isms_p|ISMS-P]]) — 한국 통합 [[303_authentication_authorization_patterns|인증]]
788. [[788_isp_obligations|정보통신서비스]]提供者 ([[101_isp_information_strategy_planning_4_steps|ISP]]) — 한국법상 의무
789. 利用약관 — [[090_service_kubernetes_network_load_balancing|서비스]] 제공을 위한 기본 계약
790. [[790_consent_methods|동의 방식]] — 필수 동의/선택 동의
791. [[791_gdpr_eu|GDPR]] (EU General [[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]] Regulation) — 2018 시행
792. [[791_gdpr_eu|GDPR]] 6가지 처리 근거나유 — 동의/계약/법적 의무/생명 [[571_protection_vs_security|보호]]/공익/정당한 이해관계
793. [[793_data_subject_rights|정보 주체 권리]] — 접근/정정/삭제/처리 제한/이동/거부
794. Right to be Forgotten — 삭제권 ([[791_gdpr_eu|GDPR]] 17조)
795. [[795_data_portability|Data Portability]] — 이동권 ([[791_gdpr_eu|GDPR]] 20조)
796. [[796_gdpr_dpia|DPIA]] ([[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]] Impact Assessment) — [[791_gdpr_eu|GDPR]] 의무
797. [[270_embedding_model|DPO]] ([[797_gdpr_dpo|Data Protection Officer]]) — [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]]관
798. [[798_breach_notification|Breach Notification]] — 72시간 내 신고 의무
799. [[799_cross_border_data_transfer|개인정보 해외 이전]] — 충분성 인정 국가/표준 계약 조항
800. [[800_ccpa|CCPA]] (California Consumer Privacy Act) — 2020 시행
801. [[801_cpra|CPRA]] (California Privacy Rights Act) — [[800_ccpa|CCPA]] 강화
802. [[802_pdpa|PDPA]] (Personal [[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]] Act) — 싱가포르
803. [[803_privacy_law_comparison|개인정보보호]] 法律体系 — 한국/미국/EU 비교
804. [[171_isms_p|ISMS-P]] 심사 — 기술적/관리적/물리적 安全 Control 평가
805. [[805_security_measures|정보보호 주요]]安全管理 —
806. [[781_personal_information|개인정보]] 유출 사고 — 신고/통지/공표 의무
807. 과태료/벌칙 — 한국 [[783_pipa_korea|개인정보보호법]] 제64조
808. [[808_data_classification|데이터 분류]] — 공개/내부/기밀/극비
809. [[809_data_sovereignty|데이터 주권]] — 국가별 [[001_dikw_pyramid|데이터]]本地화 법規
810. [[001_dikw_pyramid|데이터]] 이동 — Cross-border [[001_dikw_pyramid|데이터]] 흐름
811. [[811_privacy_in_cloud|클라우드 개인정보보호]] — [[001_dikw_pyramid|데이터]] 소재지 주의
812. [[001_dikw_pyramid|데이터]]匿名화 — 완전히 역추적 불가능
813. [[001_dikw_pyramid|데이터]]가명화 — [[655_ir_detection_analysis|식별]]가능성 제거,pseudo-anonymization
814. [[185_k_anonymity_masking_data_pipeline|k-익명성]] — k-person indistinguishability
815. [[815_l_diversity|l-다양성]] — 민감 [[082_attribute_types_er_model|속성]] 다변화
816. [[816_t_closeness|t-근접성]] — 레코드 분포 유사성
817. [[817_differential_privacy|차분 개인정보보호]] — [[817_differential_privacy|differential privacy]]
818. [[818_synthetic_data|합성 데이터]] — [[818_synthetic_data|Synthetic data]] [[087_process_state_transition|생성]]
819. [[819_data_masking|데이터 마스킹]] — 동적/정적 마스킹
820. [[820_tokenization|토큰화]] ([[820_tokenization|Tokenization]]) — 원본↔토큰 매핑
821. TTT ([[821_taas|Tokenization-as-a-Service]]) — 클라우드 [[820_tokenization|토큰화]]
822. [[822_fpe|Format Preserving Encryption]] — [[822_fpe|FPE]], 원 [[001_dikw_pyramid|데이터]] 형식 유지
823. [[386_dlp|DLP]] ([[823_dlp|Data Loss Prevention]]) — [[001_dikw_pyramid|데이터]] 반출 방지
824. [[386_dlp|DLP]] 구성要素 —엔진/에이전트/서버
825. [[386_dlp|DLP]] [[164_policy|정책]] — 콘텐츠 검사/[[033_context|컨텍스트]] 기반
826. 네트워크 [[386_dlp|DLP]] — 네트워크 경계 [[001_dikw_pyramid|데이터]] 통제
827. 엔드포인트 [[386_dlp|DLP]] — 단말기 내 [[001_dikw_pyramid|데이터]] 통제
828. 클라우드 [[386_dlp|DLP]] — [[309_saas|SaaS]]/ [[184_paas_platform_as_a_service|PaaS]]/[[183_iaas_infrastructure_as_a_service|IaaS]] [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]]
829. [[741_casb_cloud_access_security_broker|CASB]] (Cloud Access [[283_security_tactics|Security]] Broker) — 클라우드 가시성/제어
830. [[830_db_security|데이터베이스 보안]] — [[387_access_control_pattern|접근 통제]]/암호화/[[606_auditing_linux_auditd|감사]]
831. [[831_field_level_security|필드 레벨 보안]] — DB 컬럼/행 수준 접근 제어
832. DB [[606_auditing_linux_auditd|감사]] — 접속 기록, 질의 [[568_logs_distributed_logging_elk_fluentd|로그]]
833. [[833_encryption_in_transit|전송 중 암호화]] — [[694_thread_local_storage_tls|TLS]], [[589_ipsec_offload|IPsec]]
834. [[834_encryption_at_rest|저장 중 암호화]] — [[403_tde_transparent_data_encryption|TDE]], 디스크 암호화
835. [[835_encryption_in_use|메모리 내 암호화]] — 클라우드 [[475_hsm|HSM]]

---

## 17. 보안 프레임워크 / 컴플라이언스 — 55개

836. ISO/IEC 27001 — 정보보안 [[372_management|management]] 시스템 ([[836_iso_27001_isms|ISMS]])
837. [[836_iso_27001_isms|ISMS]] [[303_authentication_authorization_patterns|인증]] — 3자 [[606_auditing_linux_auditd|감사]], [[303_authentication_authorization_patterns|인증]]서 발급
838. [[838_pdca_model|PDCA]] ([[838_pdca_model|Plan-Do-Check-Act]]) — 관리 시스템 적용 모델
839. ISO 27001 114개 통제 — Annex A
840. ISO/IEC 27002 — 보안 통제 implementation 지침
841. ISO/IEC 27005 — 정보보안 위험 관리
842. [[842_iso_27017_cloud_security|ISO 27017]] — 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]] 보안 통제
843. [[843_iso_27018_cloud_pii|ISO 27018]] — 클라우드 PII [[571_protection_vs_security|보호]]
844. [[844_iso_27701_pims|ISO 27701]] — [[803_privacy_law_comparison|개인정보보호]] 정보安全管理
845. [[845_iso_22301_bcms|ISO 22301]] — 사업 연속성 관리 시스템 ([[845_iso_22301_bcms|BCMS]])
846. NIST [[017_csf|CSF]] 2.0 —Identify/Protect/Detect/Respond/Recover + Govern
847. [[847_nist_csf_tier|NIST CSF Tier]] — [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Inform/Repeatable/Adaptive
848. [[848_nist_sp_800_53|NIST SP 800-53]] — 연방 정보시스템 보안 통제 (800+ 통제)
849. [[849_nist_sp_800_171|NIST SP 800-171]] — CUI [[571_protection_vs_security|보호]] (110 통제)
850. [[850_nist_sp_800_207|NIST SP 800-207]] — [[184_zero_trust_architecture|제로 트러스트 아키텍처]]
851. [[851_nist_sp_800_63|NIST SP 800-63]] — 디지털 신원 지침
852. [[852_nist_sp_800_63a|NIST SP 800-63A]] — Enrollment and Identity Proofing
853. [[853_nist_sp_800_63b|NIST SP 800-63B]] — [[604_authentication_factors|Authentication]] and Lifecycle
854. [[854_nist_sp_800_63c|NIST SP 800-63C]] — [[543_federation|Federation]] and Assertions
855. [[855_soc_2|SOC 2]] — AICPA [[090_service_kubernetes_network_load_balancing|서비스]] 조직 통제 보고서
856. [[855_soc_2|SOC 2]] Trust [[090_service_kubernetes_network_load_balancing|Service]] Criteria — 보안/[[452_availability|가용성]]/처리 [[003_integrity|무결성]]/机密性/隐私
857. [[855_soc_2|SOC 2]] Type I/II — 설계 적정성/운영 효과성
858. [[858_soc_3|SOC 3]] — 공용 [[288_version_ihl_tos_total_length|버전]] [[855_soc_2|SOC 2]]
859. [[355_pci|PCI]] DSS v4.0 — Payment Card Industry [[001_dikw_pyramid|Data]] [[283_security_tactics|Security]] Standard
860. [[355_pci|PCI]] DSS 12개 요구사항 — [[690_firewall_generation_evolution|방화벽]]/비밀번호/[[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]] 등
861. [[355_pci|PCI]] DSS 수준 —merchant/[[535_sp_service_provider|service provider]] 등급
862. [[862_pa_dss|PA-DSS]] — Payment Application [[001_dikw_pyramid|Data]] [[283_security_tactics|Security]] Standard
863. [[863_hipaa|HIPAA]] — 미국 의료정보 [[571_protection_vs_security|보호]]법
864. [[864_phi|PHI]] ([[864_phi|Protected Health Information]]) — [[863_hipaa|HIPAA]] 적용 정보
865. [[865_hitech|HITECH]] — 미국 의료기술법, 위반 시 책임 강화
866. [[866_glba|GLBA]] ([[866_glba|Gramm-Leach-Bliley Act]]) — 미국 금융정보보호
867. [[867_ferpa|FERPA]] — 미국 교육 기록 프라이버시
868. [[194_cmmc_cybersecurity_maturity|CMMC]] (Cybersecurity [[011_maturity_model|Maturity Model]] Certification) — 미국 방위산업
869. [[194_cmmc_cybersecurity_maturity|CMMC]] 5단계 — Level 1~5 점진적 [[303_authentication_authorization_patterns|인증]]
870. [[870_fisma|FISMA]] — 미국 연방 정보 보안 법
871. [[871_fedramp|FedRAMP]] — 미국 정부 클라우드 보안 [[303_authentication_authorization_patterns|인증]]
872. [[871_fedramp|FedRAMP]] Moderate/High — 영향 수준별 기준
873. ITGrc — IT 거버넌스/[[096_risk_non_risk_architecture_evaluation_flaws|리스크]]/컴플라이언스
874. [[042_sabsa|SABSA]] —Business-driven [[302_security_architecture_design|보안 아키텍처]]
875. [[113_togaf|TOGAF]] — 기업 아키텍처 프레임워크
876. [[112_zachman_framework|Zachman Framework]] — [[110_enterprise_architecture_ea|EA]] planning 매트릭스
877. [[877_cis_controls_v8|CIS Controls v8]] — 18개 핵심 보안 통제
878. [[878_cis_safeguard|CIS Safeguard]] — Implement/M测量/관리
879. [[005_cobit_2019|COBIT 2019]] — IT 거버넌스 프레임워크
880. [[062_itil|ITIL]] (Information Technology Infrastructure [[336_library_vs_framework|Library]]) — IT [[090_service_kubernetes_network_load_balancing|서비스]] 관리
881. [[060_privacy_by_design|Privacy by Design]] — 설계 단계 [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]]
882. [[060_privacy_by_design|PbD]] 7基本原则 — 사전 [[571_protection_vs_security|보호]]/기본값私密性 등
883. [[883_common_criteria_iso_15408|CC]] ([[883_common_criteria_iso_15408|Common Criteria]]) / ISO 15408 — 제품 보안 [[303_authentication_authorization_patterns|인증]]
884. [[884_cc_eal_evaluation_assurance_levels|CC EAL]] — 평가 보증 수준 (EAL 1~7)
885. FIPS 140-2/3 — 암호 [[192_module_independence|모듈]] 보안 표준
886. [[886_k_isms|K-ISMS]] — 한국 정보보호管理체계 [[303_authentication_authorization_patterns|인증]]
887. [[887_kisa_assessment|정보보호평가]] — 한국互联网振興院 (KISA)
888. [[888_electronic_financial_supervision_regulation|전자금융감독규정]] — 금융 전산 보안 기준
889. [[889_fss_cyber_supervision|금융감독원]] ([[889_fss_cyber_supervision|FSS]]) — 금융 사이버 감독
890. [[890_sbom_cyclonedx_spdx|SBOM]] (Software [[124_bom_bill_of_materials|Bill of Materials]]) — 소프트웨어 부품 목록

---

## 18. [[101_iot_concept|IoT]] / [[891_ot_operational_technology|OT]] / [[893_ics_industrial_control_system|ICS]] / 물리 보안 — 50개

891. [[891_ot_operational_technology|OT]] ([[891_ot_operational_technology|Operational Technology]]) — 운영기술, 산업控制系统
892. [[892_ot_vs_it|OT vs IT]] — [[345_reliability_security|reliability]]/[[452_availability|availability]]/real-time 차이
893. [[893_ics_industrial_control_system|ICS]] ([[893_ics_industrial_control_system|Industrial Control System]]) — 산업 제어 시스템
894. [[894_scada|SCADA]] (Supervisory Control and [[001_dikw_pyramid|Data]] [[042_aarrr_funnel|Acquisition]]) — 원격 감시 제어
895. [[895_dcs_distributed_control_system|DCS]] ([[895_dcs_distributed_control_system|Distributed Control System]]) — [[136_variance|분산]] 제어 시스템
896. [[896_plc_programmable_logic_controller|PLC]] ([[896_plc_programmable_logic_controller|Programmable Logic Controller]]) — 현장 제어기
897. [[897_rtu_remote_terminal_unit|RTU]] ([[897_rtu_remote_terminal_unit|Remote Terminal Unit]]) — 원격 터미널 장치
898. Modbus [[295_protocol_field_tcp_udp_icmp|프로토콜]] — 산업용 [[149_serial_communication_rs232_rs485|직렬]] 통신, 암호화 없음
899. [[899_dnp3_distributed_network_protocol|DNP3]] — 전력/상하수도 [[894_scada|SCADA]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
900. [[900_profinet|PROFINET]] — 산업용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]
901. [[230_ethernet_structure_and_principles_ieee_802_3|EtherNet]]/IP — CIP 기반 산업용 [[230_ethernet_structure_and_principles_ieee_802_3|이더넷]]
902. Purdue 모델 — IT/[[891_ot_operational_technology|OT]] 네트워크 5단계分层
903. Purdue 레벨 0~5 — Field/Level 1~2 ([[891_ot_operational_technology|OT]])/Level 3 ([[219_demilitarized_zone_dmz_public_subnet|DMZ]])/Level 4~5 (IT)
904. [[904_iec_62443|IEC 62443]] — 산업 사이버보안 표준
905. [[157_isa|ISA]]/[[904_iec_62443|IEC 62443]] 보안 레벨 — SL 0~4 (no [[283_security_tactics|security]]→most secure)
906. [[906_sl_cf_capability|SL-CF]] ([[906_sl_cf_capability|Security Level Capability]]) — 시설 보안 수준
907. [[907_sl_tf_target|SL-TF]] ([[907_sl_tf_target|Security Level Target]]) — 목표 보안 수준
908. Zone/Conduit 모델 — 구역 분리+ conduits통제
909. Zone 맵핑 — 자산 [[104_classification_analysis|분류]]→ [[283_security_tactics|security]] level
910. [[910_nist_ir_8259|NIST IR 8259]] — [[101_iot_concept|IoT]] 보안基礎
911. [[911_nist_ir_8259d|NIST IR 8259D]] — [[101_iot_concept|IoT]] 제조 商arangement
912. OWASP [[101_iot_concept|IoT]] Top [[489_raid_10_hybrid|10]] — 취약한 [[032_firmware|펌웨어]]/기본 계정/불안전한 接口
913. [[101_iot_concept|IoT]] 보안 설계 —[[061_secure_by_default|Secure by Default]], 최소 기능 원칙
914. [[101_iot_concept|IoT]] [[032_firmware|펌웨어]] 보안 — 서명 [[395_verification_process_review|검증]], 안전 업데이트
915. [[101_iot_concept|IoT]] [[001_dikw_pyramid|데이터]] 보안 —保存中/传输中/處理中
916. [[608_secure_boot|Secure Boot]] — 부팅 과정 소프트웨어 [[003_integrity|무결성]] [[395_verification_process_review|검증]]
917. [[917_root_of_trust|rantai-root-of-trust]] — 신뢰의 근원
918. RoT 구성要素 — CRTM, [[029_bootloader|Bootloader]], [[029_bootloader|Bootloader]] certificates
919. [[476_tpm|TPM]] 원격 증명 ([[396_remote_attestation|Remote Attestation]]) — [[476_tpm|TPM]] 측정값을 원격에서 [[395_verification_process_review|검증]]하는 과정
920. [[920_firmware_update_security|펌웨어 업데이트 보안]] —签名驗證, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 방지
921. [[622_mqtt_publish_subscribe_qos|MQTT]] 보안 — [[694_thread_local_storage_tls|TLS]], [[303_authentication_authorization_patterns|인증]], [[549_acl_access_control_list|ACL]]
922. [[922_bacnet|BACnet]] — 건물 자동화 [[295_protocol_field_tcp_udp_icmp|프로토콜]]
923. ，车辆网络安全 — UNECE WP.29
924. ISO/SAE 21434 — [[923_vehicle_cybersecurity|자동차 사이버보안]] 엔지니어링
925. [[925_tara|TARA]] (Threat Analysis and [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Assessment) — 자동차 위협 분석
926. [[926_medical_device_security|의료기기 보안]] — FDA cybersecurity 지침
927. [[927_medical_device_lifecycle|의료기기 사이버보안 관리]] — 디자인 단계부터
928. [[928_smart_grid_security|스마트 그리드 보안]] — [[162_ami_advanced_metering_infrastructure|AMI]] 보안
929. [[929_nerc_cip|NERC CIP]] — 북미 전력 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] Corporation
930. [[930_nuclear_cybersecurity|원자력 사이버보안]] — IAEA 안전기준
931. [[931_satellite_security|위성 통신 보안]] —，抗ジャミング/[[598_spoofing|스푸핑]]
932. 물리적 보안 3대 요소 —威慑/ Delay/ [[961_deepfake_detection|Detection]]
933. [[933_cctv|CCTV]] (閉路テレビ) — 영상 감시
934. 접근 제어 시스템 — 카드/RFID/바이오메트릭
935. [[935_mantrap|Mantrap]] — 이중 문으로 인적 격리
936. [[936_perimeter_security|주변 보안]] — 담장/감시/巡伺
937. [[937_environmental_control|환경 통제]] — 온도/습도/소화기
938. [[938_file_carving_network_forensics_pcap_signature_recovery|서버실 보안]] — Tier 1~4数据中心分级
939. [[939_honeypot_deception_technology_cyber_decoy_system|Faraday Cage]] — 전자기 차폐
940. 금屬 탐지기/ X-ray — 물리적脅威 탐지

---

## 19. [[190_ai_llm_requirements_specification|AI]] / 신기술 보안 — 50개

941. [[190_ai_llm_requirements_specification|AI]] 보안 — [[190_ai_llm_requirements_specification|AI]] 시스템의 安全+[[190_ai_llm_requirements_specification|AI]] 활용 보안
942. [[942_adversarial_example|적대적 예제]] ([[942_adversarial_example|Adversarial Example]]) — 미세한 perturbation로 오분류
943. [[943_fgsm|FGSM]] (Fast Gradient Sign Method) — 1단계 적대적扰动
944. [[944_pgd|PGD]] ([[944_pgd|Projected Gradient Descent]]) — 반복적 적대적扰动
945. [[945_cw_attack|Carlini-Wagner]] 공격 — 강력한 적대적 공격
946. 물리 세계 적대적 공격 — 도로 표지판 등 실환경 공격
947. [[947_data_poisoning|데이터 포이즈닝]] ([[947_data_poisoning|Data Poisoning]]) — 훈련 [[001_dikw_pyramid|데이터]] 오염
948. [[948_clean_label_poisoning|Clean-Label Poisoning]] — 레이블 유지한 [[001_dikw_pyramid|데이터]] 오염
949. [[949_backdoor_attack|Backdoor Attack]] — 특정 [[507_acid_properties|트리거]] 입력에 반응
950. [[950_model_extraction|모델 추출]] ([[950_model_extraction|Model Extraction]]) — [[298_qkv_attention|쿼리]] 기반 모델 역추출
951. [[951_model_inversion|Model Inversion]] — 훈련 [[001_dikw_pyramid|데이터]] 재구성
952. [[952_membership_inference|Membership Inference]] — 특정 [[001_dikw_pyramid|데이터]] 훈련 여부 추론
953. [[190_ai_llm_requirements_specification|AI]] 모델 탈취 — [[014_api_posix|API]] [[298_qkv_attention|쿼리]]로 모델 [[016_replication_factor|복제]]
954. [[954_model_integrity|모델 무결성 공격]] — 사본 배포, 악성 교체
955. [[955_prompt_injection|프롬프트 인젝션]] — [[263_llm_large_language_model|LLM]] 지시어 오버라이드
956. [[956_jailbreaking|Jailbreaking]] — [[263_llm_large_language_model|LLM]] 안전 필터 우회
957. [[957_adversarial_prompting|적대적 프롬프트]] — 의도한 잘못된 출력 유도
958. [[958_data_extraction|데이터 추출 공격]] — 훈련 [[001_dikw_pyramid|데이터]] 기억으로 정보 유출
959. [[190_ai_llm_requirements_specification|AI]] 기반 [[752_phishing|피싱]] — 개인화된 대규모 [[752_phishing|피싱]] 자동화
960. [[960_deepfake|Deepfake]] — 합성 미디어, 신원 사칭
961. [[961_deepfake_detection|딥페이크 탐지]] — [[962_c2pa|C2PA]], 디지털 워터마킹
962. [[962_c2pa|C2PA]] (Coalition for Content Provenance and [[005_authenticity|Authenticity]]) — 콘텐츠 출처
963. [[963_synthid|SynthID]] — Google 딥마크
964. [[964_ai_trism|AI TRiSM]] — Gartner, [[190_ai_llm_requirements_specification|AI]] 신뢰/위험/보안 관리
965. [[263_llm_large_language_model|LLM]] 가드레일 — 출력 필터링, 안전 레이어
966. [[966_constitutional_ai|Constitutional AI]] — 원칙 기반 [[190_ai_llm_requirements_specification|AI]] 행동 통제
967. [[967_ai_red_team|AI Red Team]] — [[263_llm_large_language_model|LLM]] 안전성 테스트
968. 对抗性训练 — [[942_adversarial_example|적대적 예제]] 포함한 재훈련
969. [[817_differential_privacy|differential privacy]] in ML — 훈련 [[001_dikw_pyramid|데이터]] privacy [[571_protection_vs_security|보호]]
970. [[256_federated_learning_privacy_model_security|Federated Learning]] — [[136_variance|분산]] 훈련, [[001_dikw_pyramid|데이터]] 불이동
971. [[1019_homomorphic_encryption|Homomorphic Encryption]] in ML — 암호화된 채로 추론
972. [[478_tee|TEE]] 기반 ML — [[389_sgx|SGX]] 등에서 안전한 추론
973. [[973_responsible_ai|Responsible AI]] — 공정성/설명가능성/투명성/ privacy
974. [[190_ai_llm_requirements_specification|AI]] Incident — [[190_ai_llm_requirements_specification|AI]] 관련 보안 사고DB
975. OWASP [[263_llm_large_language_model|LLM]] Top [[489_raid_10_hybrid|10]] — [[263_llm_large_language_model|LLM]] 보안 취약점
976. LLM01: [[955_prompt_injection|Prompt Injection]] — 프롬프트 조작
977. LLM02: Insecure Output — 출력 [[395_verification_process_review|검증]] 없이 신뢰
978. LLM03: [[588_mlops_pipeline_automation|Training]] [[947_data_poisoning|Data Poisoning]] — 훈련 [[001_dikw_pyramid|데이터]] 오염
979. LLM04: Model Denial of [[090_service_kubernetes_network_load_balancing|Service]] — 비용巨大的 입력 유발
980. LLM05: [[520_supply_chain_attack_and_ci_cd_security|Supply Chain]] — [[520_supply_chain_attack_and_ci_cd_security|공급망]] 취약점
981. LLM06: [[782_sensitive_information|Sensitive Information]] Disclosure — 훈련 [[001_dikw_pyramid|데이터]] 유출
982. LLM07: Plugin Abuse — 플러그인 악용
983. LLM08: Autonomous Agent — 자가 실행 에이전트 위험
984. [[236_quantum_computing_pqc|양자 컴퓨팅]] — [[219_quantum_superposition_qubit|양자 중첩]]/얽힘으로 계산 혁신
985. 양자 위협 — [[110_rsa|RSA]]/[[554_ecc_circuit|ECC]] 깨뜨릴 Shor [[001_algorithm_definition|알고리즘]]
986. [[986_grover_algorithm_impact|Grover]] [[001_algorithm_definition|알고리즘]] — 대칭키 강도半감
987. NIST [[351_quantum_computing_pqc_transition|PQC]] 표준 — Kyber/Dilithium/Falcon/[[149_sphincs_slh_dsa|SPHINCS]]+
988. [[153_crypto_agility|crypto agility]] — [[001_algorithm_definition|알고리즘]] 교체 능력
989. 区块链 보안 — 51% 공격, 이중지불, [[022_smart_contract|스마트 컨트랙트]]
990. Reentrancy 공격 — [[022_smart_contract|스마트 컨트랙트]] 재진입脆弱점

---

## 20. 보안 추가 키워드 / 시험 대비 — 40개

991. [[0991_evil_maid_attack|Evil Maid Attack]] — 물리적 접근 후 [[737_backdoor_c2_beacon_behavior_analysis|백도어]] 설치
992. [[0992_cold_boot_attack|Cold Boot Attack]] — [[0992_cold_boot_attack|메모리 잔상 읽기]]
993. [[746_io_direct_memory_access_dma|DMA]] 공격 — [[360_thunderbolt|Thunderbolt]]/[[356_pcie|PCIe]] [[318_dma|Direct Memory Access]]
994. [[150_usb_ieee1394_firewire|Firewire]] 공격 — IEEE 1394 [[746_io_direct_memory_access_dma|DMA]] 활용
995. [[0995_thunderbolt_security|Thunderbolt Security]] — [[746_io_direct_memory_access_dma|DMA]] 방어를 위한 레벨 [[009_config|설정]]
996. [[0996_usb_bad_hid_emulation|USB_BAD]] — [[359_usb|USB]] 키보드 emulation
997. [[0997_rubber_ducky_hid_attack|Rubber Ducky]] — [[359_usb|USB]] 키보드 emulation 도구
998. [[0998_bash_bunny_multi_tool|Bash Bunny]] — 다목적 [[359_usb|USB]] 공격 도구
999. [[0999_omg_cable_malicious_usb|OMG Cable]] — 변형된 [[359_usb|USB]] 케이블
1000. _entropy — 난수 [[087_process_state_transition|생성]] 품질
1001. [[1001_csprng_random_generator|CSPRNG]] (Cryptographically Secure PRNG) — [[652_cryptography_concept_encryption_decryption|암호학]]적으로 안전한 난수
1002. [[1002_rdrand_intel_hardware_rng|RDRAND]] (Intel) — 하드웨어 난수 [[087_process_state_transition|생성]]
1003. /dev/urandom — Linux 난수 장치
1004. [[1004_hardware_rng_trng|hardware RNG]] — [[1004_hardware_rng_trng|물리적 난수 발생기]]
1005. [[1005_entropy_source|entropy source]] — [[1005_entropy_source|난수 생성 원천]]
1006. [[1006_perfect_security_otp|Perfect Security]] — 정보 이론적 안전 ([[074_one_time_pad|One-Time Pad]])
1007. [[1007_semantic_security|Semantic Security]] — [[652_cryptography_concept_encryption_decryption|암호학]]적으로 관찰 가능한 차이 없음
1008. [[095_ind_cpa|IND-CPA]] / IND-CCA2 — [[1008_ind_cpa_ind_cca2|암호학 안전성]] 정의
1009. [[092_aead|AEAD]] — Authenticated Encryption with Associated [[001_dikw_pyramid|Data]]
1010. [[1010_key_wrapping_kek|Key Wrapping]] — KEK 활용
1011. [[1011_envelope_encryption|Envelope Encryption]] — Digital Envelope
1012. [[1012_cloud_hsm|CloudHSM]] — 클라우드 전용 [[475_hsm|HSM]]
1013. [[1013_aws_kms|AWS KMS]] — [[067_db_key_uniqueness_minimality|Key]] [[372_management|Management]] [[090_service_kubernetes_network_load_balancing|Service]]
1014. Bring Your Own [[067_db_key_uniqueness_minimality|Key]] ([[1014_byok_bring_your_own_key|BYOK]]) — 고객 관리 키
1015. Hold Your Own [[067_db_key_uniqueness_minimality|Key]] ([[1015_hyok_hold_your_own_key|HYOK]]) — 외부 키 보관
1016. [[1016_zero_knowledge_proof|Zero Knowledge Proof]] ([[354_did_decentralized_identity_zkp|ZKP]]) — [[229_zkp_data_clean_room|영지식 증명]]
1017. [[1017_commitment_scheme|Commitment Scheme]] — [[1017_commitment_scheme|약속 기법]]
1018. [[1018_secure_multi_party_computation|Secure Multi-Party Computation]] ([[1018_secure_multi_party_computation|SMPC]]) — 안전한 다자간 계산
1019. [[1019_homomorphic_encryption|동형 암호]] ([[1019_homomorphic_encryption|Homomorphic Encryption]]) — 암호문 상태 연산
1020. [[1020_functional_encryption|Functional Encryption]] — [[1020_functional_encryption|함수 암호]]
1021. [[1021_searchable_encryption|Searchable Encryption]] — [[1021_searchable_encryption|검색 가능 암호]]
1022. [[1022_anti_tamper_hardware|방변조 하드웨어]] — [[783_anti_tamper_mesh|Anti-tamper]] Hardware ([[476_tpm|TPM]]/[[475_hsm|HSM]])
1023. [[790_secure_enclave|Secure Enclave]] — TrustZone/[[389_sgx|SGX]] 격리 영역
1024. [[478_tee|TEE]] ([[972_tee_based_ml|Trusted Execution Environment]]) — [[478_tee|신뢰 실행 환경]]
1025. [[1025_security_chaos_engineering|Security Chaos Engineering]] — 보안 [[751_chaos_engineering|카오스 엔지니어링]]
1026. [[1026_breach_attack_simulation|침해 시뮬레이션]] ([[687_bas|BAS]]) — Breach & Attack Simulation
1027. [[1027_cyber_insurance|사이버 보험]] — [[1027_cyber_insurance|Cyber Insurance]]
1028. [[680_bug_bounty|Bug Bounty]] — [[680_bug_bounty|버그 바운티]]
1029. [[1029_responsible_disclosure|Responsible Disclosure]] — [[1029_responsible_disclosure|책임 있는 공개]]
1030. [[1030_coordinated_disclosure|Coordinated Disclosure]] — [[1030_coordinated_disclosure|협력적 공개]]

---

**총 키워드 수: 800개**
