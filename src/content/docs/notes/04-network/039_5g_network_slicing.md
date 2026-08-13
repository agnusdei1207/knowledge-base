---
sidebar:
  order: 39
  label: "039. 5G 네트워크 슬라이싱"
  badge: { text: "기출 • 70%", variant: note }
title: "5G 네트워크 슬라이싱"
date: "2026-08-13T16:54:00+09:00"
tags: ["notes-network"]
weight: 39
extra:
  question_no: "039"
  source_status: "기출"
  source_history: "126회, 137회"
  priority: 70
  priority_note: "126•137회 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **네트워크 슬라이싱(Network Slicing)**: 단일 5G 물리 네트워크 위에 무선(RAN), 전송(Transport), 코어(Core) 가상 자원을 분할하여 독립적인 종단(End-to-End) 가상 논리망을 구축하는 기술이다.
- **서비스 수준 협약(Service Level Agreement, SLA)**: 사업자와 고객 간에 정의된 처리량, 종단 지연시간, 자원 격리성 및 가용성 보장 계약 수치이다.
- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: 서비스 특성에 따라 네트워크 자원을 동적 할당할 수 있도록 설계된 차세대 이동통신 표준이다.

</details>

- 정의/개념: **5G 네트워크 슬라이싱(Network Slicing)**은 단일 물리 인프라망을 가상화 기술(NFV/SDN)을 활용해 무선, 전송, 코어 전 구간에서 독립적인 전용 가상 네트워크로 격리 분할하여 서비스(eMBB, URLLC, mMTC) 맞춤형 SLA를 제공하는 5G 핵심 기술이다.
- 배경/필요성: 단일 물리망에서 단순 패킷 우선순위(QoS)를 부여하는 방식으로는 자원 경합에 의한 초저지연 및 고신뢰성 훼손을 방지할 수 없어, 전 구간 독립 가상망을 제공하는 슬라이싱 아키텍처가 도입되었다.

#### 한줄 요약

- 단일 5G 물리망을 가상화 기반으로 분할하여 서비스 특성에 맞는 독립적 종단(E2E) 가상 논리망을 생성하고 SLA를 보장하는 핵심 5G 기술.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **종단 자원 조립(End-to-End Resource Orchestration, E2E Resource Orchestration)**: RAN 서브넷, 전송 서브넷, 코어 서브넷 자원을 유기적으로 연결하여 하나의 독립 가상망으로 서비스하는 조립 과정이다.
- **자원 격리(Resource Isolation)**: 특정 슬라이스에서 트래픽 폭주나 장애가 발생해도 타 슬라이스의 대역폭, 지연, NF 자원에 전혀 영향을 미치지 않도록 차단하는 특성이다.

</details>

- **E2E 전 구간 자원 통합 오케스트레이션**: 무선망(PRB 할당), 전송망(FlexE/SRv6), 코어망(NF 인스턴스)의 가상 자원을 하나의 논리 슬라이스로 템플릿화하여 바인딩한다.
- **슬라이스 간 완벽한 자원 격리(Isolation)**: 컴퓨팅, 주파수, 라우팅 자원을 고정/가변 논리적으로 완전 격리하여 트래픽 상충 및 간섭을 원천 차단한다.
- **동적 수명주기 관리(Lifecycle Management)**: 오케스트레이터를 통해 슬라이스의 생성, 스케일링, 자원 변경, 폐기를 자동화한다.

#### 한줄 요약

- E2E 가상 자원 동적 조립, 슬라이스 간 완전 자원 격리, SLA 기반 동적 수명주기 자동화 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **슬라이스 오케스트레이터(Network Slice Orchestrator, CSO/NSO)**: 서비스 수명주기 자동화 및 영역별 서브넷 오케스트레이터(NSSMF)와 연동하여 E2E 슬라이스를 구축하는 중앙 통제 시스템이다.
- **네트워크 슬라이스 선택 기능(Network Slice Selection Function, NSSF)**: 가입자의 S-NSSAI 식별자를 분석하여 적합한 코어망 슬라이스(AMF/SMF 인스턴스)를 지정하는 5G 코어 NF이다.
- **접속·이동성 관리 기능(Access and Mobility Management Function, AMF)**: 슬라이스 인가를 확인하고 가입자 단말을 해당 슬라이스로 유도하는 5G 제어 NF이다.
- **세션 관리 기능(Session Management Function, SMF)**: 선택된 슬라이스 내에서 PDU 세션을 관리하고 UPF 경로를 제어하는 NF이다.
- **사용자면 기능(User Plane Function, UPF)**: 슬라이스 전용으로 할당되어 해당 슬라이스의 데이터 패킷만을 고속 라우팅하는 사용자 평면 NF이다.

