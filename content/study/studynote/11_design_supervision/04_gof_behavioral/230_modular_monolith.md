+++
weight = 230
title = "230. 모듈형 모놀리스 (Modular Monolith)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[599_modular_monolith_architecture|Modular Monolith]] ([[192_module_independence|모듈]]형 모놀리스)는 단일 배포 단위(Monolithic [[087_deployment_kubernetes_workload_rolling_update|Deployment]])를 유지하면서도 내부를 명확한 [[192_module_independence|모듈]] 경계([[192_module_independence|Module]] Boundary)로 분리하여, [[619_msa_traffic_hardware|MSA]] ([[365_msa_microservice_architecture|Microservice Architecture]])의 [[192_module_independence|모듈]]화 이점과 모놀리스의 운영 단순성을 동시에 달성하는 아키텍처다.
> 2. **가치**: [[619_msa_traffic_hardware|MSA]] 전환의 과도기 또는 대안으로, 단일 프로세스의 낮은 운영 복잡도를 유지하면서 [[310_architecture|DDD]] Bounded Context를 기반으로 미래 [[619_msa_traffic_hardware|MSA]] 분리를 대비한 내부 구조를 갖춘다.
> 3. **판단 포인트**: [[192_module_independence|모듈]] 간 통신은 반드시 **공개 인터페이스(Public [[014_api_posix|API]])** 를 통해서만 — [[192_module_independence|모듈]] 내부 클래스의 직접 [[316_reference_pattern_nosql|참조]]는 금지. 이 규칙 위반 감지를 위해 ArchUnit 등의 아키텍처 테스트 도구가 필수다.

---

## Ⅰ. 개요 및 필요성
```
전통 모놀리스의 문제:
  ┌──────────────────────────────────────────────┐
  │  단일 코드베이스 — 스파게티 의존성              │
  │  모든 코드가 서로 참조 가능                     │
  │  → 수정 시 전체 영향도 예측 불가                │
  └──────────────────────────────────────────────┘

MSA의 오버킬:
  ├─ 네트워크 레이턴시 (서비스 간 HTTP/gRPC)
  ├─ 분산 트랜잭션의 복잡성 (Saga, 2PC)
  ├─ 서비스 디스커버리, API Gateway 운영
  ├─ 복수의 DB 관리
  └─ 소규모 팀에게는 운영 부담이 기능 개발 시간 초과

적절한 중간 지점: Modular Monolith
```

- **Shopify**: Ruby on Rails 모놀리스를 [[192_module_independence|모듈]]화하여 수십억 달러 규모 유지
- **[[057_stack|Stack]] [[095_overflow|Overflow]]**: 대부분을 모놀리스로 운영하며 초당 수백만 페이지뷰 처리
- **Basecamp**: 의도적으로 [[619_msa_traffic_hardware|MSA]] 대신 [[192_module_independence|모듈]]형 모놀리스 선택

- **📢 섹션 요약 비유**: [[192_module_independence|모듈]]형 모놀리스는 아파트 건물 — 하나의 건물(단일 배포)이지만 각 세대([[192_module_independence|모듈]])는 독립적인 생활 공간을 가지고, 복도(공개 인터페이스)를 통해서만 서로 방문할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
┌────────────────────────────────────────────────────────────────┐
│                    Modular Monolith                            │
│                (단일 배포, 단일 프로세스)                        │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Public API 계층 (모듈 공개 인터페이스)        │   │
│  └─────────────────────────────────────────────────────────┘   │
│         │                  │                  │                │
│         ▼                  ▼                  ▼                │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐         │
│  │   주문 모듈  │   │   결제 모듈  │   │   배송 모듈  │         │
│  │  (Order BC) │   │ (Payment BC)│   │(Delivery BC)│         │
│  │             │   │             │   │             │         │
│  │  도메인 모델 │   │  도메인 모델 │   │  도메인 모델 │         │
│  │  서비스     │   │  서비스     │   │  서비스     │         │
│  │  레포지토리 │   │  레포지토리 │   │  레포지토리 │         │
│  │  [내부 클래스│   │  [내부 클래스│   │  [내부 클래스│         │
│  │   직접 참조 │   │   직접 참조 │   │   직접 참조 │         │
│  │   금지!]    │   │   금지!]    │   │   금지!]    │         │
│  └─────────────┘   └─────────────┘   └─────────────┘         │
│         │                  │                  │                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              공유 DB (스키마 격리 또는 별도 스키마)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

| 원칙 | 설명 |
|:---|:---|
| **퍼블릭 [[014_api_posix|API]] 강제** | [[192_module_independence|모듈]] 간 통신은 공개 인터페이스만 허용 (내부 구현 은닉) |
| **[[005_schema|스키마]] 격리** | 각 [[192_module_independence|모듈]]은 자신의 DB [[005_schema|스키마]]/테이블만 접근 |
| **순환 의존 금지** | [[192_module_independence|모듈]] A → B → A 순환 의존 불허 |
| **이벤트 기반 통신** | [[192_module_independence|모듈]] 간 결합 최소화 시 [[064_relation_domain|도메인]] 이벤트 활용 |
| **독립 배포 준비** | 향후 [[619_msa_traffic_hardware|MSA]] 분리 시 경계가 자연스럽게 분리선이 됨 |

