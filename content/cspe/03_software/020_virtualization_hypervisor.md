---
title: "가상화 — Type 1·Type 2 하이퍼바이저 (Virtualization Hypervisor)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 20
---

# 📖 【암기용】 개념 완전 이해

> 목적: 가상화와 하이퍼바이저를 처음 봐도 물리 자원을 여러 VM에 나누어 제공하는 계층으로 이해하게 만든다. 시험 답안 양식이 아니라, CPU·메모리·I/O 가상화 원리를 설명한다.

## 한눈에
- **개요**: 하이퍼바이저는 물리 서버 위에서 여러 가상머신이 독립 OS처럼 실행되도록 CPU, 메모리, I/O를 중재한다.
- **왜 필요한가**: 서버별 OS와 애플리케이션을 물리 장비에 1:1로 배치하면 자원 낭비와 장애 영향이 커진다. 가상화는 통합, 격리, 이동성을 제공한다.
- **핵심 직관**: 한 건물의 전기, 수도, 엘리베이터를 관리자가 나누어 각 사무실이 독립 공간처럼 쓰게 하는 구조다.

## 깊이 이해
- **배경·문제의식**: 기업 서버는 평균 CPU 사용률이 10~30% 수준인 경우가 많았다. VM은 여러 OS를 한 물리 서버에 통합해 자원 사용률을 높이고 운영 단위를 표준화한다.
- **작동 원리**: 하이퍼바이저는 privileged instruction을 trap하거나 하드웨어 지원(VT-x, AMD-V)으로 VM exit를 처리한다. 메모리는 shadow page table 또는 EPT/NPT로 매핑하고, I/O는 emulation, paravirtual driver, passthrough로 처리한다.
- **비유**: 임대 사무실 입주사는 자기 사무실만 보지만 건물 관리자는 전체 전력과 출입 통제를 관리한다. 입주사 간 벽이 isolation이다.
- **구체 예시**: Type 1은 ESXi, Hyper-V, KVM처럼 하드웨어 위에 직접 동작하고, Type 2는 VirtualBox, VMware Workstation처럼 host OS 위에서 동작한다.
- **흔한 오해·주의점**: VM은 container보다 무겁다는 단순 비교로 끝내면 부족하다. VM은 guest kernel까지 격리하고, container는 host kernel을 공유한다.

## 연결 개념
- Type 1/Type 2 Hypervisor — 배치 위치에 따른 분류
- VM Exit — guest 실행이 hypervisor 개입으로 전환되는 사건
- Consolidation — 여러 물리 서버 workload를 VM으로 통합하는 전략

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 하이퍼바이저는 Type 1/Type 2 구분을 넘어 CPU·메모리·I/O 가상화, VM exit 비용, 격리와 통합 trade-off로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하이퍼바이저는 물리 자원을 추상화해 여러 VM에 독립 CPU, 메모리, 디바이스처럼 제공하는 가상화 제어 계층이다.
> 2. **가치**: 서버 통합, workload 격리, live migration, snapshot으로 운영 유연성과 자원 사용률을 높인다.
> 3. **판단 포인트**: Type 1/Type 2, CPU virtualization, EPT/NPT, I/O emulation vs passthrough, VM exit 비용을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상화 계층 구조 이해 확인 | Type 1, Type 2, guest OS, host OS | 클라우드 VM 설명만으로 끝내지 않음 |
| 자원 가상화 원리 확인 | CPU trap, memory mapping, I/O virtualization | CPU만 설명하고 메모리·I/O 누락하지 않음 |
| 운영 판단 확인 | consolidation, isolation, VM exit overhead | VM과 container 차이 단순 우열화 지양 |

> 요약: 이 문제는 가상화 구조와 성능 오버헤드, 격리 수준을 균형 있게 설명하는지 확인한다.

---

## Ⅰ. 개요 및 필요성

하이퍼바이저는 물리 자원을 VM에 제공하는 가상화 계층이다. 기업 시스템은 서버 통합, 장애 격리, 표준 이미지 배포, live migration을 위해 가상화를 사용한다. 핵심 과제는 격리와 오버헤드의 균형이다.

---

## Ⅱ. 구조 및 구성요소

