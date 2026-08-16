---
sidebar:
  order: 10
  label: "010. 라우팅 기본: 정적•동적 라우팅 (Routing Static Dynamic)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "라우팅 기본: 정적•동적 라우팅 (Routing Static Dynamic)"
date: "2026-08-13T16:21:00+09:00"
tags:
  - "notes-network"
weight: 10
extra:
  question_no: "010"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "비교형: 정적•동적 경로의 선택 기준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **라우팅(Routing)**: 네트워크 계층(L3)에서 송신 패킷의 목적지 IP 주소를 참조하여 최적의 경로를 탐색하고 다음 홉(Next Hop) 및 출력 인터페이스로 스위칭해주는 제어 과정.
- **인터넷 프로토콜(Internet Protocol, IP)**: 이기종 네트워크 간 패킷 전송과 호스트 지정을 담당하는 논리적 주소 체계 프로토콜.

</details>

- 정의/개념: 목적지 IP의 최적 경로를 선택하는 **라우팅**
- 배경/필요성: 단일 링크 주소만으로는 **다중 네트워크 전달 불가**

#### 한줄 요약

- 목적지별 최적 경로와 다음 홉 선택

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **관리 거리(Administrative Distance, AD)**: 서로 다른 라우팅 프로토콜(예: OSPF, BGP, Static)이 동일 목적지 경로를 알릴 때 신뢰 경로를 결정하는 소스 신뢰도 값(값이 작을수록 우수한 경로).
- **메트릭(Metric)**: 동일 라우팅 프로토콜 내부에서 최적 경로를 산출하기 위해 대역폭(Bandwidth), 지연(Delay), 홉 수(Hop Count), 코스트(Cost) 등을 기준으로 계산한 비용 값.
- **제어 평면(Control Plane)**: 라우팅 프로토콜(OSPF, BGP) 동작, 경로 정보 교환, AD/Metric 연산 및 RIB(Routing Information Base) 생성을 담당하는 소프트웨어 영역.
- **데이터 평면(Data Plane / Forwarding Plane)**: 제어 평면에서 수립된 FIB(Forwarding Information Base)를 바탕으로 실제 패킷을 입출력 인터페이스로 고속 전달하는 하드웨어 ASIC 영역.

</details>

- **관리 거리** 기반 라우팅 출처 간 신뢰 우선순위 결정 (예: Direct(0) > Static(1) > EBGP(20) > OSPF(110) > IBGP(200)).
- 동일 프로토콜 내 **메트릭** 연산을 통한 최소 비용 경로 산출.
- 경로 수집/연산을 담당하는 **제어 평면**과 고속 패킷 스위칭을 담당하는 **데이터 평면**의 완벽한 기능 분리.

#### 한줄 요약

- AD•메트릭 평가와 제어•데이터 평면 분리


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **라우팅 정보 베이스(Routing Information Base, RIB)**: 다양한 경로 출처로부터 수집된 모든 후보 경로 및 상태 정보를 보관하는 제어 평면의 소프트웨어 데이터베이스.
- **포워딩 정보 베이스(Forwarding Information Base, FIB)**: RIB에서 최종 승리한 최적 경로만을 추출하여 라우팅 하드웨어(TCAM/ASIC)에 탑재하는 데이터 평면의 고속 포워딩 표.
- **동일 비용 다중 경로(Equal-Cost Multi-Path, ECMP)**: 동일 목적지에 대해 메트릭 비용이 같은 최적 경로가 복수 존재할 경우 이를 모두 FIB에 등록하여 로드 밸런싱을 수행하는 기술.
- **최장 프리픽스 일치(Longest Prefix Match, LPM)**: FIB 조회 시 서브넷 마스크 비트가 가장 길게 일치하는 세부 경로를 최우선 선택하는 라우팅 검색 규칙.

</details>