</details>

```text
5G 엔드투엔드 네트워크 슬라이싱 구조
├─ 오케스트레이션 및 관리 도메인 (SLA & Lifecycle Management)
│  ├─ 서비스 서비스 수준 협약 모델 (Service Profile / SLA)
│  ├─ 네트워크 슬라이스 오케스트레이터 (CSMF / NSMF / NSSMF)
│  └─ 도메인별 가상 자원 (RAN / Transport / Core Slice Subnets)
└─ 코어망 가입자 및 세션 제어 도메인 (Core Control Plane)
   ├─ 네트워크 슬라이스 선택 기능 (NSSF)
   ├─ 접속 및 이동성 관리 기능 (AMF)
   ├─ 세션 관리 기능 (SMF)
   └─ 사용자 평면 기능 (UPF - Edge/Central)
```

선의 의미: 서비스 SLA 모델에 맞춰 오케스트레이션 도메인이 3대 영역(RAN/전송/코어) 서브넷을 구축하고, 코어 제어 도메인이 NSSF를 통해 가입자 단말을 전용 슬라이스 세션으로 바인딩하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 서비스 SLA 프로파일 | 서비스별 필요 대역폭, 엔드투엔드 목표 지연시간, 최대 접속 단말 수 및 자원 격리 수준 수치화 |
| 슬라이스 오케스트레이터(NSMF) | E2E 슬라이스 템플릿(NST) 관리, 서브넷(AN/TN/CN NSSMF) 분할 명령 및 수명주기 통제 |
| 무선/전송/코어 자원 서브넷 | 무선(PRB/지연), 전송(FlexE/VLAN/SRv6), 코어망(가상 NF 인스턴스) 독립 자원 수용 |
| NSSF (Slice Selection Function) | 가입자 정보(S-NSSAI) 및 단말 위치를 기반으로 단말이 접근할 코어망 슬라이스 셋 결정 |
| AMF / SMF | 선택된 슬라이스의 접속 인가를 검증하고, 슬라이스 전용 PDU 세션 정책 및 UPF 라우팅 제어 |
| UPF (User Plane Function) | 슬라이스별로 물리/가상 분리 배치되어 전용 백본 또는 에지(MEC)로 패킷 라우팅 |

#### 한줄 요약

- 오케스트레이터가 SLA 프로필에 맞춰 RAN, 전송, 코어 서브넷을 동적 조립하고 NSSF가 가입자별 적합 슬라이스를 접속 선택하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **슬라이스 선택 정책(Slice Selection Policy)**: 단말의 서비스 요청 정보(S-NSSAI), 가입자 프로필 및 네트워크 상태에 따라 사용할 슬라이스를 매핑하는 지침이다.
- **도메인 자원 배치(Domain Resource Instantiation)**: 무선, 전송, 코어 각 도메인에서 오케스트레이션 명령에 맞춰 실체화된 자원(Subnet Instance)을 할당받는 과정이다.
- **종단 연결 검증(End-to-End Connectivity Verification)**: 영역별로 생성된 슬라이스 서브넷 간의 가상 패킷 연결성 및 자원 격리 성능을 사전 테스팅하는 절차이다.

</details>

```text
1. SLA 및 서비스 프로필 요구 입력 (Service SLA Input)
      │
      v
2. 영역별 슬라이스 서브넷 자원 인스턴스화 (RAN/Transport/Core Instantiation)
      │
      v
3. 엔드투엔드 바인딩 및 연결성 검증 (E2E Connectivity & Isolation Verification)
      │
      ├─ 검증 실패 ---- 자원 재할당 및 파라미터 보정
      └─ 검증 성공
          │
          v
4. NSSF에 S-NSSAI 선택 정책 등록 (NSSF Policy Provisioning)
          │
          v
5. PDU 세션 확립 및 전용 UPF 패킷 라우팅 경로 설정 (Session & UPF Setup)
          │
          v
슬라이스 활성화 및 실시간 SLI 모니터링
```

### 동작 원리