```java
// module-info.java (Java 9+ JPMS)
module com.example.order {
    exports com.example.order.api;           // 공개 인터페이스만 노출
    requires com.example.payment.api;        // 결제 모듈의 공개 API만 참조
    requires com.example.inventory.api;

    // com.example.order.internal은 exports하지 않음 → 외부 접근 불가
}
```

- **📢 섹션 요약 비유**: Java [[192_module_independence|모듈]] 시스템에서 `exports`는 건물의 공식 입구(공개 [[014_api_posix|API]]) — 방문자는 반드시 정문(exports된 패키지)으로만 들어와야 하고, 건물 내부 통로(internal 패키지)는 외부에서 접근 불가하다.

---

## Ⅲ. 비교 및 연결
| 단계 | 아키텍처 | 특징 | 적합한 팀 규모 |
|:---|:---|:---|:---|
| 1단계 | 전통 모놀리스 | 단순, 경계 없음 | 1~5명 |
| 2단계 | **[[192_module_independence|모듈]]형 모놀리스** | **경계 있음, 단일 배포** | **5~50명** |
| 3단계 | [[619_msa_traffic_hardware|MSA]] | 경계 있음, 다중 배포 | 50명+ |

| 항목 | 전통 모놀리스 | [[192_module_independence|모듈]]형 모놀리스 | [[619_msa_traffic_hardware|MSA]] |
|:---|:---|:---|:---|
| 배포 단위 | 단일 | 단일 | [[090_service_kubernetes_network_load_balancing|서비스]]별 독립 |
| 코드 경계 | 없음 | [[192_module_independence|모듈]] 경계 있음 | [[090_service_kubernetes_network_load_balancing|서비스]] 경계 |
| 운영 복잡도 | 낮음 | 낮음 | 높음 |
| 기술 [[057_stack|스택]] 다양성 | 없음 | 없음 | 가능 |
| 독립 배포 | 불가 | 불가 | 가능 |
| 장애 격리 | 없음 | 부분적 | 강함 |
| [[619_msa_traffic_hardware|MSA]] 이전 용이성 | 어려움 | 용이 | — |

- **📢 섹션 요약 비유**: 전통 모놀리스는 방 없는 오픈 사무실, [[192_module_independence|모듈]]형 모놀리스는 칸막이 있는 사무실, MSA는 각자 다른 건물에 있는 사무실 — 소통과 독립성의 트레이드오프이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
```java
// 아키텍처 규칙을 단위 테스트로 강제
@AnalyzeClasses(packages = "com.example")
public class ModuleBoundaryTest {

    @ArchTest
    static final ArchRule ordersDoNotAccessPaymentInternals =
        noClasses()
            .that().resideInAPackage("com.example.order..")
            .should()
            .dependOnClassesThat()
            .resideInAPackage("com.example.payment.internal..");

    @ArchTest
    static final ArchRule noCyclicDependencies =
        slices()
            .matching("com.example.(*)..")
            .should()
            .beFreeOfCycles();
}
```

```
Phase 1: Modular Monolith 구축
  - DDD로 Bounded Context 식별
  - 각 BC를 모듈로 구현 (명확한 Public API)
  - 모듈 간 이벤트 기반 통신 설계

Phase 2: 병목/분리 필요 모듈 식별
  - 성능 병목 모듈 → 먼저 분리 검토
  - 독립 배포 요구 모듈 → MSA 전환 후보

Phase 3: 선택적 MSA 전환
  - 준비된 모듈부터 별도 서비스로 추출
  - 나머지는 모놀리스 유지 (Strangler Fig 패턴)
  - 점진적 MSA 전환 (빅뱅 전환 방지)
```

| 함정 | 설명 | 방지책 |
|:---|:---|:---|
| Shared DB [[161_anti_pattern|Anti-Pattern]] | 모든 [[192_module_independence|모듈]]이 같은 테이블 직접 접근 | [[005_schema|스키마]] 격리 + Repository 패턴 |
| 경계 침식 | 편의상 내부 클래스 직접 [[316_reference_pattern_nosql|참조]] | ArchUnit 테스트 강제 |
| [[192_module_independence|모듈]] 간 순환 의존 | A가 B를, B가 A를 [[316_reference_pattern_nosql|참조]] | 이벤트 기반 디커플링 |
| 거대 공유 [[192_module_independence|모듈]] | 공통 [[192_module_independence|모듈]]이 비대해짐 | 공유 [[192_module_independence|모듈]] 최소화 원칙 |

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 해결하려는 변화 축이 분명한가?
2. [[198_abstraction_control_data_process|추상화]] 비용보다 변경 절감 효과가 큰가?
3. 테스트·[[568_logs_distributed_logging_elk_fluentd|로그]]·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Shared DB Anti-Pattern은 아파트에서 모든 세대가 옆집 냉장고를 직접 열어보는 것 — 각 세대([[192_module_independence|모듈]])는 자신의 냉장고([[005_schema|스키마]])만 접근하고, 필요한 것은 문을 두드려(공개 [[014_api_posix|API]]) 부탁해야 한다.

