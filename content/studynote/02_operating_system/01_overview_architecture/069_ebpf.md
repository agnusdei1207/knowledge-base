---
title: "69. BPF (Berkeley Packet Filter) / eBPF (Extended BPF) - 커널 내 샌드박스 프로그램"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안에서 안전하게 실행되는 샌드박스형 프로그램 프레임워크다.
> 2. **가치**: 네트워킹, 관측성, 보안, 트레이싱을 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수정 없이 확장할 수 있다.
> 3. **판단**: 검증기(verifier)와 제한된 실행 모델이 안전성의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능을 직접 바꾸면 위험하지만, 관찰과 제어는 더 유연해야 한다. eBPF는 이 두 요구를 절충한다.

그래서 현대 리눅스 관측성 스택에서 매우 중요하다.

- **📢 섹션 요약 비유**: 안전한 유리창 너머로 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안을 들여다보는 망원경이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
eBPF Program
  v verifier
Kernel Hook
  v
Safe Execution
```

| 요소 | 역할 |
| :-- | :-- |
| Verifier | 안전성 검사 |
| Hook | 실행 지점 |
| Map | 상태 공유 |

eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 이벤트에 붙어서 동작한다. 위험한 루프나 무한 실행을 막기 위해 검증기를 통과해야 한다.

- **📢 섹션 요약 비유**: 놀이기구에 타기 전에 안전 점검을 받는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) | [LKM](/studynote/02_operating_system/01_overview_architecture/067_lkm/) |
| :-- | :-- | :-- |
| 안전성 | 높음 | 상대적으로 낮음 |
| 유연성 | 높음 | 높음 |
| 적용 | 관측/보안/네트워킹 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능 확장 |

| 기능 | 예 |
| :-- | :-- |
| [Tracing](/studynote/04_software_engineering/uncategorized/657_observability/) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 경로 추적 |
| Networking | 필터링/오프로드 |
| [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 강화 |

eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 고치지 않고도 확장할 수 있어 운영 부담이 적다.

- **📢 섹션 요약 비유**: 벽에 구멍을 내지 않고도 카메라를 설치하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. verifier가 안전성을 보장하는가?
2. hook과 map을 이해하는가?
3. [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수정 없이 필요한가?
4. 관측성과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용을 분리하는가?
5. [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향과 제약을 아는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- eBPF를 단순 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모듈로 보는 설계
- 안전성 검증을 무시하는 설계
- 과도한 hook 남발 설계
- 관측과 제어를 혼동하는 설계

기술사 관점에서는 eBPF를 "[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내 안전 실행 프레임워크"로 설명해야 한다.

- **📢 섹션 요약 비유**: 안전장치가 있는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 전용 작업대다.

---

## Ⅴ. 기대효과 및 결론

eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 가시성과 제어를 크게 높인다. 그래서 클라우드/보안 운영의 핵심 기술이 되었다.

결론적으로 eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내 샌드박스 프로그램 프레임워크다.

- **📢 섹션 요약 비유**: 안전하게 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 더 똑똑하게 만드는 도구다.

---

## 관련 개념 맵

```text
BPF
  v
eBPF
  v
Verifier / Map
  v
Observability
```

---

## 관련 키워드 및 발전 흐름도

```text
Packet Filter
  v
BPF
  v
eBPF
  v
Kernel Observability
```

---

## 어린이를 위한 3줄 비유 설명

[커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안을 안전하게 들여다봐요.
무엇이 일어나는지 볼 수 있어요.
eBPF는 그런 똑똑한 안경이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 800

<- **이전**: [68. 동적 커널 패치 (Live Patching) - kpatch, kGraft](/studynote/02_operating_system/01_overview_architecture/068_live_patching/)
**다음**: [70. 하드웨어 추상화 계층 (HAL, Hardware Abstraction Layer)](/studynote/02_operating_system/01_overview_architecture/070_hal/) ->

---
