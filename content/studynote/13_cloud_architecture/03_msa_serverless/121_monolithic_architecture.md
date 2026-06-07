---
title: "121. Monolithic Architecture"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 121
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모놀리식 아키텍처는 <strong>전체 애플리케이션이 하나의 <a href="/studynote/15_devops_sre/01_culture_methodology/007_codebase/">코드베이스</a>·빌드·배포 단위로 구성</strong>되는 전통적 구조이며, 모든 기능(UI·비즈니스 로직·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근)이 하나의 프로세스에서 실행된다.
> 2. **가치**: 단순하고 디버깅·테스트가 쉬우며 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 개발 속도가 빠르지만, 규모가 커지면 **빌드 시간 증가·부분 배포 불가·팀 간 코드 충돌·장애 전파** 등의 한계가 발생한다.
> 3. **판단 포인트**: [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)(Micro Services)로의 전환은 <strong>팀 규모·<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 복잡도·배포 빈도</strong>를 기준으로 판단하며, 소규모 팀·[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 스타트업에서는 오히려 <strong>모놀리식이 최적</strong>일 수 있다("Monolith First" [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)).

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    모놀리식 vs MSA                                    |
+-------------------------------------------------------+
|  [모놀리식]                [MSA]                      |
|  +--------------+        +---+ +---+ +---+          |
|  | UI           |        |Svc| |Svc| |Svc|          |
|  | BizLogic     |        | A | | B | | C |          |
|  | DataAccess   |        +---+ +---+ +---+          |
|  | 단일 DB      |          <->     <->     <->            |
|  +--------------+        DB_A  DB_B  DB_C            |
|  하나의 배포 단위         독립 배포·스케일링           |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 모놀리식은 원룸(모든 기능이 한 공간)이고, MSA는 방이 여러 개인 아파트(기능별 독립 공간)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 모놀리식의 장단점

| 장점 | 단점 |
|:---|:---|
| 개발·디버깅 단순 | 빌드 시간 ^ (규모 증가 시) |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 관리 쉬움 | **부분 배포 불가** |
| 호출 오버헤드 없음 | **장애 전파 (단일 프로세스)** |
| [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 속도 빠름 | 팀 간 코드 충돌 |

- **📢 섹션 요약 비유**: 원룸은 혼자 살 때 편리하지만, 가족이 늘어나면 부엌에서 요리하는 동안 거실을 쓸 수 없다(배포 병목).

---

## Ⅲ. 비교 및 연결

| 비교 | 모놀리식 | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
|:---|:---|:---|
| **배포** | 전체 재배포 | **서비스별 독립** |
| <strong><a href="/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | 전체 | **서비스별** |
| **복잡도** | 낮음 ([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)) | **높음 (운영)** |
| **적합** | <strong>소규모·<a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a></strong> | 대규모·복잡 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Monolith First [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (Martin Fowler)
1. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에는 모놀리식으로 빠르게 개발.
2. [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계가 명확해지면 서비스를 분리.
3. "처음부터 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)"는 과잉 엔지니어링 위험.

---

## Ⅴ. 기대효과 및 결론

모놀리식은 <strong>MSA의 반대가 아닌 출발점</strong>이며, 적절한 시점에 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계를 따라 서비스를 분리하는 것이 현실적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **모놀리식** | 단일 [코드베이스](/studynote/15_devops_sre/01_culture_methodology/007_codebase/)·배포 단위 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a></strong> | 서비스별 독립 배포·[스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) |
| <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/599_modular_monolith_architecture/">Modular Monolith</a></strong> | 모놀리식 + [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 경계 (절충안) |
| **Monolith First** | Martin Fowler의 점진적 전환 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/">Strangler Fig</a></strong> | 모놀리식->[MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 점진 마이그레이션 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 (전통, ~2010s)]
    |
    v
[SOA (Service Oriented Architecture, 2005~)]
    |
    v
[MSA (2014, Netflix·Amazon) — 서비스 분리]
    |
    v
[Modular Monolith (2020~) — 모놀리식 + 모듈 경계]
    |
    v
[현재: "Right-sizing" — 상황에 맞는 아키텍처 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 모놀리식은 <strong>원룸</strong>이에요. 혼자 살 때는 편리하지만, **가족이 늘면** 좁아요.
2. MSA는 <strong>방이 여러 개인 아파트</strong>예요. 각자 방에서 독립적으로 생활할 수 있어요.
3. 처음에는 원룸(모놀리식)에서 시작하고, 가족이 늘면 <strong>아파트(<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)로 이사</strong>하는 게 좋답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 371

<- **이전**: [120. Pod Eviction과 QoS Class (K8s 리소스 관리) - Guaranteed·Burstable·BestEffort](/studynote/13_cloud_architecture/07_container_k8s/120_pod_eviction_qos_class_kubernetes/)
**다음**: [122. MSA (Microservices Architecture) - 서비스별 독립 배포·스케일링 아키텍처](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/) ->

---
