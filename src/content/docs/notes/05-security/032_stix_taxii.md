---
sidebar:
  order: 32
  label: "032. STIX•TAXII 위협 공유"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 정보 표준 표현 및 자동 교환 규격 : STIX 및 TAXII"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: STIX 표현과 TAXII 전송을 결합한 CTI 교환 표준
- 배경/필요성: 글로벌 사이버 보안 생태계에서 기관 및 벤더마다 독자적인 위협 데이터 포맷과 전송 방식을 사용할 경우, 이기종 보안 솔루션(SIEM/SOAR/방화벽) 간 실시간 위협 연동이 불가능하고 수동 데이터 변환으로 인한 치명적인 대응 지연을 초래함에 따라, 사이버 위협 지표(IoC), 공격자, TTP 간의 관계를 기계 판독 가능한 JSON 그래프 객체(SDO/SRO)로 정형화한 OASIS STIX 2.1과 이를 RESTful HTTPS 기반으로 안전하게 실시간 교환하는 TAXII 2.1 전송 프로토콜을 도입하여 위협 정보 표현 및 전송 규격의 글로벌 표준화, TLP 2.0 기반 정보 공유 거버넌스 확립 및 기계 간(M2M) 제로터치 자동 차단 연동을 달성할 필요

#### 한줄 요약
- 표현(STIX)과 전송(TAXII)을 분리한 덕에 한쪽 규격을 바꿔도 다른 쪽이 영향받지 않지만, 그 대가로 두 규격의 버전을 함께 맞춰야 연동이 성립한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SDO vs SRO**: 도메인 실체를 정의하는 STIX Domain Objects(18종)와 객체 간 관계를 정의하는 STIX Relationship Objects.
- **TLP 2.0 (Traffic Light Protocol)**: 위협 정보 공유 범위를 RED, AMBER+STRICT, AMBER, GREEN, CLEAR 5단계로 규정하는 보안 마킹 표준.

</details>

- **STIX 2.1**로 위협 객체의 다대다 관계 표현
- **TAXII 2.1**의 증분 조회로 전송량 절감
- **TLP 2.0** 마킹으로 공유 범위 통제

#### 한줄 요약
- 그래프 모델은 표현력을 얻은 대신 파서 구현 부담을 소비자에게 넘겼고, 증분 조회는 대역폭을 아낀 대신 소비자가 마지막 동기화 시점을 상태로 관리할 책임을 진다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII Collection**: 클라이언트가 접근 권한에 따라 STIX 객체를 조회 및 게시할 수 있는 논리적 데이터 저장소 엔드포인트.

</details>

