---
sidebar:
  order: 96
  label: "096. 위협 인텔리전스 (STIX/TAXII)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 인텔리전스 표현 및 전송 표준 : STIX 및 TAXII (Threat Intelligence)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 96
extra:
  question_no: "096"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "OASIS 표준, STIX(SDO/SRO 기반 표현 언어), TAXII(REST/HTTPS 전송 프로토콜) 및 TLP 공유 통제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **사이버 위협 인텔리전스(Cyber Threat Intelligence, CTI)**: 공격 주체(Threat Actor), 공격 기법(TTPs), 침해 지표(IoC: IP, 도메인, 파일 해시), 취약점 정보를 수집·분석하여 보안 방어 의사결정에 활용 가능한 지식 체계.
- **STIX(Structured Threat Information eXpression)**: 사이버 위협 정보를 기계가 파싱하고 자동 처리할 수 있도록 JSON 기반의 그래프 구조(SDO, SRO)로 표현하는 OASIS 국제 표준 규격 (STIX 2.1).
- **TAXII(Trusted Automated eXchange of Intelligence Information)**: STIX 형식으로 작성된 위협 인텔리전스를 HTTPS 기반의 REST API 웹 서비스를 통해 조직 및 보안 장비 간에 안전하게 공유·전송하는 프로토콜.

</details>

- 정의/개념: 이기종 보안 장비 및 조직 간에 사이버 위협 정보를 실시간 기계 가독형(Machine-Readable)으로 표준화하는 **STIX(표현 언어)** 와, 이를 HTTPS RESTful API로 안전하게 배포하는 **TAXII(전송 프로토콜)** 로 구성된 **글로벌 위협 정보 자동 교환 프레임워크**
- 배경/필요성: 자연어 PDF 문서 중심의 정적 위협 보고서로 인한 수동 입력 지연 및 형식 불일치 문제를 극복하고, 제로데이 위협 지표를 방화벽, SIEM, SOAR로 1초 내에 실시간 주입하여 선제 방어(Proactive Defense)를 달성할 요구

#### 한줄 요약
- STIX의 그래프 기반 위협 정보 표준화와 TAXII의 RESTful 전송을 통해 CTI의 자동 교환 및 실시간 방어를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **STIX 도메인 객체(SDO) 및 관계 객체(SRO)**: 위협 행위자, 악성코드, 취약성, 침해 지표 등의 엔티티를 정의하는 SDO(Domain Objects)와 이들 간의 연관성(예: `uses`, `targets`, `indicates`)을 연결하는 SRO(Relationship Objects).
- **트래픽 라이트 프로토콜(Traffic Light Protocol, TLP)**: 정보의 민감도와 공유 허용 범위를 4개 등급(TLP:RED, TLP:AMBER+STRICT, TLP:AMBER, TLP:GREEN, TLP:CLEAR)으로 분류하여 무분별한 기밀 유출을 통제하는 공유 규약.

</details>

- **그래프 기반 문맥적 위협 모델링 (STIX SDO/SRO)**: 단순 IP 나열을 탈피하여 공격자 그룹 $\rightarrow$ 공격 기법(MITRE ATT&CK) $\rightarrow$ 대상 취약점의 전체 인과 관계 구조화
- **HTTPS 기반 안전한 RESTful 전송 (TAXII 2.1)**: JSON 페이로드와 OpenAPI 3.0 규격을 채택하여 웹 친화적인 엔드포인트(Collection, Channel) 통신 제공
- **정밀한 정보 공유 거버넌스 (TLP & 생애주기)**: TLP 등급에 따른 접근 인가 및 지표의 유효기간(Valid-Until) 설정을 통한 낡은 지표(Stale IoC) 자동 만료

#### 한줄 요약
- SDO/SRO 그래프 모델링, TAXII RESTful 전송, TLP 기반 공유 통제 및 IoC 유효기간 관리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII 컬렉션(Collection)**: TAXII 서버 내부에서 특정 주제나 TLP 등급별로 STIX 위협 객체들을 그룹화하여 인가된 클라이언트가 폴링(Polling)할 수 있도록 제공하는 인터페이스.
- **침해 지표(Indicator of Compromise, IoC)**: 시스템이나 네트워크에서 침해 사실을 식별할 수 있는 관측 가능한 기술적 패턴(IP, URL, MD5/SHA-256 해시, YARA 룰).

