---
title: "하드웨어 가상화 — VT-x·AMD-V (Hardware Virtualization)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 101
---

## 미리 알고가기

- CPU(Central Processing Unit): 명령어 실행과 특권 모드 전환을 담당하는 프로세서임
- 하이퍼바이저: 하나의 물리 서버에서 여러 VM(Virtual Machine)을 실행·격리하는 소프트웨어 계층임
- VT-x(Intel Virtualization Technology for x86)/AMD-V(AMD Virtualization): x86 프로세서가 가상화 실행 모드와 특권 명령 처리 기능을 제공하는 확장임
- EPT(Extended Page Tables)/NPT(Nested Page Tables): 게스트 물리 주소를 호스트 물리 주소로 변환하는 2단계 주소 변환 기술임
- VM Exit: 게스트 실행 중 하이퍼바이저 개입이 필요한 이벤트로 제어가 전환되는 현상임
- VA(Virtual Address)/PA(Physical Address): 가상 주소와 물리 주소를 구분하는 표기임

## Ⅰ. 개요

- **정의**: 하드웨어 가상화는 CPU가 VM 실행 모드, 특권 명령 트랩, 2단계 주소 변환을 제공해 하이퍼바이저가 게스트 OS(Operating System)를 직접 실행하면서도 격리하도록 지원하는 기술임.
- **배경/필요성**: 순수 소프트웨어 가상화는 특권 명령 변환과 메모리 매핑 유지 비용이 커 성능과 호환성 문제가 있었음. 서버 통합, 격리, 클라우드 인프라 운영에서는 게스트 OS 수정 없이 특권 동작을 제어하고 메모리 격리를 강화할 수 있는 CPU 지원이 필요함.
- **비유**: 건물 관리자가 각 입주사에 독립 사무실을 주되, 출입 통제와 전기 배선을 건물 설비가 직접 지원하는 구조임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CPU 가상화 지원 구조 이해 | root/non-root mode, VMCS(Virtual-Machine Control Structure)/VMCB(Virtual Machine Control Block), VM exit, EPT/NPT | 서버 가상화 전체와 혼동 |

> 요약: 하드웨어 가상화는 CPU가 하이퍼바이저의 격리와 주소 변환을 직접 지원하는 기반 기술임.

## Ⅱ. 특징/비교

| 판단 기준 | 소프트웨어 가상화 | 하드웨어 가상화 |
|:---|:---|:---|
| 특권 명령 처리 | binary translation 또는 paravirtualization 필요 | CPU trap과 VM exit로 처리 |
| 게스트 수정 | OS 수정이나 특수 드라이버가 필요할 수 있음 | 일반 OS 실행 호환성이 높음 |
| 메모리 변환 | shadow page table 관리 부담이 큼 | EPT/NPT로 2단계 변환을 하드웨어화 |
| 성능 병목 | 변환과 trap 비용이 큼 | VM exit 빈도와 I/O(Input/Output) 가상화가 주요 병목 |

> 요약: 하드웨어 가상화는 게스트 호환성과 성능을 높이지만 VM exit와 I/O 경로 관리가 중요함.

- **적용 조건**: CPU 가상화 기능, IOMMU(Input-Output Memory Management Unit), 하이퍼바이저 버전이 워크로드 요구와 맞아야 함
- **선택 지표**: VM exit rate, EPT miss rate, TLB(Translation Lookaside Buffer) miss, CPU ready time을 함께 봐야 함
- **운영 관점**: 성능 최적화와 보안 완화 설정은 같은 기준선에서 관리되어야 함

## Ⅲ. 구성요소

