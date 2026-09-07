---
sidebar:
  order: 143
  label: "143. 보안 정보 공유 플랫폼 — ISAC (ISAC)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "산업별 사이버 위협 인텔리전스 공유 플랫폼 : ISAC (STIX 2.1 & TAXII 2.1)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 143
extra:
  question_no: "143"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, 정보공유분석센터(ISAC: Information Sharing and Analysis Center), OASIS 표준(STIX 2.1 SDO/SRO JSON 그래프 모델, TAXII 2.1 전송 프로토콜), FIRST TLP 2.0(Traffic Light Protocol) 기밀성 제어, 침해지표(IoC) 및 MITRE ATT&CK TTP 공유, 비식별화 및 반감기 모델(Decay Model)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **정보공유분석센터(ISAC: Information Sharing and Analysis Center)**: 특정 산업군(금융, 의료, 통신, 에너지, 교통 등) 내의 회원사들이 사이버 침해사고 위협 인텔리전스(CTI), 침해지표(IoC), 취약점 및 공격자 전술·기술·절차(TTP)를 안전하고 신속하게 수집, 분석, 상호 교환하도록 지원하는 산업 특화형 민관 협력 집단 방어 플랫폼.
- **개별 기업 단독 대응의 한계 및 침해 정보 유출 우려 결함(Siloed Defense & Trust Defect)**: 고도화된 APT 공격이나 공급망 침해 시 개별 기업의 관제(SIEM/EDR)만으로는 공격 징후를 선제 탐지하기 어렵고, 침해 정보를 외부에 공개할 경우 기업 평판 하락이나 2차 공격 타겟이 될 우려로 인해 수평적 정보 공유가 위축되는 구조적 결함.

</details>

- 정의/개념: 동종 산업 생태계의 집단 사이버 복원력(Collective Resilience)을 강화하기 위해 **회원사 침해 지표 수집 $\rightarrow$ 개인정보 및 민감 데이터 비식별화(Sanitization) $\rightarrow$ STIX 2.1/TAXII 2.1 표준 기반 위협 그래프 분석 $\rightarrow$ FIRST TLP 2.0 기밀성 등급 통제 $\rightarrow$ SOAR/SIEM 자동화 룰셋 실시간 배포** 를 집행하는 **산업별 위협 인텔리전스 공유 플랫폼**
- 배경/필요성: 지능화된 표적 공격(APT)과 공급망 위협이 특정 산업군(금융, 의료, 에너지, 교통) 전체를 대상으로 동시다발적으로 전개되는 환경에서, 개별 기업 단위의 고립된 방어(Siloed Defense)는 초기 침해 징후 포착에 한계가 있고 침해 사실 공개에 따른 기업 평판 하락 우려로 인해 수평적 정보 공유가 위축되는 구조적 병목이 발생함에 따라, OASIS STIX 2.1(위협 표현) 및 TAXII 2.1(전송 프로토콜) 표준에 기반하여 민감 정보 비식별화(Sanitization), FIRST TLP 2.0 기밀성 등급 통제, MITRE ATT&CK TTP 연계 및 SOAR 기반 침해지표(IoC) 실시간 배포를 결합하는 ISAC(정보공유분석센터) 집단 방어 플랫폼을 도입하여 **단일 기업 침해 사고의 전 산업군 선제 방어 지표 전환, 집단 사이버 복원력(Collective Resilience) 극대화 및 위협 대응 시간(MTTD/MTTR) 최소화**를 달성할 필요

#### 한줄 요약
- ISAC은 STIX/TAXII 표준과 TLP 통제를 기반으로 산업별 위협 인텔리전스를 자동 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ISAC 3대 핵심 공유 기술 및 통제 프로토콜**:
  - **OASIS STIX 2.1 (Structured Threat Information eXpression)**: 노드(SDO)와 엣지(SRO)로 구성된 JSON 그래프 기반의 위협 표현 표준.
  - **OASIS TAXII 2.1 (Trusted Automated eXchange of Intelligence Information)**: HTTPS REST API 기반의 기계 가독형 위협 정보 전송 프로토콜.
  - **FIRST TLP 2.0 (Traffic Light Protocol)**: 정보의 재배포 가능 범위를 4대 색상(RED, AMBER, GREEN, CLEAR)으로 규정한 기밀성 공유 규칙.

</details>

- STIX/TAXII로 방어 규칙을 배포하는 **기계 가독 연동**
- 내부 IP·호스트·PII를 제거하는 **데이터 비식별화**
- 오래된 IoC 신뢰도를 낮추는 **반감기 모델**

