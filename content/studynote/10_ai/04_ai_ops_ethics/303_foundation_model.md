---
title: "Foundation Model"
date: "2026-05-09"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) ([Foundation Model](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/))은 대규모 비라벨 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 사전 학습되어 폭넓은 일반 지식을 내재화한 뒤, [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) 또는 프롬프트로 다양한 다운스트림 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)에 적응할 수 있는 범용 대형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델이다.
> 2. **가치**: 각 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)마다 처음부터 모델을 훈련하는 대신, 하나의 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 위에 소량의 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)별 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [미세 조정](/studynote/10_ai/02_dl_architecture_new/133_fine_tuning/)([Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))만 수행하여 전문화된 모델을 신속하게 구축함으로써 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발 비용과 시간을 혁신적으로 절감한다.
> 3. **판단 포인트**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)의 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)로 <strong>편향(<a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/">Bias</a>) 증폭</strong>, <strong><a href="/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/">할루시네이션</a>(<a href="/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/">Hallucination</a>)</strong>, <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/">저작권</a> 문제</strong>, <strong>에너지 소비</strong>가 있으며, 이는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 거버넌스([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Governance) 및 윤리적 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(Ethical [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 논의의 핵심 쟁점이다.

---

## Ⅰ. 개요 및 필요성

2021년 스탠퍼드 대학교의 센터 보고서에서 처음 명명된 "[파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)([Foundation Model](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/))"은 말 그대로 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 생태계의 <strong>기반(Foundation)</strong>이 되는 모델이다. 기존 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발 패러다임은 "각 애플리케이션마다 전용 모델을 처음부터 훈련"하는 방식이었다. 이는 막대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·컴퓨팅·시간 자원을 각 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)마다 중복 투자하는 비효율의 극치였다.

[파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 이 비효율을 혁파한다. 수천억 개의 텍스트·이미지·코드에서 한 번의 대규모 사전 학습으로 일반 지식을 흡수하고, 이 하나의 "기반" 위에 번역·[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·의료 진단·법률 분석 등 수백 가지 전문 애플리케이션을 소량 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)으로 올리는 구조다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 OS([운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))다. Windows나 Linux를 한 번 설치하면 그 위에 수만 가지 앱(다운스트림 [태스크](/studynote/02_operating_system/02_process_thread/150_task/))을 설치·실행할 수 있다. 매번 앱마다 CPU·메모리 관리 코드를 짜는 것과 비교하면 개발 효율이 수천 배 차이 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|         파운데이션 모델 생태계 구조                                    |
+------------------------------------------------------------------+
|                                                                  |
|  ① 사전 학습 (Pre-training) 단계:                                  |
|  +-----------------------------------------------------------+   |
|  |  수조 토큰의 다양한 데이터 (웹 텍스트, 코드, 논문, 책...)       |   |
|  |             |                                             |   |
|  |  수천 GPU × 수개월의 대규모 학습                              |   |
|  |             |                                             |   |
|  |  파운데이션 모델 (수십억~수조 파라미터)                       |   |
|  |  "언어·코드·상식·추론 등 범용 능력 내재화"                    |   |
|  +-----------------------------------------------------------+   |
|                      |                                           |
|  ② 적응 (Adaptation) 단계:                                        |
|  +------------+  +-----------+  +------------+  +-----------+   |
|  | 파인 튜닝   |  | 프롬프트   |  | PEFT/LoRA  |  | RAG 연동  |   |
|  |(Fine-Tune) |  | 엔지니어링 |  |  경량 적응  |  | 지식 보강 |   |
|  +------------+  +-----------+  +------------+  +-----------+   |
|         |               |              |               |         |
|  +------v---------------v--------------v---------------v------+  |
|  |  법률 AI  |  의료 AI  |  코드 AI  |  챗봇  |  번역기  | ... |  |
|  +--------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

| 대표 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) | 개발사 | 파라미터 | 특징 |
|:---|:---|:---|:---|
| [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 | OpenAI | 비공개 | [멀티모달](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/), 최고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| Claude 3 | Anthropic | 비공개 | [Constitutional AI](/studynote/09_security/19_ai_advanced_security/966_constitutional_ai/), 안전성 |
| Gemini | Google DeepMind | 비공개 | [멀티모달](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/), 긴 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) |
| LLaMA 3 | Meta | 70B | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) |
| HyperCLOVA X | NAVER | 82B | 한국어 특화 |

- **📢 섹션 요약 비유**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 간 경쟁은 스마트폰 OS 전쟁이다. iOS([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4), Android(LLaMA/[오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)), 삼성OS(HyperCLOVA X)처럼 각 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 자신만의 생태계를 구축하며 그 위에 수천 개의 앱(전문 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 올라온다.

---

## Ⅲ. 비교 및 연결

<strong>일반 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> vs <a href="/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/">파운데이션 모델</a></strong>:
- 기존: 의료 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) = 의료 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만으로 처음부터 학습 -> 의료에만 사용 가능
- [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/): 범용 지식 사전 학습 -> 의료 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) -> 의료 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 법률 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) -> 법률 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)
- 핵심 차이: 범용성(Generality)과 전문성(Specialization) 동시 달성

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) ([Foundation Model](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 모든 분야에서 1년씩 인턴을 한 올라운더 컨설턴트다. 법률 사무소([파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))에 합류하면 곧바로 법률 전문가가 되고, 병원([파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/))에 가면 의료 전문가가 된다. 처음부터 한 분야만 공부한 전문가보다 범용 지식과 적응력이 훨씬 높다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/">파운데이션 모델</a> 도입 시 고려사항</strong>:
1. **비용**: 사전 학습에 수십억~수천억 원의 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 비용 발생. 대부분 기업은 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)(LLaMA) 또는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 활용
2. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 프라이버시</strong>: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 사용 시 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 외부 서버로 전송 -> 의료·금융·법률 등 기밀 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)([On-Premise](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) 배포 필요
3. <strong><a href="/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/">할루시네이션</a> 관리</strong>: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 없는 사실을 있는 것처럼 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> [RAG](/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)([검색 증강 생성](/studynote/12_it_management/05_security_compliance/222_rag_retrieval_augmented_generation/))나 팩트체킹 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 필수
4. **규제 준수**: EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act 등 규정에서 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 고위험(High-[Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)) AI로 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)하여 투명성·안전성 요구

