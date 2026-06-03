+++
title = "200. 자율주행 모방 학습 (Imitation Learning) 시뮬레이터 디지털 트윈 합성 데이터 생성"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모방 학습(Imitation [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/))은 전문가 시연(Expert Demonstration)에서 행동 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))을 학습하는 방법으로, 보상 함수 설계 없이 복잡한 자율주행 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 효율적으로 획득한다.
> 2. **가치**: [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)([Digital Twin](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)) 기반 시뮬레이터로 현실에서 수집 불가능한 위험 상황(코너 케이스)을 안전하게 무한 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 갭([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Gap) 극복이 자율주행 AI의 핵심 과제다.
> 3. **판단 포인트**: DAgger(Dataset Aggregation)는 BC(Behavioral Cloning)의 분포 이탈(Covariate Shift) 문제를 반복적 전문가 피드백으로 해결하지만, 실제 전문가 비용과 [합성 데이터](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/)의 현실성 사이의 트레이드오프를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 자율주행 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습의 도전

자율주행은 인간의 생명을 다루는 안전 크리티컬(Safety-Critical) 시스템이다. 기존 강화학습(RL)은 시행착오를 통해 학습하는데, 실제 도로에서의 실패는 사고를 의미한다.

| 학습 방법 | 장점 | 단점 |
|:---|:---|:---|
| 지도학습 (SL) | 간단, 인간 레이블 활용 | 엣지 케이스 대응 어려움 |
| 강화학습 (RL) | 최적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 탐색 가능 | 보상 설계 어려움, 안전 위험 |
| 모방 학습 (IL) | 전문가 경험 직접 학습 | 분포 이탈, 전문가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 |
| 시뮬레이션 기반 | 무한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 안전 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 갭 (Sim-to-Real) |

### 1.2 모방 학습 (Imitation [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/)) 정의

모방 학습은 전문가(Expert)의 상태-행동 시연 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) `{(s₁,a₁), (s₂,a₂), ..., (sₙ,aₙ)}`에서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) `π: S → A`를 학습하는 방법이다. 보상 함수(Reward Function) 설계 없이 직접 전문가 행동을 모방한다.

### 1.3 자율주행 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 현실

```
실제 주행 데이터 수집 현황 (예시)

Waymo: 2,000만 마일 실제 주행 + 수십억 마일 시뮬레이션
Tesla: 수억 마일 실제 주행 Autopilot 데이터 수집
       
문제점:
  ├─ 일반 주행: 충분 (고속도로, 시내 정상 주행)
  ├─ 코너 케이스: 매우 부족
  │   ├─ 역주행 차량 대응
  │   ├─ 악천후 + 공사 구간 + 보행자 조합
  │   ├─ 신호등 오작동
  │   └─ 갑작스러운 장애물 등장
  └─ 해결책: 시뮬레이터로 코너 케이스 무한 생성
```

📢 **섹션 요약 비유**: 모방 학습은 운전 교습소에서 교관(전문가)의 운전을 옆에서 관찰하며 배우는 것이다. 보상 점수 없이도 "저렇게 하면 되는구나"를 직접 보고 따라한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 BC (Behavioral Cloning, 행동 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))

BC는 가장 단순한 모방 학습 방법으로, 전문가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지도학습으로 직접 모방한다.

```
BC 학습 구조

전문가 데이터셋 D = {(s₁,a₁), ..., (sₙ,aₙ)}
  │
  ▼
지도학습: π_θ = argmin E_{(s,a)~D} [L(π_θ(s), a)]
  │
  ▼
학습된 정책 π_θ 배포

BC 문제점: 분포 이탈 (Covariate Shift)
─────────────────────────────────────
전문가가 방문한 상태: S_expert
학생 정책이 방문하는 상태: S_student

학생의 작은 오류 → 새로운 상태 진입
→ 훈련 분포(S_expert) 밖 → 더 큰 오류
→ 오류 누적 (Compounding Error)

예시:
  전문가: 항상 차선 중앙 유지
  학생: 0.1m 오른쪽으로 조금 이탈
  → 차선 가장자리 상태 (훈련에 없음)
  → 잘못된 스티어링 → 더 큰 이탈 → 충돌
```

### 2.2 DAgger (Dataset Aggregation)

DAgger는 Ross et al. (2011)이 제안한 BC의 분포 이탈 문제 해결 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

