---
sidebar:
  order: 32
  label: "032. STIX•TAXII 위협 공유 (STIX TAXII)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 정보 표준 표현 및 자동 교환 규격 : STIX 및 TAXII (OASIS Standard)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "OASIS STIX 2.1(SDO/SRO 객체 모델/JSON), TAXII 2.1(RESTful API/Collection/Channel), TLP 표식 및 지표 철회(Revoked)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **STIX(Structured Threat Information Expression / OASIS STIX 2.1)**: 사이버 공격의 침해 지표(IoC), 공격 동기, 악성코드, TTP, 표적 자산 및 공격자 그룹 간의 복잡한 상관관계를 기계가 판독 가능한 JSON 기반 그래프 오브젝트 모델로 정형화한 글로벌 표준 위협 표현 언어.
- **TAXII(Trusted Automated eXchange of Intelligence Information / TAXII 2.1)**: STIX 형식으로 구조화된 사이버 위협 인텔리전스(CTI)를 HTTPS/RESTful API 기반으로 조직 간, 또는 이종 보안 장비 간에 안전하고 신속하게 실시간 전송·공유하는 애플리케이션 계층 통신 프로토콜.

</details>

- 정의/개념: 사이버 위협의 '데이터 구조(What: STIX)'와 '전송 메커니즘(How: TAXII)'을 이원화 표준화하여, 보안 솔루션 간 **기계 판독형 CTI 실시간 자동 공유 및 차단 연동(Machine-to-Machine Integration)** 을 가능하게 하는 **사이버 위협 공유 아키텍처**
- 배경/필요성: 벤더별 독자적인 데이터 포맷(비정형 텍스트, PDF, CSV)과 수동 이메일 공유 체계로 인해 발생하는 위협 지표 파싱 오류, 대응 지연, 이종 보안 장비 연동 불능의 한계를 극복할 요구

#### 한줄 요약
- STIX JSON 객체 모델로 위협 맥락을 표현하고 TAXII REST API로 이종 보안 장비 간 실시간 자동 교환을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **STIX 2.1 도메인 객체(SDO) vs 관계 객체(SRO)**:
  - **SDO(STIX Domain Objects / 18종)**: 위협 행위자(`threat-actor`), 침해 지표(`indicator`), 악성코드(`malware`), 공격 패턴(`attack-pattern`) 등 독립된 실체.
  - **SRO(STIX Relationship Objects / 2종)**: 객체 간 의미적 연결(`relationship`, `sighting`).
- **신뢰성 및 수명주기 메타데이터(Marking & Revocation)**: 정보 공개 범위를 지정하는 TLP(Traffic Light Protocol) 라벨과, 공격자가 인프라를 폐기했을 때 지표를 무효화하는 `revoked: true` 속성.

</details>

- **그래프 기반 의미론적 표현 (Graph-Based Modeling)**: 공격자 $\rightarrow$ 사용 도구 $\rightarrow$ 침해 지표 $\rightarrow$ 표적 자산의 다차원 관계망을 JSON-LD 형태로 모델링
- **TAXII 2.1 컬렉션 및 채널 아키텍처**: P2P 공유를 지원하는 **컬렉션(Collection)** 과 Hub-and-Spoke 발행-구독을 지원하는 **채널(Channel)** 제공
- **델타 쿼리(Delta Query) 기반 고효율 동기화**: `added_after` 매개변수를 통해 최근 변경 및 철회된 객체만 증분 동기화하여 네트워크 대역폭 절감

#### 한줄 요약
- 그래프 기반 JSON-LD 모델링, TAXII RESTful API 전송, TLP 표식 및 증분(Delta) 동기화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII 서버 API 루트(API Root)**: 테넌트 또는 조직 단위로 격리된 TAXII 서비스 진입점으로, 하위에 여러 개의 컬렉션(Collections)과 상태 엔드포인트를 호스팅하는 RESTful 구조.

</details>

