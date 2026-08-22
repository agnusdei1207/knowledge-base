---
sidebar:
  order: 143
  label: "143. 보안 정보 공유 플랫폼 — ISAC (ISAC)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "산업별 사이버 위협 인텔리전스 공유 플랫폼 : ISAC (STIX 2.1 & TAXII 2.1)"
date: "2026-08-22T08:15:00+09:00"
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
- 배경/필요성: 특정 산업군(금융 SW 공급망, 의료망 랜섬웨어 등)을 타깃으로 하는 국가 배후 공격 그룹의 등장에 대응하여, 피해 기업의 침해 지표를 익명화하여 전 회원사에 0.1초 내 전파할 기계 가독형(Machine-Readable) 자동 공유 체계 필요

#### 한줄 요약
- ISAC은 STIX/TAXII 표준과 TLP 통제를 기반으로 산업별 위협 인텔리전스를 자동 공유한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ISAC 3대 핵심 공유 기술 및 통제 프로토콜**:
  - **OASIS STIX 2.1 (Structured Threat Information eXpression)**: 노드(SDO)와 엣지(SRO)로 구성된 JSON 그래프 기반의 위협 표현 표준.
  - **OASIS TAXII 2.1 (Trusted Automated eXchange of Intelligence Information)**: HTTPS REST API 기반의 기계 가독형 위협 정보 전송 프로토콜.
  - **FIRST TLP 2.0 (Traffic Light Protocol)**: 정보의 재배포 가능 범위를 4대 색상(RED, AMBER, GREEN, CLEAR)으로 규정한 기밀성 공유 규칙.

</details>

