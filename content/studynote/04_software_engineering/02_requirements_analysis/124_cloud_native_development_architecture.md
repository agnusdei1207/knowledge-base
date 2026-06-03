---
title: 124. 클라우드 네이티브 아키텍처 - CNCF 기반 현대 소프트웨어 개발 패러다임
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[531_cloud_native_architecture|클라우드 네이티브]]는 **[[561_container_based_deployment|컨테이너]]·[[619_msa_traffic_hardware|MSA]]·[[090_configuration_item|CI]]/CD·선언적 [[014_api_posix|API]]**를 핵심으로 하여 클라우드 환경의 **[[571_resiliency_fault_tolerance_patterns|탄력성]]·확장성·복원력을 최대한 활용**하는 소프트웨어 개발·운영 패러다임이다.
> 2. **가치**: [[086_lift_association_rule_marketing|Lift]] & Shift(기존 시스템을 그대로 클라우드로 이전)로는 클라우드의 이점을 [[489_raid_10_hybrid|10]]%도 활용하지 못하지만, [[531_cloud_native_architecture|클라우드 네이티브]]로 설계하면 **오토스케일링·셀프힐링·글로벌 배포**가 자연스럽게 구현된다.
> 3. **판단 포인트**: [[190_cncf_landscape_observability|CNCF]]([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Computing Foundation)의 **Trail Map**([[561_container_based_deployment|컨테이너]]화→[[090_configuration_item|CI]]/CD→[[073_container_orchestration_tools|오케스트레이션]]→관측성→[[302_service_mesh_istio|서비스 메시]])이 도입 로드맵이며, **12 Factor App**이 [[531_cloud_native_architecture|클라우드 네이티브]] 설계 원칙이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    클라우드 네이티브 4대 핵심                          │
├───────────────────────────────────────────────────────┤
│  1. 컨테이너 (Docker/containerd)                      │
│  2. MSA (마이크로서비스)                              │
│  3. CI/CD (지속적 통합·배포)                          │
│  4. 선언적 API (K8s Desired State)                    │
│                                                       │
│  + DevOps 문화 + 관측성 + 서비스 메시                 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[531_cloud_native_architecture|클라우드 네이티브]]는 처음부터 **바다(클라우드)에서 살도록 진화한 물고기**이고, [[086_lift_association_rule_marketing|Lift]] & Shift는 육지 동물이 바다에 던져진 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 12 Factor App (주요)

| Factor | 설명 |
|:---|:---|
| **[[007_codebase|코드베이스]]** | 1앱 = 1리포 |
| **의존성** | 명시적 선언 |
| **[[009_config|설정]]** | 환경 변수로 분리 |
| **[[013_port_binding|포트 바인딩]]** | 자체 [[461_http_stateless_connection_oriented|HTTP]] 서버 |
| **[[568_logs_distributed_logging_elk_fluentd|로그]]** | stdout 스트림 |
| **프로세스** | [[239_stateless_redis|Stateless]] |

- **📢 섹션 요약 비유**: 12 Factor는 [[531_cloud_native_architecture|클라우드 네이티브]]의 **건축 법규**다. 이 규칙을 따라야 건물(앱)이 안전하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 | [[086_lift_association_rule_marketing|Lift]] & Shift | [[531_cloud_native_architecture|클라우드 네이티브]] |
|:---|:---|:---|:---|
| **아키텍처** | 모놀리식 | 모놀리식 | **[[619_msa_traffic_hardware|MSA]]** |
| **배포** | 수동 | 수동 | **[[090_configuration_item|CI]]/CD** |
| **[[249_scaling_normalization_standardization|스케일링]]** | 수동 | 반자동 | **자동** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[190_cncf_landscape_observability|CNCF]] Trail Map
1. [[561_container_based_deployment|컨테이너]]화 → 2. [[090_configuration_item|CI]]/CD → 3. K8s → 4. 관측성([[136_prometheus|Prometheus]]) → 5. [[302_service_mesh_istio|서비스 메시]]([[302_service_mesh_istio|Istio]]) → 6. 보안([[237_opa_open_policy_agent_gatekeeper|OPA]]).

---

## Ⅴ. 기대효과 및 결론

[[531_cloud_native_architecture|클라우드 네이티브]]는 **현대 소프트웨어 개발의 표준 패러다임**이며, [[190_cncf_landscape_observability|CNCF]] 생태계가 사실상 모든 기술 스택을 포괄한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[190_cncf_landscape_observability|CNCF]]** | [[531_cloud_native_architecture|클라우드 네이티브]] 재단 |
| **12 Factor** | 설계 원칙 |
| **[[561_container_based_deployment|컨테이너]]** | 핵심 런타임 |
| **K8s** | [[073_container_orchestration_tools|오케스트레이션]] 표준 |
| **[[302_service_mesh_istio|서비스 메시]]** | 통신 인프라 ([[302_service_mesh_istio|Istio]]) |

### 📈 관련 키워드 및 발전 흐름도

```text
[온프레미스 (전통, ~2010s)]
    │
    ▼
[Lift & Shift (IaaS, 2010~)]
    │
    ▼
[클라우드 네이티브 (CNCF, 2015~) — 컨테이너+MSA+CI/CD]
    │
    ▼
[서비스 메시 + GitOps (2018~)]
    │
    ▼
[현재: Platform Engineering — 개발자 경험 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[531_cloud_native_architecture|클라우드 네이티브]]는 처음부터 **바다(클라우드)에서 살도록 태어난 물고기**예요.
2. 옛날 방식은 **육지 동물을 바다에 던지는([[086_lift_association_rule_marketing|Lift]] & Shift)** 거라 잘 못 수영해요.
3. 물고기처럼 설계하면 **파도(트래픽)가 커도 자유롭게** 헤엄칠 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 973

← **이전**: [[123_serverless_faas_aws_lambda|123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅]]
**다음**: [[125_12_factor_app_cloud_native_architecture|125. 12 Factor App - 클라우드 네이티브 애플리케이션 설계 12원칙]] →

---
