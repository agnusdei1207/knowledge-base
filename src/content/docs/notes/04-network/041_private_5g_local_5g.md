---
sidebar:
  order: 41
  label: "041. 5G 특화망•로컬 5G (Private 5G / 이음5G)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "5G 특화망•로컬 5G (Private 5G / 이음5G)"
date: "2026-08-13T16:58:00+09:00"
tags:
  - "notes-network"
weight: 41
extra:
  question_no: "041"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "비교•설계형: 126회 5G 특화망 장문 출제"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: 초고속, 초저지연, 대규모 연결성을 지원하는 차세대 이동통신 기술 표준이다.
- **5G 특화망(Private 5G / Local 5G)**: 스마트 공장, 항만, 병원 등 한정된 구역 내에서 기업이 전용 주파수를 받아 직접 구축·운용하는 비공중망(NPN)이다.

</details>

- 정의/개념: **5G 특화망(Private 5G, 이음5G)**은 특정 건물, 공장, 스마트 항만 등 한정된 구역에 전용 5G 주파수(4.7GHz/28GHz 대역)를 사용하여 기업이 맞춤형 5G 무선망, 코어망(5GC) 및 QoS 정책을 직접 운용하는 독립 비공중망(Non-Public Network, NPN)이다.
- 배경/필요성: 기존 이동통신사 공중망의 장애 종속성 회피, 스마트 팩토리 OT 설비의 1ms 대 초저지연 제어, 그리고 기업 내부 기밀 데이터의 외부 유출 방지를 위한 데이터 주권(Data Sovereignty) 확보를 위해 도입되었다.

#### 한줄 요약

- 전용 5G 자원으로 구내 데이터 경로와 OT 품질 통제

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **무선 접속망(Radio Access Network, RAN)**: 단말과 5G 코어망 사이의 무선 신호 송수신을 담당하는 전용 기지국(gNB) 인프라 체계이다.
- **서비스 품질(Quality of Service, QoS)**: 단말 및 앱 특성에 맞춰 무선 자원(5QI) 및 전송 폭을 차등 보장하는 네트워크 제어 파라미터이다.
- **사용자면 기능(User Plane Function, UPF)**: 사용자 데이터 패킷의 라우팅과 에지 분기를 담당하며, 특화망에서는 구내 Local UPF 형태로 설치된다.
- **가입자 식별 모듈(Subscriber Identity Module, SIM)**: 특화망 인가 단말의 고유 식별자(SUPI) 및 암호화 키를 보관하여 보안 접속을 보장하는 모듈이다.

</details>

- **전용 주파수 및 자원 독점성**: 공중망의 주파수 경합 없이 4.7GHz/28GHz 전용 주파수를 사용하여 외부 트래픽 방해 없는 독점적 통신 환경을 제공한다.
- **Local UPF 기반 데이터 주권 확보**: 구내 LAN•MEC로 직접 분기해 외부 경유를 줄인다.
- **업링크 중심 맞춤형 네트워크**: 산업용 센서 및 고화질 CCTV 영상 수집을 위해 상향(Uplink) 대 하향(Downlink) 주파수 대역 비율(예: 3:7 또는 4:6)을 맞춤 변경할 수 있다.

#### 한줄 요약

- 전용 주파수•Local UPF•SIM 기반 구내 통신 통제

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **5세대 코어(5G Core, 5GC)**: 가입자 인증(AMF/UDM), 세션 관리(SMF) 및 슬라이싱 정책을 관리하는 특화망 전용 콤팩트 코어 시스템이다.
- **로컬 사용자면 기능(Local User Plane Function, Local UPF)**: 구내 현장에 전진 배치되어 사용자 패킷을 사내 네트워크로 즉시 분기하는 사용자 평면 NF이다.
- **다중접속 에지 컴퓨팅(Multi-Access Edge Computing, MEC)**: 기지국 단에 배치되어 현장 AI 분석, 자율주행 로봇(AGV) 통제 등을 초저지연 처리하는 컴퓨팅 플랫폼이다.
- **운영 기술(Operational Technology, OT)**: 공장 제조 설비, 로봇, 공정 제어기(PLC) 등 현장 실물 설비를 직접 관제하고 제어하는 시스템 체계이다.
- **비공중망(Non-Public Network, NPN)**: 3GPP 표준에서 정의한 특정 기업 또는 구역 전용의 비공개 이동통신망 체계이다.

