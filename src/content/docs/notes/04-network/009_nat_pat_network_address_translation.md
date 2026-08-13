---
sidebar:
  order: 9
  label: "009. 네트워크•포트 주소 변환 (NAT•PAT)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "네트워크•포트 주소 변환 (NAT•PAT)"
date: "2026-08-13T16:19:00+09:00"
tags:
  - "notes-network"
weight: 9
extra:
  question_no: "009"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "비교•설계형: NAT/PAT 주소 절감•추적 한계"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **네트워크 주소 변환(Network Address Translation, NAT)**: 사설 IP 주소를 가진 내부 단말이 외부 인터넷망과 통신할 수 있도록 라우터/방화벽 경계에서 공인 IP 주소로 상호 변환해주는 기술.
- **포트 주소 변환(Port Address Translation, PAT / NAT Overload)**: 단일 공인 IP 주소의 L4 포트 번호(Port Number)를 다르게 식별하여 다수의 사설 IP 단말이 공인 IP 1개를 공유(N:1)할 수 있도록 주소와 포트를 동시 변환하는 기술.
- **인터넷 프로토콜(Internet Protocol, IP)**: 패킷 포워딩 및 논리적 호스트 주소 지정을 수행하는 네트워크 계층 표준.
- **IPv4(Internet Protocol version 4)**: 32비트 주소 체계를 사용하며 주소 부족 이슈를 겪고 있는 4세대 인터넷 프로토콜.

</details>

- 정의/개념: 사설 주소를 공인 주소•포트로 바꾸는 **NAT•PAT**
- 배경/필요성: 32비트 IPv4로는 증가하는 **공인 주소 수용 불가**

#### 한줄 요약

- 사설•공인 주소와 포트의 다대일 변환

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **상태 기반 NAT(Stateful NAT)**: 패킷의 5-Tuple(프로토콜, 출발지/목적지 IP, 출발지/목적지 Port) 정보를 변환 테이블에 세션 상태로 보관하여 수신 응답 패킷을 역변환 처리하는 메커니즘.
- **변환 테이블(Translation Table / NAT Table)**: 경계 장비 메모리상에 유지되는 변환 전/후 사설 IP, 공인 IP, L4 포트 및 세션 타임아웃 상태 정보표.

</details>

- **상태 기반 NAT(Stateful NAT)** 동작을 통해 내부에서 시작된 트래픽의 응답 패킷만 안전하게 수신 역변환 처리.
- **포트 주소 변환(PAT)** 메커니즘으로 공인 IP 1개당 최대 64,000여 개의 L4 소켓(Port)을 매핑하여 공인 주소 자원 절감 극대화.
- 동적 세션 만료 타이머(Timeout)를 가진 **변환 테이블(NAT Table)**을 내장하여 정합성 및 보안 격리성 확보.

#### 한줄 요약

