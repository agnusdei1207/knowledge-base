+++
title = "09. 정보보안 키워드 목록"
date = 2026-03-25

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++
[weight](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) = 9999

# 정보보안 (Information [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 보안 전 영역 기술사 수준 핵심 키워드
> ⚡ 기술사 보안 문제는 단순 지식이 아닌 <strong><a href="/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/">위협 모델링</a> -> 아키텍처 설계 -> 법적·제도적 대응</strong>까지 통합 서술을 요구함

---

## 1. 정보보안 개론 / 원칙 — 67개

1. 정보보안 3요소 — CIA ([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/001_cia_triad/)·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/001_cia_triad/)·[가용성](/knowledge-base/studynote/09_security/01_intro_principles/001_cia_triad/))
2. [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) ([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) — 암호화, 접근 제어, [DRM](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [분류](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)
3. [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)) — 해시, [전자서명](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [MAC](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [HMAC](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [체크섬](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)
4. [가용성](/knowledge-base/studynote/09_security/01_intro_principles/004_availability/) ([Availability](/knowledge-base/studynote/09_security/01_intro_principles/004_availability/)) — HA 설계, [RAID](/knowledge-base/studynote/09_security/01_intro_principles/004_availability/), 부하 [분산](/knowledge-base/studynote/09_security/01_intro_principles/004_availability/), DDoS 방어, [SLA](/knowledge-base/studynote/09_security/01_intro_principles/004_availability/)
5. [인증성](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/) ([Authenticity](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/)) — 신원 [확인](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/), [PKI](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/), 디지털 서명, 메시지 [인증](/knowledge-base/studynote/09_security/01_intro_principles/005_authenticity/)
6. 부인방지 (Non-repudiation) — [전자서명](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/), 타임스탬프, [로그](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/), [감사](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/) 추적
7. 책임추적성 (Accountability) — [감사](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) [로그](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/), [감사](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/) 기록, 사용자 행동 추적
8. [개인정보보호](/knowledge-base/studynote/09_security/01_intro_principles/008_security_awareness/) 3요소 — [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/008_security_awareness/)·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/008_security_awareness/)·[접근성](/knowledge-base/studynote/09_security/01_intro_principles/008_security_awareness/) ([ISO 27701](/knowledge-base/studynote/09_security/01_intro_principles/008_security_awareness/))
9. 정보보안 6요소 — CIA + [인증성](/knowledge-base/studynote/09_security/01_intro_principles/009_incident_response/) + 부인방지 + 책임추적성
[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). [최소 권한 원칙](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/) (Principle of [Least Privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/)) — 필요 알 권리
[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [직무 분리 원칙](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/) ([Separation of Duties](/knowledge-base/studynote/09_security/01_intro_principles/011_separation_of_duties/)) — 4눈 원칙, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 통제
12. [다단계 인증 원칙](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/) ([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/)) — 심층 방어
13. [알 필요성 원칙](/knowledge-base/studynote/09_security/01_intro_principles/013_need_to_know/) ([Need-to-Know](/knowledge-base/studynote/09_security/01_intro_principles/013_need_to_know/)) — 정보 접근 제한
14. [단순 보안 원칙](/knowledge-base/studynote/09_security/01_intro_principles/014_simplicity/) ([Simplicity](/knowledge-base/studynote/09_security/01_intro_principles/014_simplicity/)) — 불필요한 복잡성 제거
15. [공개 설계 원칙](/knowledge-base/studynote/09_security/01_intro_principles/015_open_design/) ([Open Design](/knowledge-base/studynote/09_security/01_intro_principles/015_open_design/)) — 키 은닉，이비 알고리즘 은닉
16. 실패 안전 원칙 ([Fail-Safe](/knowledge-base/studynote/09_security/01_intro_principles/016_data_privacy/)) — 기본값 거부, 오류 시 [안전 상태](/knowledge-base/studynote/09_security/01_intro_principles/016_data_privacy/)
17. 완전한 중재 원칙 (Complete Mediation) — 모든 접근 경로 검사
18. 경제적 설계 원칙 (Economy of Mechanism) — 최소 구현
19. [완전한 통제 원칙](/knowledge-base/studynote/09_security/01_intro_principles/019_ai_emerging_tech/) (Open Platform for [Security](/knowledge-base/studynote/09_security/01_intro_principles/019_ai_emerging_tech/)) — 분리 [보호](/knowledge-base/studynote/09_security/01_intro_principles/019_ai_emerging_tech/)
20. Least Common Mechanism — 메커니즘 공유 최소화
21. [심리적 사용성 원칙](/knowledge-base/studynote/09_security/01_intro_principles/021_psychological_acceptability_principle/) ([Psychological Acceptability](/knowledge-base/studynote/09_security/01_intro_principles/021_psychological_acceptability_principle/)) — 보안이 [사용성](/knowledge-base/studynote/09_security/01_intro_principles/021_psychological_acceptability_principle/)을 해치면 안 됨
22. 정보보안 [정책](/knowledge-base/studynote/09_security/01_intro_principles/022_information_security_policy/) — 최고 경영진 승인, 문서화된 규칙
23. 정보보안 표준 — [정책](/knowledge-base/studynote/09_security/01_intro_principles/023_information_security_standard_guideline/)실시 위한 구체적 기준
24. 정보보안 지침 — 표준 적용 방법론
25. 정보보안 절차 — 구체적 작업 지침
26. [위험 관리 프로세스](/knowledge-base/studynote/09_security/01_intro_principles/026_risk_management_process/) — [식별](/knowledge-base/studynote/09_security/01_intro_principles/026_risk_management_process/)/분석/평가/대응/모니터링/보고
27. [위험 식별](/knowledge-base/studynote/09_security/01_intro_principles/027_risk_identification/) ([Risk Identification](/knowledge-base/studynote/09_security/01_intro_principles/027_risk_identification/)) — 자산·위협·취약점 목록화
28. [정량적 위험 분석](/knowledge-base/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/) — [ALE](/knowledge-base/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/) = ARO × SLE, [MTBF](/knowledge-base/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/), [MTTF](/knowledge-base/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/), [MTTR](/knowledge-base/studynote/09_security/01_intro_principles/028_quantitative_risk_analysis/)
29. [정성적 위험 분석](/knowledge-base/studynote/09_security/01_intro_principles/029_qualitative_risk_analysis/) — High/Medium/Low 매트릭스
30. SLE (Single Loss Expectancy) — 단일 사고 예상 손실
31. ARO (Annual Rate of Occurrence) — 연간 발생 [확률](/knowledge-base/studynote/09_security/01_intro_principles/031_aro_annual_rate_of_occurrence/)
32. [ALE](/knowledge-base/studynote/09_security/01_intro_principles/032_ale_annual_loss_expectancy/) (Annual Loss Expectancy) — 연간 예상 손실
33. [위험 대응 전략](/knowledge-base/studynote/09_security/01_intro_principles/033_risk_response_strategies/) 4가지 — 회피/전가/완화/수용
34. 위험 회피 ([Risk Avoidance](/knowledge-base/studynote/09_security/01_intro_principles/034_risk_avoidance/)) — 위험 원천 제거
35. [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/035_risk_transfer/) ([Risk Transfer](/knowledge-base/studynote/09_security/01_intro_principles/035_risk_transfer/)) — 보험, 외주, 계약 조항
36. [위험 완화](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/) ([Risk Mitigation](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/)) — 통제조시 도입으로 위험 감소
37. [위험 수용](/knowledge-base/studynote/09_security/01_intro_principles/037_risk_acceptance/) ([Risk Acceptance](/knowledge-base/studynote/09_security/01_intro_principles/037_risk_acceptance/)) —관리층 승인 하에
38. [잔여 위험](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/) ([Residual Risk](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/)) — 통제 후 남은 위험
39. 검출 위험 (Detected [Risk](/knowledge-base/studynote/09_security/01_intro_principles/039_detected_vs_undetected_risk/)) vs 미검출 위험 (Undetected [Risk](/knowledge-base/studynote/09_security/01_intro_principles/039_detected_vs_undetected_risk/))
40. [inherited Risk](/knowledge-base/studynote/09_security/01_intro_principles/040_inherited_risk/) — [상속된 위험](/knowledge-base/studynote/09_security/01_intro_principles/040_inherited_risk/)
41. [보안 아키텍처](/knowledge-base/studynote/09_security/01_intro_principles/041_zachman_framework/) — [Zachman Framework](/knowledge-base/studynote/09_security/01_intro_principles/041_zachman_framework/) (6×6 매트릭스)
42. [SABSA](/knowledge-base/studynote/09_security/01_intro_principles/042_sabsa/) (Sherwood Applied Business [Security Architecture](/knowledge-base/studynote/09_security/01_intro_principles/042_sabsa/)) — 수평×수직 매트릭스
43. [OSA](/knowledge-base/studynote/09_security/01_intro_principles/043_osa/) ([Open Security Architecture](/knowledge-base/studynote/09_security/01_intro_principles/043_osa/)) — [보안 아키텍처](/knowledge-base/studynote/09_security/01_intro_principles/043_osa/) 패턴 [카탈로그](/knowledge-base/studynote/09_security/01_intro_principles/043_osa/)
44. [TOGAF](/knowledge-base/studynote/09_security/01_intro_principles/044_togaf/) ([The Open Group](/knowledge-base/studynote/09_security/01_intro_principles/044_togaf/) [Architecture](/knowledge-base/studynote/09_security/01_intro_principles/044_togaf/) Framework) — 아키텍처 개발 방법론
45. NIST [CSF](/knowledge-base/studynote/09_security/01_intro_principles/045_nist_csf_2_0/) 2.0 — Identify/Protect/Detect/Respond/Recover + Govern
46. [제로 트러스트](/knowledge-base/studynote/09_security/01_intro_principles/046_zero_trust/) ([Zero Trust](/knowledge-base/studynote/09_security/01_intro_principles/046_zero_trust/)) — "Never Trust, Always Verify", [NIST SP 800-207](/knowledge-base/studynote/09_security/01_intro_principles/046_zero_trust/)
47. [ZTA](/knowledge-base/studynote/09_security/01_intro_principles/047_zta/) ([Zero Trust Architecture](/knowledge-base/studynote/09_security/01_intro_principles/047_zta/)) — NIST 4단계 구현 로드맵
48. [SDP](/knowledge-base/studynote/09_security/01_intro_principles/048_sdp/) (Software Defined Perimeter) —적연건 정의 경계
49. [마이크로 세그멘테이션](/knowledge-base/studynote/09_security/01_intro_principles/049_micro_segmentation/) — 워크로드별 격리, 측면 이동 차단
50. East-West 트래픽 통제 — 내부 [세그멘테이션](/knowledge-base/studynote/09_security/01_intro_principles/050_east_west_traffic/)
51. North-South 트래픽 통제 — 경계 방어
52. 보안 통제 3가지 유형 — 관리적/기술적/물리적
53. [예방 통제](/knowledge-base/studynote/09_security/01_intro_principles/053_preventive_controls/) ([Preventive Controls](/knowledge-base/studynote/09_security/01_intro_principles/053_preventive_controls/)) — 사전 차단
54. [탐지 통제](/knowledge-base/studynote/09_security/01_intro_principles/054_detective_controls/) ([Detective Controls](/knowledge-base/studynote/09_security/01_intro_principles/054_detective_controls/)) — 이상 징후 발견
55. [교정 통제](/knowledge-base/studynote/09_security/01_intro_principles/055_corrective_controls/) ([Corrective Controls](/knowledge-base/studynote/09_security/01_intro_principles/055_corrective_controls/)) — 사고 후 [복구](/knowledge-base/studynote/09_security/01_intro_principles/055_corrective_controls/)
56. [억제 통제](/knowledge-base/studynote/09_security/01_intro_principles/056_deterrent_controls/) ([Deterrent Controls](/knowledge-base/studynote/09_security/01_intro_principles/056_deterrent_controls/)) — 위협 행동 [억제](/knowledge-base/studynote/09_security/01_intro_principles/056_deterrent_controls/)
57. 상실 통제 ([Compensating Controls](/knowledge-base/studynote/09_security/01_intro_principles/057_compensating_controls/)) — 기존 통제 우회 조치
58. [내재적 보안](/knowledge-base/studynote/09_security/01_intro_principles/058_security_by_design/) ([Security by Design](/knowledge-base/studynote/09_security/01_intro_principles/058_security_by_design/)) — 설계 단계 보안 고려
59. [사후 보안](/knowledge-base/studynote/09_security/01_intro_principles/059_bolt_on_security/) ([Bolt-on Security](/knowledge-base/studynote/09_security/01_intro_principles/059_bolt_on_security/)) — 완성 후 보안 추가
60. [Privacy by Design](/knowledge-base/studynote/09_security/01_intro_principles/060_privacy_by_design/) 7기본원칙 — 사전 [보호](/knowledge-base/studynote/09_security/01_intro_principles/060_privacy_by_design/), 기본값사밀성 등
61. [Secure by Default](/knowledge-base/studynote/09_security/01_intro_principles/061_secure_by_default/) — 기본적으로 안전한 기본값
62. [Secure Coding](/knowledge-base/studynote/09_security/01_intro_principles/062_secure_coding/) — 안전한 소프트웨어 개발
63. [Threat Modeling](/knowledge-base/studynote/09_security/01_intro_principles/063_threat_modeling/) — [STRIDE](/knowledge-base/studynote/09_security/01_intro_principles/063_threat_modeling/), DREAD, [MITRE ATT&CK](/knowledge-base/studynote/09_security/01_intro_principles/063_threat_modeling/) 맵핑
64. DREAD 모델 — Damage/Reproducibility/Exploitability/Affected Users discoverability
65. [STRIDE](/knowledge-base/studynote/09_security/01_intro_principles/065_stride_model/) 모델 — [Spoofing](/knowledge-base/studynote/09_security/01_intro_principles/065_stride_model/)/Tampering/Repudiation/Information Disclosure/[DoS](/knowledge-base/studynote/09_security/01_intro_principles/065_stride_model/)/Elevation
66. [PASTA](/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/) ([Process](/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/) for Attack Simulation and Threat Analysis) — 7단계 [위협 모델링](/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/)
67. [Attack Surface Analysis](/knowledge-base/studynote/09_security/01_intro_principles/067_attack_surface_analysis/) — 공격 표면 관리

---

## 2. [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/) 기초 — 42개

68. [암호학](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/) ([Cryptography](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/)) — [기밀성](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/)·[무결성](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/)·[인증](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/)·부인방지 제공
69. 고전 암호 — 치환 암호, 전치 암호
70. 개살 암호 ([Caesar Cipher](/knowledge-base/studynote/09_security/02_crypto/070_caesar_cipher/)) — 알파벳 3자리 이동
71. 단일 치환 암호 — 하나의 알파벳을 하나의 문자로 치환
72. [다중 치환 암호](/knowledge-base/studynote/09_security/02_crypto/072_vigenere_cipher/) (Vigenère Cipher) — 키워드 기반 복수 치환
73. [Enigma](/knowledge-base/studynote/09_security/02_crypto/073_enigma/) — 독일 제2차 세계대전 기계식 암호
74. 일다음성밀마본 ([One-Time Pad](/knowledge-base/studynote/09_security/02_crypto/074_one_time_pad/)) — 정보 이론적으로 완벽한 안전성
75. 현대 [암호학](/knowledge-base/studynote/09_security/02_crypto/075_computational_infeasibility/) 기본 가정 — computationally infeasible
76. [대칭키 암호](/knowledge-base/studynote/09_security/02_crypto/076_symmetric_encryption/) ([Symmetric Encryption](/knowledge-base/studynote/09_security/02_crypto/076_symmetric_encryption/)) — 동일한 키로 암호화/복호화
77. [비대칭키 암호](/knowledge-base/studynote/09_security/02_crypto/077_asymmetric_encryption/) ([Asymmetric Encryption](/knowledge-base/studynote/09_security/02_crypto/077_asymmetric_encryption/)) — 공개키/비밀키 쌍
78. 하이브리드 암호 — 대칭+비대칭 결합 (키 교환+[데이터](/knowledge-base/studynote/09_security/02_crypto/078_hybrid_encryption/) 암호화)
79. [블록 암호](/knowledge-base/studynote/09_security/02_crypto/079_block_cipher/) ([Block Cipher](/knowledge-base/studynote/09_security/02_crypto/079_block_cipher/)) — 고정 크기 블록 단위 암호화
80. [스트림 암호](/knowledge-base/studynote/09_security/02_crypto/080_stream_cipher/) ([Stream Cipher](/knowledge-base/studynote/09_security/02_crypto/080_stream_cipher/)) — [비트](/knowledge-base/studynote/09_security/02_crypto/080_stream_cipher/)/[바이트](/knowledge-base/studynote/09_security/02_crypto/080_stream_cipher/) 단위 실시간 암호화
81. [RC4](/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/) — [스트림 암호](/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/), 취약점 발견으로 사용 중단 ([WEP](/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/))
82. Salsa20/ChaCha20 — ARX 기반 [스트림 암호](/knowledge-base/studynote/09_security/02_crypto/082_salsa20_chacha20/), [TLS](/knowledge-base/studynote/09_security/02_crypto/082_salsa20_chacha20/) 1.3
83. [AES](/knowledge-base/studynote/09_security/02_crypto/083_aes_advanced_encryption_standard/) ([Advanced Encryption Standard](/knowledge-base/studynote/09_security/02_crypto/083_aes_advanced_encryption_standard/)) — 128/192/256비트 키
84. [AES](/knowledge-base/studynote/09_security/02_crypto/084_aes_spn_structure/) SPN 구조 — SubBytes/ShiftRows/MixColumns/AddRoundKey
85. [AES](/knowledge-base/studynote/09_security/02_crypto/085_aes_key_schedule/) 키 [스케줄](/knowledge-base/studynote/09_security/02_crypto/085_aes_key_schedule/) — 라운드 키 [생성](/knowledge-base/studynote/09_security/02_crypto/085_aes_key_schedule/)
86. [DES](/knowledge-base/studynote/09_security/02_crypto/086_des_data_encryption_standard/) ([Data Encryption Standard](/knowledge-base/studynote/09_security/02_crypto/086_des_data_encryption_standard/)) — 56비트 키, 취약
87. [3DES](/knowledge-base/studynote/09_security/02_crypto/087_3des/) ([Triple DES](/knowledge-base/studynote/09_security/02_crypto/087_3des/)) — 168비트 (112비트 실효 강도)
88. [블록 암호](/knowledge-base/studynote/09_security/02_crypto/088_block_cipher_modes/) 모드 — ECB/[CBC](/knowledge-base/studynote/09_security/02_crypto/088_block_cipher_modes/)/CFB/OFB/[CTR](/knowledge-base/studynote/09_security/02_crypto/088_block_cipher_modes/)
89. [CBC](/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/) ([Cipher Block Chaining](/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/)) — [초기](/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/)화 벡터([IV](/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/)) 필요, 체인 의존성
90. [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) ([Counter](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/)) — 난수 대신 [카운터](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/), [병렬](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 처리 가능
91. [GCM](/knowledge-base/studynote/09_security/02_crypto/091_gcm_mode/) (Galois/[Counter](/knowledge-base/studynote/09_security/02_crypto/091_gcm_mode/) Mode) — [AEAD](/knowledge-base/studynote/09_security/02_crypto/091_gcm_mode/), [인증](/knowledge-base/studynote/09_security/02_crypto/091_gcm_mode/) 암호화
92. [AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) (Authenticated Encryption with Associated [Data](/knowledge-base/studynote/09_security/02_crypto/092_aead/)) — 암호화+[인증](/knowledge-base/studynote/09_security/02_crypto/092_aead/) 동시
93. [CCA](/knowledge-base/studynote/09_security/02_crypto/093_cca/) ([Chosen Ciphertext Attack](/knowledge-base/studynote/09_security/02_crypto/093_cca/)) — 암호문 공격 [분류](/knowledge-base/studynote/09_security/02_crypto/093_cca/)
94. [CPA](/knowledge-base/studynote/09_security/02_crypto/094_cpa/) (Chosen Plaintext Attack) — 평문 공격 [분류](/knowledge-base/studynote/09_security/02_crypto/094_cpa/)
95. [IND-CPA](/knowledge-base/studynote/09_security/02_crypto/095_ind_cpa/) ([Indistinguishability under CPA](/knowledge-base/studynote/09_security/02_crypto/095_ind_cpa/)) — [암호학](/knowledge-base/studynote/09_security/02_crypto/095_ind_cpa/)적 안전성 정의
96. IND-CCA2 — 강인한 [암호학](/knowledge-base/studynote/09_security/02_crypto/096_ind_cca2/)적 안전성
97. [해시 함수](/knowledge-base/studynote/09_security/02_crypto/097_hash_function/) — 단방향성, 충돌 [저항](/knowledge-base/studynote/09_security/02_crypto/097_hash_function/)성, Preimage [저항](/knowledge-base/studynote/09_security/02_crypto/097_hash_function/)성
98. [MD5](/knowledge-base/studynote/09_security/02_crypto/098_md5/) — 128비트 해시, 충돌 공격 실용화 ([1996](/knowledge-base/studynote/09_security/02_crypto/098_md5/))
99. SHA-1 — 160비트, SHA-1 충돌 발견 (2017, SHAttered)
100. SHA-2 — SHA-224/256/384/512, 현재 표준
101. [SHA-3](/knowledge-base/studynote/09_security/02_crypto/101_sha_3/) ([Keccak](/knowledge-base/studynote/09_security/02_crypto/101_sha_3/)) — sponge construction, NIST 2015
102. BLAKE2/BLAKE3 — 채택성능 해시, [AES](/knowledge-base/studynote/09_security/02_crypto/102_blake2_blake3/) 대체
103. [HMAC](/knowledge-base/studynote/09_security/02_crypto/103_hmac/) (Hash-based [Message Authentication Code](/knowledge-base/studynote/09_security/02_crypto/103_hmac/)) — 키섬입 해시
104. [NMAC](/knowledge-base/studynote/09_security/02_crypto/104_nmac/) ([Nested MAC](/knowledge-base/studynote/09_security/02_crypto/104_nmac/))
105. [CMAC](/knowledge-base/studynote/09_security/02_crypto/105_cmac/) ([Cipher-based MAC](/knowledge-base/studynote/09_security/02_crypto/105_cmac/)) — [블록 암호](/knowledge-base/studynote/09_security/02_crypto/105_cmac/) 기반
106. [GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) ([Galois MAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/)) — GCM의 [인증](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) 부분
107. [rainbow table](/knowledge-base/studynote/09_security/02_crypto/107_rainbow_table/) — 사전 계산 [해시 테이블](/knowledge-base/studynote/09_security/02_crypto/107_rainbow_table/), 역산 공격
108. [salt](/knowledge-base/studynote/09_security/02_crypto/108_salt/) — [해시 충돌](/knowledge-base/studynote/09_security/02_crypto/108_salt/) 방지를 위한 난수 추가
109. [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/) — PBKDF2, bcrypt, scrypt (메모리 하드)

---

## 3. [암호학](/knowledge-base/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/) 심화 / [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) — 52개

110. [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) — 소인수분해 문제 기반, 1977년 Rivest/Shamir/Adleman
111. [RSA](/knowledge-base/studynote/09_security/03_network_security/111_rsa_key_generation/) 키 [생성](/knowledge-base/studynote/09_security/03_network_security/111_rsa_key_generation/) — 두 소수의 곱, 오일러 파이 함수
112. [RSA-OAEP](/knowledge-base/studynote/09_security/03_network_security/112_rsa_oaep/) — 최적 [asymmetric encryption](/knowledge-base/studynote/09_security/03_network_security/112_rsa_oaep/) [padding](/knowledge-base/studynote/09_security/03_network_security/112_rsa_oaep/), CCA2 안전성
113. [RSA-PSS](/knowledge-base/studynote/09_security/03_network_security/113_rsa_pss/) — [확률](/knowledge-base/studynote/09_security/03_network_security/113_rsa_pss/)적 서명 방식, [safe](/knowledge-base/studynote/09_security/03_network_security/113_rsa_pss/) 서명
114. [modulo 연산](/knowledge-base/studynote/09_security/03_network_security/114_modulo_arithmetic/) — [RSA](/knowledge-base/studynote/09_security/03_network_security/114_modulo_arithmetic/) 핵심인 나머지 연산
115. Carmichael 수 — [RSA](/knowledge-base/studynote/09_security/03_network_security/115_carmichael_number/) 안전성 분석 관련
116. [GCD](/knowledge-base/studynote/09_security/03_network_security/116_gcd_rsa/) ([최대공약수](/knowledge-base/studynote/09_security/03_network_security/116_gcd_rsa/)) — [RSA](/knowledge-base/studynote/09_security/03_network_security/116_gcd_rsa/) 키 [생성](/knowledge-base/studynote/09_security/03_network_security/116_gcd_rsa/)에서 사용
117. [확장 유클리드 알고리즘](/knowledge-base/studynote/09_security/03_network_security/117_extended_euclidean_algorithm/) — [모듈](/knowledge-base/studynote/09_security/03_network_security/117_extended_euclidean_algorithm/)로 역수 계산
118. [CRT](/knowledge-base/studynote/09_security/03_network_security/118_crt_rsa/) (Chinese Remainder Theorem) — [RSA](/knowledge-base/studynote/09_security/03_network_security/118_crt_rsa/) 복호화 최적화
119. [ECC](/knowledge-base/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/) ([Elliptic Curve Cryptography](/knowledge-base/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/)) — [타원곡선](/knowledge-base/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/) 이산 [로그](/knowledge-base/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/) 문제
120. [타원곡선](/knowledge-base/studynote/09_security/03_network_security/120_elliptic_curve_equation/) — y^ = x³ + ax + b 꼴의 곡선
121. [ECDLP](/knowledge-base/studynote/09_security/03_network_security/121_ecdlp/) (Elliptic Curve Discrete Log Problem) — [ECC](/knowledge-base/studynote/09_security/03_network_security/121_ecdlp/) 안전성 기반
122. [secp256k1](/knowledge-base/studynote/09_security/03_network_security/122_secp256k1/) — Bitcoin에서 사용되는 곡선
123. [P-256](/knowledge-base/studynote/09_security/03_network_security/123_p_256/) ([secp256r1](/knowledge-base/studynote/09_security/03_network_security/123_p_256/)) — NIST 권장 곡선
124. P-384 / P-521 — NIST 고강도 곡선
125. [ECDSA](/knowledge-base/studynote/09_security/03_network_security/125_ecdsa/) ([Elliptic Curve DSA](/knowledge-base/studynote/09_security/03_network_security/125_ecdsa/)) — [ECC](/knowledge-base/studynote/09_security/03_network_security/125_ecdsa/) 기반 디지털 서명
126. EdDSA / Ed25519 — Edwards 곡선, 결정론적 서명
127. [X25519](/knowledge-base/studynote/09_security/03_network_security/127_x25519/) — ECDH를 Edwards 곡선에서 구현
128. [DH](/knowledge-base/studynote/09_security/03_network_security/128_dh_diffie_hellman/) (Diffie-Hellman) — 이산 [로그](/knowledge-base/studynote/09_security/03_network_security/128_dh_diffie_hellman/) 기반 키 교환
129. [DHE](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/) ([Ephemeral DH](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/)) — 임시 [DH](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/), [전방 비밀성](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/)(PFS) 제공
130. [ECDH](/knowledge-base/studynote/09_security/03_network_security/130_ecdh/) — [ECC](/knowledge-base/studynote/09_security/03_network_security/130_ecdh/) 기반 효율적 키 교환
131. [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) — Ephemeral [ECDH](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/), [TLS](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) 1.3 기본
132. [키교환 프로토콜](/knowledge-base/studynote/09_security/03_network_security/132_key_exchange_protocol_mitm/) — [중간자 공격](/knowledge-base/studynote/09_security/03_network_security/132_key_exchange_protocol_mitm/) 방지를 위한 상호 [인증](/knowledge-base/studynote/09_security/03_network_security/132_key_exchange_protocol_mitm/)
133. [Hybrid Encryption](/knowledge-base/studynote/09_security/03_network_security/133_hybrid_encryption/) — [KEM](/knowledge-base/studynote/09_security/03_network_security/133_hybrid_encryption/)/[DEM](/knowledge-base/studynote/09_security/03_network_security/133_hybrid_encryption/) 분리 구조 (ISO 18033-2)
134. [KEM](/knowledge-base/studynote/09_security/03_network_security/134_kem_key_encapsulation/) ([Key Encapsulation Mechanism](/knowledge-base/studynote/09_security/03_network_security/134_kem_key_encapsulation/)) — 키 포장
135. [DEM](/knowledge-base/studynote/09_security/03_network_security/135_dem_data_encapsulation/) ([Data Encapsulation Mechanism](/knowledge-base/studynote/09_security/03_network_security/135_dem_data_encapsulation/)) — [데이터](/knowledge-base/studynote/09_security/03_network_security/135_dem_data_encapsulation/) 암호화
136. [HKDF](/knowledge-base/studynote/09_security/03_network_security/136_hkdf/) ([HMAC](/knowledge-base/studynote/09_security/03_network_security/136_hkdf/)-based [Key Derivation Function](/knowledge-base/studynote/09_security/03_network_security/136_hkdf/)) — RFC 5869
137. [TLS](/knowledge-base/studynote/09_security/03_network_security/137_tls_1_3_handshake/) 1.3 핸드셰이크 — 1-RTT, 0-RTT, [PSK](/knowledge-base/studynote/09_security/03_network_security/137_tls_1_3_handshake/)
138. [AEAD](/knowledge-base/studynote/09_security/03_network_security/138_tls_1_3_aead/) 요구 — [TLS](/knowledge-base/studynote/09_security/03_network_security/138_tls_1_3_aead/) 1.3은 [AEAD](/knowledge-base/studynote/09_security/03_network_security/138_tls_1_3_aead/) 암호만 허용
139. [전방 비밀성](/knowledge-base/studynote/09_security/03_network_security/139_pfs_perfect_forward_secrecy/) (PFS) — 과거 [세션 키](/knowledge-base/studynote/09_security/03_network_security/139_pfs_perfect_forward_secrecy/) 유출해도 과거 통신 [보호](/knowledge-base/studynote/09_security/03_network_security/139_pfs_perfect_forward_secrecy/)
140. [세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/) — 임시 [세션](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)용단기밀월
141. [마스터 시크릿](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/) — Pre-Master Secret에서 파생
142. [PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/) (Pre-Shared [Key](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/)) — 사전 공유 키
143. [Diffie-Hellman Gruppen](/knowledge-base/studynote/09_security/03_network_security/143_diffie_hellman_gruppen/) — RFC 3526 소수 그룹
144. [키 파생 함수](/knowledge-base/studynote/09_security/03_network_security/144_hkdf_tls_1_3/) — [TLS](/knowledge-base/studynote/09_security/03_network_security/144_hkdf_tls_1_3/) 1.3의 [HKDF](/knowledge-base/studynote/09_security/03_network_security/144_hkdf_tls_1_3/)-Extract/Expand
145. NIST [PQC](/knowledge-base/studynote/09_security/03_network_security/145_nist_pqc_standardization/) 표준화 — 2016년 시작, 2024년 4개 [알고리즘](/knowledge-base/studynote/09_security/03_network_security/145_nist_pqc_standardization/) 선정
146. CRYSTALS-Kyber — 격자 기반 [KEM](/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/), NIST [PQC](/knowledge-base/studynote/09_security/03_network_security/146_crystals_kyber_ml_kem/) 표준
147. [CRYSTALS-Dilithium](/knowledge-base/studynote/09_security/03_network_security/147_crystals_dilithium_ml_dsa/) — 격자 기반 디지털 서명, NIST [PQC](/knowledge-base/studynote/09_security/03_network_security/147_crystals_dilithium_ml_dsa/)
148. FALCON — 격자 기반 서명, 짧은 서명
149. [SPHINCS](/knowledge-base/studynote/09_security/03_network_security/149_sphincs_slh_dsa/)+ — 해시 기반 서명, 양자 내성
150. BIKE / HQC / Classic McEliece — 코드 기반 [PQC](/knowledge-base/studynote/09_security/03_network_security/150_code_based_pqc_bike_hqc/)
151. [양자 컴퓨팅](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/) 위협 — Shor [알고리즘](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/) ([RSA](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/)/[ECC](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/) 깨뜨림), [Grover](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/) ([AES](/knowledge-base/studynote/09_security/03_network_security/151_quantum_computing_threats/) 128->64)
152. "Harvest Now, Decrypt Later" — 양자 위협 대응 [전략](/knowledge-base/studynote/09_security/03_network_security/152_hndl_harvest_now_decrypt_later/)
153. .[crypto agility](/knowledge-base/studynote/09_security/03_network_security/153_crypto_agility/) — [알고리즘](/knowledge-base/studynote/09_security/03_network_security/153_crypto_agility/) 교체 능력, [PQC](/knowledge-base/studynote/09_security/03_network_security/153_crypto_agility/) 이전 준비
154. 키 관리 생명주기 — [생성](/knowledge-base/studynote/09_security/03_network_security/154_key_management_lifecycle/)/분배/저장/사용/순환/폐기
155. [키 폐기](/knowledge-base/studynote/09_security/03_network_security/155_key_destruction_crypto_shredding/) — 안전한 삭제, 키 재료 완전 소멸
156. [키 순환](/knowledge-base/studynote/09_security/03_network_security/156_key_rotation/) — 정기적 키 교체, 유출 시 [복구](/knowledge-base/studynote/09_security/03_network_security/156_key_rotation/)력
157. [HSM](/knowledge-base/studynote/09_security/03_network_security/157_hsm_hardware_security_module/) ([Hardware Security Module](/knowledge-base/studynote/09_security/03_network_security/157_hsm_hardware_security_module/)) — 물리적 키 [보호](/knowledge-base/studynote/09_security/03_network_security/157_hsm_hardware_security_module/)
158. [TPM](/knowledge-base/studynote/09_security/03_network_security/158_tpm_trusted_platform_module/) ([Trusted Platform Module](/knowledge-base/studynote/09_security/03_network_security/158_tpm_trusted_platform_module/)) — 플랫폼 키 저장, 원격 증명
159. [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/)) — 공개키 [인증](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/)서 체계
160. [CA](/knowledge-base/studynote/09_security/03_network_security/160_ca_certification_authority/) ([Certification Authority](/knowledge-base/studynote/09_security/03_network_security/160_ca_certification_authority/)) — [인증](/knowledge-base/studynote/09_security/03_network_security/160_ca_certification_authority/)서 발급/관리
161. [RA](/knowledge-base/studynote/09_security/03_network_security/161_ra_registration_authority/) ([Registration Authority](/knowledge-base/studynote/09_security/03_network_security/161_ra_registration_authority/)) — [인증](/knowledge-base/studynote/09_security/03_network_security/161_ra_registration_authority/) 요청 [검증](/knowledge-base/studynote/09_security/03_network_security/161_ra_registration_authority/)/승인

---

## 4. [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) 심화 / [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) — 49개

162. [CRL](/knowledge-base/studynote/09_security/04_endpoint_security/162_crl_certificate_revocation_list/) ([Certificate Revocation List](/knowledge-base/studynote/09_security/04_endpoint_security/162_crl_certificate_revocation_list/)) — 폐지 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/162_crl_certificate_revocation_list/)서 목록
163. [OCSP](/knowledge-base/studynote/09_security/04_endpoint_security/163_ocsp_online_certificate_status_protocol/) (Online Certificate Status [Protocol](/knowledge-base/studynote/09_security/04_endpoint_security/163_ocsp_online_certificate_status_protocol/)) — 실시간 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/163_ocsp_online_certificate_status_protocol/)서 상태 질의
164. [OCSP](/knowledge-base/studynote/09_security/04_endpoint_security/164_ocsp_stapling/) 스테이플링 — 서버가 [OCSP](/knowledge-base/studynote/09_security/04_endpoint_security/164_ocsp_stapling/) 응답 사전 가져옴
165. [CT](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/) ([Certificate Transparency](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/)) — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/)서 발급 공개 [로그](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/)
166. [CT](/knowledge-base/studynote/09_security/04_endpoint_security/166_ct_log_server/) [로그](/knowledge-base/studynote/09_security/04_endpoint_security/166_ct_log_server/) 서버 — Google/Rustproof 등 다수 운영
167. [SCT](/knowledge-base/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) ([Signed Certificate Timestamp](/knowledge-base/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/)) — [CT](/knowledge-base/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) 증명
168. [CAA](/knowledge-base/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/) ([Certification Authority Authorization](/knowledge-base/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/)) — 허용된 [CA](/knowledge-base/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/) [DNS](/knowledge-base/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/) 레코드
169. PKCS#[10](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/)서 서명 요청 ([CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/)) 형식
170. PKCS#7 / CMS — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/170_pkcs7_cms/)서 envelope 형식
171. PKCS#12 — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/171_pkcs12_pfx/)서+개인키 보관 형식 (.pfx)
172. DER / PEM 인코딩 — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/172_der_pem_encoding/)서 인코딩 형식
173. X.509 v3 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/173_x509_v3_certificate/)서 — Subject/Issuer/[SAN](/knowledge-base/studynote/09_security/04_endpoint_security/173_x509_v3_certificate/)/[Key](/knowledge-base/studynote/09_security/04_endpoint_security/173_x509_v3_certificate/) Usage/NSC
174. [SAN](/knowledge-base/studynote/09_security/04_endpoint_security/174_san_subject_alternative_name/) ([Subject Alternative Name](/knowledge-base/studynote/09_security/04_endpoint_security/174_san_subject_alternative_name/)) — 다중 [도메인](/knowledge-base/studynote/09_security/04_endpoint_security/174_san_subject_alternative_name/) [인증](/knowledge-base/studynote/09_security/04_endpoint_security/174_san_subject_alternative_name/)서
175. [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) — *.example.com
176. [EV](/knowledge-base/studynote/09_security/04_endpoint_security/176_ev_extended_validation_certificate/) ([Extended Validation](/knowledge-base/studynote/09_security/04_endpoint_security/176_ev_extended_validation_certificate/)) [인증](/knowledge-base/studynote/09_security/04_endpoint_security/176_ev_extended_validation_certificate/)서 — 엄격한 [검증](/knowledge-base/studynote/09_security/04_endpoint_security/176_ev_extended_validation_certificate/), 녹색 주소창
177. [DV](/knowledge-base/studynote/09_security/04_endpoint_security/177_dv_domain_validation_certificate/) ([Domain Validation](/knowledge-base/studynote/09_security/04_endpoint_security/177_dv_domain_validation_certificate/)) [인증](/knowledge-base/studynote/09_security/04_endpoint_security/177_dv_domain_validation_certificate/)서 — [도메인](/knowledge-base/studynote/09_security/04_endpoint_security/177_dv_domain_validation_certificate/) [검증](/knowledge-base/studynote/09_security/04_endpoint_security/177_dv_domain_validation_certificate/)만
178. [OV](/knowledge-base/studynote/09_security/04_endpoint_security/178_ov_organization_validation_certificate/) ([Organization Validation](/knowledge-base/studynote/09_security/04_endpoint_security/178_ov_organization_validation_certificate/)) — 조직 [검증](/knowledge-base/studynote/09_security/04_endpoint_security/178_ov_organization_validation_certificate/)
179. Self-signed [인증](/knowledge-base/studynote/09_security/04_endpoint_security/179_self_signed_certificate/)서 — 자체 발급 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/179_self_signed_certificate/)서, 내부용
180. [인증서 체인 검증](/knowledge-base/studynote/09_security/04_endpoint_security/180_certificate_chain_of_trust/) — Root [CA](/knowledge-base/studynote/09_security/04_endpoint_security/180_certificate_chain_of_trust/) -> Intermediate [CA](/knowledge-base/studynote/09_security/04_endpoint_security/180_certificate_chain_of_trust/) -> End Entity
181. 브릿지 [CA](/knowledge-base/studynote/09_security/04_endpoint_security/181_bridge_ca_cross_certification/) ([Bridge CA](/knowledge-base/studynote/09_security/04_endpoint_security/181_bridge_ca_cross_certification/)) — 교차 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/181_bridge_ca_cross_certification/)
182. [인증서 핀닝](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/) —이지 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/)서 목록 하드코딩
183. [HPKP](/knowledge-base/studynote/09_security/04_endpoint_security/183_hpkp_http_public_key_pinning_deprecated/) ([HTTP](/knowledge-base/studynote/09_security/04_endpoint_security/183_hpkp_http_public_key_pinning_deprecated/) Public [Key](/knowledge-base/studynote/09_security/04_endpoint_security/183_hpkp_http_public_key_pinning_deprecated/) Pinning) — deprecated, 동적 핀닝 권장
184. Certificate Patrol / [Security](/knowledge-base/studynote/09_security/04_endpoint_security/184_certificate_patrol_telemetry_firefox_pinning/)/Telemetry — Firefox 브라우저 핀닝
185. 동적 핀닝 — [CT](/knowledge-base/studynote/09_security/04_endpoint_security/185_dynamic_pinning_ct_log_based/) [로그](/knowledge-base/studynote/09_security/04_endpoint_security/185_dynamic_pinning_ct_log_based/) 기반pins
186. [Stapling of OCSP](/knowledge-base/studynote/09_security/04_endpoint_security/186_ocsp_stapling_tls_handshake_optimization/) Response — [TLS](/knowledge-base/studynote/09_security/04_endpoint_security/186_ocsp_stapling_tls_handshake_optimization/) 핸드셰이크 최적화
187. [mTLS](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/) ([Mutual TLS](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/)) — 서버+클라이언트 상호 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/)
188. [Code Signing](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/) — 소프트웨어 원산지 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/)
189. [Authenticode](/knowledge-base/studynote/09_security/04_endpoint_security/189_authenticode_microsoft_code_signing/) — Microsoft [코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/189_authenticode_microsoft_code_signing/)
190. [Apple Developer ID](/knowledge-base/studynote/09_security/04_endpoint_security/190_apple_developer_id_code_signing_notarization/) — macOS/iOS 앱 서명
191. [서명 타임스탬프](/knowledge-base/studynote/09_security/04_endpoint_security/191_signature_timestamping_tsa/) —[TSA](/knowledge-base/studynote/09_security/04_endpoint_security/191_signature_timestamping_tsa/) ([Time Stamping Authority](/knowledge-base/studynote/09_security/04_endpoint_security/191_signature_timestamping_tsa/))
192. [TSA](/knowledge-base/studynote/09_security/04_endpoint_security/192_time_stamping_authority_rfc3161_non_repudiation/) ([Time Stamping Authority](/knowledge-base/studynote/09_security/04_endpoint_security/192_time_stamping_authority_rfc3161_non_repudiation/)) — RFC 3161, 부인방지
193. [CRL Distribution Point](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) — [CRL](/knowledge-base/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) 발급 위치
194. [Authority Information Access](/knowledge-base/studynote/09_security/04_endpoint_security/194_authority_information_access_aia_ocsp/) — [OCSP](/knowledge-base/studynote/09_security/04_endpoint_security/194_authority_information_access_aia_ocsp/) 응답자 위치
195. [CRL Scope](/knowledge-base/studynote/09_security/04_endpoint_security/195_crl_scope_crlnumber_delta/) — 전체/crlNumber 용도
196. [delta CRL](/knowledge-base/studynote/09_security/04_endpoint_security/196_delta_crl_efficiency_improvement/) —증량 [CRL](/knowledge-base/studynote/09_security/04_endpoint_security/196_delta_crl_efficiency_improvement/), 효율성 향상
197. [LDH](/knowledge-base/studynote/09_security/04_endpoint_security/197_ldh_limited_distribution_hypothesis/) ([Limited Distribution Hypothesis](/knowledge-base/studynote/09_security/04_endpoint_security/197_ldh_limited_distribution_hypothesis/)) — [인증](/knowledge-base/studynote/09_security/04_endpoint_security/197_ldh_limited_distribution_hypothesis/)서 배포 모델
198. [Key](/knowledge-base/studynote/09_security/04_endpoint_security/198_key_usage_extension_digital_signature/) Usage 확장 — digitalSignature/keyEncipherment/codeSigning
199. [Extended Key Usage](/knowledge-base/studynote/09_security/04_endpoint_security/199_extended_key_usage_eku_serverauth/) — serverAuth/clientAuth/codeSigning/emailProtection
200. [nameConstraints](/knowledge-base/studynote/09_security/04_endpoint_security/200_name_constraints_ca_issuance_limit/) — CA가 발급 가능한 이름 공간 제한
201. [Basic Constraints](/knowledge-base/studynote/09_security/04_endpoint_security/201_basic_constraints_ca_path_length/) — [CA](/knowledge-base/studynote/09_security/04_endpoint_security/201_basic_constraints_ca_path_length/) 여부, 경로 길이 제한
202. [정책 매핑](/knowledge-base/studynote/09_security/04_endpoint_security/202_policy_mapping/) — 상위 [CA](/knowledge-base/studynote/09_security/04_endpoint_security/202_policy_mapping/) [정책](/knowledge-base/studynote/09_security/04_endpoint_security/202_policy_mapping/)과 하위 [CA](/knowledge-base/studynote/09_security/04_endpoint_security/202_policy_mapping/) [정책 매핑](/knowledge-base/studynote/09_security/04_endpoint_security/202_policy_mapping/)
203. [SPC](/knowledge-base/studynote/09_security/04_endpoint_security/203_spc_signed_public_key_challenge/) (Signed Public [Key](/knowledge-base/studynote/09_security/04_endpoint_security/203_spc_signed_public_key_challenge/) Challenge) — [코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/203_spc_signed_public_key_challenge/) blob
204. [Authenticode Timestamp Protocol](/knowledge-base/studynote/09_security/04_endpoint_security/204_authenticode_timestamp_protocol/) — RFC 3161 호환
205. [Kernel Mode Signing](/knowledge-base/studynote/09_security/04_endpoint_security/205_kernel_mode_signing_dse/) — Windows [커널](/knowledge-base/studynote/09_security/04_endpoint_security/205_kernel_mode_signing_dse/) 드라이버 필수
206. [UEFI Secure Boot](/knowledge-base/studynote/09_security/04_endpoint_security/206_uefi_secure_boot_verification/) — 부팅 과정 [코드 서명](/knowledge-base/studynote/09_security/04_endpoint_security/206_uefi_secure_boot_verification/) [검증](/knowledge-base/studynote/09_security/04_endpoint_security/206_uefi_secure_boot_verification/)
207. [DKIM](/knowledge-base/studynote/09_security/04_endpoint_security/207_dkim_domainkeys_identified_mail_authentication/) ([DomainKeys Identified Mail](/knowledge-base/studynote/09_security/04_endpoint_security/207_dkim_domainkeys_identified_mail_authentication/)) — 이메일 발신자 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/207_dkim_domainkeys_identified_mail_authentication/)
208. [SPF](/knowledge-base/studynote/09_security/04_endpoint_security/208_spf_sender_policy_framework/) ([Sender Policy Framework](/knowledge-base/studynote/09_security/04_endpoint_security/208_spf_sender_policy_framework/)) — 허용된 발신 서버 목록 ([DNS](/knowledge-base/studynote/09_security/04_endpoint_security/208_spf_sender_policy_framework/) TXT)
209. [DMARC](/knowledge-base/studynote/09_security/04_endpoint_security/209_dmarc_email_authentication_policy/) ([Domain](/knowledge-base/studynote/09_security/04_endpoint_security/209_dmarc_email_authentication_policy/)-based Message Auth Reporting) — [SPF](/knowledge-base/studynote/09_security/04_endpoint_security/209_dmarc_email_authentication_policy/)+[DKIM](/knowledge-base/studynote/09_security/04_endpoint_security/209_dmarc_email_authentication_policy/) [정책](/knowledge-base/studynote/09_security/04_endpoint_security/209_dmarc_email_authentication_policy/)
210. [DANE](/knowledge-base/studynote/09_security/04_endpoint_security/210_dane_dns_based_auth_tlsa/) ([DNS](/knowledge-base/studynote/09_security/04_endpoint_security/210_dane_dns_based_auth_tlsa/)-Based Auth of Named Entities) — TLSA 레코드, [인증](/knowledge-base/studynote/09_security/04_endpoint_security/210_dane_dns_based_auth_tlsa/)서 고정

