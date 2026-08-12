---
sidebar:
  order: 58
  label: "058. SDN 컨트롤러와 OpenFlow (SDN Controller & OpenFlow)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "SDN 컨트롤러와 OpenFlow (SDN Controller & OpenFlow)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 58
extra:
  question_no: "058"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 30
  priority_note: "설명형: Controller•OpenFlow 제어 경계"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **소프트웨어 정의 네트워킹(Software-Defined Networking, SDN)**: 네트워크 제어 평면과 전달 데이터 평면을 물리 분리하여 관제하는 기술 구조이다.
- **OpenFlow(OpenFlow Protocol / ONF Standard)**: SDN 컨트롤러와 OpenFlow 스위치 간에 흐름 테이블(Flow Table) 엔트리를 추가, 삭제, 조회하기 위한 사우스바운드 제어 프로토콜이다.
- **SDN 컨트롤러(SDN Controller)**: 전체 네트워크 토폴로지와 노드 상태 정보를 수집하여 최적 포워딩 규칙을 연산·하향 전달하는 중앙 관제 소프트웨어 두뇌이다.

</details>

- 정의/개념: **SDN 컨트롤러와 OpenFlow**는 소프트웨어 정의 네트워킹(SDN) 아키텍처를 구현하는 제어 및 통신 표준으로, 전역 경로와 정책을 중앙에서 연산하는 관제 두뇌(**SDN Controller**)와 이를 스위치 하드웨어에 주입하는 사우스바운드 프로토콜(**OpenFlow**)로 결합된다.
- 배경/필요성: 각 제조사마다 제각각이었던 사가(Proprietary) 스위치 내부 패킷 포워딩 구조를 표준 Match-Action 파이프라인으로 일원화하고, 소프트웨어로 네트워크를 즉각 조율하기 위해 ONF(Open Networking Foundation) 중심으로 정립되었다.

#### 한줄 요약

- 중앙에서 네트워크 전역 경로를 연산하는 SDN 컨트롤러와 이를 스위치 흐름 테이블에 하향 설치하는 OpenFlow 프로토콜 체계.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **Match-Action(Match-Action Pipeline)**: 수신 패킷 헤더(L2~L4 필드)가 흐름 규칙 매칭 조건(Match)과 일치 시 지정된 액션(Forward, Drop, Modify)을 실행하는 제어 기법이다.
- **Group·Meter 테이블(Group & Meter Table)**: 다중 경로 라우팅/미러링/페일오버를 관장하는 Group 테이블과 트래픽 대역폭 속도 제한(QoS)을 관장하는 Meter 테이블의 연동 구조이다.
- **Table-Miss(Table-Miss Flow Entry)**: 수신 패킷과 매칭되는 규칙이 스위치 흐름 테이블에 존재하지 않을 때 컨트롤러에 처리를 수용 요청하는 예외 상황이다.

</details>

- **Match-Action 12+ 필드 파이프라인**: MAC 주소, IP 주소, TCP/UDP 포트 번호 등 L2~L4 패킷 헤더 필드를 다계층 파이프라인으로 매칭하여 처리 액션을 수행한다.
- **Table-Miss 처리 및 동적 제어**: 스위치에 매칭 규칙이 없을 때 Packet-In 메시지를 컨트롤러에 보내 최적 라우팅 규칙을 유연 수신(Flow-Mod)한다.
- **Group 및 Meter 테이블 확장성**: 단순 단일 포트 포워딩을 넘어 엠캐스트/로드밸런싱(Group) 및 패킷 속도 제한 및 마킹(Meter) 기능을 동시 구동한다.

#### 한줄 요약

- 12개 필드 기반 Match-Action 파이프라인, Table-Miss 시 Packet-In 동적 수용, Group/Meter 연동 트래픽 제어 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **OpenFlow 채널(OpenFlow Channel / TLS Connection)**: SDN 컨트롤러와 OpenFlow 스위치 간의 암호화(TLS/TCP 6653 포트) 제어 메시지 교환 통로이다.
- **데이터 경로(Data Path / OpenFlow Pipeline)**: 스위치 내부의 흐름 테이블(Flow Table) 파이프라인을 거쳐 패킷을 실제 물리 포트로 전송하는 데이터 포워딩 영역이다.

</details>

