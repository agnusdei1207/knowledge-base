---
title: 111. 컨테이너 런타임 샌드박싱 - gVisor·Kata Containers·런타임 보안 격리
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기본 [[561_container_based_deployment|컨테이너]]([[667_container_runtime_hw_isolation|runc]])는 호스트 [[022_kernel_role|커널]]을 공유하므로 **[[022_kernel_role|커널]] 취약점을 통한 [[561_container_based_deployment|컨테이너]] 탈출([[252_container_escape_vm_gvisor_kata|Container Escape]])** 위험이 있다. [[602_sandboxing_kernel_wrapper|샌드박싱]] 런타임은 **[[022_kernel_role|커널]] 접근을 차단하는 추가 격리 계층**을 삽입하여 보안을 강화한다.
> 2. **가치**: gVisor는 **유저 스페이스 [[022_kernel_role|커널]](Sentry)**로 시스콜을 중간 차단하고, Kata Containers는 **경량 [[598_vm_migration_nic|VM]] 안에 [[561_container_based_deployment|컨테이너]]를 격리**하여, [[310_multi_tenant_database_architecture|멀티테넌트]] 환경에서 **워크로드 간 완벽 격리**를 달성한다.
> 3. **판단 포인트**: gVisor는 **시스콜 [[344_compatibility_usability|호환성]] 제한+[[282_performance_tactics|성능]] 오버헤드 5~15%**, Kata는 **[[598_vm_migration_nic|VM]] 부팅 [[015_지연_데이터_관점|지연]]+메모리 오버헤드**라는 트레이드오프가 있으며, **신뢰할 수 없는 코드([[090_configuration_item|CI]] Runner, [[342_faas|FaaS]])** 실행 시 도입을 검토한다.

---

## Ⅰ. 개요 및 필요성

기본 [[628_container_runtime_oci|컨테이너 런타임]]([[667_container_runtime_hw_isolation|runc]])은 [[061_namespace|Namespace]]·cgroups로 프로세스를 격리하지만, **호스트 [[022_kernel_role|커널]]을 직접 공유**한다. [[022_kernel_role|커널]]에 [[761_zero_day|제로데이]] 취약점이 발생하면 [[561_container_based_deployment|컨테이너]] 안의 악성 코드가 호스트 전체를 장악할 수 있다([[252_container_escape_vm_gvisor_kata|Container Escape]]).