---

## 5. [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) — 55개

211. [네트워크 보안](/knowledge-base/studynote/09_security/05_web_app_security/211_network_security_segmentation_integrity/) 3대 영역 — 경계/[세그멘테이션](/knowledge-base/studynote/09_security/05_web_app_security/211_network_security_segmentation_integrity/)/[무결성](/knowledge-base/studynote/09_security/05_web_app_security/211_network_security_segmentation_integrity/)
212. [방화벽](/knowledge-base/studynote/09_security/05_web_app_security/212_firewall_network_boundary_control/) — 네트워크 경계 접근 제어
213. [패킷 필터링 방화벽](/knowledge-base/studynote/09_security/05_web_app_security/213_packet_filtering_firewall/) — 3-4층 헤더 기반 필터
214. [상태 검사 방화벽](/knowledge-base/studynote/09_security/05_web_app_security/214_stateful_inspection_firewall/) ([Stateful Inspection](/knowledge-base/studynote/09_security/05_web_app_security/214_stateful_inspection_firewall/)) — 연결 상태 추적
215. 애플리케이션 게이트웨이 ([Proxy](/knowledge-base/studynote/09_security/05_web_app_security/215_application_gateway_proxy_firewall/)) — 7층 [프로토콜](/knowledge-base/studynote/09_security/05_web_app_security/215_application_gateway_proxy_firewall/) 검사
216. [NGFW](/knowledge-base/studynote/09_security/05_web_app_security/216_ngfw_next_generation_firewall_dpi/) (Next-Generation [Firewall](/knowledge-base/studynote/09_security/05_web_app_security/216_ngfw_next_generation_firewall_dpi/)) — DPI, 사용자식별, 앱식별
217. [방화벽 토폴로지](/knowledge-base/studynote/09_security/05_web_app_security/217_firewall_topology_screened_subnet_dual_dmz/) — 스크린 서브넷, 이중 [DMZ](/knowledge-base/studynote/09_security/05_web_app_security/217_firewall_topology_screened_subnet_dual_dmz/)
218. [bastion host](/knowledge-base/studynote/09_security/05_web_app_security/218_bastion_host_dmz_security/) — 경계 호스트, 공개 [서비스](/knowledge-base/studynote/09_security/05_web_app_security/218_bastion_host_dmz_security/) 전용
219. [DMZ](/knowledge-base/studynote/09_security/05_web_app_security/219_demilitarized_zone_dmz_public_subnet/) (Demilitarized Zone) — 비 Military Zone, 공개 구간
220. [내부 방화벽](/knowledge-base/studynote/09_security/05_web_app_security/220_internal_firewall_segmentation/) ([Internal Firewall](/knowledge-base/studynote/09_security/05_web_app_security/220_internal_firewall_segmentation/)) — 내부 [세그멘테이션](/knowledge-base/studynote/09_security/05_web_app_security/220_internal_firewall_segmentation/)
221. East-West 트래픽 — 수평 방향 통신, 내부 위협 통제
222. North-South 트래픽 — 경계 통과 통신
223. [네트워크 세그멘테이션](/knowledge-base/studynote/09_security/05_web_app_security/223_network_segmentation_vlan_vrf_isolation/) — [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/223_network_segmentation_vlan_vrf_isolation/), [VRF](/knowledge-base/studynote/09_security/05_web_app_security/223_network_segmentation_vlan_vrf_isolation/), [논리](/knowledge-base/studynote/09_security/05_web_app_security/223_network_segmentation_vlan_vrf_isolation/)적 격리
224. [VLAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) ([Virtual LAN](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/)) — 브로드캐스트 [도메인](/knowledge-base/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 분리
225. [VRF](/knowledge-base/studynote/09_security/05_web_app_security/225_vrf_virtual_routing_and_forwarding_isolation/) (Virtual [Routing](/knowledge-base/studynote/09_security/05_web_app_security/225_vrf_virtual_routing_and_forwarding_isolation/) and Forwarding) — 경로 격리
226. [NAC](/knowledge-base/studynote/09_security/05_web_app_security/226_nac_network_access_control_ieee_802_1x/) ([Network Access Control](/knowledge-base/studynote/09_security/05_web_app_security/226_nac_network_access_control_ieee_802_1x/)) — IEEE 802.[1X](/knowledge-base/studynote/09_security/05_web_app_security/226_nac_network_access_control_ieee_802_1x/), [포트](/knowledge-base/studynote/09_security/05_web_app_security/226_nac_network_access_control_ieee_802_1x/) 기반 접근 제어
227. [EAP](/knowledge-base/studynote/09_security/05_web_app_security/227_eap_extensible_authentication_protocol_802_1x/) ([Extensible Authentication Protocol](/knowledge-base/studynote/09_security/05_web_app_security/227_eap_extensible_authentication_protocol_802_1x/)) — 802.[1X](/knowledge-base/studynote/09_security/05_web_app_security/227_eap_extensible_authentication_protocol_802_1x/) [인증](/knowledge-base/studynote/09_security/05_web_app_security/227_eap_extensible_authentication_protocol_802_1x/) [프로토콜](/knowledge-base/studynote/09_security/05_web_app_security/227_eap_extensible_authentication_protocol_802_1x/)
228. [EAP-MD5](/knowledge-base/studynote/09_security/05_web_app_security/228_eap_md5_vulnerable_authentication/) — 취약, 권장되지 않음
229. [PEAP](/knowledge-base/studynote/09_security/05_web_app_security/229_peap_protected_eap_tls_tunnel_authentication/) ([Protected EAP](/knowledge-base/studynote/09_security/05_web_app_security/229_peap_protected_eap_tls_tunnel_authentication/)) — TLS수도보호 [EAP](/knowledge-base/studynote/09_security/05_web_app_security/229_peap_protected_eap_tls_tunnel_authentication/)
230. [EAP-TLS](/knowledge-base/studynote/09_security/05_web_app_security/230_eap_tls_mutual_authentication_pki/) — [인증](/knowledge-base/studynote/09_security/05_web_app_security/230_eap_tls_mutual_authentication_pki/)서 기반 상호 [인증](/knowledge-base/studynote/09_security/05_web_app_security/230_eap_tls_mutual_authentication_pki/)
231. [MAC Address Filtering](/knowledge-base/studynote/09_security/05_web_app_security/231_mac_address_filtering_spoofing_vulnerability/) — 허가된 MAC만 허용
232. [IDS](/knowledge-base/studynote/09_security/05_web_app_security/232_ids_intrusion_detection_system_misuse_anomaly/) ([Intrusion Detection System](/knowledge-base/studynote/09_security/05_web_app_security/232_ids_intrusion_detection_system_misuse_anomaly/)) — 오용 탐지/[이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/232_ids_intrusion_detection_system_misuse_anomaly/)
233. [IDS](/knowledge-base/studynote/09_security/05_web_app_security/233_ids_deployment_architecture_in_band_out_of_band/) 배치 — in-band ([IDS](/knowledge-base/studynote/09_security/05_web_app_security/233_ids_deployment_architecture_in_band_out_of_band/)) vs out-of-band (tap/mirror)
234. [IPS](/knowledge-base/studynote/09_security/05_web_app_security/234_ips_intrusion_prevention_system_inline_fail_open/) (Intrusion Prevention System) — 인라인 배치, 자동 차단
235. [Signature-based detection](/knowledge-base/studynote/09_security/05_web_app_security/235_signature_based_detection_misuse_known_attacks/) —이지 공격 패턴 매칭
236. [Anomaly-based detection](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) —정상 프로파일과 비교
237. HIDS/HIPS — 호스트 기반 [IDS](/knowledge-base/studynote/09_security/05_web_app_security/237_hids_hips_host_based_intrusion_detection/)/[IPS](/knowledge-base/studynote/09_security/05_web_app_security/237_hids_hips_host_based_intrusion_detection/)
238. [NIDS](/knowledge-base/studynote/09_security/05_web_app_security/238_nids_nips_network_based_intrusion_detection_prevention/)/NIPS — 네트워크 기반 [IDS](/knowledge-base/studynote/09_security/05_web_app_security/238_nids_nips_network_based_intrusion_detection_prevention/)/[IPS](/knowledge-base/studynote/09_security/05_web_app_security/238_nids_nips_network_based_intrusion_detection_prevention/)
239. [Snort](/knowledge-base/studynote/09_security/05_web_app_security/239_snort_open_source_nids_rule_syntax/) — [오픈소스](/knowledge-base/studynote/09_security/05_web_app_security/239_snort_open_source_nids_rule_syntax/) [NIDS](/knowledge-base/studynote/09_security/05_web_app_security/239_snort_open_source_nids_rule_syntax/)
240. [Suricata](/knowledge-base/studynote/09_security/05_web_app_security/240_suricata_multithreaded_nids_ids_ips_engine/) — 멀티스레드 [NIDS](/knowledge-base/studynote/09_security/05_web_app_security/240_suricata_multithreaded_nids_ids_ips_engine/)
241. [Zeek](/knowledge-base/studynote/09_security/05_web_app_security/241_zeek_bro_network_traffic_metadata_analysis/) (formerly Bro) — 네트워크 트래픽 분석
242. [WAF](/knowledge-base/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/) ([Web Application Firewall](/knowledge-base/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/)) — [HTTP](/knowledge-base/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/)/[HTTPS](/knowledge-base/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/) [보호](/knowledge-base/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/)
243. OWASP Core Rule Set — [WAF](/knowledge-base/studynote/09_security/05_web_app_security/243_owasp_core_rule_set_crs_waf_anomaly_scoring/) 규칙 세트
244. [Virtual Patching](/knowledge-base/studynote/09_security/05_web_app_security/244_virtual_patching_waf/) — 실제 패치 전 WAF로 취약점 우회
245. [ModSecurity](/knowledge-base/studynote/09_security/05_web_app_security/245_modsecurity_open_source_waf/) — [오픈소스](/knowledge-base/studynote/09_security/05_web_app_security/245_modsecurity_open_source_waf/) [WAF](/knowledge-base/studynote/09_security/05_web_app_security/245_modsecurity_open_source_waf/) 엔진
246. [API Gateway](/knowledge-base/studynote/09_security/05_web_app_security/246_api_gateway_security/) — [API](/knowledge-base/studynote/09_security/05_web_app_security/246_api_gateway_security/) 접근 제어,_RATE limiting, [인증](/knowledge-base/studynote/09_security/05_web_app_security/246_api_gateway_security/)
247. [API Gateway](/knowledge-base/studynote/09_security/05_web_app_security/247_api_gateway_functions/) 기능 — [인증](/knowledge-base/studynote/09_security/05_web_app_security/247_api_gateway_functions/)/[인가](/knowledge-base/studynote/09_security/05_web_app_security/247_api_gateway_functions/)/[캐싱](/knowledge-base/studynote/09_security/05_web_app_security/247_api_gateway_functions/)/로깅/변환
248. DDoS 공격 — 고의적 [서비스](/knowledge-base/studynote/09_security/03_network_security/248_ddos_attack/) 중단 공격
249. DDoS 3유형 — 볼류메트릭/[프로토콜](/knowledge-base/studynote/09_security/03_network_security/249_ddos_three_types/)/애플리케이션 계층
250. DDoS 방어 기법 — [Rate Limiting](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/), Anycast, [Scrubbing Center](/knowledge-base/studynote/09_security/03_network_security/250_scrubbing_center/)
251. [BGP Blackhole](/knowledge-base/studynote/09_security/03_network_security/251_bgp_blackhole/) — DDoS 트래픽 경로흑동
252. [DNS Amplification](/knowledge-base/studynote/09_security/03_network_security/252_dns_amplification/) — [DNS](/knowledge-base/studynote/09_security/03_network_security/252_dns_amplification/) [쿼리](/knowledge-base/studynote/09_security/03_network_security/252_dns_amplification/) 증폭 공격
253. [NTP Amplification](/knowledge-base/studynote/09_security/03_network_security/253_ntp_amplification/) — [NTP](/knowledge-base/studynote/09_security/03_network_security/253_ntp_amplification/) 모노리스트 상태 [쿼리](/knowledge-base/studynote/09_security/03_network_security/253_ntp_amplification/) 증폭
254. [memcached Amplification](/knowledge-base/studynote/09_security/03_network_security/254_memcached_amplification/) — [UDP](/knowledge-base/studynote/09_security/03_network_security/254_memcached_amplification/) [포트](/knowledge-base/studynote/09_security/03_network_security/254_memcached_amplification/) 11211 활용
255. [SYN Flood](/knowledge-base/studynote/09_security/03_network_security/255_syn_flood/) — [TCP](/knowledge-base/studynote/09_security/03_network_security/255_syn_flood/) 반개 연결 점유
256. [UDP Flood](/knowledge-base/studynote/09_security/03_network_security/256_udp_flood/) — 비효율적 [프로토콜](/knowledge-base/studynote/09_security/03_network_security/256_udp_flood/)람용
257. [HTTP Flood](/knowledge-base/studynote/09_security/03_network_security/257_http_flood/) — application layer DDoS
258. [Slowloris](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/) — [HTTP](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/) 헤더 미완성 전송으로 연결 점유
259. [IP Spoofing](/knowledge-base/studynote/09_security/03_network_security/259_ip_spoofing/) — 출발지 IP 위조, BCP38 필수
260. [uRPF](/knowledge-base/studynote/09_security/03_network_security/260_urpf_unicast_rpf/) (Unicast Reverse Path Forwarding) — [Spoofing](/knowledge-base/studynote/09_security/03_network_security/260_urpf_unicast_rpf/) 방지
261. [ARP Spoofing](/knowledge-base/studynote/09_security/03_network_security/261_arp_spoofing/) — [MAC](/knowledge-base/studynote/09_security/03_network_security/261_arp_spoofing/) 주소 위조, 스위칭 환경에서도 가능
262. [Gratuitous ARP](/knowledge-base/studynote/09_security/03_network_security/262_gratuitous_arp/) — 정상 [ARP](/knowledge-base/studynote/09_security/03_network_security/262_gratuitous_arp/) 응답 위조, MiTM 사전 준비
263. [DHCP Spoofing](/knowledge-base/studynote/09_security/03_network_security/263_dhcp_spoofing/) — [DHCP](/knowledge-base/studynote/09_security/03_network_security/263_dhcp_spoofing/) 서버 역할 사칭
264. [DNS Spoofing](/knowledge-base/studynote/09_security/03_network_security/264_dns_spoofing/) — [DNS](/knowledge-base/studynote/09_security/03_network_security/264_dns_spoofing/) 응답 캐시 오염
265. [DNS Cache Poisoning](/knowledge-base/studynote/09_security/03_network_security/265_dns_cache_poisoning/) — Kaminsky 공격, [검증](/knowledge-base/studynote/09_security/03_network_security/265_dns_cache_poisoning/) 없는 응답

---

## 6. [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 심화 — 55개

266. MITM (Man-in-the-Middle) 공격 — 통신 경로 가로채기
267. [SSL Stripping](/knowledge-base/studynote/09_security/05_web_app_security/267_ssl_stripping/) — [HTTPS](/knowledge-base/studynote/09_security/05_web_app_security/267_ssl_stripping/)->[HTTP](/knowledge-base/studynote/09_security/05_web_app_security/267_ssl_stripping/) 강제 다운그레이드
268. [HSTS](/knowledge-base/studynote/09_security/03_network_security/268_hsts/) ([HTTP](/knowledge-base/studynote/09_security/03_network_security/268_hsts/) Strict Transport [Security](/knowledge-base/studynote/09_security/03_network_security/268_hsts/)) — [HTTPS](/knowledge-base/studynote/09_security/03_network_security/268_hsts/) 강제 사용
269. [HTTP](/knowledge-base/studynote/09_security/03_network_security/269_hpkp_deprecated/) Public [Key](/knowledge-base/studynote/09_security/03_network_security/269_hpkp_deprecated/) Pinning — deprecated (2018)
270. [Cookie Hijacking](/knowledge-base/studynote/09_security/05_web_app_security/270_cookie_hijacking/) — [세션](/knowledge-base/studynote/09_security/05_web_app_security/270_cookie_hijacking/) [쿠키](/knowledge-base/studynote/09_security/05_web_app_security/270_cookie_hijacking/) 탈취
271. [세션 하이재킹](/knowledge-base/studynote/09_security/03_network_security/271_session_hijacking/) — [TCP](/knowledge-base/studynote/09_security/03_network_security/271_session_hijacking/) 시퀀스 넘버 예측
272. [패킷 스니핑](/knowledge-base/studynote/09_security/03_network_security/272_packet_sniffing/) — 프로미스큐어스 모드 네트워크 인터페이스
273. [세션 고정 공격](/knowledge-base/studynote/09_security/03_network_security/273_session_fixation/) ([Session Fixation](/knowledge-base/studynote/09_security/03_network_security/273_session_fixation/)) — 공격자 [세션](/knowledge-base/studynote/09_security/03_network_security/273_session_fixation/) ID 강제 [설정](/knowledge-base/studynote/09_security/03_network_security/273_session_fixation/)
274. [Replay Attack](/knowledge-base/studynote/09_security/03_network_security/274_replay_attack/) — 통신 [도청](/knowledge-base/studynote/09_security/03_network_security/274_replay_attack/) 후 재전송
275. [IPsec](/knowledge-base/studynote/09_security/03_network_security/275_ipsec/) — 네트워크층 투명한 보안
276. [IPsec](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/) 두 가지 [프로토콜](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/) — [AH](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/) ([인증](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/)만)/[ESP](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/) (암호화+[인증](/knowledge-base/studynote/09_security/03_network_security/276_ipsec_ah_esp/))
277. [IPsec](/knowledge-base/studynote/09_security/03_network_security/277_ipsec_modes/) 모드 — Transport 모드/Tunnel 모드
278. [IKE](/knowledge-base/studynote/09_security/03_network_security/278_ike_internet_key_exchange/) ([Internet Key Exchange](/knowledge-base/studynote/09_security/03_network_security/278_ike_internet_key_exchange/)) — 키 교환 [프로토콜](/knowledge-base/studynote/09_security/03_network_security/278_ike_internet_key_exchange/)
279. [IKEv1](/knowledge-base/studynote/09_security/03_network_security/279_ikev1/) Phase 1/2 — Main Mode/Aggressive Mode
280. [IKEv2](/knowledge-base/studynote/09_security/03_network_security/280_ikev2/) — MOBIKE 지원, [NAT-T](/knowledge-base/studynote/09_security/03_network_security/280_ikev2/) 자동 처리
281. [NAT-T](/knowledge-base/studynote/09_security/03_network_security/281_nat_traversal/) ([NAT Traversal](/knowledge-base/studynote/09_security/03_network_security/281_nat_traversal/)) — [IPsec](/knowledge-base/studynote/09_security/03_network_security/281_nat_traversal/) [VPN](/knowledge-base/studynote/09_security/03_network_security/281_nat_traversal/) [NAT](/knowledge-base/studynote/09_security/03_network_security/281_nat_traversal/) 통과
282. [L2TP](/knowledge-base/studynote/09_security/03_network_security/282_l2tp_ipsec/)/[IPsec](/knowledge-base/studynote/09_security/03_network_security/282_l2tp_ipsec/) — [L2TP](/knowledge-base/studynote/09_security/03_network_security/282_l2tp_ipsec/) 터널 + [IPsec](/knowledge-base/studynote/09_security/03_network_security/282_l2tp_ipsec/) 암호화
283. [SSL VPN](/knowledge-base/studynote/09_security/03_network_security/283_ssl_vpn/) — 브라우저 기반/클라이언트 설치형
284. [OpenVPN](/knowledge-base/studynote/09_security/03_network_security/284_openvpn/) — [오픈소스](/knowledge-base/studynote/09_security/03_network_security/284_openvpn/) [SSL VPN](/knowledge-base/studynote/09_security/03_network_security/284_openvpn/)
285. [WireGuard](/knowledge-base/studynote/09_security/03_network_security/285_wireguard/) — modern [VPN](/knowledge-base/studynote/09_security/03_network_security/285_wireguard/), Linux [커널](/knowledge-base/studynote/09_security/03_network_security/285_wireguard/)에 통합
286. [ZeroTier](/knowledge-base/studynote/09_security/03_network_security/286_zerotier/) — [분산](/knowledge-base/studynote/09_security/03_network_security/286_zerotier/) [VPN](/knowledge-base/studynote/09_security/03_network_security/286_zerotier/), [P2P](/knowledge-base/studynote/09_security/03_network_security/286_zerotier/) 터널
287. [Tailscale](/knowledge-base/studynote/09_security/03_network_security/287_tailscale/) — [WireGuard](/knowledge-base/studynote/09_security/03_network_security/287_tailscale/) 기반 관리형 [VPN](/knowledge-base/studynote/09_security/03_network_security/287_tailscale/)
288. [SASE](/knowledge-base/studynote/09_security/03_network_security/288_sase/) (Secure Access [Service](/knowledge-base/studynote/09_security/03_network_security/288_sase/) Edge) — 네트워크+보안 통합
289. [SSE](/knowledge-base/studynote/09_security/03_network_security/289_sse_security_service_edge/) ([Security Service Edge](/knowledge-base/studynote/09_security/03_network_security/289_sse_security_service_edge/)) — SASE의 보안 요소
290. [SD-WAN](/knowledge-base/studynote/09_security/03_network_security/290_sdwan_security/) ([Software-Defined WAN](/knowledge-base/studynote/09_security/03_network_security/290_sdwan_security/)) — WAN [가상화](/knowledge-base/studynote/09_security/03_network_security/290_sdwan_security/)
291. [SD-WAN](/knowledge-base/studynote/09_security/03_network_security/291_sdwan_security_detail/) 보안 — 암호화된 터널, 중앙 집중식 [정책](/knowledge-base/studynote/09_security/03_network_security/291_sdwan_security_detail/)
292. [VPN concentrator](/knowledge-base/studynote/09_security/03_network_security/292_vpn_concentrator/) — 다수 [VPN](/knowledge-base/studynote/09_security/03_network_security/292_vpn_concentrator/) 연결 집약 장치
293. [TLS](/knowledge-base/studynote/09_security/03_network_security/293_tls_ssl_vulnerabilities_history/)/SSL 취약점 역사 — [POODLE](/knowledge-base/studynote/09_security/03_network_security/293_tls_ssl_vulnerabilities_history/)/[BEAST](/knowledge-base/studynote/09_security/03_network_security/293_tls_ssl_vulnerabilities_history/)/[CRIME](/knowledge-base/studynote/09_security/03_network_security/293_tls_ssl_vulnerabilities_history/)/ROGUE
294. [POODLE](/knowledge-base/studynote/09_security/03_network_security/294_poodle/) ([Padding](/knowledge-base/studynote/09_security/03_network_security/294_poodle/) [Oracle](/knowledge-base/studynote/09_security/03_network_security/294_poodle/) On Downgraded Legacy Encryption)
295. [BEAST](/knowledge-base/studynote/09_security/03_network_security/295_beast/) (Browser Exploit Against SSL/[TLS](/knowledge-base/studynote/09_security/03_network_security/295_beast/))
296. [CRIME](/knowledge-base/studynote/09_security/03_network_security/296_crime_attack/) — [TLS](/knowledge-base/studynote/09_security/03_network_security/296_crime_attack/) [압축](/knowledge-base/studynote/09_security/03_network_security/296_crime_attack/) [사이드 채널 공격](/knowledge-base/studynote/09_security/03_network_security/296_crime_attack/)
297. [HEARTBLEED](/knowledge-base/studynote/09_security/03_network_security/297_heartbleed/) — OpenSSL 하트비트 확장 메모리 유출
298. [DROWN](/knowledge-base/studynote/09_security/03_network_security/298_drown_attack/) — SSLv2람용에よる [RSA](/knowledge-base/studynote/09_security/03_network_security/298_drown_attack/) 해독
299. [Logjam](/knowledge-base/studynote/09_security/03_network_security/299_logjam_attack/) — DH_EXPORT 키 강제 사용, 512비트 그룹
300. [FREAK](/knowledge-base/studynote/09_security/03_network_security/300_freak_attack/) — RSA_EXPORT 키 강제 사용
301. [Sweet32](/knowledge-base/studynote/09_security/03_network_security/301_sweet32_attack/) — 64비트 [블록 암호](/knowledge-base/studynote/09_security/03_network_security/301_sweet32_attack/) Birthday 공격
302. [TLS](/knowledge-base/studynote/09_security/03_network_security/302_tls_1_3/) 1.3 — 이전 [버전](/knowledge-base/studynote/09_security/03_network_security/302_tls_1_3/)과의 [호환성](/knowledge-base/studynote/09_security/03_network_security/302_tls_1_3/) 제거, 빠른 핸드셰이크
303. [TLS](/knowledge-base/studynote/09_security/03_network_security/303_tls_1_3_vs_1_2/) 1.3 vs 1.2 차이 — 1-RTT 핸드셰이크, 0-RTT, PFS 의무
304. [TLS](/knowledge-base/studynote/09_security/03_network_security/304_tls_cipher_suite/) 밀마투건 — TLS_AES_256_GCM_SHA384 등
305. cipher suite명명규칙 — TLS_kex_AUTH
306. Perfect [Forward](/knowledge-base/studynote/09_security/03_network_security/306_pfs_detail/) Secrecy — 각 [세션](/knowledge-base/studynote/09_security/03_network_security/306_pfs_detail/)독립적밀월
307. [SSH](/knowledge-base/studynote/09_security/03_network_security/307_ssh/) ([Secure Shell](/knowledge-base/studynote/09_security/03_network_security/307_ssh/)) — 안전한 원격 접속
308. [SSH](/knowledge-base/studynote/09_security/03_network_security/308_ssh_key_auth/) 키 기반 [인증](/knowledge-base/studynote/09_security/03_network_security/308_ssh_key_auth/) — 공개키/개인키 쌍
309. [SSH Agent Forwarding](/knowledge-base/studynote/09_security/03_network_security/309_ssh_agent_forwarding/) — 로컬 에이전트를원정에 전달
310. [SFTP](/knowledge-base/studynote/09_security/03_network_security/310_sftp/) — [SSH](/knowledge-base/studynote/09_security/03_network_security/310_sftp/) 기반 [파일](/knowledge-base/studynote/09_security/03_network_security/310_sftp/) 전송
311. [SCP](/knowledge-base/studynote/09_security/03_network_security/311_scp/) — [SSH](/knowledge-base/studynote/09_security/03_network_security/311_scp/) 기반 [파일](/knowledge-base/studynote/09_security/03_network_security/311_scp/) 복사
312. [SSH Tunnel](/knowledge-base/studynote/09_security/03_network_security/312_ssh_tunnel/)/[Proxy](/knowledge-base/studynote/09_security/03_network_security/312_ssh_tunnel/) — SOCKS [프록시](/knowledge-base/studynote/09_security/03_network_security/312_ssh_tunnel/)
313. [Known Hosts](/knowledge-base/studynote/09_security/03_network_security/313_known_hosts/) — 서버 공개키 최초 수락/저장
314. [SSH](/knowledge-base/studynote/09_security/03_network_security/314_ssh_hardening/) 옵션 강화 — PasswordAuthentication no, PubkeyAuthentication yes
315. [LDAP](/knowledge-base/studynote/09_security/03_network_security/315_ldap/) — [디렉터리](/knowledge-base/studynote/09_security/03_network_security/315_ldap/) [서비스](/knowledge-base/studynote/09_security/03_network_security/315_ldap/) 접근 [프로토콜](/knowledge-base/studynote/09_security/03_network_security/315_ldap/)
316. [LDAPS](/knowledge-base/studynote/09_security/03_network_security/316_ldaps/) ([LDAP over SSL](/knowledge-base/studynote/09_security/03_network_security/316_ldaps/)) — [포트](/knowledge-base/studynote/09_security/03_network_security/316_ldaps/) 636, [LDAP](/knowledge-base/studynote/09_security/03_network_security/316_ldaps/) 암호화
317. [LDAP](/knowledge-base/studynote/09_security/03_network_security/317_ldap_injection/) [인젝션](/knowledge-base/studynote/09_security/03_network_security/317_ldap_injection/) — 특수 문자주입으로 [인증](/knowledge-base/studynote/09_security/03_network_security/317_ldap_injection/) 우회
318. [ARP](/knowledge-base/studynote/09_security/03_network_security/318_arp_cache_poisoning/) 캐시poisoning —정태 [ARP](/knowledge-base/studynote/09_security/03_network_security/318_arp_cache_poisoning/) [설정](/knowledge-base/studynote/09_security/03_network_security/318_arp_cache_poisoning/)으로 MiTM
319. [VLAN Hopping](/knowledge-base/studynote/09_security/03_network_security/319_vlan_hopping/) — [Switch](/knowledge-base/studynote/09_security/03_network_security/319_vlan_hopping/) [Spoofing](/knowledge-base/studynote/09_security/03_network_security/319_vlan_hopping/)/Double Tagging
320. [Bridge](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/) [Protocol](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/) [Data](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/) Unit ([BPDU](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/)) — [스위치](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/) [프로토콜](/knowledge-base/studynote/09_security/03_network_security/320_bpdu/)

---

## 7. 시스템 보안 / 엔드포인트 — 55개

321. [엔드포인트 보안](/knowledge-base/studynote/09_security/04_endpoint_security/321_endpoint_security/) — 단말기에 대한 보안조시
322. [EPP](/knowledge-base/studynote/09_security/04_endpoint_security/322_epp/) ([Endpoint Protection Platform](/knowledge-base/studynote/09_security/04_endpoint_security/322_epp/)) — 통합 엔드포인트 [보호](/knowledge-base/studynote/09_security/04_endpoint_security/322_epp/)
323. [AV](/knowledge-base/studynote/09_security/04_endpoint_security/323_antivirus/) ([Anti-Virus](/knowledge-base/studynote/09_security/04_endpoint_security/323_antivirus/)) — 시그니처 기반 악성코드 탐지
324. [행위 기반 탐지](/knowledge-base/studynote/09_security/04_endpoint_security/324_behavior_based_detection/) — 시그니처 없이 의심 행동 감지
325. [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/) (Endpoint [Detection](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/) and Response) — 실시간 모니터링+응답
326. [XDR](/knowledge-base/studynote/09_security/04_endpoint_security/326_xdr/) (Extended [Detection](/knowledge-base/studynote/09_security/04_endpoint_security/326_xdr/) and Response) — 멀티 플랫폼 [상관 분석](/knowledge-base/studynote/09_security/04_endpoint_security/326_xdr/)
327. [MDR](/knowledge-base/studynote/09_security/04_endpoint_security/327_mdr/) (Managed [Detection](/knowledge-base/studynote/09_security/04_endpoint_security/327_mdr/) and Response) — 관리형 탐지/응답
328. [엔드포인트 보호 조합](/knowledge-base/studynote/09_security/04_endpoint_security/328_endpoint_protection_combo/) — [AV](/knowledge-base/studynote/09_security/04_endpoint_security/328_endpoint_protection_combo/)+[EDR](/knowledge-base/studynote/09_security/04_endpoint_security/328_endpoint_protection_combo/)+NDR+[UEBA](/knowledge-base/studynote/09_security/04_endpoint_security/328_endpoint_protection_combo/)
329. [TTP](/knowledge-base/studynote/09_security/04_endpoint_security/329_ttp/) (Tactics, Techniques, Procedures) — 공격자 행동 패턴
330. [버퍼 오버플로우](/knowledge-base/studynote/09_security/04_endpoint_security/330_buffer_overflow/) ([Buffer Overflow](/knowledge-base/studynote/09_security/04_endpoint_security/330_buffer_overflow/)) — 메모리 경계 초과
331. [스택 버퍼 오버플로우](/knowledge-base/studynote/09_security/04_endpoint_security/331_stack_buffer_overflow/) — 함수 복귀 주소 덮어쓰기
332. [힙 버퍼 오버플로우](/knowledge-base/studynote/09_security/04_endpoint_security/332_heap_buffer_overflow/) — 힙 메모리 오염
333. [정수 오버플로우](/knowledge-base/studynote/09_security/04_endpoint_security/333_integer_overflow/) ([Integer Overflow](/knowledge-base/studynote/09_security/04_endpoint_security/333_integer_overflow/)) — 정수 범위 초과
334. [Format String Bug](/knowledge-base/studynote/09_security/04_endpoint_security/334_format_string_bug/) — %x, %s 등 포맷 지시어 악용
335. [NX bit](/knowledge-base/studynote/09_security/04_endpoint_security/335_nx_bit/) (No-Execute) — 실행 가능 메모리 영역 분리
336. [DEP](/knowledge-base/studynote/09_security/04_endpoint_security/336_dep/) ([Data Execution Prevention](/knowledge-base/studynote/09_security/04_endpoint_security/336_dep/)) — NX를 OS 수준에서 구현
337. [ASLR](/knowledge-base/studynote/09_security/04_endpoint_security/337_aslr/) (Address Space Layout Randomization) — 주소 공간 난수화
338. [PIE](/knowledge-base/studynote/09_security/04_endpoint_security/338_pie/) ([Position Independent Executable](/knowledge-base/studynote/09_security/04_endpoint_security/338_pie/)) — EXE도 [ASLR](/knowledge-base/studynote/09_security/04_endpoint_security/338_pie/)
339. [Stack Canary](/knowledge-base/studynote/09_security/04_endpoint_security/339_stack_canary/) — [스택](/knowledge-base/studynote/09_security/04_endpoint_security/339_stack_canary/) 프레임 손상 탐지 [쿠키](/knowledge-base/studynote/09_security/04_endpoint_security/339_stack_canary/)
340. [SSP](/knowledge-base/studynote/09_security/04_endpoint_security/340_ssp/) ([Stack Smashing Protector](/knowledge-base/studynote/09_security/04_endpoint_security/340_ssp/)) — GCC의 [스택](/knowledge-base/studynote/09_security/04_endpoint_security/340_ssp/) [보호](/knowledge-base/studynote/09_security/04_endpoint_security/340_ssp/)
341. [RELRO](/knowledge-base/studynote/09_security/04_endpoint_security/341_relro/) ([Relocation Read-Only](/knowledge-base/studynote/09_security/04_endpoint_security/341_relro/)) — GOT [쓰기](/knowledge-base/studynote/09_security/04_endpoint_security/341_relro/) [보호](/knowledge-base/studynote/09_security/04_endpoint_security/341_relro/)
342. [Full RELRO](/knowledge-base/studynote/09_security/04_endpoint_security/342_full_relro/) — GOT 전체 읽기 전용
343. [FORTIFY_SOURCE](/knowledge-base/studynote/09_security/04_endpoint_security/343_fortify_source/) — _chk 함수로 버퍼 연산 대체
344. [ROP](/knowledge-base/studynote/09_security/04_endpoint_security/344_rop/) ([Return-Oriented Programming](/knowledge-base/studynote/09_security/04_endpoint_security/344_rop/)) — [가젯](/knowledge-base/studynote/09_security/04_endpoint_security/344_rop/) 체인, [셸코드](/knowledge-base/studynote/09_security/04_endpoint_security/344_rop/) 없이 코드 실행
345. [가젯](/knowledge-base/studynote/09_security/04_endpoint_security/345_gadget_rop/) (Gadget) — Ret 명령으로 끝나는 코드 조각
346. [JOP](/knowledge-base/studynote/09_security/04_endpoint_security/346_jop/) ([Jump-Oriented Programming](/knowledge-base/studynote/09_security/04_endpoint_security/346_jop/)) — 함수 포인터Hijacking
347. [COP](/knowledge-base/studynote/09_security/04_endpoint_security/347_cop/) ([Call-Oriented Programming](/knowledge-base/studynote/09_security/04_endpoint_security/347_cop/)) — 호출 기반 [가젯](/knowledge-base/studynote/09_security/04_endpoint_security/347_cop/) 체인
348. Return-to-libc — libc 함수 직접 호출
349. [Heap Spray](/knowledge-base/studynote/09_security/04_endpoint_security/349_heap_spray/) — 힙 메모리에 [셸코드](/knowledge-base/studynote/09_security/04_endpoint_security/349_heap_spray/) 대량 배치
350. [Heap Feng Shui](/knowledge-base/studynote/09_security/04_endpoint_security/350_heap_feng_shui/) — 힙 레이아웃 조작
351. [Use-After-Free](/knowledge-base/studynote/09_security/04_endpoint_security/351_use_after_free/) — 해제된 메모리 재사용
352. [Double Free](/knowledge-base/studynote/09_security/04_endpoint_security/352_double_free/) — 이중 해제로 힙 손상
353. [Race Condition](/knowledge-base/studynote/09_security/04_endpoint_security/353_race_condition/) — [TOCTOU](/knowledge-base/studynote/09_security/04_endpoint_security/353_race_condition/) (Time-of-Check-Time-of-Use)
354. [Deadlock](/knowledge-base/studynote/09_security/04_endpoint_security/354_deadlock_livelock/) / [Livelock](/knowledge-base/studynote/09_security/04_endpoint_security/354_deadlock_livelock/) — 자원 점유로 인한 교착/기아
355. [Time-of-Check to Time-of-Use](/knowledge-base/studynote/09_security/04_endpoint_security/355_toctou/) — [파일](/knowledge-base/studynote/09_security/04_endpoint_security/355_toctou/) 접근 races
356. [권한 상승](/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/) — [Local Privilege Escalation](/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/) (LPE)
357. [커널](/knowledge-base/studynote/09_security/04_endpoint_security/357_kernel_privilege_escalation/) [privilege escalation](/knowledge-base/studynote/09_security/04_endpoint_security/357_kernel_privilege_escalation/) — Dirty [COW](/knowledge-base/studynote/09_security/04_endpoint_security/357_kernel_privilege_escalation/), EternalBlue
358. [Zero-Day](/knowledge-base/studynote/09_security/04_endpoint_security/358_zero_day/) — 패치되지 않은 취약점 리용
359. [루트킷](/knowledge-base/studynote/09_security/04_endpoint_security/359_rootkit/) ([Rootkit](/knowledge-base/studynote/09_security/04_endpoint_security/359_rootkit/)) — 시스템에잠복하는 악성 코드 모음
360. [커널 루트킷](/knowledge-base/studynote/09_security/04_endpoint_security/360_kernel_rootkit/) — OS [커널](/knowledge-base/studynote/09_security/04_endpoint_security/360_kernel_rootkit/) 레벨 설치
361. 사용자모드 [루트킷](/knowledge-base/studynote/09_security/04_endpoint_security/361_user_mode_rootkit/) — 애플리케이션 레벨
362. [부트킷](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/) ([Bootkit](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/)) — 부팅 과정infecting
363. [MBR Bootkit](/knowledge-base/studynote/09_security/04_endpoint_security/363_mbr_bootkit/) — [Master Boot Record](/knowledge-base/studynote/09_security/04_endpoint_security/363_mbr_bootkit/) 감염
364. [UEFI Bootkit](/knowledge-base/studynote/09_security/04_endpoint_security/364_uefi_bootkit/) — [UEFI](/knowledge-base/studynote/09_security/04_endpoint_security/364_uefi_bootkit/) [펌웨어](/knowledge-base/studynote/09_security/04_endpoint_security/364_uefi_bootkit/) 수준 감염
365. [Secure Boot](/knowledge-base/studynote/09_security/04_endpoint_security/365_secure_boot_bypass/) 우회 — 서명 [검증](/knowledge-base/studynote/09_security/04_endpoint_security/365_secure_boot_bypass/) 무력화
366. [Firmware Rootkit](/knowledge-base/studynote/09_security/04_endpoint_security/366_firmware_rootkit/) — BIOS/[펌웨어](/knowledge-base/studynote/09_security/04_endpoint_security/366_firmware_rootkit/) 숨겨진 [백도어](/knowledge-base/studynote/09_security/04_endpoint_security/366_firmware_rootkit/)
367. [키로거](/knowledge-base/studynote/09_security/04_endpoint_security/367_keylogger/) ([Keylogger](/knowledge-base/studynote/09_security/04_endpoint_security/367_keylogger/)) — 키입력 기록
368. [백도어](/knowledge-base/studynote/09_security/04_endpoint_security/368_backdoor/) ([Backdoor](/knowledge-base/studynote/09_security/04_endpoint_security/368_backdoor/)) — 정상 [인증](/knowledge-base/studynote/09_security/04_endpoint_security/368_backdoor/) 우회
369. [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)작탄 ([Logic Bomb](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)) — 특정 조건 충족 시 발동
370. [트로이목마](/knowledge-base/studynote/09_security/04_endpoint_security/370_trojan_horse/) ([Trojan Horse](/knowledge-base/studynote/09_security/04_endpoint_security/370_trojan_horse/)) — 겉보기에 정상인 악성코드
371. [랜섬웨어](/knowledge-base/studynote/09_security/04_endpoint_security/371_ransomware/) ([Ransomware](/knowledge-base/studynote/09_security/04_endpoint_security/371_ransomware/)) — [파일](/knowledge-base/studynote/09_security/04_endpoint_security/371_ransomware/) 암호화 후 몸값
372. [CryptoLocker](/knowledge-base/studynote/09_security/04_endpoint_security/372_ransomware_variants/) / [WannaCry](/knowledge-base/studynote/09_security/04_endpoint_security/372_ransomware_variants/) / [Ryuk](/knowledge-base/studynote/09_security/04_endpoint_security/372_ransomware_variants/) — 주요 [랜섬웨어](/knowledge-base/studynote/09_security/04_endpoint_security/372_ransomware_variants/) 변종
373. [Wiper](/knowledge-base/studynote/09_security/04_endpoint_security/373_wiper_malware/) — [데이터](/knowledge-base/studynote/09_security/04_endpoint_security/373_wiper_malware/) 파괴 목적인 malware
374. [지능형 지속 위협](/knowledge-base/studynote/09_security/04_endpoint_security/374_apt/) ([APT](/knowledge-base/studynote/09_security/04_endpoint_security/374_apt/)) — 국가 수준 위협 행위자
375. [Fileless Malware](/knowledge-base/studynote/09_security/04_endpoint_security/375_fileless_malware/) — 메모리 내에서만 실행, [파일](/knowledge-base/studynote/09_security/04_endpoint_security/375_fileless_malware/) 없는 공격

---

## 8. 시스템 보안 심화 — 40개

376. [커널 취약점](/knowledge-base/studynote/09_security/04_endpoint_security/376_kernel_vulnerability/) — 시스템 콜 인터페이스 악용
377. [Spectre](/knowledge-base/studynote/09_security/04_endpoint_security/377_spectre_meltdown/)/[Meltdown](/knowledge-base/studynote/09_security/04_endpoint_security/377_spectre_meltdown/) — CPU 취약점 (추측집행 악용)
378. [Spectre](/knowledge-base/studynote/09_security/04_endpoint_security/378_spectre_variants/) v1/v2 — Bounds Check Bypass/[Branch Target Injection](/knowledge-base/studynote/09_security/04_endpoint_security/378_spectre_variants/)
379. [Meltdown](/knowledge-base/studynote/09_security/04_endpoint_security/379_meltdown/) — Rogue [Data](/knowledge-base/studynote/09_security/04_endpoint_security/379_meltdown/) Cache Load
380. [MDS](/knowledge-base/studynote/09_security/04_endpoint_security/380_mds_attack/) ([Microarchitectural Data Sampling](/knowledge-base/studynote/09_security/04_endpoint_security/380_mds_attack/)) — CPU 내부 [데이터](/knowledge-base/studynote/09_security/04_endpoint_security/380_mds_attack/) 샘플링
381. [ZombieLoad](/knowledge-base/studynote/09_security/04_endpoint_security/381_zombieload_ridl/) / [RIDL](/knowledge-base/studynote/09_security/04_endpoint_security/381_zombieload_ridl/) — Load치적[리스크](/knowledge-base/studynote/09_security/04_endpoint_security/381_zombieload_ridl/)
382. [SWAPGS](/knowledge-base/studynote/09_security/04_endpoint_security/382_swapgs/) — [GPU](/knowledge-base/studynote/09_security/04_endpoint_security/382_swapgs/) 취약점 악용
383. CPU 취약점완화 — 마이크로코드 업데이트, OS 패치
384. [펌웨어](/knowledge-base/studynote/09_security/04_endpoint_security/384_firmware_security_uefi/) 보안 — [UEFI Secure Boot](/knowledge-base/studynote/09_security/04_endpoint_security/384_firmware_security_uefi/)
385. [Measured Boot](/knowledge-base/studynote/09_security/04_endpoint_security/385_measured_boot/) — TPM리용, boot 측정값 기록
386. [Static PCR](/knowledge-base/studynote/09_security/04_endpoint_security/386_static_pcr/) — 부팅 과정 [무결성](/knowledge-base/studynote/09_security/04_endpoint_security/386_static_pcr/) 측정
387. [Dynamic PCR](/knowledge-base/studynote/09_security/04_endpoint_security/387_dynamic_pcr/) — late launch으로 동적 측정
388. [Intel TXT](/knowledge-base/studynote/09_security/04_endpoint_security/388_intel_txt/) ([Trusted Execution Technology](/knowledge-base/studynote/09_security/04_endpoint_security/388_intel_txt/)) — late launch
389. [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) ([Software Guard Extensions](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)) — [enclave](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) [메모리 보호](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)
390. [enclave](/knowledge-base/studynote/09_security/04_endpoint_security/390_enclave/) — SGX의가밀 메모리 영역
391. [AMD SEV](/knowledge-base/studynote/09_security/04_endpoint_security/391_amd_sev/) ([Secure Encrypted Virtualization](/knowledge-base/studynote/09_security/04_endpoint_security/391_amd_sev/)) — [VM](/knowledge-base/studynote/09_security/04_endpoint_security/391_amd_sev/) 암호화
392. SEV-ES — [VM](/knowledge-base/studynote/09_security/04_endpoint_security/392_sev_es/) [레지스터](/knowledge-base/studynote/09_security/04_endpoint_security/392_sev_es/) [state](/knowledge-base/studynote/09_security/04_endpoint_security/392_sev_es/) 암호화
393. [Memory Encryption 엔진](/knowledge-base/studynote/09_security/04_endpoint_security/393_memory_encryption_engine/) — 하드웨어 [메모리 암호화](/knowledge-base/studynote/09_security/04_endpoint_security/393_memory_encryption_engine/)
394. [TPM](/knowledge-base/studynote/09_security/04_endpoint_security/394_tpm_2_0/) 2.0 — 키 저장, 플랫폼 증명
395. [TPM](/knowledge-base/studynote/09_security/04_endpoint_security/395_tpm_functions_pcr_ek_nv_attestation/) 기능 — PCR, EK, NV [Index](/knowledge-base/studynote/09_security/04_endpoint_security/395_tpm_functions_pcr_ek_nv_attestation/), Attestation
396. [remote attestation](/knowledge-base/studynote/09_security/04_endpoint_security/396_remote_attestation/) — [원격 플랫폼 증명](/knowledge-base/studynote/09_security/04_endpoint_security/396_remote_attestation/)
397. [BitLocker](/knowledge-base/studynote/09_security/04_endpoint_security/397_bitlocker_windows_fde/) — Windows FDE, [TPM](/knowledge-base/studynote/09_security/04_endpoint_security/397_bitlocker_windows_fde/)+N PIN/[USB](/knowledge-base/studynote/09_security/04_endpoint_security/397_bitlocker_windows_fde/) 사용
398. [FileVault](/knowledge-base/studynote/09_security/04_endpoint_security/398_filevault_macos_fde/) — macOS FDE
399. [LUKS](/knowledge-base/studynote/09_security/04_endpoint_security/399_luks_linux_unified_key_setup/) — Linux Unified [Key](/knowledge-base/studynote/09_security/04_endpoint_security/399_luks_linux_unified_key_setup/) Setup, 디스크 암호화
400. [VeraCrypt](/knowledge-base/studynote/09_security/04_endpoint_security/400_veracrypt_cross_platform_disk_encryption/) — [오픈소스](/knowledge-base/studynote/09_security/04_endpoint_security/400_veracrypt_cross_platform_disk_encryption/) 암호화 도구
401. 전드라이브 암호화 (FDE) — OS 레벨 암호화
402. [필드 레벨 암호화](/knowledge-base/studynote/09_security/04_endpoint_security/402_field_level_encryption/) — DB 컬럼/필드별 암호화
403. [TDE](/knowledge-base/studynote/09_security/04_endpoint_security/403_tde_transparent_data_encryption/) ([Transparent Data Encryption](/knowledge-base/studynote/09_security/04_endpoint_security/403_tde_transparent_data_encryption/)) — DB 엔진 레벨 암호화
404. [백업 암호화](/knowledge-base/studynote/09_security/04_endpoint_security/404_backup_encryption/) — [백업](/knowledge-base/studynote/09_security/04_endpoint_security/404_backup_encryption/) [데이터](/knowledge-base/studynote/09_security/04_endpoint_security/404_backup_encryption/)도 암호화 필수
405. [Secure Erase](/knowledge-base/studynote/09_security/04_endpoint_security/405_secure_erase/) — [SSD](/knowledge-base/studynote/09_security/04_endpoint_security/405_secure_erase/) trim + 암호화 키 삭제
406. [패치 관리](/knowledge-base/studynote/09_security/04_endpoint_security/406_patch_management/) — [CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/406_patch_management/) 점수 기반 우선순위
407. [CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/) (Common Vulnerability Scoring System) — 0~10점
408. [CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/408_cvss_metrics/) 구성 — Base/Transient/Temporal/Global 벡터
409. [CVE](/knowledge-base/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) (Common Vulnerabilities and Exposures) — 취약점 등록 번호
410. [CWE](/knowledge-base/studynote/09_security/04_endpoint_security/410_cwe_taxonomy/) ([Common Weakness Enumeration](/knowledge-base/studynote/09_security/04_endpoint_security/410_cwe_taxonomy/)) — 취약점 유형 [분류](/knowledge-base/studynote/09_security/04_endpoint_security/410_cwe_taxonomy/)
411. [CPE](/knowledge-base/studynote/09_security/04_endpoint_security/411_cpe_inventory_mapping/) ([Common Platform Enumeration](/knowledge-base/studynote/09_security/04_endpoint_security/411_cpe_inventory_mapping/)) — 플랫폼 명칭
412. OVAL (Open Vulnerability and Assessment Language) — 취약점 검사 언어
413. 약구령측정 — 기본パスワード/사전공격
414. 시스템 강화 — Hardening, 불필요 [서비스](/knowledge-base/studynote/09_security/05_web_app_security/414_authentication_failures/) 제거
415. CIS Benchmarks — Center for Internet [Security](/knowledge-base/studynote/09_security/05_web_app_security/415_integrity_failures/) 강화 가이드

---

## 9. 웹 / 애플리케이션 보안 — 60개

416. [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) — 가장 위험한 웹 보안 취약점
417. A01. [취약한 접근 제어](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/) — [IDOR](/knowledge-base/studynote/09_security/05_web_app_security/417_broken_access_control/), 권한 없는 기능 접근
418. [IDOR](/knowledge-base/studynote/09_security/05_web_app_security/418_idor/) (Insecure [Direct](/knowledge-base/studynote/09_security/05_web_app_security/418_idor/) Object [Reference](/knowledge-base/studynote/09_security/05_web_app_security/418_idor/)) — 객체 참조Manipulation
419. [경로 순회](/knowledge-base/studynote/09_security/05_web_app_security/419_path_traversal/) ([Path Traversal](/knowledge-base/studynote/09_security/05_web_app_security/419_path_traversal/)) — ../../etc/passwd
420. [보편적 자원 순회](/knowledge-base/studynote/09_security/05_web_app_security/420_directory_traversal/) ([Directory Traversal](/knowledge-base/studynote/09_security/05_web_app_security/420_directory_traversal/)) — 경로 역추적
421. Local [File](/knowledge-base/studynote/09_security/05_web_app_security/421_local_file_inclusion_lfi/) Inclusion (LFI) —본지 [파일](/knowledge-base/studynote/09_security/05_web_app_security/421_local_file_inclusion_lfi/) 포함
422. Remote [File](/knowledge-base/studynote/09_security/05_web_app_security/422_remote_file_inclusion_rfi/) Inclusion (RFI) — [원격 파일 포함](/knowledge-base/studynote/09_security/05_web_app_security/422_remote_file_inclusion_rfi/)
423. [접근 제어 회피](/knowledge-base/studynote/09_security/05_web_app_security/423_access_control_bypass/) — 메소드 제한 우회, [CORS Misconfiguration](/knowledge-base/studynote/09_security/05_web_app_security/423_access_control_bypass/)
424. A02. [암호화 실패](/knowledge-base/studynote/09_security/05_web_app_security/424_cryptographic_failures/) — 안전하지 않은 암호화 사용
425. [하드코딩 자격증명](/knowledge-base/studynote/09_security/05_web_app_security/425_hardcoded_credentials/) — 소스코드 내 평문 비밀번호
426. 약한 [TLS](/knowledge-base/studynote/09_security/05_web_app_security/426_weak_tls_version/) [버전](/knowledge-base/studynote/09_security/05_web_app_security/426_weak_tls_version/) — [TLS](/knowledge-base/studynote/09_security/05_web_app_security/426_weak_tls_version/) 1.0/1.1 사용
427. [Certificate Pinning](/knowledge-base/studynote/09_security/05_web_app_security/427_certificate_pinning_bypass/) 우회 — Frida, Objection
428. A03. [인젝션](/knowledge-base/studynote/09_security/05_web_app_security/428_injection_overview/) — 입력값 [검증](/knowledge-base/studynote/09_security/05_web_app_security/428_injection_overview/) 부재로 인한 코드 실행
429. SQL [인젝션](/knowledge-base/studynote/09_security/05_web_app_security/429_sql_injection_deep/) — [데이터베이스](/knowledge-base/studynote/09_security/05_web_app_security/429_sql_injection_deep/) [쿼리](/knowledge-base/studynote/09_security/05_web_app_security/429_sql_injection_deep/)Manipulation
430. [Error-based SQL Injection](/knowledge-base/studynote/09_security/05_web_app_security/430_error_based_sqli/) — 오류 메시지 통한 정보 탈취
431. [Blind SQL Injection](/knowledge-base/studynote/09_security/05_web_app_security/431_blind_sql_injection/) — [논리](/knowledge-base/studynote/09_security/05_web_app_security/431_blind_sql_injection/)적 참/거짓 반응으로 정보 추출
432. Time-based [Blind SQL Injection](/knowledge-base/studynote/09_security/05_web_app_security/432_time_based_blind_sqli/) — SLEEP() 함수로 반응 [지연](/knowledge-base/studynote/09_security/05_web_app_security/432_time_based_blind_sqli/)
433. [ORM Injection](/knowledge-base/studynote/09_security/05_web_app_security/433_orm_injection/) — 객체-[관계](/knowledge-base/studynote/09_security/05_web_app_security/433_orm_injection/) 매핑 프레임워크 공격
434. [NoSQL Injection](/knowledge-base/studynote/09_security/05_web_app_security/434_nosql_injection/) — [MongoDB](/knowledge-base/studynote/09_security/05_web_app_security/434_nosql_injection/) 등 문서DB 공격
435. [OS Command Injection](/knowledge-base/studynote/09_security/05_web_app_security/435_os_command_injection/) — 서버 [명령어](/knowledge-base/studynote/09_security/05_web_app_security/435_os_command_injection/) 실행
436. [LDAP Injection](/knowledge-base/studynote/09_security/05_web_app_security/436_ldap_injection_web/) — [LDAP](/knowledge-base/studynote/09_security/05_web_app_security/436_ldap_injection_web/) [쿼리](/knowledge-base/studynote/09_security/05_web_app_security/436_ldap_injection_web/) 조작
437. [XPath Injection](/knowledge-base/studynote/09_security/05_web_app_security/437_xpath_injection/) — XML [데이터](/knowledge-base/studynote/09_security/05_web_app_security/437_xpath_injection/) 질의 조작
438. [Expression Language Injection](/knowledge-base/studynote/09_security/05_web_app_security/438_el_injection/) — Spring/Struts EL 공격
439. [Template Injection](/knowledge-base/studynote/09_security/05_web_app_security/439_ssti/) ([SSTI](/knowledge-base/studynote/09_security/05_web_app_security/439_ssti/)) — 서버 사이드 템플릿 엔진 공격
440. A04. [안전하지 않은 설계](/knowledge-base/studynote/09_security/05_web_app_security/440_insecure_design/) — [threat modeling](/knowledge-base/studynote/09_security/05_web_app_security/440_insecure_design/) 부재
441. [위협 모델링 부재](/knowledge-base/studynote/09_security/05_web_app_security/441_missing_threat_modeling/) — 설계 단계 보안 평가 미실시
442. [안전하지 않은 기본값](/knowledge-base/studynote/09_security/05_web_app_security/442_insecure_defaults/) — 기본 계정/비밀번호
443. [초과 기능](/knowledge-base/studynote/09_security/05_web_app_security/443_excess_functionality/) — 불필요한 기능 활성화
444. A05. [보안 설정 오류](/knowledge-base/studynote/09_security/05_web_app_security/444_security_misconfiguration_deep/) — 잘못된 구성으로 인한 노출
445. 기본 계정 —엄상 제공 기본 비밀번호
446. 불필요 [서비스](/knowledge-base/studynote/09_security/05_web_app_security/446_unnecessary_services/) — 사용 안 하는 [서비스](/knowledge-base/studynote/09_security/05_web_app_security/446_unnecessary_services/) running
447. 오류 메시지 정보 유출 — 내부 경로/[스택](/knowledge-base/studynote/09_security/05_web_app_security/447_error_message_info_leak/) 트레이스
448. [Missing Security Headers](/knowledge-base/studynote/09_security/05_web_app_security/448_missing_security_headers/) — [보안 헤더 미설정](/knowledge-base/studynote/09_security/05_web_app_security/448_missing_security_headers/)
449. Debug Mode — 개발용 모드 생산 환경 노출
450. [CORS Misconfiguration](/knowledge-base/studynote/09_security/05_web_app_security/450_cors_misconfiguration/) — Access-Control-Allow-Origin: *
451. A06. 취약한 [컴포넌트](/knowledge-base/studynote/09_security/05_web_app_security/451_vulnerable_components/) — 알려진 취약점 포함 [라이브러리](/knowledge-base/studynote/09_security/05_web_app_security/451_vulnerable_components/)
452. [Log4Shell](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/) ([CVE-2021-44228](/knowledge-base/studynote/09_security/05_web_app_security/452_log4shell/)) — Log4j RCE
453. [서드파티 라이브러리 취약점](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/) — npm/PyPI/RubyGems 의존성
454. A07. [인증](/knowledge-base/studynote/09_security/05_web_app_security/454_authentication_failures/) 실패 — 부적절한 [인증](/knowledge-base/studynote/09_security/05_web_app_security/454_authentication_failures/) 메커니즘
455. [크리덴셜 스터핑](/knowledge-base/studynote/09_security/05_web_app_security/455_credential_stuffing/) — 유출 계정 재사용
456. [브루트포스](/knowledge-base/studynote/09_security/05_web_app_security/456_brute_force/) — 무차별 대입 공격
457. [패스워드 스프레이](/knowledge-base/studynote/09_security/05_web_app_security/457_password_spraying/) — 다양한 비밀번호 소량 시도
458. [크리덴셜 풀링](/knowledge-base/studynote/09_security/05_web_app_security/458_credential_pooling/) — 자격증명 목록 활용
459. [세션](/knowledge-base/studynote/09_security/05_web_app_security/459_session_id_exposure/) ID 노출 — URL, [로그](/knowledge-base/studynote/09_security/05_web_app_security/459_session_id_exposure/), Referer 헤더
460. [세션 고정](/knowledge-base/studynote/09_security/05_web_app_security/460_session_fixation/) — [세션](/knowledge-base/studynote/09_security/05_web_app_security/460_session_fixation/) ID 고정 공격
461. A08. [무결성](/knowledge-base/studynote/09_security/05_web_app_security/461_integrity_failures/) 실패 — 소프트웨어 [무결성](/knowledge-base/studynote/09_security/05_web_app_security/461_integrity_failures/) [검증](/knowledge-base/studynote/09_security/05_web_app_security/461_integrity_failures/) 부재
462. [CI](/knowledge-base/studynote/09_security/05_web_app_security/462_cicd_security/)/CD 보안 — 파이프라인 침해, [의존성 오염](/knowledge-base/studynote/09_security/05_web_app_security/462_cicd_security/)
463. [의존성 오염](/knowledge-base/studynote/09_security/05_web_app_security/463_dependency_confusion/) ([Dependency Confusion](/knowledge-base/studynote/09_security/05_web_app_security/463_dependency_confusion/)) — 비공개 패키지 덮어쓰기
464. [잘못된 서명 검증](/knowledge-base/studynote/09_security/05_web_app_security/464_insecure_signature_verification/) — [코드 서명](/knowledge-base/studynote/09_security/05_web_app_security/464_insecure_signature_verification/) [검증](/knowledge-base/studynote/09_security/05_web_app_security/464_insecure_signature_verification/) 우회
465. A09. 로깅/모니터링 실패 — 증거 미보존
466. [Blindness](/knowledge-base/studynote/09_security/05_web_app_security/466_logging_blindness/) — 공격 탐지 못 함
467. [Logging Without Alert](/knowledge-base/studynote/09_security/05_web_app_security/467_logging_without_alert/) — [로그](/knowledge-base/studynote/09_security/05_web_app_security/467_logging_without_alert/)만 기록, 알림 없음
468. A10. [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/468_ssrf/) — 서버 사이드 요청 위조
469. [SSRF](/knowledge-base/studynote/09_security/05_web_app_security/469_ssrf_metadata/) [메타데이터](/knowledge-base/studynote/09_security/05_web_app_security/469_ssrf_metadata/) — 169.254.169.254 등 cloud [metadata](/knowledge-base/studynote/09_security/05_web_app_security/469_ssrf_metadata/)
470. [XSS](/knowledge-base/studynote/09_security/05_web_app_security/470_xss/) ([Cross-Site Scripting](/knowledge-base/studynote/09_security/05_web_app_security/470_xss/)) —객호단 스크립트 삽입
471. 반사형 [XSS](/knowledge-base/studynote/09_security/05_web_app_security/471_reflected_xss/) — URL 파라미터 반영
472. 저장형 [XSS](/knowledge-base/studynote/09_security/05_web_app_security/472_stored_xss/) — DB에 저장, 모든 사용자에게 발동
473. [DOM-based XSS](/knowledge-base/studynote/09_security/05_web_app_security/473_dom_xss/) —객호단 JavaScript 변조
474. [XSS](/knowledge-base/studynote/09_security/05_web_app_security/474_xss_payload/) 페이로드 — <script>alert(1)</script>, img onerror
475. [CSP](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) ([Content Security Policy](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/)) — [XSS](/knowledge-base/studynote/09_security/05_web_app_security/475_csp/) 완화 헤더

---

## [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/). 웹 보안 심화 / [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 보안 — 50개

476. [CSRF](/knowledge-base/studynote/09_security/05_web_app_security/476_csrf_deep/) ([Cross-Site Request Forgery](/knowledge-base/studynote/09_security/05_web_app_security/476_csrf_deep/)) — 사용자의 의지와 무관한 요청
477. SameSite [쿠키](/knowledge-base/studynote/09_security/05_web_app_security/477_samesite_cookie/) — [CSRF](/knowledge-base/studynote/09_security/05_web_app_security/477_samesite_cookie/) 방어
478. [CSRF Token](/knowledge-base/studynote/09_security/05_web_app_security/478_csrf_token/) — 난수 토큰 요구
479. 쌍중 Submit [Cookie](/knowledge-base/studynote/09_security/05_web_app_security/479_double_submit_cookie/) — [쿠키](/knowledge-base/studynote/09_security/05_web_app_security/479_double_submit_cookie/)+파라미터 대조
480. [Clickjacking](/knowledge-base/studynote/09_security/05_web_app_security/480_clickjacking/) — 투명 iframe 덮기
481. X-Frame-Options — frame [embedding](/knowledge-base/studynote/09_security/05_web_app_security/481_x_frame_options/) 차단
482. [frame-ancestors](/knowledge-base/studynote/09_security/05_web_app_security/482_frame_ancestors/) — [CSP](/knowledge-base/studynote/09_security/05_web_app_security/482_frame_ancestors/) [버전](/knowledge-base/studynote/09_security/05_web_app_security/482_frame_ancestors/)의 [frame-ancestors](/knowledge-base/studynote/09_security/05_web_app_security/482_frame_ancestors/)
483. [CORS Preflight](/knowledge-base/studynote/09_security/05_web_app_security/483_cors_preflight/) — OPTIONS 요청으로 사전 [검증](/knowledge-base/studynote/09_security/05_web_app_security/483_cors_preflight/)
484. CORS 요청 흐름 — Origin 헤더 -> 서버 허용/거부
485. [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/) — 웹 취약점 스캐너
486. [Burp Suite](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/) — 웹 [프록시](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/),삼투 테스트 도구
487. [SQLMap](/knowledge-base/studynote/09_security/05_web_app_security/487_sqlmap/) — SQL [인젝션](/knowledge-base/studynote/09_security/05_web_app_security/487_sqlmap/) 자동화 도구
488. [Nikto](/knowledge-base/studynote/09_security/05_web_app_security/488_nikto/) — 웹 서버 취약점 스캐너
489. [httpoxy](/knowledge-base/studynote/09_security/05_web_app_security/489_httpoxy/) — CGI 환경변수 proxyManipulation
490. [Host Header Injection](/knowledge-base/studynote/09_security/05_web_app_security/490_host_header_injection/) — X-Forwarded-Host [검증](/knowledge-base/studynote/09_security/05_web_app_security/490_host_header_injection/) 우회
491. [Web Cache Deception](/knowledge-base/studynote/09_security/05_web_app_security/491_web_cache_deception/) — 캐시poisoning
492. [Unicode Normalization](/knowledge-base/studynote/09_security/05_web_app_security/492_unicode_normalization/) — нормализация 차이 공격
493. [NULL Byte Injection](/knowledge-base/studynote/09_security/05_web_app_security/493_null_byte_injection/) — %00로 확장자 우회
494. [Null Byte Poisoning](/knowledge-base/studynote/09_security/05_web_app_security/494_null_byte_poisoning/) — [파일](/knowledge-base/studynote/09_security/05_web_app_security/494_null_byte_poisoning/)명 내 null 문자
495. [OAS](/knowledge-base/studynote/09_security/05_web_app_security/495_oas_openapi_specification/) ([OpenAPI Specification](/knowledge-base/studynote/09_security/05_web_app_security/495_oas_openapi_specification/)) — [REST API](/knowledge-base/studynote/09_security/05_web_app_security/495_oas_openapi_specification/) 표준
496. [GraphQL](/knowledge-base/studynote/09_security/05_web_app_security/496_graphql_introspection/) 인트로스펙션 — [API](/knowledge-base/studynote/09_security/05_web_app_security/496_graphql_introspection/) [스키마](/knowledge-base/studynote/09_security/05_web_app_security/496_graphql_introspection/) 공개
497. [GraphQL DoS](/knowledge-base/studynote/09_security/05_web_app_security/497_graphql_dos/) — depth/alias 제한 없으면 무한 [쿼리](/knowledge-base/studynote/09_security/05_web_app_security/497_graphql_dos/)
498. [REST API](/knowledge-base/studynote/09_security/05_web_app_security/498_rest_api_security/) 보안 — [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/498_rest_api_security/), [JWT](/knowledge-base/studynote/09_security/05_web_app_security/498_rest_api_security/), [HMAC](/knowledge-base/studynote/09_security/05_web_app_security/498_rest_api_security/)
499. [API Versioning](/knowledge-base/studynote/09_security/05_web_app_security/499_api_versioning_security/) — [API](/knowledge-base/studynote/09_security/05_web_app_security/499_api_versioning_security/) [버전](/knowledge-base/studynote/09_security/05_web_app_security/499_api_versioning_security/) 관리와 보안
500. [JWT](/knowledge-base/studynote/09_security/05_web_app_security/500_jwt_json_web_token/) ([JSON Web Token](/knowledge-base/studynote/09_security/05_web_app_security/500_jwt_json_web_token/)) — [stateless](/knowledge-base/studynote/09_security/05_web_app_security/500_jwt_json_web_token/) [인증](/knowledge-base/studynote/09_security/05_web_app_security/500_jwt_json_web_token/)
501. [JWT](/knowledge-base/studynote/09_security/05_web_app_security/501_jwt_structure_jws_jwe/) 구조 — Header/Payload/Signature (JWS/JWE)
502. [JWT](/knowledge-base/studynote/09_security/05_web_app_security/502_jwt_alg_none_vulnerability/) [alg](/knowledge-base/studynote/09_security/05_web_app_security/502_jwt_alg_none_vulnerability/): none — 취약점, [alg](/knowledge-base/studynote/09_security/05_web_app_security/502_jwt_alg_none_vulnerability/) [검증](/knowledge-base/studynote/09_security/05_web_app_security/502_jwt_alg_none_vulnerability/) 필수
503. [HS256 vs RS256](/knowledge-base/studynote/09_security/05_web_app_security/503_hs256_vs_rs256_jwt_signing/) — 대칭/비대칭 서명
504. [JWT](/knowledge-base/studynote/09_security/05_web_app_security/504_jwt_leakage_xss_protection/) 유출 — XSS로 토큰 탈취
505. [Refresh Token](/knowledge-base/studynote/09_security/05_web_app_security/505_refresh_token/) — [액세스 토큰 재발급](/knowledge-base/studynote/09_security/05_web_app_security/505_refresh_token/)
506. OAuth 2.0 — 델리게이션 [프로토콜](/knowledge-base/studynote/09_security/05_web_app_security/506_oauth_2_0/)
507. OAuth 2.0 4가지 Grant — [Authorization](/knowledge-base/studynote/09_security/05_web_app_security/507_oauth_2_0_grants/) [Code](/knowledge-base/studynote/09_security/05_web_app_security/507_oauth_2_0_grants/)/[PKCE](/knowledge-base/studynote/09_security/05_web_app_security/507_oauth_2_0_grants/)/[Client](/knowledge-base/studynote/09_security/05_web_app_security/507_oauth_2_0_grants/) Credentials/[ROP](/knowledge-base/studynote/09_security/05_web_app_security/507_oauth_2_0_grants/)
508. [Authorization Code Grant](/knowledge-base/studynote/09_security/05_web_app_security/508_authorization_code_grant/) —redirect_uri 기반
509. [PKCE](/knowledge-base/studynote/09_security/05_web_app_security/509_pkce_public_client/) (Proof [Key](/knowledge-base/studynote/09_security/05_web_app_security/509_pkce_public_client/) for [Code](/knowledge-base/studynote/09_security/05_web_app_security/509_pkce_public_client/) Exchange) — public [client](/knowledge-base/studynote/09_security/05_web_app_security/509_pkce_public_client/) 보안
510. [Open Redirect](/knowledge-base/studynote/09_security/05_web_app_security/510_open_redirect_oauth/) — OAuth redirect_uri 우회
511. [Token Leakage](/knowledge-base/studynote/09_security/05_web_app_security/511_token_leakage/) — URL 내 토큰 노출
512. [Scope](/knowledge-base/studynote/09_security/05_web_app_security/512_oauth_scope/) — OAuth 권한 범위
513. Access Token vs [Refresh Token](/knowledge-base/studynote/09_security/05_web_app_security/513_access_token_vs_refresh_token/) — 수명 차이
514. [OIDC](/knowledge-base/studynote/09_security/05_web_app_security/514_oidc_overview/) — OAuth 2.0지상적 신원 레이어
515. [ID Token](/knowledge-base/studynote/09_security/05_web_app_security/515_id_token_jwt/) — OIDC의 사용자 신원 증명
516. [ID Token](/knowledge-base/studynote/09_security/05_web_app_security/516_id_token_vs_access_token/) vs Access Token — 용도 구분
517. [Discovery Document](/knowledge-base/studynote/09_security/05_web_app_security/517_oidc_discovery_document/) — .well-known/openid-configuration
518. [jwks_uri](/knowledge-base/studynote/09_security/05_web_app_security/518_jwks_uri_endpoint/) — [JSON](/knowledge-base/studynote/09_security/05_web_app_security/518_jwks_uri_endpoint/) Web [Key](/knowledge-base/studynote/09_security/05_web_app_security/518_jwks_uri_endpoint/) Set 엔드포인트
519. [Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/) — [replay attack](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/) 방지
520. [Rate Limiting](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) — 요청 수 제한으로 [DoS](/knowledge-base/studynote/09_security/05_web_app_security/520_rate_limiting/) 방지
521. [WAF](/knowledge-base/studynote/09_security/05_web_app_security/521_waf_rules_owasp_crs/) 규칙 — OWASP [CRS](/knowledge-base/studynote/09_security/05_web_app_security/521_waf_rules_owasp_crs/) 기반
522. [ModSecurity](/knowledge-base/studynote/09_security/05_web_app_security/522_modsecurity_crs/) Core Rule Set — [generic 공격 탐지](/knowledge-base/studynote/09_security/05_web_app_security/522_modsecurity_crs/)
523. [HTTP Request Smuggling](/knowledge-base/studynote/09_security/05_web_app_security/523_http_request_smuggling_concept/) — front-end/back-end interpretation 차이
524. [HTTP](/knowledge-base/studynote/09_security/05_web_app_security/524_http_request_smuggling_types/) Request주사 — CL.[TE](/knowledge-base/studynote/09_security/05_web_app_security/524_http_request_smuggling_types/), [TE](/knowledge-base/studynote/09_security/05_web_app_security/524_http_request_smuggling_types/).CL, H2.CL
525. [HTTP Response Smuggling](/knowledge-base/studynote/09_security/05_web_app_security/525_http_response_smuggling/) — 응답 분할

---

## [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). [신원 관리](/knowledge-base/studynote/09_security/11_iam_access_control/527_identity_management/) / 접근 제어 — 55개

526. [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/)) — 신원+접근 통합 관리
527. [신원 관리](/knowledge-base/studynote/09_security/11_iam_access_control/527_identity_management/) — 사용자 lifecycle ([프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/527_identity_management/)/수정/비활성화/삭제)
528. [Provisioning](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) — 사용자 계정 자동 [생성](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)
529. [Deprovisioning](/knowledge-base/studynote/09_security/11_iam_access_control/529_deprovisioning/) — 퇴직/이직 시 계정 즉시 삭제
530. Joiner/Mover/Leaver 프로세스 — 신원 lifecycle 관리
531. [SSO](/knowledge-base/studynote/09_security/11_iam_access_control/531_sso/) ([Single Sign-On](/knowledge-base/studynote/09_security/11_iam_access_control/531_sso/)) —일다음등록，다アプリ access
532. SAML 2.0 — XML 기반 [SSO](/knowledge-base/studynote/09_security/11_iam_access_control/532_saml_2_0/) [프로토콜](/knowledge-base/studynote/09_security/11_iam_access_control/532_saml_2_0/)
533. [SAML Assertion](/knowledge-base/studynote/09_security/11_iam_access_control/533_saml_assertion/) — 신원 정보 포함 XML
534. SAML Request/Response — [SP](/knowledge-base/studynote/09_security/11_iam_access_control/534_saml_request_response/)-Initiated/[IdP](/knowledge-base/studynote/09_security/11_iam_access_control/534_saml_request_response/)-Initiated
535. [SP](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/) ([Service Provider](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/)) — [서비스](/knowledge-base/studynote/09_security/11_iam_access_control/535_sp_service_provider/) 제공자
536. [IdP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) ([Identity Provider](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)) — 신원 제공자
537. [OpenID Connect](/knowledge-base/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/) — OAuth 2.0 기반 [SSO](/knowledge-base/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/)
538. [OIDC Discovery](/knowledge-base/studynote/09_security/11_iam_access_control/538_oidc_discovery/) — 자동 [설정](/knowledge-base/studynote/09_security/11_iam_access_control/538_oidc_discovery/) [메타데이터](/knowledge-base/studynote/09_security/11_iam_access_control/538_oidc_discovery/)
539. [Claims](/knowledge-base/studynote/09_security/11_iam_access_control/539_claims/) — OIDC의 사용자 [속성](/knowledge-base/studynote/09_security/11_iam_access_control/539_claims/)
540. [OIDC Scope](/knowledge-base/studynote/09_security/11_iam_access_control/540_scope_oidc/) ([OpenID Connect Scope](/knowledge-base/studynote/09_security/11_iam_access_control/540_scope_oidc/)) — 요청하는 정보 범위 (openid/profile/email)
541. [PKCE in OIDC](/knowledge-base/studynote/09_security/11_iam_access_control/541_pkce_in_oidc/) — [Authorization](/knowledge-base/studynote/09_security/11_iam_access_control/541_pkce_in_oidc/) [Code](/knowledge-base/studynote/09_security/11_iam_access_control/541_pkce_in_oidc/) [보호](/knowledge-base/studynote/09_security/11_iam_access_control/541_pkce_in_oidc/)
542. OAuth 2.0 vs [OIDC](/knowledge-base/studynote/09_security/11_iam_access_control/542_oauth2_vs_oidc/) — 델리게이션 vs [인증](/knowledge-base/studynote/09_security/11_iam_access_control/542_oauth2_vs_oidc/)
543. [Federation](/knowledge-base/studynote/09_security/11_iam_access_control/543_federation/) — 조직 간 신뢰 기반 ID 공유
544. [Trust Relationship](/knowledge-base/studynote/09_security/11_iam_access_control/544_trust_relationship/) — [federation](/knowledge-base/studynote/09_security/11_iam_access_control/544_trust_relationship/) 파트너 간 신뢰
545. [eduGAIN](/knowledge-base/studynote/09_security/11_iam_access_control/545_edugain/) — 학술 기관간 [federation](/knowledge-base/studynote/09_security/11_iam_access_control/545_edugain/)
546. [Shibboleth](/knowledge-base/studynote/09_security/11_iam_access_control/546_shibboleth/) — SAML 기반 [federation](/knowledge-base/studynote/09_security/11_iam_access_control/546_shibboleth/)
547. [LDAP](/knowledge-base/studynote/09_security/11_iam_access_control/547_ldap/) 기반 [인증](/knowledge-base/studynote/09_security/11_iam_access_control/547_ldap/)/조회 — [디렉터리](/knowledge-base/studynote/09_security/11_iam_access_control/547_ldap/) [서비스](/knowledge-base/studynote/09_security/11_iam_access_control/547_ldap/) [프로토콜](/knowledge-base/studynote/09_security/11_iam_access_control/547_ldap/)
548. [Active Directory](/knowledge-base/studynote/09_security/11_iam_access_control/548_active_directory/) — Microsoft [디렉터리](/knowledge-base/studynote/09_security/11_iam_access_control/548_active_directory/) [서비스](/knowledge-base/studynote/09_security/11_iam_access_control/548_active_directory/)
549. Azure AD / Microsoft Entra ID — 클라우드 신원
550. [Azure AD Connect](/knowledge-base/studynote/09_security/11_iam_access_control/550_azure_ad_connect/) — [온프레미스](/knowledge-base/studynote/09_security/11_iam_access_control/550_azure_ad_connect/) AD 클라우드 연동
551. [Okta](/knowledge-base/studynote/09_security/11_iam_access_control/551_okta_idaas/) — [SaaS](/knowledge-base/studynote/09_security/11_iam_access_control/551_okta_idaas/) [IDaaS](/knowledge-base/studynote/09_security/11_iam_access_control/551_okta_idaas/)
552. [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) ([Multi-Factor Authentication](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/)) — 다중 [인증](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/)
553. [지식 요인](/knowledge-base/studynote/09_security/11_iam_access_control/553_knowledge_factor/) — 비밀번호, PIN
554. [소유 요인](/knowledge-base/studynote/09_security/11_iam_access_control/554_possession_factor/) — 토큰, 스마트폰, 스마트카드
555. [내재 요인](/knowledge-base/studynote/09_security/11_iam_access_control/555_inherence_factor/) — 지문, 홍채, 음성, 얼굴
556. [위치 요인](/knowledge-base/studynote/09_security/11_iam_access_control/556_location_factor/) — GPS, IP 기반 위치
557. [행동 요인](/knowledge-base/studynote/09_security/11_iam_access_control/557_behavioral_factor/) — 타이핑 패턴, 마우스 움직임
558. [TOTP](/knowledge-base/studynote/09_security/11_iam_access_control/558_totp/) ([Time-based OTP](/knowledge-base/studynote/09_security/11_iam_access_control/558_totp/)) — 30초마다 변경
559. [HOTP](/knowledge-base/studynote/09_security/11_iam_access_control/559_hotp/) ([HMAC-based OTP](/knowledge-base/studynote/09_security/11_iam_access_control/559_hotp/)) — [카운터](/knowledge-base/studynote/09_security/11_iam_access_control/559_hotp/) 기반
560. [Push Notification](/knowledge-base/studynote/09_security/11_iam_access_control/560_push_notification/) — 모바일 푸시 알림
561. FIDO2 / WebAuthn —공개키 암호 기반 [인증](/knowledge-base/studynote/09_security/11_iam_access_control/561_fido2_webauthn/)
562. [Passkey](/knowledge-base/studynote/09_security/11_iam_access_control/562_passkey/) — FIDO2 기반, 플랫폼 관리
563. [Passkey](/knowledge-base/studynote/09_security/11_iam_access_control/563_passkey_benefits/) 장점 — [피싱](/knowledge-base/studynote/09_security/11_iam_access_control/563_passkey_benefits/) [저항](/knowledge-base/studynote/09_security/11_iam_access_control/563_passkey_benefits/), 암호 불필요
564. [PAM](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/) ([Privileged Access Management](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/)) — [특권 계정](/knowledge-base/studynote/09_security/11_iam_access_control/564_pam/) 관리
565. 특권 계정 — 관리자,root, [서비스 계정](/knowledge-base/studynote/09_security/11_iam_access_control/565_privileged_accounts/)
566. [세션 레코딩](/knowledge-base/studynote/09_security/11_iam_access_control/566_session_recording/) — 특권 [세션](/knowledge-base/studynote/09_security/11_iam_access_control/566_session_recording/) 녹화/[감사](/knowledge-base/studynote/09_security/11_iam_access_control/566_session_recording/)
567. [vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/) — 비밀번호 금고 (HashiCorp [Vault](/knowledge-base/studynote/09_security/11_iam_access_control/567_vault/))
568. [Just-In-Time](/knowledge-base/studynote/09_security/11_iam_access_control/568_jit_access/) Access — 필요 시만 일시적 권한
569. [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) ([Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) — 역할 기반 권한
570. [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/570_rbac_1_2_3/) 1/2/3 —.flat/hierarchical/constrained
571. [역할 계층](/knowledge-base/studynote/09_security/11_iam_access_control/571_role_hierarchy/) — 상위 역할이 하위 권한 [상속](/knowledge-base/studynote/09_security/11_iam_access_control/571_role_hierarchy/)
572. [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) ([Attribute-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/)) — [속성](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) 기반
573. [속성 종류](/knowledge-base/studynote/09_security/11_iam_access_control/573_abac_attributes/) — subject/object/[environment](/knowledge-base/studynote/09_security/11_iam_access_control/573_abac_attributes/)/action
574. [XACML](/knowledge-base/studynote/09_security/11_iam_access_control/574_xacml/) (eXtensible [Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/574_xacml/) Markup Language) — [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/574_xacml/) [정책](/knowledge-base/studynote/09_security/11_iam_access_control/574_xacml/) 언어
575. [ReBAC](/knowledge-base/studynote/09_security/11_iam_access_control/575_rebac/) ([Relationship-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/575_rebac/)) — [관계](/knowledge-base/studynote/09_security/11_iam_access_control/575_rebac/) 기반
576. [Zanzibar](/knowledge-base/studynote/09_security/11_iam_access_control/576_zanzibar/) — Google의 권한 시스템
577. [최소 권한 원칙](/knowledge-base/studynote/09_security/11_iam_access_control/577_principle_of_least_privilege/) — 필요한 최소 권한만 부여
578. [직무 분리](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/) (SoD) —권한 [분산](/knowledge-base/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/)으로 부정행위 방지
579. [어카운팅](/knowledge-base/studynote/09_security/11_iam_access_control/579_accounting_auditing/) — 접근 기록, [감사](/knowledge-base/studynote/09_security/11_iam_access_control/579_accounting_auditing/) 자료
580. [접근 검토](/knowledge-base/studynote/09_security/11_iam_access_control/580_access_review/) ([Access Review](/knowledge-base/studynote/09_security/11_iam_access_control/580_access_review/)) — 정기적 권한 재검토

---

## 12. 신원 보안 심화 / 위협 — 40개

581. [인증 서버](/knowledge-base/studynote/09_security/12_identity_threat_advanced/581_authentication_server/) — [KDC](/knowledge-base/studynote/09_security/12_identity_threat_advanced/581_authentication_server/), [IdP](/knowledge-base/studynote/09_security/12_identity_threat_advanced/581_authentication_server/), [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/581_authentication_server/) endpoints
582. [Kerberos](/knowledge-base/studynote/09_security/12_identity_threat_advanced/582_kerberos/) — 네트워크 [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/582_kerberos/) [프로토콜](/knowledge-base/studynote/09_security/12_identity_threat_advanced/582_kerberos/) (v5)
583. [KDC](/knowledge-base/studynote/09_security/12_identity_threat_advanced/583_kdc/) ([Key Distribution Center](/knowledge-base/studynote/09_security/12_identity_threat_advanced/583_kdc/)) — [AS](/knowledge-base/studynote/09_security/12_identity_threat_advanced/583_kdc/)+[TGS](/knowledge-base/studynote/09_security/12_identity_threat_advanced/583_kdc/) 통합
584. [AS](/knowledge-base/studynote/09_security/12_identity_threat_advanced/584_as/) ([Authentication Server](/knowledge-base/studynote/09_security/12_identity_threat_advanced/584_as/)) — [초기](/knowledge-base/studynote/09_security/12_identity_threat_advanced/584_as/) [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/584_as/)
585. [TGS](/knowledge-base/studynote/09_security/12_identity_threat_advanced/585_tgs/) ([Ticket Granting Server](/knowledge-base/studynote/09_security/12_identity_threat_advanced/585_tgs/)) — 티켓 발급
586. [TGT](/knowledge-base/studynote/09_security/12_identity_threat_advanced/586_tgt/) ([Ticket Granting Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/586_tgt/)) — 장기 티켓
587. [ST](/knowledge-base/studynote/09_security/12_identity_threat_advanced/587_st/) ([Service Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/587_st/)) — 특정 [서비스](/knowledge-base/studynote/09_security/12_identity_threat_advanced/587_st/)용 단기 티켓
588. [Kerberos](/knowledge-base/studynote/09_security/12_identity_threat_advanced/588_mutual_authentication/) 상호 [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/588_mutual_authentication/) — [client](/knowledge-base/studynote/09_security/12_identity_threat_advanced/588_mutual_authentication/)+server mutual
589. [Silver Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/589_silver_ticket/) — [ST](/knowledge-base/studynote/09_security/12_identity_threat_advanced/589_silver_ticket/) 위조 ([서비스 계정](/knowledge-base/studynote/09_security/12_identity_threat_advanced/589_silver_ticket/) 키 사용)
590. [Golden Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/590_golden_ticket/) — [TGT](/knowledge-base/studynote/09_security/12_identity_threat_advanced/590_golden_ticket/) 위조 (KRBTGT 키 사용)
591. [Pass-the-Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/591_ptt/) — 메모리 내 티켓 재사용
592. [Pass-the-Hash](/knowledge-base/studynote/09_security/12_identity_threat_advanced/592_pth/) — [NTLM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/592_pth/) 해시 재사용
593. [Kerberos Bronze Attack](/knowledge-base/studynote/09_security/12_identity_threat_advanced/593_bronze_attack/) — [AS-REP Roasting](/knowledge-base/studynote/09_security/12_identity_threat_advanced/593_bronze_attack/)
594. [NTLM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/594_ntlm/) — Windows 네이티브 [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/594_ntlm/) [프로토콜](/knowledge-base/studynote/09_security/12_identity_threat_advanced/594_ntlm/)
595. [NTLM Hash](/knowledge-base/studynote/09_security/12_identity_threat_advanced/595_ntlm_hash/) — MD4(UTF-16LE(password))
596. [NTLM Authentication](/knowledge-base/studynote/09_security/12_identity_threat_advanced/596_ntlm_authentication/) — 3-way handshake (질순/응답)
597. [LM Hash](/knowledge-base/studynote/09_security/12_identity_threat_advanced/597_lm_hash/) — [DES](/knowledge-base/studynote/09_security/12_identity_threat_advanced/597_lm_hash/) 기반, 취약한 레거시
598. [NTLMv2](/knowledge-base/studynote/09_security/12_identity_threat_advanced/598_ntlmv2/) — [HMAC](/knowledge-base/studynote/09_security/12_identity_threat_advanced/598_ntlmv2/)-[MD5](/knowledge-base/studynote/09_security/12_identity_threat_advanced/598_ntlmv2/) 기반 강화 [버전](/knowledge-base/studynote/09_security/12_identity_threat_advanced/598_ntlmv2/)
599. [NetNTLM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/599_netntlm/) — 네트워크 상에서만 사용되는 [NTLM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/599_netntlm/)
600. [MS-CHAPv2](/knowledge-base/studynote/09_security/12_identity_threat_advanced/600_ms_chapv2/) — [PPP](/knowledge-base/studynote/09_security/12_identity_threat_advanced/600_ms_chapv2/)/[EAP](/knowledge-base/studynote/09_security/12_identity_threat_advanced/600_ms_chapv2/) 내부의 [NTLM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/600_ms_chapv2/) 변형
601. [Credential Dumping](/knowledge-base/studynote/09_security/uncategorized/601_input_validation/) — LSASS 메모리/ [SAM hive](/knowledge-base/studynote/09_security/uncategorized/601_input_validation/) 추출
602. [Mimikatz](/knowledge-base/studynote/09_security/12_identity_threat_advanced/602_mimikatz/) — 크리덴셜 추출 도구
603. [WDigest](/knowledge-base/studynote/09_security/uncategorized/603_buffer_overflow/) — 평문 비밀번호 [캐싱](/knowledge-base/studynote/09_security/uncategorized/603_buffer_overflow/) ([레지스트리](/knowledge-base/studynote/09_security/uncategorized/603_buffer_overflow/) [설정](/knowledge-base/studynote/09_security/uncategorized/603_buffer_overflow/))
604. [SSP](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/) ([Security Support Provider](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/)) — [인증](/knowledge-base/studynote/09_security/uncategorized/604_sql_injection/) 공급자 DLL
605. Golden/[Silver Ticket](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/) [mitigation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/605_golden_silver_ticket_mitigation/) — KRBTGT 비밀번호 주월적 교체
606. Protected Users 그룹 — [Kerberos](/knowledge-base/studynote/09_security/uncategorized/606_csrf/) 전용 [인증](/knowledge-base/studynote/09_security/uncategorized/606_csrf/)
607. [Smart Card](/knowledge-base/studynote/09_security/uncategorized/607_secure_session_management/) — [인증](/knowledge-base/studynote/09_security/uncategorized/607_secure_session_management/)서 기반 [MFA](/knowledge-base/studynote/09_security/uncategorized/607_secure_session_management/)
608. [PKINIT](/knowledge-base/studynote/09_security/uncategorized/608_error_handling_logging/) — Kerberos에서 공개키 [인증](/knowledge-base/studynote/09_security/uncategorized/608_error_handling_logging/) 사용
609. [Remote Desktop Gateway](/knowledge-base/studynote/09_security/12_identity_threat_advanced/609_remote_desktop_gateway/) — RDG, [HTTPS](/knowledge-base/studynote/09_security/12_identity_threat_advanced/609_remote_desktop_gateway/) 기반 원격접속
610. Azure AD조건부 액세스 — [정책](/knowledge-base/studynote/09_security/uncategorized/610_memory_management/) 기반 접근 제어
611. [조건부 액세스 신호](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) — 사용자/위험/디바이스/위치
612. [Identity Protection](/knowledge-base/studynote/09_security/uncategorized/612_dependency_management/) — Azure AD ID [보호](/knowledge-base/studynote/09_security/uncategorized/612_dependency_management/)
613. [UEBA](/knowledge-base/studynote/09_security/uncategorized/613_static_dynamic_analysis/) (User Entity Behavior Analytics) — 행동 기반 [이상 탐지](/knowledge-base/studynote/09_security/uncategorized/613_static_dynamic_analysis/)
614. [애드혹 identity](/knowledge-base/studynote/09_security/uncategorized/614_cryptographic_implementation/) — 임시/외부 사용자 관리
615. [Federated Identity](/knowledge-base/studynote/09_security/uncategorized/615_api_security/) — SAML/[OIDC](/knowledge-base/studynote/09_security/uncategorized/615_api_security/) 기반 연합
616. [Identity Bridge](/knowledge-base/studynote/09_security/12_identity_threat_advanced/616_identity_bridge/) — AD FS, [Azure AD Connect](/knowledge-base/studynote/09_security/12_identity_threat_advanced/616_identity_bridge/) [Federation](/knowledge-base/studynote/09_security/12_identity_threat_advanced/616_identity_bridge/)
617. SCIM 2.0 — 자동 사용자 [프로비저닝](/knowledge-base/studynote/09_security/12_identity_threat_advanced/617_scim_2_0/) [프로토콜](/knowledge-base/studynote/09_security/12_identity_threat_advanced/617_scim_2_0/)
618. [JIT](/knowledge-base/studynote/09_security/12_identity_threat_advanced/618_jit_provisioning/) [프로비저닝](/knowledge-base/studynote/09_security/12_identity_threat_advanced/618_jit_provisioning/) — [Just-In-Time](/knowledge-base/studynote/09_security/12_identity_threat_advanced/618_jit_provisioning/), On-Demand [프로비저닝](/knowledge-base/studynote/09_security/12_identity_threat_advanced/618_jit_provisioning/)
619. [ID Governance](/knowledge-base/studynote/09_security/12_identity_threat_advanced/619_id_governance_iga/) — 권한 [인증](/knowledge-base/studynote/09_security/12_identity_threat_advanced/619_id_governance_iga/), 합성성 검토
620. [Privileged Identity Management](/knowledge-base/studynote/09_security/12_identity_threat_advanced/620_privileged_identity_management_pim/) ([PIM](/knowledge-base/studynote/09_security/12_identity_threat_advanced/620_privileged_identity_management_pim/)) —Azure 특권 ID 관리

---

## 13. 보안 운영 (SecOps) — 60개

621. [SOC](/knowledge-base/studynote/09_security/13_secops_ir_forensics/621_soc/) ([Security Operations Center](/knowledge-base/studynote/09_security/13_secops_ir_forensics/621_soc/)) — 보안 관제 조직
622. [SOC](/knowledge-base/studynote/09_security/13_secops_ir_forensics/622_soc_tiers/) 티어 — 티어 1(alert 분석)/2( approfondita조사)/3( [threat hunting](/knowledge-base/studynote/09_security/13_secops_ir_forensics/622_soc_tiers/))
623. [NOC](/knowledge-base/studynote/09_security/13_secops_ir_forensics/623_noc/) ([Network Operations Center](/knowledge-base/studynote/09_security/13_secops_ir_forensics/623_noc/)) — 네트워크 모니터링
624. [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) ([Security](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) Information and [Event Management](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/)) — [로그](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/) 집적/[상관 분석](/knowledge-base/studynote/09_security/13_secops_ir_forensics/624_siem/)
625. [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/625_siem_architecture/) 구성 — 수집(Curator)/저장(Repository)/분석(Analyzer)/가시화(Dashboard)
626. [로그 수집](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/) — [syslog](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/), Windows Event Log, [NetFlow](/knowledge-base/studynote/09_security/13_secops_ir_forensics/626_log_collection/), PCAP
627. Normalizzazione — 다양 [로그](/knowledge-base/studynote/09_security/13_secops_ir_forensics/627_normalization/) 형식 [정규화](/knowledge-base/studynote/09_security/13_secops_ir_forensics/627_normalization/)
628. [상관 분석](/knowledge-base/studynote/09_security/13_secops_ir_forensics/628_correlation_analysis/) (Correlation) — 이벤트 간 [관계](/knowledge-base/studynote/09_security/13_secops_ir_forensics/628_correlation_analysis/) 탐지
629. [UEBA in SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/629_ueba_in_siem/) — 행동 분석 기반 [이상 탐지](/knowledge-base/studynote/09_security/13_secops_ir_forensics/629_ueba_in_siem/)
630. [Splunk](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/) — Enterprise [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/)
631. [Elastic SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/631_elastic_siem/) — [Elasticsearch](/knowledge-base/studynote/09_security/13_secops_ir_forensics/631_elastic_siem/) 기반
632. [QRadar](/knowledge-base/studynote/09_security/13_secops_ir_forensics/632_qradar/) — IBM [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/632_qradar/)
633. [ArcSight](/knowledge-base/studynote/09_security/13_secops_ir_forensics/633_arcsight/) — HPE/Micro Focus [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/633_arcsight/)
634. [Graylog](/knowledge-base/studynote/09_security/13_secops_ir_forensics/634_graylog/) — [오픈소스](/knowledge-base/studynote/09_security/13_secops_ir_forensics/634_graylog/) [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/634_graylog/)
635. [Wazuh](/knowledge-base/studynote/09_security/13_secops_ir_forensics/635_wazuh/) — [오픈소스](/knowledge-base/studynote/09_security/13_secops_ir_forensics/635_wazuh/) [SIEM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/635_wazuh/)/[EDR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/635_wazuh/)
636. [SOAR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/636_soar/) ([Security](/knowledge-base/studynote/09_security/13_secops_ir_forensics/636_soar/) [Orchestration](/knowledge-base/studynote/09_security/13_secops_ir_forensics/636_soar/), Automation, Response) — 자동화 대응
637. [플레이북](/knowledge-base/studynote/09_security/13_secops_ir_forensics/637_playbook/) — 시나리오별 자동 대응 절차
638. [보안 자동화](/knowledge-base/studynote/09_security/13_secops_ir_forensics/638_security_automation/) — 반복 작업 자동화
639. [Threat Intelligence](/knowledge-base/studynote/09_security/13_secops_ir_forensics/639_threat_intelligence/) — 위협 정보 공유
640. [TI](/knowledge-base/studynote/09_security/13_secops_ir_forensics/640_ti_types/) 4가지 유형 — [전략](/knowledge-base/studynote/09_security/13_secops_ir_forensics/640_ti_types/)/전술/운영/기술적
641. STIX/TAXII — 위협 정보 교환 표준
642. [MITRE ATT&CK](/knowledge-base/studynote/09_security/13_secops_ir_forensics/642_mitre_attack/) — 공격자 전술/기법/절차DB
643. [ATT&CK Matrix](/knowledge-base/studynote/09_security/13_secops_ir_forensics/643_attack_matrix/) — Pre-ATT&CK/Enterprise/Mobile
644. [Sub-techniques](/knowledge-base/studynote/09_security/13_secops_ir_forensics/644_sub_techniques/) — 세분화된 공격 기법
645. [Cyber Kill Chain](/knowledge-base/studynote/09_security/13_secops_ir_forensics/645_cyber_kill_chain/) — Lockheed Martin 7단계
646. UNC/[APT](/knowledge-base/studynote/09_security/13_secops_ir_forensics/646_unc_apt_groups/) 그룹 — [APT](/knowledge-base/studynote/09_security/13_secops_ir_forensics/646_unc_apt_groups/) 집합 명칭 (MITRE)
647. [Diamond Model](/knowledge-base/studynote/09_security/13_secops_ir_forensics/647_diamond_model/) — 공격 분석 4요소 모델
648. [Pyramid of Pain](/knowledge-base/studynote/09_security/13_secops_ir_forensics/648_pyramid_of_pain/) — 위협 Inteligence 가치 계층
649. [OSINT](/knowledge-base/studynote/09_security/13_secops_ir_forensics/649_osint/) ([Open Source Intelligence](/knowledge-base/studynote/09_security/13_secops_ir_forensics/649_osint/)) — 공개 출처 위협 정보
650. [CVE](/knowledge-base/studynote/09_security/13_secops_ir_forensics/650_cve_cvss/)/[CVSS](/knowledge-base/studynote/09_security/13_secops_ir_forensics/650_cve_cvss/) — 취약점 점수 체계
651. [NVD](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/) ([National Vulnerability Database](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/)) — NIST [CVE](/knowledge-base/studynote/09_security/13_secops_ir_forensics/651_nvd/) DB
652. [인시던트 대응](/knowledge-base/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/) ([IR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/652_incident_response_nist_800_61/)) — NIST 6단계
653. [IR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/) 단계 — 준비/[식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/)/[억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/)/[근절](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/)/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/)/[교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/653_ir_phases/)
654. [IR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/654_ir_preparation/) 준비 — 대응 계획, 팀 구성, 교육
655. [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) — 모니터링/알람->초보 분석
656. [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) ([Containment](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)) — 단기([isolation](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/))/장기(정상운영 복귀)
657. [근절](/knowledge-base/studynote/09_security/13_secops_ir_forensics/657_ir_eradication/) ([Eradication](/knowledge-base/studynote/09_security/13_secops_ir_forensics/657_ir_eradication/)) — 감염 원인 제거
658. [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) — 시스템 정상화, 운영 재개
659. [교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/) ([Lessons Learned](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)) — 후속 조치, 보고서 작성
660. [tabletop exercise](/knowledge-base/studynote/09_security/13_secops_ir_forensics/660_tabletop_exercise/) —탁상연습, 시나리오 기반 연습
661. [DFIR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/661_dfir/) (Digital Forensics and [Incident Response](/knowledge-base/studynote/09_security/13_secops_ir_forensics/661_dfir/)) — 디지털 포렌식+[IR](/knowledge-base/studynote/09_security/13_secops_ir_forensics/661_dfir/)
662. [포렌식 4원칙](/knowledge-base/studynote/09_security/13_secops_ir_forensics/662_forensics_4_principles/) — 순수성/재현성/[검증](/knowledge-base/studynote/09_security/13_secops_ir_forensics/662_forensics_4_principles/)/객관성
663. [증거 보전](/knowledge-base/studynote/09_security/13_secops_ir_forensics/663_evidence_preservation/) —write blocker, [integrity](/knowledge-base/studynote/09_security/13_secops_ir_forensics/663_evidence_preservation/) hashing
664. [Chain of Custody](/knowledge-base/studynote/09_security/13_secops_ir_forensics/664_chain_of_custody/) — 증거 이동/처리 기록
665. [메모리 포렌식](/knowledge-base/studynote/09_security/13_secops_ir_forensics/665_memory_forensics/) — Volatility, Rekall
666. [RAM Dump](/knowledge-base/studynote/09_security/13_secops_ir_forensics/666_ram_dump/) — 물리 메모리 덤프
667. [페이지 파일 분석](/knowledge-base/studynote/09_security/13_secops_ir_forensics/667_pagefile_hiberfil_analysis/) — pagefile.sys, hiberfil.sys
668. [네트워크 포렌식](/knowledge-base/studynote/09_security/13_secops_ir_forensics/668_network_forensics/) — PCAP, [NetFlow](/knowledge-base/studynote/09_security/13_secops_ir_forensics/668_network_forensics/), [DNS](/knowledge-base/studynote/09_security/13_secops_ir_forensics/668_network_forensics/) [로그](/knowledge-base/studynote/09_security/13_secops_ir_forensics/668_network_forensics/)
669. [로그 보전](/knowledge-base/studynote/09_security/13_secops_ir_forensics/669_log_preservation/) — [syslog](/knowledge-base/studynote/09_security/13_secops_ir_forensics/669_log_preservation/), Windows Event, [Firewall](/knowledge-base/studynote/09_security/13_secops_ir_forensics/669_log_preservation/) [로그](/knowledge-base/studynote/09_security/13_secops_ir_forensics/669_log_preservation/)
670. [타임라인 분석](/knowledge-base/studynote/09_security/13_secops_ir_forensics/670_timeline_analysis/) — 이벤트 시간순 재구성
671. MFT 분석 — Windows NTFS [메타데이터](/knowledge-base/studynote/09_security/13_secops_ir_forensics/671_mft_analysis/)
672. [레지스트리 분석](/knowledge-base/studynote/09_security/13_secops_ir_forensics/672_registry_analysis/) — NTUSER.DAT, SAM, [SECURITY](/knowledge-base/studynote/09_security/13_secops_ir_forensics/672_registry_analysis/) [hive](/knowledge-base/studynote/09_security/13_secops_ir_forensics/672_registry_analysis/)
673. [스텔스 기법](/knowledge-base/studynote/09_security/13_secops_ir_forensics/673_stealth_techniques/) — [anti-forensics](/knowledge-base/studynote/09_security/13_secops_ir_forensics/673_stealth_techniques/), [로그](/knowledge-base/studynote/09_security/13_secops_ir_forensics/673_stealth_techniques/) 삭제
674. [anti-forensics](/knowledge-base/studynote/09_security/13_secops_ir_forensics/674_anti_forensics/) — 증거 인멸/변조 기술
675. 취약점 スキャン — Nessus, OpenVAS, Qualys
676. [침투 테스트](/knowledge-base/studynote/09_security/13_secops_ir_forensics/676_penetration_testing/) — 합법적 해킹 시뮬레이션
677. [PTES](/knowledge-base/studynote/09_security/13_secops_ir_forensics/677_ptes/) — [Penetration Testing](/knowledge-base/studynote/09_security/13_secops_ir_forensics/677_ptes/) Execution Standard
678. [OWASP Testing Guide](/knowledge-base/studynote/09_security/13_secops_ir_forensics/678_owasp_testing_guide/) — 웹 앱 테스트 가이드
679. [OSSTMM](/knowledge-base/studynote/09_security/13_secops_ir_forensics/679_osstmm/) — 보안 테스트 방법론
680. [버그 바운티](/knowledge-base/studynote/09_security/13_secops_ir_forensics/680_bug_bounty/) — 공개 취약점 보상 프로그램

