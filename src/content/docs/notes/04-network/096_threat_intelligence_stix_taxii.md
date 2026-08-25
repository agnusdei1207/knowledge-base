---
sidebar:
  order: 96
  label: "096. 위협 인텔리전스 (STIX/TAXII)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 인텔리전스 표현 및 전송 표준 : STIX 및 TAXII"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 96
extra:
  question_no: "96"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "OASIS 표준, STIX(SDO/SRO 기반 표현 언어), TAXII(REST/HTTPS 전송 프로토콜) 및 TLP 공유 통제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **STIX (Structured Threat Information eXpression)**: 위협 주체, 공격 기법, IoC 지표를 JSON 그래프 구조(SDO/SRO)로 표현하는 OASIS 표준 언어.
- **TAXII (Trusted Automated eXchange of Intelligence Information)**: STIX 위협 인텔리전스를 HTTPS REST API를 통해 안전하게 공유·전송하는 표준 프로토콜.

</details>

- 정의/개념: 이종 보안 장비 및 조직 간에 사이버 위협 정보(CTI)를 **JSON 그래프 언어(STIX)와 HTTPS REST API(TAXII)로 실시간 자동 교환하는 OASIS 국제 표준 기술**
- 배경/필요성: 벤더별 파편화된 침해 지표(IoC) 포맷과 수동 공유 한계로 인한 **위협 전파 지연, 신종 랜섬웨어 사전 차단 룰 적재 불가 및 집단 방어 실패**

#### 한줄 요약
- STIX 구조화 언어와 TAXII 전송 프로토콜을 결합하여 위협 인텔리전스를 실시간 자동 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SDO vs SRO (STIX Domain/Relationship Objects)**: 위협 실체(Indicator, Malware 등)를 나타내는 도메인 객체(SDO)와 이들 간의 인과 관계(`indicates`, `uses`)를 나타내는 관계 객체(SRO).
- **TLP (Traffic Light Protocol, v2.0)**: 위협 정보의 공유 범위를 RED(비공개), AMBER(조직 한정), GREEN(커뮤니티), CLEAR(전체 공개) 4단계로 통제하는 규약.

</details>

- **JSON 기반 그래프 데이터 모델링(SDO/SRO)**: 위협 주체, 취약점, 공격 기법(TTPs)의 **다차원 연관 관계를 직관적인 그래프로 구조화**
- **HTTPS RESTful API 기반 고속 전송**: TAXII 2.1 표준을 통해 **SIEM/SOAR 시스템과의 증분(Incremental) 폴링 연동 지원**
- **TLP 2.0 기반 유통 거버넌스 통제**: RED/AMBER/GREEN 등급을 부여하여 **민감 위협 정보의 외부 무단 유출 통제**

#### 한줄 요약
- JSON 그래프 모델링, RESTful 고속 전송, TLP 기반 정보 공유 거버넌스를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII Collections**: 특정 위협 주제 또는 TLP 공유 등급별로 STIX 객체들을 그룹화하여 호스팅하는 서버 상의 데이터 저장소.

</details>

```text
[OASIS STIX 2.1 및 TAXII 2.1 위협 인텔리전스 공유 아키텍처]
|-- CTI Producer (보안 분석 기관, ISAC, CERT: STIX 2.1 JSON 객체 생성)
`-- TAXII 2.1 Server (Trusted Automated Exchange Server)
    |-- API Root / Discovery (지원 API 버전 및 컬렉션 목록 제공)
    |-- Collections (TLP 등급별 STIX 객체 저장소: RED / AMBER / GREEN)
    `-- Access Control (mTLS, OAuth 2.0 기반 클라이언트 인증/인가)
`-- CTI Consumers (엔터프라이즈 보안 인프라: HTTPS GET/POST 증분 폴링)
    |-- TIP / SIEM (위협 지표 파싱 및 상관 분석 룰 자동 생성)
    |-- SOAR Platform (침해 지표 기반 방화벽/WAF 차단 플레이북 가동)
    `-- EDR / FW (악성 IP, 도메인, 파일 해시 IoC 블랙리스트 즉시 주입)
```

선의 의미: 외부 위협 정보가 STIX 규격으로 TAXII 서버에 게시되고 기업의 SIEM, SOAR, 방화벽이 이를 구독하여 실시간 방어 룰로 변환하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **STIX 도메인 객체 (SDO)**| Attack Pattern, Threat Actor, Indicator 등 **위협 실체 18종 정의** | OASIS STIX 2.1 |
| **STIX 관계 객체 (SRO)**| SDO 간의 인과적 관계(`relationship`, `sighting`)를 **방향성 그래프로 연결** | Graph Model |
| **TAXII 서버 (Server)** | STIX 객체의 인덱싱, **컬렉션 관리, 접근 권한 통제 및 REST API 제공** | TAXII 2.1 |
| **TAXII 클라이언트** | 지정된 주기로 **TAXII 서버를 폴링하여 최신 증분(Incremental) IoC 수집** | SIEM / SOAR 연동 |
| **TLP 정책 통제기** | 위협 정보 유출 방지를 위해 **TLP 등급별 전송 대상 클라이언트 필터링** | FIRST TLP v2.0 |

