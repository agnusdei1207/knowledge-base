---
title: "SDN 소프트웨어 정의 네트워킹 (Software Defined Networking)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 66
---

# 📖 【암기용】 개념 완전 이해

> 목적: SDN을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 네트워크 제어 평면을 장비에서 분리해 중앙 컨트롤러가 정책과 경로를 제어하는 구조
- **왜 필요한가**: 장비별 CLI 설정은 변경 시간이 길고 오류가 많아 클라우드·가상화 환경의 빠른 네트워크 변경을 따라가기 어려움
- **핵심 직관**: 각 교차로가 스스로 신호를 정하지 않고, 교통관제센터가 전체 교통 흐름을 보고 신호 정책을 내려주는 방식임

## 깊이 이해
- **배경·문제의식**: 기존 네트워크는 장비마다 Control Plane과 Data Plane이 결합되어 있음. VLAN, ACL, 라우팅 정책을 장비별로 설정하면 변경 일관성과 자동화가 어려움.
- **작동 원리**: SDN Controller가 전체 토폴로지와 정책을 계산하고, 스위치·라우터의 Forwarding Plane에 Flow Rule을 설치함. Northbound API는 애플리케이션과 연동하고, Southbound API는 OpenFlow, NETCONF, gNMI 등으로 장비를 제어함.
- **비유**: 물류 창고의 모든 컨베이어 벨트 방향을 작업자가 각자 정하는 대신, 중앙 WMS가 주문 흐름을 보고 경로를 배치하는 구조와 같음.
- **구체 예시**: 데이터센터에서 신규 테넌트가 생성되면 Controller가 VNI, ACL, QoS 정책을 계산하고 ToR 스위치에 VXLAN 터널과 Flow Rule을 자동 반영함.
- **흔한 오해·주의점**: SDN은 OpenFlow 하나만 의미하지 않음. 핵심은 제어·전달 분리와 API 기반 자동화이며, 구현은 OpenFlow, EVPN, NETCONF 기반 등으로 다양함.

## 연결 개념
- OpenFlow — SDN Southbound 프로토콜의 대표 사례
- NFV — 네트워크 기능을 소프트웨어 VNF/CNF로 실행하는 구조
- Network Automation — API·IaC 기반 네트워크 변경 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SDN은 장비 교체 기술이 아니라 Control/Data Plane 분리와 API 기반 정책 자동화 구조임을 명확히 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SDN은 Control Plane을 중앙 Controller로 분리하고 Data Plane 장비에 정책·Flow를 프로그램하는 네트워크 아키텍처이다.
> 2. **가치**: API 기반 자동화로 VLAN·ACL·QoS·경로 정책을 서비스 요구와 연동해 분 단위로 배포한다.
> 3. **판단 포인트**: Controller 가용성, Southbound 프로토콜, 정책 충돌, 벤더 종속, 관측성 지표를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SDN 구조 이해 확인 | Control/Data Plane 분리, Controller, API | OpenFlow만 SDN으로 단정 금지 |
| 자동화 가치 판단 확인 | Northbound/Southbound API, 정책 기반 제어 | 장비 CLI 자동화와 동일시 금지 |
| 운영 리스크 인식 확인 | Controller 장애, 정책 충돌, 보안 경계 | 중앙 제어의 장애 영향 누락 금지 |

> 요약: 이 문제는 SDN을 제어 구조, API, 운영 리스크까지 연결해 설명하는지를 평가한다.

---

## Ⅰ. 개요 및 필요성

SDN은 네트워크 제어 기능을 장비에서 분리해 소프트웨어 Controller가 중앙 제어하는 아키텍처이다. 클라우드·가상화 환경은 테넌트, 보안정책, 경로가 수시로 바뀌므로 장비별 수동 설정으로는 변경 일관성 확보가 어렵다. SDN은 정책 기반 자동화와 전체 토폴로지 관점의 제어를 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Application/Policy -> Northbound API -> SDN Controller
-> Southbound API -> Switch/Router Data Plane -> Packet Forwarding
Telemetry/Events -> Controller State -> Policy Recalculation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Application Plane | 보안, QoS, 경로 정책 요구 | Intent, Service Chain |
| SDN Controller | 토폴로지·정책 계산 | HA Cluster, State Store |
| Northbound API | 외부 시스템 연동 | REST, gRPC, Intent API |
| Southbound API | 장비 제어 | OpenFlow, NETCONF, gNMI, P4Runtime |
| Data Plane | 패킷 전달 | Flow Table, TCAM, ASIC |