```text
[ Route Sources (Static, OSPF, BGP) ]
                  |
                  v
[ Control Plane: RIB (Routing Information Base) ] -- (AD & Metric Evaluation)
                  |
                  v (Best Route Selection)
[ Data Plane: FIB (Forwarding Information Base) ] -- (Hardware TCAM / ASIC)
                  |
                  v (LPM Lookup)
[ Packet Forwarding to Outgoing Interface / Next-Hop ]
```

*제어 평면(RIB)의 AD/Metric 기반 최적 경로 평가 및 데이터 평면(FIB) 설치 구조.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| **관리 거리 ** | 이종 프로토콜 간 우선순위 결정 (Static: 1, OSPF: 110, BGP: 20/200) | AD 값이 낮을수록 우선 선점 |
| **메트릭 ** | 동종 프로토콜 간 최적 경로 산출 (Hop Count, Cost 등) | 프로토콜마다 알고리즘 상이 |
| **RIB (Control Plane)** | 모든 라우팅 소스의 후보 경로 수집 및 최적 경로 판정 DB | CPU/RAM 메모리 자원 사용 |
| **FIB (Data Plane)** | 최적 경로 기반 하드웨어 포워딩 테이블 구축 및 **LPM** 검색 | TCAM 고속 메모리 장착 |
| **ECMP (Load Balancing)** | 동일 Metric 경로에 대한 5-Tuple 기반 분산 | 대역폭 활용성 극대화 |

#### 한줄 요약

- RIB 최적 경로를 FIB에 설치해 LPM 조회

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **다음 홉(Next Hop)**: 목적지 IP로 전달하기 위해 거쳐야 하는 인접 라우터의 IP 주소 또는 출구 포트.
- **후보 경로 수집(Candidate Route Collection)**: 정적 설정(Static Route) 및 동적 프로토콜(OSPF/BGP)로부터 패킷의 목적지 경로 정보를 RIB로 수집하는 절차.
- **최선 경로 선택(Best Route Selection)**: RIB에 수집된 경로 중 AD 값 및 Metric 값을 비교하여 단일/ECMP 최적 경로를 결정하는 절차.
- **FIB 경로 설치(FIB Installation)**: 선발된 최적 경로를 하드웨어 포워딩 엔진(Data Plane)으로 렌더링하는 절차.
- **LPM 경로 조회(LPM Route Lookup)**: 패킷 수신 시 목적지 IP와 FIB 테이블의 서브넷 마스크 비트를 최장 비교하여 Next-Hop을 확정하는 절차.

</details>

```text
[ 정적 설정 & 동적 라우팅 광고 ]
                 |
                 v
[ 1. 후보 경로 수집 (RIB Entry) ] ---> 다양한 라우팅 소스의 경로 수집
                 |
                 v
[ 2. 최선 경로 선택 (Best Route) ] --> ① AD 값 비교 (작은 값 승리)
                 |                     ② AD 동율 시 Metric 비교 (작은 값 승리)
                 v
[ 3. FIB 경로 설치 (FIB Install) ] --> 데이터 평면 TCAM에 최적 경로 등록 (ECMP 포함)
                 |
                 | (패킷 유입)
                 v
[ 4. LPM 경로 조회 (LPM Lookup) ] --> 목적지 IP에 대해 최장 비트 매칭(LPM) 적용 후 Next-Hop 전송
```

### 동작 원리

1. **후보 경로 수집**: 정적•동적 경로를 RIB에 수집
2. **최선 경로 선택**: AD와 메트릭 순으로 경로 판정
3. **FIB 경로 설치**: 선택 경로를 데이터 평면에 등록
4. **LPM 경로 조회**: 최장 프리픽스로 다음 홉 선택

#### 한줄 요약