---

## 14. 보안 운영 심화 / [위협 헌팅](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/689_threat_hunting/) — 40개

681. [레드팀](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/681_red_team/) — 적대적 관점, 실제 공격 시뮬레이션
682. [블루팀](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/682_blue_team/) — 방어 관점, 탐지/대응
683. [퍼플팀](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/683_purple_team/) — 레드+블루 협력
684. [White Team](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/684_white_team/) — 시나리오 관리/심사
685. [적대적 시뮬레이션](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/685_adversarial_simulation/) — [Red Team](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/685_adversarial_simulation/) vs [Purple Team](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/685_adversarial_simulation/) exercises
686. [가정 침투](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/686_assumed_breach/) ([Assumed Breach](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/686_assumed_breach/)) — 내부 접근 가정
687. [BAS](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/687_bas/) (Breach and Attack Simulation) — 자동화된 공격 시뮬레이션
688. [Purple Team](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/688_purple_team_collaboration/) — 공격/방어 협력, 탐지 규칙 개선
689. [위협 헌팅](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/689_threat_hunting/) ([Threat Hunting](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/689_threat_hunting/)) — 가설 기반 선제적 탐색
690. Huntington 가설 — "공격자는 이미 내부에 있다"
691. [Hunting Loop](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/691_hunting_loop/) —가설/탐색/발견/정보 공유
692. [MITRE Engage](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/692_mitre_engage/) — 방어적 사이버 [전략](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/692_mitre_engage/) 프레임워크
693. [Deception Technology](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/693_deception_technology/) —밀관/밀망/ [canary token](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/693_deception_technology/)
694. [Honey Pot](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/694_honey_pot/) — 유인 시스템
695. [Honey Net](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/695_honey_net/) — 유인 네트워크 세그먼트
696. [Canary Token](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/696_canary_token/) — 조기 탐지용 경보
697. [파일](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/697_file_canary/) [canary](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/697_file_canary/) — 조기 침해 탐지
698. 브라우저 [canary](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/698_browser_canary/) — [세션](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/698_browser_canary/) 탈취 탐지
699. [포렌식 이미지](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/699_forensic_image/) — [DD](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/699_forensic_image/), FTK Imager
700. [MD5](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/700_evidence_integrity_hash/)/SHA-256 해시 — 증거 [무결성](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/700_evidence_integrity_hash/) [검증](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/700_evidence_integrity_hash/)
701. FTK / EnCase — 포렌식 도구
702. [AXIOM](/knowledge-base/studynote/09_security/uncategorized/702_biometric_authentication/) — [Magnet Forensics](/knowledge-base/studynote/09_security/uncategorized/702_biometric_authentication/) 포렌식
703. UAC요과 — 사용자 계정 컨트롤 우회
704. LSASS 추출 — [Mimikatz](/knowledge-base/studynote/09_security/uncategorized/704_mfa_authentication/), procdump
705. [SAM hive](/knowledge-base/studynote/09_security/uncategorized/705_kerberos_authentication/) 추출 — [reg save](/knowledge-base/studynote/09_security/uncategorized/705_kerberos_authentication/) HKLM\SAM
706. [Kerberoasting](/knowledge-base/studynote/09_security/uncategorized/706_oauth_saml/) — SPN 요청 티켓 hash 추출
707. [AS-REP Roasting](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/707_asrep_roasting/) — 사전 [인증](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/707_asrep_roasting/) 미사용 계정 공격
708. [DCSync](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/708_dcsync/) — DC에서 크리덴셜Replication 요청
709. NTDS.dit 추출 — DC [데이터베이스](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/709_ntds_dit/) 직접 추출
710. [BloodHound](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/710_bloodhound/) — AD 공격 경로 분석 도구
711. [CrackMapExec](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/711_crackmapexec/) — 네트워크 크리덴셜 공격 도구
712. [Empire](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/712_empire/) / PowerShell [Empire](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/712_empire/) — 포스트-침투 프레임워크
713. [Cobalt Strike](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/713_cobalt_strike/) — 상업용 [침투 테스트](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/713_cobalt_strike/) 도구
714. [Sliver](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/714_sliver/) — [오픈소스](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/714_sliver/) [C2](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/714_sliver/) 프레임워크
715. [Caldera](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/715_caldera/) — MITRE 자동화 [적대적 시뮬레이션](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/715_caldera/)
716. [Red Canary](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/716_red_canary/) — [EDR](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/716_red_canary/),위협검출
717. [osquery](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/717_osquery/) —Endpoint [시각화](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/717_osquery/)/[쿼리](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/717_osquery/)
718. Sysmon — Windows 시스템 모니터링
719. [Zeek](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/719_kape/) — 네트워크 트래픽 분석
720. YARA — 악성코드 패턴 규칙