1. **SLA 요구사항 수용**: 고객의 서비스 요구사항(전송속도, 지연, 격리성)을 서비스 프로필로 변환하여 오케스트레이터(NSMF)에 전달한다.
2. **영역별 서브넷 자원 할당**: RAN, 전송, 코어 서브넷 오케스트레이터(NSSMF)가 기지국 PRB, 전송 채널(FlexE), 가상 NF(VNF/CNF)를 할당한다.
3. **E2E 바인딩 및 격리 검증**: 3개 도메인 자원을 엮어 종단 가상망을 완성하고 패킷 전달 테스트 및 자원 격리성 검증을 수행한다.
4. **NSSF 정책 등록**: 완료된 슬라이스의 식별자(S-NSSAI) 및 해당 슬라이스를 처리할 코어 NF 주소를 NSSF에 등록한다.
5. **세션 개통 및 유저 트래픽 처리**: 단말 접속 시 NSSF가 슬라이스를 지정하면 전용 UPF 경로를 통해 패킷 통신이 활성화된다.

#### 한줄 요약

- SLA 입력부터 서브넷 자원 인스턴스화, E2E 검증, NSSF 정책 등록 및 PDU 세션 경로 설정을 거쳐 슬라이스를 개통하는 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **네트워크 슬라이스(Network Slice)**: 독립된 가상화 네트워크 자원 집합으로, 완전히 분리된 전용 5G 인프라 환경을 의미한다.
- **서비스 품질 제어(Quality of Service Control, QoS Control)**: 동일한 물리 네트워크 채널 내에서 패킷 큐의 우선순위(DSCP, 5QI)를 부여해 품질 차등을 주는 기법이다.

</details>

| 비교 항목 | **5G 네트워크 슬라이싱 (Network Slicing)** | **전통적 서비스 품질 제어 (DiffServ QoS)** |
|:---|:---|:---|
| 자원 격리 수준 | 무선•전송•코어의 논리•물리 자원 분리 | 트래픽 큐잉•패킷 분류 기반 공유 자원 제어 |
| 관리 영역 | End-to-End (무선 렌더링, 프론트홀/백홀, 5GC 전 구간) | 네트워크 일부 링크 또는 IP 전송 백본 구간 한정 |
| 제어 및 관리 체계 | 슬라이스 오케스트레이터 기반 가상망 생성 및 오토스케일링 | 큐 크기, DSCP 태깅 기반 정적 자원 할당 정책 적용 |
| SLA 보장 능력 | 전용 NF•자원 예약과 SLI 기반 검증 | 혼잡 시 공유 자원 경합 가능 |
| 운용 복잡성 | 오케스트레이터 및 S-NSSAI 연동 등 구축/운영 복잡도 높음 | 상대적으로 간단한 큐 설정 및 DSCP 마킹으로 적용 용이 |

> 요약: 전통적 QoS는 공유 자원 큐 조정 방식이나, 네트워크 슬라이싱은 전 구간 자원 완전 격리 전용 가상망 방식.

#### 한줄 요약

- 슬라이싱은 E2E 자원 분리, QoS는 공유 큐 차등화

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **서비스 수준 지표(Service Level Indicator, SLI)**: SLA 보장 여부를 판가름하기 위해 정밀 측정하는 실제 성능 수치(지연시간, 패킷손실률 등)이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 슬라이스 간 자원 침범 | 무선 구간의 동적 자원 공유 | 무선 PRB 예약•격리 정책 적용 | URLLC 지연 변동 완화 |
| 전송망 구간 병목 | 백홀 IP 전송 구간에서 일반 트래픽과 혼재 | FlexE(Flexible Ethernet) 및 SRv6 전송 슬라이싱 | 유선 전송망 구간에서의 자원 격리 및 저지연 확보 |
| SLI 모니터링 미비 | 자원 초과 및 위반 징후 사전 감지 실패 | AI 기반 Closed-loop 오케스트레이션 및 Auto-scaling | 장애 유발 전 사전 자원 확장 및 SLA 지속 유지 |
| 보안 구역 침범 | 공용 슬라이스를 통한 사설 통신 슬라이스 해킹 | 슬라이스별 IPSec 터널링 및 암호화 인증 차단 | 산업용 슬라이스의 완벽한 기밀성 확보 |

#### 한줄 요약

- 무선 PRB 하드 격리, FlexE/SRv6 전송망 격리 및 AI 기반 Closed-loop 오케스트레이션을 통해 실무 네트워크 슬라이싱 품질 제어.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **종단 슬라이스(End-to-End Network Slice, E2E Network Slice)**: 무선 접속망, 유선 전송망, 5G 코어망 전 영역이 유기적으로 연동된 완전한 형태의 가상 네트워크이다.

</details>

- 엄격한 격리는 **슬라이싱**, 우선순위 차등은 **QoS** 선택

#### 한줄 요약

- E2E 가상 자원 오케스트레이션 및 무선/전송/코어 전 구간 완전 자원 격리 체계 구현 필수.
