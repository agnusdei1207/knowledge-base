---
sidebar:
  order: 57
  label: "057. 네트워크 기능 가상화: NFV"
  badge:
    text: "기출 · 30%"
    variant: note
title: "네트워크 기능 가상화 : NFV (Network Functions Virtualization)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-network"
weight: 57
extra:
  question_no: "57"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 50
  priority_note: "ETSI NFV 표준 아키텍처, MANO 프레임워크(NFVO/VNFM/VIM), VNF/CNF 및 하드웨어 가속(DPDK/SR-IOV)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NFV (Network Functions Virtualization)**: 전용 하드웨어 장비의 네트워크 기능을 범용 COTS 서버의 VM/컨테이너 SW로 구현하는 ETSI 표준.
- **MANO (Management and Orchestration)**: NFVO, VNFM, VIM으로 구성되어 가상 네트워크 인프라와 VNF의 수명주기를 총괄 오케스트레이션하는 프레임워크.

</details>

- 정의/개념: 전용 하드웨어 장비와 기능을 분리하고 범용 COTS 서버 위에서 **MANO**를 통해 VNF/CNF의 수명주기를 자동화 관리하는 ETSI 표준 가상화 기술
- 배경/필요성: 전통적인 통신 및 엔터프라이즈 네트워크는 방화벽(FW), 라우터, 로드밸런서(LB), 5G 코어(UPF/AMF) 등의 네트워크 기능을 고가의 독점 하드웨어 어플라이언스에 의존하여 구축함에 따라, 막대한 초기 투자 비용(CAPEX)과 상면/전력 유지비(OPEX)가 발생하고, 신규 서비스 도입 시 장비 발주부터 현장 설치까지 수개월 이상이 소요되며 트래픽 급증 시 탄력적인 스케일아웃이 불가능한 한계를 극복하기 위해, 전용 하드웨어와 기능을 완전히 분리하여 범용 상용 서버(COTS x86/ARM)의 가상 머신(VNF) 또는 컨테이너(CNF) 소프트웨어로 인스턴스화하고 ETSI MANO(NFVO/VNFM/VIM) 프레임워크로 오케스트레이션하는 **NFV**(Network Functions Virtualization)를 도입하여 배포 시간 수분 내 단축, 유연한 서비스 기능 체이닝(SFC) 및 자원 탄력성(Elasticity)을 달성할 필요

#### 한줄 요약
- NFV는 전용 장비의 성능 최적화를 포기하고 범용 서버의 유연성을 택한 것이므로, 그로 인한 패킷 처리 성능 손실을 하드웨어 가속으로 되사는 비용이 뒤따른다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **COTS (Commercial Off-The-Shelf)**: 상용 표준 x86/ARM 서버, 표준 스토리지, 고속 이더넷 NIC 등 범용 상용 하드웨어.
- **SFC (Service Function Chaining)**: 방화벽 $\to$ 로드밸런서 $\to$ NAT $\to$ 웹 서버 순으로 트래픽을 가상 VNF 체인 경로를 따라 조향하는 기술.

</details>

- 하드웨어와 소프트웨어의 완전 분리: 고가의 독점 ASIC 어플라이언스를 표준 범용 **COTS** x86/ARM 서버로 대체
- MANO 기반 생애주기 자동화(LCM): VNF 인스턴스의 생성, 스케일아웃, 마이그레이션, 자동 복구(Self-Healing) 지원
- 서비스 기능 체이닝(**SFC**) 유연성: NSH(Network Service Header) 기반으로 복수의 VNF를 통과하는 가상 서비스 경로 자유 구성

#### 한줄 요약
- COTS 서버 기반 HW/SW 분리, MANO 생명주기 자동화, SFC 서비스 체이닝 유연성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NFVO vs VNFM vs VIM**: E2E 서비스 토폴로지를 조율하는 NFVO, 개별 VNF의 수명주기를 제어하는 VNFM, 가상화 인프라 자원을 할당하는 VIM.

</details>

```text
[NFV 구성]
|-- NFVO
|-- VNFM
|-- VIM
|-- VNF / CNF
`-- NFVI
```

선의 의미: MANO 계층(NFVO/VNFM/VIM)이 NFVI 물리/가상 자원을 제어하여 VNF를 인스턴스화하고 SFC로 연계하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **NFVO (오케스트레이터)** | E2E 네트워크 서비스(NS) 템플릿(NSD) 해석 및 **전역 가상 자원 인가·조율** | MANO 계층 |
| **VNFM (VNF 매니저)** | 개별 VNF의 인스턴스화, 구성 갱신, 스케일아웃, 자가 치유(LCM) | VNF 수명주기 관리 |
| **VIM (인프라 매니저)** | 물리 하드웨어(NFVI) 자원 가상화 풀 관리 및 **VM/컨테이너 자원 할당** | OpenStack, K8s |
| **VNF / CNF** | 방화벽, vEPC, vUPF, vBRAS 등 소프트웨어로 구현된 네트워크 기능 | 가상 네트워크 기능 |
| **NFVI (인프라)** | COTS x86 서버 하드웨어, 고속 이더넷 패브릭 및 가상화 계층 | 물리/가상 인프라 |

#### 한줄 요약
- VNF가 전용 하드웨어 장비의 자리를 소프트웨어로 채우고, MANO 3요소가 장비를 새로 들여놓던 절차를 자원 예약과 인스턴스화로 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NSD (Network Service Descriptor)**: 서비스 구성에 필요한 VNF 목록, VNF 간 연결 토폴로지, SLA 조건을 정의한 표준 배포 템플릿.

</details>

```text
NFV 서비스 배포 및 수명주기 관리 파이프라인
        │
   1. [서비스 요청 인입] 운용자(OSS/BSS)가 서비스 청사진(NSD)을 NFVO로 전달
        │
   2. [가상 자원 예약] NFVO가 무결성 검증 후 VIM에 필요한 vCPU/RAM/vNIC 예약 요청
        │
   3. [NFVI 인프라 프로비저닝] VIM이 물리 COTS 서버에서 가상 머신/컨테이너 슬롯 할당
        │
   4. [VNF 인스턴스화] VNFM이 VNF 이미지를 로드하여 부팅 및 초기 설정(VNFD 주입)
        │
   ▼