#### 한줄 요약
- STIX/TAXII 자동 연동, TLP 기밀성 제어, 침해 기관 비식별화, 지표 반감기(Decay) 관리를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ISAC 4대 핵심 아키텍처 계층**:
  1. **Data Collection Layer**: TAXII 2.1 Inbox, MISP 연동, Syslog/Webhook 수집기.
  2. **Processing & Enrichment Layer**: 데이터 정제기(Sanitizer), MITRE ATT&CK 매퍼, OSINT 연동기.
  3. **Storage Layer**: 위협 연관 관계 그래프 DB(Neo4j) 및 STIX 레포지토리.
  4. **Distribution Layer**: TAXII 2.1 Collection 서비스, TLP 권한 필터, SOAR 웹훅 배포기.

</details>

```text
[ISAC 위협 정보 공유 플랫폼]
├── [수집 계층 (Data Collection)]
│   └── TAXII Inbox · MISP · Webhook
├── [처리·보강 계층 (Processing & Enrichment)]
│   └── 민감정보 비식별화 및 ATT&CK 매핑
├── [저장 계층 (Storage Layer)]
│   └── STIX 2.1 레포지토리 및 그래프 DB
└── [배포 계층 (Distribution Layer)]
    └── TLP 등급 필터 및 회원사 SOAR 연동
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **Data Collection Layer** | 회원사와 외부 피드의 IoC 수집 |
| **Processing·Enrichment Layer** | 비식별화와 평판·TTP 보강 |
| **Storage Layer** | STIX 객체와 관계 그래프 저장 |
| **Distribution Layer** | TLP 범위에 따라 회원사 SOAR로 배포 |

#### 한줄 요약
- 비식별화 정제기가 침해 사실이 드러날 위험을 걷어 내 회원사가 자료를 내놓을 수 있게 만드는 전제 계층이고, 그래프 DB는 낱개로 흩어진 IoC를 관계로 이어 한 기관이 치른 피해를 다른 회원사가 겪기 전에 재사용하게 하며, TLP 배포 엔진이 공유 범위를 건마다 협의하던 자리를 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ISAC 위협 정보 전주기 공유 5단계 파이프라인**:
  1. 침해 사고를 겪은 회원사 A가 C2 IP 및 악성 해시를 TAXII Inbox로 제출
  2. ISAC 정제기가 회원사 IP 및 식별 정보를 비식별화 마스킹
  3. OSINT 연동 및 STIX 2.1 SDO/SRO 객체 그래프 생성
  4. 데이터 민감도에 따른 TLP:AMBER 등급 부여 및 DB 저장
  5. 타 회원사 B가 TAXII Poll을 통해 수집하여 SOAR 방화벽 자동 차단 반영

</details>

```text
1. [위협 지표 제출] 회원사 A가 랜섬웨어 침해 탐지 ➔ C2 IP(198.51.100.22) 제출 (TAXII POST)
            │
            ▼
2. [비식별화 및 구문 검증]
    ├─ JSON Schema 유효성 검증 (비정상 패킷 즉시 차단)
    └─ [회원사 내부 IP 및 기업명을 'ANONYMOUS_MEMBER'로 100% 자동 마스킹]
            │
            ▼
3. [위협 컨텍스트 보강]
    ├─ VirusTotal API 조회 ➔ 해당 C2 IP 악성 판정 98% 확인
    └─ [MITRE ATT&CK 매핑 ➔ T1071(응용계층 프로토콜 악용) SRO 엣지 연결]
            │
            ▼
4. [TLP 마킹 및 그래프 저장]
    ├─ 정보 공유 범위 판정 ➔ 'TLP:AMBER' 객체 마킹(object_marking_refs) 부여
    └─ [STIX 2.1 Bundle 형태로 Neo4j 그래프 데이터베이스에 영구 적재]
            │
            ▼
5. [배포 및 타 회원사 자동 방어]
    ├─ 회원사 B의 SOAR 시스템이 TAXII Poll GET 요청 ➔ TLP:AMBER 권한 확인 후 수신
    └─ [SOAR 플레이북 자동 트리거 ➔ 전사 방화벽에 해당 C2 IP 인바운드/아웃바운드 차단 룰 즉각 주입]
