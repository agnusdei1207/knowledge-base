---
sidebar:
  order: 57
  label: "057. 네트워크 기능 가상화 (NFV, Network Functions Virtualization)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "네트워크 기능 가상화 (NFV, Network Functions Virtualization)"
date: "2026-08-13T15:49:00+09:00"
tags:
  - "notes-network"
weight: 57
extra:
  question_no: "057"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 50
  priority_note: "비교•설계형: SDN 연계 가상화 기반축"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 기능 가상화(Network Functions Virtualization, NFV)**: 라우터, 방화벽, L4/L7 스위치 등 전용 장비의 제어 및 전달 기능을 범용 하드웨어 상의 소프트웨어 가상화 환경으로 구현하는 ETSI 아키텍처이다.
- **가상 네트워크 기능(Virtual Network Function, VNF)**: 하이퍼바이저 기반 가상머신(VM) 위에서 독립 구동되는 라우팅/보안 소프트웨어 모듈이다.
- **클라우드 네이티브 네트워크 기능(Cloud-native Network Function, CNF)**: K8s 컨테이너 런타임 위에서 가볍게 구동되는 차세대 Microservice 형태의 네트워크 모듈이다.

</details>

- 정의/개념: **네트워크 기능 가상화(NFV, Network Functions Virtualization)**는 전통적인 전용 하드웨어 네트워크 장비(라우터, 방화벽, L4 스위치)의 소프트웨어 기능을 범용 COTS 서버 하드웨어 상의 가상화(VNF) 또는 컨테이너(CNF) 환경으로 분리하여 구현하는 ETSI 표준 아키텍처이다.
- 배경/필요성: 벤더 전용 하드웨어 어플라이언스의 긴 신규 도입 주기(CAPEX 부담) 및 고정된 자원 용량으로 인한 운용 비효율성(OPEX 증가)을 해결하기 위해 통신사업자(Telco) 주도로 제정되었다.

#### 한줄 요약

- 전용 네트워크 장비의 소프트웨어 기능을 COTS 서버 하드웨어 상의 가상화(VNF) 및 컨테이너(CNF)로 분리 구현하는 ETSI 표준 아키텍처.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **관리 및 오케스트레이션(Management and Orchestration, MANO)**: VNF/CNF 및 NFVI 컴퓨팅/저장/네트워크 자원의 수명주기를 관리하는 ETSI 표준 오케스트레이션 체계이다.
- **상태 동기화(State Synchronization / Session Migration)**: VNF 인스턴스가 오토스케일링되거나 타 노드로 이관될 때 수신 패킷의 L4/L7 세션 컨텍스트를 동기화하는 기술이다.

</details>

- **SW 및 HW 수명주기 분리**: 범용 x86/ARM COTS 서버 하드웨어를 수용함으로써 벤더 종속(Lock-in)을 차단하고 유연한 자원 배치가 가능하다.
- **ETSI MANO 연동 자동화**: NFVO, VNFM, VIM 모듈의 상호작용을 통해 VNF/CNF 인스턴스의 생성, 설정, 상태 감시 및 소멸을 자동 통제한다.
- **탄력적 오토스케일링 (Elastic Scaling)**: 트래픽 증감에 맞춰 동적으로 VM/컨테이너 개수(Scale-Out/In) 및 자원 용량(Scale-Up/Down)을 가변 조정한다.

#### 한줄 요약

- HW/SW 기능 분리, ETSI MANO 기반 자동 오케스트레이션, 트래픽에 따른 동적 탄력 확장성 제공.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NFV 오케스트레이터(NFV Orchestrator, NFVO)**: 네트워크 서비스 오케스트레이션 및 NFVI 전역 자원 할당을 총괄하는 중앙 모듈이다.
- **VNF 관리자(VNF Manager, VNFM)**: 각 VNF 인스턴스의 인스턴스화, 배포, 파기 및 스케일링을 관리하는 모듈이다.
- **가상화 인프라 관리자(Virtualized Infrastructure Manager, VIM)**: OpenStack 또는 K8s와 연동되어 NFVI 가상화 하드웨어 자원을 직접 할당·제어하는 모듈이다.
- **NFV 인프라(NFV Infrastructure, NFVI)**: 컴퓨팅, 저장장치, 네트워크 하드웨어와 하이퍼바이저/컨테이너 가상화 레이어를 합친 물리/가상 기반 구조이다.

