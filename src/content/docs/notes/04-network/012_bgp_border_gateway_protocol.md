---
sidebar:
  order: 12
  label: "012. 경계 게이트웨이 프로토콜: BGP (Border Gateway Protocol)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "경계 게이트웨이 프로토콜: BGP (Border Gateway Protocol)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 12
extra:
  question_no: "012"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "자율 시스템 간 정책 기반 경로 벡터 라우팅"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **경계 게이트웨이 프로토콜(Border Gateway Protocol, BGP)**: 서로 다른 자율 시스템(AS) 간에 네트워크 도달 가능성 정보(NLRI)와 경로 속성(Path Attributes)을 교환하는 사실상의 표준 외부 라우팅 프로토콜(EGP).
- **자율 시스템(Autonomous System, AS)**: 동일한 단일 라우팅 정책과 관리 주체(ISP, 기업 등) 아래 운영되는 라우터들의 집합으로, 고유의 ASN(AS Number)을 부여받음.
- **네트워크 계층 도달 가능성 정보(Network Layer Reachability Information, NLRI)**: BGP 라우팅 업데이트 메시지에 포함되어 특정 IP 프리픽스(Prefix)와 서브넷 마스크의 도달 가능성을 전달하는 데이터.

</details>

- 정의/개념: 대규모 인터넷 환경에서 자율 시스템(AS) 간에 정책 기반의 경로 벡터(Path Vector) 알고리즘을 사용하여 IP 프리픽스 도달성을 교환하는 **외부 게이트웨이 프로토콜(EGP)**
- 배경/필요성: 단순 최단 홉(RIP) 또는 링크 비용(OSPF) 기반 라우팅의 한계를 극복하고, ISP 간의 상호 접속 계약, 트래픽 엔지니어링 및 보안 정책을 반영한 경로 제어 요구

#### 한줄 요약
- 자율 시스템(AS) 간에 정책 속성을 기반으로 IP 도달성 정보를 교환하는 경로 벡터 라우팅 프로토콜이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **AS 경로 속성(AS_PATH)**: 특정 경로가 통과해 온 자율 시스템들의 일련번호 목록으로, 라우팅 루프 방지와 최선 경로 선택의 핵심 척도로 사용.
- **증분 갱신(Incremental Update)**: 전체 라우팅 테이블을 주기적으로 재전송하지 않고, 토폴로지 변경 시 수정 및 철회(Withdraw)된 프리픽스 정보만 선별 전송하는 방식.

</details>

- 신뢰성 있는 세션 유지를 위해 **TCP 포트 179번** 기반으로 피어링(Peering) 및 킵얼라이브(Keepalive) 세션 수립
- **AS_PATH** 속성에 자신의 AS 번호가 포함되어 있을 경우 해당 경로를 즉시 폐기하여 **라우팅 루프 원천 차단**
- 전체 테이블 대신 변경된 정보만 전송하는 **증분 갱신(Incremental Update)** 과 소프트 리셋(Soft Reconfiguration) 지원

#### 한줄 요약
- TCP 179 포트 기반의 안정적 피어링을 유지하며, AS_PATH를 통해 루프를 방지하고 증분 갱신을 수행한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BGP 피어(BGP Peer / Neighbor)**: TCP 179번 포트를 통해 연결되어 라우팅 정보를 상호 교환하는 인접 BGP 라우터.
- **최선 경로 선택(Best Path Selection Algorithm)**: Weight $\rightarrow$ Local Preference $\rightarrow$ AS_PATH $\rightarrow$ Origin $\rightarrow$ MED 등의 우선순위 규칙에 따라 단 하나의 최적 경로를 결정하는 알고리즘.

</details>

```text
[ BGP Peer A (AS 100) ] <─── TCP 179 세션 ───> [ BGP Peer B (AS 200) ]
           │
           ├─ 1. 인바운드 정책 (Inbound Policy / Prefix Filter)
           │
           ├─ 2. BGP 테이블 (Adj-RIB-In ➔ Loc-RIB 적재)
           │
           ├─ 3. 최선 경로 알고리즘 (Best Path Selection)
           │
           ├─ 4. 아웃바운드 정책 (Outbound Policy / Route Map)
           │
           ▼
[ 포워딩 테이블 (FIB) 및 인접 라우터 광고 (Adj-RIB-Out) ]
```

선의 의미: 인접 BGP 피어 간 세션 수립 후 인바운드 필터, RIB 테이블, 최선 경로 산출, 아웃바운드 광고로 전이되는 구조

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **BGP 피어(Neighbor)** | TCP 179 포트를 통해 BGP 상태 머신(Idle $\rightarrow$ Established)을 유지하고 메시지 교환 | 킵얼라이브 주기 검증 |
| **경로 속성(Path Attributes)** | 경로의 선호도와 제약 조건을 명시하는 메타데이터 (Well-known, Optional) | Weight, Local_Pref, MED 등 |
| **인바운드 정책(Inbound Filter)** | 유입된 라우팅 정보 중 비인가 프리픽스 차단 및 속성 조작(Local_Pref 할당) | 유출 트래픽 경로 제어 |
| **최선 경로 선정기** | 10단계 이상의 정형화된 BGP Best Path 알고리즘을 통해 최적 경로 1개 선출 | Loc-RIB 적재 |
| **아웃바운드 정책(Outbound Filter)** | 선출된 최선 경로를 인접 피어에 광고할지 여부 통제 및 AS_PATH Prepend 수행 | 유입 트래픽 유도 제어 |

