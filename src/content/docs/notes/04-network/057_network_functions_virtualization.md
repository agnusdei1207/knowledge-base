---
sidebar:
  order: 57
  label: "057. 네트워크 기능 가상화 (NFV)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "네트워크 기능 가상화 : NFV (Network Functions Virtualization)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 57
extra:
  question_no: "057"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 50
  priority_note: "ETSI NFV 표준 아키텍처, MANO 프레임워크(NFVO/VNFM/VIM), VNF/CNF 및 하드웨어 가속(DPDK/SR-IOV)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 기능 가상화(Network Functions Virtualization, NFV)**: 전용 하드웨어 어플라이언스(방화벽, 라우터, EPC, IMS 등)로 동작하던 네트워크 기능을 범용 서버(COTS x86/ARM) 상의 가상 머신(VM) 또는 컨테이너(CNF) 소프트웨어 인스턴스로 분리·구동하는 기술 (ETSI 표준).
- **가상 네트워크 기능(Virtual Network Function, VNF)**: 전용 ASIC 장비의 소프트웨어 패킷 처리 로직을 가상화 하이퍼바이저 위에서 독립된 VM 형태로 패키징한 소프트웨어 엔티티.

</details>

- 정의/개념: 독점 전용 하드웨어 장비와 네트워크 기능 소프트웨어를 디커플링(Decoupling)하고, 범용 COTS 인프라 위에서 **MANO 프레임워크** 를 통해 VNF/CNF의 생애주기를 자동화 관리하는 **ETSI 표준 네트워크 가상화 기술**
- 배경/필요성: 신규 네트워크 서비스 배포 시 전용 하드웨어 도입에 소요되는 고비용(CAPEX/OPEX) 및 장기간의 리드 타임을 극복하고, 트래픽 변동에 따른 탄력적 오토스케일링을 달성할 요구

#### 한줄 요약
- 전용 HW 종속을 제거하고 범용 COTS 서버 위에서 VNF 소프트웨어를 MANO로 자동 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MANO(Management and Orchestration)**: ETSI NFV 표준의 핵심 관리 프레임워크로, 가상 인프라 자원(VIM), VNF 생애주기(VNFM), 종단간 네트워크 서비스(NFVO)를 통합 제어하는 오케스트레이션 엔진.
- **서비스 기능 체이닝(Service Function Chaining, SFC)**: 인입된 트래픽을 가상 방화벽 $\rightarrow$ DPI $\rightarrow$ 가상 로드밸런서 $\rightarrow$ 가상 라우터 순으로 소프트웨어 기반 논리 경로를 따라 순차 통과시키는 기술.

</details>

- **하드웨어-소프트웨어 분리(Decoupling)**: 벤더 독점 장비 종속(Lock-in)을 탈피하여 표준 범용 x86/ARM 서버에서 자유롭게 네트워크 소프트웨어 교체 운용
- **탄력적 수평 확장(Auto-Scaling)**: 트래픽 증감에 따라 VNF 인스턴스를 수 분 내에 수평 확장(Scale-out)하거나 축소(Scale-in)하여 자원 활용률 최적화
- **서비스 신속 출시(Agility)**: 물리 장비의 구매·배선 절차 없이 소프트웨어 템플릿(NSD/VNFD) 배포만으로 신규 서비스 개통 시간을 수개월에서 수 시간으로 단축

#### 한줄 요약
- HW/SW 디커플링, MANO 기반 탄력적 오토스케일링, 서비스 체이닝(SFC)을 통한 신속한 서비스 배포를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NFVO(NFV Orchestrator)**: 전체 네트워크 서비스(NS)의 토폴로지 설계, 신규 VNF 생성 및 복수 VIM 간의 물리/가상 자원 조율을 총괄하는 최상위 오케스트레이터.
- **VNFM(VNF Manager)**: 개별 VNF 인스턴스의 생성(Instantiate), 상태 모니터링, 스케일링 및 장애 복구(Self-Healing) 등 생애주기(LCM)를 전담 관리하는 모듈.
- **VIM(Virtualized Infrastructure Manager)**: NFVI의 물리적 컴퓨팅, 스토리지, 네트워크 자원을 가상화하여 할당 및 회수하는 하위 인프라 제어기 (OpenStack, Kubernetes 등).

</details>