```text
Physical Hardware -> Hypervisor -> VM1 / VM2 / VM3
       / CPU Virtualization: vCPU Scheduling, VM Exit
       / Memory Virtualization: Guest VA -> Guest PA -> Host PA
       / I/O Virtualization: Emulation / VirtIO / Passthrough
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Hypervisor | VM 생성, 자원 할당, 격리 제어 | Type 1은 bare-metal, Type 2는 host OS 위 |
| vCPU Scheduler | 물리 CPU를 vCPU에 배분 | overcommit ratio 관리 |
| Virtual Device | guest I/O 요청 중재 | emulation, paravirtual, SR-IOV |

> 요약: 하이퍼바이저는 CPU, 메모리, I/O를 각각 가상화하고 VM 간 격리를 유지한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Guest Instruction -> Execute in VMX Non-root
  / Privileged Event -> VM Exit -> Hypervisor Handle -> VM Entry
Guest Memory Access -> EPT/NPT Translation -> Host Physical Memory
Guest I/O -> VirtIO / Emulation / Passthrough -> Physical Device
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | vCPU가 guest instruction 실행 | CPU ready time |
| 2 | privileged event 발생 시 VM exit | VM exit/sec |
| 3 | EPT/NPT로 2단계 주소 변환 | EPT violation, TLB miss |
| 4 | I/O 요청을 가상 디바이스로 처리 | IOPS, latency p99 |

> 요약: VM 실행은 대부분 직접 실행하고, privileged event와 I/O에서 hypervisor가 개입해 격리와 제어를 수행한다.

---

## Ⅳ. 특징

| 구분 | Type 1 Hypervisor | Type 2 Hypervisor | 수치·판단 기준 |
|:---|:---|:---|:---|
| 위치 | 하드웨어 위 직접 실행 | host OS 위 실행 | 운영 서버는 Type 1 우선 |
| 대표 | ESXi, Hyper-V, KVM | VirtualBox, Workstation | 개발·테스트는 Type 2 가능 |
| 오버헤드 | 낮은 host 경로 | host OS 스케줄링 추가 | CPU ready 5% 이하 |
| 격리 | VM별 guest kernel 격리 | host 의존성 존재 | tenant isolation 요구 |

> 요약: Type 1은 운영 서버와 클라우드 기반, Type 2는 개발·교육·테스트 환경에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 물리 서버 1:1 배치 | VM 기반 consolidation | 평균 CPU 사용률 30% 이하 서버 통합 |
| 비용/성능 | native 실행 | VM exit, EPT, I/O 오버헤드 | CPU ready 5% 이하, p99 관리 |
| 운영/위험 | 장비 단위 장애 | host 장애 시 다수 VM 영향 | HA cluster, live migration 필요 |

> 요약: VM 도입은 자원 통합 이익과 host 장애 영향, hypervisor 오버헤드를 함께 평가한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Noisy Neighbor | CPU·I/O overcommit | reservation, limit, QoS | CPU ready, I/O latency p99 |
| Escape 취약점 | hypervisor 또는 device emulation 결함 | 패치, device isolation, 최소 권한 | CVE patch SLA |
| Single Host Failure | host 장애에 VM 집중 | HA, live migration, anti-affinity | HA failover time, RTO |

> 요약: 가상화 리스크는 자원 경합, 격리 취약점, host 장애 집중이며 예약과 HA로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| CPU | CPU ready 5% 이하 | vCenter, KVM steal time |
| Memory | ballooning/swap 0 또는 기준선 이하 | hypervisor metrics |
| I/O | storage latency p99 목표 충족 | fio, datastore latency |

> 요약: VM 운영은 CPU ready, ballooning, storage latency p99가 핵심 점검 지표다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 운영 서버는 Type 1 하이퍼바이저와 HA cluster를 기본으로 구성하고 anti-affinity로 동일 서비스 VM을 서로 다른 host에 배치함.
2. 고성능 네트워크·스토리지는 VirtIO, vhost, SR-IOV, PCI passthrough 중 격리 요구와 p99 latency 목표에 맞춰 선택함.
3. overcommit은 vCPU:pCPU 3:1 이하에서 시작하고 CPU ready 5% 초과, ballooning 발생 시 증설 또는 VM 재배치를 수행함.

**결론 (2줄):**
- 기술사 판단: 강한 OS 격리와 운영 이동성이 필요하면 VM, 커널 공유와 빠른 배포가 우선이면 container를 선택함.
- 향후 방향: confidential VM, microVM, hardware-assisted isolation으로 VM 격리와 배포 속도의 간극을 줄이는 방향으로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "하이퍼바이저를 설명하시오" | CPU, 메모리, I/O 가상화 흐름 | Type 1과 Type 2 비교 |
| 요구사항 명시형 | "비교하시오", "구축 방안을 제시하시오" | VM exit, EPT, I/O 경로 진단 | consolidation, isolation, HA 선택 기준 |

> 요약: 구축형은 Type 분류보다 CPU ready, overcommit, HA, I/O 경로 선택을 중심으로 답안을 전환한다.
