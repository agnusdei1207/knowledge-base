---
sidebar:
  order: 112
  label: "112. 가상 기지국 vRAN"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 네이티브 기지국 가상화 : vRAN (Virtualized Radio Access Network)"
date: "2026-08-22T08:15:00+09:00"
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

- **가상 무선 접속망(Virtualized Radio Access Network, vRAN)**: 전용 ASIC/DSP 하드웨어 어플라이언스로 구현되던 기지국 기저대역 처리 장치(BBU: CU 및 DU)를 표준 상용 x86 COTS(Commercial Off-The-Shelf) 서버 상에서 소프트웨어(가상머신 또는 클라우드 네이티브 컨테이너) 인스턴스로 구동하는 기술.
- **하드웨어 가속기(Hardware Accelerator / SmartNIC)**: x86 CPU 단독으로는 감당하기 어려운 초고연산 High-PHY 계층의 LDPC(채널 부호화) 및 FFT 연산을 전담 처리하여 CPU 부하를 제거하는 전용 가속 카드(FPGA, eASIC, GPU).

</details>

- 정의/개념: 기지국 기저대역 연산(CU/DU)을 범용 COTS 서버의 **클라우드 네이티브 컨테이너(K8s/vDU/vCU)** 환경으로 가상화하고, **실시간 커널(PREEMPT_RT)** 과 **하드웨어 가속기(Lookaside/Inline)** 를 결합하여 무선 처리 시한을 완벽히 만족하는 **소프트웨어 정의 기지국 플랫폼**
- 배경/필요성: 특정 벤더 하드웨어에 종속된 레거시 BBU의 높은 구축·유지보수 비용(CapEx/OpEx)을 절감하고, 트래픽 수요에 따른 기지국 자원의 탄력적 오토스케일링(Auto-Scaling) 및 CI/CD 자동화 배포를 실현할 요구

#### 한줄 요약
- COTS 서버 상에서 vCU/vDU를 컨테이너로 가상화하고 가속기를 결합하여 탄력적 기지국 운영을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **인라인 가속(Inline Acceleration) vs 룩어사이드 가속(Lookaside Acceleration)**: PHY 계층 전체와 프론트홀 eCPRI를 가속 카드 내부에서 직결 처리하는 방식(Inline)과, x86 CPU가 LDPC 부호화 연산만을 PCIe를 통해 가속 카드로 오프로드하는 방식(Lookaside).
- **실시간 리눅스(Real-Time Linux / PREEMPT_RT)**: 5G TDD 슬롯 주기(125$\mu\text{s}$~1ms) 내에 스케줄링 및 무선 처리를 완료할 수 있도록, 커널 선점성을 부여하여 인터럽트 지터(Jitter)를 수 마이크로초 이내로 제어하는 OS.

</details>

- **소프트웨어 기반 탄력적 확장성**: 트래픽이 밀집한 핫스팟 셀에 vDU/vCU 자원을 동적으로 집중 할당하고 야간 유휴 시 자원 회수
- **하드웨어 디커플링(Decoupling) 및 비용 절감**: 범용 x86 서버 생태계를 활용하여 기지국 인프라 조달 비용 절감 및 벤더 종속 탈피
- **클라우드 네이티브 운영 자동화 (CI/CD)**: 신규 기능(5G Rel-17/18) 추가 및 보안 패치를 현장 하드웨어 교체 없이 소프트웨어 무중단 OTA 배포

#### 한줄 요약
- COTS 서버 기반 탄력적 확장, Inline/Lookaside 가속, PREEMPT_RT 실시간성, CI/CD 소프트웨어 배포를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SR-IOV 및 DPDK**: 범용 서버의 네트워크 가상화 오버헤드를 제거하기 위해 커널 네트워크 스택을 우회(DPDK)하고 물리 NIC 포트를 가상머신/컨테이너에 1:1 직결(SR-IOV)하여 초고속 라인 레이트 패킷 전송을 달성하는 기술.

</details>

