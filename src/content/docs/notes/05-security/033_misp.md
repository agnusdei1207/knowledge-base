---
sidebar:
  order: 33
  label: "033. MISP 위협 공유 플랫폼"
  badge:
    text: "기출 · 50%"
    variant: note
title: "오픈소스 사이버 위협 인텔리전스 공유 플랫폼 : MISP"
date: "2026-08-26T14:43:40+09:00"
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

- 정의/개념: 사건별 IoC를 검증·공유하는 **MISP CTI 플랫폼**
- 배경/필요성: 같은 침해 지표를 기관마다 따로 분석·오탐 검증하면 동일한 분석 비용이 회원사 수만큼 중복 발생하므로, 기관들 사이에 사건 단위 공유 저장소를 두어 관측 피드백(Sighting)과 오탐 목록(Warninglist)으로 검증 비용을 한 번에 분담할 계층이 필요

#### 한줄 요약
- 지표의 신뢰도를 생산자 한 곳의 판단이 아니라 회원사들의 관측 누적으로 결정하므로, 공유 범위를 넓힐수록 검증 품질은 올라가지만 기밀 노출 위험도 함께 커진다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Taxonomy & Galaxy**: 위협 공유 등급(TLP) 분류 체계(Taxonomy)와 공격자 그룹(APT), 악성코드 계열 등 심층 맥락(Galaxy)을 매핑하는 메타데이터.
- **Warninglists**: 구글 DNS, 마이크로소프트 CDN 등 정상 공용 IP/도메인을 등록해 두고 IoC 등록 시 오탐 경고를 띄워 차단을 방지하는 화이트리스트.

</details>

- **사건 중심(Event-Centric) 위협 맥락화**: 단편적 IP/해시를 넘어 **공격 대상, 사용 도구, MITRE ATT&CK TTP를 단일 사건으로 묶어 관리**
- **내장 Warninglist 기반 오탐 방어**: 정상 공용 인프라(8.8.8.8 등)가 **블랙리스트로 등록되는 오류를 사전 감지하여 오차단 사고 원천 차단**
- **집단지성 기반 사이팅(Sighting) 피드백**: 회원사들의 **실제 탐지(True Positive) 및 오탐 보고를 수렴하여 지표의 신뢰도와 유효 기간 자동 갱신**

#### 한줄 요약
- 지표를 사건에 묶어 두는 대가로 등록 시점에 맥락 입력 부담을 지지만, 그 덕에 IP 하나가 폐기돼도 같은 사건의 TTP와 도구 정보는 남아 재사용된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Sharing Groups (공유그룹)**: 특정 금융 ISAC 회원사 등 사전에 인가된 신뢰 조직 간에만 위협 이벤트를 동기화하도록 제한하는 접근 통제 모델.

</details>

```text
MISP 플랫폼
|-- 이벤트 데이터 모델
|   |-- 속성·객체
|   `-- Taxonomy·Galaxy
|-- 검증 엔진
|   |-- Warninglist
|   `-- Sighting
`-- 공유·연동 계층
    |-- Sharing Group
    `-- STIX·TAXII 브리지
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
- 데이터 모델과 공유 계층 사이에 Warninglist·Sighting 검증 엔진이 끼어들어 있어, MISP는 지표를 전달만 하는 STIX/TAXII와 달리 전달 전에 품질을 거르는 비용을 자체 부담한다.

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
- 3단계에서 정상 인프라로 걸러진 지표는 배포 비용 없이 소멸하는 반면 통과한 지표는 회원사 장비에 인라인 차단으로 박히므로, 오탐 한 건의 비용은 필터 앞뒤에서 자릿수가 달라진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **비정형 수동 공유 (Email / PDF)**: 침해 정보를 자연어 문서로 주고받아 수신 측 담당자가 직접 읽고 장비에 옮겨 적음으로써, 도입 비용은 없지만 지표 하나마다 사람의 개입 비용을 반복해서 치르는 방식.
- **표준 통신 프로토콜 (STIX / TAXII)**: 위협 정보를 규격화된 객체로 직렬화해 기계 간 전송만 담당함으로써 변환·전달 비용을 없애되, 지표의 진위 검증은 여전히 각 소비자에게 남겨 두는 전송 계층.
- **위협 공유 플랫폼 (MISP)**: 전송에 더해 이벤트 저장·태깅·Warninglist 대조·Sighting 집계까지 한 인스턴스에서 수행해, 회원사가 개별로 치르던 검증 비용을 커뮤니티 단위로 통합하는 협업 플랫폼.

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
- 실무 대책은 대부분 공유 폭을 좁혀 안전을 사는 거래이므로, Sharing Group 격리와 Decaying으로 얻는 기밀성·성능은 커뮤니티 지표의 커버리지를 일부 포기한 대가로 성립한다.

## Ⅶ. 결론

- 제한 공유는 **Sharing Group**, 자동 검증은 **Sighting** 적용

#### 한줄 요약
- MISP는 사건 중심 모델과 Warninglist/Sighting 검증 및 TLP 공유그룹 통제를 통해 고신뢰 CTI 협업 생태계를 완성하는 오픈소스 플랫폼이다.
