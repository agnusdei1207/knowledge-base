---
title: "210. Synthetic Data"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)([Synthetic Data](/studynote/09_security/16_data_privacy/818_synthetic_data/))는 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 통계적 특성·패턴을 학습하여 원본 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)를 포함하지 않으면서 통계적으로 동등한 가상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 기술로, [GAN](/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/)·[VAE](/studynote/06_ict_convergence/04_ai_llm/315_autoencoder_vae/)·통계적 방법론이 주요 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 기법이다.
- **가치**: [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/PIPA 준수 하에 ML 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 확보, 소프트웨어 테스트 환경의 현실적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공급, 희귀 사례(Rare Event) 증강, 조직 간 [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 등 다양한 활용이 가능하다.
- **판단 포인트**: [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 품질은 Fidelity(원본과의 통계적 유사성)·Utility(ML 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 동등성)·Privacy([멤버십 추론 공격](/studynote/09_security/19_ai_advanced_security/952_membership_inference/) [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)성)의 3중 평가 체계로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 하며, 세 지표 간 트레이드오프가 설계 핵심이다.

---

## Ⅰ. 개요 및 필요성

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)가 필요한 상황

현실에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용을 막는 주요 장벽들:

| 장벽 | 내용 | [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 해결 방안 |
|:---|:---|:---|
| <strong><a href="/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a> <a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong> | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/PIPA로 원본 공유 불가 | 원본 없는 합성본 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·공유 |
| **희귀 사례 부족** | 사기 거래, 희귀 질환 등 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 극소 | 합성으로 소수 클래스 증강 |
| **테스트 환경** | 개발자에게 실제 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 불가 | 현실적 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)로 대체 |
| **조직 간 협업** | 법인 간 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 불가 | [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)로 모델 협력 개발 |
| **신규 시나리오** | 아직 발생하지 않은 사례 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없음 | 시뮬레이션 기반 합성 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

**📢 섹션 요약 비유**: [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)는 <strong>스턴트 배우</strong>와 같다. 위험한 장면([개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 처리)에 실제 배우(실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 대신 스턴트 배우([합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/))를 쓰되, 외모와 동작(통계적 특성)은 거의 동일하게 유지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 방법론 3종

```
+-------------------------------------------------------------+
|              합성 데이터 생성 방법론                         |
+--------------------------------------------------------------+
|  1. GAN 기반 (Generative Adversarial Network)               |
|  +--------------------------------------------------------+ |
|  |  생성기(Generator) <--> 판별기(Discriminator) 적대적 학습| |
|  |                                                        | |
|  |  CTGAN (Conditional Tabular GAN):                      | |
|  |  - 수치형+범주형 혼합 표 형식 데이터 처리 최적화        | |
|  |  - 조건부 생성으로 희귀 범주 불균형 해결                | |
|  |                                                        | |
|  |  TVAE (Tabular Variational Autoencoder):                | |
|  |  - 잠재 공간(Latent Space) 기반 연속 생성              | |
|  |  - 수치형 데이터 분포 재현 우수                         | |
|  +--------------------------------------------------------+ |
+--------------------------------------------------------------+
|  2. 통계적/코퓰러(Copula) 기반                              |
|  +--------------------------------------------------------+ |
|  |  SDV (Synthetic Data Vault) 라이브러리:                 | |
|  |  - Gaussian Copula: 컬럼 간 상관구조 보존               | |
|  |  - 조건부 분포: 주어진 값에서 다른 값 샘플링           | |
|  |  - 다중 테이블: FK 관계 보존하며 합성 생성             | |
|  +--------------------------------------------------------+ |
+--------------------------------------------------------------+
|  3. 규칙 기반/시뮬레이션                                     |
|  +--------------------------------------------------------+ |
|  |  도메인 전문 지식으로 데이터 생성 규칙 정의             | |
|  |  - 자동차 보험: 나이·운전 이력 기반 사고율 시뮬레이션  | |
|  |  - 사기 탐지: 실제 사기 패턴 기반 시나리오 합성        | |
|  +--------------------------------------------------------+ |
+-------------------------------------------------------------+
```

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 품질 3중 평가 체계

| 평가 축 | 의미 | 측정 방법 |
|:---|:---|:---|
| **Fidelity (충실도)** | 원본과 통계적으로 얼마나 유사한가? | 컬럼별 분포 비교, 상관계수 비교, KS 검정 |
| **Utility (유용성)** | ML 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 얼마나 같은가? | TSTR (Train Synthetic, Test Real): 합성으로 학습, 실제로 평가 |
| **Privacy (프라이버시)** | 재식별 위험이 얼마나 낮은가? | [멤버십 추론 공격](/studynote/09_security/19_ai_advanced_security/952_membership_inference/)(MIA) [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)성, 가장 가까운 실제 레코드 거리 |

**📢 섹션 요약 비유**: [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)의 3중 평가는 <strong>모조품 평가 기준</strong>과 같다. 진품과 얼마나 비슷한지(Fidelity), 실제로 쓸 수 있는지(Utility), 진품 정보를 누출하지 않는지(Privacy) — 세 기준을 모두 통과해야 좋은 모조품이다.

---

## Ⅲ. 비교 및 연결

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) vs 전통적 비식별화

| 차원 | [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) | 가명처리/[마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 |
|:---|:---|:---|
| **원본 레코드 존재** | 없음 (완전 가상) | 있음 (원본 변형) |
| **통계 보존** | 높음 (학습 기반) | 보통 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 보존</strong> | CTGAN 등으로 가능 | 어려움 |
| **재식별 위험** | 낮음 (원본 없음) | 중간 (원본 변형) |
| <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 복잡도</strong> | 높음 | 낮음 |
| <strong><a href="/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a> 상태</strong> | [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 아님 (진정한 합성 시) | 가명정보 |

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 도구 비교

| 도구 | 특징 | 강점 |
|:---|:---|:---|
| **SDV (Python)** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 다중 테이블 지원, CTGAN·TVAE·HMA | 무료, Pandas 통합 |
| <strong>Gretel.<a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">ai</a></strong> | 클라우드 기반 상용+[오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 합성 | 사용 편의, 다양한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 |
| <strong>Mostly <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong> | 엔터프라이즈 전용, 시계열 지원 | 규제 산업 특화 |
| **Syntho** | EU 프라이버시 준수 특화 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 컴플라이언스 |

**📢 섹션 요약 비유**: CTGAN은 <strong>미술 복원가</strong>와 같다. 원본 그림(실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))의 스타일·색상·구도(통계 특성)를 학습하여 원본을 보지 않고도 유사한 새 그림([합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/))을 그릴 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### SDV 활용 예시

```python
from sdv.tabular import CTGAN
from sdv.evaluation import evaluate

# 모델 학습
model = CTGAN(epochs=300)
model.fit(real_data)

# 합성 데이터 생성
synthetic_data = model.sample(num_rows=10000)

# 품질 평가
score = evaluate(synthetic_data, real_data)
print(f"품질 점수: {score}")  # 0-1 사이, 높을수록 좋음
```

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 활용 단계별 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| 단계 | 활용 방식 |
|:---|:---|
| **개발·테스트** | 실제 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 대신 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)로 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)·UI 개발 |
| **ML 모델 개발** | [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)로 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델 개발 후 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 파인튜닝 |
| <strong><a href="/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/">데이터 공유</a></strong> | 파트너사와 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 공유로 공동 분석 |
| **소수 클래스 증강** | [SMOTE](/studynote/14_data_engineering/05_exam_keywords/231_smote_oversampling_class_imbalance_augmentation/)·CTGAN으로 불균형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 보완 |
| **시나리오 테스트** | 극단적 시나리오(블랙 스완) 합성 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

**📢 섹션 요약 비유**: 소수 클래스 증강은 <strong>의학 시뮬레이션</strong>과 같다. 실제 희귀 질환 환자(소수 클래스)가 부족할 때 의학 지식 기반 시뮬레이션 환자를 만들어 의료진 교육(ML 훈련)에 활용하는 것이다.

---

## Ⅴ. 기대효과 및 결론

### [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) 도입 효과

| 영역 | 효과 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 학습 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 준수하에 충분한 ML 훈련 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 확보 |
| **테스트 환경** | 프로덕션 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 위험 없는 현실적 테스트 |
| **개발 속도** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 승인 대기 없이 즉시 개발 가능 |
| **소수 클래스** | 희귀 사기·질환 사례 증강으로 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 |
| **국제 협업** | 국가 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이전 규제 우회 가능 |

### 결론

[합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 프라이버시 패러독스의 실용적 해법</strong>이다. 프라이버시와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유용성이 상충하는 문제를, 통계적 동등성을 유지하는 가상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)으로 해결한다. 그러나 완벽한 해법은 아니다: GAN의 훈련 불안정성, Mode Collapse(일부 패턴만 반복 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)), 원본 특이값 노출 위험 등 기술적 한계가 존재한다. 정보통신기술사는 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)를 "프라이버시 만능 해결책"이 아닌, 구체적인 활용 목적과 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기준을 갖춘 <strong>설계 아이템</strong>으로 접근해야 한다.

