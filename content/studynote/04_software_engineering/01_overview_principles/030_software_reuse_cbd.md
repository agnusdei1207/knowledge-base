---
title: 30. 소프트웨어 재사용과 CBD — Component Based Development
date: '2026-04-29'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 재사용(Software Reuse)은 이미 [[395_verification_process_review|검증]]된 소프트웨어 자산을 새 시스템 개발에 활용하는 전략이다. CBD(Component-Based Development)는 독립적으로 배포 가능한 [[603_component_independent_deployment_unit|컴포넌트]] 단위로 소프트웨어를 개발·조립하는 방법론이다.
> 2. **가치**: 재사용은 생산성 향상·품질 개선·비용 절감의 세 가지 이점을 동시에 제공한다. CBD는 인터페이스 기반 조립(Black-box Reuse)으로 최고 수준의 재사용성을 실현한다.
> 3. **판단 포인트**: 재사용의 역설 — 재사용 가능한 [[603_component_independent_deployment_unit|컴포넌트]]를 만들려면 일반화 비용이 들고, 재사용 자산을 관리하는 인프라도 필요하다. 재사용 투자 효과는 동일 [[603_component_independent_deployment_unit|컴포넌트]]를 3번 이상 사용할 때 본전을 넘는 것으로 알려져 있다.

---

## Ⅰ. 개요 및 필요성

```text
재사용 수준 계층:

  시스템 수준  ← 전체 애플리케이션 재사용 (SaaS 활용)
  서브시스템  ← 라이브러리·프레임워크·미들웨어
  컴포넌트    ← CBD, 인터페이스로 조립
  객체/클래스 ← OOP 상속·다형성
  함수/모듈   ← 가장 기본적인 재사용
  코드 복사   ← Copy-Paste (재사용 최하위)
```

- **📢 섹션 요약 비유**: 소프트웨어 재사용 수준은 레고 블록 조립 방식이다. 기성 완성품([[309_saas|SaaS]]) 구매부터 큰 레고 세트(프레임워크) 활용, 개별 블록([[603_component_independent_deployment_unit|컴포넌트]]) 조립까지 다양한 수준이 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### CBD 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **[[603_component_independent_deployment_unit|컴포넌트]]** | 독립 배포·교체 가능한 소프트웨어 단위 |
| **인터페이스** | [[603_component_independent_deployment_unit|컴포넌트]] 간 통신 계약 (Provided/Required) |
| **[[446_port_and_bus|포트]]** | [[603_component_independent_deployment_unit|컴포넌트]] 외부 연결 지점 |
| **커넥터** | [[603_component_independent_deployment_unit|컴포넌트]] 간 통신 메커니즘 |
| **[[603_component_independent_deployment_unit|컴포넌트]] 저장소** | 재사용 자산 관리 [[235_registry_immutable_tag|레지스트리]] |

### 재사용 유형

```text
White-Box Reuse (화이트박스):
  - 소스 코드 수정 후 재사용
  - 유연하지만 유지보수 비용↑
  - 예: 오픈소스 포크

Black-Box Reuse (블랙박스):
  - 인터페이스만 사용, 내부 비공개
  - CBD의 이상적 형태
  - 예: 라이브러리, API, 마이크로서비스

Glass-Box Reuse (글래스박스):
  - 소스 보기는 가능, 수정 불가
  - 중간 수준 재사용
```

- **📢 섹션 요약 비유**: 재사용 유형은 레시피 활용 방식이다. 화이트박스(레시피 수정), 블랙박스(완성품 구매), 글래스박스(레시피 참고만)에 따라 자유도와 편의성이 달라진다.

---

## Ⅲ. 비교 및 연결

| 비교 | CBD | [[322_oop_4_characteristics|OOP]] | [[618_soa_hardware|SOA]] |
|:---|:---|:---|:---|
| 단위 | [[603_component_independent_deployment_unit|컴포넌트]] | 클래스 | [[090_service_kubernetes_network_load_balancing|서비스]] |
| 배포 | 독립 배포 | 함께 컴파일 | 독립 [[090_service_kubernetes_network_load_balancing|서비스]] |
| 통신 | 인터페이스 | 메서드 호출 | 웹서비스/[[014_api_posix|API]] |
| 현대화 | [[532_microservices_decomposition_patterns|마이크로서비스]]로 진화 | 여전히 핵심 | MSA로 발전 |

