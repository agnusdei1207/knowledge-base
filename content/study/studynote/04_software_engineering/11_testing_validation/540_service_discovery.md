+++
weight = 540
title = "540. 서비스 디스커버리 (Service Discovery) - 동적 IP/Port 레지스트리 (Eureka, Consul)"
date = "2026-05-08"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) - 동적 IP/[[446_port_and_bus|Port]] [[235_registry_immutable_tag|레지스트리]] (Eureka, Consul)은(는) [[001_software_engineering_definition|소프트웨어 공학]]의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[[346_maintainability_portability|유지보수성]]·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[090_service_kubernetes_network_load_balancing|서비스]]는 [[561_container_based_deployment|컨테이너]] 재시작이나 오토스케일링으로 주소가 바뀐다. 그래서 호출자는 고정 주소가 아니라 [[235_registry_immutable_tag|레지스트리]]를 통해 현재 위치를 알아내야 한다.

- **📢 섹션 요약 비유**: 이사한 친구의 새 집 주소를 전화번호부에서 찾아가는 것과 같다.

---

다음은 [[306_service_discovery_pattern|서비스 디스커버리]] ([[090_service_kubernetes_network_load_balancing|Service]] D의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  서비스 디스커버리 (Service D                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [[306_service_discovery_pattern|서비스 디스커버리]] ([[090_service_kubernetes_network_load_balancing|Service]] D가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[[090_service_kubernetes_network_load_balancing|서비스]]는 시작할 때 자신을 등록하고, 호출자는 필요할 때 조회한다.

```text
Service A -> Registry -> Service B 위치(IP/Port)
Service A -> Service B (실제 호출)
```

| 요소 | 역할 |
|:---|:---|
| [[235_registry_immutable_tag|Registry]] | [[090_service_kubernetes_network_load_balancing|서비스]] 주소 저장 |
| Heartbeat | 살아 있음 [[396_validation|확인]] |
| Lookup | 최신 위치 조회 |

- **📢 섹션 요약 비유**: 전화번호부에 이름과 번호를 적어 두고, 전화 걸기 전마다 [[396_validation|확인]]하는 방식이다.

---

---

---

---

## Ⅲ. 비교 및 연결

Eureka (Netflix [[191_oss_license_compliance|OSS]])와 Consul은 대표적인 [[090_service_kubernetes_network_load_balancing|서비스]] [[235_registry_immutable_tag|레지스트리]]다. [[511_dns_hierarchical_distributed_architecture|DNS]] ([[511_dns_hierarchical_distributed_architecture|Domain Name System]])만으로는 세밀한 헬스체크와 [[012_metadata|메타데이터]] 관리가 부족할 수 있다.

| 구분 | [[306_service_discovery_pattern|서비스 디스커버리]] | 고정 [[009_config|설정]] |
|:---|:---|:---|
| 유연성 | 높음 | 낮음 |
| 운영 부담 | 중간 | 낮음 |
| 확장성 | 높음 | 낮음 |

- **📢 섹션 요약 비유**: 벽에 박아 둔 간판보다, 매일 바뀌는 안내판이 더 현실적이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 헬스체크 실패 시 목록에서 제거하고, 캐시 [[294_ttl_time_to_live_looping_prevention|TTL]] ([[294_ttl_time_to_live_looping_prevention|Time To Live]])과 재조회 정책을 정한다.

점검 포인트는 다음과 같다.
1. [[235_registry_immutable_tag|레지스트리]] 장애가 전체 호출을 멈추지 않는가?
2. 조회 결과를 얼마나 오래 믿을 것인가?
3. [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]] 환경에서 일관성을 어떻게 맞출 것인가?

- **📢 섹션 요약 비유**: 친구 주소록이 틀릴 때를 대비해 다시 물어볼 방법이 필요하다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

[[306_service_discovery_pattern|서비스 디스커버리]]는 동적 인프라에서 호출 안정성을 높인다.

결론적으로 이 항목은 "현재 살아 있는 [[090_service_kubernetes_network_load_balancing|서비스]] 위치를 찾아 연결하는 메커니즘"이다.

- **📢 섹션 요약 비유**: 주소가 자주 바뀌는 가게를 찾는 가장 안전한 지도다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]]) | [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle) | [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]]) | [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
서비스 디스커버리 (Service Discovery) 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [[002_software_crisis|소프트웨어 위기]] 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]])은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [[001_software_engineering_definition|소프트웨어 공학]]은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.