- **기계 가독형(Machine-Readable) 실시간 연동**: 수작업 문서 전달을 배제하고 STIX/TAXII RESTful API를 통해 회원사 SOAR/방화벽에 차단 룰셋 자동 반영
- **엄격한 데이터 비식별화(De-identification)**: 수집 단계에서 사설 IP(RFC 1918), 내부 호스트명, 개인정보(PII)를 정규식/DLP로 자동 마스킹하여 공유사의 익명성 완벽 보장
- **시효 만료(Decay Model) 및 평판 관리**: 시간 경과에 따라 동적 IP C2 서버의 신뢰도 점수를 자동 감쇄(Valid_Until)하여 오탐(False Positive)으로 인한 정상 트래픽 차단 방지

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
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 데이터 수집 계층 (Data Collection: TAXII 2.1 Inbox & Feeds) ]       │
│  ├─ [ 회원사 CSIRT ] ➔ 침해사고 악성 패킷/로그 제출 (TAXII POST)         │
│  └─ [ 유관기관 및 상용 CTI ] ➔ KISA, 경찰청, Mandiant 글로벌 피드 수집   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (mTLS 1.3 암호 통신)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 데이터 정제 및 위협 보강 계층 (Processing & Enrichment Engine) ]   │
│  ├─ [ 비식별화 (Sanitization) ] ➔ 내부 IP, PII, 회원사 식별자 자동 마스킹│
│  ├─ [ OSINT 보강 ] ➔ VirusTotal, Shodan 연동 악성 해시 평판 조회        │
│  └─ [ TTP 매핑 ] ➔ MITRE ATT&CK 공격 그룹(APT38 등) 및 기법 자동 분류   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (STIX 2.1 JSON 그래프 변환)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 위협 지식 저장 계층 (Graph DB & STIX Repository: Neo4j) ]          │
│  └─ [ SDO 노드 (침해지표, 악성코드) $\longleftrightarrow$ SRO 엣지 (사용함, 공격대상) ]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (TLP 권한 필터링)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 안전 배포 및 SOAR 자동 연동 계층 (Distribution & TLP Enforcer) ]    │
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ TLP 등급 검증 (Enforcer) ]      │ [ 실시간 배포 및 방어 자동화 ]      │
│ ├─ TLP:RED ➔ 지정된 특정인만 전송│ ├─ TAXII 2.1 Poll / Pub-Sub 배포    │
│ └─ TLP:AMBER/GREEN ➔ 커뮤니티 공유│ └─ [ 회원사 SOAR ➔ 방화벽 자동 차단]│
└───────────────────────────────────┴─────────────────────────────────────┘
```

선의 의미: 회원사 및 CTI에서 수집된 위협 데이터를 정제/보강하여 그래프 DB에 저장하고, TLP 권한 필터링을 거쳐 회원사 SOAR로 자동 배포하는 구조

| 컴포넌트 | 핵심 기능 및 역할 | 주요 기술 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **수집 엔진 (Inbox)** | 회원사 및 외부 CTI 피드로부터 침해 로그 및 IoC 실시간 수집 | TAXII 2.1 Inbox Service, REST API | Ingestion |
| **정제기 (Sanitizer)** | 침해 기관 유추 방지를 위한 내부 IP, 도메인, 개인정보 자동 마스킹 | 정규표현식, DLP 필터, PII Masker | Privacy |
| **위협 보강 (Enricher)**| 공격자 그룹 식별 및 MITRE ATT&CK TTP 연계, 평판 점수 부여 | VirusTotal API, ATT&CK Navigator | Analytics |
| **그래프 레포지토리** | 위협 객체 간의 다대다(N:M) 연관 관계 저장 및 초고속 탐색 | Neo4j Graph DB, STIX 2.1 SDO/SRO | Knowledge |
| **배포 엔진 (Collection)**| 회원사 권한 및 TLP 등급에 따른 STIX 번들 동적 필터링 및 푸시 | TAXII 2.1 Collection, mTLS, JWT | Distribution |

#### 한줄 요약
- 수집 엔진, 비식별화 정제기, 위협 보강기, 그래프 DB 레포지토리, TLP 배포 엔진으로 구성된다.

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

1. **익명성 보장을 통한 공유 활성화**: 침해 기관의 사설 정보가 자동 삭제되어 기업 평판 훼손 우려 없이 자유로운 공유 가능
2. **공유 범위의 논리적 강제**: TLP Enforcer 모듈이 수신자 권한을 대조하여 비인가 등급의 STIX 객체는 응답 번들에서 자동 누락
3. **오탐 자동 정화 루프**: 회원사에서 정상 트래픽 오탐 리포트 제출 시 신뢰도 점수가 하락하고 특정 임계치 도달 시 자동 폐기(Revoke) 공지
4. **집단 선제 방어 실현**: 1개 기관이 공격당한 즉시 전 산업계 회원사가 동일 공격 지표에 대해 0.1초 내 방어 태세 완비
5. **국제 표준 준거성**: OASIS STIX/TAXII 및 MITRE ATT&CK 채택으로 이기종 글로벌 보안 솔루션 간 100% 호환성 확보

#### 한줄 요약
- 지표 제출, 비식별화, 컨텍스트 보강, TLP 마킹 및 그래프 저장, SOAR 자동 차단 배포 순으로 동작한다.

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

- 개별 기업의 단독 방어를 넘어 산업 생태계 전체의 집단 면역 체계를 형성하는 핵심 신경망인 **ISAC 정보 공유 플랫폼**은 국가 기간시설 및 민간 산업 보안의 중추 인프라로서, 실무 구현 시 **OASIS STIX 2.1 및 TAXII 2.1 국제 표준 프로토콜 완벽 준수**, **FIRST TLP 2.0 기반의 엄격한 기밀성 유통 통제**, **침해 기관 익명성을 보장하는 자동화된 데이터 비식별화(Sanitization) 내재화**, **회원사 SOAR 플랫폼과의 실시간 룰셋 연동 및 반감기(Decay) 평판 관리**를 통합 완성하여 최고 수준의 집단 사이버 복원력을 완성

#### 한줄 요약
- STIX/TAXII 표준과 TLP 통제 및 비식별화 정제를 통해 무결점 산업별 위협 공유 체계를 완성한다.