</details>

```text
[ 외부 CTI 제공기관 (KISA, ISAC, 상용 벤더) ]
                       │ (STIX 2.1 JSON 객체 생성)
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ TAXII 서버 (Trusted Automated Exchange Server) ]                      │
│  ├─ API Root / Discovery ── (지원 API 버전 및 컬렉션 목록 제공)           │
│  ├─ Collections ── (TLP 등급별 STIX 객체 저장소: RED / AMBER / GREEN)   │
│  └─ 사용자 인증 및 접근 제어 (mTLS, HTTP Basic / OAuth 2.0)             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (TAXII Client Polling / Push: HTTPS GET/POST)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 엔터프라이즈 보안 인프라 (CTI Consumer) ]                              │
│  ├─ SIEM / TIP (Threat Intelligence Platform) ──▶ (상관 분석 룰 자동 생성) │
│  ├─ SOAR 플랫폼 ──────────────────────────────▶ (자동 차단 플레이북 가동) │
│  └─ 방화벽 / IPS / EDR ────────────────────────▶ (IoC 블랙리스트 즉시 주입)│
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 외부 위협 정보가 STIX 규격으로 TAXII 서버에 게시되고, 기업의 SIEM, SOAR, 방화벽이 이를 구독(Poll)하여 실시간 방어 룰로 변환하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **STIX 도메인 객체 (SDO)** | Attack Pattern, Threat Actor, Indicator, Malware 등 위협 실체 정의 | OASIS STIX 2.1 |
| **STIX 관계 객체 (SRO)** | SDO 간의 인과적 관계(`relationship`, `sighting`)를 방향성 그래프로 결합 | Graph Model |
| **TAXII 서버 (Server)** | STIX 객체의 인덱싱, 컬렉션 관리, 접근 권한 통제 및 REST API 서비스 | TAXII 2.1 |
| **TAXII 클라이언트 (Consumer)**| 지정된 주기로 TAXII 서버를 폴링하여 최신 증분(Incremental) IoC 수집 | SIEM / SOAR 연동 |
| **TLP 정책 통제기** | 위협 정보의 유출 방지를 위해 TLP 등급별로 전송 대상 클라이언트 필터링 | FIRST TLP v2.0 |

#### 한줄 요약
- SDO/SRO 객체, TAXII 서버 컬렉션, TAXII 클라이언트, TLP 통제기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **증분 폴링(Incremental Polling)**: 매 요청마다 전체 DB를 전송받지 않고, `added_after` 파라미터를 사용하여 마지막 동기화 시점 이후에 새로 추가되거나 변경된 STIX 객체만을 수신하는 기법.

</details>

```text
1. 보안 분석 기관이 신규 APT 공격 캠페인을 분석하여 STIX 2.1 표준 JSON 객체(SDO/SRO) 생성
            │
            ▼
2. TLP:AMBER 공유 등급과 지표 유효기간(Valid-Until)을 부여하여 TAXII 서버의 전용 Collection에 게시
            │
            ▼
3. 기업의 TIP/SOAR 시스템이 TAXII API를 호출하여 최신 증분 위협 객체(Incremental STIX) 수집
            │
            ▼
4. STIX Indicator(악성 C&C IP)를 파싱하여 사내 방화벽 및 WAF 블랙리스트에 API로 자동 등록
            │
            ▼