- **📢 섹션 요약 비유**: CBD·[[322_oop_4_characteristics|OOP]]·SOA는 건물 [[192_module_independence|모듈]]화 단계다. [[322_oop_4_characteristics|OOP]](벽돌), CBD(방 [[192_module_independence|모듈]]), [[618_soa_hardware|SOA]](건물 동 전체) 순으로 [[192_module_independence|모듈]] 크기가 커지고 독립성이 높아진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 재사용 성숙도 모델

```text
레벨 1 (임시적): 개인 판단에 의한 비공식 재사용
레벨 2 (반복적): 팀 내 재사용 관행 정착
레벨 3 (정의된): 조직 재사용 프로세스 공식화
레벨 4 (관리된): 재사용 측정·추적
레벨 5 (최적화): 재사용 기반 조직 학습·개선
```

### 현대 CBD 실현: [[532_microservices_decomposition_patterns|마이크로서비스]]

```text
전통 CBD:          마이크로서비스 (현대 CBD):
  컴포넌트 저장소     컨테이너 레지스트리 (Docker Hub)
  인터페이스 명세     OpenAPI Spec / gRPC Proto
  배포 단위          Docker 이미지
  오케스트레이션      Kubernetes
  서비스 탐색        Service Mesh (Istio)
```

- **📢 섹션 요약 비유**: [[532_microservices_decomposition_patterns|마이크로서비스]]는 현대적 레고 블록이다. 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 독립 [[561_container_based_deployment|컨테이너]] 박스([[603_component_independent_deployment_unit|컴포넌트]])에 담기고, [[014_api_posix|API]](인터페이스)로 연결되며, [[205_kubernetes_container_orchestration|Kubernetes]](레고 베이스플레이트)가 조립을 관리한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **생산성** | [[395_verification_process_review|검증]] [[603_component_independent_deployment_unit|컴포넌트]] 조립으로 개발 속도↑ |
| **품질** | 기존 테스트된 [[603_component_independent_deployment_unit|컴포넌트]] 재활용 |
| **유지보수** | [[603_component_independent_deployment_unit|컴포넌트]] 교체로 유연한 시스템 변경 |

[[190_ai_llm_requirements_specification|AI]] 기반 코드 재사용이 새로운 지평을 열고 있다. GitHub Copilot·Amazon CodeWhisperer는 수십억 줄의 공개 코드를 학습하여 컨텍스트에 맞는 재사용 코드를 자동 제안한다. 이는 CBD의 개념을 AI가 자동화하는 것과 유사하다.

- **📢 섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] 코드 재사용은 [[190_ai_llm_requirements_specification|AI]] 요리사가 수백만 개 레시피를 학습해서 내 요청에 맞는 레시피를 즉석에서 조합해주는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[532_microservices_decomposition_patterns|마이크로서비스]]** | CBD의 현대적 실현 |
| **[[561_container_based_deployment|컨테이너]]** | [[603_component_independent_deployment_unit|컴포넌트]] 독립 배포 단위 |
| **[[322_oop_4_characteristics|OOP]]** | CBD 이론적 기반 |
| **[[618_soa_hardware|SOA]]** | CBD [[090_service_kubernetes_network_load_balancing|서비스]] 수준 확장 |
| **[[190_ai_llm_requirements_specification|AI]] 코드 [[087_process_state_transition|생성]]** | 지능형 재사용 자동화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[코드 복사·라이브러리 — 기초 재사용]
    │
    ▼
[OOP — 클래스·상속 기반 재사용]
    │
    ▼
[CBD — 컴포넌트 인터페이스 기반 블랙박스 재사용]
    │
    ▼
[SOA — 서비스 수준 재사용, 웹서비스]
    │
    ▼
[마이크로서비스 — 컨테이너 기반 현대 CBD]
    │
    ▼
[AI 코드 생성 — 지능형 자동 재사용 추천]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 소프트웨어 재사용은 레고 블록 조립이에요 — 이미 만들어진 블록을 조립하면 훨씬 빠르게 완성품을 만들 수 있어요!
2. CBD는 레고 블록마다 표준 연결 홈을 만드는 거예요 — 어떤 블록이든 맞게 연결돼요!
3. [[532_microservices_decomposition_patterns|마이크로서비스]]는 현대판 CBD예요 — 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 독립된 [[561_container_based_deployment|컨테이너]] 박스에 담겨 어디서든 조립될 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 973

← **이전**: [[029_reverse_engineering|29. 역공학 (Reverse Engineering)]]
**다음**: [[031_software_maintenance_types|31. 소프트웨어 유지보수 유형 — 4가지 변경 분류]] →

---