```text
+-------------+      +--------------+      +-------------+
| Guest OS    | ---> | CPU VM mode  | ---> | Hypervisor  |
+-------------+      +--------------+      +-------------+
        |                    |                    |
        v                    v                    v
+-------------+      +--------------+      +-------------+
| Guest VA/PA |      | EPT/NPT      |      | Host memory |
+-------------+      +--------------+      +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| VM 실행 모드 | 게스트와 하이퍼바이저의 특권 실행 상태를 분리함 | 입주자 구역과 관리실 |
| VMCS/VMCB | 게스트 상태, 제어 비트, exit 조건을 저장하는 제어 구조임 | 출입 규칙표 |
| EPT/NPT | 게스트 물리 주소를 호스트 물리 주소로 변환하고 권한을 검증함 | 주소 재배정 장부 |
| 인터럽트·I/O 가상화 | 장치 접근, 인터럽트 전달, DMA(Direct Memory Access) 격리를 처리함 | 공용 설비 관리 |

> 요약: 하드웨어 가상화는 실행 모드, 제어 구조, 주소 변환, I/O 제어가 결합된 CPU 지원 체계임.

## Ⅳ. 절차

```text
+----------+      +----------+      +----------+      +----------+
| Create   | ---> | Run      | ---> | Exit     | ---> | Resume   |
+----------+      +----------+      +----------+      +----------+
```

1. **VM 생성** — 하이퍼바이저가 vCPU(Virtual CPU) 상태, 메모리 매핑, VMCS/VMCB 제어값을 설정함
2. **게스트 실행** — CPU가 non-root 모드에서 게스트 명령을 직접 실행함
3. **VM Exit 처리** — 특권 명령, I/O, page fault, interrupt 발생 시 하이퍼바이저로 전환함
4. **상태 갱신·재진입** — 하이퍼바이저가 이벤트를 처리하고 게스트 상태를 갱신한 뒤 다시 실행함

> 요약: 게스트는 대부분 직접 실행되고, 통제가 필요한 순간에만 하이퍼바이저가 개입함.

## Ⅴ. 문제점 및 개선방안

- **P1 VM Exit 비용**: 빈번한 특권 명령, I/O, timer interrupt가 발생하면 전환 비용으로 성능이 저하됨
- **P1 대응**: paravirtual driver, interrupt coalescing, timer 최적화로 exit 빈도를 줄임 (확인: VM exit rate)
- **P2 주소 변환 오버헤드**: 2단계 page walk와 TLB miss가 메모리 집약 워크로드 지연을 증가시킴
- **P2 대응**: huge page, EPT/NPT tuning, TLB shootdown 최소화로 주소 변환 비용을 낮춤 (확인: EPT miss rate)
- **P3 격리 취약점**: CPU 마이크로아키텍처 공유 자원과 speculative execution이 VM 간 정보 노출 경로가 될 수 있음
- **P3 대응**: CPU microcode, core scheduling, cache partitioning, side-channel mitigation을 적용함 (확인: isolation test)

> 요약: 하드웨어 가상화 병목은 직접 실행 자체보다 exit, address translation, 공유 자원 격리에서 발생하며 워크로드별 튜닝으로 완화함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 클라우드 VM 집적 | VT-x(Intel Virtualization Technology for x86)/AMD-V(AMD Virtualization), EPT/NPT, paravirtual driver를 표준 이미지에 적용해 게스트 OS(Operating System)를 무수정 실행함 | VM exit rate, CPU ready time |
| 데이터베이스 가상화 | huge page와 NUMA(Non-Uniform Memory Access) affinity를 적용해 2단계 주소 변환과 원격 메모리 접근을 줄임 | EPT miss rate, p99 latency |
| 다중 테넌트 보안 | microcode, side-channel 완화, core scheduling 정책을 하이퍼바이저 기준선에 포함함 | isolation test pass, mitigation compliance |

> 요약: 실무에서는 VM 밀도보다 exit 빈도, 메모리 변환 비용, 격리 검증을 함께 확인해야 함.

## Ⅶ. 전망

- **발전 방향**: confidential computing, nested virtualization, hardware-assisted I/O, cloud bare-metal 가상화와 결합해 격리 수준이 고도화됨
- **기술사적 판단**: 가상화 플랫폼 선택은 VM 밀도만이 아니라 VM exit 비용, 메모리 오버헤드, 보안 격리 요구를 기준으로 해야 함
- **기술사 제언**: 운영 환경에서는 CPU feature flag, microcode, 하이퍼바이저 버전, 취약점 완화 상태를 표준 점검 항목으로 관리해야 함