```text
[ COTS 범용 x86 서버 하드웨어 풀 (Dell, HPE x86 Server) ]
 ├─ Intel Xeon / AMD EPYC CPU (실시간 코어 격리: CPU Pinning)
 ├─ PCIe vRAN 가속 카드 (eASIC / FPGA: LDPC FEC 가속)
 └─ 100Gbps SmartNIC (IEEE 1588 PTP 시간 동기화 내장)
                           │
                           ▼ (가상화 및 오케스트레이션 계층)
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 클라우드 네이티브 vRAN 플랫폼 (Red Hat OpenShift / K8s Baremetal) ]    │
│  ├─ 실시간 OS 커널 (RHEL with PREEMPT_RT Patch)                         │
│  ├─ 초저지연 패킷 처리 엔진 (DPDK + SR-IOV)                              │
│  ├─ vCU-CP / vCU-UP 컨테이너 (RRC, PDCP 처리: 비실시간 계층)            │
│  └─ vDU 컨테이너 (RLC, MAC, High-PHY 스케줄링: 초정밀 실시간 계층)       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Open Fronthaul: eCPRI Option 7-2x)
                                     ▼
                      [ 물리 무선 장치 (Open RAN RU) ]
```

선의 의미: 범용 x86 하드웨어 위에 RTOS 및 K8s 플랫폼이 탑재되어 vCU와 vDU가 컨테이너로 격리 구동되고, 가속기와 DPDK를 통해 RU와 초저지연 eCPRI 통신을 수행하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **범용 x86 서버 (COTS)** | 고성능 CPU, 고속 DDR5 메모리, PCIe Gen5 슬롯을 제공하는 표준 서버 하드웨어 | Telco Grade Server |
| **실시간 OS (PREEMPT_RT)**| TDD 슬롯(0.5ms) 내의 결정론적(Deterministic) 무선 스케줄링 실행 보장 | RT Kernel |
| **vRAN 가속기 (SmartNIC)** | LDPC Encoding/Decoding, FFT/IFFT 등 극고부하 PHY 연산 하드웨어 오프로드 | Inline / Lookaside |
| **DPDK & SR-IOV** | 커널 인터럽트를 배제한 폴링 모드(PMD) 패킷 처리로 eCPRI 프론트홀 지연 최소화 | Kernel Bypass |
| **vDU 컨테이너** | 1ms 이내의 실시간 MAC 스케줄링, 무선 자원 블록(RB) 할당 및 High-PHY 실행 | Real-time vDU |
| **vCU 컨테이너** | 호 설정, 이동성 제어(RRC), 사용자 데이터 암호화(PDCP) 및 코어망 인터페이스 | Cloud vCU |

#### 한줄 요약
- COTS x86 서버, PREEMPT_RT 커널, vRAN 가속기, DPDK/SR-IOV, vDU/vCU 컨테이너가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CPU 격리 및 피닝(CPU Pinning / Isolation)**: vDU 컨테이너가 사용하는 특정 x86 CPU 코어를 OS 태스크 스케줄러 대상에서 제외(Isolate)하고 100% vDU 프로세스 전용으로 고정(Pin)하여 컨텍스트 스위칭 지터를 0으로 만드는 튜닝 기법.

</details>

```text
1. RU로부터 eCPRI 디지털 IQ 데이터 프레임이 COTS 서버의 100G SmartNIC으로 인입
            │
            ▼
2. SR-IOV 및 DPDK를 통해 커널을 거치지 않고 vDU 사용자 공간 메모리로 제로 카피 DMA 전달
            │
            ▼
3. vDU가 초고연산 LDPC 복호화 요청을 PCIe 버스를 통해 하드웨어 가속기(FPGA/eASIC)로 전달
            │
            ▼
4. 가속기가 100$\mu\text{s}$ 이내에 복호화를 완료하고 결과를 vDU로 반환 ➔ vDU가 실시간 MAC 스케줄링 완료
            │
            ▼
5. F1 인터페이스(GTP-U)를 통해 vCU 풀로 데이터 전달 ➔ 5G 코어망(UPF)으로 최종 패킷 라우팅
```

**동작 원리**

1. **커널 우회 수신**: DPDK를 통해 NIC 수신 링 버퍼에서 패킷을 직접 읽어 레이턴시 제거
2. **코어 격리 연산**: CPU Pinning된 전용 코어가 OS 간섭 없이 무선 프로토콜 스케줄러 실행
3. **하드웨어 오프로드**: 연산 집약적인 기저대역 복호화를 전용 가속 카드로 넘겨 CPU 코어 절약
4. **결정론적 완결**: 5G TDD 무선 서브프레임 경계 이전에 모든 상향/하향 신호 처리 100% 완료
5. **중앙 집중 연계**: 처리된 패킷을 가상화된 상위 vCU 계층으로 전달하여 전송 완수