---

## 15. 악성코드 / 공격 기법 — 60개

721. [악성코드 분류](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/) — [바이러스](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/)/웜/[트로이목마](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/)/[랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/)/[스파이웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/)/[루트킷](/knowledge-base/studynote/09_security/15_malware_attack_vectors/721_malware_classification/)
722. [바이러스](/knowledge-base/studynote/09_security/15_malware_attack_vectors/722_virus/) ([Virus](/knowledge-base/studynote/09_security/15_malware_attack_vectors/722_virus/)) — 정상 [파일](/knowledge-base/studynote/09_security/15_malware_attack_vectors/722_virus/)에감염, 자기 [복제](/knowledge-base/studynote/09_security/15_malware_attack_vectors/722_virus/)
723. 웹orm — 네트워크 통해 само[복제](/knowledge-base/studynote/09_security/15_malware_attack_vectors/723_worm/), 독립 실행
724. [네트워크 웜](/knowledge-base/studynote/09_security/15_malware_attack_vectors/724_network_worm/) — 취약점 직접 침투 ([Code](/knowledge-base/studynote/09_security/15_malware_attack_vectors/724_network_worm/) Red, SQL Slammer)
725. [이메일 웜](/knowledge-base/studynote/09_security/15_malware_attack_vectors/725_email_worm/) — 메일부건/링크 (ILOVEYOU)
726. [트로이목마](/knowledge-base/studynote/09_security/15_malware_attack_vectors/726_trojan_horse/) — 겉보기에 정상, 실질적으로 악성
727. バックドア — 정상software위장된 후면입구
728. [드롭퍼](/knowledge-base/studynote/09_security/15_malware_attack_vectors/728_dropper/) ([Dropper](/knowledge-base/studynote/09_security/15_malware_attack_vectors/728_dropper/)) — 다단계 [Downloader](/knowledge-base/studynote/09_security/15_malware_attack_vectors/728_dropper/)
729. [Downloader](/knowledge-base/studynote/09_security/15_malware_attack_vectors/729_downloader/) — 원격에서 추가 악성코드 가져옴
730. [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 공격 체인 — [파일](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 암호화 후 몸값
731. [CryptoLocker](/knowledge-base/studynote/09_security/15_malware_attack_vectors/731_cryptolocker/) — 2014년 대규모 [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/731_cryptolocker/)
732. [WannaCry](/knowledge-base/studynote/09_security/15_malware_attack_vectors/732_wannacry/) — 2017년 글로벌, EternalBlue 활용
733. [NotPetya](/knowledge-base/studynote/09_security/15_malware_attack_vectors/733_notpetya/) — 2017년 Ukraine 전력망공격
734. [Ryuk](/knowledge-base/studynote/09_security/15_malware_attack_vectors/734_ryuk/) — 목표형 대규모 [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/734_ryuk/)
735. 이중extortion — 암호화+[데이터](/knowledge-base/studynote/09_security/15_malware_attack_vectors/735_double_extortion/) 유출
736. [RaaS](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/) ([Ransomware](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/) [as](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/) a [Service](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/)) — [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/) 임대 [서비스](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/)
737. [Locker](/knowledge-base/studynote/09_security/15_malware_attack_vectors/737_locker/) — 화면 잠금형 [Ransomware](/knowledge-base/studynote/09_security/15_malware_attack_vectors/737_locker/)
738. wipers — [데이터](/knowledge-base/studynote/09_security/15_malware_attack_vectors/738_wiper/) 파괴 목적
739. [스파이웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/739_spyware/) ([Spyware](/knowledge-base/studynote/09_security/15_malware_attack_vectors/739_spyware/)) — 사용자 활동 감시
740. [키로거](/knowledge-base/studynote/09_security/15_malware_attack_vectors/740_keylogger/) — 키입력 기록
741. 애드웨어 ([Adware](/knowledge-base/studynote/09_security/15_malware_attack_vectors/741_adware/)) — 강제 광고 표시
742. [cryptominer](/knowledge-base/studynote/09_security/15_malware_attack_vectors/742_cryptominer/) — 시스템 자원 활용 암호화폐 채굴
743. [bots](/knowledge-base/studynote/09_security/15_malware_attack_vectors/743_bots/) — 명령 제압력 갖춘 감염 호스트
744. [botnet](/knowledge-base/studynote/09_security/15_malware_attack_vectors/744_botnet/) — 다수의 [bots](/knowledge-base/studynote/09_security/15_malware_attack_vectors/744_botnet/) 집합
745. [botnet](/knowledge-base/studynote/09_security/15_malware_attack_vectors/745_botnet_architecture/) 구조 — 중앙집중형 (C&C)/[P2P](/knowledge-base/studynote/09_security/15_malware_attack_vectors/745_botnet_architecture/)
746. [C2](/knowledge-base/studynote/09_security/15_malware_attack_vectors/746_c2/) ([Command and Control](/knowledge-base/studynote/09_security/15_malware_attack_vectors/746_c2/)) — [봇넷](/knowledge-base/studynote/09_security/15_malware_attack_vectors/746_c2/) 지휘 통제
747. [Cobalt Strike Beacon](/knowledge-base/studynote/09_security/15_malware_attack_vectors/747_cobalt_strike/) — [침투 테스트](/knowledge-base/studynote/09_security/15_malware_attack_vectors/747_cobalt_strike/)용 [C2](/knowledge-base/studynote/09_security/15_malware_attack_vectors/747_cobalt_strike/)
748. [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/) ([Advanced Persistent Threat](/knowledge-base/studynote/09_security/15_malware_attack_vectors/748_apt/)) — 국가/조직적 위협
749. [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/749_apt_groups/) 그룹 — Lazarus(북한국), FIN7(범죄조직), APT29(러시아)
750. [APT](/knowledge-base/studynote/09_security/15_malware_attack_vectors/750_apt_lifecycle/) 공격 단계 — 정찰/침투/내부정찰/횡향이동/유지/[데이터](/knowledge-base/studynote/09_security/15_malware_attack_vectors/750_apt_lifecycle/)반출
751. First [Initial Access](/knowledge-base/studynote/09_security/15_malware_attack_vectors/751_initial_access/) — 최초 침투 수단
752. [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/752_phishing/) ([Phishing](/knowledge-base/studynote/09_security/15_malware_attack_vectors/752_phishing/)) — 가장 일반적인 침투 수단
753. [스피어 피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/753_spear_phishing/) ([Spear Phishing](/knowledge-base/studynote/09_security/15_malware_attack_vectors/753_spear_phishing/)) — 목표 맞춤형
754. [웨일링](/knowledge-base/studynote/09_security/15_malware_attack_vectors/754_whaling/) ([Whaling](/knowledge-base/studynote/09_security/15_malware_attack_vectors/754_whaling/)) — 임원 대상 고대상 [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/754_whaling/)
755. [BEC](/knowledge-base/studynote/09_security/15_malware_attack_vectors/755_bec/) ([Business Email Compromise](/knowledge-base/studynote/09_security/15_malware_attack_vectors/755_bec/)) — 경영자 사칭 금융 사기
756. [스미싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/756_smishing/) ([Smishing](/knowledge-base/studynote/09_security/15_malware_attack_vectors/756_smishing/)) — SMS 기반 [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/756_smishing/)
757. [비싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/757_vishing/) ([Vishing](/knowledge-base/studynote/09_security/15_malware_attack_vectors/757_vishing/)) — 전화 기반 [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/757_vishing/)
758. [사전조사](/knowledge-base/studynote/09_security/15_malware_attack_vectors/758_pretexting/) ([Pretexting](/knowledge-base/studynote/09_security/15_malware_attack_vectors/758_pretexting/)) — 거짓 상황 구성
759. [테일게이팅](/knowledge-base/studynote/09_security/15_malware_attack_vectors/759_tailgating/) ([Tailgating](/knowledge-base/studynote/09_security/15_malware_attack_vectors/759_tailgating/)) — 따라 들어가기
760. [버스딩](/knowledge-base/studynote/09_security/15_malware_attack_vectors/760_busybasing/) ([Busybasing](/knowledge-base/studynote/09_security/15_malware_attack_vectors/760_busybasing/)) —주의력전이
761. [제로데이](/knowledge-base/studynote/09_security/15_malware_attack_vectors/761_zero_day/) — 공개되지 않은 취약점 리용
762. [watering hole](/knowledge-base/studynote/09_security/15_malware_attack_vectors/762_watering_hole/) — 목표 집합 자주 방문 사이트 감염
763. [drive-by download](/knowledge-base/studynote/09_security/15_malware_attack_vectors/763_drive_by_download/) — 악성 사이트 접근만으로 감염
764. 공응련공격 — 소프트웨어 개발망 침해 (SolarWinds)
765. [업데이트 역추적](/knowledge-base/studynote/09_security/15_malware_attack_vectors/765_update_interception/) ([Update Interception](/knowledge-base/studynote/09_security/15_malware_attack_vectors/765_update_interception/)) — 자동갱신 가로채기
766. 다형성 (Polymorphic) — 암호화된 코드,정마 변경
767. 메타모픽 (Metamorphic) — 코드 자체 변환
768. [armored virus](/knowledge-base/studynote/09_security/15_malware_attack_vectors/768_armored_virus/) —정마 회피를 위한 [보호](/knowledge-base/studynote/09_security/15_malware_attack_vectors/768_armored_virus/) 층
769. [파일](/knowledge-base/studynote/09_security/15_malware_attack_vectors/769_fileless_attack/)리스 (Fileless) — 메모리만 사용, [파일](/knowledge-base/studynote/09_security/15_malware_attack_vectors/769_fileless_attack/) 없는 공격
770. [LOLBins](/knowledge-base/studynote/09_security/15_malware_attack_vectors/770_lolbins/) (Living Off the Land) — 정당한 도구 활용
771. PowerShell 공격 — 메모리 내 스크립트 실행
772. WMI 공격 — WMI 이벤트소비자 활용
773. JScript/VBScript 공격 — 스크립트 기반
774. [레지스트리 런키](/knowledge-base/studynote/09_security/15_malware_attack_vectors/774_registry_run_key/) — 자동 실행 등록 정보
775. [예약 작업](/knowledge-base/studynote/09_security/15_malware_attack_vectors/775_scheduled_task/) ([Scheduled Task](/knowledge-base/studynote/09_security/15_malware_attack_vectors/775_scheduled_task/)) — 정기적 실행
776. [서비스](/knowledge-base/studynote/09_security/15_malware_attack_vectors/776_rootkit/) 등록 — Windows [서비스](/knowledge-base/studynote/09_security/15_malware_attack_vectors/776_rootkit/)로잠복
777. [DNS](/knowledge-base/studynote/09_security/15_malware_attack_vectors/777_dns_tunneling/) [터널링](/knowledge-base/studynote/09_security/15_malware_attack_vectors/777_dns_tunneling/) — [DNS](/knowledge-base/studynote/09_security/15_malware_attack_vectors/777_dns_tunneling/) [프로토콜](/knowledge-base/studynote/09_security/15_malware_attack_vectors/777_dns_tunneling/) 내 [데이터](/knowledge-base/studynote/09_security/15_malware_attack_vectors/777_dns_tunneling/) 반출
778. [ICMP](/knowledge-base/studynote/09_security/15_malware_attack_vectors/778_icmp_tunneling/) [터널링](/knowledge-base/studynote/09_security/15_malware_attack_vectors/778_icmp_tunneling/) — [ICMP](/knowledge-base/studynote/09_security/15_malware_attack_vectors/778_icmp_tunneling/) 패킷 내 [데이터](/knowledge-base/studynote/09_security/15_malware_attack_vectors/778_icmp_tunneling/) 운반
779. [HTTPS](/knowledge-base/studynote/09_security/15_malware_attack_vectors/779_https_reverse_relay/) 역투명 relay — 내부망 통신 외부로
780. [동적 프록시](/knowledge-base/studynote/09_security/15_malware_attack_vectors/780_dynamic_proxy/) — 감염 호스트를 Proxy로 활용

---

## 16. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) / [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) — 55개

781. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) ([Personal Information](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)) — 재식별 가능 정보
782. [민감정보](/knowledge-base/studynote/09_security/16_data_privacy/782_sensitive_information/) — 건강/범죄기록/유전정보/ biometric
783. [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) (한국) — 수집/처리/제공/파기 원칙
784. [개인정보 3대 원칙](/knowledge-base/studynote/09_security/16_data_privacy/784_privacy_3_principles/) — 수집 제한/목적 명확/보유 기간
785. [개인정보 영향평가](/knowledge-base/studynote/09_security/16_data_privacy/785_pia_process/) ([PIA](/knowledge-base/studynote/09_security/16_data_privacy/785_pia_process/)) — 고위험 처리전 평가
786. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/786_standard_protection_guideline/) [파일](/knowledge-base/studynote/09_security/16_data_privacy/786_standard_protection_guideline/) 표준 [protection](/knowledge-base/studynote/09_security/16_data_privacy/786_standard_protection_guideline/) 지침 — 한국 [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/786_standard_protection_guideline/) 시행규칙
787. 정보보호 관리체계 ([ISMS-P](/knowledge-base/studynote/09_security/16_data_privacy/787_isms_p/)) — 한국 통합 [인증](/knowledge-base/studynote/09_security/16_data_privacy/787_isms_p/)
788. [정보통신서비스](/knowledge-base/studynote/09_security/16_data_privacy/788_isp_obligations/)제공자 ([ISP](/knowledge-base/studynote/09_security/16_data_privacy/788_isp_obligations/)) — 한국법상 의무
789. 리용약관 — [서비스](/knowledge-base/studynote/09_security/16_data_privacy/789_terms_of_use/) 제공을 위한 기본 계약
790. [동의 방식](/knowledge-base/studynote/09_security/16_data_privacy/790_consent_methods/) — 필수 동의/선택 동의
791. [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) (EU General [Data](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [Protection](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) Regulation) — 2018 시행
792. [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/792_gdpr_legal_bases/) 6가지 처리 근거나유 — 동의/계약/법적 의무/생명 [보호](/knowledge-base/studynote/09_security/16_data_privacy/792_gdpr_legal_bases/)/공익/정당한 이해관계
793. [정보 주체 권리](/knowledge-base/studynote/09_security/16_data_privacy/793_data_subject_rights/) — 접근/정정/삭제/처리 제한/이동/거부
794. Right to be Forgotten — 삭제권 ([GDPR](/knowledge-base/studynote/09_security/16_data_privacy/794_right_to_be_forgotten/) 17조)
795. [Data Portability](/knowledge-base/studynote/09_security/16_data_privacy/795_data_portability/) — 이동권 ([GDPR](/knowledge-base/studynote/09_security/16_data_privacy/795_data_portability/) 20조)
796. [DPIA](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) ([Data](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) [Protection](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) Impact Assessment) — [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/796_gdpr_dpia/) 의무
797. [DPO](/knowledge-base/studynote/09_security/16_data_privacy/797_gdpr_dpo/) ([Data Protection Officer](/knowledge-base/studynote/09_security/16_data_privacy/797_gdpr_dpo/)) — [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/797_gdpr_dpo/) [보호](/knowledge-base/studynote/09_security/16_data_privacy/797_gdpr_dpo/)관
798. [Breach Notification](/knowledge-base/studynote/09_security/16_data_privacy/798_breach_notification/) — 72시간 내 신고 의무
799. [개인정보 해외 이전](/knowledge-base/studynote/09_security/16_data_privacy/799_cross_border_data_transfer/) — 충분성 인정 국가/표준 계약 조항
800. [CCPA](/knowledge-base/studynote/09_security/16_data_privacy/800_ccpa/) (California Consumer Privacy Act) — 2020 시행
801. [CPRA](/knowledge-base/studynote/09_security/16_data_privacy/801_cpra/) (California Privacy Rights Act) — [CCPA](/knowledge-base/studynote/09_security/16_data_privacy/801_cpra/) 강화
802. [PDPA](/knowledge-base/studynote/09_security/16_data_privacy/802_pdpa/) (Personal [Data](/knowledge-base/studynote/09_security/16_data_privacy/802_pdpa/) [Protection](/knowledge-base/studynote/09_security/16_data_privacy/802_pdpa/) Act) — 싱가포르
803. [개인정보보호](/knowledge-base/studynote/09_security/16_data_privacy/803_privacy_law_comparison/) 법률체계 — 한국/미국/EU 비교
804. [ISMS-P](/knowledge-base/studynote/09_security/16_data_privacy/804_isms_p_audit/) 심사 — 기술적/관리적/물리적 안전 Control 평가
805. [정보보호 주요](/knowledge-base/studynote/09_security/16_data_privacy/805_security_measures/)안전관리 —
806. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/806_incident_response/) 유출 사고 — 신고/통지/공표 의무
807. 과태료/벌칙 — 한국 [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/807_penalties_fines/) 제64조
808. [데이터 분류](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/) — 공개/내부/기밀/극비
809. [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) — 국가별 [데이터](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/)본지화 법규
810. [데이터](/knowledge-base/studynote/09_security/16_data_privacy/810_data_localization/) 이동 — Cross-border [데이터](/knowledge-base/studynote/09_security/16_data_privacy/810_data_localization/) 흐름
811. [클라우드 개인정보보호](/knowledge-base/studynote/09_security/16_data_privacy/811_privacy_in_cloud/) — [데이터](/knowledge-base/studynote/09_security/16_data_privacy/811_privacy_in_cloud/) 소재지 주의
812. [데이터](/knowledge-base/studynote/09_security/16_data_privacy/812_anonymization/)닉명화 — 완전히 역추적 불가능
813. [데이터](/knowledge-base/studynote/09_security/16_data_privacy/813_pseudonymization/)가명화 — [식별](/knowledge-base/studynote/09_security/16_data_privacy/813_pseudonymization/)가능성 제거,pseudo-anonymization
814. [k-익명성](/knowledge-base/studynote/09_security/16_data_privacy/814_k_anonymity/) — k-person indistinguishability
815. [l-다양성](/knowledge-base/studynote/09_security/16_data_privacy/815_l_diversity/) — 민감 [속성](/knowledge-base/studynote/09_security/16_data_privacy/815_l_diversity/) 다변화
816. [t-근접성](/knowledge-base/studynote/09_security/16_data_privacy/816_t_closeness/) — 레코드 분포 유사성
817. [차분 개인정보보호](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/) — [differential privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/)
818. [합성 데이터](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/) — [Synthetic data](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/) [생성](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/)
819. [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/) — 동적/정적 마스킹
820. [토큰화](/knowledge-base/studynote/09_security/16_data_privacy/820_tokenization/) ([Tokenization](/knowledge-base/studynote/09_security/16_data_privacy/820_tokenization/)) — 원본↔토큰 매핑
821. TTT ([Tokenization-as-a-Service](/knowledge-base/studynote/09_security/16_data_privacy/821_taas/)) — 클라우드 [토큰화](/knowledge-base/studynote/09_security/16_data_privacy/821_taas/)
822. [Format Preserving Encryption](/knowledge-base/studynote/09_security/16_data_privacy/822_fpe/) — [FPE](/knowledge-base/studynote/09_security/16_data_privacy/822_fpe/), 원 [데이터](/knowledge-base/studynote/09_security/16_data_privacy/822_fpe/) 형식 유지
823. [DLP](/knowledge-base/studynote/09_security/16_data_privacy/823_dlp/) ([Data Loss Prevention](/knowledge-base/studynote/09_security/16_data_privacy/823_dlp/)) — [데이터](/knowledge-base/studynote/09_security/16_data_privacy/823_dlp/) 반출 방지
824. [DLP](/knowledge-base/studynote/09_security/16_data_privacy/824_dlp_components/) 구성요소 —엔진/에이전트/서버
825. [DLP](/knowledge-base/studynote/09_security/16_data_privacy/825_dlp_policy/) [정책](/knowledge-base/studynote/09_security/16_data_privacy/825_dlp_policy/) — 콘텐츠 검사/[컨텍스트](/knowledge-base/studynote/09_security/16_data_privacy/825_dlp_policy/) 기반
826. 네트워크 [DLP](/knowledge-base/studynote/09_security/16_data_privacy/826_network_dlp/) — 네트워크 경계 [데이터](/knowledge-base/studynote/09_security/16_data_privacy/826_network_dlp/) 통제
827. 엔드포인트 [DLP](/knowledge-base/studynote/09_security/16_data_privacy/827_endpoint_dlp/) — 단말기 내 [데이터](/knowledge-base/studynote/09_security/16_data_privacy/827_endpoint_dlp/) 통제
828. 클라우드 [DLP](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/) — [SaaS](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/)/ [PaaS](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/)/[IaaS](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/) [데이터](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/) [보호](/knowledge-base/studynote/09_security/16_data_privacy/828_cloud_dlp/)
829. [CASB](/knowledge-base/studynote/09_security/16_data_privacy/829_casb/) (Cloud Access [Security](/knowledge-base/studynote/09_security/16_data_privacy/829_casb/) Broker) — 클라우드 가시성/제어
830. [데이터베이스 보안](/knowledge-base/studynote/09_security/16_data_privacy/830_db_security/) — [접근 통제](/knowledge-base/studynote/09_security/16_data_privacy/830_db_security/)/암호화/[감사](/knowledge-base/studynote/09_security/16_data_privacy/830_db_security/)
831. [필드 레벨 보안](/knowledge-base/studynote/09_security/16_data_privacy/831_field_level_security/) — DB 컬럼/행 수준 접근 제어
832. DB [감사](/knowledge-base/studynote/09_security/16_data_privacy/832_database_auditing/) — 접속 기록, 질의 [로그](/knowledge-base/studynote/09_security/16_data_privacy/832_database_auditing/)
833. [전송 중 암호화](/knowledge-base/studynote/09_security/16_data_privacy/833_encryption_in_transit/) — [TLS](/knowledge-base/studynote/09_security/16_data_privacy/833_encryption_in_transit/), [IPsec](/knowledge-base/studynote/09_security/16_data_privacy/833_encryption_in_transit/)
834. [저장 중 암호화](/knowledge-base/studynote/09_security/16_data_privacy/834_encryption_at_rest/) — [TDE](/knowledge-base/studynote/09_security/16_data_privacy/834_encryption_at_rest/), 디스크 암호화
835. [메모리 내 암호화](/knowledge-base/studynote/09_security/16_data_privacy/835_encryption_in_use/) — 클라우드 [HSM](/knowledge-base/studynote/09_security/16_data_privacy/835_encryption_in_use/)

