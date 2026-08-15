---
sidebar:
  order: 33
  label: "033. MISP 위협 공유 플랫폼 (MISP)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "MISP 위협 공유 플랫폼 (MISP)"
date: "2026-08-13T18:58:00+09:00"
tags:
  - "notes-security"
weight: 33
extra:
  question_no: "033"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출이나 특정 플랫폼 단독 답안 비중은 낮음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **악성코드 정보 공유 플랫폼(Malware Information Sharing Platform, MISP)**: 위협 사건•지표•관측 데이터를 자동 상관 분석하고 기관 간 안전하게 공유하는 오픈소스 위협 인텔리전스 플랫폼.
- **사이버 위협 인텔리전스(Cyber Threat Intelligence, CTI)**: 위협 데이터에 공격자•전술•신뢰도•영향 맥락을 부여한 정형 지식.

</details>

- 정의/개념: CTI 상관 분석과 공유를 통제하는 **MISP**
- 배경/필요성: 단편 지표만으로는 **사건 맥락•공유 권한** 관리 불가

#### 한줄 요약

- 이종 위협 지표 간 자동 상관 분석 및 조직 간 안전한 선택적 정보 공유를 지원함.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **분류체계(Taxonomy)**: 위협 정보에 TLP, 신뢰 등급, 산업 분류 등의 분류 태그를 표준화하여 부여하는 체계.
- **갤럭시(Galaxy)**: 위협 행위자, 기법, 악성코드 툴킷 등 고차원 위협 맥락 지식을 맵핑하는 묶음 구조.
- **관측(Sighting)**: 공유된 지표가 실제 조직 환경에서 탐지되거나 오탐된 사례 및 시각을 기록한 피드백 데이터.

</details>

- 이벤트 중심 사건•지표 데이터 및 관측 맥락 통합.
- 표준 **분류체계(Taxonomy)** 및 **갤럭시(Galaxy)** 기반 고차원 위협 태깅.
- 지표 간 상관관계 자동 분석 및 **관측(Sighting)** 데이터를 활용한 유효성 검증.

#### 한줄 요약

- 이벤트 맥락 표현을 위한 태깅과 실제 탐지 관측 피드백을 통해 지표 유효성을 검증함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **이벤트(Event)**: 관련 속성, 지표, 맥락 정보를 하나의 사건 단위로 카테고리화한 MISP 분석 기본 단위.
- **공유그룹(Sharing Group)**: 위협 정보의 열람•재배포 권한을 특정 조직 집합으로 제한하는 통제 메커니즘.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 외부 보안 장비 및 SIEM/SOAR과의 자동화 연동을 위한 RESTful 규약.

</details>

```text
MISP 플랫폼 구조
├─ 이벤트•분석
│  ├─ 속성•객체
│  ├─ 분류•갤럭시
│  └─ 상관•관측
└─ 공유 정책
```

가지의 의미: 이벤트의 분석 정보와 이를 통제하는 공유 정책의 포함 관계를 표현.

| 구성요소 | 책임 |
|:---|:---|
| 이벤트•분석 | **이벤트** 기반 사건 맥락 및 속성 통합 |
| 속성•객체 | 구조화 지표(IoC) 및 상세 관측 정보 표현 |
| 분류•갤럭시 | **분류체계**•**갤럭시** 기반 위협 맥락 및 취급 등급 태깅 |
| 상관•관측 | **관측** 피드백 기반 지표 적중 및 오탐 추적 |
| 공유 정책 | **API** 및 **공유그룹** 기반 정보 동기화 권한 통제 |

#### 한줄 요약

- 분석 이벤트와 연관 속성을 공유 그룹 단위로 세밀하게 권한 통제함.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **경고목록(Warninglist)**: Google DNS, CDN 등 정상 주소를 위협 지표로 오인하는 오탐을 방지하기 위한 예외 검증 목록.
- **트래픽 라이트 프로토콜(Traffic Light Protocol, TLP)**: RED, AMBER, GREEN, CLEAR 4가지 색상으로 위협 정보의 공유 허용 범위를 명시하는 공유 규약.
- **분류•갤럭시 보강(Context Enrichment)**: 이벤트에 위협 행위자, TTP 및 TLP 취급 태그를 추가하는 단계.
- **경고목록•상관•관측 검증(Validation & Correlation)**: 경고목록 대조, 기존 이벤트 상관 분석 및 관측 데이터로 유효성을 검증하는 단계.
- **TLP•공유그룹 게시(Targeted Publication)**: TLP 등급과 지정된 공유그룹 정책을 적용하여 수신 조직에 배포하는 단계.
- **지표 품질 재평가(Indicator Quality Re-assessment)**: 피드백 관측을 수집하여 지표의 유효 상태, 신뢰 점수 및 수명을 갱신하는 단계.