```text
SDN 컨트롤러 및 OpenFlow 파이프라인 아키텍처
├─ 제어 평면 도메인 (Control Plane - Controller Cluster)
│  ├─ 전역 라우팅 연산 모듈 (Global Topology & Path Engine)
│  └─ OpenFlow 제어 채널 (Secure OpenFlow Channel - TLS/TCP 6653)
└─ 데이터 평면 도메인 (Data Plane - OpenFlow Switch)
   ├─ 흐름 테이블파이프라인 (Flow Tables - Table 0 ~ N)
   ├─ 그룹 및 미터 테이블 (Group Table & Meter Table)
   └─ 하드웨어 포워딩 엔진 (Bare-metal Switch TCAM)
```

선의 의미: SDN 컨트롤러가 TLS 보안 채널을 통하여 OpenFlow 스위치 내부의 흐름 테이블, 그룹 테이블, 미터 테이블에 규칙을 하향 주입하는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| SDN 컨트롤러 (Controller) | NBI 정책을 수용하여 최적 패킷 경로를 계산하고 OpenFlow Flow-Mod 메시지로 스위치를 제어 |
| OpenFlow 제어 채널 | TLS/TCP 6653 포트를 이용해 컨트롤러와 스위치 간 메시지(Packet-In, Flow-Mod, Echo)를 보안 수송 |
| 흐름 테이블 (Flow Table 0~N) | Match Fields, Priority, Counters, Instructions, Timeouts 엔트리를 보관하고 다단계 파이프라인 연산 |
| 그룹 테이블 (Group Table) | All(다중 방송), Select(로드밸런싱), Fast Failover(장애 우회) 등 복잡한 그룹 포워딩 액션 처리 |
| 미터 테이블 (Meter Table) | QoS 트래픽 제한을 위해 수신 패킷 전송 속도(Rate)를 측정하고 한도 초과 시 Drop 또는 DSCP Remarking |

#### 한줄 요약

- SDN 컨트롤러가 안전한 OpenFlow 채널(TLS)을 통해 스위치의 흐름/그룹/미터 테이블(TCAM)에 패킷 처리 규칙을 하향 설치하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **Packet-In(Packet-In Control Message)**: 스위치 흐름 테이블에 일치하는 매칭 엔트리가 없을 때(Table-Miss) 패킷의 헤더 및 입력 포트 정보를 컨트롤러로 보내는 회신 메시지이다.
- **Flow-Mod(Flow Modification Message / Flow-Mod)**: 컨트롤러가 스위치 흐름 테이블에 규칙을 추가(ADD), 수정(MODIFY), 삭제(DELETE)하도록 지시하는 하향 제어 메시지이다.

</details>

```text
1. 스위치 포트로 패킷 수신 및 흐름 테이블 매칭 (Packet Arrival)
      │
      ├─ 흐름 테이블 매칭 성공 ── 4. 지정 액션(Forward / Modify) 고속 실행
      │
      └─ Table-Miss 발생 (매칭 실패)
            │
            v
      2. 스위치 -> 컨트롤러: Packet-In 메시지 송신 (Packet-In Alert)
            │
            v
      3. 컨트롤러: 전역 경로 연산 후 Flow-Mod 규칙 하향 주입 (Flow-Mod Push)
            │
            v
      5. 스위치 TCAM 규칙 저장 및 수신 패킷 수용 전송 (Packet Out)
```

### 동작 원리

1. **패킷 수신 및 매칭 검색**: 스위치 포트로 들어온 수신 패킷이 Flow Table 0번부터 순차적으로 Match 필드를 검사한다.
2. **Table-Miss 발생**: 흐름 테이블에 일치하는 규칙이 없는 경우 Table-Miss 엔트리에 따라 해당 패킷 정보를 캡슐화한다.
3. **Packet-In 질의 송신**: OpenFlow 채널을 통해 컨트롤러로 Packet-In 메시지를 보내 처리 경로 배정을 요청한다.
4. **컨트롤러 연산 및 Flow-Mod 배포**: 컨트롤러가 토폴로지를 기반으로 최적 경로를 산출하고 Flow-Mod 메시지를 스위치에 주입(Push)한다.
5. **TCAM 저장 및 고속 포워딩**: 스위치가 주입된 흐름 규칙을 TCAM에 보관하고 첫 패킷(Packet-Out) 전송 후, 이후 연속 수신 패킷을 0ms로 하드웨어 포워딩한다.

#### 한줄 요약

