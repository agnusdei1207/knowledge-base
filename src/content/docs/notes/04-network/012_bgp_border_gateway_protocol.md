---
sidebar:
  order: 12
  label: "012. BGP 라우팅 프로토콜"
  badge:
    text: "미출 · 50%"
    variant: note
title: "경계 게이트웨이 프로토콜: BGP (Border Gateway Protocol)"
date: "2026-08-26T13:37:26+09:00"
tags:
  - "notes-network"
weight: 12
extra:
  question_no: "12"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "자율 시스템 간 정책 기반 경로 벡터 라우팅"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **BGP (Border Gateway Protocol)**: 전 세계 인터넷 자율 시스템(AS) 간에 경로 벡터(Path-Vector) 알고리즘으로 IP 도달성(NLRI)을 교환하는 표준 EGP 프로토콜.
- **Autonomous System (AS, 자율 시스템)**: 단일 관리 주체(ISP, 글로벌 기업)에 의해 통일된 라우팅 정책으로 운영되는 라우터들의 집합(ASN 부여).

</details>

- 정의/개념: 인터넷 자율 시스템(AS) 간에 **경로 벡터(Path-Vector) 알고리즘과 다양한 경로 속성을 기반으로 패킷 전달 경로를 결정하는 외부 라우팅 프로토콜**
- 배경/필요성: 단순 링크 비용 기반 IGP 알고리즘만으로는 **ISP 간 비즈니스 계약 정책(Policy), 트래픽 엔지니어링 및 AS 간 라우팅 루프 방어 불가**

#### 한줄 요약
- TCP 179 기반의 피어링과 AS_PATH 속성 제어를 통해 인터넷 자율 시스템 간 정책 라우팅을 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Path-Vector Algorithm**: 최단 비용 대신 패킷이 통과해야 할 AS 번호의 나열(AS_PATH)을 전달하여 라우팅 루프를 원천 차단하는 알고리즘.
- **BGP Path Attributes**: Weight, Local Preference, AS_PATH, MED 등 경로의 선호도를 결정하는 정책 속성.

</details>

- 신뢰성 있는 세션 유지를 위해 **TCP 포트 179번** 기반 피어링 및 킵얼라이브 수행
- 경로 정보에 포함된 AS_PATH에 자신의 ASN이 있으면 폐기하여 **라우팅 루프 원천 차단**
- 조직 간 비즈니스 계약과 트래픽 방향을 유연하게 제어하는 **정책 기반 라우팅(Policy Routing)**

#### 한줄 요약
- TCP 179 피어링, AS_PATH 루프 방지, 풍부한 경로 속성 정책 제어를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BGP Best Path Selection**: Weight(높음) $\to$ Local_Pref(높음) $\to$ Local Originated $\to$ AS_PATH(짧음) $\to$ Origin $\to$ MED(낮음) 순으로 단 하나의 최적 경로 선발.

</details>

```text
[BGP 구성]
|-- BGP 피어
|-- 경로 속성
|-- 인바운드 정책 필터
|-- 최선 경로 선정기
`-- 아웃바운드 정책 필터
```

선의 의미: 계층 및 인접 피어로부터 유입된 경로가 인바운드 정책을 거쳐 Loc-RIB에서 최선 경로로 선발된 후 아웃바운드 정책을 통해 재전파되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| BGP 피어 (Neighbor) | TCP 179번 포트를 통해 **피어링을 맺고 Open/Update/Keepalive 메시지 교환** | TCP 179 수신 |
| 경로 속성 (Attributes) | 경로의 선호도와 제약 조건을 명시하는 **메타데이터 (Weight, Local_Pref, AS_PATH, MED)** | 정책 제어 핵심 |
| 인바운드 정책 필터 | 유입된 경로 중 비인가 프리픽스를 차단하고 **Local_Pref를 조작하여 아웃바운드 트래픽 제어** | 유출 경로 제어 |
| 최선 경로 선정기 | 10단계 이상의 정형화된 **BGP 의사결정 프로세스를 통해 프리픽스당 최적 경로 1개 선출** | Loc-RIB 적재 |
| 아웃바운드 정책 필터 | 선출된 최선 경로에 **AS_PATH Prepend를 적용하여 인바운드 유입 트래픽 경로 유도** | 유입 트래픽 제어 |

#### 한줄 요약
- BGP 피어, 경로 속성, 인바운드 필터, 최선 경로 선정기, 아웃바운드 필터가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP 의사결정 5단계**: UPDATE 메시지 수신 $\to$ RPKI/인바운드 필터링 $\to$ Best Path 알고리즘 연산 $\to$ FIB 적재 $\to$ 아웃바운드 정책 재광고.

</details>

```text
BGP 라우팅 업데이트 수신 및 처리
        │
   1. [UPDATE 수신] BGP 피어로부터 TCP 179 세션을 통해 NLRI 및 경로 속성 수신
        │
   2. [인바운드 필터링] RPKI 유효성(Valid) 검증 및 Inbound Route-Map (Local_Pref=200 부여)
        │
   3. [최선 경로 선출] BGP Best Path 알고리즘 가동 -> 최단 AS_PATH 경로를 Loc-RIB에 등록
   ┌────┴───────────────────────────┐
  최적 경로 선발 완료              경로 무효/루프 감지 (AS_PATH에 내 ASN 존재)
   │                                 │