</details>

```text
5G 특화망 (Private 5G / NPN) 구조
├─ 무선 접속망 도메인 (Dedicated RAN - gNB)
├─ 코어망 도메인 (Compact 5GC - AMF/SMF/UDM)
├─ 현장 분기 도메인 (Local UPF)
└─ 현장 연동 도메인 (MEC Platform & Industrial OT System)
```

선의 의미: 구내 인프라에 전용 기지국(RAN), 콤팩트 5GC 및 Local UPF가 구축되어 사내 MEC 및 OT 제어 시스템과 직결 통신하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 전용 무선 접속망 (RAN gNB) | 4.7GHz / 28GHz 전용 특화망 주파수를 활용하여 구내 단말과의 무선 커버리지 구축 |
| 구내 콤팩트 5GC | AMF, SMF, UDM 등 가입자 식별, 이동성 및 세션 관리를 수행하는 소형 코어망 인프라 |
| Local UPF (현장 분기) | SMF의 제어를 받아 사용자 패킷을 외부 인터넷이 아닌 사내 LAN/MEC로 직결 바이패스 |
| MEC 플랫폼 | 현장 카메라 영상 분석, 자율주행 AGV 위치 제어, AR 설비 점검 등 초저지연 앱 구동 |
| OT 시스템 (PLC / SCADA) | Local UPF를 통해 전달된 초저지연 패킷을 수신하여 현장 제조 설비 및 로봇 직접 제어 |

#### 한줄 요약

- 전용 5G 기지국과 Compact 5GC, Local UPF가 구내 인프라에 통합 구축되어 외부망 경유 없이 현장 OT 시스템과 직접 통신하는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **프로토콜 데이터 단위 세션(Protocol Data Unit Session, PDU Session)**: 단말과 특화망 내부 데이터망(DN) 간 패킷을 주고받기 위해 형성되는 논리적 세션 연결이다.
- **가입자 인증 요청(Subscriber Authentication Request)**: USIM의 식별 정보를 바탕으로 구내 5GC UDM에서 접근 권한을 확인하는 절차이다.
- **PDU 세션 규칙(PDU Session Rule)**: 트래픽을 외부망이 아닌 현장 Local UPF로 라우팅하도록 5GC SMF가 지정하는 패킷 전달 규칙이다.

</details>

```text
1. 산업용 단말(UE) 특화망 전용 USIM 접속 요청 (NAS Registration)
      │
      v
2. 구내 Compact 5GC: 가입자 식별 및 특화망 전용 인증 (UDM Auth & NPN Check)
      │
      ├─ 인증 실패 ---- 접속 차단 및 접속 불허 (Access Denied)
      └─ 인증 성공
            │
            v
      3. PDU 세션 확립 및 Local UPF 로컬 패킷 라우팅 경로 세팅 (PDU Session Setup)
            │
            v
      4. 산업 서비스별 5QI 무선/전송 QoS 정책 적용 (QoS Policy Enforce)
            │
            v
      5. Local UPF를 통한 현장 MEC 및 OT 설비 초저지연 데이터 송수신
```

### 동작 원리

1. **특화망 접속 요청**: 산업용 단말(AGV, 센서 등)이 구내 전용 기지국(RAN)을 통해 특화망 전용 USIM 정보로 접속을 요청한다.
2. **가입자 식별 및 승인**: 콤팩트 5GC의 AMF/UDM이 해당 USIM의 구내 비공중망(NPN) 접근 인가 권한을 검증한다.
3. **PDU 세션 및 Local UPF 경로 설정**: SMF가 세션을 생성하고 패킷이 사내망으로 라우팅되도록 Local UPF에 PFCP 세션을 확립한다.
4. **QoS 파라미터 적용**: 트래픽 특성(원격 제어 5QI=82, 일반 영상 5QI=9 등)에 맞춰 무선 구간 우선순위 및 대역폭 정책을 하향 적용한다.
5. **초저지연 현장 통신 실행**: Local UPF를 거쳐 트래픽이 구내 MEC 및 OT 시스템(PLC)에 전달되어 1ms 대의 즉각적 제어가 이루어진다.