---

## 17. 보안 프레임워크 / 컴플라이언스 — 55개

836. ISO/IEC 27001 — 정보보안 [management](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) 시스템 ([ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/))
837. [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/837_isms_certification_process/) [인증](/knowledge-base/studynote/09_security/17_framework_compliance/837_isms_certification_process/) — 3자 [감사](/knowledge-base/studynote/09_security/17_framework_compliance/837_isms_certification_process/), [인증](/knowledge-base/studynote/09_security/17_framework_compliance/837_isms_certification_process/)서 발급
838. [PDCA](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/) ([Plan-Do-Check-Act](/knowledge-base/studynote/09_security/17_framework_compliance/838_pdca_model/)) — 관리 시스템 적용 모델
839. ISO 27001 114개 통제 — Annex A
840. ISO/IEC 27002 — 보안 통제 implementation 지침
841. ISO/IEC 27005 — 정보보안 위험 관리
842. [ISO 27017](/knowledge-base/studynote/09_security/17_framework_compliance/842_iso_27017_cloud_security/) — 클라우드 [서비스](/knowledge-base/studynote/09_security/17_framework_compliance/842_iso_27017_cloud_security/) 보안 통제
843. [ISO 27018](/knowledge-base/studynote/09_security/17_framework_compliance/843_iso_27018_cloud_pii/) — 클라우드 PII [보호](/knowledge-base/studynote/09_security/17_framework_compliance/843_iso_27018_cloud_pii/)
844. [ISO 27701](/knowledge-base/studynote/09_security/17_framework_compliance/844_iso_27701_pims/) — [개인정보보호](/knowledge-base/studynote/09_security/17_framework_compliance/844_iso_27701_pims/) 정보안전관리
845. [ISO 22301](/knowledge-base/studynote/09_security/17_framework_compliance/845_iso_22301_bcms/) — 사업 연속성 관리 시스템 ([BCMS](/knowledge-base/studynote/09_security/17_framework_compliance/845_iso_22301_bcms/))
846. NIST [CSF](/knowledge-base/studynote/09_security/17_framework_compliance/846_nist_csf_2_0/) 2.0 —Identify/Protect/Detect/Respond/Recover + Govern
847. [NIST CSF Tier](/knowledge-base/studynote/09_security/17_framework_compliance/847_nist_csf_tier/) — [Risk](/knowledge-base/studynote/09_security/17_framework_compliance/847_nist_csf_tier/) Inform/Repeatable/Adaptive
848. [NIST SP 800-53](/knowledge-base/studynote/09_security/17_framework_compliance/848_nist_sp_800_53/) — 연방 정보시스템 보안 통제 (800+ 통제)
849. [NIST SP 800-171](/knowledge-base/studynote/09_security/17_framework_compliance/849_nist_sp_800_171/) — CUI [보호](/knowledge-base/studynote/09_security/17_framework_compliance/849_nist_sp_800_171/) (110 통제)
850. [NIST SP 800-207](/knowledge-base/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/) — [제로 트러스트 아키텍처](/knowledge-base/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/)
851. [NIST SP 800-63](/knowledge-base/studynote/09_security/17_framework_compliance/851_nist_sp_800_63/) — 디지털 신원 지침
852. [NIST SP 800-63A](/knowledge-base/studynote/09_security/17_framework_compliance/852_nist_sp_800_63a/) — Enrollment and Identity Proofing
853. [NIST SP 800-63B](/knowledge-base/studynote/09_security/17_framework_compliance/853_nist_sp_800_63b/) — [Authentication](/knowledge-base/studynote/09_security/17_framework_compliance/853_nist_sp_800_63b/) and Lifecycle
854. [NIST SP 800-63C](/knowledge-base/studynote/09_security/17_framework_compliance/854_nist_sp_800_63c/) — [Federation](/knowledge-base/studynote/09_security/17_framework_compliance/854_nist_sp_800_63c/) and Assertions
855. [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/855_soc_2/) — AICPA [서비스](/knowledge-base/studynote/09_security/17_framework_compliance/855_soc_2/) 조직 통제 보고서
856. [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/856_soc_2_trust_service_criteria/) Trust [Service](/knowledge-base/studynote/09_security/17_framework_compliance/856_soc_2_trust_service_criteria/) Criteria — 보안/[가용성](/knowledge-base/studynote/09_security/17_framework_compliance/856_soc_2_trust_service_criteria/)/처리 [무결성](/knowledge-base/studynote/09_security/17_framework_compliance/856_soc_2_trust_service_criteria/)/궤밀성/은사
857. [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/857_soc_2_type_i_ii/) Type I/II — 설계 적정성/운영 효과성
858. [SOC 3](/knowledge-base/studynote/09_security/17_framework_compliance/858_soc_3/) — 공용 [버전](/knowledge-base/studynote/09_security/17_framework_compliance/858_soc_3/) [SOC 2](/knowledge-base/studynote/09_security/17_framework_compliance/858_soc_3/)
859. [PCI](/knowledge-base/studynote/09_security/17_framework_compliance/859_pci_dss_v4_0/) DSS v4.0 — Payment Card Industry [Data](/knowledge-base/studynote/09_security/17_framework_compliance/859_pci_dss_v4_0/) [Security](/knowledge-base/studynote/09_security/17_framework_compliance/859_pci_dss_v4_0/) Standard
860. [PCI](/knowledge-base/studynote/09_security/17_framework_compliance/860_pci_dss_12_requirements/) DSS 12개 요구사항 — [방화벽](/knowledge-base/studynote/09_security/17_framework_compliance/860_pci_dss_12_requirements/)/비밀번호/[데이터](/knowledge-base/studynote/09_security/17_framework_compliance/860_pci_dss_12_requirements/) [보호](/knowledge-base/studynote/09_security/17_framework_compliance/860_pci_dss_12_requirements/) 등
861. [PCI](/knowledge-base/studynote/09_security/17_framework_compliance/861_pci_dss_compliance_levels/) DSS 수준 —merchant/[service provider](/knowledge-base/studynote/09_security/17_framework_compliance/861_pci_dss_compliance_levels/) 등급
862. [PA-DSS](/knowledge-base/studynote/09_security/17_framework_compliance/862_pa_dss/) — Payment Application [Data](/knowledge-base/studynote/09_security/17_framework_compliance/862_pa_dss/) [Security](/knowledge-base/studynote/09_security/17_framework_compliance/862_pa_dss/) Standard
863. [HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/) — 미국 의료정보 [보호](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/)법
864. [PHI](/knowledge-base/studynote/09_security/17_framework_compliance/864_phi/) ([Protected Health Information](/knowledge-base/studynote/09_security/17_framework_compliance/864_phi/)) — [HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/864_phi/) 적용 정보
865. [HITECH](/knowledge-base/studynote/09_security/17_framework_compliance/865_hitech/) — 미국 의료기술법, 위반 시 책임 강화
866. [GLBA](/knowledge-base/studynote/09_security/17_framework_compliance/866_glba/) ([Gramm-Leach-Bliley Act](/knowledge-base/studynote/09_security/17_framework_compliance/866_glba/)) — 미국 금융정보보호
867. [FERPA](/knowledge-base/studynote/09_security/17_framework_compliance/867_ferpa/) — 미국 교육 기록 프라이버시
868. [CMMC](/knowledge-base/studynote/09_security/17_framework_compliance/868_cmmc/) (Cybersecurity [Maturity Model](/knowledge-base/studynote/09_security/17_framework_compliance/868_cmmc/) Certification) — 미국 방위산업
869. [CMMC](/knowledge-base/studynote/09_security/17_framework_compliance/869_cmmc_levels/) 5단계 — Level 1~5 점진적 [인증](/knowledge-base/studynote/09_security/17_framework_compliance/869_cmmc_levels/)
870. [FISMA](/knowledge-base/studynote/09_security/17_framework_compliance/870_fisma/) — 미국 연방 정보 보안 법
871. [FedRAMP](/knowledge-base/studynote/09_security/17_framework_compliance/871_fedramp/) — 미국 정부 클라우드 보안 [인증](/knowledge-base/studynote/09_security/17_framework_compliance/871_fedramp/)
872. [FedRAMP](/knowledge-base/studynote/09_security/17_framework_compliance/872_fedramp_impact_levels/) Moderate/High — 영향 수준별 기준
873. ITGrc — IT 거버넌스/[리스크](/knowledge-base/studynote/09_security/17_framework_compliance/873_it_grc/)/컴플라이언스
874. [SABSA](/knowledge-base/studynote/09_security/17_framework_compliance/874_sabsa/) —Business-driven [보안 아키텍처](/knowledge-base/studynote/09_security/17_framework_compliance/874_sabsa/)
875. [TOGAF](/knowledge-base/studynote/09_security/17_framework_compliance/875_togaf/) — 기업 아키텍처 프레임워크
876. [Zachman Framework](/knowledge-base/studynote/09_security/17_framework_compliance/876_zachman_framework/) — [EA](/knowledge-base/studynote/09_security/17_framework_compliance/876_zachman_framework/) planning 매트릭스
877. [CIS Controls v8](/knowledge-base/studynote/09_security/17_framework_compliance/877_cis_controls_v8/) — 18개 핵심 보안 통제
878. [CIS Safeguard](/knowledge-base/studynote/09_security/17_framework_compliance/878_cis_safeguard/) — Implement/M측량/관리
879. [COBIT 2019](/knowledge-base/studynote/09_security/17_framework_compliance/879_cobit_2019/) — IT 거버넌스 프레임워크
880. [ITIL](/knowledge-base/studynote/09_security/17_framework_compliance/880_itil/) (Information Technology Infrastructure [Library](/knowledge-base/studynote/09_security/17_framework_compliance/880_itil/)) — IT [서비스](/knowledge-base/studynote/09_security/17_framework_compliance/880_itil/) 관리
881. [Privacy by Design](/knowledge-base/studynote/09_security/17_framework_compliance/881_privacy_by_design/) — 설계 단계 [개인정보](/knowledge-base/studynote/09_security/17_framework_compliance/881_privacy_by_design/) [보호](/knowledge-base/studynote/09_security/17_framework_compliance/881_privacy_by_design/)
882. [PbD](/knowledge-base/studynote/09_security/17_framework_compliance/882_pbd_7_foundational_principles/) 7기본원칙 — 사전 [보호](/knowledge-base/studynote/09_security/17_framework_compliance/882_pbd_7_foundational_principles/)/기본값사밀성 등
883. [CC](/knowledge-base/studynote/09_security/17_framework_compliance/883_common_criteria_iso_15408/) ([Common Criteria](/knowledge-base/studynote/09_security/17_framework_compliance/883_common_criteria_iso_15408/)) / ISO 15408 — 제품 보안 [인증](/knowledge-base/studynote/09_security/17_framework_compliance/883_common_criteria_iso_15408/)
884. [CC EAL](/knowledge-base/studynote/09_security/17_framework_compliance/884_cc_eal_evaluation_assurance_levels/) — 평가 보증 수준 (EAL 1~7)
885. FIPS 140-2/3 — 암호 [모듈](/knowledge-base/studynote/09_security/17_framework_compliance/885_fips_140_3_cryptographic_module/) 보안 표준
886. [K-ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/886_k_isms/) — 한국 정보보호관리체계 [인증](/knowledge-base/studynote/09_security/17_framework_compliance/886_k_isms/)
887. [정보보호평가](/knowledge-base/studynote/09_security/17_framework_compliance/887_kisa_assessment/) — 한국호련망진흥원 (KISA)
888. [전자금융감독규정](/knowledge-base/studynote/09_security/17_framework_compliance/888_electronic_financial_supervision_regulation/) — 금융 전산 보안 기준
889. [금융감독원](/knowledge-base/studynote/09_security/17_framework_compliance/889_fss_cyber_supervision/) ([FSS](/knowledge-base/studynote/09_security/17_framework_compliance/889_fss_cyber_supervision/)) — 금융 사이버 감독
890. [SBOM](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/) (Software [Bill of Materials](/knowledge-base/studynote/09_security/17_framework_compliance/890_sbom_cyclonedx_spdx/)) — 소프트웨어 부품 목록

