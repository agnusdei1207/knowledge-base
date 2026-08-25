---
sidebar:
  order: 33
  label: "033. MISP 위협 공유 플랫폼"
  badge:
    text: "기출 · 50%"
    variant: note
title: "오픈소스 사이버 위협 인텔리전스 공유 플랫폼 : MISP"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 33
extra:
  question_no: "33"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "이벤트(Event)/속성(Attribute)/객체(Object) 모델, Taxonomy/Galaxy 태깅, Sighting 관측 피드백, TLP 및 Warninglist"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MISP (Malware Information Sharing Platform)**: 침해사고 IoC, 공격자 TTP를 안전하게 수집, 검증, 공유하는 오픈소스 위협 인텔리전스 플랫폼.
- **Event-Centric Model (사건 중심 모델)**: 단편적 지표가 아닌 침해 사건(Event)을 중심으로 관련 속성과 공격자 맥락을 결합 관리하는 구조.

</details>

- 정의/개념: 침해사고 이벤트 단위로 IoC를 구조화하고 **Taxonomy/Galaxy 태깅, Warninglist 오탐 정제, Sighting 피드백으로 협업하는 CTI 공유 플랫폼**
- 배경/필요성: 개별 기관의 고립된 수동 위협 분석으로 인한 **동일 공격 그룹에 대한 중복 피해 발생, 위협 지표의 체계적 검증 및 자동 공유 체계 부재**

#### 한줄 요약
- 사건 중심 모델과 Warninglist 오탐 정제 및 Sighting 피드백을 통해 기관 간 위협을 실시간 신뢰 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Taxonomy & Galaxy**: 위협 공유 등급(TLP) 분류 체계(Taxonomy)와 공격자 그룹(APT), 악성코드 계열 등 심층 맥락(Galaxy)을 매핑하는 메타데이터.
- **Warninglists**: 구글 DNS, 마이크로소프트 CDN 등 정상 공용 IP/도메인을 등록해 두고 IoC 등록 시 오탐 경고를 띄워 차단을 방지하는 화이트리스트.

</details>

- **사건 중심(Event-Centric) 위협 맥락화**: 단편적 IP/해시를 넘어 **공격 대상, 사용 도구, MITRE ATT&CK TTP를 단일 사건으로 묶어 관리**
- **내장 Warninglist 기반 오탐 방어**: 정상 공용 인프라(8.8.8.8 등)가 **블랙리스트로 등록되는 오류를 사전 감지하여 오차단 사고 원천 차단**
- **집단지성 기반 사이팅(Sighting) 피드백**: 회원사들의 **실제 탐지(True Positive) 및 오탐 보고를 수렴하여 지표의 신뢰도와 유효 기간 자동 갱신**

#### 한줄 요약
- 사건 중심 맥락화, Warninglist 기반 오탐 방어, Sighting 집단지성 피드백을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Sharing Groups (공유그룹)**: 특정 금융 ISAC 회원사 등 사전에 인가된 신뢰 조직 간에만 위협 이벤트를 동기화하도록 제한하는 접근 통제 모델.

</details>

```text
[MISP 플랫폼 내부 구조 및 다자간 동기화 아키텍처]
|-- 1. Event Data Model (Event Container -> Attributes/Objects -> Taxonomy/Galaxy 태깅)
`-- 2. Verification Engine (Warninglist 정상 IP 대조 + Sighting 커뮤니티 피드백 수렴)
`-- 3. Sharing & Integration Layer (Sharing Groups 권한 통제 + STIX 2.1 / TAXII 2.1 서버)
    |-- MISP-to-MISP P2P Mesh Sync ──▶ 타 기관 MISP 인스턴스 (기관 간 위협 동기화)
    `-- PyMISP REST API ──▶ 사내 SIEM / SOAR / 차세대 방화벽 (실시간 자동 차단)
```

선의 의미: MISP가 이벤트를 생성하고 Warninglist와 Sighting으로 검증한 후 공유그룹 정책에 따라 타 기관 MISP 및 사내 보안 장비로 전송하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **이벤트 (Event)** | 단일 침해사고 맥락(Context)을 캡슐화하는 **최상위 컨테이너** | Event Container |
| **속성 및 객체** | 침해 지표(IP, Domain, File Hash, YARA 룰)의 **구체적 기술 값 정의** | IoC Data |
| **택소노미 및 갤럭시**| TLP 공유 등급 및 **MITRE ATT&CK TTP, APT 행위자 맥락 맵핑** | Taxonomy/Galaxy |
| **경고목록 (Warninglist)**| 정상 공용 IP/도메인 매칭 시 **경고 플래그를 부착하여 오차단 방지** | False Positive |
| **사이팅 엔진 (Sighting)**| 커뮤니티의 실제 관측 피드백을 수집하여 **신뢰도 점수 및 수명 갱신** | Feedback Metric |
| **STIX/TAXII 브릿지** | 외부 이종 보안 플랫폼과의 **글로벌 표준 상호운용성 보장** | Interoperability |

#### 한줄 요약
- 이벤트 컨테이너, 속성/객체, Taxonomy/Galaxy, Warninglist, Sighting 엔진, STIX/TAXII 브릿지가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MISP Sync (동기화)**: 다수 기관의 MISP 서버가 P2P 또는 Hub-and-Spoke 토폴로지로 연결되어 설정된 TLP 등급에 맞는 이벤트를 상호 복제하는 절차.

</details>

```text
이벤트 등록, 태깅, Warninglist 검증, 공유그룹 동기화 및 Sighting 환류 파이프라인
        │
   1. [이벤트 생성] 보안 분석가가 신규 침해 사건을 등록하고 IoC(C2 IP, 파일 해시) 입력
        │
   2. [맥락 보강 및 태깅] MITRE ATT&CK T1059 갤럭시 및 TLP:AMBER 택소노미 태그 부착
        │
   3. [오탐 필터링] MISP Warninglist 엔진이 정상 CDN/DNS IP 여부 자동 대조 ➔ [정상 인프라 제외]
        │
   4. [공유그룹 배포] 암호화된 REST API로 인가된 금융 ISAC 회원사 MISP 인스턴스로 동기화
        │
   ▼
