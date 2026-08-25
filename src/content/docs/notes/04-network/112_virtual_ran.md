---
sidebar:
  order: 112
  label: "112. 가상 기지국 vRAN"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 네이티브 기지국 가상화 : vRAN"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 112
extra:
  question_no: "112"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "vCU/vDU 가상화(Container/K8s), COTS x86 서버, 실시간 OS(RTOS), 하드웨어 가속기(Lookaside/Inline)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **vRAN (Virtualized RAN)**: 전용 하드웨어 어플라이언스로 구현되던 BBU(CU/DU)를 표준 x86 COTS 서버 상의 컨테이너/VM으로 구동하는 가상화 기지국.
- **Hardware Accelerator (vRAN 가속기)**: x86 CPU 부하를 방지하기 위해 High-PHY 계층의 LDPC 부호화 및 FFT 연산을 전담하는 PCIe 가속 카드(FPGA/eASIC/GPU).

</details>

- 정의/개념: 기지국 기저대역(CU/DU)을 **범용 COTS 서버 상의 클라우드 네이티브 컨테이너로 가상화하고 실시간 OS 및 가속기로 구동하는 소프트웨어 기지국 기술**
- 배경/필요성: 전용 ASIC 하드웨어 기지국의 **막대한 구축/유지보수 비용, 트래픽 변동에 따른 동적 자원 스케일링 불가 및 신규 기능 배포 지연**

#### 한줄 요약
- COTS 서버 가상화, 클라우드 네이티브 컨테이너, 하드웨어 오프로드를 통해 기지국 민첩성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PREEMPT_RT Real-Time Kernel**: 리눅스 커널의 인터럽트 지연을 $5\mu\text{s}$ 이하로 억제하여 5G TDD 무선 서브프레임(0.5ms) 내의 결정론적 연산을 보장하는 실시간 패치.
- **DPDK (Data Plane Development Kit)**: 커널 네트워크 스택을 우회하여 유저 공간 메모리로 직접 패킷을 초고속 수신하는 라이브러리.

</details>

- **하드웨어-소프트웨어 완전 분리(Decoupling)**: 고가의 독점 장비 대신 **범용 상용 서버(COTS x86) 상에서 소프트웨어로 기지국 구현**
- **실시간 결정론적 스케줄링(Deterministic)**: PREEMPT_RT 실시간 커널과 **CPU 피닝(Pinning)을 통해 무선 프레임 시한 엄격 준수**
- **클라우드 오토스케일링 및 CI/CD**: 쿠버네티스(K8s) 오케스트레이션을 통해 **트래픽 수요에 따른 vDU/vCU 인스턴스 자동 확장**

#### 한줄 요약
- 하드웨어 분리, 실시간 결정론적 스케줄링, 클라우드 네이티브 오토스케일링을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **vCU vs vDU**: 비실시간 제어를 담당하는 클라우드 vCU와 1ms 이내의 실시간 변복조 스케줄링을 수행하는 엣지 vDU.

</details>

```text
[클라우드 네이티브 vRAN 시스템 토폴로지]
|-- COTS x86 Server Hardware (Intel Xeon/AMD EPYC, 100G SmartNIC PTP, PCIe Gen5)
|   `-- Hardware Accelerator (FPGA / eASIC: LDPC FEC 가속 카드)
`-- Cloud-Native vRAN Platform (Baremetal K8s / PREEMPT_RT Real-Time Kernel)
    |-- DPDK & SR-IOV Engine (커널 우회 제로 카피 패킷 수집)
    |-- vCU Container (RRC 호 제어, PDCP 암호화: 비실시간 계층)
    `-- vDU Container (RLC, MAC, High-PHY 스케줄링: 1ms 실시간 계층)
`-- Physical Radio Unit (Open RAN RU: eCPRI Option 7-2x 프론트홀 직결)
```

선의 의미: 범용 x86 하드웨어 위에 RTOS 및 K8s 플랫폼이 탑재되어 vCU와 vDU가 컨테이너로 격리 구동되고 가속기를 통해 RU와 초저지연 통신을 수행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **범용 x86 서버 (COTS)** | 고성능 CPU, 고속 메모리, PCIe Gen5 슬롯을 제공하는 **표준 상용 서버** | Telco Server |
| **실시간 OS (PREEMPT_RT)**| TDD 슬롯(0.5ms) 내의 **결정론적 무선 스케줄링 실행 보장** | RT Kernel |
| **vRAN 가속기 (SmartNIC)** | LDPC 복호화, FFT 등 **초고연산 PHY 계층 하드웨어 오프로드** | Inline / Lookaside |
| **DPDK & SR-IOV** | 커널 인터럽트를 배제한 **폴링 모드(PMD) 패킷 처리로 프론트홀 지연 극소화**| Kernel Bypass |
| **vDU 컨테이너** | 1ms 이내의 **실시간 MAC 스케줄링, 자원 블록 할당 및 High-PHY 실행** | Real-time vDU |
| **vCU 컨테이너** | **호 설정, 이동성 제어(RRC), 사용자 데이터 암호화(PDCP) 및 5GC 인터페이스**| Cloud vCU |

#### 한줄 요약
- COTS x86 서버, PREEMPT_RT 커널, vRAN 가속기, DPDK/SR-IOV, vDU/vCU 컨테이너가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CPU Pinning (CPU 피닝)**: OS의 스케줄러 간섭을 차단하기 위해 특정 CPU 코어를 vDU 프로세스 전용으로 100% 격리 할당하는 기술.

