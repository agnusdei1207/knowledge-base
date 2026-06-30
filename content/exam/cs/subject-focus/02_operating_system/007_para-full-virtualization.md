---
title: "전가상화·반가상화 (Full/Para Virtualization)"
date: "2026-06-30"
weight: 7
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 전가상화(Full Virtualization)는 게스트 OS 수정 없이 하드웨어를 완전히 모사하는 방식이고, 반가상화(Para Virtualization)는 게스트 OS를 수정하여 하이퍼바이저에 직접 요청(Hypercall)함으로써 가상화 오버헤드를 줄이는 방식이다.

## Ⅱ. 구성요소 / 원리
- **전가상화 + 바이너리 변환(Binary Translation)**: 게스트의 특권명령을 런타임에 변환·트랩
- **반가상화 + 하이퍼콜(Hypercall)**: 게스트가 하이퍼바이저 API를 직접 호출
- **게스트 OS 수정 여부**: 전가상화=불필요, 반가상화=필요
- **트랩 앤 에뮬레이트(Trap & Emulate)**: 민감 명령을 가로채 VMM이 대행
- **드라이버**: 반가상화는 전용 가상 드라이버(virtio 등)로 I/O 가속

## Ⅲ. 흐름도 / 구조
```text
[전가상화]                       [반가상화]
게스트 OS(수정X)                 게스트 OS(수정O)
   │ 특권명령                       │ Hypercall(직접 요청)
   ▼ Binary Translation/Trap        ▼
하이퍼바이저(에뮬레이션)          하이퍼바이저(즉시 처리)
   │                                │
   ▼                                ▼
 Hardware                         Hardware
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 가상화 환경에서 성능과 호환성의 균형 확보 |
| 장점 | 전가상화=OS 무수정 호환, 반가상화=낮은 오버헤드·고성능 |
| 한계 | 전가상화=변환 오버헤드, 반가상화=게스트 OS 수정 필요 |

### 전가상화 vs 반가상화 비교표
| 구분 | 전가상화(Full) | 반가상화(Para) |
|:---|:---|:---|
| 게스트 수정 | 불필요 | 필요 |
| 핵심 기법 | Binary Translation/Trap | Hypercall |
| 성능 | 상대적 낮음 | 높음 |
| 예시 | VMware(초기), QEMU | Xen(PV), virtio |

## Ⅴ. 기술사적 적용
- 하드웨어 보조 가상화(VT-x/AMD-V) 등장으로 전가상화 성능 격차 축소
- I/O는 반가상화(virtio) 드라이버로 가속하는 하이브리드 구성이 일반적
- 게스트 무수정 요구(상용 OS) 시 전가상화+HW 가속 조합 채택
