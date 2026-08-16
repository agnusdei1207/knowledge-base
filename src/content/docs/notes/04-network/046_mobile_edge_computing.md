---
sidebar:
  order: 46
  label: "046. 모바일 엣지 컴퓨팅 (MEC, Mobile Edge Computing / Multi-access Edge Computing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "모바일 엣지 컴퓨팅 (MEC, Mobile Edge Computing / Multi-access Edge Computing)"
date: "2026-08-13T17:10:00+09:00"
tags:
  - "notes-network"
weight: 46
extra:
  question_no: "046"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "설계형: 132회 MEC 구조•배치 직접 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **다중접속 에지 컴퓨팅(Multi-Access Edge Computing, MEC)**: 5G 무선 기지국(gNB) 및 코어망 인접 에지에 연산, 저장 및 네트워크 서비스(RNIS) 기능을 분산 배치하는 클라우드 아키텍처이다.
- **로컬 브레이크아웃(Local Breakout, LBO)**: 사용자 데이터 패킷을 코어망 백본까지 이동시키지 않고 에지 기지국 단의 Local UPF에서 즉시 라우팅하여 분기하는 기술이다.

</details>

- 정의/개념: **모바일 에지 컴퓨팅**은 5G 무선 기지국 및 기지국 인근 국사에 서버 연산 자원과 로컬 사용자면 기능(Local UPF)을 전진 배치하여, 트래픽을 중앙망 경유 없이 현장에서 즉시 오프로딩(LBO) 처리하는 분산 컴퓨팅 기술이다.
- 배경/필요성: 기존 중앙 클라우드 전송 방식의 긴 왕복 지연 시간(RTT 30~100ms)과 백홀 유선망 트래픽 폭주 문제를 해결하고, 자율주행, AR/VR, 스마트 공장 OT 등 1ms 대 극저지연 반응과 현장 데이터 보안을 실현하기 위해 도입되었다.

#### 한줄 요약

- 무선 기지국 및 코어 인접 에지에 연산 자원을 전진 배치하고 Local UPF 기반 트래픽 오프로딩을 통해 초저지연 및 백본 트래픽 감소를 구현하는 분산 컴퓨팅 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **다중접속 에지 컴퓨팅 오케스트레이터(MEC Orchestrator, MEO)**: 에지 응용의 배치와 수명주기를 관리하는 제어기이다.
- **사용자면 기능(User Plane Function, UPF)**: 5G 코어 아키텍처에서 사용자 패킷을 오프로딩하여 에지 데이터망으로 라우팅하는 핵심 NF이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 에지 앱이 기지국의 무선 신호 품질(RNIS), 위치 정보(Location) 및 트래픽 정책에 접근하게 해주는 기술 규격이다.

</details>

- **로컬 트래픽 오프로딩 **: Local UPF 연동을 통해 데이터 패킷을 중앙 코어망으로 보내지 않고 구내망/사내 MEC 서버로 직결 분기 처리한다.
- **무선망 정보 서비스 연동 **: ETSI 표준 MEC 플랫폼(MEP)을 제공하여 에지 애플리케이션이 실시간 무선 채널 세기(RSSI), 셀 부하 정보를 활용하게 한다.
- **초저지연 및 데이터 잔류성 보장**: 물리적 전송 거리를 수십 km에서 수백m 이내로 단축하여 무선 응답 지연 1ms 대를 달성하고, 사내 민감 데이터의 외부 유출을 방지한다.

#### 한줄 요약

- Local UPF 연동 로컬 브레이크아웃, ETSI 규격 MEP/RNIS API 제공, 초저지연 및 현장 데이터 보안 확보.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **로컬 사용자면 기능(Local User Plane Function, Local UPF)**: SMF의 제어를 받아 트래픽을 코어 백본망이 아닌 현장 MEC 호스트로 라우팅하는 5G NF이다.
- **MEC 플랫폼(MEC Platform, MEP)**: 에지 호스트 내에서 응용 프로그램의 등록, 데이터 릴레이 및 무선 네트워크 서비스 API를 중계하는 제어 모듈이다.

