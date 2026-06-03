+++
title = "256. 연합 학습 (Federated Learning) 프라이버시 모델 보안"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연합 학습(Federated [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))은 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 서버에 모으지 않고, 각 디바이스에서 로컬 훈련 후 그래디언트(Gradient)만 집계하여 전역 모델(Global Model)을 개선하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) ML 패러다임이다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 규제 준수([GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/)), 낮은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 비용을 동시에 달성하며 의료·금융·모바일 키보드 등 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역의 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습을 가능하게 한다.
> 3. **판단 포인트**: 그래디언트 역전(Gradient Inversion) 공격으로 그래디언트에서 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복원할 수 있으므로, [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/)([Differential Privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/))·안전 집계(Secure Aggregation) 추가 계층이 필수이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 중앙 집중형 ML의 프라이버시 문제

전통적인 ML은 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙 서버에 모아 훈련한다. 하지만 다음 시나리오에서 이 방식은 불가능하다.

| 시나리오 | 문제 |
|:---|:---|
| 병원 간 환자 [데이터 공유](/knowledge-base/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) | [HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/) 위반 |
| 스마트폰 타이핑 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 침해 |
| 은행 간 사기 탐지 모델 공유 | 금융 정보 유출 |
| 자동차 제조사 주행 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 영업 비밀 노출 |

### 1.2 연합 학습의 탄생

구글은 2017년 Gboard(스마트폰 키보드) 다음 단어 예측에 처음 적용했다. 수억 개의 스마트폰에서 타이핑 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 서버로 보내지 않고, 각 폰에서 학습 후 모델 파라미터만 전송한다.

📢 **섹션 요약 비유**: 연합 학습은 "각 셰프가 자기 비법 레시피를 공개하지 않고, 음식을 만들어 맛만 평가단에게 제출한 후 종합 평가를 받아 실력을 키우는 요리 대회"와 같다. 비법(원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 숨기고 맛(그래디언트)만 공유한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 연합 학습 기본 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│               연합 학습 (Federated Learning) 아키텍처            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              ┌─────────────────────┐                            │
│              │   중앙 서버 (Server) │                            │
│              │  - 전역 모델 관리   │                             │
│              │  - 그래디언트 집계  │                             │
│              └──────────┬──────────┘                            │
│                         │                                       │
│              ① 전역 모델 배포 (Global Model Broadcast)           │
│                         │                                       │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ 클라이언트1  │ │ 클라이언트2  │ │ 클라이언트3  │               │
│  │ (병원 A)    │ │ (병원 B)    │ │ (병원 C)    │               │
│  │             │ │             │ │             │               │
│  │ ② 로컬 데이터│ │ ② 로컬 데이터│ │ ② 로컬 데이터│               │
│  │   로컬 훈련  │ │   로컬 훈련  │ │   로컬 훈련  │               │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘               │
│         │               │               │                       │
│         └───────────────┼───────────────┘                       │
│                         │                                       │
│              ③ 로컬 그래디언트 업로드                             │
│                         │                                       │
│              ④ FedAvg 집계 → 전역 모델 갱신                      │
│                                                                  │
│  ① ~ ④ 반복 (Round)                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 FedAvg(Federated Averaging) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)

FedAvg는 연합 학습의 표준 집계 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

```
FedAvg 수식:
W_global ← Σ (nₖ/N) × W_k

nₖ: 클라이언트 k의 데이터 수
N: 전체 데이터 수
W_k: 클라이언트 k의 로컬 모델 파라미터

특징:
- 데이터가 많은 클라이언트의 영향력이 큼 (가중 평균)
- Non-IID(Independent Identically Distributed) 문제:
  각 클라이언트 데이터가 다른 분포를 가질 때 수렴 어려움
```

### 2.3 Non-IID [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 문제와 해결책

| 문제 | 설명 | 해결 기법 |
|:---|:---|:---|
| **통계적 이질성(Statistical Heterogeneity)** | 각 클라이언트 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분포가 다름 | FedProx, SCAFFOLD |
| **시스템 이질성(System Heterogeneity)** | 클라이언트 컴퓨팅 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이 | 비동기 집계, 클라이언트 선택 |
| **통신 효율** | 대규모 그래디언트 전송 비용 | 그래디언트 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 희소화 |

