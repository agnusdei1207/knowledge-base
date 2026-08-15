---
sidebar:
  order: 48
  label: "048. 컴퓨팅 연속체 (Computing Continuum / Cloud-Edge Continuum)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "컴퓨팅 연속체 (Computing Continuum / Cloud-Edge Continuum)"
date: "2026-08-13T17:14:00+09:00"
tags:
  - "notes-network"
weight: 48
extra:
  question_no: "048"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "설명형: 126회 Cloud-Edge-IoT 단답"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **컴퓨팅 연속체(Computing Continuum / Cloud-Edge-IoT Continuum)**: IoT 단말, 최말단 에지(Far Edge), 근접 에지(Near Edge) 및 중앙 클라우드의 파편화된 자원을 단일 가상화 환경으로 통합하여 워크로드를 동적 배치하는 분산 패러다임이다.
- **서비스 수준 목표(Service Level Objective, SLO)**: 시스템이 준수해야 할 전송 지연시간, 처리량, 자원 비용 및 가용성에 관한 정량적 성과 목표이다.

</details>

- 정의/개념: **컴퓨팅 연속체(Computing Continuum)**는 단말, 최말단 에지, 근접 에지 및 중앙 클라우드 인프라에 흩어진 컴퓨팅/전송 자원을 단일 제어 평면으로 통합 추상화하고, 서비스 요구 성능(SLO)과 네트워크 상태에 따라 컨테이너 워크로드를 가장 적합한 위치로 동적 자동 재배치하는 클라우드-에지 융합 아키텍처이다.
- 배경/필요성: 기존 클라우드와 에지 인프라의 상호 고립(Siloed)으로 인한 자원 낭비, 단말 이동 시의 서비스 마비, 그리고 데이터 수송 대역폭 오버헤드 문제를 단일 관제 체계로 극복하기 위해 제정되었다.

#### 한줄 요약

- IoT 단말부터 에지, 코어, 클라우드 전 구역의 연산 인프라를 하나로 융합하고 요구 SLO에 따라 워크로드를 동적 최적 배치하는 아키텍처.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **워크로드 이식성(Workload Portability)**: 애플리케이션 컨테이너 및 상태 데이터가 물리적 노드 위치나 이종 인프라 하드웨어 환경에 영향받지 않고 자유롭게 마이그레이션되는 성질이다.
- **데이터 중력(Data Gravity)**: 데이터의 규모와 입출력 의존성이 커짐에 따라 연산 애플리케이션이 데이터가 위치한 물리적 장소 인근으로 이끌려 배치되는 현상이다.

</details>

- **E2E 자원 통합 관측 및 추상화**: K8s Federation 및 OpenStack 기술을 적용하여 최말단 단말 자원부터 대규모 IDC 클라우드까지 단일 관리 뷰(Single-pane-of-glass)로 추상화한다.
- **데이터 중력(Data Gravity) 반영 오케스트레이션**: 무작정 에지나 클라우드로 워크로드를 보내지 않고, 데이터 대용량 수송 비용과 SLO 지연 단축 이득을 비교 평가하여 최적화된 위치에 배치한다.
- **자원 유연성과 재배치**: 과부하 시 상태와 컨테이너를 다른 노드로 이관한다.

#### 한줄 요약

- 단일 관제면을 통한 자원 추상화, 컨테이너 기반 워크로드 이식성, 데이터 중력(Data Gravity) 기반 동적 최적 배치 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **통합 제어면(Unified Control Plane)**: 전체 계층 노드의 연산 가용량, 네트워크 지연 및 에너지 상태(Telemetry)를 수집하여 워크로드 배치를 결정하는 오케스트레이터이다.
- **최말단·근접 에지(Far-Edge & Near-Edge)**: 산업 현장 직결 제어를 수행하는 최말단(Far-Edge) 노드와 국사 및 지역 서버 단위에서 집계를 담당하는 근접(Near-Edge) 노드의 구성이다.

</details>

```text
컴퓨팅 연속체 (Cloud-Edge-IoT Continuum) 구조
├─ 통합 오케스트레이션 계층 (Unified Control Plane - MEAO/K8s Federation)
├─ 심층 분산 실행 계층 (Heterogeneous Multi-Tier Computing)
│  ├─ 중앙 클라우드 (Central Cloud - Big Data / Model Training)
│  ├─ 근접 에지 (Near Edge - Regional Node / Local UPF)
│  └─ 최말단 에지 및 단말 (Far Edge & IoT Devices)
└─ 글로벌 상태 및 데이터 연동 계층 (Global State & Data Synchronization)
```

선의 의미: 통합 오케스트레이터 제어면이 중앙 클라우드, 근접 에지, 최말단 에지 간 연산 자원과 글로벌 데이터 상태를 동적으로 제어·연동하는 계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 통합 제어면 (Unified Control Plane) | 멀티 클라우드/에지 K8s 연합(Federation)을 통해 유휴 자원 추적 및 워크로드 마이그레이션 통제 |
| 중앙 클라우드 (Central Cloud) | 대용량 데이터베이스 보관, 글로벌 AI/ML 딥러닝 모델 학습 및 백업 수행 |
| 근접 에지 (Near Edge) | 기지국 국사 및 5G Local UPF 인근에 위치하여 지역 트래픽 1차 분석 및 비디오 캐싱 담당 |
| 최말단 에지 및 단말 (Far Edge) | 실물 기계, 센서, 가공기 내부에 위치하여 1ms 급 실시간 즉시 제어 및 초저지연 오프로딩 수행 |
| 글로벌 상태 연동 계층 | 워크로드 마이그레이션 시 데이터 런타임 상태(State Context) 및 데이터베이스 일관성 동기화 |

