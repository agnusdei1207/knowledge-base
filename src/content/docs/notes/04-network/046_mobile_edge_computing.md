---
sidebar:
  order: 46
  label: "046. 모바일 엣지 컴퓨팅: MEC"
  badge:
    text: "기출 · 50%"
    variant: note
title: "모바일 엣지 컴퓨팅 : MEC (Multi-access Edge Computing)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 46
extra:
  question_no: "46"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "ETSI MEC 표준 프레임워크, Local Breakout(LBO) 및 RNIS 무선망 정보 서비스"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MEC (Multi-access Edge Computing)**: 기지국 인접 지점(Edge)에 컴퓨팅 인프라를 배치하여 데이터를 로컬에서 즉시 연산·처리하는 ETSI 표준 아키텍처.
- **LBO (Local Breakout)**: 사용자 트래픽을 중앙 코어망으로 보내지 않고 기지국 인근의 로컬 UPF를 통해 현장 MEC 호스트로 직접 분기하는 기술.

</details>

- 정의/개념: 기지국(gNB) 및 국사 종단에 IT 컴퓨팅과 **Local UPF를 전진 배치하여 로컬 트래픽 분기(LBO)와 1ms 초저지연 연산을 제공하는 ETSI 표준 엣지 기술**
- 배경/필요성: 중앙 클라우드 원거리 왕복 지연(30~100ms)과 백홀 병목으로 인한 **자율주행 V2X, 실시간 머신비전 AI 제어 및 백홀 대역폭 비용 폭증 해결 불가**

#### 한줄 요약
- 기지국 인접 Local UPF를 통해 데이터를 현장에서 즉시 분기 처리하여 1ms 초저지연을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RNIS (Radio Network Information Service)**: 기지국의 실시간 채널 품질, 사용자 위치, 셀 혼잡도 정보를 엣지 앱에 REST API로 제공하는 ETSI 표준 서비스.
- **Data Sovereignty (데이터 주권)**: 사내 핵심 영상/센서 데이터가 외부 공용망으로 나가지 않고 로컬 엣지에서 완결 처리되는 보안 권한.

</details>

- 물리적 전송 거리를 단축하여 무선 종단 간 왕복 지연을 1~5ms로 단축하는 **결정론적 초저지연**
- 고용량 CCTV 영상 등을 로컬에서 전처리하여 **백홀 트래픽 80% 이상 절감 및 데이터 주권 확보**
- 기지국 무선 품질 지표를 실시간 조회하여 비디오 해상도를 적응 제어하는 **무선망 인지형 서비스(RNIS)**

#### 한줄 요약
- 1ms 초저지연, 백홀 트래픽 절감, 데이터 주권 보호, RNIS 기반 무선망 인지 서비스를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MEO (MEC Orchestrator)**: 전체 분산 MEC 호스트의 자원을 통합 관리하고 앱 패키지 배치 및 생명주기를 총괄하는 최상위 관리자.
- **MEP (MEC Platform)**: 개별 엣지 서버 내에서 엣지 앱(MEC App)의 런타임을 제공하고 RNIS, 위치 API를 중계하는 플랫폼.

</details>

```text
[ETSI MEC 시스템 아키텍처 및 5G 로컬 트래픽 분기 구조]
|-- MEC Management (MEO: MEC Orchestrator -> 분산 엣지 호스트 자원 총괄)
`-- MEC Host (gNB 기지국 인접 엣지 서버)
    |-- MEP (MEC Platform: RNIS, Location API, DNS 중계 서비스)
    `-- MEC Apps (컨테이너 기반 자율주행 V2X, 실시간 비전 AI 추론 앱)
`-- 5G Core Network Integration
    |-- 5G gNB (단말 무선 신호 인입)
    |-- Local UPF (SMF 제어 N4 PFCP -> N6 인터페이스 사내 MEC App 로컬 분기 LBO)
    `-- Central UPF & 5GC Core (비엣지 일반 인터넷 트래픽 중앙 전송)
```

선의 의미: 계층 및 기지국에서 수신된 트래픽 중 초저지연 요청은 Local UPF를 통해 MEC Host로 즉시 분기되고 일반 트래픽은 중앙 5GC로 전송되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **MEC 오케스트레이터 (MEO)**| 전체 분산 엣지 호스트의 자원 토폴로지를 관리하고 **SLA 기반 컨테이너 앱 자동 배포** | Mm1, Mm3 관리 |
| **MEC 플랫폼 (MEP)** | 엣지 앱 등록 관리, **무선망 정보(RNIS) 및 위치 서비스 API를 응용에 중계 제공** | Mp1, Mp2 인터페이스 |
| **Local UPF (LBO)** | 5GC SMF의 트래픽 조향 규칙에 따라 **엣지 트래픽을 사내 MEC로 직접 로컬 분기(LBO)** | U-Plane 고속 라우팅 |
| **MEC Apps (엣지 응용)**| 컨테이너 기반으로 구동되는 **실시간 영상 분석, AI 추론 및 V2X 차량 관제 모듈** | Mp1 연동 |