</details>

```text
vRAN SmartNIC 패킷 수신, 하드웨어 오프로드 및 vCU 라우팅 파이프라인
        │
   1. [eCPRI 프레임 인입] RU로부터 eCPRI 패킷이 COTS 서버의 100G SmartNIC으로 인입
        │
   2. [커널 우회 제로 카피] SR-IOV 및 DPDK를 통해 커널을 거치지 않고 vDU 메모리로 직접 DMA
        │
   3. [하드웨어 FEC 가속 오프로드] vDU가 초고연산 LDPC 복호화 요청을 전용 가속 카드로 전달
        │
   4. [100us 내 복호화 완료] 가속기가 복호화 결과를 vDU로 반환하고 실시간 MAC 스케줄링 완료
        │
   ▼
5. [vCU 및 5GC 라우팅] F1-U(GTP-U)를 통해 vCU 풀로 데이터 전달 후 5G 코어망(UPF)으로 라우팅
```

#### 한줄 요약
- DPDK 제로 카피 수신 → 전용 코어 스케줄링 → 가속기 LDPC 연산 → 서브프레임 내 완료 → vCU 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Legacy BBU** vs **1세대 VM vRAN** vs **차세대 컨테이너 vRAN (CNF)**.

</details>

| 비교 항목 | 전통적 전용 기지국 (Legacy BBU) | 1세대 VM 기반 vRAN | 차세대 컨테이너 기반 vRAN (CNF) |
|:---|:---|:---|:---|
| **실행 인프라** | **특화된 전용 하드웨어 (ASIC/DSP)**| 상용 서버 + 하이퍼바이저 (KVM/ESXi)| **상용 서버 + 베어메탈 K8s 컨테이너**|
| **자원 효율성** | 피크 트래픽 기준 고정 (자원 낭비) | 게스트 OS 오버헤드로 다소 저하 | **극대화 (초경량 프로세스 격리)** |
| **스케일링 속도** | 물리 하드웨어 증설 필요 (수개월) | 가상머신 기동 수 분 소요 | **초 단위 오토스케일링 ($\le 5\text{초}$)** |
| **운영 복잡도** | 벤더별 상이한 폐쇄적 툴셋 | 가상화 인프라 관리 부담 | **전사 GitOps 및 CI/CD 단일 파이프라인**|
| **실시간 지터 제어**| 하드웨어 결정론적 (지터 0) | 하이퍼바이저 간섭으로 지터 발생 위험| **PREEMPT_RT + 베어메탈 직결로 지터 극소화**|

#### 한줄 요약
- 레거시 BBU는 폐쇄적 고비용, VM vRAN은 가상화 오버헤드가 있으나, 컨테이너 vRAN은 초경량 고효율 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Deadline Miss (무선 처리 시한 위반)**: vDU의 연산 처리가 5G 무선 슬롯 시한($500\mu\text{s}$)을 넘겨 패킷이 폐기되거나 셀 연결이 끊어지는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 범용 OS의 CPU 컨텍스트 스위칭으로 인한 **vDU 무선 처리 시한 위반** | **`PREEMPT_RT 커널, CPU 코어 피닝(Pinning) 및 C-State 절전 해제`** | 스케줄링 지터 $\le 5\mu\text{s}$ 극소화 및 프레임 드롭 제로 달성 |
| Massive MIMO 환경에서 x86 CPU 단독 처리 시 **CPU 사용률 100% 포화** | **`PCIe 가속 카드(FPGA/eASIC) 기반 LDPC FEC 오프로드`** | CPU 사용률 70% 절감 및 단일 서버 수용 용량 4배 확대 |
| 다수 vDU 컨테이너 간 리소스 경합으로 인한 **패킷 처리 지연 발생** | **`K8s CPU Manager 정적 독점 할당 및 SR-IOV VF 전용 매핑`** | 컨테이너 간 간섭 원천 차단 및 라인 레이트 대역폭 보증 |
| 대규모 COTS 서버 팜 구축 시 에너지 소비량 및 전력 비용 폭증 | **`AI 기반 vDU 코어 동적 슬립 제어 및 그린 트래픽 스케줄링`** | 기지국 유휴 시간대 서버 전력 소비 30% 절감 |

#### 한줄 요약
- RTOS/CPU Pinning으로 지터를 방지하고, 전용 가속기로 CPU를 보존하며, K8s 정적 할당으로 간섭을 차단한다.

## Ⅶ. 결론

- 5G-Advanced 및 6G 통신망의 경제성과 민첩성을 확보하기 위해 **클라우드 네이티브 컨테이너 기반 vRAN 아키텍처를 핵심 인프라 전략으로 도입**하되, 실무 구축 시 **COTS x86 하드웨어 최적화, 하드웨어 가속기(eASIC/FPGA)의 전략적 오프로드, O-RAN 개방형 프론트홀 인터페이스 연동**을 결합하여 개방형 자율 이동통신 인프라 완성

#### 한줄 요약
- vRAN은 COTS 서버 상의 컨테이너 가상화와 하드웨어 가속기 및 RTOS를 결합하여 고효율 5G/6G 기지국을 실현하는 핵심 기술이다.