```

**동작 원리**

1. **위협 지표 제출**: 회원사의 IoC를 TAXII Inbox로 수집
2. **비식별화 및 구문 검증**: 식별정보 제거와 스키마 검증
3. **위협 컨텍스트 보강**: IoC 평판과 ATT&CK TTP 연결
4. **TLP 마킹 및 그래프 저장**: 공유 범위 부여와 STIX 적재
5. **배포 및 타 회원사 자동 방어**: SOAR 차단 규칙 반영

#### 한줄 요약
- 공유 범위가 넓을수록 집단 방어력은 오르지만 제출 기관의 피해 사실이 드러날 위험도 커지므로, 비식별화와 TLP 등급이 참여를 지속시키는 최소 조건이 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **사이버 위협 정보 공유 3대 모델 비교**:
  - ISAC (산업별 정보공유분석센터): 특정 산업 섹터 중심의 상호 신뢰 기반 양방향 공유 (산업 특화).
  - CSIRT / CERT (침해사고대응팀): 단일 조직 또는 국가 공공망 침해사고 대응 및 조사 (대응 중심).
  - Commercial CTI (상용 위협 인텔리전스): 글로벌 텔레메트리 기반의 유료 위협 피드 판매 (상업적 광범위).

</details>

| 비교 항목 | ISAC (산업별 정보공유분석센터) | CSIRT / CERT (침해사고대응팀) | Commercial CTI (상용 인텔리전스) |
|:---|:---|:---|:---|
| **설립 목적** | **특정 산업군 공동 방어 및 상향 평준화**| **개별 조직 내부 사고 대응 및 복구** | 광범위 위협 피드 수집 및 상업적 판매 |
| **운영 주체 예시** | **금융보안원(금융), KISA(민간), 보건복지부**| KrCERT/CC, 금융사 내부 보안팀 | Mandiant, CrowdStrike, Recorded Future |
| **공유 데이터** | **실제 산업 타깃 공격 지표(IoC), 비식별 로그**| 자사 내부망 Raw 침해 로그 (비공개) | **전 세계 허니팟/다크웹 수집 대량 데이터**|
| **신뢰 모델** | **폐쇄적 신뢰 그룹, 강력한 비밀유지(NDA)**| 조직 내부 상하 계층적 기밀 유지 | 계약 및 SLA 기반의 상업적 신뢰 |
| **주요 배포 방식** | **STIX/TAXII 자동화 피드, TLP 통제** | 내부 티켓팅(Jira), 긴급 보안 권고문 | REST API, 클라우드 대시보드 스트림 |

#### 한줄 요약
- ISAC은 폐쇄 신뢰 기반의 산업 특화 공유, CSIRT는 개별 사고 대응, 상용 CTI는 광범위 유료 피드에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **FIRST TLP 2.0 및 OASIS STIX 2.1/TAXII 2.1**: 위협 인텔리전스 공유 및 기밀성 통제 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 검증되지 않은 C2 IP가 자동 공유되어 **전 회원사 방화벽에서 Google DNS나 클라우드 CDN 등 정상 서비스 IP가 차단되는 전산 장애 발생** | **Bogon/정상 IP 화이트리스트 필터링을 강제하고, 7일 반감기(Decay Model) 및 회원사 오탐 피드백 루프 API 구축** | 정상 트래픽 오차단 장애 0% 및 신뢰성 확보 |
| TAXII 서버 엔드포인트가 외부에 노출되어 **공격자의 크리덴셜 스터핑 또는 인가되지 않은 TLP:RED 기밀 지표 무단 수집 발생** | **mTLS 1.3 상호 인증 및 JWT 기반 속성 기반 접근 제어(ABAC)를 적용하고, API 게이트웨이 Rate Limiting 구축** | 비인가 접근 및 무단 정보 수집 100% 원천 차단 |
| 회원사가 제출한 패킷 덤프 내에 고객 주민등록번호나 계좌번호 등 **민감한 개인정보(PII)가 포함되어 타 회원사로 유출되는 법적 위반 발생** | **전송 전 로컬 DLP 1차 필터링 강제 및 ISAC 수집단에 정규표현식 기반 PII 자동 마스킹(Sanitization) 엔진 배치** | 개인정보보호법 및 컴플라이언스 위반 100% 방지 |

#### 한줄 요약
- 반감기 모델로 오차단을 막고, mTLS로 TAXII 서버를 보호하며, 자동 마스킹으로 개인정보 유출을 방지한다.

## Ⅶ. 결론

- 개별 기관의 고립된 보안 한계를 극복하고 동종 산업 생태계 전체가 유기적으로 연대하여 공격에 대응하는 **산업별 사이버 위협 인텔리전스 공유 및 집단 방어(ISAC / STIX 2.1 & TAXII 2.1 / TLP 2.0)의 핵심 협력 플랫폼**으로 확고히 자리 잡았으며, AI 기반 이상징후 상관분석 및 글로벌 ISAC 간 연합 체계로 진화하는 가운데, 실무 ISAC 운영 및 회원사 연동 구축 시에는 **회원사 개인정보(PII) 및 내부망 정보에 대한 자동 비식별화(Sanitization) 강제, 정상 IP 오차단 방지를 위한 화이트리스트 검증 및 지표 반감기(Decay Model) 관리, mTLS 1.3 기반 TAXII 채널 암호화 및 SOAR 플레이북과의 실시간 정책 주입 자동화**를 결합하여 완벽한 산업 사이버 방어 생태계를 완성

#### 한줄 요약
- STIX/TAXII 표준과 TLP 통제 및 비식별화 정제를 통해 무결점 산업별 위협 공유 체계를 완성한다.