- 상태 기반 변환표의 5-튜플 바인딩


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **사설 IP 주소(Private IP Address)**: 공공 인터넷 라우팅이 불가능한 사내/내부 전용 주소 대역 (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
- **공인 IP 주소(Public IP Address)**: ICANN/KISA 등 주소 할당 기관으로부터 정식 부여받아 인터넷 전역 라우팅이 가능한 주소.
- **주소 풀(Address Pool)**: Dynamic NAT/PAT 구동 시 경계 장비가 변환할 공인 IP 주소들의 모음 블록.

</details>

```text
[ Private Network ]                                       [ Public Internet ]
(192.168.1.10:50001)                                      (203.0.113.50:80)
         \
          \ [ Outbound Packet ]
           v
  +----------------------------------------------------+
  |  NAT/PAT Gateway Device                            |
  |  - Private IP:Port -> Public IP:Port (PAT Table)   |
  |  - Header IP/Port Rewrite & L3/L4 Checksum Recalc  |
  +----------------------------------------------------+
           |
           v [ Transformed Packet ]
(203.0.113.1:10001) -------------------------------------> (203.0.113.50:80)
```

*내부 사설 5-Tuple을 공인 5-Tuple로 변환하고 체크섬을 재계산하는 경계 변환 아키텍처.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| **사설 IP 주소 (Private IP)** | 호스트 내부망 식별 (RFC 1918 주소 체계) | 인터넷 직접 통신 불가 |
| **공인 IP 주소 (Public IP)** | 인터넷 전역 라우팅 가능 대표 주소 | **주소 풀(Address Pool)**에서 동적 할당 |
| **변환 테이블 (NAT Table)** | [내부 IP:Port] <-> [공인 IP:Port] 바인딩 및 세션 타임아웃 유지 | 메모리(TCAM/DRAM) 점유 |
| **L3/L4 체크섬 재계산** | 헤더 내 IP/Port 변경에 따른 Checksum 필드 보정 | 패킷 훼손 오탐 방지 |

#### 한줄 요약

- 경계 장비에서 사설•공인 5-튜플 변환

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **5-튜플(5-Tuple)**: 패킷의 프로토콜, 출발지 IP, 출발지 Port, 목적지 IP, 목적지 Port 5가지 요소로 구성된 단일 연결 식별 단위.
- **체크섬 갱신(Checksum Recalculation)**: NAT 장비가 IP 헤더 및 TCP/UDP 헤더의 주소/포트를 변경한 후 L3/L4 무결성 검증용 체크섬을 재산출하는 작업.
- **송신 튜플 변환(Outbound Tuple Translation)**: 내부 사설 망에서 외부로 향하는 패킷의 출발지 IP/Port를 공인 IP/Port로 변환하고 상태표에 기록하는 과정.
- **수신 튜플 복원(Inbound Tuple Restoration)**: 외부로부터 도착한 응답 패킷의 목적지 공인 IP/Port를 변환 상태표를 조회하여 원래 사설 IP/Port로 복원하는 과정.

</details>

```text
[ 송신 패킷 (Inbound -> Outbound) ]
  Src: 192.168.1.100:52100 / Dst: 8.8.8.8:53
                     |
                     v
  [ 1. NAT Table Lookup & PAT Assignment ]
   -> 공인 IP (203.0.113.1) 및 가용 Port (10050) 바인딩 세션 생성
                     |
                     v
  [ 2. 송신 튜플 변환 & Checksum 갱신 ]
   -> Src: 203.0.113.1:10050 / Dst: 8.8.8.8:53 으로 헤더 Rewrite 후 전송
                     |
                     | (외부 서버 응답 도달)
                     v
  [ 3. 수신 튜플 복원 (Inbound Tuple Restoration) ]
   -> Dst: 203.0.113.1:10050 패킷 도착 시 NAT Table 역조회
   -> Dst: 192.168.1.100:52100 로 변환 및 내부 단말 전달
```

### 동작 원리

1. **NAT Table Lookup & PAT Assignment**: 공인 주소•포트 할당
2. **송신 튜플 변환 & Checksum 갱신**: 헤더 변환 후 송출
3. **수신 튜플 복원**: 변환표 역조회 후 내부 주소 복원

#### 한줄 요약

- 송신 튜플 변환과 수신 튜플 역복원

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **정적 NAT(Static NAT)**: 사설 IP 주소와 공인 IP 주소를 1:1로 고정 매핑하는 방식.
- **동적 NAT(Dynamic NAT)**: 여러 사설 IP 주소가 다수의 공인 IP 주소 풀(Pool)에서 미사용 주소를 선점하여 1:1로 임시 매핑하는 방식.

</details>

| 분류 | **정적 NAT (Static NAT)** | **동적 NAT (Dynamic NAT)** | **포트 주소 변환 (PAT / Overload)** |
|:---|:---|:---|:---|
| 매핑 비율 | 1 : 1 (고정) | N : M (임시 1:1) | N : 1 (포트 기반 다대일) |
| 주 활용 대상 | 내부 웹/DB 서버 외부 서비스 노출 | 동시 접속 호스트 수가 제한된 환경 | 일반 Enterprise 사내망 호스트 전체 |
| 주요 특징 | 외부에서 내부 서버로 직접 inbound 접근 가능 | 공인 주소 풀 고갈 시 추가 접속 불가 | 단일 공인 IP로 대규모 사설 호스트 수용 |
| 보안성/효율성 | 노출 위험 높음 / 공인 IP 전용 점유 | 중간 / 공인 IP 자원 낭비 | 높음 (외부 직접 접속 불가) / 자원 극대화 |

> 요약: 외부 연동 서버용 1:1 정적 NAT와 내부 단말 자원 절감용 N:1 PAT의 역할 분담.

#### 한줄 요약

- 서버는 정적 NAT, 다수 단말은 PAT 적용

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **포트 포워딩(Port Forwarding)**: PAT 환경에서 외부 특정 포트(예: 8080)로 유입되는 연결 요청을 내부의 특정 사설 IP:Port로 전달하도록 정적으로 개방해 주는 기법.
- **응용 계층 게이트웨이(Application Layer Gateway, ALG)**: FTP, SIP, H.323 등 패킷 페이로드(Payload) 내부에 IP/Port 정보가 포함된 프로토콜을 인지하여 페이로드 주소까지 보정 변환해주는 기능.
- **변환 매핑 로그(Translation Mapping Log / NAT Log)**: 공인 IP/Port를 공유한 사설 IP 사용자의 접속 이력(시각, 5-Tuple 매핑)을 추적하기 위해 저장하는 로그.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| PAT Port 고갈 (Port Exhaustion) | 대규모 호스트가 동시 다량 세션(예: P2P) 형성 시 64k 포트 매진 | 공인 IP 주소 풀 추가 배정 및 NAT Session Timeout 튜닝 | PAT 접속 단절 장애 예방 |
| 복합 응용 통신 실패 | FTP Active Mode 또는 VoIP SIP 페이로드 내 사설 IP 포함 | 해당 프로토콜용 **응용 계층 게이트웨이(ALG)** 활성화 | 응용 페이로드 주소 자동 보정 |
| 침해 사고 시 사용자 추적 불가 | PAT로 인해 외부에는 동일한 공인 IP만 노출됨 | **변환 매핑 로그(NAT Log)** 중앙 Syslog/SIEM 수집 체계 구축 | 공인 IP 기반 내부 접속자 정밀 추적 |
| 외부에서 내부 서버 접속 불가 | PAT는 외부발 신규 세션을 차단함 | 특정 서비스 포트에 대한 **포트 포워딩(Port Forwarding)** 설정 | 사설 서버 외부 공개 수용 |

#### 한줄 요약

- 포트 포워딩•ALG•변환 로그로 운영 위험 통제

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **NAT 방식 선택(NAT Strategy Selection)**: 서비스 도달성(Inbound) 필요 유무와 내부 호스트 수 및 보안 요건을 고려하여 Static NAT, Dynamic NAT, PAT 중 최적을 결정하는 아키텍처 수립.

</details>

- 외부 공개 서버는 **정적 NAT**, 내부 단말은 **PAT** 선택

#### 한줄 요약

- 외부 도달성과 단말 수에 따라 NAT 방식 결정