---

## Ⅴ. 기대효과 및 결론
[[192_module_independence|모듈]]형 모놀리스는 "MSA의 [[192_module_independence|모듈]]화 + 모놀리스의 단순성"을 모두 취하는 현실적인 선택이다:

**기대효과**:
- **개발 생산성**: 단일 프로세스로 디버깅 단순 ([[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 불필요)
- **배포 단순성**: [[090_configuration_item|CI]]/CD 파이프라인 1개, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 단순
- **[[619_msa_traffic_hardware|MSA]] 준비**: 경계가 명확하여 필요 시 점진적 분리 가능
- **일관된 [[191_transaction_concept_states|트랜잭션]]**: ACID [[191_transaction_concept_states|트랜잭션]] 적용 가능 (MSA의 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 불필요)

**적합한 시나리오**:
- 스타트업 [[459_quic_fec_forward_error_correction|초기]]~중기 (빠른 개발 우선)
- 팀 규모 [[489_raid_10_hybrid|10]]~30명
- [[064_relation_domain|도메인]] 경계가 안정화 단계
- [[619_msa_traffic_hardware|MSA]] 전환을 고려하지만 아직 필요성 불명확

기술사 시험에서는 **[[192_module_independence|모듈]]형 모놀리스와 전통 모놀리스의 차이([[192_module_independence|모듈]] 경계 존재 여부)**, **MSA와의 트레이드오프(운영 복잡도 vs 독립 배포)**, **[[310_architecture|DDD]] → [[599_modular_monolith_architecture|Modular Monolith]] → [[619_msa_traffic_hardware|MSA]] 진화 경로**를 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② [[111_observability_metrics_logs_traces|관측 가능성]]([[642_observability_telemetry|Observability]]) 내장, ③ [[136_variance|분산]] 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: [[192_module_independence|모듈]]형 모놀리스는 레고 성 — 하나의 성(단일 배포)이지만 내부는 왕궁, 마굿간, 군사 요새 등 독립적인 구역([[192_module_independence|모듈]])으로 나뉘어 있다. 언제든 특정 구역([[192_module_independence|모듈]])만 떼어내 새 성([[619_msa_traffic_hardware|MSA]])으로 확장할 수 있도록 연결부(공개 [[014_api_posix|API]])가 표준화되어 있다.

---

### 📌 관련 개념 맵
| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [[201_software_architecture_definition|소프트웨어 아키텍처]] 스타일 | [[192_module_independence|모듈]]형 모놀리스가 속하는 아키텍처 범주 |
| 진화 전 단계 | 전통 모놀리스 (Monolith) | 경계 없는 단일 [[007_codebase|코드베이스]] |
| 진화 후 단계 | [[619_msa_traffic_hardware|MSA]] ([[365_msa_microservice_architecture|Microservice Architecture]]) | 독립 배포, 다중 [[090_service_kubernetes_network_load_balancing|서비스]] |
| 핵심 기반 개념 | [[310_architecture|DDD]] [[221_bounded_context_ddd_msa_boundary|Bounded Context]] | [[192_module_independence|모듈]] 경계의 [[655_ir_detection_analysis|식별]] 방법 |
| 경계 강제 도구 | ArchUnit | Java 아키텍처 테스트 [[336_library_vs_framework|라이브러리]] |
| 전환 패턴 | [[308_strangler_fig_pattern|Strangler Fig Pattern]] | 모놀리스에서 MSA로 점진적 전환 |
| 성공 사례 | Shopify, [[057_stack|Stack]] [[095_overflow|Overflow]] | 대규모 [[192_module_independence|모듈]]형 모놀리스 운영 사례 |

### 📈 관련 키워드 및 발전 흐름도
monolith boundary → [[192_module_independence|모듈]]형 모놀리스 → [[619_msa_traffic_hardware|microservices]] 분해

### 👶 어린이를 위한 3줄 비유 설명
1. [[192_module_independence|모듈]]형 모놀리스는 잘 정리된 학교 건물 — 하나의 건물(단일 배포)이지만 국어실, 수학실, 과학실(각 [[192_module_independence|모듈]])이 따로 있어서 각 방에서 필요한 것은 복도(공개 [[014_api_posix|API]])를 통해서만 요청해.
2. 방([[192_module_independence|모듈]]) 안에 있는 물건(내부 클래스)은 다른 방에서 직접 가져오면 안 되고, 담당 선생님([[192_module_independence|모듈]] [[014_api_posix|API]])을 통해서만 빌릴 수 있어.
3. 나중에 학교가 커지면(팀/[[090_service_kubernetes_network_load_balancing|서비스]] 규모 증가) 수학실만 떼어내 다른 건물(별도 [[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]])로 이전할 수 있어 — 이미 경계가 명확하기 때문에 분리가 쉬워.