#### 한줄 요약

- 통합 제어면(Control Plane)이 최말단 에지, 근접 에지, 중앙 클라우드의 연산 자원과 데이터 중력을 고려하여 워크로드를 동적 스케줄링하는 구조.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **워크로드 배치 명세(Workload Placement Spec / Manifest)**: 애플리케이션에 필요한 CPU/GPU 자원, 허용 Latency 및 데이터 위치 요구사항을 작성한 매니페스트 파일이다.
- **자원 상태(Resource Telemetry & Capacity)**: 전 영역 노드들의 현재 자원 사용률, 무선 신호 세기, 전력량 및 유선 백홀 지연시간 정보이다.

</details>

```text
1. 분산 노드 자원 상태 및 텔레메트리 모니터링 (Resource Telemetry)
      │
      v
2. 데이터 및 런타임 상태 위치 조회 (Data & State Lookup)
      │
      v
3. 요구 SLO 반영 워크로드 최적 배치 명세 도출 (Placement Scheduling)
      │
      v
4. 컨테이너 워크로드 마이그레이션 및 런타임 복제 (Workload Migration)
      │
      v
5. 앤드투엔드 연산 실행 지표 모니터링 및 Closed-Loop 재배치 (Metrics Evaluation)
```

### 동작 원리

1. **분산 노드 자원 상태 및 텔레메트리 모니터링**: 용량 수집
2. **데이터 및 런타임 상태 위치 조회**: 이동 비용 확인
3. **요구 SLO 반영 워크로드 최적 배치 명세 도출**: 노드 선택
4. **컨테이너 워크로드 마이그레이션 및 런타임 복제**: 세션 전환
5. **앤드투엔드 연산 실행 지표 모니터링 및 Closed-Loop 재배치**: SLO 검증

#### 한줄 요약

- 자원 모니터링, 데이터 위치 조회, SLO 반영 스케줄링, 컨테이너 마이그레이션 및 실시간 지표 모니터링으로 이어지는 동적 배치 흐름.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **위치별 고립 운영(Siloed Island Operation)**: 클라우드와 에지 자원이 단일 관제망으로 결합되지 않고 각각 독립적인 K8s 클러스터로 고정 운영되는 이전 방식이다.

</details>

| 비교 항목 | **컴퓨팅 연속체 (Computing Continuum)** | **위치별 고립 운영 (Siloed Edge & Cloud)** |
|:---|:---|:---|
| 제어 및 관리 체계 | 유니파이드 단일 통합 오케스트레이터 체계 | 파편화된 개별 제어판 (Edge K8s, Cloud K8s 분리) |
| 워크로드 배치 | SLO, 데이터 중력, 전력 상태에 따른 동적 자동 재배치 | 개발자가 초기 설정한 고정 노드에 영구 상주 배치 |
| 자원 효율성 | 클라우드•에지 유휴 자원 공동 활용 | 노드별 자원 파편화•핫스팟 발생 |
| 운용 복잡성 | 계층 간 상태 동기화 및 텔레메트리 수집 복잡도 높음 | 노드 독립 운영으로 상대적 구축/관리 단순 |

> 요약: 통합 관제면으로 클라우드•에지 자원을 동적 배치한다.

#### 한줄 요약

- 연속체는 SLO•데이터 위치에 따라 계층 자원을 재배치

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **워크로드 신원(Workload Identity / SPIFFE)**: 워크로드가 타 노드로 이관되더라도 동일한 인가 앱임을 암호화 서명으로 증명하는 식별자 체계이다.
- **인스턴스 중복 실행(Dual Active Instance Conflict)**: 마이그레이션 도중 이전 노드와 신규 노드에서 동일 컨테이너가 동시에 활성화되어 데이터 일관성이 파괴되는 오류 현상이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 데이터 이동 비용 폭증 | 데이터 중력 고려 없이 연산 노드만 잦은 이동 | Data Gravity 고려한 수송 비용 수식화 스케줄링 | 네트워크 대역폭 낭비 및 이동 오버헤드 방지 |
| 워크로드 보안 위상 차이 | 노드 이관 시 이종 에지 환경의 보안 정책 불일치 | SPIFFE/SPIRE 기반 암호화 워크로드 신원 부여 | 무단 노드 호스팅 차단 및 통합 보안 확보 |
| 마이그레이션 중복 상태 | 이관 과정에서 이전 노드 컨테이너의 잔류 | CRIO/K8s 기반 Make-before-break 세션 락 체계 | 데이터 덮어쓰기 및 일관성 파괴 예방 |
| 노드 텔레메트리 미비 | 계층 간 이종 하드웨어 성능 지표 측정 불가 | eBPF 기반 에이전트리스 광역 텔레메트리 수집 | 실시간 자원 모니터링 및 정밀 오케스트레이션 |

#### 한줄 요약

- 데이터 수송 비용 산정 모델 적용, SPIFFE 기반 워크로드 보안 신원 통합, CRIO/K8s 기반 무손실 컨테이너 이관으로 컴퓨팅 연속체 완성.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **재배치 이득(Relocation Net Gain)**: 워크로드 이동으로 얻는 SLO 성능 향상값에서 데이터 수송 및 마이그레이션 오버헤드 비용을 차감한 실제 효과 수치이다.

</details>

- 재배치 이득이 양수면 **연속체 이동**, 아니면 현 위치 유지

#### 한줄 요약

- 클라우드-에지-IoT 전 구간 통합 제어면 및 데이터 중력 기반 동적 워크로드 오케스트레이션 체계 구현 필수.