#### 한줄 요약
- MEO 오케스트레이터, MEP 플랫폼, Local UPF, MEC Apps가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DNAI (Data Network Access Identifier)**: 5G 코어망에서 사용자 세션이 특정 로컬 엣지 데이터망(MEC)으로 라우팅되도록 지정하는 식별자.

</details>

```text
MEC 로컬 트래픽 오프로딩(LBO) 파이프라인
        │
   1. [엣지 앱 배포] MEO가 지연 SLA를 분석하여 최적 엣지 호스트(MEC Host)에 컨테이너 배포
        │
   2. [트래픽 조향 룰 등록] MEP가 5GC 코어(SMF/NEF)로 DNAI 매핑 및 LBO 라우팅 규칙 등록
        │
   3. [단말 패킷 인입] 단말이 gNB로 데이터 전송 -> Local UPF가 패킷 검사(PDR) 수행
        │
   ▼
4. [사내 MEC 직결 포워딩] Local UPF가 중앙 코어 경유 없이 사내 MEC App으로 1ms 내 즉시 포워딩
```

#### 한줄 요약
- 엣지 앱 배포 → 트래픽 조향 룰 등록 → Local UPF 패킷 분기 → 초저지연 로컬 연산 및 응답 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **MEC** vs **Central Cloud**: 기지국 인접 분산 배치(MEC)와 원거리 대형 데이터센터 집중 배치(Central Cloud).

</details>

| 비교 항목 | 모바일 엣지 컴퓨팅 (MEC) | 중앙 집중형 클라우드 (Central Cloud) |
|:---|:---|:---|
| **배치 위치** | **기지국(gNB), 국사, 온프레미스 현장 (Edge)** | 대규모 리전 데이터센터 (수백 km 원거리) |
| **네트워크 지연 (RTT)** | **1 ~ 10 ms (결정론적 초저지연)** | 30 ~ 100 ms (공용 인터넷 백본 전송 지연) |
| **백홀 트래픽 부하** | **현장 처리로 백홀 트래픽 80% 이상 절감** | 모든 트래픽이 백본망을 통과하여 병목 유발 |
| **무선망 인지(RNIS)** | **가능 (기지국 채널/위치 정보 API 활용)** | 불가능 (무선 계층 제어 정보 접근 불가) |
| **주요 적합 서비스** | **자율주행(V2X), 스마트 팩토리, 원격 수술** | 대규모 빅데이터 분석, LLM 학습, 중앙 DB |

#### 한줄 요약
- MEC는 기지국 인접 배치로 초저지연과 데이터 주권을 보장하고, 중앙 클라우드는 대규모 연산 처리를 전담한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Context Relocation (상태 컨텍스트 재배치)**: 단말 이동 시 이전 엣지 서버의 활성 세션 상태(State)를 신규 엣지 서버로 고속 복제·이관하는 기술.
- **Remote Attestation (원격 무결성 증명)**: 분산 배치된 엣지 서버 하드웨어의 부팅 무결성을 TPM(신뢰 플랫폼 모듈) 기반으로 원격 검증하는 보안 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단말 고속 이동 시 서빙 기지국 전환에 따른 엣지 세션 단절 | **`상태 컨텍스트 재배치(Context Relocation)` 및 L3 세션 인계** | 엣지 간 핸드오버 시 지연 없는 서비스 연속성 유지 |
| 물리적 보안이 취약한 분산 국사 엣지 서버의 침해 및 변조 위협 | **하드웨어 `TPM 기반 원격 무결성 증명(Remote Attestation)`** | 비인가 펌웨어 위변조 탐지 및 제로 트러스트 보안 |
| 트래픽 조향 룰 오류로 로컬 패킷이 중앙 코어로 오라우팅 누수 | **`DNAI(데이터망 접근 식별자) 자동 검증` 및 패킷 필터링 감사** | 로컬 오프로딩 누락 방지 및 데이터 주권 보증 |
| 다수 엣지 서버 관리 복잡도 및 장애 모니터링 한계 | **`쿠버네티스 기반 엣지 오케스트레이션(K8s/K3s)` 일원화** | 중앙 단일 콘솔을 통한 수천 개 엣지 무인 배포 |

#### 한줄 요약
- Context Relocation, TPM 원격 증명, DNAI 검증, 쿠버네티스 엣지 오케스트레이션으로 운영한다.

## Ⅶ. 결론

- 초저지연 미션 크리티컬 서비스와 데이터 주권 확보를 위해 **ETSI 표준 MEC 아키텍처와 Local UPF 오프로딩을 기지국 종단에 전진 배치**하고, 분산 인프라의 이동성과 보안 한계를 해결하기 위해 **Context Relocation과 TPM 기반 원격 무결성 검증 체계**를 통합 구축하여 고신뢰 엣지 컴퓨팅 생태계 완성

#### 한줄 요약
- MEC는 기지국 인접 컴퓨팅과 Local UPF를 통해 1ms 초저지연과 데이터 주권을 실현하는 핵심 분산 클라우드 아키텍처다.