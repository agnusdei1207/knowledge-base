---
sidebar:
  order: 32
  label: "032. STIX•TAXII 위협 공유"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 정보 표준 표현 및 자동 교환 규격 : STIX 및 TAXII"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 32
extra:
  question_no: "32"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "OASIS STIX 2.1(SDO/SRO 객체 모델/JSON), TAXII 2.1(RESTful API/Collection/Channel), TLP 표식 및 지표 철회(Revoked)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **STIX (OASIS STIX 2.1)**: 사이버 위협 지표, 공격자, TTP 간의 관계를 기계 판독 가능한 JSON 그래프로 정형화한 표현 언어.
- **TAXII (TAXII 2.1)**: STIX 위협 인텔리전스를 RESTful HTTPS API를 통해 안전하게 실시간 교환하는 전송 프로토콜.

</details>

- 정의/개념: 위협 데이터 표현(STIX: JSON 그래프 모델)과 전송 메커니즘(TAXII: RESTful API)을 분리하여 **이종 시스템 간 CTI를 실시간 교환하는 표준 기술**
- 배경/필요성: 벤더별 독자 포맷 사용으로 인한 **위협 데이터 파편화, 수동 변환 지연에 따른 실시간 자동 방어 실패 및 공유 폐쇄성**

#### 한줄 요약
- STIX JSON 그래프 모델과 TAXII RESTful 전송을 결합하여 이종 보안 장비 간 실시간 위협 공유를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SDO vs SRO**: 도메인 실체를 정의하는 STIX Domain Objects(18종)와 객체 간 관계를 정의하는 STIX Relationship Objects.
- **TLP 2.0 (Traffic Light Protocol)**: 위협 정보 공유 범위를 RED, AMBER+STRICT, AMBER, GREEN, CLEAR 5단계로 규정하는 보안 마킹 표준.

</details>

- **JSON 기반 그래프 데이터 모델링(STIX 2.1)**: 공격자, **도구, 취약점 간의 다대다(N:M) 관계망을 노드와 엣지로 구조화 표현**
- **RESTful HTTPS 증분 동기화(TAXII 2.1)**: 컬렉션 API를 통해 **변경분(Delta) 데이터만 효율적으로 질의하여 네트워크 오버헤드 최소화**
- **글로벌 정보 공유 거버넌스(TLP 2.0 내장)**: 객체 헤더에 **TLP 라벨을 강제 부착하여 비인가 외부 유출 및 공유 범위 위반 원천 방지**

#### 한줄 요약
- JSON 그래프 모델링, RESTful 증분 동기화, TLP 2.0 공유 거버넌스를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII Collection**: 클라이언트가 접근 권한에 따라 STIX 객체를 조회 및 게시할 수 있는 논리적 데이터 저장소 엔드포인트.

</details>

```text
[STIX 2.1 / TAXII 2.1 생산-유통-소비 아키텍처]
|-- CTI Producer (STIX 2.1 JSON 인코딩: SDO/SRO -> HTTPS POST 전송)
`-- TAXII 2.1 Server (Repository)
    |-- API Root (/api/v2.1/)
    |-- Collections (/collections/financial-threats/objects/)
    `-- Access Control (OAuth 2.0 / mTLS 상호 인증 & TLP 권한 필터링)
`-- CTI Consumer (Enterprise SOC / SIEM / SOAR / NGFW)
    |-- Delta Ingest (HTTPS GET ?added_after=...)
    |-- STIX Parser (JSON 파싱 -> IP/Domain 지표 및 revoked 검사)
    `-- Firewall Enforce (고신뢰 IoC 방화벽 ACL 실시간 자동 주입)
```

선의 의미: 생산자가 STIX 2.1 그래프 객체를 생성하여 TAXII 서버에 게시하면 소비자가 API를 통해 증분 조회하여 방화벽/SOAR에 자동 반영하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **STIX SDO (Domain Objects)** | 위협 행위자, 캠페인, 침해 지표 등 **18개 도메인 실체 정의** | OASIS STIX 2.1 |
| **STIX SRO (Relationships)** | SDO 간의 관계(`uses`, `indicates`, `targets`)를 **그래프로 연결** | Relationship |
| **TAXII API Root** | 특정 보안 도메인에 할당된 **RESTful 서비스 진입점 인스턴스** | Endpoint |
| **TAXII Collection** | STIX 객체를 **조회·구독할 수 있는 논리적 데이터셋 엔드포인트** | Data Store |
| **TLP 마킹 메타데이터**| TLP 2.0 라벨 기반 **정보 공유 허용 범위 제약 관리** | Data Marking |

#### 한줄 요약
- STIX SDO/SRO 객체, TAXII API Root/컬렉션, TLP 마킹 메타데이터가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **STIX/TAXII 4단계 연동**: 1. 직렬화(Serialize) → 2. TAXII 게시(Publish) → 3. 증분 수집(Ingest) → 4. 보안 장비 집행(Enforce).

</details>

