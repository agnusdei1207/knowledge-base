---
sidebar:
  order: 8
  label: "008. 도메인 이름 시스템 (Domain Name System, DNS)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "도메인 이름 시스템 (Domain Name System, DNS)"
date: "2026-08-13T16:17:00+09:00"
tags:
  - "notes-network"
weight: 8
extra:
  question_no: "008"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 50
  priority_note: "설계•운영형: 계층•재귀•Cache•장애 대응"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **도메인 이름 시스템(Domain Name System, DNS)**: 사람이 읽기 쉬운 문자열 도메인 주소(예: www.example.com)를 컴퓨터가 상호 통신할 수 있는 IP 주소로 상호 변환해주는 전 세계 분산 계층형 데이터베이스 시스템.
- **자원 레코드(Resource Record, RR)**: 이름•유형•값•TTL로 구성된 DNS 정보 단위.

</details>

- 정의/개념: 도메인과 자원 레코드를 해석하는 분산 **DNS**
- 배경/필요성: 단일 `hosts.txt`로는 인터넷 규모의 **이름 관리 불가**

#### 한줄 요약

- 계층형 위임으로 도메인과 자원 레코드 분산 관리

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **위임(Delegation)**: 상위 도메인 존(Zone)이 하위 도메인 영역의 관리 권한과 권한 있는 네임서버(NS 레코드) 정보를 분산 이관하는 메커니즘.
- **유효 시간(Time To Live, TTL)**: DNS 리졸버가 특정 자원 레코드를 재조회하지 않고 캐시(Cache) 메모리에 보관 및 응답할 수 있는 유효 시간 규격.
- **도메인 이름 시스템 보안 확장(Domain Name System Security Extensions, DNSSEC)**: 비대칭키 공개키 암호화 전자서명을 통해 DNS 응답 정보의 위변조(DNS Spoofing/Poisoning) 방지 및 무결성을 검증하는 보안 기술.
- **최상위 도메인(Top-Level Domain, TLD)**: Root 도메인 바로 아래에 위치하는 국가/일반 범주 도메인 영역(.com, .net, .kr 등).

</details>

- 루트(Root) 및 **최상위 도메인(Top-Level Domain, TLD)** 네임서버 체계 중심의 계층적 **위임(Delegation)** 아키텍처 적용.
- **유효 시간(Time To Live, TTL)** 튜닝을 통해 트래픽 부하 분산과 도메인 변경 사항의 조기 전파 속도 조율.
- **DNSSEC(Domain Name System Security Extensions)**을 통한 응답 데이터의 출처 인증 및 데이터 무결성 보장.

#### 한줄 요약

- 위임•TTL 캐시•DNSSEC 기반 분산 해석


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스텁 리졸버(Stub Resolver)**: 클라이언트 OS 단에 내장되어 재귀 리졸버로 DNS 질의를 전송하고 최종 결과를 반환받는 최소 기능 리졸버.
- **재귀 리졸버(Recursive Resolver / Local DNS)**: 클라이언트 대신 Root-TLD-Authoritative 계층을 직접 순회하며 질의하고 결과를 캐싱하는 네임서버.
- **권한 있는 네임서버(Authoritative Name Server)**: 해당 도메인 존(Zone)의 원본 자원 레코드(RR)를 관리하고 최종 정답(Authoritative Answer)을 반환하는 네임서버.

</details>

```text
[ 클라이언트 단말 ] -> (스텁 리졸버)
                           |
                           v  (재귀 질의)
                [ 재귀 리졸버 (로컬 DNS) ]
                /          |          \
(반복 질의)    /           |           \ (반복 질의)
              v            v            v
     [ 루트 서버 ]    [ TLD 서버 ]    [ 권한 서버 ]
```

*스텁 리졸버, 재귀 리졸버, 계층별 네임서버 간 분산 협력 구조.*

| 구성요소 | 역할 및 세부 기능 | 대표 레코드/구조 |
|:---|:---|:---|
| **스텁 리졸버 (Stub Resolver)** | 애플리케이션의 DNS 요청 수신, Local DNS로 재귀 질의 전달 | OS DNS Client Service |
| **재귀 리졸버 (Local DNS)** | Iterative 질의 순회 실행, TTL Caching, 질의 결과 최종 클라이언트 반환 | ISP DNS, 8.8.8.8, 1.1.1.1 |
| **루트 네임서버 (Root Server)** | 전 세계 13개 대표 IP(Anycast 라우팅), TLD 네임서버 위치 안내 | Root Zone (`.`) |
| **TLD 네임서버 (TLD Server)** | `.com`, `.net`, `.kr` 등 최상위 도메인의 권한 있는 네임서버 정보 안내 | gTLD / ccTLD Server |
| **권한 있는 네임서버 (Authoritative)** | 특정 도메인의 원본 **자원 레코드(Resource Record)** 관리 및 정답 응답 | Primary/Secondary DNS |
| **자원 레코드 (Resource Record)** | A(IPv4), AAAA(IPv6), CNAME(별칭), MX(메일), NS(네임서버), TXT 등 | Zone File 정보 레코드 |

#### 한줄 요약