- 패킷 수신, Table-Miss 발생, Packet-In 송신, 컨트롤러 Flow-Mod 주입 및 TCAM 저장 후 패킷 포워딩 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **반응형 제어(Reactive Flow Setup / Dynamic Setup)**: 미지 패킷이 올 때마다 Packet-In으로 컨트롤러에 질의하여 동적으로 규칙을 주입받는 제어 방식이다.
- **선제형 제어(Proactive Flow Setup / Static Setup)**: 트래픽 발생 이전에 컨트롤러가 예상 경로 규칙을 스위치에 미리 일괄 정적으로 주입해 두는 제어 방식이다.
- **삼진 내용 주소화 메모리(Ternary Content-Addressable Memory, TCAM)**: 0, 1, Don't Care(*) 3가지 상태를 병렬 탐색해 마스크 매칭 포워딩을 구현하는 스위치 메모리이다.

</details>

| 비교 항목 | **반응형 제어 (Reactive Mode)** | **선제형 제어 (Proactive Mode)** |
|:---|:---|:---|
| 규칙 주입 시점 | Table-Miss 및 Packet-In 발생 직후 동적 주입 | 서비스 개통 시 컨트롤러가 사전에 일괄 정적 주입 |
| 첫 패킷 전송 지연 | 발생 (컨트롤러 왕복 딜레이로 10~50ms 지연) | 없음 (스위치 TCAM에 이미 규칙 존재하여 0ms) |
| 스위치 TCAM 사용량 | 매우 적음 (필요한 활성 흐름 규칙만 최소 유지) | 큼 (발생 가능한 모든 소스-디바이스 규칙 점유) |
| 컨트롤러 부하 | 큼 (미지 패킷 접속 시마다 Packet-In 처리 과부하) | 매우 적음 (평시 스위치 질의 메시지 없음) |
| 적합 네트워크 환경 | 사용자 접속이 유동적이고 단기 세션 위주 환경 | 데이터센터 코어망 및 정적 백본 트래픽 환경 |

> 요약: 반응형은 첫 패킷 지연이 발생하나 TCAM을 절약하고, 선제형은 초기 지연이 없고 컨트롤러 부하가 적으나 TCAM 사용량이 큼.

#### 한줄 요약

- 반응형은 첫 패킷 지연이 발생하나 TCAM을 절약하고, 선제형은 초기 지연이 없고 컨트롤러 부하가 적으나 TCAM 사용량이 큼.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **유휴 제한 시간(Idle Timeout / Hard Timeout)**: 스위치 TCAM의 메모리 고갈을 막기 위해 지정 시간 동안 일치 패킷이 없거나(Idle) 일정 시간(Hard)이 지나면 엔트리를 자동으로 파기하는 기술이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| Packet-In 폭주 (DoS) | 공격용 미지 IP 무한 발송으로 Table-Miss 폭주 | OpenFlow Packet-In Rate Limiting 및 Drop 규칙 적용 | 컨트롤러 제어면 마비 및 CPU 과부하 차단 |
| TCAM 메모리 고갈 | 과도한 Proactive 규칙 주입으로 스위치 TCAM 마비 | Idle Timeout 및 Hard Timeout 최적 파기 설정 | TCAM 메모리 효율화 및 신규 규칙 수용 공간 확보 |
| Flow-Mod 주입 지연 | OpenFlow 제어 채널 대역폭 부족으로 규칙 주입 지연 | OpenFlow 채널 QoS 보장 및 TLS 가속 모듈 적용 | 하향 규칙 주입 시간 1ms 대 축소 |
| 컨트롤러 채널 끊김 | 스위치와 컨트롤러 간 OpenFlow 채널 접속 단락 | Standalone 모드 전환 (전통적 L2/L3 포워딩) | 채널 단락 시에도 패킷 완전 폐기 예방 |

#### 한줄 요약

- 하이브리드(선제형+반응형) 규칙 설치, Idle/Hard Timeout 최적화, Packet-In Rate Limiting을 통해 OpenFlow 네트워크 성능 최적화.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **규칙 설치 전략(Hybrid Flow Rule Installation Strategy)**: 대용량 코어 트래픽은 선제형(Proactive)으로 주입하고 예외 트래픽은 반응형(Reactive)으로 조합하는 모범 구축 방식이다.

</details>

- 차세대 SDN 스위칭망 구축 시 **하이브리드 Flow 설치 전략 채택**, **TCAM 메모리 타임아웃 최적화**, **OpenFlow/P4 사우스바운드 보안 채널 구축 필수**.

#### 한줄 요약

- 하이브리드 흐름 규칙 주입 전략 및 TCAM 타임아웃 최적화를 통한 OpenFlow 기반 SDN 제어망 구현 필수.