```text
┌────────────────────────────────────────────────────────────┐
│ [ ETSI NFV MANO (관리 및 오케스트레이션) ]                  │
│ ├─ NFVO (NFV 오케스트레이터: E2E 서비스 토폴로지 관리)      │
│ ├─ VNFM (VNF 매니저: VNF 생애주기 LCM 제어)                │
│ └─ VIM (가상 인프라 매니저: OpenStack / K8s 자원 할당)     │
└─────────────────────────────┬──────────────────────────────┘
                              │ (자원 프로비저닝 및 라이프사이클 제어)
                              ▼
┌────────────────────────────────────────────────────────────┐
│ [ VNF / CNF 계층 (가상 네트워크 기능) ]                    │
│  [ vFirewall ] ──▶ [ vLoadBalancer ] ──▶ [ vRouter / vUPF ]│
├────────────────────────────────────────────────────────────┤
│ [ NFVI 계층 (NFV 인프라스트럭처) ]                         │
│  ├─ 가상화 계층: 하이퍼바이저 (KVM), 컨테이너 런타임       │
│  └─ 물리 COTS 인프라: COTS x86 서버, NVMe 스토리지, NIC   │
└────────────────────────────────────────────────────────────┘
```

선의 의미: MANO 계층(NFVO/VNFM/VIM)이 NFVI 물리/가상 자원을 제어하여 VNF를 인스턴스화하고 SFC로 연계하는 ETSI 표준 아키텍처

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **NFVO (오케스트레이터)** | E2E 네트워크 서비스(NS) 템플릿(NSD) 해석 및 전역 자원 인가·조율 | MANO 계층 |
| **VNFM (VNF 매니저)** | 개별 VNF의 인스턴스화, 구성 갱신, 스케일아웃, 자가 치유(LCM) | MANO 계층 |
| **VIM (인프라 매니저)** | 물리 하드웨어(NFVI) 자원 가상화 풀 관리 및 VM/컨테이너 자원 할당 | OpenStack, K8s |
| **VNF / CNF** | 방화벽, vBRAS, vEPC, vUPF 등 소프트웨어로 구현된 네트워크 기능 | 가상화 기능 |
| **NFVI (인프라)** | COTS x86 서버 하드웨어, 고속 이더넷 패브릭 및 하이퍼바이저 계층 | 물리/가상 인프라 |

#### 한줄 요약
- NFVO, VNFM, VIM의 MANO 3요소와 VNF 기능, NFVI 인프라가 유기적으로 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **네트워크 서비스 기술자(Network Service Descriptor, NSD)**: 서비스 구성에 필요한 VNF 목록, VNF 간 가상 링크 연결 관계, SLA QoS 파라미터를 정의한 표준 배포 청사진 파일.

</details>

```text
1. 운용자(OSS/BSS)가 신규 서비스 청사진(NSD)을 작성하여 NFVO로 서비스 생성 요청
            │
            ▼
2. NFVO가 서비스 무결성 검증 후 VIM에 필요한 가상 컴퓨팅/네트워크 자원(VM/vCPU) 예약 요청
            │
            ▼
3. VIM이 NFVI 물리 COTS 서버에서 가상 자원을 프로비저닝하여 VNF 인프라 인계
            │
            ▼
4. VNFM이 VNF 소프트웨어 이미지를 다운로드하여 인스턴스 기동 및 초기 설정(VNFD 주입)
            │
            ▼
5. NFVO가 서비스 기능 체이닝(SFC) 경로를 설정하여 트래픽 인입 및 실시간 텔레메트리 감시
```

**동작 원리**

1. **서비스 요청**: OSS/BSS가 네트워크 서비스 디스크립터(NSD)를 통해 배포 명령 전달
2. **자원 조율**: NFVO가 가용 인프라 용량을 조회하고 VIM을 통해 VM/컨테이너 슬롯 확보
3. **인스턴스 기동**: VNFM이 사전 정의된 패키지(VNFD)를 바탕으로 VNF를 부팅하고 IP 부여
4. **체이닝 구성**: SDN 컨트롤러와 연계하여 VNF 간 트래픽 전달 경로(SFC)를 OpenFlow로 프로그래밍
5. **자동 확장**: VNFM이 CPU/트래픽 임계치 초과를 감지하면 자동으로 신규 VNF를 스케일아웃 복제