- 스텁•재귀•권한 서버의 분산 질의 구조

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **캐시 미스(Cache Miss)**: 질의 도메인의 유효한 RR이 재귀 리졸버의 캐시 메모리에 존재하지 않아 상위 네임서버 추적이 필요한 상태.
- **루트 서버(Root Server)**: DNS 계층 구조의 최상단에서 TLD 서버의 IP 주소를 안내하는 시작점.
- **위임 경로 질의(Delegation Path Query)**: Root -> TLD -> Authoritative 네임서버 순으로 반복(Iterative)하여 질의를 전달하는 절차.
- **권한 서버 안내(Authoritative Server Referral)**: 상위 네임서버가 하위 권한 서버의 NS 레코드 및 A 레코드(Glue Record)를 반환하는 응답 단계.

</details>

```text
[클라이언트] ── 질의 ──> [재귀 리졸버]
                              |
                    1. 캐시 확인
                              |
                    +-- 적중 ──────────+
                    |                  |
                    `-- 미적중         |
                         |             |
                 2. 위임 경로 질의     |
                 [루트]-[TLD]-[권한]   |
                         |             |
                 3. 권한 응답 캐싱     |
                         |             |
                         +-------------+
                              |
[클라이언트] <── 최종 응답 ── [재귀 리졸버]
```

### 동작 원리

1. **캐시 확인**: 유효한 자원 레코드 존재 여부 판단
2. **위임 경로 질의**: 루트•TLD•권한 서버 순회
3. **권한 응답 캐싱**: 최종 레코드를 TTL 동안 저장

#### 한줄 요약

- 루트•TLD•권한 서버 질의와 TTL 캐싱

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **재귀 질의(Recursive Query)**: 요청을 받은 리졸버가 최종 정답이나 에러 결과를 얻을 때까지 책임을 지고 상위 서버들을 추적하여 응답하는 방식.
- **반복 질의(Iterative Query)**: 요청을 받은 네임서버가 스스로 추적하지 않고, 자신이 아는 다음 상위/하위 네임서버의 위치(Referral)만을 즉시 응답하는 방식.

</details>

| 비교 항목 | **재귀 질의 (Recursive Query)** | **반복 질의 (Iterative Query)** |
|:---|:---|:---|
| 질의 주체 | Client -> Recursive Resolver (Local DNS) | Recursive Resolver -> Root/TLD/Auth Server |
| 응답 형태 | 최종 IP 주소 (또는 NXDOMAIN 에러) | 다음 위임 네임서버의 IP 주소 (Referral) |
| 서버 부하 및 보안 | 리졸버 서버에 메모리/CPU 부하 가중, Open Resolver DDoS 악용 위험 | 권한 네임서버 부하 최소화, 단시간 내 Referral 반환 |

> 요약: 클라이언트 단의 단순 편의성을 위한 재귀 질의와 DNS 서버 간의 분산 처리 및 서버 보호를 위한 반복 질의의 구별.

#### 한줄 요약

- 클라이언트 재귀 질의와 리졸버 반복 질의 분리

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **DNS 증폭 공격(DNS Amplification Attack)**: UDP 프로토콜의 IP Spoofing 및 EDNS0 특징을 악용하여 위조된 피해자 IP로 대용량 DNS 응답을 집중 유도하는 반사 DDoS 공격.
- **트랜잭션 서명(Transaction Signature, TSIG)**: Primary-Secondary DNS 간의 Zone Transfer(존 동기화) 시 HMAC 공유키를 사용하여 전송 데이터의 인가 여부와 무결성을 검증하는 기술.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| IP 변경 시 캐시 잔존 장애 | 긴 TTL 설정으로 타 네임서버 캐시 갱신 지연 | 주소 이관 작업 24~48시간 전 **TTL**을 300초로 사전 축소 | IP 전환 후 접속 에러 즉시 해결 |
| **DNS 증폭 공격** 반사체 활용 | Open Recursive Resolver 방치 | 외부 IP 재귀 질의 차단 및 Response Rate Limiting(RRL) 설정 | DDoS 반사체 활용 원천 차단 |
| DNS 캐시 포이즈닝 (Spoofing) | 질의 TxID 및 Port 예측을 통한 위조 응답 삽입 | **DNSSEC** 도입 및 Source Port Randomization 적용 | 위조 주소 유도 공격 차단 |
| Zone File 유출 | 비인가 IP의 Zone Transfer 요청 허용 | **TSIG** 서명 적용 및 허용된 Secondary IP만 렌더링 | DNS 내부 자원 식별 정보 보호 |

#### 한줄 요약

- DNSSEC•TSIG•RRL로 위조와 증폭 공격 통제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **TTL 전환 계획(TTL Transition Planning)**: 서비스 IP 변경 및 컷오버(Cutover) 시 사전에 TTL을 축소하고 작업 완료 후 원복하는 단계별 가이드라인.
- **운영 정책 결정(Operation Policy Selection)**: 고가용성 멀티 벤더 Authoritative DNS 이중화 및 DNSSEC 무결성 검증 정책을 결정하는 체계.

</details>

- 변경 전 **TTL 축소**, 운영 응답은 **DNSSEC** 검증 적용

#### 한줄 요약

- 변경 시 TTL을 줄이고 상시 DNSSEC 무결성 검증
