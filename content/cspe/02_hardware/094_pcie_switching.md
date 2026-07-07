---
title: "PCIe 스위칭 아키텍처 (PCIe Switching)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 94
---

# PCIe 스위칭 아키텍처 (PCIe Switching)

## 미리 알고가기

- PCIe(Peripheral Component Interconnect Express): point-to-point lane 기반 고속 직렬 I/O(Input/Output) 인터페이스임
- Root Complex: CPU(Central Processing Unit)/칩셋 쪽에서 PCIe 계층과 주소 공간을 시작하는 루트 장치임
- Endpoint: NVMe(Non-Volatile Memory Express) SSD(Solid-State Drive), NIC(Network Interface Card), GPU(Graphics Processing Unit)처럼 PCIe 버스에 연결되는 말단 장치임
- Switch: 하나의 upstream port와 여러 downstream port 사이 패킷을 라우팅하는 PCIe 장치임

## 1. 개요

- **정의/개념**: PCIe 스위칭 아키텍처는 Root Complex와 여러 Endpoint 사이에 PCIe switch를 배치해 lane, 주소 공간, 트래픽을 포트 단위로 분배하는 확장 구조임. 제한된 CPU PCIe 포트를 여러 고성능 장치에 연결하고 I/O 확장성과 구성 유연성을 확보하기 위해 사용함.
- **배경/필요성**: 서버는 GPU, NVMe, NIC, DPU(Data Processing Unit) 등 PCIe 장치 수가 늘어나지만 CPU가 제공하는 lane 수와 물리 슬롯은 제한적임. 스위치는 장치 fan-out과 peer-to-peer 전송을 제공하지만 oversubscription과 지연을 함께 관리해야 함.
- **비유**: 큰 도로 하나를 여러 진입로로 나누는 나들목처럼, 제한된 상위 연결을 여러 장치 경로로 배분하는 구조임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 고속 I/O 확장 구조 판단 | Root Complex, switch, endpoint, lane, oversubscription | 허브처럼 단순 공유 버스로 설명 |

> 요약: PCIe 스위치는 point-to-point 링크를 계층적으로 확장하지만 대역폭과 지연 설계가 핵심임.

## 2. 특징 및 비교

| 판단 기준 | 직접 연결 | PCIe 스위칭 |
|:---|:---|:---|
| 확장성 | CPU lane과 슬롯 수에 직접 제한됨 | downstream port로 장치 수를 확장함 |
| 지연 | 경로가 짧아 latency가 낮음 | 스위치 hop과 버퍼링 지연이 추가됨 |
| 대역폭 | 장치별 전용 lane 확보가 쉬움 | upstream 공유로 oversubscription 가능성이 있음 |
| 기능 | 단순 연결 중심 | hot-plug, bifurcation, P2P(Peer-to-Peer), 관리 기능을 제공함 |

> 요약: PCIe 스위칭은 장치 확장성과 연결 유연성을 얻는 대신 공유 상위 링크의 병목을 관리해야 함.

- **적용 조건**: 하위 장치 총 요구 대역폭과 upstream lane 용량의 비율이 허용 범위여야 함
- **선택 지표**: oversubscription ratio, switch hop latency, ACS(Access Control Services) 지원 여부를 함께 봐야 함

## 3. 구성요소/구조

```text
+--------------+      +--------------+      +-------------+
| Root Complex | ---> | PCIe Switch  | ---> | Endpoint A  |
+--------------+      +--------------+      +-------------+
                              |        ---> | Endpoint B  |
                              |        ---> | Endpoint C  |
                              v
                       +--------------+
                       | Mgmt/ACS     |
                       +--------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Root Complex | CPU 메모리 주소 공간과 PCIe hierarchy를 연결함 | 중앙 터미널 |
| Upstream Port | switch가 root complex 쪽으로 연결되는 포트임 | 상행 진입로 |
| Downstream Port | endpoint 장치로 나가는 포트와 lane 묶음임 | 하행 출구 |
| Routing·관리 기능 | TLP(Transaction Layer Packet) 라우팅, ACS, error reporting, hot-plug를 처리함 | 교통 관제 센터 |

> 요약: PCIe 스위치는 upstream 공유 링크와 downstream 장치 포트를 관리 기능으로 연결하는 계층 구조임.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Enumerate| ---> | Route    | ---> | Forward  | ---> | Manage   |
+----------+      +----------+      +----------+      +----------+
```