```text
┌───────────────────────────────────────────────────────┐
│      런타임별 격리 수준 비교                            │
├───────────────────────────────────────────────────────┤
│  [runc (기본)]                                        │
│   Container ──syscall──▶ Host Kernel (직접 접근 ⚠️)  │
│                                                       │
│  [gVisor (runsc)]                                     │
│   Container ──syscall──▶ Sentry(유저커널) ──▶ Kernel  │
│   시스콜 중간 차단, 200+개만 허용                     │
│                                                       │
│  [Kata Containers]                                    │
│   Container ──▶ [경량 VM (QEMU/Firecracker)]         │
│                      └──▶ Guest Kernel ──▶ Host      │
│   완전한 커널 격리, VM 수준 보안                      │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: runc는 사무실 칸막이(넘어가기 쉬움), gVisor는 유리벽(보이지만 못 넘어감), Kata는 별도 건물(완전 분리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 런타임 | 격리 방식 | [[022_kernel_role|커널]] 공유 | [[282_performance_tactics|성능]] 오버헤드 | [[344_compatibility_usability|호환성]] |
|:---|:---|:---|:---|:---|
| **[[667_container_runtime_hw_isolation|runc]]** | [[061_namespace|Namespace]]+[[062_cgroups|cgroups]] | 공유 | 거의 없음 | 100% |
| **gVisor** | 유저 스페이스 [[022_kernel_role|커널]] (Sentry) | **차단** | 5~15% | 제한 (200+ syscall) |
| **Kata** | 경량 [[598_vm_migration_nic|VM]] (Firecracker) | **게스트 [[022_kernel_role|커널]]** | 부팅 [[015_지연_데이터_관점|지연]]+메모리 | 높음 |

### gVisor 동작 원리
앱이 `open()` 시스콜을 호출하면, 호스트 [[022_kernel_role|커널]]에 직접 가지 않고 **Sentry(유저 스페이스 [[022_kernel_role|커널]])**가 가로채어 [[395_verification_process_review|검증]] 후 제한적으로 호스트에 전달한다. 악성 시스콜은 Sentry에서 차단된다.

- **📢 섹션 요약 비유**: gVisor는 회사 메일 시스템이다. 직원([[561_container_based_deployment|컨테이너]])이 외부에 메일(시스콜)을 보내면, 보안팀(Sentry)이 검열한 후 통과시킨다.

---

## Ⅲ. 비교 및 연결

| 비교 | 기본 [[561_container_based_deployment|컨테이너]] | [[598_vm_migration_nic|VM]] | gVisor | Kata |
|:---|:---|:---|:---|:---|
| **격리** | 약함 | 강함 | **중간~강함** | **강함 (VM급)** |
| **[[282_performance_tactics|성능]]** | 최고 | 낮음 | 중간 | 중간 |
| **부팅** | ms | 수 초 | ms | **< 100ms (Firecracker)** |
| **밀도** | 최고 | 낮음 | 높음 | 중간 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 시나리오
1. **[[090_configuration_item|CI]]/CD Runner**: 사용자 제출 코드를 빌드 → gVisor 격리로 악성 코드 차단.
2. **[[342_faas|FaaS]] ([[216_lambda_kappa_architecture_batch_realtime|Lambda]])**: [[310_multi_tenant_database_architecture|멀티테넌트]] 함수 실행 → Firecracker (Kata 기반) 격리.
3. **일반 워크로드**: 신뢰 가능한 내부 앱 → [[667_container_runtime_hw_isolation|runc]] 유지 ([[282_performance_tactics|성능]] 우선).

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **모든 파드를 gVisor로 실행**: 시스콜 [[344_compatibility_usability|호환성]] 문제로 일부 앱 오작동 → [[085_confidence_association_rule_conditional_probability|신뢰도]] 높은 내부 앱에는 불필요.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [[667_container_runtime_hw_isolation|runc]] (기본) | gVisor / Kata | 개선 |
|:---|:---|:---|:---|
| [[561_container_based_deployment|컨테이너]] 탈출 위험 | 높음 | **차단/격리** | 보안 강화 |
| [[310_multi_tenant_database_architecture|멀티테넌트]] 격리 | 약함 | **강함** | 규정 준수 |
| [[282_performance_tactics|성능]] | 최고 | 5~15% 오버헤드 | 트레이드오프 |

[[561_container_based_deployment|컨테이너]] [[602_sandboxing_kernel_wrapper|샌드박싱]]은 [[795_confidential_computing|Confidential Computing]]([[795_confidential_computing|기밀 컴퓨팅]])과 결합하여 하드웨어 [[478_tee|TEE]]([[972_tee_based_ml|Trusted Execution Environment]]) 내에서 [[561_container_based_deployment|컨테이너]]를 실행하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[667_container_runtime_hw_isolation|runc]]** | [[333_process|OCI]] 표준 기본 [[628_container_runtime_oci|컨테이너 런타임]] |
| **gVisor (runsc)** | Google의 유저 스페이스 [[022_kernel_role|커널]] 샌드박스 |
| **Kata Containers** | 경량 [[598_vm_migration_nic|VM]] 기반 [[561_container_based_deployment|컨테이너]] 격리 |
| **Firecracker** | AWS Lambda가 사용하는 마이크로VM |
| **[[252_container_escape_vm_gvisor_kata|Container Escape]]** | [[602_sandboxing_kernel_wrapper|샌드박싱]]이 방지하려는 공격 벡터 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Docker + runc (2013~) — 커널 공유 컨테이너 표준화]
    │
    ▼
[Container Escape 공격 증가 (2017~) — CVE-2019-5736 등]
    │
    ▼
[gVisor (2018, Google) — 유저 스페이스 커널 격리]
    │
    ▼
[Kata + Firecracker (2018~) — 경량 VM 격리]
    │
    ▼
[현재: Confidential Containers — 하드웨어 TEE + 컨테이너]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 보통 [[561_container_based_deployment|컨테이너]]([[667_container_runtime_hw_isolation|runc]])는 교실 **칸막이**로 나뉜 거예요. 칸막이를 넘으면 옆 자리를 볼 수 있죠.
2. gVisor는 **유리벽**이에요. 보이지만 넘어갈 수 없어요.
3. Kata는 아예 **다른 건물**로 분리해서, 절대 옆 교실에 갈 수 없게 만든답니다!