---

## 18. [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) / [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) / [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) / 물리 보안 — 50개

891. [OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/) ([Operational Technology](/knowledge-base/studynote/09_security/18_iot_ot_physical/891_ot_operational_technology/)) — 운영기술, 산업공제시스템
892. [OT vs IT](/knowledge-base/studynote/09_security/18_iot_ot_physical/892_ot_vs_it/) — [reliability](/knowledge-base/studynote/09_security/18_iot_ot_physical/892_ot_vs_it/)/[availability](/knowledge-base/studynote/09_security/18_iot_ot_physical/892_ot_vs_it/)/real-time 차이
893. [ICS](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/) ([Industrial Control System](/knowledge-base/studynote/09_security/18_iot_ot_physical/893_ics_industrial_control_system/)) — 산업 제어 시스템
894. [SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/) (Supervisory Control and [Data](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/) [Acquisition](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/)) — 원격 감시 제어
895. [DCS](/knowledge-base/studynote/09_security/18_iot_ot_physical/895_dcs_distributed_control_system/) ([Distributed Control System](/knowledge-base/studynote/09_security/18_iot_ot_physical/895_dcs_distributed_control_system/)) — [분산](/knowledge-base/studynote/09_security/18_iot_ot_physical/895_dcs_distributed_control_system/) 제어 시스템
896. [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) ([Programmable Logic Controller](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)) — 현장 제어기
897. [RTU](/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/) ([Remote Terminal Unit](/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/)) — 원격 터미널 장치
898. Modbus [프로토콜](/knowledge-base/studynote/09_security/18_iot_ot_physical/898_modbus_protocol/) — 산업용 [직렬](/knowledge-base/studynote/09_security/18_iot_ot_physical/898_modbus_protocol/) 통신, 암호화 없음
899. [DNP3](/knowledge-base/studynote/09_security/18_iot_ot_physical/899_dnp3_distributed_network_protocol/) — 전력/상하수도 [SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/899_dnp3_distributed_network_protocol/) [프로토콜](/knowledge-base/studynote/09_security/18_iot_ot_physical/899_dnp3_distributed_network_protocol/)
900. [PROFINET](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/) — 산업용 [이더넷](/knowledge-base/studynote/09_security/18_iot_ot_physical/900_profinet/)
901. [EtherNet](/knowledge-base/studynote/09_security/18_iot_ot_physical/901_ethernet_ip/)/IP — CIP 기반 산업용 [이더넷](/knowledge-base/studynote/09_security/18_iot_ot_physical/901_ethernet_ip/)
902. Purdue 모델 — IT/[OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/902_purdue_model/) 네트워크 5단계분층
903. Purdue 레벨 0~5 — Field/Level 1~2 ([OT](/knowledge-base/studynote/09_security/18_iot_ot_physical/903_purdue_levels/))/Level 3 ([DMZ](/knowledge-base/studynote/09_security/18_iot_ot_physical/903_purdue_levels/))/Level 4~5 (IT)
904. [IEC 62443](/knowledge-base/studynote/09_security/18_iot_ot_physical/904_iec_62443/) — 산업 사이버보안 표준
905. [ISA](/knowledge-base/studynote/09_security/18_iot_ot_physical/905_iec_62443_security_levels/)/[IEC 62443](/knowledge-base/studynote/09_security/18_iot_ot_physical/905_iec_62443_security_levels/) 보안 레벨 — SL 0~4 (no [security](/knowledge-base/studynote/09_security/18_iot_ot_physical/905_iec_62443_security_levels/)->most secure)
906. [SL-CF](/knowledge-base/studynote/09_security/18_iot_ot_physical/906_sl_cf_capability/) ([Security Level Capability](/knowledge-base/studynote/09_security/18_iot_ot_physical/906_sl_cf_capability/)) — 시설 보안 수준
907. [SL-TF](/knowledge-base/studynote/09_security/18_iot_ot_physical/907_sl_tf_target/) ([Security Level Target](/knowledge-base/studynote/09_security/18_iot_ot_physical/907_sl_tf_target/)) — 목표 보안 수준
908. Zone/Conduit 모델 — 구역 분리+ conduits통제
909. Zone 맵핑 — 자산 [분류](/knowledge-base/studynote/09_security/18_iot_ot_physical/909_zone_mapping/)-> [security](/knowledge-base/studynote/09_security/18_iot_ot_physical/909_zone_mapping/) level
910. [NIST IR 8259](/knowledge-base/studynote/09_security/18_iot_ot_physical/910_nist_ir_8259/) — [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/910_nist_ir_8259/) 보안기초
911. [NIST IR 8259D](/knowledge-base/studynote/09_security/18_iot_ot_physical/911_nist_ir_8259d/) — [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/911_nist_ir_8259d/) 제조 상arangement
912. OWASP [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/912_owasp_iot_top_10/) Top [10](/knowledge-base/studynote/09_security/18_iot_ot_physical/912_owasp_iot_top_10/) — 취약한 [펌웨어](/knowledge-base/studynote/09_security/18_iot_ot_physical/912_owasp_iot_top_10/)/기본 계정/불안전한 접구
913. [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/913_iot_secure_design/) 보안 설계 —[Secure by Default](/knowledge-base/studynote/09_security/18_iot_ot_physical/913_iot_secure_design/), 최소 기능 원칙
914. [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/914_iot_firmware_security/) [펌웨어](/knowledge-base/studynote/09_security/18_iot_ot_physical/914_iot_firmware_security/) 보안 — 서명 [검증](/knowledge-base/studynote/09_security/18_iot_ot_physical/914_iot_firmware_security/), 안전 업데이트
915. [IoT](/knowledge-base/studynote/09_security/18_iot_ot_physical/915_iot_data_security/) [데이터](/knowledge-base/studynote/09_security/18_iot_ot_physical/915_iot_data_security/) 보안 —보존중/전수중/처리중
916. [Secure Boot](/knowledge-base/studynote/09_security/18_iot_ot_physical/916_secure_boot/) — 부팅 과정 소프트웨어 [무결성](/knowledge-base/studynote/09_security/18_iot_ot_physical/916_secure_boot/) [검증](/knowledge-base/studynote/09_security/18_iot_ot_physical/916_secure_boot/)
917. [rantai-root-of-trust](/knowledge-base/studynote/09_security/18_iot_ot_physical/917_root_of_trust/) — 신뢰의 근원
918. RoT 구성요소 — CRTM, [Bootloader](/knowledge-base/studynote/09_security/18_iot_ot_physical/918_rot_components/), [Bootloader](/knowledge-base/studynote/09_security/18_iot_ot_physical/918_rot_components/) certificates
919. [TPM](/knowledge-base/studynote/09_security/18_iot_ot_physical/919_measured_boot/) 원격 증명 ([Remote Attestation](/knowledge-base/studynote/09_security/18_iot_ot_physical/919_measured_boot/)) — [TPM](/knowledge-base/studynote/09_security/18_iot_ot_physical/919_measured_boot/) 측정값을 원격에서 [검증](/knowledge-base/studynote/09_security/18_iot_ot_physical/919_measured_boot/)하는 과정
920. [펌웨어 업데이트 보안](/knowledge-base/studynote/09_security/18_iot_ot_physical/920_firmware_update_security/) —첨명험증, [롤백](/knowledge-base/studynote/09_security/18_iot_ot_physical/920_firmware_update_security/) 방지
921. [MQTT](/knowledge-base/studynote/09_security/18_iot_ot_physical/921_mqtt_security/) 보안 — [TLS](/knowledge-base/studynote/09_security/18_iot_ot_physical/921_mqtt_security/), [인증](/knowledge-base/studynote/09_security/18_iot_ot_physical/921_mqtt_security/), [ACL](/knowledge-base/studynote/09_security/18_iot_ot_physical/921_mqtt_security/)
922. [BACnet](/knowledge-base/studynote/09_security/18_iot_ot_physical/922_bacnet/) — 건물 자동화 [프로토콜](/knowledge-base/studynote/09_security/18_iot_ot_physical/922_bacnet/)
923. ，차량네트워크 보안 — UNECE WP.29
924. ISO/SAE 21434 — [자동차 사이버보안](/knowledge-base/studynote/09_security/18_iot_ot_physical/924_iso_sae_21434/) 엔지니어링
925. [TARA](/knowledge-base/studynote/09_security/18_iot_ot_physical/925_tara/) (Threat Analysis and [Risk](/knowledge-base/studynote/09_security/18_iot_ot_physical/925_tara/) Assessment) — 자동차 위협 분석
926. [의료기기 보안](/knowledge-base/studynote/09_security/18_iot_ot_physical/926_medical_device_security/) — FDA cybersecurity 지침
927. [의료기기 사이버보안 관리](/knowledge-base/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle/) — 디자인 단계부터
928. [스마트 그리드 보안](/knowledge-base/studynote/09_security/18_iot_ot_physical/928_smart_grid_security/) — [AMI](/knowledge-base/studynote/09_security/18_iot_ot_physical/928_smart_grid_security/) 보안
929. [NERC CIP](/knowledge-base/studynote/09_security/18_iot_ot_physical/929_nerc_cip/) — 북미 전력 [신뢰성](/knowledge-base/studynote/09_security/18_iot_ot_physical/929_nerc_cip/) Corporation
930. [원자력 사이버보안](/knowledge-base/studynote/09_security/18_iot_ot_physical/930_nuclear_cybersecurity/) — IAEA 안전기준
931. [위성 통신 보안](/knowledge-base/studynote/09_security/uncategorized/931_emp_protection_faraday_cage_optical_fiber_shielding/) —，항ジャミング/[스푸핑](/knowledge-base/studynote/09_security/uncategorized/931_emp_protection_faraday_cage_optical_fiber_shielding/)
932. 물리적 보안 3대 요소 —위섭/ Delay/ [Detection](/knowledge-base/studynote/09_security/uncategorized/932_sniffing_detection_arp_ping_promiscuous_mode/)
933. [CCTV](/knowledge-base/studynote/09_security/uncategorized/933_packet_fragmentation_offset_overlapping_ids_evasion_defense/) (폐쇄 회로텔레비전) — 영상 감시
934. 접근 제어 시스템 — 카드/RFID/바이오메트릭
935. [Mantrap](/knowledge-base/studynote/09_security/uncategorized/935_rpki_resource_public_key_infrastructure_bgp_hijacking_prevention/) — 이중 문으로 인적 격리
936. [주변 보안](/knowledge-base/studynote/09_security/uncategorized/936_dns_sinkhole_botnet_cnc_blocking_kisa/) — 담장/감시/순사
937. [환경 통제](/knowledge-base/studynote/09_security/uncategorized/937_hybrid_cryptography_symmetric_asymmetric_ssl_pgp/) — 온도/습도/소화기
938. [서버실 보안](/knowledge-base/studynote/09_security/uncategorized/938_file_carving_network_forensics_pcap_signature_recovery/) — Tier 1~4수거중심분급
939. [Faraday Cage](/knowledge-base/studynote/09_security/uncategorized/939_honeypot_deception_technology_cyber_decoy_system/) — 전자기 차폐
940. 금속 탐지기/ X-ray — 물리적협위 탐지