</details>

```text
ETSI MEC 시스템 아키텍처
├─ 오케스트레이션 및 관리 계층 (MEC System Level Management - MEO)
├─ 로컬 패킷 전송 계층 (Local UPF & Traffic Offloading)
└─ 에지 연산 및 플랫폼 계층 (MEC Host)
   ├─ 에지 서비스 플랫폼 (MEC Platform - MEP)
   └─ 에지 응용 컨테이너 (MEC Applications - App1, App2)
```

선의 의미: 오케스트레이터(MEO)가 에지 호스트의 응용 수명주기를 관리하고, Local UPF가 트래픽을 오프로딩하면 MEP가 서비스 API를 연동해 에지 응용을 구동하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| MEC 시스템 오케스트레이터 (MEO) | 글로벌 자원 상태 및 SLA를 기반으로 에지 응용의 생성, 배치 위치 결정 및 수명주기 관리 |
| 로컬 UPF (Local UPF) | N4 규격(PFCP)에 따라 5G 무선 패킷을 중앙 코어망 대신 구내 MEC 호스트로 즉시 분기 처리 |
| MEC 플랫폼 (MEP) | RNIS•위치 API 제공 및 에지 응용 간 패킷 라우팅 |
| MEC 호스트 (MEC Host) | 에지 서버 상에서 K8s/Docker 가상화 자원을 제공하고 에지 응용(App Container)을 직접 구동 |
| 에지 응용 (MEC Apps) | 초저지연 자율주행 알고리즘, AR/VR 렌더링, 공장 불량 AI 검사 등 실시간 서비스 구동 |

#### 한줄 요약

- MEO가 에지 응용 수명주기를 관리하고 MEP가 무선 망 정보 API를 제공하며 Local UPF가 트래픽을 MEC 호스트로 라우팅하는 아키텍처.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **트래픽 조향(Traffic Steering)**: 5G 코어 SMF와 MEC MEP 간 연동을 통해 특정 5QI 트래픽의 데이터 전달 경로를 Local UPF로 지정하는 규칙 적용 절차이다.
- **프로토콜 데이터 단위 세션(Protocol Data Unit Session, PDU Session)**: 단말과 MEC 에지 데이터망(DN) 간에 확립되는 사용자 세션 경로이다.

</details>

```text
1. MEC 오케스트레이터의 에지 응용 패키징 및 배치 (App Deployment Spec)
      │
      v
2. 지정된 MEC 호스트로 컨테이너 구동 및 인스턴스화 (App Instantiation)
      │
      v
3. MEP -> 5GC SMF: 로컬 트래픽 오프로딩 정책 요청 (Traffic Steering Rule)
      │
      v
4. SMF -> Local UPF: N4 인터페이스 PFCP 패킷 라우팅 세팅 (PDU Session Setup)
      │
      v
5. 단말 패킷의 Local UPF 경유 및 MEC 초저지연 연산 처리 (LBO Offloading)
```

### 동작 원리

1. **에지 응용 배치 요청**: MEO 오케스트레이터가 서비스 요구 프로필을 분석하여 적합한 에지 호스트에 응용 이미지를 배포한다.
2. **응용 인스턴스화 및 셋업**: 지정된 MEC 호스트가 가상화(K8s/Container) 엔진을 통해 에지 응용을 구동하고 MEP에 등록한다.
3. **트래픽 조향 규칙 요청**: MEP가 5GC SMF에 해당 응용 트래픽을 분기하기 위한 오프로딩 규칙(Traffic Steering Rule)을 전달한다.
4. **Local UPF 세션 설정**: SMF가 Local UPF에 PFCP 세션 라우팅 지침을 내려 전용 PDU 세션 통로를 완성한다.
5. **초저지연 로컬 처리**: 단말 패킷이 기지국과 Local UPF를 거쳐 코어망 경유 없이 현장 MEC 응용으로 오프로딩되어 실시간 연산을 수행한다.

