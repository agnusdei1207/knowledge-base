---
sidebar:
  order: 96
  label: "096. 위협 인텔리전스 (STIX/TAXII)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 인텔리전스 표현 및 전송 표준 : STIX 및 TAXII"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: **STIX 표현**과 **TAXII 전송** 기반 CTI 공유 표준
- 배경/필요성: 글로벌 사이버 위협이 조직화·고도화됨에 따라 공격자(Threat Actor), 공격 기법(TTP), 침해 지표(IoC) 등의 사이버 위협 인텔리전스(CTI)를 유관 기관 및 보안 기업 간에 신속히 공유해야 하나, 과거에는 비정형 텍스트(이메일/PDF)나 벤더별 독점 XML 포맷으로 유통되어 수신 측에서 수동 파싱 및 정규화에 막대한 시간을 소모하고 방화벽·SIEM으로의 기계적 자동 연동이 불가능했던 한계를 극복하기 위해, 위협 정보를 JSON 기반 그래프 관계형 객체(SDO/SRO)로 표준 구조화하는 STIX(Structured Threat Information eXpression)와 이를 HTTPS REST API로 안전하게 실시간 교환하는 TAXII(Trusted Automated eXchange of Intelligence Information) 표준을 도입하여 **기계 판독 가능한(Machine-Readable) CTI 공유 자동화, SIEM/SOAR/방화벽 실시간 방어 정책 자동 주입 및 글로벌 집단 사이버 방어 생태계**를 달성할 필요

#### 한줄 요약
- STIX 구조화 언어와 TAXII 전송 프로토콜을 결합하여 위협 인텔리전스를 실시간 자동 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SDO vs SRO (STIX Domain/Relationship Objects)**: 위협 실체(Indicator, Malware 등)를 나타내는 도메인 객체(SDO)와 이들 간의 인과 관계(`indicates`, `uses`)를 나타내는 관계 객체(SRO).
- **TLP (Traffic Light Protocol, v2.0)**: 위협 정보의 공유 범위를 RED(비공개), AMBER(조직 한정), GREEN(커뮤니티), CLEAR(전체 공개) 4단계로 통제하는 규약.

</details>

- **SDO/SRO 그래프**: 위협 실체와 **인과관계 구조화**
- **TAXII REST API**: SIEM·SOAR와 **증분 폴링** 연동
- **TLP 2.0**: 등급별 **공유 범위 통제**

#### 한줄 요약
- JSON 그래프 모델링, RESTful 고속 전송, TLP 기반 정보 공유 거버넌스를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TAXII Collections**: 특정 위협 주제 또는 TLP 공유 등급별로 STIX 객체들을 그룹화하여 호스팅하는 서버 상의 데이터 저장소.

</details>

```text
[CTI 공유 체계]
|-- STIX SDO       : 위협 실체 표현
|-- STIX SRO       : 객체 관계 표현
|-- TAXII 서버     : 컬렉션·API 제공
|-- TAXII 클라이언트: 증분 IoC 수집
`-- TLP 통제기     : 공유 범위 제한
```

선의 의미: 외부 위협 정보가 STIX 규격으로 TAXII 서버에 게시되고 기업의 SIEM, SOAR, 방화벽이 이를 구독하여 실시간 방어 룰로 변환하는 구조

| 구성요소 | 책임 |
|:---|:---|
| STIX SDO | 공격자·기법·지표 등 **위협 실체 정의** |
| STIX SRO | 객체 간 **관계·관측 표현** |
| TAXII 서버 | 컬렉션·접근 통제와 **REST API 제공** |
| TAXII 클라이언트 | 최신 **증분 IoC 수집** |
| TLP 통제기 | 등급별 **수신자 필터링** |

#### 한줄 요약
- STIX가 위협을 객체와 관계로 나눠 표현하고 TAXII 컬렉션이 그 묶음의 배포 단위를 맡으므로, 데이터 모델링과 공유 범위 통제가 서로 얽히지 않고 다뤄진다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Incremental Polling (증분 폴링)**: `added_after` 파라미터로 마지막 동기화 이후 새로 추가/변경된 STIX 객체만 수신하여 네트워크 대역폭을 절감하는 기법.

</details>

```text
CTI 생산자
    |
 1. STIX 번들 생성
    |
 2. TAXII 컬렉션 게시
    |
 3. 증분 IoC 수집
    |
 4. 방화벽 규칙 배포
    |
 5. 만료 규칙 회수
    |