---

## 19. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) / 신기술 보안 — 50개

941. [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/941_ai_security/) 보안 — [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/941_ai_security/) 시스템의 안전+[AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/941_ai_security/) 활용 보안
942. [적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/) ([Adversarial Example](/knowledge-base/studynote/09_security/19_ai_advanced_security/942_adversarial_example/)) — 미세한 perturbation로 오분류
943. [FGSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/943_fgsm/) (Fast Gradient Sign Method) — 1단계 적대적우동
944. [PGD](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/) ([Projected Gradient Descent](/knowledge-base/studynote/09_security/19_ai_advanced_security/944_pgd/)) — 반복적 적대적우동
945. [Carlini-Wagner](/knowledge-base/studynote/09_security/19_ai_advanced_security/945_cw_attack/) 공격 — 강력한 적대적 공격
946. 물리 세계 적대적 공격 — 도로 표지판 등 실환경 공격
947. [데이터 포이즈닝](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/) ([Data Poisoning](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/)) — 훈련 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/947_data_poisoning/) 오염
948. [Clean-Label Poisoning](/knowledge-base/studynote/09_security/19_ai_advanced_security/948_clean_label_poisoning/) — 레이블 유지한 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/948_clean_label_poisoning/) 오염
949. [Backdoor Attack](/knowledge-base/studynote/09_security/19_ai_advanced_security/949_backdoor_attack/) — 특정 [트리거](/knowledge-base/studynote/09_security/19_ai_advanced_security/949_backdoor_attack/) 입력에 반응
950. [모델 추출](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/) ([Model Extraction](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/)) — [쿼리](/knowledge-base/studynote/09_security/19_ai_advanced_security/950_model_extraction/) 기반 모델 역추출
951. [Model Inversion](/knowledge-base/studynote/09_security/19_ai_advanced_security/951_model_inversion/) — 훈련 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/951_model_inversion/) 재구성
952. [Membership Inference](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/) — 특정 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/952_membership_inference/) 훈련 여부 추론
953. [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/953_model_theft/) 모델 탈취 — [API](/knowledge-base/studynote/09_security/19_ai_advanced_security/953_model_theft/) [쿼리](/knowledge-base/studynote/09_security/19_ai_advanced_security/953_model_theft/)로 모델 [복제](/knowledge-base/studynote/09_security/19_ai_advanced_security/953_model_theft/)
954. [모델 무결성 공격](/knowledge-base/studynote/09_security/19_ai_advanced_security/954_model_integrity/) — 사본 배포, 악성 교체
955. [프롬프트 인젝션](/knowledge-base/studynote/09_security/19_ai_advanced_security/955_prompt_injection/) — [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/955_prompt_injection/) 지시어 오버라이드
956. [Jailbreaking](/knowledge-base/studynote/09_security/19_ai_advanced_security/956_jailbreaking/) — [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/956_jailbreaking/) 안전 필터 우회
957. [적대적 프롬프트](/knowledge-base/studynote/09_security/19_ai_advanced_security/957_adversarial_prompting/) — 의도한 잘못된 출력 유도
958. [데이터 추출 공격](/knowledge-base/studynote/09_security/19_ai_advanced_security/958_data_extraction/) — 훈련 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/958_data_extraction/) 기억으로 정보 유출
959. [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/959_ai_phishing/) 기반 [피싱](/knowledge-base/studynote/09_security/19_ai_advanced_security/959_ai_phishing/) — 개인화된 대규모 [피싱](/knowledge-base/studynote/09_security/19_ai_advanced_security/959_ai_phishing/) 자동화
960. [Deepfake](/knowledge-base/studynote/09_security/19_ai_advanced_security/960_deepfake/) — 합성 미디어, 신원 사칭
961. [딥페이크 탐지](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) — [C2PA](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/), 디지털 워터마킹
962. [C2PA](/knowledge-base/studynote/09_security/19_ai_advanced_security/962_c2pa/) (Coalition for Content Provenance and [Authenticity](/knowledge-base/studynote/09_security/19_ai_advanced_security/962_c2pa/)) — 콘텐츠 출처
963. [SynthID](/knowledge-base/studynote/09_security/19_ai_advanced_security/963_synthid/) — Google 딥마크
964. [AI TRiSM](/knowledge-base/studynote/09_security/19_ai_advanced_security/964_ai_trism/) — Gartner, [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/964_ai_trism/) 신뢰/위험/보안 관리
965. [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/965_llm_guardrails/) 가드레일 — 출력 필터링, 안전 레이어
966. [Constitutional AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/966_constitutional_ai/) — 원칙 기반 [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/966_constitutional_ai/) 행동 통제
967. [AI Red Team](/knowledge-base/studynote/09_security/19_ai_advanced_security/967_ai_red_team/) — [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/967_ai_red_team/) 안전성 테스트
968. 대항성훈련 — [적대적 예제](/knowledge-base/studynote/09_security/19_ai_advanced_security/968_adversarial_training/) 포함한 재훈련
969. [differential privacy](/knowledge-base/studynote/09_security/19_ai_advanced_security/969_differential_privacy_ml/) in ML — 훈련 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/969_differential_privacy_ml/) privacy [보호](/knowledge-base/studynote/09_security/19_ai_advanced_security/969_differential_privacy_ml/)
970. [Federated Learning](/knowledge-base/studynote/09_security/19_ai_advanced_security/970_federated_learning_ml/) — [분산](/knowledge-base/studynote/09_security/19_ai_advanced_security/970_federated_learning_ml/) 훈련, [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/970_federated_learning_ml/) 불이동
971. [Homomorphic Encryption](/knowledge-base/studynote/09_security/19_ai_advanced_security/971_homomorphic_encryption_ml/) in ML — 암호화된 채로 추론
972. [TEE](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/) 기반 ML — [SGX](/knowledge-base/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/) 등에서 안전한 추론
973. [Responsible AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/973_responsible_ai/) — 공정성/설명가능성/투명성/ privacy
974. [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/974_ai_incident_database/) Incident — [AI](/knowledge-base/studynote/09_security/19_ai_advanced_security/974_ai_incident_database/) 관련 보안 사고DB
975. OWASP [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/975_owasp_llm_top10/) Top [10](/knowledge-base/studynote/09_security/19_ai_advanced_security/975_owasp_llm_top10/) — [LLM](/knowledge-base/studynote/09_security/19_ai_advanced_security/975_owasp_llm_top10/) 보안 취약점
976. LLM01: [Prompt Injection](/knowledge-base/studynote/09_security/uncategorized/976_dns_spoofing_cache_poisoning_dnssec_arp/) — 프롬프트 조작
977. LLM02: Insecure Output — 출력 [검증](/knowledge-base/studynote/09_security/19_ai_advanced_security/977_llm02_insecure_output/) 없이 신뢰
978. LLM03: [Training](/knowledge-base/studynote/09_security/19_ai_advanced_security/978_llm03_training_data_poisoning/) [Data Poisoning](/knowledge-base/studynote/09_security/19_ai_advanced_security/978_llm03_training_data_poisoning/) — 훈련 [데이터](/knowledge-base/studynote/09_security/19_ai_advanced_security/978_llm03_training_data_poisoning/) 오염
979. LLM04: Model Denial of [Service](/knowledge-base/studynote/09_security/uncategorized/979_ipsec_tunnel_transport_mode_vpn_encapsulation/) — 비용거대적 입력 유발
980. LLM05: [Supply Chain](/knowledge-base/studynote/09_security/uncategorized/980_ah_authentication_header_ipsec_integrity_no_encryption/) — [공급망](/knowledge-base/studynote/09_security/uncategorized/980_ah_authentication_header_ipsec_integrity_no_encryption/) 취약점
981. LLM06: [Sensitive Information](/knowledge-base/studynote/09_security/uncategorized/981_esp_encapsulating_security_payload_ipsec_confidentiality/) Disclosure — 훈련 [데이터](/knowledge-base/studynote/09_security/uncategorized/981_esp_encapsulating_security_payload_ipsec_confidentiality/) 유출
982. LLM07: Plugin Abuse — 플러그인 악용
983. LLM08: Autonomous Agent — 자가 실행 에이전트 위험
984. [양자 컴퓨팅](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/) — [양자 중첩](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/)/얽힘으로 계산 혁신
985. 양자 위협 — [RSA](/knowledge-base/studynote/09_security/uncategorized/985_x509_certificate_pki_digital_signature_format/)/[ECC](/knowledge-base/studynote/09_security/uncategorized/985_x509_certificate_pki_digital_signature_format/) 깨뜨릴 Shor [알고리즘](/knowledge-base/studynote/09_security/uncategorized/985_x509_certificate_pki_digital_signature_format/)
986. [Grover](/knowledge-base/studynote/09_security/uncategorized/986_symmetric_asymmetric_key_cryptography_rsa_aes/) [알고리즘](/knowledge-base/studynote/09_security/uncategorized/986_symmetric_asymmetric_key_cryptography_rsa_aes/) — 대칭키 강도반감
987. NIST [PQC](/knowledge-base/studynote/09_security/uncategorized/987_hash_function_one_way_integrity_avalanche_sha256/) 표준 — Kyber/Dilithium/Falcon/[SPHINCS](/knowledge-base/studynote/09_security/uncategorized/987_hash_function_one_way_integrity_avalanche_sha256/)+
988. [crypto agility](/knowledge-base/studynote/09_security/uncategorized/988_digital_signature_non_repudiation_integrity_hash_private_key/) — [알고리즘](/knowledge-base/studynote/09_security/uncategorized/988_digital_signature_non_repudiation_integrity_hash_private_key/) 교체 능력
989. 블록체인 보안 — 51% 공격, 이중지불, [스마트 컨트랙트](/knowledge-base/studynote/09_security/uncategorized/989_dos_ddos_denial_of_service_drdos_amplification_reflection/)
990. Reentrancy 공격 — [스마트 컨트랙트](/knowledge-base/studynote/09_security/uncategorized/990_botnet_cnc_zombie_pc_ddos_infrastructure/) 재진입취약점