```
DAgger 반복 알고리즘

초기화: D = {} (빈 데이터셋)

for 반복 t = 1, 2, ..., T:
  1. 현재 정책 π_t로 환경 실행
     → 학생 정책이 방문하는 상태 S_t 수집

  2. 전문가에게 S_t 상태에서 올바른 행동 질의
     → 전문가 레이블 a* = π_expert(s), ∀s ∈ S_t

  3. 새 데이터 추가: D = D ∪ {(s, a*) | s ∈ S_t}

  4. D에서 새 정책 π_{t+1} 학습

결과: 학생이 방문하는 모든 상태에 전문가 레이블
     → 분포 이탈 문제 해결!

단점: 매 반복마다 전문가 개입 필요 (비용 높음)
```

### 2.3 모방 학습 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 핵심 아이디어 | 장점 | 단점 |
|:---|:---|:---|:---|
| BC (Behavioral Cloning) | 지도학습으로 전문가 모방 | 간단, 구현 쉬움 | 분포 이탈 |
| DAgger | 반복적 전문가 피드백 | 분포 이탈 해결 | 전문가 비용 높음 |
| GAIL (Generative Adversarial IL) | GAN으로 보상 함수 학습 | 보상 함수 불필요 | 학습 불안정 |
| IRL (Inverse RL) | 전문가 행동에서 보상 추론 | 보상 해석 가능 | 계산 비용 높음 |

### 2.4 [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) ([Digital Twin](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)) 기반 시뮬레이션

```
자율주행 디지털 트윈 아키텍처

┌────────────────────────────────────────────────────────────┐
│              실제 세계 (Real World)                         │
│                                                            │
│  LiDAR, 카메라, GPS, HD 맵 → 3D 환경 재현                   │
└────────────────────────────┬───────────────────────────────┘
                             │ 3D 스캔/측정 데이터
                             ▼
┌────────────────────────────────────────────────────────────┐
│            디지털 트윈 (시뮬레이터)                          │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ 물리 엔진     │  │ 렌더링 엔진  │  │ 교통 흐름 모델   │ │
│  │ (충돌, 마찰)  │  │ (포토리얼)   │  │ (차량, 보행자)   │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                            │
│  코너 케이스 자동 생성:                                     │
│  ├─ 폭우 + 야간 + 공사 구간                                 │
│  ├─ 역주행 오토바이                                         │
│  ├─ 갑자기 뛰어드는 보행자                                  │
│  └─ 신호등 오작동 + 안개                                    │
└────────────────────────────┬───────────────────────────────┘
                             │ 학습 데이터 (무한 생성)
                             ▼
┌────────────────────────────────────────────────────────────┐
│              AI 모델 학습                                    │
│  모방 학습(BC/DAgger) + 강화학습 + 데이터 증강               │
└────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: DAgger는 피아노 교습과 같다. 처음에는 악보(BC)로만 연습하다가, 실수하는 부분(분포 이탈)이 생기면 선생님(전문가)이 직접 시범을 보여준다(레이블링). 반복할수록 모든 어려운 부분에 대한 정확한 지도가 쌓인다.

---

## Ⅲ. 비교 및 연결

### 3.1 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 갭 ([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Gap, Sim-to-Real Gap) 극복

시뮬레이터에서 학습한 모델이 실제 환경에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되는 현상이다.

```
도메인 갭 발생 원인 및 해결책

원인:
  ├─ 렌더링 품질 차이 (텍스처, 조명)
  ├─ 물리 시뮬레이션 오차 (마찰, 공기 저항)
  ├─ 센서 노이즈 모델 부정확
  └─ 교통 참여자 행동 모델 단순화

해결책:
┌──────────────────────────────────────────────────────┐
│  1. 도메인 랜덤화 (Domain Randomization)              │
│     시뮬레이터 파라미터를 랜덤하게 변경               │
│     (텍스처, 조명, 물체 위치, 센서 노이즈)            │
│     → 모델이 다양한 환경에 일반화                     │
│                                                      │
│  2. 포토리얼리스틱 렌더링 (Photorealistic Rendering)  │
│     NVIDIA DRIVE Sim, CARLA 고품질 렌더링             │
│     → 시뮬-현실 시각적 차이 최소화                    │
│                                                      │
│  3. 도메인 적응 (Domain Adaptation)                  │
│     실제 도메인 소량 데이터 + 시뮬 대용량 데이터      │
│     → Transfer Learning으로 갭 보정                  │
│                                                      │
│  4. 현실 데이터 증강 (Real Data Augmentation)        │
│     실제 이미지 + 합성 객체 삽입 (Cut-Paste)          │
│     → 코너 케이스 현실적 합성                         │
└──────────────────────────────────────────────────────┘
```

### 3.2 주요 자율주행 시뮬레이터 비교

| 시뮬레이터 | 개발사 | 특징 | 주요 사용처 |
|:---|:---|:---|:---|
| CARLA | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 포토리얼, 다양한 시나리오 | 연구 |
| SUMO | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 교통 흐름 특화 | 교통 연구 |
| NVIDIA DRIVE Sim | NVIDIA | 최고 품질 렌더링 | 산업용 |
| Waymo Simulation | Waymo | 폐쇄적, 대규모 | Waymo 내부 |
| AirSim | Microsoft | 드론/자동차 | 연구 |
| Carcraft | Waymo | 재현 시뮬레이션 | 사고 재현 |

### 3.3 [합성 데이터](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/) ([Synthetic Data](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/)) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
합성 데이터 생성 파이프라인

실제 사고 데이터 수집
    │
    ▼
디지털 트윈 재현 (사고 상황 정확 복제)
    │
    ▼
파라미터 변형 (무한 변형 생성)
  ├─ 날씨: 맑음/비/눈/안개 × 시간대 4 × 강도 5 = 80가지
  ├─ 도로: 건식/습식/동결 × 경사도 5 = 15가지
  ├─ 교통: 차량 밀도 5 × 속도 5 = 25가지
  └─ 코너케이스: 보행자 행동 10 × 차량 행동 10 = 100가지
  
  총: 약 3,000+ 변형 시나리오 자동 생성
    │
    ▼
AI 모델 학습 및 검증
    │
    ▼
실제 데이터로 도메인 적응 Fine-tuning
```