4A. [FIB 하드웨어 주입]             4B. [즉시 경로 폐기 (Drop)]
   메인 라우팅 테이블 및 TCAM FIB 반영     라우팅 루프 방지
   │                                 │
   ▼                                 │
5. [아웃바운드 재전파]               │
   AS_PATH Prepend 적용 후 피어 광고 │
   │                                 │
   └────┬────────────────────────────┘
        ▼
   글로벌 인터넷 AS 간 최적 패킷 포워딩 수행
```

#### 한줄 요약
- UPDATE 수신 → 인바운드 필터링 → 최선 경로 선출 → FIB 주입 → 아웃바운드 재광고 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **eBGP vs iBGP**: 서로 다른 AS 간 외부 라우팅(eBGP)과 동일 AS 내부 라우터 간 외부 경로 동기화(iBGP).

</details>

| 비교 항목 | eBGP (External BGP) | iBGP (Internal BGP) |
|:---|:---|:---|
| 세션 연결 대상 | **서로 다른 ASN에 속한 경계 라우터 간 연결** | **동일한 단일 ASN 내부 라우터 간 연결** |
| AS_PATH 갱신 동작 | 경로 광고 시 **자신의 AS 번호를 AS_PATH에 추가(Prepend)**| AS 내부 전달 시 **AS_PATH를 변경하지 않고 유지** |
| 루프 방지 규칙 | **수신 AS_PATH에 자신의 ASN 존재 시 패킷 폐기** | iBGP로 학습한 경로는 타 iBGP 피어에 **재광고 금지 (Split Horizon)** |
| 토폴로지 확장성 | 일반적으로 직접 연결(Directly Connected) 1홉 | 풀 메시(Full-Mesh) 필요 $\to$ **Route Reflector(RR)로 완화** |

#### 한줄 요약
- AS 간 통신은 eBGP를 적용하고, AS 내부 경로 전파는 iBGP와 Route Reflector(RR)를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RPKI (Resource Public Key Infrastructure)**: IP 주소 소유권과 공인 ASN의 매핑(ROA: Route Origin Authorization)을 암호화 전자서명으로 검증하여 BGP 하이재킹을 차단하는 보안 기술.
- **AS_PATH Prepending**: 인바운드 트래픽을 특정 회선으로 유도하기 위해, 비선호 회선으로 나가는 BGP 광고에 자신의 AS 번호를 중복 추가하여 경로 길이를 인위적으로 늘리는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 AS의 허위 프리픽스 광고로 인한 BGP 하이재킹(탈취) | **`RPKI 기반 ROA(Route Origin Authorization)` 유효성 검증 강제** | 비인가 위조 경로(Invalid) 즉각 폐기 |
| 실수로 수신된 외부 경로를 다른 ISP에 재광고하는 경로 유출 | **명시적 `BGP Community 필터링` 및 고객/피어별 전송 정책 강제** | 비의도적 무료 중계(Transit) 트래픽 차단 |
| 멀티홈(Dual-Homed) 환경에서 인바운드 트래픽의 단일 회선 편중 | **백업 회선으로 나가는 경로에 `AS_PATH Prepending (3회 추가)` 적용** | 외부 유입 트래픽의 메인 회선 집중 유도 |
| 대규모 iBGP 망에서 $N(N-1)/2$ 풀메시 세션 폭증 문제 | **중앙 집중식 `BGP Route Reflector (RR) 이중화 클러스터` 구성** | iBGP 피어링 복잡도 극소화 |

#### 한줄 요약
- RPKI 유효성 검증, 커뮤니티 필터링, AS_PATH Prepend, Route Reflector로 운영한다.

## Ⅶ. 결론

- AS 간 연결은 **eBGP**, 내부 경로 동기화는 **iBGP·RR** 선택

#### 한줄 요약
- BGP는 TCP 179 기반의 경로 벡터 알고리즘과 다양한 속성을 통해 자율 시스템 간 정책 라우팅을 수행하며, RPKI 보안 검증과 결합하여 안전한 인터넷 통신을 보장하는 핵심 기술이다.