📢 **섹션 요약 비유**: FedAvg는 여러 학교에서 수학 시험을 치른 후 학교별 평균 성적을 학생 수 비율로 합산해 전국 평균을 구하는 것과 같다. 학생 수가 많은 학교일수록 전국 평균에 미치는 영향이 크다.

---

## Ⅲ. 비교 및 연결

### 3.1 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 기법 계층

```
┌─────────────────────────────────────────────────────────────────┐
│              연합 학습 프라이버시 방어 계층                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: 로컬 차등 프라이버시 (Local DP)                        │
│    → 각 클라이언트가 그래디언트에 가우시안 노이즈 추가            │
│    → ε-DP 보장: Pr[M(x)∈S] ≤ eᵉ × Pr[M(x')∈S]                │
│                                                                  │
│  Layer 2: 안전 집계 (Secure Aggregation)                         │
│    → 비밀 분산 (Secret Sharing) 기반 암호화                      │
│    → 서버는 개별 클라이언트 그래디언트를 볼 수 없음              │
│                                                                  │
│  Layer 3: 동형 암호화 (Homomorphic Encryption)                   │
│    → 암호화된 상태에서 그래디언트 집계 연산                      │
│    → 가장 강력하지만 계산 비용 매우 높음                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 그래디언트 역전(Gradient Inversion) 공격

```
공격 원리:
클라이언트 그래디언트 ∇W → 역최적화 → 원본 입력 데이터 복원

방어 수단:
1. 배치 크기 증가 (배치 클수록 복원 어려움)
2. 그래디언트 클리핑(Gradient Clipping)
3. 차등 프라이버시 노이즈 추가 (ε ≤ 8 권장)
4. 안전 집계로 개별 그래디언트 서버 노출 방지
```

### 3.3 연합 학습 유형 비교

| 유형 | 특징 | 예시 |
|:---|:---|:---|
| **수평 연합 학습(Horizontal FL)** | 동일 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/), 다른 샘플 (클라이언트 다수) | 스마트폰 여러 대 |
| **수직 연합 학습(Vertical FL)** | 다른 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/), 동일 샘플 (소수 기관 협업) | 은행+보험사 동일 고객 |
| **연합 [전이 학습](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/)(Federated [Transfer Learning](/knowledge-base/studynote/10_ai/02_dl_architecture_new/132_transfer_learning/))** | [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)·샘플 모두 다를 때 사전학습 활용 | 글로벌 기업 간 협업 |

📢 **섹션 요약 비유**: 수평 연합 학습은 전국 각 학교가 같은 수업 내용을 다른 학생들에게 가르치는 것이고, 수직 연합 학습은 한 학생을 국어 선생님·수학 선생님·영어 선생님이 각자 다른 과목 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 갖고 협력 평가하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 의료 분야 적용 사례: 암 진단 모델

```
시나리오: 희귀암 진단 모델 개발
- 병원 A (서울): 환자 500명, CT 스캔 데이터
- 병원 B (부산): 환자 300명, CT 스캔 데이터
- 병원 C (대구): 환자 200명, CT 스캔 데이터