📢 **섹션 요약 비유**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 랜덤화는 운전 연습을 다양한 날씨와 도로 조건에서 하는 것과 같다. 항상 맑은 날 고속도로만 연습하면 빗길 좁은 골목에서 당황하지만, 다양한 조건에서 연습하면 어떤 상황에서도 대응할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 자율주행 학습 파이프라인 설계

```
자율주행 AI 개발 파이프라인

1. 실제 데이터 수집
   ├─ Fleet 차량 데이터 수집 (정상 주행)
   └─ 사고/위험 상황 레이블링

2. 시뮬레이터 구축
   ├─ 디지털 트윈 환경 구성
   ├─ 코너 케이스 시나리오 설계
   └─ 전문가 데모 데이터 생성

3. 모방 학습
   ├─ BC로 기본 정책 학습
   ├─ DAgger로 분포 이탈 보완
   └─ GAIL/IRL로 정제

4. 강화학습 Fine-tuning
   └─ 시뮬레이터에서 RL로 최적화

5. 도메인 적응
   └─ 실제 데이터로 Transfer Learning

6. 안전 검증
   ├─ 시뮬레이터 10억 마일 가상 주행
   └─ 폐쇄 구간 실도로 테스트
```

### 4.2 코너 케이스 (Corner Case) 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

| 카테고리 | 예시 시나리오 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 방법 |
|:---|:---|:---|
| 극한 기상 | 폭설 + 야간 + 글레어 | 시뮬레이터 파라미터 |
| 비정상 교통 참여자 | 역주행 오토바이, 취한 보행자 | 행동 모델 변형 |
| 인프라 장애 | 신호등 오작동, 차선 표시 훼손 | 환경 훼손 모델 |
| 복합 상황 | 공사 + 구급차 + 자전거 동시 | 시나리오 조합 |
| 희귀 물체 | 트랙터, 가축, 이상한 적재물 | [GAN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/) 합성 |

### 4.3 기술사 논술 핵심 판단 기준

| 논점 | 핵심 내용 |
|:---|:---|
| BC vs DAgger 선택 | 전문가 비용 허용 범위로 결정 |
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 갭 극복 | 랜덤화 + 포토리얼 + [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 적응 3단계 조합 |
| [합성 데이터](/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/) 한계 | 물리 법칙 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) + 비전 품질이 핵심 |
| 안전 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 시뮬 10억 마일 + 실도로 점진적 확장 |

### 4.4 자율주행 안전성 입증 방법론

```
자율주행 안전 검증 피라미드

       실도로 상용화
      /              \
    폐쇄 구간 파일럿
   /                  \
  SIL(소프트웨어 통합 테스트)
 /                      \
HiL(하드웨어 통합 테스트)
/                          \
시뮬레이터 테스트 (수십억 마일)
```

📢 **섹션 요약 비유**: 자율주행 코너 케이스 수집은 항공기 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스와 같다. 실제 사고가 드물어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 부족하므로, 시뮬레이터로 "만약 이런 상황이라면?"을 무한 재현하여 모든 가능한 위험 상황을 안전하게 학습한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 시뮬레이션 기반 학습 기대효과

| 효과 | 정량 지표 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 비용 | 실제 대비 99% 절감 |
| 코너 케이스 커버리지 | 실제 수집 대비 100배+ |
| 안전성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 속도 | 실도로 대비 1,000배+ |
| 사고 위험 | 시뮬레이션에서 0 (안전한 실험) |
| 레이블링 비용 | 자동 레이블로 90% 절감 |