</details>

```text
ETSI NFV 참조 아키텍처
├─ 오케스트레이션 관리 계층 (NFV MANO - MANO Framework)
│  ├─ 서비스 오케스트레이터 (NFV Orchestrator - NFVO)
│  ├─ 가상 기능 관리자 (VNF Manager - VNFM)
│  └─ 가상 인프라 관리자 (Virtualized Infrastructure Manager - VIM / OpenStack, K8s)
└─ 실행 인프라 및 기능 계층 (Execution Layer)
   ├─ 가상/클라우드 네트워크 기능 (VNF / CNF - vRouter, vFW, vEPC)
   └─ 하드웨어 및 가상 인프라 (NFVI - COTS Hardware, Hypervisor / Container Runtime)
```

선의 의미: MANO 계층의 NFVO, VNFM, VIM이 하부의 가상 네트워크 기능(VNF) 및 물리 인프라(NFVI) 자원을 수직 통제하는 참조 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| NFV 오케스트레이터 (NFVO) | NSD(네트워크 서비스 명세)를 해석하여 인프라 자원을 예약하고 E2E 네트워크 서비스를 토폴로지 구성 |
| VNF 관리자 (VNFM) | VNF/CNF 인스턴스의 생애주기(Instantiation, Scaling, Healing, Termination) 직접 수행 |
| 가상 인프라 관리자 (VIM) | OpenStack, Kubernetes 기반으로 NFVI 하드웨어(CPU, RAM, Disk, NIC) 자원을 직접 프로비저닝 |
| 가상 네트워크 기능 (VNF / CNF) | vFW(가상 방화벽), vDNS, vEPC, vUPF 등 과거 전용 장비가 수행하던 소프트웨어 패킷 연산 실행 |
| NFV 인프라 (NFVI) | 범용 COTS 서버, SAN 저장장치, L2/L3 스위치 및 KVM/Docker 가상화 런타임 환경 제공 |

#### 한줄 요약

- MANO(NFVO/VNFM/VIM)가 자원과 수명주기를 오케스트레이션하고 VNF/CNF가 소프트웨어 패킷 연산을 수행하며 NFVI가 하드웨어/가상화를 제공하는 구조.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **네트워크 서비스 명세(Network Service Descriptor, NSD)**: 서비스 구축에 필요한 VNF 모듈 목록, 연결 토폴로지(VLD) 및 자원 SLA 파라미터를 정의한 청사진 파일이다.

</details>

```text
1. OSS/BSS의 네트워크 서비스 생성 요청 (NSD Service Request)
      │
      v
2. NFVO -> VIM: NSD 프로필 기반 NFVI 범용 자원 할당 요청 (Resource Allocation)
      │
      v
3. VIM -> VNFM: 가상 VM/컨테이너 자원 식별자 할당 완료 통보 (Resource Granted)
      │
      v
4. VNFM: VNF/CNF 패키지 이미지 수송 및 런타임 인스턴스화 (Instantiation)
      │
      v
5. 패킷 인터페이스 결합 및 텔레메트리 기반 자율 오토스케일링 (State & Scaling)
```

### 동작 원리

1. **OSS/BSS의 네트워크 서비스 생성 요청**
2. **NFVO의 NSD 기반 NFVI 범용 자원 할당 요청**
3. **VIM의 가상 자원 식별자 할당 완료 통보**
4. **VNFM의 VNF/CNF 런타임 인스턴스화**
5. **패킷 인터페이스 결합 및 텔레메트리 기반 오토스케일링**

