---
title: 121. 모놀리식 아키텍처 (Monolithic Architecture) - 단일체 구조의 특징과 한계
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모놀리식 아키텍처는 **전체 애플리케이션이 하나의 [[007_codebase|코드베이스]]·빌드·배포 단위로 구성**되는 전통적 구조이며, 모든 기능(UI·비즈니스 로직·[[001_dikw_pyramid|데이터]] 접근)이 하나의 프로세스에서 실행된다.
> 2. **가치**: 단순하고 디버깅·테스트가 쉬우며 [[459_quic_fec_forward_error_correction|초기]] 개발 속도가 빠르지만, 규모가 커지면 **빌드 시간 증가·부분 배포 불가·팀 간 코드 충돌·장애 전파** 등의 한계가 발생한다.
> 3. **판단 포인트**: [[619_msa_traffic_hardware|MSA]](Micro Services)로의 전환은 **팀 규모·[[064_relation_domain|도메인]] 복잡도·배포 빈도**를 기준으로 판단하며, 소규모 팀·[[459_quic_fec_forward_error_correction|초기]] 스타트업에서는 오히려 **모놀리식이 최적**일 수 있다("Monolith First" [[268_strategy_pattern|전략]]).

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    모놀리식 vs MSA                                    │
├───────────────────────────────────────────────────────┤
│  [모놀리식]                [MSA]                      │
│  ┌──────────────┐        ┌───┐ ┌───┐ ┌───┐          │
│  │ UI           │        │Svc│ │Svc│ │Svc│          │
│  │ BizLogic     │        │ A │ │ B │ │ C │          │
│  │ DataAccess   │        └───┘ └───┘ └───┘          │
│  │ 단일 DB      │          ↕     ↕     ↕            │
│  └──────────────┘        DB_A  DB_B  DB_C            │
│  하나의 배포 단위         독립 배포·스케일링           │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 모놀리식은 원룸(모든 기능이 한 공간)이고, MSA는 방이 여러 개인 아파트(기능별 독립 공간)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 모놀리식의 장단점

| 장점 | 단점 |
|:---|:---|
| 개발·디버깅 단순 | 빌드 시간 ↑ (규모 증가 시) |
| [[191_transaction_concept_states|트랜잭션]] 관리 쉬움 | **부분 배포 불가** |
| 호출 오버헤드 없음 | **장애 전파 (단일 프로세스)** |
| [[459_quic_fec_forward_error_correction|초기]] 속도 빠름 | 팀 간 코드 충돌 |

- **📢 섹션 요약 비유**: 원룸은 혼자 살 때 편리하지만, 가족이 늘어나면 부엌에서 요리하는 동안 거실을 쓸 수 없다(배포 병목).

---

## Ⅲ. 비교 및 연결

| 비교 | 모놀리식 | [[619_msa_traffic_hardware|MSA]] |
|:---|:---|:---|
| **배포** | 전체 재배포 | **서비스별 독립** |
| **[[249_scaling_normalization_standardization|스케일링]]** | 전체 | **서비스별** |
| **복잡도** | 낮음 ([[459_quic_fec_forward_error_correction|초기]]) | **높음 (운영)** |
| **적합** | **소규모·[[459_quic_fec_forward_error_correction|초기]]** | 대규모·복잡 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Monolith First [[268_strategy_pattern|전략]] (Martin Fowler)
1. [[459_quic_fec_forward_error_correction|초기]]에는 모놀리식으로 빠르게 개발.
2. [[064_relation_domain|도메인]] 경계가 명확해지면 서비스를 분리.
3. "처음부터 [[619_msa_traffic_hardware|MSA]]"는 과잉 엔지니어링 위험.

---

## Ⅴ. 기대효과 및 결론

모놀리식은 **MSA의 반대가 아닌 출발점**이며, 적절한 시점에 [[064_relation_domain|도메인]] 경계를 따라 서비스를 분리하는 것이 현실적 [[268_strategy_pattern|전략]]이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **모놀리식** | 단일 [[007_codebase|코드베이스]]·배포 단위 |
| **[[619_msa_traffic_hardware|MSA]]** | 서비스별 독립 배포·[[249_scaling_normalization_standardization|스케일링]] |
| **[[599_modular_monolith_architecture|Modular Monolith]]** | 모놀리식 + [[192_module_independence|모듈]] 경계 (절충안) |
| **Monolith First** | Martin Fowler의 점진적 전환 [[268_strategy_pattern|전략]] |
| **[[310_strangler_fig_pattern|Strangler Fig]]** | 모놀리식→[[619_msa_traffic_hardware|MSA]] 점진 마이그레이션 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 (전통, ~2010s)]
    │
    ▼
[SOA (Service Oriented Architecture, 2005~)]
    │
    ▼
[MSA (2014, Netflix·Amazon) — 서비스 분리]
    │
    ▼
[Modular Monolith (2020~) — 모놀리식 + 모듈 경계]
    │
    ▼
[현재: "Right-sizing" — 상황에 맞는 아키텍처 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 모놀리식은 **원룸**이에요. 혼자 살 때는 편리하지만, **가족이 늘면** 좁아요.
2. MSA는 **방이 여러 개인 아파트**예요. 각자 방에서 독립적으로 생활할 수 있어요.
3. 처음에는 원룸(모놀리식)에서 시작하고, 가족이 늘면 **아파트([[619_msa_traffic_hardware|MSA]])로 이사**하는 게 좋답니다!