### 5.2 자율주행 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 미래 방향

```
자율주행 AI 기술 발전

현재 (2024, SAE Level 2~3):
  ├─ 모방 학습 + RL 조합
  ├─ 단일 도시 지오펜싱 운영
  └─ 원격 모니터링 의존

단기 (2025~2027, SAE Level 4):
  ├─ 멀티모달 대형 모델 (카메라 + LiDAR + 언어)
  ├─ 세계 모델(World Model) 기반 예측
  └─ 도심 전역 운영

장기 (2030+, SAE Level 5):
  ├─ 완전 자율 (모든 조건, 지역 제한 없음)
  └─ V2X + 인프라 연계 협력 주행
```

### 5.3 결론 요약

자율주행 모방 학습과 [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) 시뮬레이션은 안전 크리티컬 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템 개발의 현실적 해결책이다. BC의 분포 이탈 문제를 DAgger로 보완하고, 시뮬레이터로 현실 수집 불가능한 코너 케이스를 무한 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 방법론이 자율주행 안전성의 핵심이다. 기술사 관점에서는 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 갭 극복 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 3가지(랜덤화·포토리얼·<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 적응), BC vs DAgger의 트레이드오프, <a href="/knowledge-base/studynote/09_security/16_data_privacy/818_synthetic_data/">합성 데이터</a>의 품질 평가 방법</strong>을 명확히 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: 자율주행 [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)은 비행기 조종사 훈련용 비행 시뮬레이터와 같다. 실제 비행기(자동차)를 타기 전에 시뮬레이터(CARLA)로 모든 비상 상황(코너 케이스)을 수천 번 연습하여 실제 상황에서도 침착하게 대응할 수 있도록 한다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기법 | Imitation [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) (모방 학습) | 전문가 시연에서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 학습 |
| 기본 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | BC (Behavioral Cloning) | 지도학습 방식 모방 |
| 개선 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | DAgger (Dataset Aggregation) | 반복적 전문가 피드백 |
| 고급 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | GAIL | [GAN](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/154_gan_generative_adversarial_network/) 기반 보상 없는 모방 |
| 인프라 | [Digital Twin](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) ([디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/)) | 현실 환경의 가상 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) |
| 시뮬레이터 | CARLA | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 자율주행 시뮬레이터 |
| 문제 | Covariate Shift (공변량 이탈) | 훈련-테스트 분포 불일치 |
| 문제 | [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Gap ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 갭) | 시뮬-현실 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이 |
| 해결책 | [Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Randomization | 시뮬 파라미터 랜덤화 |

### 👶 어린이를 위한 3줄 비유 설명

1. 모방 학습은 운전 교관(전문가) 옆에 앉아서 운전하는 모습을 보고 배우는 거예요. 직접 스티어링 휠을 잡지 않아도, 보면서 "아, 이렇게 하면 되는구나"를 배우죠.

### 📈 관련 키워드 및 발전 흐름도

```text
규칙 기반 제어 (if-then 로직)
    │
    ▼
모방 학습 (Imitation Learning)
    ├─► 행동 복제 (Behavior Cloning): 전문가 시연 → 지도 학습
    ├─► DAgger: 분포 불일치 보정 (반복 레이블링)
    └─► IRL (Inverse RL): 보상 함수 역추론
    │
    ▼
시뮬레이터 · 디지털 트윈
    ├─► CARLA · LGSVL · NVIDIA Isaac
    └─► 합성 데이터 생성: 도메인 랜덤화
    │
    ▼
Sim-to-Real Transfer → 실차 배포 · V2X 통신
```
2. DAgger는 피아노 학원에서 틀린 부분만 선생님이 다시 시범 보여주는 것이에요. 연습하다가 막히는 부분(분포 이탈)에 딱 맞는 가르침(전문가 레이블)이 쌓여요.
3. [디지털 트윈](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/126_digital_twin_concept/) 시뮬레이터는 자동차 게임 같아요. 게임에서는 충돌해도 다시 살아나기 때문에, 현실에서 절대 못 해볼 위험한 상황(역주행 차, 폭설)을 안전하게 연습할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 200 / 258

← **이전**: [199. 인텐트 기반 네트워킹 (IBN, Intent-Based Networking) 트래픽 AI 라우팅 분배망](/knowledge-base/studynote/14_data_engineering/04_mlops/199_intent_based_networking_ibn_ai_traffic_routing/)
**다음**: [201. 빅데이터 3V·5V 특성 (Big Data 3V·5V Characteristics)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/201_bigdata_3v_5v_volume_velocity_variety/) →

---
