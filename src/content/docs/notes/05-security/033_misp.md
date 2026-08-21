---
sidebar:
  order: 33
  label: "033. MISP 위협 공유 플랫폼 (MISP)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "오픈소스 사이버 위협 인텔리전스 공유 플랫폼 : MISP (Open Source Threat Sharing)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 33
extra:
  question_no: "033"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "이벤트(Event)/속성(Attribute)/객체(Object) 모델, Taxonomy/Galaxy 태깅, Sighting 관측 피드백, TLP 및 Warninglist"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **MISP(Malware Information Sharing Platform / Open Source Threat Intelligence Platform)**: 조직 간 사이버 침해사고 데이터, 악성코드 IoC, 공격자 TTP, 금융 사기 지표를 안전하게 수집, 상관분석, 정제 및 상호 공유하기 위해 EU 및 글로벌 보안 커뮤니티가 개발한 오픈소스 위협 인텔리전스 공유 플랫폼.
- **사건 중심 데이터 모델(Event-Centric Data Model)**: 단편적인 악성 IP나 해시값을 개별적으로 관리하지 않고, 특정 침해사고나 캠페인을 단일 '이벤트(Event)'로 정의한 후 하위에 속성(Attributes), 객체(Objects), 위협 행위자(Galaxy)를 유기적으로 바인딩하는 아키텍처.

</details>

- 정의/개념: 침해사고 이벤트 단위로 IoC를 구조화하고, **Taxonomy/Galaxy 기반 맥락 부여**, **Warninglist 기반 오탐 정제**, **Sighting 기반 커뮤니티 교차 검증**, **STIX/TAXII 표준 상호 연동** 을 제공하는 **오픈소스 CTI 플랫폼 아키텍처**
- 배경/필요성: 폐쇄적인 1:1 이메일/문서 기반 위협 공유가 가진 공유 지연, 이기종 장비 연동 한계, 그리고 민감 기밀 정보의 공유 경계 통제 부재를 극복하고 글로벌 신뢰 기반의 협업 방어망을 구축할 요구

#### 한줄 요약
- 이벤트 중심 데이터 모델과 Sighting 교차 검증 및 TLP 공유그룹 제어로 신뢰성 높은 CTI 공유를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MISP 택소노미(Taxonomy) & 갤럭시(Galaxy)**:
  - **택소노미(Taxonomy)**: 이벤트에 부착하는 표준화된 분류 태그(예: TLP 등급, NIST CSWP 분류, 악성코드 패밀리).
  - **갤럭시(Galaxy)**: 고차원 위협 맥락(예: MITRE ATT&CK TTP, APT 공격 그룹, 위협 행위자 프로파일)을 클러스터 형태로 이벤트에 맵핑하는 지식 모델.
- **사이팅(Sighting / 관측 피드백)**: 공유받은 위협 지표가 실제 자사 보안 장비(SIEM/EDR)에서 탐지(Hit)되었는지, 혹은 정상 자산으로 오탐(False Positive)되었는지를 원 게시자 및 커뮤니티에 피드백하여 지표의 신뢰도와 유효기간을 집단지성으로 갱신하는 기능.

</details>

- **자동 상관분석 (Correlation Engine)**: 신규 등록된 IoC가 과거 등록된 타 조직의 침해 이벤트와 일치할 경우 자동으로 연관 링크 생성
- **다단계 오탐 방지 (Warninglists)**: 클라우드플레어, 구글 DNS, 마이크로소프트 등 정상 공용 IP/도메인 목록과 대조하여 오탐 자동 필터링
- **세분화된 공유 제어 (Sharing Groups & TLP)**: 커뮤니티 전체, 특정 산업군(ISAC), 또는 1:1 파트너로 정보 열람 범위를 암호학적으로 제약