**📢 섹션 요약 비유**: [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)는 <strong>드라마 세트장</strong>과 같다. 실제 공항(실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에서 촬영하면 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 문제가 생기지만, 똑같이 만든 세트장([합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/))에서 촬영하면 훨씬 자유롭게 작업할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| CTGAN | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델 | 조건부 표 형식 [GAN](/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/) — 범주형+수치형 혼합 처리 |
| TVAE | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모델 | 표 형식 [VAE](/studynote/06_ict_convergence/04_ai_llm/315_autoencoder_vae/) — 연속적 분포 재현 |
| SDV | Python [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | 다중 테이블 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 통합 프레임워크 |
| Fidelity | 품질 평가 축 | 원본과 합성의 통계적 유사성 |
| Utility | 품질 평가 축 | ML 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 동등성 (TSTR) |
| Privacy | 품질 평가 축 | [멤버십 추론 공격](/studynote/09_security/19_ai_advanced_security/952_membership_inference/) [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)성 |
| [멤버십 추론 공격](/studynote/09_security/19_ai_advanced_security/952_membership_inference/) | 프라이버시 위협 | [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)에서 원본 포함 여부를 역추론하는 공격 |

### 📈 관련 키워드 및 발전 흐름도

```text
[실 데이터 (Real Data) — 개인정보·희귀 이벤트로 수집·공유 제한]
    |
    v
[데이터 증강 (Data Augmentation) — 회전·크롭·노이즈 추가로 다양성 확보]
    |
    v
[합성 데이터 생성 (GAN / VAE / Diffusion Model) — 통계 분포 학습 후 신규 생성]
    |
    v
[품질 검증 (Fidelity / Utility / Privacy 평가) — 실 데이터와 유사성 및 프라이버시 확인]
    |
    v
[AI 모델 학습·테스트 활용 — 데이터 부족·편향·규제 장벽 극복]
```
실 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 수집·공유 한계를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 증강으로 보완하고, [GAN](/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/)/[VAE](/studynote/06_ict_convergence/04_ai_llm/315_autoencoder_vae/) 기반 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)으로 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 규제와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 부족 문제를 동시에 해결한다.

### 👶 어린이를 위한 3줄 비유 설명

- [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)는 <strong>모형 집</strong>과 같아요: 실제 집(실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 대신 건축 설계도를 배운 AI가 만든 모형 집([합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/))은 구조는 비슷하지만 실제 사람이 살지 않아요([개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 없음).
- 좋은 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)는 "진짜 같아 보이고(Fidelity), 실제로 유용하며(Utility), 원본 정보를 노출하지 않는(Privacy)" 세 가지를 모두 만족해야 해요.
- 이 기술 덕분에 병원이나 은행은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발자에게 실제 환자·고객 정보 대신 [합성 데이터](/studynote/09_security/16_data_privacy/818_synthetic_data/)를 제공할 수 있어서, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 걱정 없이 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 개발이 가능해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 210 / 262

<- **이전**: [203. 차등 프라이버시 (Differential Privacy) — 통계 쿼리에 수학적 노이즈 추가](/studynote/16_bigdata/10_governance/209_differential_privacy/)
**다음**: [205. 데이터 윤리 (Data Ethics) — 알고리즘 편향/공정성/투명성](/studynote/16_bigdata/10_governance/211_data_ethics/) ->

---
