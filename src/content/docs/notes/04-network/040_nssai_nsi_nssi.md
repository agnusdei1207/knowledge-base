---
sidebar:
  order: 40
  label: "040. NSSAI•NSI•NSSI"
  badge:
    text: "기출 · 50%"
    variant: note
title: "5G 네트워크 슬라이스 식별 체계 : NSSAI•NSI•NSSI"
date: "2026-08-26T13:47:36+09:00"
tags:
  - "notes-network"
weight: 40
extra:
  question_no: "40"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, S-NSSAI 구조(SST/SD) 및 NSI/NSSI 계층적 관리 모델"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NSSAI (Network Slice Selection Assistance Information)**: 단말이 접속 시 망에 전달하는 단일 슬라이스 식별자(S-NSSAI)들의 집합 (최대 8개).
- **NSI (Network Slice Instance)**: 무선(RAN), 전송(Transport), 코어(Core) 도메인이 E2E로 결합되어 구동되는 완전한 가상 네트워크 인스턴스.
- **NSSI (Network Slice Subnet Instance)**: NSI를 구성하기 위해 각 도메인(RAN, Transport, Core)별로 독립 생성·관리되는 하위 서브넷 인스턴스.

</details>

- 정의/개념: 5G 슬라이싱을 식별·운용하기 위해 **단말 식별자(NSSAI), E2E 가상망 인스턴스(NSI), 도메인별 서브넷 인스턴스(NSSI)로 구성된 3GPP 표준 관리 체계**
- 배경/필요성: 5G 다중 테넌트 환경에서 단말의 요구조건(SLA)과 실제 무선·전송·코어 자원 간의 **매핑 기준 부재 시 슬라이스 선택 오류, 자원 격리 실패 및 라이프사이클 관리 불가**를 겪으므로, 단말이 요구를 알리는 식별자(NSSAI)와 E2E 인스턴스(NSI), 도메인별 구성 단위(NSSI)를 세 계층으로 분리해 요구 표현과 자원 조립을 서로 독립적으로 바꿀 수 있게 할 필요

#### 한줄 요약
- 단말의 S-NSSAI 요청을 분석하여 도메인별 NSSI를 조립한 E2E NSI로 매핑·개통한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **S-NSSAI (Single NSSAI, 32-bit)**: SST(Slice/Service Type, 8비트: eMBB 1, URLLC 2, mMTC 3, V2X 4)와 SD(Slice Differentiator, 24비트)로 구성.
- **Dedicated vs Shared NSSI**: 특정 NSI만 독점 사용하는 전용 서브넷과 복수 NSI가 공용으로 공유하는 공유 서브넷.

</details>

- **32비트 S-NSSAI 식별 체계**: 표준 SST(8비트)와 테넌트 구분용 SD(24비트)로 구성되며 단말당 최대 8개 동시 수용
- **계층적 인스턴스 조립 아키텍처**: 1개의 E2E NSI는 RAN NSSI, Transport NSSI, Core NSSI의 서브넷 결합으로 완성
- **서브넷(NSSI) 재사용성**: 코어망 NSSI를 단독 전용(Dedicated)하거나 복수 슬라이스가 공용(Shared) 공유 가능

#### 한줄 요약
- 32비트 S-NSSAI 파라미터, NSI-NSSI 계층적 조립, 전용/공유 서브넷 재사용을 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NSMF (Network Slice Management Function)**: E2E 슬라이스(NSI)의 생성, 변경, 삭제를 총괄 오케스트레이션하는 엔티티.
- **NSSMF (Network Slice Subnet Management Function)**: RAN, Transport, Core 각 도메인 서브넷(NSSI)의 자원을 직접 제어하는 도메인 관리자.

</details>