```text
[ CTI 생산자 (Threat Intel Provider / ISAC) ]
 ├─ 위협 이벤트 분석 ➔ STIX 2.1 JSON 객체 생성:
 │  ├─ SDO: `indicator` (IP: 198.51.100.1), `malware` (Ransomware.LockBit)
 │  ├─ SRO: `relationship` (`indicator` ── indicates ──▶ `malware`)
 │  └─ Meta: `confidence: 90`, `lang: "en"`, `revoked: false`
 └─ HTTPS POST ➔ TAXII 2.1 서버 API 루트로 전송
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ TAXII 2.1 서버 (Trusted Intelligence Repository) ]                    │
│  ├─ API Root: `/api/v2.1/`                                              │
│  ├─ Collections: `/collections/financial-threats/objects/`              │
│  └─ 접근 제어: OAuth 2.0 / mTLS 상호 인증 및 TLP 기반 권한 필터링      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (HTTPS GET / Delta Query: `?added_after=...`)
                                     ▼
[ CTI 소비자 (Enterprise SOC / SIEM / SOAR / NGFW) ]
 ├─ STIX 파서: JSON 객체 파싱 ➔ IP/Domain 지표 추출
 ├─ 철회 검사: `revoked: true` 확인 시 기존 차단 룰셋 자동 해제
 └─ 방화벽 자동 주입: `confidence >= 80` 지표를 차단 ACL에 실시간 반영
```

선의 의미: 생산자가 STIX 2.1 그래프 객체를 생성하여 TAXII 서버에 게시하면, 소비자가 API를 통해 증분 조회하여 방화벽/SOAR에 자동 반영하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **STIX SDO (Domain Objects)** | 위협 행위자, 캠페인, 침해 지표, 취약점 등 18개 도메인 실체 정의 | OASIS STIX 2.1 |
| **STIX SRO (Relationships)** | SDO 간의 인과적·행위적 관계(`uses`, `indicates`, `targets`)를 그래프로 연결 | Relationship |
| **TAXII API Root** | 특정 보안 도메인 및 권한 그룹에 할당된 RESTful 서비스 인스턴스 | Endpoint |
| **TAXII Collection** | 소비자가 접근 권한에 따라 STIX 객체를 조회·구독할 수 있는 논리적 데이터셋 | Data Store |
| **TLP 마킹 메타데이터** | TLP 2.0(RED, AMBER+STRICT, AMBER, GREEN, CLEAR) 기반 정보 공유 범위 제약 | Data Marking |

#### 한줄 요약
- STIX SDO/SRO 객체, TAXII API Root/컬렉션, TLP 마킹 메타데이터가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **STIX/TAXII 연동 4단계 파이프라인**:
  1. **생산 및 직렬화(Produce & Serialize)**: 위협 데이터를 STIX 2.1 JSON으로 인코딩
  2. **게시(Publish)**: TAXII 서버 컬렉션에 HTTPS POST
  3. **증분 수집(Ingest)**: 소비자가 변경분(Delta) 쿼리로 최신 객체 가져오기
  4. **보안 장비 집행(Enforce)**: 파싱된 지표를 차세대 방화벽 및 EDR에 실시간 적용

</details>

```text
1. [위협 인텔리전스 생산] CTI 분석가가 새로운 APT 침해 지표 및 TTP를 STIX 2.1 JSON 객체로 직렬화
            │
            ▼
2. [TAXII 게시] 생산자가 TAXII 2.1 서버의 지정된 컬렉션 엔드포인트로 `POST /collections/{id}/objects/` 호출
            │
            ▼
3. [접근 제어 및 저장] TAXII 서버가 생산자의 mTLS 인증서 및 API 토큰을 검증하고 DB에 STIX 번들 저장
            │
            ▼
4. [증분 동기화] 기업 SOC의 SOAR 시스템이 `GET /collections/{id}/objects/?added_after=2026-08-20T00:00:00Z` 질의
            │
            ▼
5. [객체 파싱 및 집행] SOAR가 STIX 번들을 파싱하여 `revoked` 여부 확인 ➔ 고신뢰 IoC를 NGFW 블랙리스트에 자동 등록
```