```text
STIX 객체 직렬화, TAXII REST 게시, 증분 동기화 및 자동 차단 파이프라인
        │
   1. [위협 인텔리전스 생산] CTI 분석가가 APT 침해 지표 및 TTP를 STIX 2.1 JSON 객체로 직렬화
        │
   2. [TAXII 게시] 생산자가 TAXII 2.1 서버의 엔드포인트로 `POST /collections/{id}/objects/` 호출
        │
   3. [접근 제어 및 저장] TAXII 서버가 생산자의 mTLS 인증서를 검증하고 DB에 STIX 번들 저장
        │
   4. [증분 동기화] 기업 SOC의 SOAR가 `GET /collections/{id}/objects/?added_after=...` 질의
        │
   ▼
5. [객체 파싱 및 집행] SOAR가 STIX를 파싱하여 `revoked` 확인 ➔ 고신뢰 IoC를 NGFW에 자동 등록
```

#### 한줄 요약
- STIX 직렬화 → TAXII REST 게시 → mTLS 인증 저장 → 증분 쿼리 수집 → SOAR/방화벽 자동 배포 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX 1.x / TAXII 1.x (레거시)** vs **STIX 2.1 / TAXII 2.1 (현재 표준)**.

</details>

| 비교 항목 | STIX 1.x / TAXII 1.x (레거시) | STIX 2.1 / TAXII 2.1 (현재 표준) |
|:---|:---|:---|
| **데이터 표현 형식** | **XML (복잡하고 무거운 스키마)** | **JSON (경량화, 고속 파싱, 기계 친화적)** |
| **데이터 모델 구조** | 계층적 트리(Tree) 구조 | **노드-엣지 그래프(Graph) 오브젝트 모델** |
| **통신 프로토콜** | SOAP / XML-RPC 기반 웹 서비스 | **RESTful API (HTTPS + JSON)** |
| **메타데이터 관리** | TLP 및 수명주기 표현 복잡 | **TLP 2.0 마킹 및 `revoked`/`confidence` 기본 내장** |
| **처리 성능 및 대역폭**| 파싱 오버헤드 큼, 대용량 트래픽 발생 | **초고속 직렬화, 증분(Delta) 쿼리로 대역폭 극소화** |
| **상용 솔루션 지원** | 점진적 지원 중단 (Deprecated) | **글로벌 SIEM, SOAR, TIP(MISP 등) 표준 채택** |

#### 한줄 요약
- STIX 1.x는 무거운 XML 구조였으나, STIX 2.1/TAXII 2.1은 경량 JSON 그래프 모델과 RESTful API로 진화하였다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Revocation Handling**: STIX 객체의 `revoked: true` 속성을 실시간 파싱하여 이미 만료되거나 오탐으로 판명된 차단 룰을 방화벽에서 즉시 회수하는 처리 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| STIX JSON 확장 필드 남용으로 인한 **이기종 보안 장비 파싱 실패 및 연동 단절** | **`OASIS STIX 2.1 Core 스펙 준수 및 커스텀 프로퍼티(x_...) 사용 제한`** | 이기종 SIEM/SOAR 간 위협 데이터 상호운용성 보장 |
| 공격자가 C2 도메인을 변경했음에도 방화벽 룰이 남아 발생하는 **정상 IP 오차단 장애** | **STIX 객체의 `revoked: true 및 valid_until 속성 파싱 후 룰 자동 회수`** | 노후 지표 능동 폐기 및 비즈니스 트래픽 보호 |
| 인터넷 구간 TAXII API 통신 시 공격자의 중간자 도청 및 **위협 지표 변조(Tampering)** | **TAXII 채널에 `TLS 1.3 암호화 및 mTLS 상호 인증 강제`** | 위협 정보 전송 구간 무결성 확보 및 비인가자 차단 |
| 대규모 위협 피드 수신 시 파싱 엔진 과부하 및 메모리 병목 | **`비동기 스트리밍 파서(ijson) 및 백프레셔(Backpressure) 큐`** 도입 | 수백만 건 STIX 번들 인제스트 시 무중단 고속 처리 |

#### 한줄 요약
- Core 규격 준수로 호환성을 확보하고, `revoked` 파싱으로 오차단을 막으며, mTLS로 전송 구간을 보호한다.

## Ⅶ. 결론

- 사이버 위협 정보의 글로벌 공유와 무인 자동화 대응을 실현하는 **STIX 및 TAXII 아키텍처는 CTI 생태계의 핵심 표준 프로토콜**이며, 실무 구현 시 **STIX 2.1 기반 그래프 객체 모델링, TAXII 2.1 RESTful API 기반 전사 TIP 및 SOAR 연동, TLP 2.0 기반 데이터 거버넌스 및 `revoked` 자동 파기 메커니즘**을 통합 구축하여 단절 없는 실시간 위협 정보 교환 생태계 완성

#### 한줄 요약
- STIX/TAXII는 STIX 2.1의 구조화된 위협 표현과 TAXII 2.1의 안전한 RESTful 전송을 결합하여 실시간 위협 공유를 실현하는 국제 표준 규격이다.