```text
[5G 슬라이스 식별 체계]
|-- S-NSSAI
|-- AMF / NSSF
|-- NSI
`-- NSSI
```

선의 의미: 계층 및 단말의 S-NSSAI 요청을 NSSF가 검증하고 NSMF/NSSMF가 NSI와 하위 도메인 NSSI를 조립하여 바인딩하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **S-NSSAI** | 단말이 요청하는 **SST(8비트 서비스 유형) + SD(24비트 테넌트 식별자) 32비트 식별자** | 단말당 최대 8개 |
| **AMF / NSSF** | 단말의 S-NSSAI를 수신하여 가입자 UDM 정보를 대조하고 **최적의 NSI 인스턴스 선택 매핑** | 슬라이스 선택 NF |
| **NSI (E2E 인스턴스)** | RAN, Transport, Core 도메인을 엮어 **단말부터 데이터망까지 종단간 개통된 완전한 가상 네트워크**| E2E 슬라이스 실체 |
| **NSSI (서브넷 인스턴스)**| 무선망, 전송망, 코어망 각 도메인에서 **독립적으로 생성·관리되는 하위 자원 파티션 조각** | 도메인별 단위 블록 |

#### 한줄 요약
- NSSI를 도메인 단위 부품으로 떼어 두었기에 슬라이스마다 코어망을 새로 세우지 않고 공용 서브넷을 재사용할 수 있고, 단말은 32비트 S-NSSAI 하나만 실어 보내 그 조립 결과인 NSI를 지목한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **슬라이스 바인딩 5단계**: S-NSSAI 요청 제출 $\to$ AMF/NSSF 검증 $\to$ 가용 NSI 인스턴스 매핑 $\to$ NSSI 자원 정합성 확인 $\to$ PDU 세션 개통.

</details>

```text
S-NSSAI 기반 슬라이스 인스턴스 매핑 파이프라인
        │
   1. [S-NSSAI 요청 제출] 단말이 망 등록(Registration) 시 요청 S-NSSAI 목록 전송
        │
   2. [AMF / NSSF 검증] 가입자 UDM 프로파일을 대조하여 허용된 NSSAI(Allowed NSSAI) 결정
        │
   3. [가용 NSI 인스턴스 매핑] NSSF가 정책에 따라 최적의 E2E NSI 인스턴스 식별자 매핑
        │
   4. [NSSI 자원 정합성 확인] NSI를 구성하는 RAN/Transport/Core NSSI 정상 가용 상태 확인
        │
   ▼
5. [PDU 세션 개통] 격리된 전용 UPF 경로를 통해 사용자 데이터 송수신 시작
```

#### 한줄 요약
- S-NSSAI는 식별자일 뿐이어서 NSSF가 실제 NSI에 붙이기 전까지 아무 자원도 잡지 않으므로, 요청과 자원 사이의 한 겹 매핑이 슬라이스 재배치를 단말 설정 변경 없이 흡수한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NSSAI vs NSI vs NSSI**: 논리적 식별 파라미터(NSSAI), 종단간 가상망 완성체(NSI), 도메인별 자원 블록(NSSI).

</details>

| 비교 항목 | NSSAI / S-NSSAI | NSI (Network Slice Instance) | NSSI (Subnet Instance) |
|:---|:---|:---|:---|
| **개념적 성격** | **논리적 슬라이스 식별 파라미터** | **종단간(E2E) 가상 네트워크 완성품** | **도메인별 하위 가상 자원 서브넷 조각** |
| **물리적 실체성** | 32비트 제어 데이터 (SST+SD) | **실제 패킷이 전송되는 E2E 파이프라인** | RAN, Transport, Core 내 독립 자원 블록 |
| **관리 엔티티** | 단말(UE) 및 5GC NSSF/AMF | **NSMF (Network Slice Management)** | **NSSMF (Subnet Management Function)** |
| **수명주기(Lifecycle)**| 세션/단말 접속 단위 동적 전달 | B2B 서비스 계약 단위 생성·삭제 | NSI 생성 시 할당 또는 기존 서브넷 공유 |

#### 한줄 요약
- NSSAI는 식별 파라미터이고, NSI는 종단간 가상망 인스턴스이며, NSSI는 도메인별 서브넷 자원이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Orphan Resource (고아 자원)**: 상위 NSI 인스턴스가 삭제되었으나 하위 NSSMF가 NSSI 자원을 정상 회수하지 않아 메모리/스펙트럼을 낭비하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 로밍 환경에서 방문망(VPLMN) NSSF에 홈망 S-NSSAI 매핑 부재 | **`NSSF 간 매핑 테이블 동기화` 및 3GPP 표준 SST(1~4) 준수** | 글로벌 로밍 슬라이스 접속 실패 예방 |
| 상위 NSI 삭제 후 하위 도메인 NSSI 미회수로 인한 **고아 자원(Orphan) 발생** | **NSMF-NSSMF 간 `자원 연쇄 회수 자동화 트리거` 구현** | 가상 자원 누수 차단 및 클라우드 비용 절감 |
| 비인가 단말이 특수 목적(URLLC) S-NSSAI로 위장 접속 시도 | UDM 가입자 DB 기반 **`Secondary Slice Authentication (2차 인증)`** | 비인가 단말의 슬라이스 침투 원천 차단 |
| 복수 NSI가 단일 Core NSSI 공유 시 트래픽 폭주로 인한 자원 고갈 | **`도메인별 Dynamic Quota 및 Rate Limiting` 적용** | 공유 서브넷 환경에서의 공평성 및 안정성 보장 |

#### 한줄 요약
- NSSF 로밍 동기화, 자원 연쇄 회수 자동화, 2차 인증 적용, 서브넷 Rate Limiting으로 운영한다.

## Ⅶ. 결론

- 요청 식별은 **S-NSSAI**, E2E·도메인 자원은 **NSI·NSSI**로 관리

#### 한줄 요약
- NSSAI, NSI, NSSI는 5G 네트워크 슬라이싱의 식별, 종단간 조립, 서브넷 관리를 전담하는 핵심 3대 아키텍처 요소다.