```text
[STIX·TAXII 공유 체계]
├─ CTI 생산 계층
│  └─ STIX 표현 모델 (SDO·SRO 객체)
├─ TAXII 전송 허브
│  ├─ API Root (REST API 진입점)
│  ├─ Collection (논리 데이터 저장소)
│  └─ 접근 통제 (mTLS·TLP 마킹)
└─ CTI 소비 계층
   ├─ STIX 파서 (그래프 객체 역직렬화)
   └─ 보안 집행 솔루션 (SIEM·SOAR·방화벽)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| STIX SDO (Domain Objects) | 위협 행위자·악성코드·침해지표 등 18종 도메인 실체 객체 정의 |
| STIX SRO (Relationship Objects) | SDO 간 연관 관계(indicates, targets 등) 그래프 연결 표현 |
| TAXII API Root | RESTful HTTPS API 서비스 진입점 및 버전 협상 엔드포인트 제공 |
| TAXII Collection | 클라이언트 인가 권한에 따른 STIX 객체 논리 저장소 및 쿼리 엔드포인트 |
| TLP 마킹 (Data Marking) | TLP 2.0 규격 기반 정보 공유 허용 범위(RED~CLEAR) 통제 |

#### 한줄 요약
- 위협의 의미는 SDO가 아니라 SRO에 담기므로, 관계 객체 없이 지표만 주고받으면 표준을 써도 결국 IoC 나열로 되돌아간다.

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

- 1. 위협 인텔리전스 생산
- 2. TAXII 게시
- 3. 접근 제어 및 저장
- 4. 증분 동기화
- 5. 객체 파싱 및 집행

#### 한줄 요약
- 게시는 생산자가 밀어 넣지만 수집은 소비자가 `added_after`로 끌어가는 폴링이라, 공유 지연은 전송 속도가 아니라 소비자의 조회 주기가 결정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX 1.x / TAXII 1.x (레거시)**: 위협 정보를 XML 트리로 표현하고 SOAP 웹 서비스로 전송하여, 표현력은 확보했으나 스키마 검증과 파싱에 큰 연산 비용을 치르던 1세대 규격.
- **STIX 2.1 / TAXII 2.1 (현재 표준)**: 동일한 위협 정보를 JSON 그래프 객체로 경량화하고 RESTful HTTPS 증분 조회로 전송하여, 파싱·대역폭 비용을 제거하고 `revoked`·`confidence` 같은 수명주기 속성을 규격 자체에 내장한 현행 규격.

</details>

| 비교 항목 | STIX 1.x / TAXII 1.x (레거시) | STIX 2.1 / TAXII 2.1 (현재 표준) |
|:---|:---|:---|
| 데이터 표현 형식 | XML (복잡하고 무거운 스키마) | JSON (경량화, 고속 파싱, 기계 친화적) |
| 데이터 모델 구조 | 계층적 트리(Tree) 구조 | 노드-엣지 그래프(Graph) 오브젝트 모델 |
| 통신 프로토콜 | SOAP / XML-RPC 기반 웹 서비스 | RESTful API (HTTPS + JSON) |
| 메타데이터 관리 | TLP 및 수명주기 표현 복잡 | TLP 2.0 마킹 및 `revoked`/`confidence` 기본 내장 |
| 처리 성능 및 대역폭| 파싱 오버헤드 큼, 대용량 트래픽 발생 | 초고속 직렬화, 증분(Delta) 쿼리로 대역폭 극소화 |
| 상용 솔루션 지원 | 점진적 지원 중단 (Deprecated) | 글로벌 SIEM, SOAR, TIP(MISP 등) 표준 채택 |

#### 한줄 요약
- STIX 1.x는 무거운 XML 구조였으나, STIX 2.1/TAXII 2.1은 경량 JSON 그래프 모델과 RESTful API로 진화하였다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Revocation Handling**: STIX 객체의 `revoked: true` 속성을 실시간 파싱하여 이미 만료되거나 오탐으로 판명된 차단 룰을 방화벽에서 즉시 회수하는 처리 메커니즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| STIX JSON 확장 필드 남용으로 인한 이기종 보안 장비 파싱 실패 및 연동 단절 | `OASIS STIX 2.1 Core 스펙 준수 및 커스텀 프로퍼티(x_...) 사용 제한` | 이기종 SIEM/SOAR 간 위협 데이터 상호운용성 보장 |
| 공격자가 C2 도메인을 변경했음에도 방화벽 룰이 남아 발생하는 **정상 IP 오차단 장애** | STIX 객체의 `revoked: true 및 valid_until 속성 파싱 후 룰 자동 회수` | 노후 지표 능동 폐기 및 비즈니스 트래픽 보호 |
| 인터넷 구간 TAXII API 통신 시 공격자의 중간자 도청 및 **위협 지표 변조(Tampering)** | TAXII 채널에 `TLS 1.3 암호화 및 mTLS 상호 인증 강제` | 위협 정보 전송 구간 무결성 확보 및 비인가자 차단 |
| 대규모 위협 피드 수신 시 파싱 엔진 과부하 및 메모리 병목 | `비동기 스트리밍 파서(ijson) 및 백프레셔(Backpressure) 큐` 도입 | 수백만 건 STIX 번들 인제스트 시 무중단 고속 처리 |

#### 한줄 요약
- 커스텀 프로퍼티는 표현력을 얻는 대신 상호운용성을 잃으므로, 표준 연동을 택한 조직은 자사 고유 정보를 규격 밖에 남겨 두는 손실을 감수하는 편이 유리하다.

## Ⅶ. 결론

- 이기종 보안 솔루션 및 글로벌 위협 공유 커뮤니티 간의 언어 장벽을 허물고 위협 인텔리전스의 실시간 기계 간(M2M) 유통을 가능케 한 차세대 사이버 위협 정보 공유 및 자동화(SOAR) 연동의 가장 핵심적인 국제 표준 기술(OASIS Open)로 확고히 자리매김하였으며, 양자내성 전송 및 공급망 위협(CSCRM) 데이터셋 확장으로 진화하는 가운데, 실무 STIX/TAXII 연동 인프라 구축 시에는 무거운 XML 트리 구조의 구형 1.x 규격을 탈피하여 JSON 그래프 기반 STIX 2.1 및 RESTful TAXII 2.1 표준 전면 채택, 오탐으로 인한 서비스 장애를 방어하기 위한 `revoked: true` 및 `valid_until` 속성 기반 보안 정책 자동 회수(Revocation) 파이프라인 구축, 전송 구간 무결성을 보장하는 mTLS 상호 인증 및 TLP 2.0 마킹 기반 데이터 기밀성 통제를 결합하여 완벽한 자동화 위협 대응 생태계를 완성

#### 한줄 요약
- STIX/TAXII는 STIX 2.1의 구조화된 위협 표현과 TAXII 2.1의 안전한 RESTful 전송을 결합하여 실시간 위협 공유를 실현하는 국제 표준 규격이다.
