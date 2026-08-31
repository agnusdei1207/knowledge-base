---
sidebar:
  order: 112
  label: "112. 가상 기지국 vRAN"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 네이티브 기지국 가상화 : vRAN"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: CU·DU를 **COTS 서버**에서 구동하는 가상 RAN
- 배경/필요성: 전용 하드웨어 ASIC/DSP 어플라이언스에 의존하던 전통적인 기지국(BBU) 인프라는 특정 통신 장비 제조사 종속(Vendor Lock-in), 트래픽 수요 변동에 따른 유연한 용량 증설의 한계 및 신규 기능 배포 시 현장 장비 교체에 따른 막대한 CAPEX/OPEX를 발생시키는 문제를 드러냄에 따라, 기지국 기저대역 처리 기능(vCU, vDU)을 표준 범용(COTS) x86/ARM 서버 상의 클라우드 네이티브 컨테이너(CNF / Kubernetes)로 가상화하고 실시간 커널(PREEMPT_RT) 및 하드웨어 가속기(FPGA/ASIC/GPU)를 결합한 가상 기지국(vRAN) 기술을 도입하여 **하드웨어와 소프트웨어의 완전한 분리를 통한 벤더 종속 탈피, Kubernetes 기반 기지국 소프트웨어 CI/CD 자동화 및 트래픽 부하에 따른 동적 오토스케일링**을 달성할 필요

#### 한줄 요약
- COTS 서버 가상화, 클라우드 네이티브 컨테이너, 하드웨어 오프로드를 통해 기지국 민첩성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PREEMPT_RT Real-Time Kernel**: 리눅스 커널의 인터럽트 지연을 $5\mu\text{s}$ 이하로 억제하여 5G TDD 무선 서브프레임(0.5ms) 내의 결정론적 연산을 보장하는 실시간 패치.
- **DPDK (Data Plane Development Kit)**: 커널 네트워크 스택을 우회하여 유저 공간 메모리로 직접 패킷을 초고속 수신하는 라이브러리.

</details>

- 하드웨어와 소프트웨어 **분리·독립 배포**
- PREEMPT_RT와 **CPU 피닝** 기반 시한 제어
- Kubernetes 기반 **오토스케일링·CI/CD**

#### 한줄 요약
- 하드웨어 분리, 실시간 결정론적 스케줄링, 클라우드 네이티브 오토스케일링을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **vCU vs vDU**: 비실시간 제어를 담당하는 클라우드 vCU와 1ms 이내의 실시간 변복조 스케줄링을 수행하는 엣지 vDU.

</details>

```text
vRAN
|-- COTS Server
|   |-- Accelerator
|   `-- Real-Time Platform
|       |-- DPDK and SR-IOV
|       |-- vCU
|       `-- vDU
`-- RU
```

선의 의미: 범용 x86 하드웨어 위에 RTOS 및 K8s 플랫폼이 탑재되어 vCU와 vDU가 컨테이너로 격리 구동되고 가속기를 통해 RU와 초저지연 통신을 수행하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **COTS Server** | 범용 연산·메모리·PCIe 자원 제공 |
| **Accelerator** | **LDPC·FFT** 연산 오프로드 |
| **Real-Time Platform** | PREEMPT_RT와 Kubernetes 실행 |
| **DPDK and SR-IOV** | **커널 우회·VF 격리** 패킷 처리 |
| **vCU** | **RRC·PDCP** 비실시간 처리 |
| **vDU** | **RLC·MAC·High-PHY** 실시간 처리 |
| **RU** | 프론트홀 종단과 무선 송수신 |

#### 한줄 요약
- PREEMPT_RT 커널과 전용 가속기가 범용 서버에 없는 결정론과 연산 밀도를 메우므로, 가상화의 유연성을 얻으면서도 서브프레임 마감을 지킨다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CPU Pinning (CPU 피닝)**: OS의 스케줄러 간섭을 차단하기 위해 특정 CPU 코어를 vDU 프로세스 전용으로 100% 격리 할당하는 기술.

</details>

```text
vRAN SmartNIC 패킷 수신, 하드웨어 오프로드 및 vCU 라우팅 파이프라인
        │
       [eCPRI 프레임 인입]
        │
   1. [커널 우회 제로 카피]
        │
   2. [하드웨어 FEC 가속 요청]
        │
   3. [복호화 및 MAC 스케줄링]
        │
   ▼
   4. [vCU 및 5GC 라우팅]
