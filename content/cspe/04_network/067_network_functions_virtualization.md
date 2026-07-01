---
title: "NFV 네트워크 기능 가상화 (Network Functions Virtualization)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 67
---

# 📖 【암기용】 개념 완전 이해

> 목적: NFV를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 방화벽, 라우터, 로드밸런서 같은 네트워크 기능을 전용 장비 대신 범용 서버의 소프트웨어로 실행하는 구조
- **왜 필요한가**: 전용 장비는 도입·증설·교체 주기가 길어 서비스 출시와 용량 변경을 따라가기 어려움
- **핵심 직관**: 전용 가전제품을 하나씩 사는 대신, 범용 컴퓨터에 필요한 앱을 설치해 기능을 바꾸는 방식임

## 깊이 이해
- **배경·문제의식**: 통신망과 데이터센터는 방화벽, NAT, DPI, EPC/5GC 기능을 여러 전용 장비로 구성해왔다. NFV는 이러한 기능을 VNF 또는 CNF로 실행해 배포와 증설을 소프트웨어 운영으로 전환함.
- **작동 원리**: NFVI는 Compute/Storage/Network 자원을 제공하고, VNF/CNF는 네트워크 기능을 수행함. MANO가 VNF 배치, 스케일링, 장애 복구, 서비스 체이닝을 조정함.
- **비유**: 식당마다 전용 조리기구를 고정 배치하는 대신, 공용 주방에 필요한 장비와 레시피를 배치해 메뉴를 바꾸는 구조와 같음.
- **구체 예시**: 통신사가 vFirewall, vRouter, vEPC를 x86 서버 클러스터에 배치하고 트래픽 증가 시 VNF 인스턴스를 2대에서 6대로 확장함.
- **흔한 오해·주의점**: NFV는 SDN과 동일하지 않음. NFV는 네트워크 기능의 실행 위치와 형태를 가상화하고, SDN은 네트워크 제어 방식을 소프트웨어화함.

## 연결 개념
- VNF/CNF — VM 기반 또는 컨테이너 기반 네트워크 기능
- MANO — NFV Orchestrator, VNF Manager, VIM으로 구성되는 관리·오케스트레이션
- Service Function Chaining — 트래픽을 FW, IDS, LB 순서로 통과시키는 기능 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NFV는 전용 장비 대체가 아니라 NFVI, VNF/CNF, MANO, 서비스 체이닝을 갖춘 운영 구조임을 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NFV는 네트워크 기능을 전용 어플라이언스에서 분리해 범용 서버의 VNF/CNF로 실행하는 아키텍처이다.
> 2. **가치**: 서비스 출시, 용량 증설, 장애 복구를 소프트웨어 배포·스케일링·오케스트레이션 절차로 전환한다.
> 3. **판단 포인트**: 처리량, 지연, DPDK/SR-IOV, MANO 자동화, VNF 라이선스, 장애 격리를 함께 검토해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| NFV 구조 이해 확인 | NFVI, VNF/CNF, MANO, VIM | VM에 네트워크 SW 설치 정도로 축소 금지 |
| SDN과 구분 확인 | NFV는 기능 가상화, SDN은 제어 분리 | SDN과 NFV를 동일 기술로 서술 금지 |
| 운영 판단 확인 | 성능 가속, 오케스트레이션, 서비스 체이닝 | 전용 장비 대비 처리량 검증 누락 금지 |

> 요약: 이 문제는 네트워크 기능 가상화의 구조와 성능·운영 리스크를 함께 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

NFV는 네트워크 기능을 범용 서버의 소프트웨어 인스턴스로 구현하는 아키텍처이다. 전용 장비 중심 네트워크는 도입 리드타임과 용량 변경 비용이 크다. NFV는 방화벽, 라우터, NAT, EPC/5GC 기능을 VNF/CNF로 배포해 서비스 출시와 확장을 소프트웨어 운영으로 전환함.

---

## Ⅱ. 구조 및 구성요소

