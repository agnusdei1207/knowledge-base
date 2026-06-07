---
title: "019. Ai Emerging Tech"
date: "2025-02-24"
tags:
  - "security"
  - "studynote-security"
weight: 19
---
# [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 및 신기술 보안 ([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) & Emerging Tech [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 기존 소프트웨어의 '로직 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)(Bug)'을 막는 것을 넘어, 모델이 학습하는 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 오염(Poisoning)'과 추론 과정의 '수학적 착시(Adversarial)'를 방어하는 완전히 새로운 패러다임이다.
> 2. **가치**: 신뢰할 수 있는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) (Trustworthy [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))와 [양자 내성 암호](/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)([PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/)) 전환 체계를 구축하여, 차세대 비즈니스의 무결성을 보장하고 [Q-Day](/studynote/09_security/03_network_security/151_quantum_computing_threats/)(양자컴퓨터로 인한 암호 체계 붕괴일) 생존력을 확보한다.
> 3. **융합**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 자체가 해커의 공격 무기([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)-driven Attack)가 됨과 동시에 방어자의 핵심 엔진([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)-driven Defense)이 되는 창과 방패의 비대칭적 융합이 일어나고 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

과거의 보안이 "작성된 코드 라인([Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Line)"에 존재하는 취약점(예: [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/), SQL [인젝션](/studynote/04_software_engineering/11_testing_validation/872_injection/))을 방어하는 것이었다면, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대의 보안은 "수십억 개의 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(Weights)와 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"에 숨겨진 취약점을 방어해야 한다. [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(대형 언어 모델)이 기업의 핵심 의사결정과 고객 응대를 대체하면서, AI가 잘못된 판단을 내리도록 유도하는 <strong>적대적 공격(<a href="/studynote/10_ai/02_dl_architecture_new/197_adversarial_attack/">Adversarial Attack</a>)</strong>과 악의적 지시를 삽입하는 <strong><a href="/studynote/09_security/19_ai_advanced_security/955_prompt_injection/">프롬프트 인젝션</a>(<a href="/studynote/09_security/19_ai_advanced_security/955_prompt_injection/">Prompt Injection</a>)</strong>은 비즈니스에 치명적인 타격을 입히고 있다. 또한, 머지않은 미래에 실용화될 [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)([Quantum Computer](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/))는 현재 우리가 사용하는 RSA와 [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 공개키 암호 체계를 무력화할 수 있어, 이에 대비한 [암호 민첩성](/studynote/09_security/19_ai_advanced_security/988_crypto_agility/)([Crypto Agility](/studynote/09_security/03_network_security/153_crypto_agility/)) 확보가 시급하다.

<strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">전통적 소프트웨어 보안 vs [AI</a> 모델 보안 위협 표면 도식]</strong>
이 도식은 코드 기반 시스템과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 간의 공격 벡터(Attack Vector)가 어떻게 변화했는지를 보여준다.
```text
[ 전통적 App Security ]         [ AI/ML Model Security ]
+-------------------+         +---------------------------+
| Source Code (로직)|<-(SQLi)  | Training Data (데이터)    |<-(Poisoning)
+-------------------+         +---------------------------+
| Compiler/Build    |         | ML Algorithm (가중치)     |<-(Backdoor)
+-------------------+         +---------------------------+
| Runtime (실행)    |<-(RCE)   | Inference (추론/프롬프트) |<-(Evasion)
+-------------------+         +---------------------------+
```
이 비교의 핵심은 공격자가 더 이상 서버의 루트 권한(Root)을 얻기 위해 복잡한 익스플로잇(Exploit)을 작성할 필요가 없다는 점이다. 단순히 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 셋에 미세한 노이즈를 섞거나([Data Poisoning](/studynote/09_security/19_ai_advanced_security/947_data_poisoning/)), 챗봇에게 교묘하게 작성된 자연어 문장([Prompt Injection](/studynote/09_security/19_ai_advanced_security/955_prompt_injection/))을 던지는 것만으로도 시스템을 완전히 통제하거나 기밀 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 탈취할 수 있다. 따라서 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 개발 전 단계(학습 [데이터 정제](/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/))부터 배포 이후(추론 필터링)까지 이어지는 새로운 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 파이프라인의 보안(DevSecMLOps)을 요구한다.

> 📢 **섹션 요약 비유**: 전통적인 보안이 도둑이 들어오지 못하게 은행의 '자물쇠(코드)'를 튼튼하게 만드는 것이라면, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 은행원([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델)이 보이스피싱 전화를 받고 스스로 금고 문을 열어주지 않도록 '판단력과 신원 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 절차([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 프롬프트 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))'를 교육하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템에 대한 공격은 크게 학습 단계([Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/) Phase)와 추론 단계(Inference Phase)로 나뉜다. 특히 추론 단계의 회피 공격(Evasion Attack) 중 가장 대표적인 것이 <strong><a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">적대적 예제</a>(<a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">Adversarial Example</a>)</strong>이다.

| 공격 유형 | 공격 단계 | 핵심 원리 및 기법 | 방어 기술 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/19_ai_advanced_security/947_data_poisoning/">데이터 포이즈닝</a> (<a href="/studynote/09_security/19_ai_advanced_security/947_data_poisoning/">Data Poisoning</a>)</strong> | 학습 ([Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) | 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 악성 샘플을 주입하여 모델의 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 경계선(Decision Boundary)을 왜곡함 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)([Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)) 제거 |
| <strong><a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">적대적 예제</a> (<a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">Adversarial Example</a>)</strong> | 추론 (Inference)| 사람의 눈에는 보이지 않는 미세한 노이즈(Perturbation)를 입력값에 더해 오분류 유도 | [적대적 훈련](/studynote/09_security/19_ai_advanced_security/968_adversarial_training/) ([Adversarial Training](/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)) |
| <strong><a href="/studynote/09_security/19_ai_advanced_security/955_prompt_injection/">프롬프트 인젝션</a> (<a href="/studynote/09_security/19_ai_advanced_security/955_prompt_injection/">Prompt Injection</a>)</strong> | 추론 (Inference)| LLM의 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시스템 프롬프트를 무시하고 공격자의 지시를 따르도록 자연어 조작 | 입력/출력 가드레일 ([Guardrails](/studynote/09_security/19_ai_advanced_security/965_llm_guardrails/)) |
| <strong><a href="/studynote/09_security/19_ai_advanced_security/950_model_extraction/">모델 추출</a> (<a href="/studynote/09_security/19_ai_advanced_security/950_model_extraction/">Model Extraction</a>)</strong> | 추론 (Inference)| [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 질의 응답 쌍을 대량으로 수집하여 타겟 모델과 유사한 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 모델을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [비율 제한](/studynote/04_software_engineering/08_security_compliance_devsecops/511_api_rate_limiting_throttling/)([Rate Limiting](/studynote/09_security/05_web_app_security/520_rate_limiting/)), 노이즈 추가 |

**FGSM (Fast Gradient Sign Method) 기반 적대적 공격 메커니즘]**
이 도식은 원본 이미지에 노이즈를 추가하여 인공지능이 어떻게 완벽하게 속게 되는지를 수학적 직관으로 보여준다.
```text
   [원본 이미지 (판다)]       [적대적 노이즈 (Perturbation)]     [조작된 이미지 (긴팔원숭이)]
       x (데이터)        +    ε * sign(∇x J(θ, x, y))   =        x' (조작된 데이터)
+----------------------+  +--------------------------+   +------------------------+
| Confidence:          |  | 손실 함수(J)를 최대화하는|   | Confidence:            |
| Panda (99.8%)        |  | 방향(∇)으로 미세 이동(ε) |   | Gibbon (99.3%)         |
+----------------------+  +--------------------------+   +------------------------+
```
이 흐름의 핵심은 공격이 철저하게 "모델의 오차(Loss) 기울기를 역이용"하는 수학적 최적화 과정이라는 점이다. 사람의 눈에는 조작된 이미지(x')가 여전히 판다로 보이지만, 모델 내부의 신경망 연산에서는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)와 곱해진 노이즈가 증폭되어 완전히 다른 클래스(긴팔원숭이)로 판정된다. 이를 방어하는 가장 효과적인 방법은 [적대적 예제](/studynote/09_security/19_ai_advanced_security/942_adversarial_example/)를 미리 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 정답(판다)과 함께 재학습시키는 <strong><a href="/studynote/09_security/19_ai_advanced_security/968_adversarial_training/">적대적 훈련</a>(<a href="/studynote/09_security/19_ai_advanced_security/968_adversarial_training/">Adversarial Training</a>)</strong>이나, 입력 이미지의 노이즈를 제거하는 **입력 정제(Input Sanitization)** 기법이다.

최근 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 보안에서는 OWASP [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) Top 10이 글로벌 표준으로 자리 잡았으며, LLM01([프롬프트 인젝션](/studynote/09_security/19_ai_advanced_security/955_prompt_injection/))과 LLM06(민감 정보 노출)을 막기 위해 입력과 출력 사이에 시맨틱 라우터(Semantic Router)나 가드레일을 배치하는 아키텍처가 필수적이다.

> 📢 **섹션 요약 비유**: 적대적 공격은 자율주행 자동차의 카메라에 '보이지 않는 특수 필름'을 붙여, 정지(STOP) 표지판을 시속 100km 속도 제한 표지판으로 잘못 읽게 만드는 정교한 시각적 마술입니다. 방어자는 AI에게 이 마술의 트릭을 미리 가르쳐야([적대적 훈련](/studynote/09_security/19_ai_advanced_security/968_adversarial_training/)) 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안 외에도 미래 기술 보안의 양대 산맥은 <strong><a href="/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">양자 내성 암호</a>(<a href="/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/">PQC</a>)</strong>와 <strong><a href="/studynote/09_security/19_ai_advanced_security/989_blockchain_security/">블록체인 보안</a>(Web3 <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>이다. 특히 [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)의 발전은 기존 암호 체계의 근간을 흔든다.

| 구분 | [RSA](/studynote/09_security/03_network_security/110_rsa/) / [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (현재 암호) | [PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/) ([양자 내성 암호](/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)) | [QKD](/studynote/03_network/18_optical_nextgen_automation/922_qkd_quantum_key_distribution_bb84_eavesdropping/) ([양자 암호 통신](/studynote/03_network/18_optical_nextgen_automation/922_qkd_quantum_key_distribution_bb84_eavesdropping/)) |
|:---|:---|:---|:---|
| **기반 수학/물리 원리** | 소인수분해, 이산대수 (수학적 복잡성) | 격자(Lattice), 해시 등 다변수 수학 문제 | [양자 얽힘](/studynote/06_ict_convergence/03_cloud_infrastructure/220_quantum_entanglement/), [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 불가능성 (물리 법칙) |
| <strong>양자 공격 (Shor <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>) 내성</strong>| 취약함 (몇 시간 내 키 도출 가능) | 안전함 (양자 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로도 풀기 어려움) | 완벽히 안전함 ([도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/) 즉시 상태 붕괴) |
| **구현 방식 및 인프라** | 기존 소프트웨어/하드웨어 그대로 사용 | 기존 시스템에 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(SW)만 교체 적용 | 전용 양자 채널(광케이블) 및 물리적 장비 필요 |
| **NIST 표준 (최신)** | FIPS 186-5 ([RSA](/studynote/09_security/03_network_security/110_rsa/)/[ECDSA](/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/)) | FIPS 203 (Dilithium), 204 (Kyber) | 암호가 아닌 통신 계층의 물리적 보안 |

<strong><a href="/studynote/09_security/19_ai_advanced_security/988_crypto_agility/">양자 위협에 대비하는 [암호 민첩성</a> (<a href="/studynote/09_security/03_network_security/153_crypto_agility/">Crypto Agility</a>) 구조도]</strong>
이 도식은 하드코딩된 암호 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 위험성과, [PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/) 전환을 위한 유연한 아키텍처를 비교한다.
```text
[ Legacy: Hardcoded Crypto ]      [ Modern: Crypto Agility Architecture ]
+-------------------------+       +-------------------------------------+
| Application Code        |       | Application Code (암호 로직 분리)   |
|  L  AES-256 + RSA-2048  |       |   v 호출 (API)                      |
+-------------------------+       | [ Crypto Abstraction Layer (KMS) ]  |
            | 교체 불가           |   +- RSA/ECC (Current)              |
         [Q-Day 파국]             |   +- Kyber/Dilithium (PQC Ready)    |
                                  +-------------------------------------+
```
이 비교의 핵심은 [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)가 상용화되는 시점([Q-Day](/studynote/09_security/03_network_security/151_quantum_computing_threats/))에 대응하기 위해, 지금 당장 모든 암호를 PQC로 바꾸는 것이 아니라 <strong>"언제든 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>을 스위칭할 수 있는 구조(<a href="/studynote/09_security/03_network_security/153_crypto_agility/">Crypto Agility</a>)"</strong>를 만드는 것이 중요하다는 점이다. 현재 공격자들이 암호화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 미리 수집해두고 [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)가 개발되면 복호화하려는 <strong>"Harvest Now, Decrypt Later (<a href="/studynote/09_security/03_network_security/152_hndl_harvest_now_decrypt_later/">HNDL</a>)"</strong> 공격을 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이므로, 장기 보관이 필요한 기밀 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 즉시 [KEM](/studynote/09_security/03_network_security/134_kem_key_encapsulation/)([Key Encapsulation Mechanism](/studynote/09_security/03_network_security/134_kem_key_encapsulation/)) 기반의 [PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/) 하이브리드 암호화로 전환해야 한다.

> 📢 **섹션 요약 비유**: 현재의 암호([RSA](/studynote/09_security/03_network_security/110_rsa/))가 매우 복잡한 자물쇠라면, [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)는 이 자물쇠를 단번에 녹여버리는 만능 용접기입니다. [양자 내성 암호](/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/)([PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/))는 용접기의 열을 흡수하는 전혀 다른 재질(격자 수학)로 만든 새로운 자물쇠로 교체하는 작업입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

신기술 보안을 실무에 적용할 때 가장 위험한 것은 기존 IT 보안의 잣대로 신기술의 리스크를 평가하는 것이다.

1. <strong><a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> 사내 도입 시 <a href="/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/">DLP</a>(<a href="/studynote/12_it_management/05_security_compliance/186_dlp_data_loss_prevention/">데이터 유출 방지</a>) 한계</strong>
   - **상황**: 임직원들이 챗GPT 등 외부 LLM을 사용할 때 사내 기밀을 입력하는 것을 막기 위해, 사내망 웹 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)([SWG](/studynote/03_network/14_network_security_threats/742_swg_secure_web_gateway/))에서 '대외비' 키워드 필터링을 적용함.
   - **문제**: 직원이 소스코드를 입력하거나 재무 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 질문에 녹여서(은어 사용) 물어볼 경우, 기존 키워드 기반 DLP는 문맥([Context](/studynote/02_operating_system/01_overview_architecture/033_context/))을 이해하지 못해 100% 우회됨.
   - **의사결정**: 외부 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 접속을 직접 통제하기보다는, 사내 전용 격리된 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)(Private [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))을 구축하거나, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동 시 PII([개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)) 및 기밀을 실시간으로 마스킹/비식별화하는 <strong><a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> <a href="/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/">방화벽</a>(<a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> <a href="/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/">Firewall</a>/Trust Layer)</strong>을 아키텍처에 추가해야 한다.

2. <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 기반 악성코드 방어의 오탐률 (False Positive) 관리</strong>
   - **상황**: [EDR](/studynote/09_security/04_endpoint_security/325_edr/)(엔드포인트 탐지 및 대응) 솔루션에 최신 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [행위 기반 탐지](/studynote/09_security/04_endpoint_security/324_behavior_based_detection/) 엔진을 적용함.
   - **문제**: 개발자의 정상적인 스크립트 실행이나 관리자의 PowerShell 스크립트가 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 행위로 오탐되어 업무 PC가 격리([Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))되는 사태 빈발.
   - **의사결정**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델은 결정의 이유를 설명하지 못하는 '블랙박스(Blackbox)' 한계가 있다. 실무에서는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 탐지 엔진의 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)(Threshold)를 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 보수적으로 설정하고, <strong><a href="/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/">XAI</a> (<a href="/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/">Explainable AI</a>, 설명 가능한 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>)</strong> 기능이 포함된 솔루션을 채택하여 [SOC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)(보안관제) 팀이 오탐 사유를 명확히 해석하고 예외 처리할 수 있도록 프로세스를 정립해야 한다.

3. <strong><a href="/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">스마트 컨트랙트</a> (<a href="/studynote/06_ict_convergence/01_blockchain/022_smart_contract/">Smart Contract</a>) 배포 <a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
   - **상황**: [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 기반의 웹3 서비스를 런칭하며, 빠른 출시를 위해 내부 코드 리뷰만 거친 후 메인넷에 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)를 배포함.
   - **문제**: 배포된 컨트랙트에 재진입(Reentrancy) 취약점이 존재하여 해커가 무한 루프로 자금을 탈취함. ([블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 코드 수정/패치가 불가능함)
   - **의사결정**: 배포 후 패치가 불가능한 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 특성상, 배포 전 <strong>정형 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(<a href="/studynote/06_ict_convergence/01_blockchain/093_smart_contract_formal_verification/">Formal Verification</a>)</strong>과 외부 전문 업체의 [보안 감사](/studynote/04_software_engineering/11_testing_validation/919_security_audit_trail/)([Smart Contract](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) [Audit](/studynote/12_it_management/05_security_compliance/363_audit/))를 의무화하는 것이 유일한 해법이다.

> 📢 **섹션 요약 비유**: AI와 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)이라는 강력한 최새로운 유형의 스포츠카를 샀다면, 그에 걸맞은 탄소 세라믹 브레이크([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 가드레일, 정형 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/))를 장착해야 합니다. 구형 자전거의 브레이크(기존 보안)를 달고 고속 주행을 하면 첫 번째 코너에서 반드시 사고가 납니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

AI와 [양자 컴퓨팅](/studynote/12_it_management/05_security_compliance/236_quantum_computing_pqc/) 등 신기술에 대한 [보안 아키텍처](/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/) 선제 구축은 단순한 '방어'를 넘어, 글로벌 규제 준수와 고객 신뢰 확보라는 '비즈니스 경쟁력'으로 직결된다.

| 기대 효과 | 정성적 지표 | 정량적 지표 |
|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> <a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>(Trust) 확보</strong> | 편향성 및 [할루시네이션](/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/)([환각](/studynote/06_ict_convergence/04_ai_llm/275_react_framework/)) 통제로 브랜드 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 비윤리적/악성 출력률 99% 차단 |
| **선제적 양자 위협 대응** | [HNDL](/studynote/09_security/03_network_security/152_hndl_harvest_now_decrypt_later/)(선수집 후해독) 공격으로부터 핵심 기밀 사수 | [PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 전환을 통한 암호 수명 30년 연장 |
| **보안 운영의 고도화** | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안 관제([SOAR](/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/))를 통한 인력 의존도 감소 | 보안 이벤트 평균 대응 시간([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)) 80% 단축 |

최종적으로 보안 업계는 공격자가 AI를 이용해 스피어피싱과 취약점 익스플로잇을 자동화하는 <strong>"<a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> vs <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>"의 무한 경쟁 시대</strong>에 돌입했다. 이에 대응하기 위해 기업은 가트너가 제시한 <strong><a href="/studynote/09_security/19_ai_advanced_security/964_ai_trism/">AI TRiSM</a> (Trust, <a href="/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">Risk</a> and <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong> 프레임워크를 전사적으로 도입해야 한다. 모델의 안전성([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프라이버시(Privacy), 그리고 결정의 설명 가능성(Explainability)을 설계 단계부터 통합하는 기업만이 차세대 기술 혁신의 주도권을 안전하게 쥘 수 있을 것이다.

> 📢 **섹션 요약 비유**: 신기술 보안은 다가오는 거대한 쓰나미([양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 해킹)에 대비해 방파제를 높이는 작업입니다. 쓰나미가 눈앞에 보일 때 콘크리트를 붓기 시작하면 이미 늦습니다. 지금 바로 뼈대([암호 민첩성](/studynote/09_security/19_ai_advanced_security/988_crypto_agility/)과 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가드레일)를 세워야 생존할 수 있습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">적대적 예제</a> (<a href="/studynote/09_security/19_ai_advanced_security/942_adversarial_example/">Adversarial Example</a>)</strong> | 인간 눈에는 무해한 미세 노이즈를 이미지에 삽입해 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 오분류시키는 공격으로, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안의 출발점 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/">PQC</a> (<a href="/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">Post-Quantum Cryptography</a>, <a href="/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">양자 내성 암호</a>)</strong> | [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)가 현재 [RSA](/studynote/09_security/03_network_security/110_rsa/)·ECC를 수분 내 해독하는 Q-Day에 대비해 NIST가 표준화한 격자 기반 신규 암호 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 체계 |
| <strong><a href="/studynote/09_security/19_ai_advanced_security/964_ai_trism/">AI TRiSM</a> (Trust, <a href="/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">Risk</a> and <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong> | 가트너가 제시한 프레임워크로 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)·위험·보안을 설계 단계부터 통합 관리하는 차세대 거버넌스 구조 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 보안 — 시그니처·룰 기반 방어]
    |
    v
[AI 기반 위협 등장 — 적대적 공격·데이터 포이즈닝·프롬프트 인젝션]
    |
    v
[AI 보안 (AI Security) — LLM 방화벽·XAI·모델 강건화]
    |
    v
[PQC (양자 내성 암호) — Q-Day 대비 암호 민첩성 확보]
    |
    v
[AI TRiSM — 신뢰·위험·보안 통합 거버넌스]
```
AI와 [양자 컴퓨팅](/studynote/12_it_management/05_security_compliance/236_quantum_computing_pqc/)의 부상은 전통 보안 패러다임을 무력화하며, [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 가드레일·[PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/) 전환·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) TRiSM이라는 3축의 선제적 아키텍처를 요구한다.

### 👶 어린이를 위한 3줄 비유 설명

1. [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 보안은 아주 똑똑한 로봇 경비원이지만, 눈에 보이지 않는 이상한 스티커([적대적 예제](/studynote/09_security/19_ai_advanced_security/942_adversarial_example/))를 붙이면 친구를 도둑으로 오해하는 <strong>약점</strong>이 있어요!
2. [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)는 세상에서 가장 강력한 자물쇠 따개라서, 지금 사용하는 열쇠([RSA](/studynote/09_security/03_network_security/110_rsa/) 암호)로 잠근 금고를 순식간에 열 수 있다고 해요!
3. 그래서 과학자들은 [양자 컴퓨터](/studynote/01_computer_architecture/12_accelerators_ai_hardware/447_quantum_computer/)도 못 여는 마법의 새 자물쇠([PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/))를 미리 만들어두고, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 경비원이 헷갈리지 않도록 훈련시키고 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 19 / 1108

<- **이전**: [18. IoT, OT, ICS 및 물리적 보안 (IoT, OT, ICS & Physical Security)](/studynote/09_security/01_intro_principles/018_iot_ot_ics_physical/)
**다음**: [20. 보안 심화 및 최신 위협 (Security Advanced & Emerging Threats)](/studynote/09_security/01_intro_principles/020_security_advanced_exam/) ->

---