</details>

```text
사건•속성 등록
        │
        ▼
1. 분류•갤럭시 보강
        │
        ▼
2. 경고목록•상관•관측 검증
        ├─ 정상•중복 ── 게시 제외
        └─ 유효 지표
                │
                ▼
3. TLP•공유그룹 게시
        └─ 허용 조직에만 배포
                │
                ▼
API 적중•오탐 관측 등록
        │
        ▼
4. 지표 품질 재평가
        └─ 상태•신뢰도•공유 범위 갱신
```

### 동작 원리

1. **분류•갤럭시 보강**: 위협 맥락 및 TLP 취급 태그 부여.
2. **경고목록•상관•관측 검증**: **경고목록(Warninglist)** 대조 및 **관측(Sighting)** 데이터를 통한 유효성 검증.
3. **TLP•공유그룹 게시**: **TLP(Traffic Light Protocol)** 및 **공유그룹(Sharing Group)** 기반 차등 배포.
4. **지표 품질 재평가**: 관측 피드백 수집 기반 신뢰 점수 및 유효 상태 갱신.

#### 한줄 요약

- 경고목록 기반 오탐 필터링 및 TLP 통제 배포 후 관측 데이터로 지표 수명을 재평가함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **구조화 위협 정보 표현(Structured Threat Information eXpression, STIX)**: 위협 객체와 연관 관계를 표현하는 표준 언어.
- **신뢰 정보 자동 교환(Trusted Automated eXchange of Intelligence Information, TAXII)**: STIX 위협 데이터를 안전하게 전송하는 프로토콜.

</details>

| 위협 정보 공유 | 문서 공유 | STIX/TAXII | MISP |
|:---|:---|:---|:---|
| 적용 기준 | 소규모 비정형 정보 전달 | 기관 간 표준 자동 교환 | 분석•권한•동기화 통합 |
| 핵심 특징 | 사람이 읽는 지표•설명 | **STIX**•**TAXII**의 표준 객체•자동 교환 | **MISP**의 사건•상관•관측 운영 |
| 한계 | 수동 파싱•갱신 누락 | 형식만으로 품질 보장 불가 | 태그•권한 오류 확산 |

> 요약: 분석•상관 기능 중심의 통합 위협 공유 플랫폼 운영.

#### 한줄 요약

- 이종 시스템 연동 표준인 STIX/TAXII와 연계하여 사건 맥락 중심 상관 분석을 구동함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **사고 대응•보안 팀 포럼(Forum of Incident Response and Security Teams, FIRST)**: 전 세계 침해사고대응팀(CSIRT) 간 글로벌 협력 포럼.
- **FIRST TLP 2.0**: 위협 정보의 기밀성 수준과 정보 공유 경계를 표준 정의한 최신 규격.
- **구조화 정보 표준 발전 기구(Organization for the Advancement of Structured Information Standards, OASIS)**: STIX/TAXII 등 글로벌 오픈 기술 표준을 주도하는 기관.
- **OASIS STIX 2.1**: CTI 표현을 위한 최신 표준 데이터 모델 명세서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 경계 표시 | **FIRST TLP 2.0** 적용 | 재배포 범위 명확화 |
| 외부 객체 교환 | **OASIS STIX 2.1** 변환 | CTI 상호운용성 확보 |
| 정상 지표 오탐 | **경고목록**•**관측** 검증 | 오차단•품질 저하 억제 |
| 플랫폼 간 동기화 | **API**•**TAXII** 권한 검증 | 무단 조회•게시 차단 |

#### 한줄 요약

- 파일 해시•도메인•공격자 정보를 MISP 이벤트로 통합 관리하며 TLP 규약에 따라 차등 배포함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **운영 품질(Operational Quality Metrics)**: 지표의 단순 수집량을 넘어 상관 관계 분석, 관측 피드백 적시성, TLP 공유 통제 준수율을 평가하는 성과 지표.

</details>

- **운영 품질** 확보를 위해 내부 분석 및 관측 통제는 **MISP**, 이종 플랫폼 간 자동 공유는 **STIX/TAXII** 연계 적용.

#### 한줄 요약

- **사건 상관•관측 품질**은 MISP, 교환은 STIX/TAXII 적용
