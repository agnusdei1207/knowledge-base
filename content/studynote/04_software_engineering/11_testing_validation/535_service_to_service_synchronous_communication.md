+++
title = "535. 서비스 간 동기 통신 - REST API, gRPC"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신 - [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/), gRPC은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신은 직관적이고 구현이 쉽다. [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API와 gRPC가 대표적이다.

하지만 체인이 길어지면 지연과 장애 전파가 커질 수 있다.

- **📢 섹션 요약 비유**: 전화로 물어보고 바로 답을 기다리는 것과 같다.

---

다음은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  서비스 간 동기 통신                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

REST는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([Hypertext Transfer Protocol](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))와 리소스 중심 설계이고, gRPC는 [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers를 쓰는 고성능 RPC다.

```text
요청 -> 서비스 A -> 서비스 B -> 응답
```

| 방식 | 특징 |
|:---|:---|
| [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | 단순/범용 |
| [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) | 고성능/강타입 |
| Sync | 즉시 응답 |

- **📢 섹션 요약 비유**: 편지는 읽기 쉬운 대신 오래 걸리고, 전화는 빠르지만 즉시 받아야 한다.

---

---

---

---

## Ⅲ. 비교 및 연결

동기 통신은 개발이 쉽지만, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수가 늘면 복잡해진다.

| 구분 | [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) | [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) |
|:---|:---|:---|
| 직관성 | 높음 | 중간 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 보통 | 높음 |
| 계약 | 느슨함 | 엄격함 |

동기 체인이 길어지면 회복력이 떨어질 수 있다.

- **📢 섹션 요약 비유**: 한 명이 대답을 늦게 하면 줄 선 모두가 멈춘다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/), retry, [circuit breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/), idempotency를 고려한다.

점검 포인트는 다음과 같다.
1. 타임아웃이 충분히 짧은가?
2. 실패 시 재시도가 안전한가?
3. 계약이 명확한가?

- **📢 섹션 요약 비유**: 전화가 안 되면 바로 포기할지, 다시 걸지 정해야 한다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

동기 통신은 단순한 호출 구조를 제공한다.

결론적으로 이 항목은 "즉시 응답형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신"이다.

- **📢 섹션 요약 비유**: 묻고 답하기가 빠를수록 일이 쉬워진다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
서비스 간 동기 통신 개념 정립
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

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 통신은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 661 / 973

← **이전**: [534. 하위 도메인에 따른 분해 (DDD 기반)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/534_subdomain_decomposition/)
**다음**: [535. 서비스 간 동기 통신 - REST API, gRPC (Protocol Buffers)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) →

---