---

## 20. 보안 추가 키워드 / 시험 대비 — 40개

991. [Evil Maid Attack](/knowledge-base/studynote/09_security/uncategorized/991_arp_spoofing_man_in_the_middle_cache_poisoning/) — 물리적 접근 후 [백도어](/knowledge-base/studynote/09_security/uncategorized/991_arp_spoofing_man_in_the_middle_cache_poisoning/) 설치
992. [Cold Boot Attack](/knowledge-base/studynote/09_security/uncategorized/992_stateful_inspection_firewall_session_state_table/) — [메모리 잔상 읽기](/knowledge-base/studynote/09_security/uncategorized/992_stateful_inspection_firewall_session_state_table/)
993. [DMA](/knowledge-base/studynote/09_security/uncategorized/993_waf_web_application_firewall_l7_sql_injection/) 공격 — [Thunderbolt](/knowledge-base/studynote/09_security/uncategorized/993_waf_web_application_firewall_l7_sql_injection/)/[PCIe](/knowledge-base/studynote/09_security/uncategorized/993_waf_web_application_firewall_l7_sql_injection/) [Direct Memory Access](/knowledge-base/studynote/09_security/uncategorized/993_waf_web_application_firewall_l7_sql_injection/)
994. [Firewire](/knowledge-base/studynote/09_security/uncategorized/994_ids_ips_intrusion_detection_prevention_false_positive/) 공격 — IEEE 1394 [DMA](/knowledge-base/studynote/09_security/uncategorized/994_ids_ips_intrusion_detection_prevention_false_positive/) 활용
995. [Thunderbolt Security](/knowledge-base/studynote/09_security/uncategorized/995_network_slicing_5g_sdn_nfv_qos_isolation/) — [DMA](/knowledge-base/studynote/09_security/uncategorized/995_network_slicing_5g_sdn_nfv_qos_isolation/) 방어를 위한 레벨 [설정](/knowledge-base/studynote/09_security/uncategorized/995_network_slicing_5g_sdn_nfv_qos_isolation/)
996. [USB_BAD](/knowledge-base/studynote/09_security/uncategorized/996_nfv_vnf_virtual_network_function_cnf/) — [USB](/knowledge-base/studynote/09_security/uncategorized/996_nfv_vnf_virtual_network_function_cnf/) 키보드 emulation
997. [Rubber Ducky](/knowledge-base/studynote/09_security/uncategorized/997_sdn_data_control_plane_separation_architecture/) — [USB](/knowledge-base/studynote/09_security/uncategorized/997_sdn_data_control_plane_separation_architecture/) 키보드 emulation 도구
998. [Bash Bunny](/knowledge-base/studynote/09_security/uncategorized/998_openflow_protocol_sdn_southbound_flow_table/) — 다목적 [USB](/knowledge-base/studynote/09_security/uncategorized/998_openflow_protocol_sdn_southbound_flow_table/) 공격 도구
999. [OMG Cable](/knowledge-base/studynote/09_security/uncategorized/999_mec_mobile_edge_computing_local_breakout_5g/) — 변형된 [USB](/knowledge-base/studynote/09_security/uncategorized/999_mec_mobile_edge_computing_local_breakout_5g/) 케이블
1000. _entropy — 난수 [생성](/knowledge-base/studynote/09_security/uncategorized/1000_cloud_native_network_cni_kubernetes_pod_overlay/) 품질
1001. [CSPRNG](/knowledge-base/studynote/09_security/20_extra_exam_prep/1001_csprng_random_generator/) (Cryptographically Secure PRNG) — [암호학](/knowledge-base/studynote/09_security/20_extra_exam_prep/1001_csprng_random_generator/)적으로 안전한 난수
1002. [RDRAND](/knowledge-base/studynote/09_security/20_extra_exam_prep/1002_rdrand_intel_hardware_rng/) (Intel) — 하드웨어 난수 [생성](/knowledge-base/studynote/09_security/20_extra_exam_prep/1002_rdrand_intel_hardware_rng/)
1003. /dev/urandom — Linux 난수 장치
1004. [hardware RNG](/knowledge-base/studynote/09_security/20_extra_exam_prep/1004_hardware_rng_trng/) — [물리적 난수 발생기](/knowledge-base/studynote/09_security/20_extra_exam_prep/1004_hardware_rng_trng/)
1005. [entropy source](/knowledge-base/studynote/09_security/20_extra_exam_prep/1005_entropy_source/) — [난수 생성 원천](/knowledge-base/studynote/09_security/20_extra_exam_prep/1005_entropy_source/)
1006. [Perfect Security](/knowledge-base/studynote/09_security/20_extra_exam_prep/1006_perfect_security_otp/) — 정보 이론적 안전 ([One-Time Pad](/knowledge-base/studynote/09_security/20_extra_exam_prep/1006_perfect_security_otp/))
1007. [Semantic Security](/knowledge-base/studynote/09_security/20_extra_exam_prep/1007_semantic_security/) — [암호학](/knowledge-base/studynote/09_security/20_extra_exam_prep/1007_semantic_security/)적으로 관찰 가능한 차이 없음
1008. [IND-CPA](/knowledge-base/studynote/09_security/20_extra_exam_prep/1008_ind_cpa_ind_cca2/) / IND-CCA2 — [암호학 안전성](/knowledge-base/studynote/09_security/20_extra_exam_prep/1008_ind_cpa_ind_cca2/) 정의
1009. [AEAD](/knowledge-base/studynote/09_security/20_extra_exam_prep/1009_aead_authenticated_encryption/) — Authenticated Encryption with Associated [Data](/knowledge-base/studynote/09_security/20_extra_exam_prep/1009_aead_authenticated_encryption/)
1010. [Key Wrapping](/knowledge-base/studynote/09_security/20_extra_exam_prep/1010_key_wrapping_kek/) — KEK 활용
1011. [Envelope Encryption](/knowledge-base/studynote/09_security/20_extra_exam_prep/1011_envelope_encryption/) — Digital Envelope
1012. [CloudHSM](/knowledge-base/studynote/09_security/20_extra_exam_prep/1012_cloud_hsm/) — 클라우드 전용 [HSM](/knowledge-base/studynote/09_security/20_extra_exam_prep/1012_cloud_hsm/)
1013. [AWS KMS](/knowledge-base/studynote/09_security/20_extra_exam_prep/1013_aws_kms/) — [Key](/knowledge-base/studynote/09_security/20_extra_exam_prep/1013_aws_kms/) [Management](/knowledge-base/studynote/09_security/20_extra_exam_prep/1013_aws_kms/) [Service](/knowledge-base/studynote/09_security/20_extra_exam_prep/1013_aws_kms/)
1014. Bring Your Own [Key](/knowledge-base/studynote/09_security/20_extra_exam_prep/1014_byok_bring_your_own_key/) ([BYOK](/knowledge-base/studynote/09_security/20_extra_exam_prep/1014_byok_bring_your_own_key/)) — 고객 관리 키
1015. Hold Your Own [Key](/knowledge-base/studynote/09_security/20_extra_exam_prep/1015_hyok_hold_your_own_key/) ([HYOK](/knowledge-base/studynote/09_security/20_extra_exam_prep/1015_hyok_hold_your_own_key/)) — 외부 키 보관
1016. [Zero Knowledge Proof](/knowledge-base/studynote/09_security/02_crypto/1016_zero_knowledge_proof/) ([ZKP](/knowledge-base/studynote/09_security/02_crypto/1016_zero_knowledge_proof/)) — [영지식 증명](/knowledge-base/studynote/09_security/02_crypto/1016_zero_knowledge_proof/)
1017. [Commitment Scheme](/knowledge-base/studynote/09_security/20_extra_exam_prep/1017_commitment_scheme/) — [약속 기법](/knowledge-base/studynote/09_security/20_extra_exam_prep/1017_commitment_scheme/)
1018. [Secure Multi-Party Computation](/knowledge-base/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/) ([SMPC](/knowledge-base/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/)) — 안전한 다자간 계산
1019. [동형 암호](/knowledge-base/studynote/09_security/02_crypto/1019_homomorphic_encryption/) ([Homomorphic Encryption](/knowledge-base/studynote/09_security/02_crypto/1019_homomorphic_encryption/)) — 암호문 상태 연산
1020. [Functional Encryption](/knowledge-base/studynote/09_security/20_extra_exam_prep/1020_functional_encryption/) — [함수 암호](/knowledge-base/studynote/09_security/20_extra_exam_prep/1020_functional_encryption/)
1021. [Searchable Encryption](/knowledge-base/studynote/09_security/uncategorized/1021_vlc_visible_light_communication_lifi_modulation/) — [검색 가능 암호](/knowledge-base/studynote/09_security/uncategorized/1021_vlc_visible_light_communication_lifi_modulation/)
1022. [방변조 하드웨어](/knowledge-base/studynote/09_security/uncategorized/1022_leo_satellite_starlink_mega_constellation_6g/) — [Anti-tamper](/knowledge-base/studynote/09_security/uncategorized/1022_leo_satellite_starlink_mega_constellation_6g/) Hardware ([TPM](/knowledge-base/studynote/09_security/uncategorized/1022_leo_satellite_starlink_mega_constellation_6g/)/[HSM](/knowledge-base/studynote/09_security/uncategorized/1022_leo_satellite_starlink_mega_constellation_6g/))
1023. [Secure Enclave](/knowledge-base/studynote/09_security/uncategorized/1023_isl_inter_satellite_link_low_earth_orbit_routing/) — TrustZone/[SGX](/knowledge-base/studynote/09_security/uncategorized/1023_isl_inter_satellite_link_low_earth_orbit_routing/) 격리 영역
1024. [TEE](/knowledge-base/studynote/09_security/uncategorized/1024_v2x_vehicle_to_everything_connected_car/) ([Trusted Execution Environment](/knowledge-base/studynote/09_security/uncategorized/1024_v2x_vehicle_to_everything_connected_car/)) — [신뢰 실행 환경](/knowledge-base/studynote/09_security/uncategorized/1024_v2x_vehicle_to_everything_connected_car/)
1025. [Security Chaos 엔진ering](/knowledge-base/studynote/09_security/uncategorized/1025_security_chaos_engineering/) — 보안 [카오스 엔지니어링](/knowledge-base/studynote/09_security/uncategorized/1025_security_chaos_engineering/)
1026. [침해 시뮬레이션](/knowledge-base/studynote/09_security/uncategorized/1026_smart_grid_ami_two_way_communication_energy/) ([BAS](/knowledge-base/studynote/09_security/uncategorized/1026_smart_grid_ami_two_way_communication_energy/)) — Breach & Attack Simulation
1027. [사이버 보험](/knowledge-base/studynote/09_security/uncategorized/1027_uwsn_mac_routing_depth_based_protocol/) — [Cyber Insurance](/knowledge-base/studynote/09_security/uncategorized/1027_uwsn_mac_routing_depth_based_protocol/)
1028. [Bug Bounty](/knowledge-base/studynote/09_security/uncategorized/1028_wban_mac_duty_cycle_healthcare_sleep_mode/) — [버그 바운티](/knowledge-base/studynote/09_security/uncategorized/1028_wban_mac_duty_cycle_healthcare_sleep_mode/)
1029. [Responsible Disclosure](/knowledge-base/studynote/09_security/uncategorized/1029_lora_lpwan_chirp_spread_spectrum_iot/) — [책임 있는 공개](/knowledge-base/studynote/09_security/uncategorized/1029_lora_lpwan_chirp_spread_spectrum_iot/)
1030. [Coordinated Disclosure](/knowledge-base/studynote/09_security/uncategorized/1030_sigfox_lpwan_ultra_narrow_band_iot/) — [협력적 공개](/knowledge-base/studynote/09_security/uncategorized/1030_sigfox_lpwan_ultra_narrow_band_iot/)

---

**총 키워드 수: 800개**