#### 한줄 요약
- NSD 요청, VIM 자원 할당, VNFM 인스턴스화, SFC 체이닝 구성, 오토스케일링 감시 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SDN vs NFV**: SDN은 네트워크 제어 평면을 중앙 집중화하여 트래픽 경로를 최적화하는 기술이며, NFV는 전용 네트워크 하드웨어 기능을 범용 서버 소프트웨어로 전환하는 가상화 기술.

</details>

| 비교 항목 | 네트워크 기능 가상화 (NFV) | 소프트웨어 정의 네트워킹 (SDN) | 전용 하드웨어 어플라이언스 |
|:---|:---|:---|:---|
| **핵심 목적** | **네트워크 L4~L7 기능의 소프트웨어화** | **L2~L3 패킷 제어 평면의 중앙 집중화** | 특정 고유 기능의 고속 처리 |
| **표준화 기구** | **ETSI (유럽 전기통신 표준협회)** | **ONF (Open Networking Foundation)** | 제조사 독점 규격 (시스코, 주니퍼 등) |
| **운영 인프라** | 범용 COTS x86/ARM 서버 (NFVI) | 화이트박스 스위치 및 중앙 컨트롤러 | 벤더 전용 ASIC 및 독점 섀시 |
| **상호 보완성** | SDN을 활용하여 VNF 간 체이닝(SFC) 제어 | VNF 형태로 SDN 컨트롤러 호스팅 가능 | 타 장비와의 결합 및 수정 제한 |
| **투자 비용 (CAPEX)**| **초기 도입 비용 대폭 절감 (COTS 활용)** | 화이트박스 스위치로 비용 절감 | 장비당 고가의 라이선스/하드웨어 비용 |

#### 한줄 요약
- NFV는 네트워크 기능 소프트웨어 가상화 기술이며, SDN은 트래픽 전달 경로 제어 기술이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **데이터 평면 개발 키트(DPDK)**: 리눅스 커널의 네트워크 스택을 우회(Kernel Bypass)하여 사용자 공간(User Space)에서 NIC 링 버퍼의 패킷을 직접 고속 처리하는 소프트웨어 가속 라이브러리.
- **단일 루트 입출력 가상화(SR-IOV)**: 단일 물리 PCIe 랜카드를 복수의 가상 인터페이스(VF)로 분할하여 하이퍼바이저 오버헤드 없이 VM에 네이티브 1:1 직결하는 기술.
- **CPU 피닝(CPU Pinning) 및 NUMA 노드 고정**: 가상 CPU를 특정 물리 코어와 NUMA 메모리 노드에 1:1 전용 매핑하여 코어 컨텍스트 스위칭 및 메모리 버스 지연을 방지하는 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 가상화 하이퍼바이저 및 OS 커널 오버헤드로 인한 VNF 패킷 처리 성능 저하 | **DPDK(커널 바이패스)** 및 **SR-IOV(PCIe 직결 가상화)** 기술 적용 | 커널 컨텍스트 스위칭 제거 및 라인 레이트 100Gbps 패킷 처리 |
| NUMA 노드 간 원격 메모리 접근으로 인한 처리 지연 및 지터(Jitter) 발생 | **CPU Pinning(코어 고정)** 및 **NUMA 노드 메모리 지역성(Locality) 바인딩** | 메모리 접근 지연 시간 단축 및 결정론적 저지연 보증 |
| 복수의 VNF 간 트래픽 연결 복잡도로 인한 가상 인터페이스 루프 발생 | **NSH(Network Service Header) 기반 SFC(서비스 기능 체이닝)** 표준화 | 논리적 패킷 서비스 경로 보존 및 체이닝 오라우팅 원천 방지 |

#### 한줄 요약
- DPDK/SR-IOV로 가상화 성능을 보완하고, NUMA/CPU Pinning으로 지연을 방지하며, NSH SFC로 체이닝을 정합화한다.

## Ⅶ. 결론

- 통신망의 민첩성과 CAPEX/OPEX 절감을 달성하기 위해 **ETSI 표준 NFV 아키텍처**와 **MANO 프레임워크**를 필수 도입하되, 소프트웨어 가상화에 따른 패킷 처리 성능 한계를 극복하기 위해 **DPDK, SR-IOV, NUMA CPU Pinning 가속 기술**과 **SDN 기반 SFC 체이닝**을 통합 구축하여 캐리어급(Carrier-Grade) 고성능 가상화 인프라를 완성

#### 한줄 요약
- MANO 프레임워크와 DPDK/SR-IOV 가속 기술을 결합하여 고성능 NFV 인프라를 구현한다.