#### 한줄 요약
- DPDK 제로 카피 수신, 전용 코어 스케줄링, 가속기 LDPC 연산, 서브프레임 내 완료, vCU 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전용 BBU vs VM 기반 vRAN vs 클라우드 네이티브 컨테이너 vRAN (cRAN)**: 레거시 하드웨어 어플라이언스, 1세대 가상머신 vRAN, 차세대 경량 컨테이너 기반 vRAN의 비교.

</details>

| 비교 항목 | 전통적 전용 기지국 (Legacy BBU) | 1세대 VM 기반 vRAN | 차세대 컨테이너 기반 vRAN (CNF) |
|:---|:---|:---|:---|
| **실행 인프라** | **특화된 전용 하드웨어 (ASIC/DSP)**| 상용 서버 + 하이퍼바이저 (KVM/ESXi)| **상용 서버 + 베어메탈 K8s 컨테이너**|
| **자원 효율성** | 피크 트래픽 기준 고정 (자원 낭비) | 게스트 OS 오버헤드로 다소 저하 | **극대화 (초경량 프로세스 격리)** |
| **스케일링 속도** | 물리 하드웨어 증설 필요 (수개월) | 가상머신 기동 수 분 소요 | **초 단위 오토스케일링 ($\le 5\text{초}$)** |
| **운영 복잡도** | 벤더별 상이한 폐쇄적 툴셋 | 가상화 인프라 관리 부담 | **전사 GitOps 및 CI/CD 단일 파이프라인**|
| **실시간 지터 제어** | 하드웨어 결정론적 (지터 0) | 하이퍼바이저 간섭으로 지터 발생 위험| **PREEMPT_RT + 베어메탈 직결로 지터 극소화**|

#### 한줄 요약
- 레거시 BBU는 폐쇄적 고비용, VM vRAN은 가상화 오버헤드가 있으나, 컨테이너 vRAN은 초경량 고효율 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **무선 처리 시한 위반(Deadline Miss)**: vDU의 스케줄링 연산이 5G 슬롯 시한(통상 $500\mu\text{s}$)을 넘겨 지연되면, 단말이 보낸 상향 패킷이 폐기되거나 하향 전송 타이밍을 놓쳐 전사 셀이 드롭(Drop)되는 치명적 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 범용 OS의 CPU 컨텍스트 스위칭 및 인터럽트로 인한 **vDU 무선 처리 시한 위반(Deadline Miss)** | **PREEMPT_RT 커널 적용, CPU 코어 격리(CPU Pinning) 및 C-State 절전 모드 비활성화** | 스케줄링 지터 $\le 5\mu\text{s}$ 극소화 및 무선 프레임 드롭 0% 달성 |
| Massive MIMO 환경에서 x86 CPU 단독 처리 시 발생하는 **CPU 사용률 100% 포화 및 서버 폭증** | **인라인(Inline) 또는 룩어사이드(Lookaside) PCIe 가속 카드 기반 LDPC FEC 오프로드** | CPU 사용률 70% 절감 및 단일 x86 서버당 수용 셀 용량 4배 확대 |
| 다수 vDU 컨테이너 간 리소스 경합으로 인한 **순간적 패킷 처리 지연 및 처리율 급락** | **K8s CPU Manager 기반 정적 코어 독점 할당 및 SR-IOV 가상 기능(VF) 전용 매핑** | 컨테이너 간 리소스 간섭 원천 차단 및 라인 레이트 대역폭 보증 |

#### 한줄 요약
- RTOS/CPU Pinning으로 지터를 방지하고, 전용 가속기로 CPU를 보존하며, K8s 정적 할당으로 간섭을 차단한다.

## Ⅶ. 결론

- 5G-Advanced 및 6G 통신망의 경제성과 민첩성을 확보하기 위해 **클라우드 네이티브 컨테이너 기반 vRAN 아키텍처**는 전 세계 주요 통신사(MNO)의 필수 전략으로 도입되고 있으며, 실무 구축 시 **COTS x86 하드웨어 최적화**, **하드웨어 가속기(eASIC/FPGA)의 전략적 오프로드**, **O-RAN 개방형 프론트홀 인터페이스 연동**을 결합하여 개방형 자율 이동통신 인프라를 완성

#### 한줄 요약
- COTS 서버 상의 컨테이너 가상화와 하드웨어 가속기 및 RTOS를 결합하여 고효율 5G/6G vRAN을 실현한다.
