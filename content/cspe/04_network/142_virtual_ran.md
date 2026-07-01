---
title: "가상 기지국 vRAN (Virtual RAN)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 142
---

# 📖 【암기용】 개념 완전 이해

> 목적: vRAN을 장비 교체 용어가 아니라 RAN 기능을 서버와 소프트웨어로 옮기는 구조로 이해하게 만든다.

## 한눈에
- **개요**: 기지국의 CU·DU 기능을 전용 장비 대신 COTS 서버와 가상화 환경에서 실행하는 RAN 구조
- **왜 필요한가**: 5G는 트래픽 패턴이 지역·시간별로 달라 전용 장비만으로는 용량 재배치와 자동화 운영이 어렵다.
- **핵심 직관**: 기지국 처리 기능을 전용 가전제품에서 범용 서버 위 애플리케이션으로 옮기는 방식이다.

## 깊이 이해
- **배경·문제의식**: 기존 RAN 장비는 하드웨어와 소프트웨어가 묶여 있어 용량 증설, 패치, 벤더 변경이 장비 단위로 진행된다.
- **작동 원리**: CU와 DU 소프트웨어가 COTS 서버, 가상화 계층, 가속 카드에서 동작하고 RU는 무선 송수신을 담당한다.
- **비유**: 회사 전화교환기를 전용 장비에서 데이터센터 서버의 소프트웨어 교환기로 옮기는 것과 같다.
- **구체 예시**: DU는 L1/L2 실시간 처리가 필요해 DPDK, SR-IOV, FPGA 또는 SmartNIC 가속을 사용하고, CU는 클라우드 네이티브 배치가 가능하다.
- **흔한 오해·주의점**: vRAN은 모든 RAN 기능을 일반 VM에 올리는 뜻이 아니라 실시간 L1 처리와 프런트홀 제약을 만족하는 서버 설계가 필요하다.

## 연결 개념
- CU·DU·RU 기능 분리 - vRAN의 구조적 전제
- COTS 서버 - 전용 장비 대신 사용하는 범용 하드웨어
- O-RAN - vRAN과 개방형 인터페이스를 결합하는 생태계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: vRAN 답안은 가상화 장점보다 실시간 처리, 가속, 운영 지표를 중심으로 작성한다.
> 핵심: 출제자는 vRAN이 기존 RAN을 어떻게 소프트웨어화하고 어떤 성능·운영 제약을 갖는지 확인한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vRAN은 CU·DU 기능을 전용 BBU가 아니라 COTS 서버와 가상화 계층에서 실행하는 무선 접속망 구조이다.
> 2. **가치**: 서버 자원 풀, 자동 배포, 소프트웨어 패치, 다중 벤더 조합을 통해 RAN 운영 단위를 장비에서 워크로드로 바꾼다.
> 3. **판단 포인트**: L1 지연, CPU 코어 고정, DPDK/SR-IOV, 프런트홀 대역폭, 가속 카드 지원 여부가 도입 판단 축이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| RAN 가상화 구조 이해 확인 | COTS, hypervisor/container, CU/DU SW, accelerator | vRAN을 단순 클라우드 이전으로 설명 |
| 실시간 처리 제약 판단 확인 | L1 처리, DPDK, SR-IOV, CPU pinning, NUMA | 일반 IT 워크로드와 동일한 운영으로 단정 |
| 운영 자동화 역량 확인 | CI/CD, 관측성, 장애 롤백, PM counter | 벤더 비용 절감만 강조하고 KPI 누락 |

> 요약: vRAN 문제는 가상화 개념보다 무선 실시간 처리와 클라우드 운영 제약을 함께 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: RAN 기능을 COTS 서버에서 실행
- 배경: 전용 BBU 장비 중심 RAN은 용량 증설과 소프트웨어 패치가 장비 공급 주기에 종속됨.
- 필요성: 5G 트래픽 편차, MEC 연동, 자동화 운영 요구로 CU·DU 소프트웨어 배치 단위 전환이 필요함.
- 판단 기준: L1 지연, CPU 사용률, 가속 카드, 프런트홀 대역폭, 무선 KPI를 기준으로 적용 범위를 결정함.

---

## Ⅱ. 구조 및 구성요소

