---
title: "068. Live Patching"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Live Patching은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 재부팅 없이 취약점이나 버그를 패치하는 기술이다.
> 2. **가치**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단을 최소화하면서 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 결함을 신속히 수정할 수 있다.
> 3. **판단**: [kpatch](/studynote/02_operating_system/11_exam_summary/789_live_patching_kpatch_no_downtime/), kGraft 같은 구현은 패치 적용 범위와 안정성 관리가 핵심이다.

---

## Ⅰ. 개요 및 필요성

운영 중인 서버를 재부팅하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 끊길 수 있다. Live Patching은 이 문제를 줄이기 위해 등장했다.

그래서 고가용성 환경에서 특히 중요하다.

- **📢 섹션 요약 비유**: 달리는 기차 바퀴를 멈추지 않고 갈아 끼우는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Kernel Bug
  v
Live Patch
  v
Redirect / Replace
  v
Patched Kernel
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Patch [Module](/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | 수정 코드 |
| Hot Update | 실시간 적용 |
| [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 |

Live Patching은 기존 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 함수 실행을 새 코드로 전환하는 방식으로 동작한다. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 상태를 깨지 않도록 설계하는 것이 중요하다.

- **📢 섹션 요약 비유**: 운행 중인 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 부품을 멈추지 않고 갈아 끼우는 수리다.

---

## Ⅲ. 비교 및 연결

| 방식 | 재부팅 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| Reboot Patch | 필요 | 단순 | 다운타임 |
| Live Patching | 불필요 | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지 | 적용 범위 제한 |
| [LKM](/studynote/02_operating_system/01_overview_architecture/067_lkm/) | 불필요 | 모듈화 | 기능 추가 중심 |

| 구현 | 특징 |
| :-- | :-- |
| [kpatch](/studynote/02_operating_system/11_exam_summary/789_live_patching_kpatch_no_downtime/) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패치 프레임워크 |
| kGraft | [실시간 커널](/studynote/02_operating_system/03_cpu_scheduling/200_real_time_kernel_preempt_rt/) 업데이트 |

Live Patching은 장애 대응보다 예방적 보안 패치에 특히 유용하다.

- **📢 섹션 요약 비유**: 문을 닫지 않고 자물쇠를 바꾸는 일이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 재부팅 없이 패치 가능한가?
2. 패치 적용 범위가 명확한가?
3. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 상태 안전성을 보장하는가?
4. [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 전략이 있는가?
5. 지원 환경과 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 제약을 아는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 패치를 라이브로 해결하려는 설계
- 적용 범위와 호환성을 무시하는 설계
- [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획 없이 적용하는 설계
- 안정성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 운영하는 설계

기술사 관점에서는 Live Patching을 "무중단 패치"로 설명하되, 제약과 운영 절차까지 함께 말해야 한다.

- **📢 섹션 요약 비유**: 움직이는 차를 바로 고칠 수 있지만, 아무 부품이나 다 바꿀 수는 없다.

---

## Ⅴ. 기대효과 및 결론

Live Patching은 [커널 취약점](/studynote/09_security/04_endpoint_security/376_kernel_vulnerability/) 대응과 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지에 도움이 된다. 그래서 운영 환경에서 매우 유용하다.

결론적으로 Live Patching은 재부팅 없이 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 수정하는 기술이다.

- **📢 섹션 요약 비유**: 쉬지 않고 고치는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 센터다.

---

## 관련 개념 맵

```text
Kernel
  v
Live Patching
  v
kpatch / kGraft
  v
Zero Downtime Maintenance
```

---

## 관련 키워드 및 발전 흐름도

```text
Kernel Patch
  v
Live Patching
  v
kpatch / kGraft
  v
High Availability
```

---

## 어린이를 위한 3줄 비유 설명

멈추지 않고 고치는 방법이에요.
기차를 세우지 않고 바퀴를 바꿔요.
라이브 패칭은 그런 기술이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 68 / 800

<- **이전**: [67. 모듈 적재 (Loadable Kernel Modules, LKM)](/studynote/02_operating_system/01_overview_architecture/067_lkm/)
**다음**: [69. BPF (Berkeley Packet Filter) / eBPF (Extended BPF) - 커널 내 샌드박스 프로그램](/studynote/02_operating_system/01_overview_architecture/069_ebpf/) ->

---