**동작 원리**

1. **스키마 유효성 검증**: JSON Schema에 따른 필수 필드(`id`, `type`, `created`, `spec_version`) 검사
2. **RESTful 전송 계층**: HTTP 표준 상태 코드(200 OK, 202 Accepted)와 JSON 미디어 타입 사용
3. **타임스탬프 기반 필터링**: 불필요한 전체 덤프 전송을 배제하고 변경분만 효율적으로 동기화
4. **지표 상태 머신 평가**: 신규 등록, 신뢰도 수정, 지표 폐기(`revoked`) 상태를 분기 처리
5. **오케스트레이션 실행**: 보안 장비 API(REST)를 호출하여 차단 정책을 무인 자동화로 배포

#### 한줄 요약
- STIX 직렬화, TAXII REST 게시, mTLS 인증 저장, 증분 쿼리 수집, SOAR/방화벽 자동 배포 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX/TAXII 1.x vs 2.1 버전 진화 비교**: XML에서 JSON으로의 전환, 폴링 중심에서 RESTful API로의 아키텍처 현대화 비교.

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

- **TLP 2.0 (Traffic Light Protocol)**: 위협 정보의 공유 허용 범위를 명시하는 퍼스트(FIRST) 표준 규격:
  - `TLP:RED`: 발신자와 수신자 개인으로 한정 (외부 공유 절대 불가)
  - `TLP:AMBER+STRICT`: 수신 조직 내부로만 한정 (고객사/협력사 공유 불가)
  - `TLP:AMBER`: 수신 조직 및 관련 고객사/협력사 공유 가능
  - `TLP:GREEN`: 동일 커뮤니티(ISAC 회원사) 내 공유 가능
  - `TLP:CLEAR`: 대외 공개 가능 (과거 TLP:WHITE)

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 벤더 간 STIX JSON 확장 필드 남용으로 인한 **이기종 보안 장비 파싱 실패 및 연동 단절** | **OASIS STIX 2.1 Core 스펙 준수 및 커스텀 프로퍼티(`x_...`) 사용 엄격 제한** | 이기종 SIEM/SOAR 간 위협 데이터 상호운용성 100% 보장 |
| 공격자가 C2 도메인을 변경했음에도 방화벽 룰이 잔존하여 발생하는 **정상 IP 오차단 장애** | **STIX 객체의 `revoked: true` 및 `valid_until` 만료 속성 우선 파싱 및 룰 자동 회수** | 노후화된 지표의 능동적 폐기 및 비즈니스 정상 트래픽 보호 |
| 인터넷 구간 TAXII API 통신 시 공격자의 중간자 도청 및 위협 지표 변조(Tampering) | **TAXII 통신 채널에 TLS 1.3 암호화 및 클라이언트-서버 간 mTLS 상호 인증 강제** | 위협 정보 전송 구간 기밀성/무결성 100% 확보 및 비인가 주체 차단 |

#### 한줄 요약
- Core 규격 준수로 호환성을 확보하고, `revoked` 파싱으로 오차단을 막으며, mTLS로 전송 구간을 보호한다.

## Ⅶ. 결론

- 사이버 위협 정보의 글로벌 공유와 무인 자동화 대응을 실현하는 **STIX 및 TAXII 아키텍처**는 CTI 생태계의 핵심 표준 프로토콜이며, 실무 구현 시 **STIX 2.1 기반 그래프 객체 모델링**, **TAXII 2.1 RESTful API 기반 전사 TIP 및 SOAR 연동**, **TLP 2.0 기반 데이터 거버넌스 및 `revoked` 자동 파기 메커니즘**을 통합 구축하여 단절 없는 실시간 위협 정보 교환 생태계를 완성

#### 한줄 요약
- STIX 2.1의 구조화된 위협 표현과 TAXII 2.1의 안전한 RESTful 전송을 결합하여 실시간 위협 공유를 실현한다.