- **📢 섹션 요약 비유**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 도입은 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 도입과 같다. AWS([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 쓰면 빠르고 편하지만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 외부로 나간다. [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 서버([오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) LLaMA)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통제권이 있지만 구축 비용이 크다. 의료·금융 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 반드시 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)를 고려해야 한다.

---

## Ⅴ. 기대효과 및 결론

[파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발의 패러다임을 "[태스크](/studynote/02_operating_system/02_process_thread/150_task/)별 전용 모델 개발"에서 "범용 기반 모델 + 전문화 어댑테이션"으로 전환시켰다. 이 패러다임 전환은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발 민주화(소기업도 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 위에 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구축 가능)와 동시에 소수 빅테크의 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 패권 집중이라는 양날의 검이다. 대한민국의 HyperCLOVA X, EXAONE처럼 국가 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 주권 차원에서 자국어 [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 개발이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 과제로 부상하고 있다.

- **📢 섹션 요약 비유**: [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 세계의 원자력 발전소다. 하나를 지으면(사전 학습) 전국 가정·공장·병원(모든 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에 전기를 공급한다. 건설 비용은 천문학적이지만, 한번 가동하면 수많은 곳에서 동시에 활용된다. 그래서 국가마다 자국 원전([파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)) 확보가 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 패권 경쟁의 핵심이 된 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 사전 학습 (Pre-[training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) | 대규모 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [자기 지도 학습](/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/) / [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)의 핵심 단계 |
| [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) ([Fine-Tuning](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/)) | 다운스트림, 전문화 / [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)을 특정 [태스크](/studynote/02_operating_system/02_process_thread/150_task/)에 적응 |
| [할루시네이션](/studynote/14_data_engineering/05_exam_keywords/251_hallucination_rag_augmented_retrieval_vector_db/) ([Hallucination](/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) | 거짓 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 사실 오류 / [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/)의 핵심 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) |
| [PEFT](/studynote/10_ai/04_ai_ops_ethics/306_peft_lora/)/[LoRA](/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) | 경량 [파인 튜닝](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/), 파라미터 효율 / 대형 모델의 효율적 적응 기법 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 거버넌스 | 편향, [저작권](/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/), EU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Act / [파운데이션 모델](/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/) 배포의 규제 환경 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [파운데이션 모델 (Foundation Model)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/">파운데이션 모델</a></strong>은 마치 스마트폰의 <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>(OS)</strong>처럼, 수많은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 앱(번역기, 챗봇, 코딩 도우미)의 <strong>기반</strong>이 되는 아주 큰 AI예요!
2. 이 거대한 AI를 처음에 <strong>엄청난 양의 글과 정보</strong>로 학습시켜 두면, 나중에 특정 분야(의료, 법률)에 **조금만 더 가르쳐서** 전문 AI로 만들 수 있어요.
3. [GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4, Claude, NAVER의 HyperCLOVA X 같은 것들이 <strong><a href="/studynote/12_it_management/05_security_compliance/225_foundation_model_peft_lora/">파운데이션 모델</a></strong>이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 303 / 420

<- **이전**: [302. GPT (Generative Pre-trained Transformer)](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)
**다음**: [304. 파인 튜닝 (Fine-Tuning)](/studynote/10_ai/04_ai_ops_ethics/304_fine_tuning/) ->

---