#### 한줄 요약

- 서비스 요청, NFVO 자원 요구, VIM 자원 할당, VNFM 인스턴스화 및 텔레메트리 오토스케일링 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전용 어플라이언스(Dedicated Hardware Appliance)**: 전용 ASIC 파이프라인과 독점 하드웨어가 일체형으로 고정 판매되는 기존 장비이다.

</details>

| 비교 항목 | **네트워크 기능 가상화 (NFV / VNF, CNF)** | **전용 하드웨어 어플라이언스 (Dedicated HW)** |
|:---|:---|:---|
| 하드웨어 가용성 | 범용 x86/COTS 서버 활용 (특정 벤더 종속 해제) | 제조사 전용 ASIC/FPGA 탑재 하드웨어 장비 |
| 구축 및 확장 속도 | 이미지 기반 자동 배포와 Scale-Out | 물리 장비 조달·설치 필요 |
| 하드웨어 성능 | 가상화 계층의 처리 오버헤드 발생 가능 | 전용 ASIC 기반 고성능 처리 |
| 서비스 체이닝 | Service Function Chaining(SFC) 유연 구현 | 물리 유선 케이블 재배치 필요로 체이닝 불연속 |
| CAPEX / OPEX | 범용 자원 공유로 증설 유연성 확보 | 기능별 전용 장비 구매 필요 |

> 요약: NFV는 COTS 서버 기반의 유연한 자동 확장성 및 서비스 체이닝을 제공하고, 전용 장비는 최고 수준의 전용 HW 성능을 제공.

#### 한줄 요약

- NFV는 COTS 서버 기반의 유연한 자동 확장성 및 서비스 체이닝을 제공하고, 전용 장비는 최고 수준의 전용 HW 성능을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **가상화 오버헤드(Virtualization & Packet IO Overhead)**: 하이퍼바이저 패킷 복사 및 OS 컨텍스트 스위칭으로 인해 패킷 스루풋이 저하되는 현상이다.
- **중앙처리장치(Central Processing Unit, CPU / NUMA Pinning)**: 가상화 인프라의 CPU 소켓 및 코어를 VNF 메모리 버스에 직접 고정 고립 할당하여 지연을 줄이는 기법이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 가상 패킷 I/O 병목 | 커널 소켓 패킷 복사 및 컨텍스트 스위칭 처리 복잡 | DPDK(Data Plane Dev Kit) 및 SR-IOV 직결 적용 | 패킷 처리량과 지연 개선 |
| NUMA 메모리 지연 | 이종 CPU 소켓 전송에 따른 메모리 버스 지연 | CPU NUMA Pinning 및 HugePages 기법 적용 | 메모리 엑세스 오버헤드 최소화 |
| VNF 간 복잡한 체이닝 | 다수 VNF 패킷 순차 전달 시 포워딩 복잡도 증가 | NSH(Network Service Header) 기반 SFC 오케스트레이션 | 유연하고 투명한 VNF 트래픽 체이닝 완성 |
| VNF 이미지 무결성 위협 | 인스턴스화 이미지 변조 및 해킹 | TPM 기반 Remote Attestation 및 이미지 암호화 서명 | 인프라 내 위변조 VNF 인스턴스 구동 차단 |

#### 한줄 요약

- DPDK/SR-IOV 기반 입출력 가속, NUMA 코어 핀닝, NSH 기반 Service Function Chaining으로 NFV 가상화 성능 최적화.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **탄력 확장(Elastic Auto-Scaling)**: 실시간 트래픽 폭주 시 VNF/CNF 인스턴스를 자동으로 증설하고 유휴 시 회수하는 동적 가용성 관리이다.

</details>

- 탄력적 기능 배치는 **NFV**, 고정 고성능 처리는 **전용 장비** 선택.

#### 한줄 요약

- ETSI MANO 준수 및 DPDK/SR-IOV 가속 기반 가상 네트워크 기능(VNF/CNF) 오케스트레이션 구현 필수.