5. [장비 적용 및 Sighting]
    ├─ 회원사 방화벽/SIEM이 PyMISP/TAXII API로 IoC를 인출하여 실시간 차단 적용
    └─ 탐지 발생 시 회원사가 MISP로 Sighting 피드백 전송 ➔ 해당 IoC 신뢰도 자동 상승
```

#### 한줄 요약
- 이벤트 생성 → Galaxy 태깅 → Warninglist 필터링 → 공유그룹 배포 → Sighting 관측 환류 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **비정형 수동 공유** vs **표준 프로토콜 (STIX/TAXII)** vs **위협 공유 플랫폼 (MISP)**.

</details>

| 비교 항목 | 비정형 수동 공유 (Email / PDF) | 표준 통신 프로토콜 (STIX / TAXII) | 위협 공유 플랫폼 (MISP) |
|:---|:---|:---|:---|
| **정보 표현 방식** | 자연어 텍스트, 비정형 문서 | **OASIS 표준 JSON 그래프 모델** | **이벤트-속성-갤럭시 복합 객체 모델** |
| **자동화 연동성** | **불가 (수동 복사 및 사람의 개입 필수)**| **매우 높음 (기계 대 기계 M2M 전송)** | **매우 높음 (PyMISP, REST API, WebUI)** |
| **오탐 검증 기제** | 없음 (전적으로 담당자 개인 역량 의존)| 지표 단위 메타데이터 제공 | **Warninglists + Sighting 피드백 내장** |
| **접근 권한 제어** | 수신 메일 주소 기반 (제어 한계) | TAXII API Authentication | **Sharing Groups, TLP, 기관별 정밀 제어**|
| **커뮤니티 협업** | 단방향 통보 중심 | 발행-구독(Pub-Sub) 중심 | **양방향 사건 토론, 공동 분석, Sighting**|

#### 한줄 요약
- 비정형 공유는 수동 비효율, STIX/TAXII는 표준 전송 파이프라인, MISP는 종합적인 협업·검증·공유 플랫폼이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PyMISP**: 파이썬 환경에서 MISP REST API를 호출하여 이벤트 생성, 지표 검색, SOAR 플레이북 연동을 자동화하는 공식 라이브러리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유된 오탐 IoC(공용 DNS 등)의 무조건 차단으로 인한 **사내 비즈니스 접속 마비** | **`MISP Warninglist 상시 활성화 및 Sighting 기반 신뢰도 임계치 필터링`** | 공용 IP 오차단 0% 달성 및 고신뢰 지표 선별 방어 |
| 극비 침해사고 정보가 미흡한 권한으로 인해 **외부 커뮤니티로 무단 노출되는 위험** | **`FIRST TLP 2.0 규약 준수 및 인가 파트너 전용 Sharing Group 격리`** | 민감 침해 정보 외부 노출 방지 및 규제 준수 |
| 이종 SIEM/SOAR 솔루션과의 API 규격 불일치로 인한 **실시간 자동 차단 실패** | **`PyMISP 자동화 스크립트 및 MISP 내장 STIX/TAXII 서버 모듈 활성화`** | 이기종 보안 장비 간 M2M 자동 연동 100% 달성 |
| 수십만 건의 IoC 누적으로 인한 데이터베이스 쿼리 성능 저하 | **`오래된 미관측(Zero Sighting) 지표 자동 만료(Decaying) 엔진`** 가동 | 고품질 유효 지표 유지 및 시스템 검색 성능 보존 |

#### 한줄 요약
- Warninglist로 오차단을 막고, Sharing Group으로 기밀을 보호하며, PyMISP/STIX로 장비 자동화를 구현한다.

## Ⅶ. 결론

- 글로벌 위협 행위자에 맞서 집단지성 기반의 협업 방어망을 구축하는 **MISP 위협 공유 플랫폼 아키텍처는 CTI 생태계의 대표적인 핵심 허브**이며, 실무 구현 시 **사건 중심(Event) 모델 기반의 TTP 맥락화, Warninglist 및 Sighting 엔진을 통한 지표 무결성 검증, TLP 2.0 및 Sharing Group 기반의 철저한 접근 통제, STIX/TAXII 표준 프로토콜 연동**을 결합하여 신뢰성 높고 능동적인 글로벌 사이버 방어 인프라 완성

#### 한줄 요약
- MISP는 사건 중심 모델과 Warninglist/Sighting 검증 및 TLP 공유그룹 통제를 통해 고신뢰 CTI 협업 생태계를 완성하는 오픈소스 플랫폼이다.