#### 한줄 요약
- 인바운드 필터링, 최선 경로 산출, 아웃바운드 광고 정책을 통해 트래픽 경로를 정밀 제어한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **라우팅 정보 베이스(RIB)**: 수신된 원시 경로(Adj-RIB-In), 최선 경로(Loc-RIB), 송신 대상 경로(Adj-RIB-Out)로 구분 관리되는 BGP 전용 라우팅 데이터베이스.

</details>

```text
1. BGP UPDATE 메시지 수신 (신규 프리픽스 NLRI 또는 철회 정보)
            │
            ▼
2. 인바운드 필터링 및 속성 부여: Prefix-list 검증 및 Local Preference 설정
            │
            ▼
3. Adj-RIB-In 저장 및 Loc-RIB 최선 경로(Best Path) 산출
            │
            ▼
4. 최선 경로를 라우팅 테이블(RIB/FIB)에 주입하여 실제 포워딩 반영
            │
            ▼
5. 아웃바운드 정책 적용 후 인접 피어로 BGP UPDATE 광고 전파
```

**동작 원리**

1. **메시지 수신**: BGP 피어로부터 TCP 세션을 통해 UPDATE 메시지(NLRI 및 경로 속성) 수신
2. **수신 정책 검증**: RPKI 유효성 검사 및 인바운드 Prefix-list를 적용하여 불량 경로 필터링 및 Local_Pref 설정
3. **최선 경로 결정**: BGP 의사결정 프로세스를 수행하여 동일 프리픽스에 대한 최적 경로 1개를 Loc-RIB에 등록
4. **FIB 적재**: 선정된 최선 경로를 라우팅 엔진의 메인 라우팅 테이블 및 하드웨어 FIB에 반영
5. **광고 정책 적용**: 아웃바운드 정책 및 AS_PATH 조작(Prepend)을 거쳐 eBGP/iBGP 이웃에게 재전파

#### 한줄 요약
- UPDATE 패킷 수신 후 인바운드 검증, 최선 경로 산출, FIB 적재, 아웃바운드 광고 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **eBGP(External BGP)**: 서로 다른 AS 번호를 가진 라우터 간에 체결되는 외부 BGP 세션.
- **iBGP(Internal BGP)**: 동일한 AS 내부에서 외부 라우팅 정보를 동기화하기 위해 체결되는 내부 BGP 세션.
- **경로 반사기(Route Reflector, RR)**: iBGP의 풀 메시(Full-mesh) 요구사항을 완화하기 위해 중앙에서 라우팅 정보를 중계해 주는 전용 라우터.

</details>

| 비교 항목 | eBGP (External BGP) | iBGP (Internal BGP) |
|:---|:---|:---|
| **세션 연결 대상** | 서로 **다른 AS**에 속한 라우터 간 연결 | 동일한 **단일 AS** 내부 라우터 간 연결 |
| **AS_PATH 갱신** | 광고 시 자신의 AS 번호를 **AS_PATH에 추가(Prepend)** | AS 내부 전달 시 **AS_PATH를 변경하지 않고 유지** |
| **루프 방지 메커니즘** | AS_PATH 내 자신의 AS 번호 존재 시 패킷 폐기 | iBGP로 학습한 경로는 타 iBGP 피어에 **재광고 금지(Split Horizon)** |
| **토폴로지 확장성** | 일반적으로 직접 연결(Directly Connected) 인터페이스 사용 | 풀 메시(Full-mesh) 필요 ➔ **경로 반사기(RR)** 또는 연합(Confederation) 적용 |

#### 한줄 요약
- 이기종 AS 간 연동에는 eBGP를 적용하고, AS 내부 경로 동기화에는 iBGP와 경로 반사기(RR)를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **RPKI(Resource Public Key Infrastructure)**: IP 주소 프리픽스 소유권과 허가된 ASN의 매핑(ROA)을 암호학적으로 서명하여 BGP 하이재킹을 방어하는 보안 프레임워크.
- **BGP 하이재킹(BGP Hijacking)**: 공격자가 타 기관의 IP 프리픽스를 자신이 소유한 것처럼 허위 광고하여 트래픽을 가로채거나 서비스를 마비시키는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 AS의 허위 프리픽스 광고로 인한 **BGP 하이재킹** | **RPKI 기반 ROA(Route Origin Authorization) 유효성 검증** 의무화 | 비인가 경로 광고(Invalid) 즉각 폐기 및 트래픽 탈취 차단 |
| 수신된 경로를 타 피어에 무단 재광고하는 **경로 유출(Route Leak)** | 명시적 **커뮤니티(Community) 필터링** 및 고객/피어별 인바운드 통제 | 비의도적 중계(Transit) 트래픽 발생 및 회선 과부하 예방 |
| 다중 회선 환경에서 특정 아웃바운드 링크로의 트래픽 편중 | 정책 기반 **Local_Preference 속성 튜닝** 및 BGP 멀티패스 활성화 | 아웃바운드 트래픽 분산 및 회선 대역폭 최적화 |

#### 한줄 요약
- RPKI 검증으로 하이재킹을 방어하고, 커뮤니티 필터로 경로 유출을 막으며, Local_Preference로 트래픽을 분산한다.

## Ⅶ. 결론

- 글로벌 라우팅의 안정성과 확장성을 확보하기 위해 **BGP** 기반의 정책 라우팅을 기본으로 운용하되, 경로 하이재킹 및 비정상 유출 사고를 방지하기 위해 **RPKI(ROA)** 유효성 검증과 철저한 인바운드/아웃바운드 **Prefix-list** 필터링 거버넌스를 결합하여 안전한 대외 연동망을 구축

#### 한줄 요약
- 정책 기반 경로 제어와 RPKI 보안 검증을 통해 신뢰성 있는 대규모 인터넷 연동망을 실현한다.