#### 한줄 요약
- 이벤트 상관분석, Galaxy 맥락화, Sighting 집단지성 검증, Warninglist 오탐 필터링, 세분화된 공유 통제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MISP 경고목록(Warninglist)**: 검색 엔진 크롤러, 공용 DNS 서버, CDN IP 등 정상적인 인터넷 인프라 주소가 실수로 악성 IoC로 등록되어 대규모 서비스 장애(오차단)를 유발하는 것을 방지하는 정규화 화이트리스트 데이터베이스.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ MISP 플랫폼 코어 아키텍처 (Threat Intelligence Hub) ]                │
│  ├─ 1. 이벤트 계층 (Event Layer): 사건 ID, 제목, 일시, 조직 정보        │
│  │     ├─ 속성 및 객체 (Attributes & Objects): IP, Hash, CVE, 이메일    │
│  │     ├─ 분류 태그 (Taxonomies): TLP 2.0 (AMBER), PAP, 신뢰도 등급     │
│  │     └─ 지식 성단 (Galaxies): MITRE ATT&CK TTP, Threat Actor (Lazarus)│
│  │                                                                      │
│  ├─ 2. 정제 및 검증 엔진:                                               │
│  │     ├─ Warninglist (정상 공용 IP 대조 ➔ 오탐 지표 자동 플래그)        │
│  │     └─ Sighting Engine (커뮤니티 관측 피드백 수렴 ➔ 신뢰도 점수 갱신)│
│  │                                                                      │
│  └─ 3. 공유 및 전송 계층:                                               │
│       ├─ 공유그룹 (Sharing Groups): 특정 금융권 회원사 전용 접근 통제   │
│       └─ STIX 2.1 / TAXII 2.1 서버: 외부 SIEM/SOAR/방화벽 실시간 연동   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼ (MISP-to-MISP 동기화)                 ▼ (보안 장비 API 연동)
   [ 타 기관 MISP 인스턴스 (P2P Mesh) ]         [ 사내 SIEM / SOAR / 차세대 방화벽 ]
```

선의 의미: MISP가 이벤트를 생성하고 Warninglist와 Sighting으로 검증한 후, 공유그룹 정책에 따라 타 기관 MISP 및 사내 보안 장비로 전송하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **이벤트 (Event)** | 단일 침해사고 맥락(Context)을 캡슐화하는 최상위 컨테이너 | Event Container |
| **속성 및 객체 (Attributes)** | 침해 지표(IP, Domain, File Hash, YARA 룰)의 구체적 기술 값 정의 | IoC Data |
| **택소노미 및 갤럭시** | TLP 공유 등급 및 MITRE ATT&CK TTP, APT 행위자 맥락 맵핑 | Taxonomy / Galaxy |
| **경고목록 (Warninglist)** | 정상 인프라 IP/도메인 매칭 시 경고 플래그를 부착하여 오차단 방지 | False Positive Filter|
| **사이팅 엔진 (Sighting)** | 커뮤니티의 실제 탐지/미탐/오탐 피드백을 수집하여 지표 수명 자동 연장/단축 | Feedback Metric |
| **STIX/TAXII 브릿지** | 외부 이종 보안 플랫폼과의 글로벌 표준 상호운용성 보장 | Interoperability |

#### 한줄 요약
- 이벤트 컨테이너, 속성/객체, Taxonomy/Galaxy, Warninglist, Sighting 엔진, STIX/TAXII 브릿지가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **MISP 인스턴스 간 동기화(MISP Sync)**: 여러 기관의 MISP 서버가 P2P 또는 Hub-and-Spoke 토폴로지로 연결되어, 설정된 공유 필터(Push/Pull 규칙 및 TLP 등급)에 부합하는 이벤트만을 상호 암호화 동기화하는 분산 아키텍처.

</details>

```text
1. [이벤트 생성] 보안 분석가가 신규 랜섬웨어 공격 사건을 등록하고 IoC(C2 IP, 파일 해시) 입력
            │
            ▼
2. [맥락 보강 및 태깅] MITRE ATT&CK T1059(PowerShell) 갤럭시 및 TLP:AMBER 택소노미 태그 부착
            │
            ▼
3. [오탐 필터링] MISP Warninglist 엔진이 정상 CDN/DNS IP 여부 자동 대조 ➔ [정상 인프라 검출 시 제외]
            │
            ▼