```

- 1. 커널 우회 제로 카피
- 2. 하드웨어 FEC 가속 요청
- 3. 복호화 및 MAC 스케줄링
- 4. vCU 및 5GC 라우팅

#### 한줄 요약
- 서브프레임 마감 준수 여부가 통화 품질을 가르며, 범용 하드웨어의 유연성은 CPU 고정 할당과 가속기 전용화라는 자원 낭비를 대가로만 유지된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Legacy BBU** vs **1세대 VM vRAN** vs **차세대 컨테이너 vRAN (CNF)**.

</details>

| 비교 항목 | 전통적 전용 기지국 (Legacy BBU) | 1세대 VM 기반 vRAN | 차세대 컨테이너 기반 vRAN (CNF) |
|:---|:---|:---|:---|
| 실행 인프라 | 전용 ASIC·DSP | COTS와 하이퍼바이저 | COTS와 베어메탈 Kubernetes |
| 자원 격리 | 하드웨어 고정 | VM 단위 | 컨테이너 단위 |
| 확장 방식 | 장비 증설 | VM 증설 | **컨테이너 오토스케일링** |
| 운영 방식 | 벤더별 도구 | 가상 인프라 관리 | **GitOps·CI/CD** |
| 지터 제어 | 하드웨어 기반 | 하이퍼바이저 간섭 가능 | **PREEMPT_RT·CPU 피닝** |

#### 한줄 요약
- 레거시 BBU는 폐쇄적 고비용, VM vRAN은 가상화 오버헤드가 있으나, 컨테이너 vRAN은 초경량 고효율 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Deadline Miss (무선 처리 시한 위반)**: vDU의 연산 처리가 5G 무선 슬롯 시한($500\mu\text{s}$)을 넘겨 패킷이 폐기되거나 셀 연결이 끊어지는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CPU 문맥 전환으로 **처리 시한 위반** | **PREEMPT_RT·CPU 피닝** | 스케줄링 지터 완화 |
| PHY 연산으로 **CPU 포화** | **FPGA·eASIC FEC 오프로드** | CPU 부하 분산 |
| vDU 간 **자원 경합** | CPU Manager와 **SR-IOV VF** | 컨테이너 간섭 완화 |
| 서버 팜의 전력 비용 증가 | **vDU 코어 동적 휴면** | 유휴 전력 절감 |

#### 한줄 요약
- RTOS/CPU Pinning으로 지터를 방지하고, 전용 가속기로 CPU를 보존하며, K8s 정적 할당으로 간섭을 차단한다.

## Ⅶ. 결론

- 하드웨어 중심의 통신망을 완전한 소프트웨어 및 클라우드 플랫폼 중심의 통신 인프라로 전환시키는 **5G-Advanced 및 6G 클라우드 네이티브 기지국의 절대적 핵심 표준 아키텍처**로 자리 잡았으며, O-RAN 개방형 인터페이스 및 AI 기반 기지국 에너지 절감 알고리즘과의 융합으로 진화하는 가운데, 실무 vRAN 인프라 구축 시에는 **5G 무선 슬롯 시한($500\mu\text{s}$) 내 처리를 보장하는 PREEMPT_RT 실시간 리눅스 커널 패치 및 전용 코어 격리(CPU Pinning/Isolation), vDU의 복잡한 L1 High-PHY(LDPC/FFT) 연산 부하를 전담하는 인라인(Inline) 하드웨어 가속 카드(FPGA/eASIC) 장착, 네트워크 패킷 인터럽트 병목을 제거하는 DPDK 및 SR-IOV 기반 제로카피 고속 패킷 처리**를 결합하여 완벽한 통신사급 가상 기지국 안정성을 완성

#### 한줄 요약
- vRAN은 COTS 서버 상의 컨테이너 가상화와 하드웨어 가속기 및 RTOS를 결합하여 고효율 5G/6G 기지국을 실현하는 핵심 기술이다.
