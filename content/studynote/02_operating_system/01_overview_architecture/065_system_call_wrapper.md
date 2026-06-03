---
title: 65. 시스템 콜 래퍼 (System Call Wrapper)
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시스템 콜 래퍼([[013_system_call|System Call]] Wrapper)는 사용자 공간 함수 호출을 [[022_kernel_role|커널]] 시스템 콜로 변환해 주는 중간 계층이다.
> 2. **가치**: 래퍼는 [[015_abi|ABI]]([[015_abi|Application Binary Interface]]), errno 처리, 이식성, 편의성을 보장한다.
> 3. **판단**: 실제 [[022_kernel_role|커널]] 진입과 [[336_library_vs_framework|라이브러리]] API를 구분해야 시스템 콜의 비용과 동작을 정확히 이해할 수 있다.

---

## Ⅰ. 개요 및 필요성

프로그램이 파일을 읽거나 프로세스를 만들 때는 결국 [[022_kernel_role|커널]]의 도움이 필요하다. 하지만 개발자가 매번 어셈블리 수준의 시스템 콜을 직접 호출하는 것은 번거롭다.

그래서 libc 같은 표준 [[336_library_vs_framework|라이브러리]]가 래퍼를 제공해, 개발자는 일반 함수처럼 호출하고 내부에서 시스템 콜로 연결되게 한다.

- **📢 섹션 요약 비유**: 택배 앱이 대신 문을 열고 창고에 맡겨 주는 것처럼, 사용자는 편하게 요청하고 뒤에서는 더 복잡한 일이 처리된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
User Program
  ↓
Library Wrapper
  ↓
syscall instruction
  ↓
Kernel
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Wrapper | 인자 정리와 호출 [[198_abstraction_control_data_process|추상화]] |
| syscall | [[022_kernel_role|커널]] 진입 명령 |
| [[022_kernel_role|Kernel]] | 실제 자원 접근 |
| errno | 오류 코드 전달 |

시스템 콜 래퍼는 호출 규약과 오류 처리 방식을 숨겨 준다. 그래서 같은 API라도 운영체제와 아키텍처에 따라 내부 구현이 달라질 수 있다.

- **📢 섹션 요약 비유**: 전화번호를 대신 눌러 주는 교환원과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | Wrapper | [[013_system_call|System Call]] | [[336_library_vs_framework|Library]] [[014_api_posix|API]] |
| :-- | :-- | :-- | :-- |
| 위치 | 사용자 공간 | [[022_kernel_role|커널]] 경계 | 사용자 공간 |
| 역할 | 변환/편의 | 실제 [[022_kernel_role|커널]] 기능 | 고수준 기능 |
| 비용 | 낮음~중간 | 상대적으로 큼 | 호출마다 다름 |

Wrapper는 단순한 껍데기가 아니라, 시스템 콜을 안전하고 일관되게 쓰도록 만드는 인터페이스다. 덕분에 같은 코드를 더 쉽게 이식할 수 있다.

- **📢 섹션 요약 비유**: 직접 고속도로 톨게이트를 통과하는 대신, 하이패스를 대신 써 주는 장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[336_library_vs_framework|라이브러리]] API와 시스템 콜을 구분하는가?
2. errno와 반환값의 차이를 이해하는가?
3. 호출 비용이 큰 경로를 알고 있는가?
4. 비동기/차단 호출의 차이를 구분하는가?
5. 이식성 이슈를 고려하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 래퍼와 [[022_kernel_role|커널]] 기능을 같은 것으로 보는 설계
- 시스템 콜 비용을 무시하고 남발하는 설계
- 오류 처리를 반환값만으로 끝내는 설계
- 플랫폼 차이를 고려하지 않는 설계

기술사 관점에서는 래퍼를 "부가 코드"가 아니라 "[[022_kernel_role|커널]]과 프로그램을 연결하는 계약층"으로 봐야 한다.

- **📢 섹션 요약 비유**: 통역사가 있어야 서로 다른 언어를 쓰는 두 사람이 대화할 수 있다.

---

## Ⅴ. 기대효과 및 결론

시스템 콜 래퍼를 이해하면 [[282_performance_tactics|성능]] 병목, 오류 처리, 이식성 문제를 더 명확히 설명할 수 있다.

결론적으로 래퍼는 사용자 공간과 [[022_kernel_role|커널]] 사이의 안전한 중개자다.

- **📢 섹션 요약 비유**: 문지방을 안전하게 넘어가게 해 주는 손잡이 같다.

---

## 관련 개념 맵

```text
User Space
  ↓
Wrapper
  ↓
syscall
  ↓
Kernel Space
```

---

## 관련 키워드 및 발전 흐름도

```text
API Call
  ↓
System Call Wrapper
  ↓
Kernel Entry
  ↓
User-Kernel Boundary
```

---

## 어린이를 위한 3줄 비유 설명

문을 직접 열지 않아도 대신 열어 주는 사람이 있어요.  
시스템 콜 래퍼가 그런 역할을 해요.  
그래서 프로그램이 [[022_kernel_role|커널]]과 쉽게 이야기할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 65 / 800

← **이전**: [[064_rootfs_overlayfs|64. 루트 파일 시스템 (Root Filesystem) / 오버레이 파일 시스템 (OverlayFS)]]
**다음**: [[066_vfs|66. VFS (Virtual File System)]] →

---