4. [인가된 공유그룹 배포] 암호화된 REST API를 통해 신뢰된 금융 ISAC 회원사 MISP 인스턴스로 이벤트 동기화
            │
            ▼
5. [장비 적용 및 관측 환류]
    ├─ 회원사 방화벽/SIEM이 PyMISP/TAXII API로 IoC를 인출하여 실시간 차단 룰 적용
    └─ 탐지 발생 시 회원사가 MISP로 Sighting(True Positive) 피드백 전송 ➔ 해당 IoC 신뢰도 자동 상승
```

**동작 원리**

1. **지표 정형화 입력**: 비정형 텍스트를 파싱하여 정규 표현식 기반 MISP Object로 구조화
2. **다차원 태깅**: 정보 공유 규약(TLP)과 위협 수준을 표준화된 메타데이터로 고정
3. **사전 오탐 정제**: 100개 이상의 글로벌 화이트리스트 목록과 실시간 교차 검증
4. **선택적 복제 전송**: Sharing Group 규칙에 따라 권한이 부여된 테넌트로만 이벤트 복제
5. **동적 신뢰도 거버넌스**: 다수 조직의 Sighting 응답 비율을 기반으로 지표의 유효 수명(TTL) 자동 조정

#### 한줄 요약
- 이벤트 생성, Galaxy 태깅, Warninglist 필터링, 공유그룹 배포, Sighting 관측 환류 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **위협 정보 공유 방식 비교**: 비정형 수동 공유(Email/PDF), 표준 프로토콜(STIX/TAXII), 종합 위협 플랫폼(MISP)의 비교.

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

- **PyMISP**: 파이썬 환경에서 MISP REST API를 호출하여 이벤트 생성, 속성 검색, 지표 추출, SOAR 플레이북 연동을 자동화하는 공식 클라이언트 라이브러리.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 타 기관에서 공유된 오염/오탐 IoC(공용 DNS 등)의 무조건 차단으로 인한 **사내 비즈니스 접속 마비** | **MISP Warninglist 상시 활성화 및 Sighting 기반 신뢰도 점수(Confidence) 임계치 필터링** | 정상 비즈니스 공용 IP 오차단 0% 달성 및 고신뢰 위협 지표만 선별 방어 |
| 극비 침해사고 정보가 미흡한 권한 설정으로 인해 **외부 커뮤니티로 무단 노출되는 기밀 유출 위험** | **FIRST TLP 2.0 규약 준수 및 인가된 특정 파트너만 지정하는 Sharing Group 격리** | 민감한 내부 침해 정보의 외부 노출 방지 및 법적 컴플라이언스 준수 |
| 이종 SIEM/SOAR 솔루션과의 API 연동 규격 불일치로 인한 **실시간 위협 지표 차단 자동화 실패** | **PyMISP 기반 자동화 스크립트 구축 및 MISP 내장 STIX 2.1/TAXII 2.1 서버 모듈 활성화** | 이기종 보안 장비 간 M2M 자동화 연동 100% 달성 및 수동 등록 오버헤드 소거 |

#### 한줄 요약
- Warninglist로 오차단을 막고, Sharing Group으로 기밀을 보호하며, PyMISP/STIX로 장비 자동화를 구현한다.

## Ⅶ. 결론

- 글로벌 위협 행위자에 맞서 집단지성 기반의 협업 방어망을 구축하는 **MISP 위협 공유 플랫폼 아키텍처**는 CTI 생태계의 대표적인 핵심 허브이며, 실무 구현 시 **사건 중심(Event) 모델 기반의 TTP 맥락화**, **Warninglist 및 Sighting 엔진을 통한 지표 무결성 검증**, **TLP 2.0 및 Sharing Group 기반의 철저한 접근 통제**, **STIX/TAXII 표준 프로토콜 연동**을 결합하여 신뢰성 높고 능동적인 글로벌 사이버 방어 인프라를 완성

#### 한줄 요약
- 사건 중심 모델과 Warninglist/Sighting 검증 및 TLP 공유그룹 통제를 통해 고신뢰 CTI 협업 생태계를 완성한다.