5. 만료 기간 도래 시 방화벽 룰에서 자동 회수 ➔ 실제 침해 탐지 시 Sighting 객체를 생성하여 역피드백
```

**동작 원리**

1. **지식 구조화**: 공격 기법(T1059)과 악성 해시를 결합한 STIX 번들(Bundle) 생성
2. **보안 전송**: HTTPS mTLS 인증을 통해 TAXII 서버의 `/collections/{id}/objects/` 엔드포인트에 적재
3. **증분 동기화**: 클라이언트가 타임스탬프 기반 필터링으로 네트워크 대역폭 최소화 수집
4. **보안 장비 주입**: SOAR가 STIX 패턴을 방화벽 ACL 및 IDS Snort 룰로 자동 컴파일 배포
5. **생애주기 만료**: `valid_until` 만료 시 차단 룰을 자동 해제하여 오차단 방지

#### 한줄 요약
- STIX 번들 생성, TAXII 컬렉션 게시, 증분 폴링 수집, 방화벽 룰 자동 주입, 유효기간 만료 회수 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX 1.x (XML) vs STIX 2.x (JSON-Graph)**: 복잡하고 무거운 XML 기반에서 직관적인 JSON 기반의 분산 그래프 객체 모델로의 진화.

</details>

| 비교 항목 | 1세대 CTI 공유 (STIX 1.x / TAXII 1.x) | 차세대 CTI 공유 (STIX 2.1 / TAXII 2.1) |
|:---|:---|:---|
| **데이터 표현 형식** | **XML 기반 스키마 (무겁고 파싱 복잡)** | **JSON 기반 분산 그래프 객체 (가볍고 직관적)** |
| **객체 모델 구조** | 거대한 단일 문서(Monolithic Document) 계층 구조 | **독립된 SDO/SRO 노드-엣지 그래프 네트워크** |
| **전송 프로토콜** | SOAP / XML over HTTP (별도 메시지 프로토콜) | **RESTful API / JSON over HTTPS (OpenAPI 3.0)** |
| **연동 편의성** | 파서 개발 난이도 높음, 실시간 연동 지연 | **Python/REST 친화적, SOAR/SIEM 네이티브 지원** |
| **문맥 표현력** | 정적 지표 나열 위주 | **공격자-기법-취약점-지표 간 다차원 관계 표현** |

#### 한줄 요약
- STIX/TAXII 2.1은 JSON 그래프 모델과 REST API를 채택하여 실시간 보안 자동화에 최적화되었다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **낡은 지표(Stale IoC) 오차단**: 클라우드 IP의 동적 재할당 특성으로 인해 과거 악성 C&C였던 IP가 정상 웹 서비스로 변경되었음에도 방화벽에서 지속 차단하여 발생하는 정상 트래픽 차단 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동적 IP 재할당 환경에서 만료된 악성 IP의 지속 차단으로 인한 **정상 서비스 오차단 발생** | STIX 객체의 **`valid_until` 필드 강제 적용 및 TTL 경과 시 방화벽 룰 자동 만료** | 낡은 지표(Stale IoC) 오차단 제거 및 정책 테이블 메모리 보존 |
| TLP 공유 규약 위반으로 인한 기밀 위협 인텔리전스의 외부 비인가 유출 사고 | TAXII 서버의 **OAuth 2.0/mTLS 역할 기반 접근 제어(RBAC) 및 TLP 필터링** | TLP 등급별 엄격한 수신자 격리 및 CTI 기밀성 100% 보장 |
| 이종 보안 장비별 STIX 파싱 불일치로 인한 차단 룰 적재 누락 및 오작동 | 전용 **TIP(Threat Intelligence Platform) 기반의 룰 정규화 및 사전 문법 검증** | 장비별 이질성 해소 및 100% 무손실 보안 정책 자동 배포 달성 |

#### 한줄 요약
- 유효기간 설정으로 오차단을 방지하고, TLP 접근 제어로 기밀성을 보장하며, TIP 정규화로 파싱 누락을 차단한다.

## Ⅶ. 결론

- 지능형 APT 공격에 대한 집단 면역 체계를 구축하기 위해 **OASIS STIX 2.1 및 TAXII 2.1 표준 기반의 위협 인텔리전스 공유 체계**를 필수 도입하되, 정보의 신뢰성과 운영 효율성을 확보하기 위해 **TLP 기반 다계층 거버넌스**, **IoC 유효기간 자동 만료 메커니즘**, **SIEM/SOAR 연동 실시간 정책 주입 파이프라인**을 통합 구축하여 능동적 사이버 위협 대응 생태계를 완성

#### 한줄 요약
- STIX/TAXII 표준과 TLP 거버넌스 및 SOAR 연동을 통해 실시간 지능형 위협 대응을 구현한다.