```text
OSS/BSS -> NFV MANO -> VIM/Kubernetes
-> NFVI Compute/Storage/Network -> VNF/CNF
Traffic -> Service Function Chain -> FW/NAT/LB/DPI -> Destination
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NFVI | 서버·스토리지·네트워크 자원 | x86, NIC, DPDK, SR-IOV |
| VNF | VM 기반 네트워크 기능 | vFW, vRouter, vEPC |
| CNF | 컨테이너 기반 네트워크 기능 | Kubernetes, CNI, Helm |
| MANO | 배치·스케일링·장애 복구 | NFVO, VNFM, VIM |
| SFC | 기능 순서 연결 | FW -> IDS -> LB |

> 요약: NFV는 NFVI 위에 VNF/CNF를 배치하고 MANO가 수명주기와 서비스 체인을 조정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 -> VNF/CNF Descriptor 선택 -> 자원 할당
-> 인스턴스 배포 -> 네트워크 연결/SFC 구성
-> 트래픽 처리 -> Telemetry 수집 -> Scale/Heal 수행
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스 카탈로그에서 기능 선택 | VNFD/CNF Chart, SLA |
| 2 | VIM/Kubernetes가 자원 할당 | CPU Pinning, NUMA, Hugepage |
| 3 | VNF/CNF 인스턴스 배포 | Image Signature, Config |
| 4 | SFC와 라우팅 정책 구성 | Service Chain Order, ACL |
| 5 | 부하·장애 기준으로 Scale/Heal | TPS, p95 지연, Health Check |

> 요약: NFV는 기능 서술자 기반 배포 후 트래픽 처리 상태를 관측해 확장과 복구를 수행한다.

---

## Ⅳ. 특징

| 구분 | 전용 네트워크 장비 | NFV | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 실행 형태 | Appliance ASIC/전용 HW | VNF/CNF on COTS | ETSI NFV, MANO |
| 배포 | 장비 구매·설치 | 이미지 배포·오케스트레이션 | VNFD, Helm, CI/CD |
| 성능 | ASIC 가속 | DPDK/SR-IOV 필요 | pps, Gbps, p95 지연 측정 |
| 운영 | 장비 단위 관리 | 인스턴스 단위 Scale/Heal | Auto-healing, Rolling Update |

> 요약: NFV는 배포와 확장 유연성을 제공하나, 패킷 처리 성능은 가속 기술과 자원 배치로 검증해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | NFV | 선택 기준 |
|:---|:---|:---|:---|
| 통신망 기능 | 전용 EPC/방화벽 | vEPC, vFW, vRouter | 출시 속도, 지역별 용량 변경 |
| 클라우드 네트워크 | 하드웨어 LB | VNF/CNF LB | 트래픽 변동, 자동 Scale 요구 |
| 운영 모델 | 장비 유지보수 | GitOps/CI/CD, MANO | 조직 자동화 역량, 관측성 |

> 요약: NFV는 네트워크 기능 변경이 잦고 지역별 용량 편차가 큰 환경에서 적용 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 처리량 부족 | 가상화 오버헤드 | DPDK, SR-IOV, CPU Pinning | pps, Gbps, CPU 사용률 |
| 장애 전파 | 다수 VNF가 동일 호스트 의존 | Anti-affinity, AZ 분산 | Host Failure Impact |
| 라이선스 복잡도 | VNF 벤더 과금 방식 | 인스턴스·처리량 단위 계약 검토 | License Utilization |

> 요약: NFV의 핵심 리스크는 성능, 장애 격리, 라이선스이며 배치 정책과 계약 조건으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | 목표 pps/Gbps 충족 | RFC 2544, TRex, IXIA |
| 지연 | p95 지연 SLA 이하 | 패킷 타임스탬프, APM |
| 복구 | Auto-healing RTO 5분 이하 | 장애 주입, MANO 이벤트 |

> 요약: NFV 검증은 처리량, 지연, 복구시간을 벤치마크와 장애 주입으로 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 고성능 VNF는 DPDK, SR-IOV, Hugepage, CPU Pinning을 적용하고 NUMA 경계를 고려해 배치함
2. MANO 또는 Kubernetes 기반으로 Scale-out, Auto-healing, Rolling Update 절차를 작성하고 장애 주입으로 RTO를 검증함
3. Service Function Chain은 FW -> IDS -> LB 순서를 정책으로 관리하고 Flow Counter와 p95 지연을 체인별로 수집함

**결론 (2줄):**
- 기술사 판단: 서비스 출시와 용량 변경이 잦으면 NFV, 초저지연·초고pps 요구가 절대 조건이면 전용 ASIC 장비를 검토함
- 향후 방향: NFV는 VNF에서 CNF로 이동하며 5G Core, MEC, Service Mesh와 결합한 클라우드 네이티브 네트워크로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NFV를 설명하시오" | VNFD 배포, SFC, Scale/Heal 흐름 | 전용 장비 대비 구조 차이 |
| 요구사항 명시형 | "NFV 도입 방안을 제시하시오" | DPDK/SR-IOV와 MANO 운영 | 성능·장애·라이선스 리스크 |

> 요약: 설명형은 ETSI NFV 구조, 방안형은 성능 검증과 자동화 운영 중심으로 전개한다.