#### 한줄 요약

- 특화망 USIM 인증, PDU 세션 생성, Local UPF 경로 설정, 맞춤형 5QI 적용 및 현장 OT 초저지연 데이터 통신 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **독립형 비공중망(Standalone Non-Public Network, SNPN)**: 공중망 연동 없이 전용 5GC와 전용 기지국을 100% 구내에 독립 구축하여 운용하는 특화망이다.
- **공중망 통합 비공중망(Public Network Integrated Non-Public Network, PNI-NPN)**: 기지국만 구내에 두고 코어망 및 가입자 관리는 통신사 공중망을 공유·위탁하는 특화망이다.

</details>

| 비교 항목 | **독립형 5G 특화망 (SNPN)** | **기업용 Wi-Fi (Wi-Fi 6E/7)** | **공중망 슬라이싱 (PNI-NPN)** |
|:---|:---|:---|:---|
| 주파수 대역 | 전용 특화망 주파수 (4.7G/28GHz) | 비면허 공유 주파수 (2.4G/5G/6GHz) | 통신사 공용 면허 주파수 대역 공유 |
| 보안 및 데이터 주권 | 구내 Local UPF로 내부 경로 통제 | 사내 정책 적용•공유 대역 간섭 | 통신사 코어 정책과 경로 의존 |
| 무선 이동성 | 고속 이동 시에도 Seamless 무손실 로밍 | 셀 전환 시 수십ms 전송 끊김 및 손실 | 넓은 광역 이동성 지원하나 자원 경합 가능 |
| 구축 및 운용 모델 | 초기 5GC/RAN CAPEX 고비용, 전문 기술 필요 | 매우 저렴한 AP 구축비용 및 관리의 용이성 | 월 정액 기반 OPEX 처리, 통신사 위탁 관리 |

> 요약: 높은 보안성, 이동성 및 OT 저지연이 요구되면 SNPN 5G 특화망, 단순 근거리 통신은 Wi-Fi 적용.

#### 한줄 요약

- 구내 통제는 SNPN, 저비용은 Wi-Fi, 광역은 PNI-NPN

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **무선 음영(Radio Shadow Area)**: 공장 내 금속 구조물, 고중량 설비에 전파가 반사·차단되어 전파 세기가 수신 한계 이하로 떨어지는 현상이다.
- **경로 정책(Traffic Steering Policy)**: 특정 단말의 트래픽을 예외 없이 Local UPF로 분기하도록 규정하는 세션 라우팅 지침이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 공장 내 전파 음영 구역 | 금속 설비의 전파 반사•차단 | 3D 전파 측정 및 DAS 배치 | 음영 구역 축소•품질 균일화 |
| 상향(Uplink) 대역폭 부족 | 고화질 CCTV, 산업 AR 영상 전송 급증으로 Uplink 병목 | TDD 프레임 패턴 가변 변경(Downlink:Uplink = 4:6) | Uplink 전송 속도 2배 증대 및 영상 병목 해소 |
| 5GC 운영 전문성 부족 | 기업 내 5G 전문 인력 부재로 장애 복구 지연 | Managed 5GC 서비스 도입 및 AI 네트워크 AIOps 도입 | 코어망 운용 오버헤드 감소 및 가용성 확보 |
| 사설망 간 주파수 간섭 | 인접 특화망 사업자 간 4.7GHz 주파수 경계면 파형 간섭 | 기지국 GPS 시간 동기화 및 3GPP Guard Band 설정 | 인접 사설망 간 전파 간섭 최소화 |

#### 한줄 요약

- 3D 전파 섀도잉 분석, Uplink 대역폭 가변 분할(TDD Pattern 변경), Local UPF 오프로딩 및 관리형 5GC 도입으로 특화망 안정성 확보.

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **데이터 주권(Data Sovereignty)**: 데이터의 생성, 저장, 처리 및 이동 경로를 조직이 타인의 개입 없이 완전 통제할 수 있는 권리이다.

</details>

- 구내 독립 통제는 **SNPN**, 통신사 연계는 **PNI-NPN** 선택

#### 한줄 요약

- 전용 주파수 기반 SNPN 특화망 구축 및 Local UPF/MEC 연동 기반 데이터 주권 체계 구현 필수.