5. [SFC 체이닝 및 감시] NFVO가 VNF 간 서비스 체이닝 경로를 확정하고 텔레메트리 감시 개시
```

#### 한줄 요약
- 장비 반입 대신 자원 예약으로 기능을 세우므로 증설이 배포 시간 문제로 바뀌지만, 그 대가로 성능은 범용 서버와 가상화 계층의 처리 한계에 묶인다.

## Ⅴ. 종류 및 비교


| 비교 항목 | 네트워크 기능 가상화 (NFV) | 소프트웨어 정의 네트워킹 (SDN) | 전용 하드웨어 어플라이언스 |
|:---|:---|:---|:---|
| 핵심 목적 | 네트워크 L4~L7 기능의 소프트웨어화 | L2~L3 패킷 제어 평면의 중앙 집중화 | 특정 고유 기능의 고속 처리 |
| 표준화 기구 | ETSI (유럽 전기통신 표준협회) | ONF (Open Networking Foundation) | 제조사 독점 규격 (시스코, 주니퍼) |
| 운영 인프라 | 범용 COTS x86/ARM 서버 (NFVI) | 화이트박스 스위치 및 중앙 컨트롤러 | 벤더 전용 ASIC 및 독점 섀시 |
| 상호 보완성 | SDN을 활용하여 VNF 간 체이닝(SFC) 제어 | VNF 형태로 SDN 컨트롤러 호스팅 가능 | 타 장비와의 결합 및 수정 제한 |
| 투자 비용 (CAPEX) | 초기 도입 비용 대폭 절감 (COTS 활용) | 화이트박스 스위치로 비용 절감 | 장비당 고가의 하드웨어 비용 |

#### 한줄 요약
- NFV는 네트워크 기능 소프트웨어 가상화 기술이며, SDN은 트래픽 전달 경로 제어 기술이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DPDK (Data Plane Development Kit)**: 리눅스 커널을 우회(Kernel Bypass)하여 유저 공간에서 NIC 버퍼 패킷을 직접 고속 처리하는 가속 라이브러리.
- **SR-IOV (Single Root I/O Virtualization)**: 단일 물리 PCIe NIC을 복수의 가상 인터페이스(VF)로 분할하여 VM에 하이퍼바이저 없이 1:1 직결하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 가상화 하이퍼바이저 및 커널 오버헤드로 인한 VNF 패킷 처리 저하 | **DPDK** (커널 바이패스) 및 **SR-IOV** (PCIe 직결 가상화) 적용 | 컨텍스트 스위칭 제거 및 라인 레이트 100Gbps 처리 |
| NUMA 노드 간 원격 메모리 접근으로 인한 처리 지연 및 지터 발생 | CPU Pinning (코어 고정) 및 NUMA 노드 메모리 지역성 바인딩 | 메모리 버스 지연 단축 및 결정론적 저지연 보증 |
| 복수 VNF 간 트래픽 연결 복잡도로 인한 가상 인터페이스 루프 | NSH (Network Service Header) 기반 SFC 표준화 | 논리적 패킷 서비스 경로 보존 및 오라우팅 방지 |
| 컨테이너 기반 CNF 전환 시 공유 커널 보안 격리 취약 | gVisor / Kata Containers (경량 샌드박스) 격리 런타임 적용 | 컨테이너 침해 시 호스트 커널 오염 원천 차단 |

#### 한줄 요약
- DPDK/SR-IOV로 가상화 성능을 극대화하고, NUMA/CPU Pinning으로 지연을 방지하며, NSH SFC로 체이닝을 정합화한다.

## Ⅶ. 결론

- 5G 코어망(SBA), vRAN/Open RAN 및 클라우드 네이티브 네트워크 인프라의 근간을 이루며 통신 사업자(Telco) 및 대규모 엔터프라이즈의 네트워크 민첩성과 비용 효율성을 혁신한 핵심 가상화 표준으로 정립되었으며, 가상 머신 기반 VNF에서 쿠버네티스 마이크로서비스 기반 CNF(Cloud-native Network Function)로 진화하는 가운데, 실무 구축 시에는 가상화 오버헤드를 극복하는 DPDK 커널 바이패스 및 SR-IOV 하드웨어 가속, NUMA 노드 및 CPU Pinning을 통한 결정론적 저지연 보장, 복잡한 서비스 경로를 일관되게 제어하는 NSH 기반 서비스 기능 체이닝(SFC)을 결합하여 통신사급 캐리어 그레이드 고성능과 고가용성을 완성

#### 한줄 요약
- NFV는 네트워크 기능을 범용 COTS 서버 위 소프트웨어로 전환하여 MANO로 자동화 제어하는 핵심 통신 가상화 패러다임이다.