보안 통제 장비
```

동작 원리

1. STIX 번들 생성
2. TAXII 컬렉션 게시
3. 증분 IoC 수집
4. 방화벽 규칙 배포
5. 만료 규칙 회수

#### 한줄 요약
- 유효기간 도달 시 룰 유지와 자동 회수로 갈리며, 회수하지 않으면 낡은 IoC가 그대로 정상 트래픽 오차단 비용으로 남는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STIX 1.x (XML)** vs **STIX 2.x (JSON-Graph)**: 무거운 단일 문서 스키마에서 가벼운 분산 그래프 RESTful 모델로의 진화.

</details>

| 비교 항목 | 1세대 CTI 공유 (STIX 1.x / TAXII 1.x) | 차세대 CTI 공유 (STIX 2.1 / TAXII 2.1) |
|:---|:---|:---|
| 데이터 표현 형식 | **XML 스키마** | **JSON 그래프 객체** |
| 객체 모델 구조 | 단일 문서 계층 | 독립 **SDO/SRO 그래프** |
| 전송 프로토콜 | SOAP/XML over HTTP | **REST/JSON over HTTPS** |
| 연동 편의성 | 파서 복잡·연동 지연 | SIEM·SOAR 연동 용이 |
| 문맥 표현력 | 정적 지표 나열 | 위협 실체 간 **다차원 관계** |

#### 한줄 요약
- STIX/TAXII 2.1은 JSON 그래프 모델과 REST API를 채택하여 실시간 보안 자동화에 최적화되었다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Stale IoC (낡은 지표 오차단)**: 클라우드 IP 동적 재할당으로 과거 악성 C&C였던 IP가 정상 서비스로 변경된 후에도 방화벽에서 지속 차단되어 발생하는 오차단 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 만료 IoC로 **정상 서비스 오차단** | **valid_until·TTL**로 규칙 회수 | 낡은 지표와 정책 낭비 제거 |
| TLP 위반으로 **기밀정보 유출** | **mTLS·RBAC·TLP 필터** 적용 | 등급별 수신자 격리 |
| 파싱 차이로 **규칙 적재 누락** | **TIP 정규화·사전 검증** | 장비별 정책 변환 일관성 확보 |
| 대량 IoC로 **ACL 용량 초과** | **신뢰도 상위 지표** 우선 주입 | TCAM 자원 고갈 방지 |

#### 한줄 요약
- 유효기간 설정으로 오차단을 방지하고, TLP 접근 제어로 기밀성을 보장하며, TIP 정규화로 파싱 누락을 차단한다.

## Ⅶ. 결론

- 파편화된 사이버 위협 지표를 단일화된 글로벌 표준 규격으로 구조화하고 실시간 기계 간 자동 연동을 실현하는 **글로벌 사이버 위협 인텔리전스(CTI) 유통 및 집단 방어의 가장 보편적이고 핵심적인 표준 프레임워크(OASIS 표준)**로 확립되었으며, MITRE ATT&CK 프레임워크 및 위협 인텔리전스 플랫폼(TIP)과의 심층 결합으로 진화하는 가운데, 실무 STIX/TAXII 연동 인프라 구축 시에는 **과거 악성 IP가 정상 서비스로 재할당되었을 때 오차단을 방지하는 유효기간(valid_until/TTL) 기반 자동 룰 회수(Stale IoC 방지), 조직별 민감 정보 유출을 차단하는 TLP 2.0 기반 엄격한 접근 통제, 방화벽 하드웨어 TCAM 용량 고갈을 방지하는 신뢰도(Confidence Score) 기반 상위 지표 선별 주입**을 결합하여 완벽한 CTI 운영 신뢰성을 완성

#### 한줄 요약
- STIX/TAXII 표준과 TLP 거버넌스 및 SOAR 연동을 통해 실시간 지능형 위협 대응을 구현한다.