문제: 희귀암이라 단일 병원 데이터로 모델 성능 불충분
해결: 수평 연합 학습으로 데이터 공유 없이 1,000명 모델 학습
보호: 차등 프라이버시 (ε=4) + 안전 집계 적용
결과: AUROC 0.82 → 0.94 향상 (단일 병원 대비)
```

### 4.2 금융 분야: 사기 탐지 모델

| 참여 기관 | 보유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 기여 |
|:---|:---|:---|
| 카드사 A | 신용카드 거래 패턴 | 수평 FL |
| 카드사 B | 해외 거래 패턴 | 수평 FL |
| 전기통신사 | 동일 고객 통신 패턴 | 수직 FL |

### 4.3 기술사 논술 핵심 포인트

- **프라이버시-유틸리티 트레이드오프**: DP 노이즈 증가 → 프라이버시 ↑, 모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) ↓
- **클라이언트 참여 유인(Incentive)**: [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 기반 기여도 보상 시스템
- **규제 연계**: [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) Article 25 (프라이버시 바이 디자인) 충족 메커니즘으로 활용

📢 **섹션 요약 비유**: 연합 학습은 각 나라가 핵 기술을 공유하지 않고 핵발전 안전 기준만 IAEA(국제원자력기구)에 보고하는 것과 같다. 실제 기술([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 각국이 갖고, 안전 수준(모델 파라미터)만 공유하여 전 세계 핵 안전을 높인다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 연합 학습 기대효과

| 기대효과 | 세부 내용 |
|:---|:---|
| **프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)** | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 없음, [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[HIPAA](/knowledge-base/studynote/09_security/17_framework_compliance/863_hipaa/) 준수 |
| **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 확장성** | 단일 기관 불가능한 희귀 사례 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합 학습 |
| **통신 비용 절감** | 모델 파라미터만 전송 (원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 대비 수십~수백배 감소) |
| **온디바이스 개인화** | 각 클라이언트 로컬 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 개인화 모델 미세조정 |
| **지적 재산 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 유지하면서 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 협력 가능 |

### 5.2 결론

연합 학습은 AI의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 굶주림([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Hunger)과 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)의 근본적 갈등을 해결하는 핵심 기술이다. FedAvg가 기본 집계를 담당하고, [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/)와 안전 집계가 프라이버시 방어를 강화하는 세 계층 구조가 실무 표준이다. 특히 의료·금융·통신 분야에서 규제 준수와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 발전을 동시에 달성하는 유일한 솔루션으로 자리매김하고 있다.

📢 **섹션 요약 비유**: 연합 학습은 비밀 유지 각서를 쓴 연구자들이 각자 실험실에서 연구하고 결론만 공유하는 공동 연구 프로젝트다. 비법([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 각자 지키면서도 집단 지성(전역 모델)의 혜택을 누릴 수 있다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 패러다임 | 연합 학습(Federated [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 로컬 훈련 + 그래디언트 집계 |
| 집계 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | FedAvg(Federated Averaging) | 가중 평균 그래디언트 집계 |
| 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/)([Differential Privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/)) | 그래디언트 노이즈 추가 |
| 암호화 집계 | 안전 집계(Secure Aggregation) | 비밀 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 기반 암호화 |
| 공격 유형 | 그래디언트 역전(Gradient Inversion) | 그래디언트로 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복원 |
| 수평 FL | 동일 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)·다른 샘플 | 스마트폰, 병원 동일 질환 |
| 수직 FL | 다른 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)·동일 샘플 | 은행+보험사 협업 |
| 규제 연계 | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) Article 25 | 프라이버시 바이 디자인 |

### 👶 어린이를 위한 3줄 비유 설명
1. 연합 학습은 각자 일기장(개인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 비공개로 두고, 일기에서 배운 [교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)(그래디언트)만 선생님께 말씀드리는 거예요—비밀은 지키면서 다 같이 성장해요.

### 📈 관련 키워드 및 발전 흐름도

```text
중앙 집중 학습 (데이터 이동 필요)
    │
    ▼
연방 학습: 데이터는 로컬 유지 + 모델 업데이트만 교환
    ├─► FedAvg: 글로벌 모델 평균 집계
    └─► 차분 프라이버시 + 보안 집계
    │
    ▼
모델 포이즈닝 방어 · 비IID 데이터 대응
```
2. [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/)는 [교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)을 말할 때 일부러 약간 틀리게 말해서 원래 일기 내용을 알 수 없게 만드는 방법이에요.
3. 그래디언트 역전 공격은 "[교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)만 들어도 원래 일기 내용을 알아낼 수 있다"는 해킹 방법인데, [차등 프라이버시](/knowledge-base/studynote/16_bigdata/10_governance/209_differential_privacy/)가 이걸 막아줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 256 / 258

← **이전**: [255. XAI (Explainable AI) 설명 가능 AI LIME SHAP 기여도 분할](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/255_xai_lime_shap_explainable_contribution/)
**다음**: [257. 빅데이터 분석 클라우드 파이프라인 통합 아키텍처 종합](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/257_bigdata_analysis_cloud_pipeline_integration/) →

---