1. **열거·설정** — BIOS(Basic Input/Output System)/OS(Operating System)가 switch 하위 장치를 탐색하고 bus/device/function 번호와 BAR(Base Address Register)를 할당함
2. **주소 라우팅** — TLP 주소, ID, message 유형에 따라 upstream 또는 downstream 포트를 선택함
3. **패킷 전달** — lane 속도, flow control credit, ordering rule에 맞춰 패킷을 버퍼링·전달함
4. **오류·관리 처리** — AER(Advanced Error Reporting), hot-plug, ACS, 링크 상태를 감시하고 장애를 보고함

> 요약: PCIe 스위칭은 장치 열거 후 TLP 라우팅과 링크 관리로 다수 endpoint를 투명하게 연결함.

## 4. 문제점 및 개선방안

- **P1 upstream 병목**: 하위 장치 총 대역폭이 상위 링크보다 크면 NVMe나 GPU 작업에서 oversubscription이 발생함
- **P1 대응**: 장치별 요구 대역폭으로 oversubscription ratio를 설계하고 workload별 포트 배치를 조정함 (확인: upstream utilization)
- **P2 지연·순서 영향**: switch hop, 버퍼링, flow control이 latency 민감 I/O와 P2P 전송에 영향을 줌
- **P2 대응**: latency 민감 장치는 직접 연결하거나 switch hop 수와 P2P 경로를 제한함 (확인: p99 I/O latency)
- **P3 격리 취약성**: ACS/IOMMU(Input-Output Memory Management Unit) 설정이 부정확하면 endpoint 간 DMA(Direct Memory Access) 접근 격리가 약해질 수 있음
- **P3 대응**: ACS, ATS(Address Translation Services), IOMMU group, firmware 설정을 검증해 DMA 격리를 보장함 (확인: isolation test result)

> 요약: PCIe 스위치 도입은 포트 수 확장보다 대역폭 계획과 DMA 보안 검증이 우선임.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| GPU·NVMe 서버 설계 | 하위 장치 총 대역폭과 upstream 링크를 비교해 슬롯 배치와 oversubscription 허용치를 정함 | upstream utilization, oversubscription ratio |
| P2P 데이터 경로 최적화 | GPU Direct Storage, NVMe P2P 전송에서 switch hop 수와 ACS 설정이 지연에 미치는 영향을 측정함 | p99 I/O latency, P2P throughput |
| DMA 격리 검증 | IOMMU group, ACS, firmware 설정을 점검해 테넌트·장치 간 무단 DMA 접근을 차단함 | isolation test result, unauthorized DMA 차단 |

> 요약: 실무에서는 PCIe 스위치를 포트 확장 장치가 아니라 대역폭, 지연, DMA 격리를 함께 설계해야 하는 공유 패브릭으로 다뤄야 함.

## 6. 결론

- **발전 방향**: PCIe 고속 세대와 CXL(Compute Express Link) switch, composable infrastructure가 결합되며 메모리와 가속기 자원의 동적 연결이 확대됨
- **기술사적 판단**: 스위치 선택은 lane 수, 세대, latency, ACS/CXL 기능, 관리성, 장애 격리를 기준으로 해야 함
- **기술사 제언**: 서버 설계 시 slot diagram뿐 아니라 실제 워크로드별 트래픽 행렬과 격리 정책을 함께 검증해야 함