#### 한줄 요약
- SDO/SRO 객체, TAXII 서버 컬렉션, TAXII 클라이언트, TLP 통제기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Incremental Polling (증분 폴링)**: `added_after` 파라미터로 마지막 동기화 이후 새로 추가/변경된 STIX 객체만 수신하여 네트워크 대역폭을 절감하는 기법.

</details>

```text
STIX 위협 정보 생성, TAXII 전송 및 방화벽 자동 주입 파이프라인
        │
   1. [STIX 번들 생성] 보안 기관이 APT 캠페인을 분석하여 SDO/SRO 기반 STIX 2.1 JSON 생성
        │
   2. [TAXII 컬렉션 적재] TLP 등급(AMBER)과 지표 유효기간(Valid-Until)을 부여하여 TAXII 게시
        │
   3. [증분 폴링 수집] 기업 TIP/SOAR가 HTTPS REST API로 최신 증분 위협 객체 수집
        │
   4. [방화벽 룰 자동 배포] STIX Indicator(악성 C&C IP)를 파싱하여 방화벽/WAF ACL에 즉시 주입
        │
   ▼
5. [유효기간 만료 회수] 만료 기간 도래 시 차단 룰 자동 삭제 및 탐지 시 Sighting 객체 역피드백
```

#### 한줄 요약
- STIX 번들 생성 → TAXII 컬렉션 게시 → 증분 폴링 수집 → 방화벽 룰 자동 주입 → 유효기간 만료 회수 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX 1.x (XML)** vs **STIX 2.x (JSON-Graph)**: 무거운 단일 문서 스키마에서 가벼운 분산 그래프 RESTful 모델로의 진화.

</details>

| 비교 항목 | 1세대 CTI 공유 (STIX 1.x / TAXII 1.x) | 차세대 CTI 공유 (STIX 2.1 / TAXII 2.1) |
|:---|:---|:---|
| **데이터 표현 형식** | **XML 기반 스키마 (무겁고 파싱 복잡)** | **JSON 기반 분산 그래프 객체 (가볍고 직관적)** |
| **객체 모델 구조** | 거대한 단일 문서(Monolithic) 계층 구조 | **독립된 SDO/SRO 노드-엣지 그래프 네트워크** |
| **전송 프로토콜** | SOAP / XML over HTTP (별도 프로토콜) | **RESTful API / JSON over HTTPS (OpenAPI 3.0)** |
| **연동 편의성** | 파서 개발 난이도 높음, 실시간 연동 지연 | **Python 친화적, SOAR/SIEM 네이티브 지원** |
| **문맥 표현력** | 정적 지표 나열 위주 | **공격자-기법-취약점-지표 간 다차원 관계 표현** |

#### 한줄 요약
- STIX/TAXII 2.1은 JSON 그래프 모델과 REST API를 채택하여 실시간 보안 자동화에 최적화되었다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Stale IoC (낡은 지표 오차단)**: 클라우드 IP 동적 재할당으로 과거 악성 C&C였던 IP가 정상 서비스로 변경된 후에도 방화벽에서 지속 차단되어 발생하는 오차단 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동적 IP 재할당 환경에서 만료된 악성 IP 차단으로 인한 **정상 서비스 오차단** | STIX **`valid_until` 필드 강제 및 TTL 만료 시 방화벽 룰 자동 회수** | 낡은 지표(Stale IoC) 오차단 제거 및 정책 메모리 보존 |
| TLP 공유 규약 위반으로 인한 기밀 위협 인텔리전스 외부 유출 | TAXII 서버의 **`OAuth 2.0/mTLS 기반 RBAC` 및 TLP 필터링** | TLP 등급별 엄격한 수신자 격리 및 기밀성 100% 보장 |
| 이종 보안 장비별 STIX 파싱 불일치로 인한 차단 룰 적재 누락 | **`TIP (Threat Intelligence Platform)` 기반 룰 정규화 및 사전 검증** | 장비별 이질성 해소 및 100% 무손실 보안 정책 자동 배포 |
| 글로벌 대량 IoC 수집 시 로컬 방화벽 ACL 용량 한계 초과 | **신뢰도 점수(Confidence) 상위 10% 우선 주입 및 계층화** | 방화벽 하드웨어 TCAM 자원 고갈 방지 |

#### 한줄 요약
- 유효기간 설정으로 오차단을 방지하고, TLP 접근 제어로 기밀성을 보장하며, TIP 정규화로 파싱 누락을 차단한다.

## Ⅶ. 결론

- 지능형 APT 공격에 대한 집단 면역 체계를 구축하기 위해 **OASIS STIX 2.1 및 TAXII 2.1 표준 기반의 위협 인텔리전스 공유 체계를 필수 도입**하되, 정보의 신뢰성과 운영 효율성을 확보하기 위해 **TLP 기반 다계층 거버넌스, IoC 유효기간 자동 만료 메커니즘, SIEM/SOAR 연동 실시간 정책 주입 파이프라인**을 통합 구축하여 능동적 사이버 위협 대응 생태계 완성

#### 한줄 요약
- STIX/TAXII 표준과 TLP 거버넌스 및 SOAR 연동을 통해 실시간 지능형 위협 대응을 구현한다.