```text
RU -> Fronthaul -> vDU on COTS -> Midhaul -> vCU on COTS -> 5G Core
                     |                         |
                     +-> DPDK / SR-IOV         +-> Kubernetes / VM
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| vDU | MAC, RLC, High-PHY 일부 처리 | CPU pinning, NUMA, 가속 카드 필요 |
| vCU | PDCP, SDAP, RRC 처리 | 중앙 데이터센터 또는 엣지 클라우드 배치 |
| COTS Server | 범용 CPU, NIC, 가속 자원 제공 | Intel AVX, FPGA, SmartNIC 구성 검토 |
| Virtualization Layer | VM, Container, Kubernetes 실행 | 실시간 커널과 네트워크 패스 최적화 필요 |

> 요약: vRAN은 RU를 현장에 두고 vDU와 vCU를 서버 자원 위에 배치해 RAN 기능을 소프트웨어 워크로드로 운영한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
RU 무선 수신 -> eCPRI 프런트홀 -> vDU 실시간 처리
-> vCU 제어 / 사용자면 처리 -> 5G Core 연동 -> KPI 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | RU가 RF와 Low-PHY 처리를 수행 | RSRP, SINR, RU alarm |
| 2 | vDU가 MAC 스케줄링과 HARQ를 처리 | PRB 사용률, BLER, HARQ retransmission |
| 3 | vCU가 RRC와 PDCP를 처리 | RRC setup success, PDCP throughput |
| 4 | 가상화 계층이 CPU와 NIC 자원을 할당 | CPU steal, NUMA locality, packet drop |
| 5 | 운영 시스템이 배포와 장애 지표를 수집 | rollout time, rollback success, KPI regression |

> 요약: vRAN은 무선 패킷을 서버 소프트웨어가 처리하므로 네트워크 패스와 CPU 배치를 무선 KPI와 함께 검증한다.

---

## Ⅳ. 특징

| 구분 | 전용 BBU RAN | vRAN | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 하드웨어 | 전용 장비 | COTS 서버, NIC, 가속 카드 | DPDK, SR-IOV, SmartNIC |
| 배포 | 장비 펌웨어 중심 | VM/Container 이미지 중심 | CI/CD, Blue-Green, rollback |
| 처리 제약 | 벤더 최적화 하드웨어 | 범용 CPU와 L1 가속 조합 | CPU pinning, NUMA, real-time kernel |
| 운영 지표 | 장비 알람 중심 | IT 지표와 RAN PM counter 결합 | CPU, packet drop, BLER, RRC success |

> 요약: vRAN은 RAN 운영을 소프트웨어 배포 모델로 전환하지만 DU 실시간 처리는 서버·NIC·가속 카드 설계가 좌우한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 전용 BBU | vDU/vCU on COTS | 자동화 배포와 자원 풀링 요구 시 선택 |
| 비용/성능 | 장비 단위 증설 | 서버·가속 자원 단위 증설 | DU CPU 부하와 무선 KPI 동시 충족 시 적용 |
| 운영/위험 | 벤더 OAM 중심 | 클라우드 OAM과 RAN OAM 결합 | 장애 분석 조직과 관측성 체계 필요 |

> 요약: vRAN 선택은 조달 방식보다 실시간 처리 보장과 클라우드 운영 역량 확보 여부로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| L1 처리 지연 | 범용 CPU 스케줄링 지연 | CPU pinning, real-time kernel, 가속 카드 적용 | scheduling latency, BLER |
| 패킷 손실 | NIC 큐와 가상 스위치 병목 | DPDK, SR-IOV, hugepage 적용 | packet drop, queue depth |
| 배포 장애 | RAN SW 이미지 변경 영향 | Canary, rollback, KPI gate | RRC success regression |

> 요약: vRAN 리스크는 실시간 처리, 패킷 경로, 배포 변경 영향으로 나누어 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 무선 품질 | RRC 성공률, 핸드오버 성공률 기준 충족 | RAN PM counter |
| 서버 자원 | CPU, NUMA, NIC 큐 임계치 관리 | Prometheus, node exporter, NIC telemetry |
| 배포 품질 | 배포 후 KPI 회귀 없음 | CI/CD gate, synthetic call |

> 요약: vRAN 성공 여부는 IT 자원 지표와 RAN 무선 지표를 같은 배포 단위에서 연결해 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. vDU 서버는 CPU pinning, NUMA affinity, DPDK, SR-IOV, 가속 카드 기준으로 실시간 처리 경로를 설계함.
2. vCU와 vDU 배포는 Kubernetes 또는 VM 이미지 기준으로 표준화하고 RAN KPI gate를 CI/CD에 연결함.
3. 운영 관측성은 CPU, NIC, packet drop, BLER, RRC success를 같은 대시보드에서 상관 분석함.

**결론 (2줄):**
- 기술사 판단: 고밀도 5G와 자동화 운영 요구가 있으면 vRAN을 검토하고, 지연 민감 DU는 가속·전송망 검증 후 단계 도입함.
- 향후 방향: vRAN은 O-RAN, RIC, MEC와 결합되어 소프트웨어 기반 RAN 최적화 구조로 확장됨.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "vRAN을 설명하시오" | RU-vDU-vCU-Core 처리 흐름 | COTS, 가상화, 가속 구조 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "비교하시오" | 실시간 처리와 배포 검증 흐름 | 전용 RAN 대비 선택 기준과 리스크 |

> 요약: 설명형은 구조와 원리를 쓰고, 구축형은 CPU/NIC/가속·KPI 검증 기준으로 답안을 전환한다.