#### 한줄 요약

- 에지 응용 배치, 호스트 인스턴스화, SMF 트래픽 조향 요청, Local UPF 라우팅 세팅 및 LBO 로컬 처리 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **중앙 클라우드(Central Cloud)**: 수도권 또는 통합 데이터센터(IDC)에 대용량 서버 인프라를 모아둔 중앙 집중형 클라우드이다.

</details>

| 비교 항목 | **모바일 에지 컴퓨팅 ** | **중앙 클라우드 ** |
|:---|:---|:---|
| 자원 배치 위치 | 기지국, Edge UPF, 국사 인근 (기지국 인접) | 중앙 전용 데이터센터 (IDC) |
| 반응 지연시간 (RTT) | 1ms ~ 10ms 이내 (초저지연) | 30ms ~ 100ms 이상 (상대적 고지연) |
| 트래픽 처리 방식 | Local UPF 기반 LBO 로컬 즉시 처리 | 무선 백홀망 및 중앙 코어망 전체 경유 처리 |
| 망 정보 연동 (RNIS) | 무선 채널 세기(RSSI), 셀 부하 정보 실시간 제공 | 무선 망 내부 정보 접근 및 피드백 불가능 |
| 주요 사용 목적 | 자율주행, AR/VR, 스마트 공장 OT, 실시간 AI | 빅데이터 분석, 글로벌 AI 모델 학습, 대용량 저장 |

> 요약: MEC는 기지국 단의 초저지연 실시간 연산 및 무선 정보(RNIS) 연동에 특화되고, 중앙 클라우드는 글로벌 빅데이터 집약 연산에 특화.

#### 한줄 요약

- MEC는 기지국 단의 초저지연 실시간 연산 및 무선 정보(RNIS) 연동에 특화되고, 중앙 클라우드는 글로벌 빅데이터 집약 연산에 특화.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **세션 앵커(Session Anchor UPF / PSA)**: 단말이 이동하더라도 PDU 세션의 데이터 분기 기준점으로 작동하는 UPF 엔티티이다.
- **원격 증명(Remote Attestation)**: 무선망 가장자리에 노출된 MEC 호스트의 OS 및 무결성 상태를 검증하는 위변조 방지 보안 기술이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 이동 시 에지 세션 단절 | 단말이 기지국을 넘어가며 인근 MEC 호스트와 세션 이탈 | Stateful User Context Relocation 및 I-UPF 핸드오버 | 이동 중에도 끊김 없는 MEC 서비스 연속성 유지 |
| 물리적 에지 노드 보안 취약 | 물리적 기지국 국사에 배치되어 원격 해킹 위험 | TPM 기반 Remote Attestation 및 자원 격리 보안 | 미승인 이미지 구동 차단 및 호스트 무결성 확보 |
| 오프로딩 경로 지정 실패 | SMF•MEP 간 트래픽 조향 오류 | **DNAI** 매핑 자동 검증 | 경로 오차•패킷 유실 방지 |
| 에지 컴퓨팅 자원 부족 | 한정된 소형 에지 서버 자원에 트래픽 폭주 | 중앙 클라우드로의 Dynamic Offloading 및 자원 확장 | 에지 자원 고갈 예방 및 시스템 서비스 가용성 확보 |

#### 한줄 요약

- 단말 이동 시 Stateful Context 이전, TPM 기반 Remote Attestation 보안 검증 및 Local UPF 직결 경로 설계로 MEC 안정성 보장.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **데이터 잔류(Data Residency)**: 기업 및 국토 내부에서 발생한 데이터 패킷이 외부 지역이나 통신사 백본망으로 나가지 않고 로컬에서 소멸되는 관제 원칙이다.

</details>

- 실시간•현장 데이터는 **MEC**, 집약 연산은 **중앙 클라우드** 선택

#### 한줄 요약

- ETSI 표준 기반 MEC 오케스트레이션 및 Local UPF 연동 로컬 브레이크아웃(LBO) 구축 필수.