- AD•메트릭 경로 선택 후 FIB의 LPM 조회

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 라우팅(Static Routing)**: 네트워크 관리자가 목적지 IP 및 Next-Hop 경로를 직접 라우터 장비에 고정 명시하여 설정하는 방식.
- **동적 라우팅(Dynamic Routing)**: 라우팅 프로토콜(OSPF, BGP 등)을 활성화하여 라우터 간에 이웃(Neighbor)을 맺고 경로 정보를 자동 교환 및 갱신하는 방식.
- **수렴(Convergence)**: 네트워크 링크 장애나 토폴로지 변화 발생 시 라우터들이 신규 최적 경로 정보로 라우팅 테이블을 완벽히 재구성 완료하는 상태.

</details>

| 비교 항목 | **정적 라우팅 ** | **동적 라우팅 ** |
|:---|:---|:---|
| 경로 설정 방식 | 관리자가 라우터마다 일일이 수동 CLI 명령어로 입력 | 라우팅 프로토콜(OSPF, BGP)에 의해 경로 자동 생성 |
| 토폴로지 변화 대응 | 링크 장애 시 관리자가 수동 변경할 때까지 대응 불가 | 프로토콜에 의해 자동으로 장애 우회 및 **수렴** |
| 장비 리소스 (CPU/RAM) | overhead 거의 없음 (라우팅 패킷 교환 없음) | 라우팅 헬로/LSA 패킷 교환 및 SPF 알고리즘 연산 부하 발생 |
| 보안성 및 관리 | 경로 노출이 없어 안전함 / 망 규모 증가 시 관리 불가능 | 프로토콜 패킷 암호화 필요 / 대규모 복잡망에 필수적 |

> 요약: 소규모/스텁 망용 정적 라우팅(Static)과 대규모/복잡 망용 동적 라우팅(Dynamic)의 환경별 구분.

#### 한줄 요약

- 소규모는 정적, 변화가 많은 망은 동적 라우팅

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **경로 추적(Route Tracking / Object Tracking)**: 정적 라우팅 설정 시 IP SLA 핑 또는 인접 링크 상태를 지속 추적하여 링크 장애 시 정적 경로를 자동으로 삭제/우회시키는 기술.
- **경로 재분배(Route Redistribution)**: 이종 라우팅 프로토콜 간(예: OSPF <-> BGP, Static -> OSPF) 경로 정보를 상호 변환하여 주입해 주는 설정.
- **비대칭 라우팅(Asymmetric Routing)**: 송신 트래픽이 거치는 경로와 수신 응답 트래픽이 거치는 경로가 서로 다르게 형상되는 네트워크 상태.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| 정적 라우팅 블랙홀 | 회선 장애 시에도 Static Route가 제거되지 않음 | IP SLA 연동 **경로 추적** 적용 | 장애 발생 시 정적 경로 자동 덤프 및 우회 |
| 라우팅 루프 (Redistribution Loop) | 이종 프로토콜 간 양방향 **경로 재분배** 시 경로 재유입 | Route Tagging, Access List 및 AD 조정 | 재분배 무한 루프 예방 |
| **비대칭 라우팅** 방화벽 세션 단절 | 송수신 경로 불일치로 Stateful 방화벽이 ACK 패킷 drop | 라우팅 Metric 튜닝을 통한 대칭 경로 확보 | Stateful 방화벽 세션 정상 유지 |

#### 한줄 요약

- 경로 추적•재분배 필터•대칭 경로로 장애 통제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **기본 경로(Default Route / Default Gateway)**: 라우팅 테이블에 명시적인 특정 서브넷 경로가 존재하지 않을 때 패킷을 포워딩하는 최후의 경로 (`0.0.0.0/0`).
- **라우팅 방식 결정(Routing Strategy Selection)**: 네트워크 규모, 장애 자동 수렴 필요성 및 하드웨어 성능을 다각도로 평가하여 정적/동적 라우팅 혼용 전략을 수립하는 절차.

</details>

- 스텁은 **정적 기본 경로**, 코어는 **동적 라우팅** 적용

#### 한줄 요약

- 규모와 수렴 요구에 따라 정적•동적 경로 선택