> 요약: SDN은 애플리케이션 정책을 Controller가 해석해 Data Plane 장비의 전달 규칙으로 변환하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요구 -> 정책 변환 -> 토폴로지/상태 조회
-> 경로·ACL·QoS 계산 -> Flow/Config 배포
-> 패킷 전달 -> Telemetry 수집 -> 정책 재계산
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스·보안 정책 입력 | Intent, ACL, QoS Profile |
| 2 | Controller가 토폴로지와 장비 상태 조회 | LLDP, BGP-LS, Telemetry |
| 3 | 경로와 Flow Rule 계산 | Loop Free, Policy Conflict Check |
| 4 | Southbound API로 장비에 규칙 배포 | Config Commit, Flow Install Success |
| 5 | 트래픽과 장애 이벤트를 수집해 재계산 | p95 지연, Drop Count, Link Event |

> 요약: SDN은 정책 입력부터 장비 규칙 배포와 Telemetry 기반 재계산까지 폐루프 제어를 수행한다.

---

## Ⅳ. 특징

| 구분 | 기존 네트워크 | SDN | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 제어 구조 | 장비별 Control Plane | 중앙 Controller | Control/Data Plane 분리 |
| 변경 방식 | CLI 수동 설정 | API·정책 자동 배포 | REST, gRPC, NETCONF |
| 경로 판단 | 분산 라우팅 수렴 | 전체 토폴로지 기반 계산 | BGP-LS, Telemetry |
| 운영 위험 | 장비별 오류 | Controller 장애·정책 오류 | Controller HA, Rollback |

> 요약: SDN은 중앙 정책 제어와 자동화를 제공하지만 Controller와 정책 저장소를 핵심 장애 도메인으로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | SDN | 선택 기준 |
|:---|:---|:---|:---|
| 데이터센터 | VLAN/STP 수동 운영 | Controller 기반 Overlay/Policy | 테넌트 수, 변경 빈도, 자동화 요구 |
| WAN | 정적 경로·MPLS 중심 | SD-WAN/Policy Routing | 애플리케이션별 경로·SLA 필요 |
| 보안 | 장비별 ACL | 중앙 정책·마이크로세그먼트 | 동서 트래픽 통제, 감사로그 |

> 요약: SDN은 변경 빈도와 정책 복잡도가 높은 데이터센터·WAN·보안 세그먼트에 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Controller 장애 | 중앙 제어 의존 | 3노드 HA, State Replication, Failover Test | Controller Quorum, RTO |
| 정책 충돌 | 다중 앱 정책 중복 | Policy Validation, Dry-run, Rollback | Conflict Count, Failed Commit |
| 장비 호환 | Southbound 구현 차이 | 표준 API 매트릭스, 벤더 검증 | Flow Install Failure |

> 요약: SDN 리스크는 중앙 제어, 정책 충돌, 장비 호환이며 HA와 사전 검증 파이프라인으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 배포 | 정책 배포 5분 이하 | CI/CD 로그, Controller Audit |
| 가용성 | Controller 99.9% 이상 | Health Check, Failover Drill |
| 전달 품질 | p95 지연·Drop Count 기준 충족 | Telemetry, Flow Counter |

> 요약: SDN 운영은 배포시간, Controller 가용성, 전달 품질 Counter를 지속 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 데이터센터는 SDN Controller 3노드 HA와 역할 기반 접근제어를 구성하고 정책 변경을 Git 기반 승인 절차와 연결함
2. Southbound는 장비별 OpenFlow/NETCONF/gNMI 지원 범위를 매트릭스로 검증하고 Rollback 가능한 Commit 방식을 적용함
3. Telemetry는 Flow Counter, Link Event, p95 지연, Drop Count를 수집해 정책 오류를 5분 이내 탐지하도록 구성함

**결론 (2줄):**
- 기술사 판단: 변경 빈도와 정책 복잡도가 높으면 SDN, 단순 고정망이면 표준 라우팅과 자동화 도구 조합을 우선 검토함
- 향후 방향: SDN은 Intent 기반 네트워킹, P4 Programmable Data Plane, AIOps 관측성과 결합해 폐루프 운영으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SDN을 설명하시오" | 정책 입력부터 Flow 배포까지 원리 | 기존 네트워크 대비 Control/Data 분리 |
| 요구사항 명시형 | "SDN 도입 방안을 제시하시오" | HA, 정책 검증, Telemetry 흐름 | 리스크·지표·운영 자동화 |

> 요약: 설명형은 구조와 원리, 방안형은 Controller 운영과 정책 검증 중심으로 목차를 전환한다.
