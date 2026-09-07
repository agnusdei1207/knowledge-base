---
sidebar:
  order: 122
  label: "122. 인텔리전스 기반 CTI 자동화 (CTI Automation)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버 위협 인텔리전스 자동화 및 상호운용성 : CTI 자동화 (STIX 2.1, TAXII 2.1 & TLP 2.0)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 122
extra:
  question_no: "122"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: '138회 기출, 사이버 위협 인텔리전스(CTI: Cyber Threat Intelligence), CTI 전주기 자동화(수집 Ingestion $\rightarrow$ 정규화 Normalization $\rightarrow$ 품질 평가 Scoring $\rightarrow$ 자동 배포 Distribution $\rightarrow$ 시효 만료 Aging), OASIS STIX 2.1(위협 정보 구조화 객체), TAXII 2.1(전송 프로토콜), FIRST TLP 2.0(정보 공유 통제 신호등)'
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **인텔리전스 기반 CTI 자동화(Cyber Threat Intelligence Automation / OASIS STIX/TAXII)**: 분산된 외부 CTI 피드(OSINT, 상용 피드, 국가 위협 공유망)로부터 침해 지표(IoC: IP, 도메인, 해시) 및 공격 전술·기법·절차(TTP)를 수집하여, 글로벌 표준 규격(STIX 2.1)으로 정규화하고, 신뢰도 및 시효(Aging)를 평가한 후, 보안 장비(방화벽, IPS, EDR, SIEM)에 TAXII 2.1 프로토콜로 실시간 자동 배포·차단하는 위협 운영 파이프라인.
- **단순 피드 주입에 따른 오탐 및 성능 저하 결함(Feed Pollution & False Positive Defect)**: 외부 CTI 피드를 검증 없이 방화벽 차단 목록에 무조건 자동 연동할 경우, 클라우드 CDN(Cloudflare, Akamai)이나 공용 DNS(8.8.8.8) 등 정상 IP가 오탐 차단되어 비즈니스 중단이 발생하거나, 만료된 수백만 건의 불필요 룰셋으로 인해 방화벽 메모리가 고갈되는 구조적 결함.

</details>

- 정의/개념: CTI의 신속성과 정확성을 확보하기 위해 **멀티소스 CTI 수집 $\rightarrow$ STIX 2.1 JSON 객체 정규화 $\rightarrow$ 출처 신뢰도 및 만료 시효(Aging) 평가 $\rightarrow$ TLP 2.0 기반 공유 범위 통제 $\rightarrow$ TAXII 2.1 기반 방화벽/EDR 자동 배포 $\rightarrow$ 탐지 피드백 환류** 를 집행하는 **사이버 위협 인텔리전스 전주기 자동화 아키텍처**
- 배경/필요성: 수작업 기반의 CTI 지표(IP, 도메인, 해시) 수집 및 보안 장비 등록 방식은 침해 지표의 빠른 변이 속도(지표 수명 수 시간~수 일)를 따라가지 못해 실시간 차단에 실패하고, 외부 피드를 무검증 자동 연동할 경우 공용 클라우드나 CDN IP의 오탐 차단 및 수백만 건의 만료 룰셋 누적으로 인한 방화벽 성능 고갈이 초래되는 구조적 결함이 발생함에 따라, OASIS STIX 2.1(객체 모델링), TAXII 2.1(HTTPS RESTful 자동 배송), FIRST TLP 2.0(공유 범위 통제) 및 동적 시효 감쇄(Decay Aging) 모델을 결합하는 사이버 위협 인텔리전스(CTI) 자동화 아키텍처를 도입하여 **위협 첩보의 기계 가독형 실시간 교환, 화이트리스트 기반 오탐 원천 차단 및 방화벽/EDR 룰셋의 지능형 자기 정화(Self-cleaning)**를 달성할 필요

#### 한줄 요약
- STIX 2.1과 TAXII 2.1 및 TLP 2.0 표준을 기반으로 CTI 수집, 정규화, 품질 평가, 자동 배포를 수행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **CTI 3대 핵심 글로벌 표준**:
  - **OASIS STIX 2.1 (Structured Threat Information eXpression)**: 공격자(Threat Actor), 악성코드(Malware), 침해지표(Indicator), 공격패턴(Attack Pattern) 간의 관계를 JSON 그래프 구조로 표준화한 위협 표현 언어.
  - **OASIS TAXII 2.1 (Trusted Automated eXchange of Intelligence Information)**: HTTPS REST API 기반으로 STIX 위협 데이터를 안전하게 게시(Publish)하고 구독(Subscribe)하는 교환 프로토콜.
  - **FIRST TLP 2.0 (Traffic Light Protocol)**: 위협 첩보의 공유 범위를 4개 색상(RED, AMBER+STRICT, AMBER, GREEN, CLEAR)으로 지정하여 무단 유출을 방지하는 공유 통제 규약.

</details>

- **그래프 기반 위협 관계망 모델링 (STIX SDO/SRO)**: 단순한 IP 리스트가 아닌, 공격자 그룹과 사용된 악성코드, 표적 취약점 간의 인과관계를 객체(SDO)와 관계(SRO)로 구조화
- **동적 시효 관리(Aging & Decay Model)**: 위협 지표의 유효 기간(예: C2 IP는 7일, 파일 해시는 1년)을 설정하여 만료된 지표를 방화벽 차단 목록에서 자동 회수(Purge)
- **엄격한 TLP 기반 정보 공유 거버넌스**: TLP 메타데이터에 따라 내부 보안팀 전용(RED/AMBER)과 외부 유관기관 공유(GREEN/CLEAR)를 기계적으로 분기 통제

#### 한줄 요약
- STIX 2.1 객체 모델링, TAXII 2.1 고속 전송, 동적 시효(Aging) 관리, TLP 2.0 공유 통제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CTI 자동화 4대 핵심 컴포넌트**:
  1. **Feed Collectors (수집기)**: OSINT, 상용 피드(Recorded Future, Mandiant), 국가 C-TAS 수집기.
  2. **TIP Core (Threat Intelligence Platform)**: 정규화, 중복 제거, 평판 스코어링, 화이트리스트 필터링.
  3. **TAXII Server & Client**: RESTful 엔드포인트 기반 STIX 2.1 묶음(Bundle) 푸시/풀 서버.
  4. **Enforcement Integrations**: 방화벽, EDR, SIEM/SOAR로의 OpenC2/API 연동 에이전트.

</details>

```text
[CTI 자동화 파이프라인]
├── [1. 다중 소스 첩보 수집]
│   ├── OSINT 피드 (OTX, AbuseIPDB)
│   ├── 상용 피드 (실시간 제로데이)
│   └── 국가망 연계 (C-TAS, F-ISAC)
├── [2. TIP 정규화 및 품질 평가]
│   ├── STIX 2.1 객체·관계 변환
│   ├── 화이트리스트 필터 (오탐 방지)
│   └── 동적 시효 만료 (Aging Decay)
├── [3. TAXII 배송 및 TLP 통제]
│   ├── TLP 2.0 공유 등급 태깅
│   └── TAXII 2.1 RESTful 배송
└── [4. 보안 장비 자동 적용]
    ├── NGFW/IPS (악성 IP·도메인 차단)
    ├── EDR (악성 파일 해시 실행 차단)
    └── SIEM/SOAR (플레이북 연계)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **위협 정보 플랫폼 (TIP)** | 위협 피드 수집, 중복 제거, 정규화 및 지표 수명주기 총괄 관리 |
| **STIX 2.1** | 위협 객체(Indicator, Malware 등)와 관계를 JSON 그래프로 구조화 |
| **TAXII 2.1** | STIX 위협 데이터를 HTTPS REST API 채널을 통해 신뢰된 엔드포인트 전송 |
| **TLP 2.0** | 위협 정보 재공유 및 공개 범위를 4단계 색상 태그로 기계적 통제 |
| **시효 만료 엔진 (Decay)** | 시간 경과에 따른 지표 신뢰도 감쇄 및 만료 차단 룰 자동 제거 |

#### 한줄 요약
- STIX 2.1이 피드마다 제각각인 표현을 하나의 객체·관계 모델로 대신하고 TAXII 2.1이 수작업 파일 교환 자리에 REST 채널을 놓으며, TLP 2.0은 재공유 가능 여부를 매번 되묻던 판단을 태그로 옮기고, 시효 만료 엔진은 사람이 낡은 IoC를 찾아 지우던 일을 신뢰도 감쇄로 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CTI 자동화 5단계 파이프라인**:
  1. 멀티소스 위협 피드 수집 및 파싱
  2. STIX 2.1 정규화 및 화이트리스트 기반 오탐 필터링
  3. 교차 검증 기반 품질 스코어링 및 유효 시효(TTL) 부여
  4. TLP 2.0 정책 확인 및 TAXII 2.1 기반 보안 솔루션 전송
  5. 방화벽/EDR 룰셋 자동 갱신 및 탐지 성공률 피드백

</details>

```text
1. [위협 피드 수집] 외부 다크웹 CTI 피드에서 신종 랜섬웨어 C2 도메인 및 IP 수신
            │
            ▼
2. [STIX 2.1 정규화 및 1차 필터링]
    ├─ JSON 기반 STIX 2.1 Indicator 객체로 데이터 정규화
    └─ [내부 화이트리스트(사내 결제망 IP, 글로벌 CDN 대역) 대조 ➔ 오탐 배제]
            │
            ▼
3. [품질 스코어링 및 시효 설정]
    ├─ 3개 이상 독립 CTI 피드에서 동시 보고 확인 ➔ 신뢰도 점수 95점 부여
    └─ [IP 특성을 고려하여 14일 유효 수명(TTL) 부여 ➔ 만료 시 자동 삭제 예약]
            │
            ▼
4. [TAXII 2.1 배포 및 TLP 태깅]
    ├─ TLP:AMBER 태그 부착 (사내 인프라 및 보안관제 전용 공유)
    └─ [TAXII 2.1 채널을 통해 차세대 방화벽 및 EDR 클러스터로 실시간 전송]
            │
            ▼
5. [장비 자동 적용 및 피드백]
    ├─ 방화벽 아웃바운드 차단 룰셋 자동 갱신 (1초 내 적용)
    ├─ [실제 침입 시도 3건 차단 성공 ➔ TIP에 해당 IoC 가중치 상향 피드백]
    └─ [14일 경과 후 침입 시도 미발생 ➔ 방화벽 룰셋에서 안전하게 자동 회수]
```

**동작 원리**

1. **지능형 오탐 방어**: 화이트리스트 대조 및 다중 소스 교차 검증을 통해 정상 트래픽 차단 원천 차단
2. **기계 가독형 상호운용성**: STIX 2.1 표준 스키마를 사용하여 서로 다른 벤더 제품 간 데이터 변환 오류 0% 달성
3. **보안 지표의 자기 정화(Self-cleaning)**: 시효 감쇄 모델을 통해 방화벽 룰셋의 비대화 및 장비 과부하 방지
4. **정보 유출 통제**: TLP 2.0 프로토콜을 시스템적으로 강제하여 민감한 침해 지표가 외부에 무단 공개되는 사고 방어
5. **폐쇄 루프 신뢰도 갱신**: 현장 장비의 실제 탐지/차단 성공 여부를 TIP에 피드백하여 피드 공급사 신뢰도 지속 보정

#### 한줄 요약
- 지표를 오래 유지하면 오탐이 쌓이고 일찍 만료시키면 탐지 공백이 생기므로, 시효(Aging) 설정이 자동화 파이프라인의 실질적인 품질 조절 손잡이가 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **FIRST TLP 2.0 4대 정보 공유 등급**:
  - **TLP:RED**: 발신자와 수신자 개인 간에만 한정 공유 (조직 내 타인 공유 불가).
  - **TLP:AMBER+STRICT**: 수신 조직 내부에서만 엄격히 공유 (외부 클라이언트 공유 불가).
  - **TLP:AMBER**: 수신 조직 및 조직을 지원하는 고객/파트너사 내부까지 공유 가능.
  - **TLP:GREEN**: 동일 커뮤니티 및 유관 보안 기관 간 공유 가능 (대외 공개 불가).
  - **TLP:CLEAR**: 인터넷 및 언론을 포함한 완전 공개 가능.

</details>

| TLP 2.0 등급 | 공유 허용 범위 | 주요 대상 정보 | 비고 |
|:---|:---|:---|:---|
| **TLP:RED** | **해당 회의/통신에 직접 참여한 개인으로 제한** | 진행 중인 제로데이 공격, 미공개 핵심 취약점 | 극비 (Non-distributable) |
| **TLP:AMBER+STRICT**| **수신 조직의 정직원 내부로만 제한 (제3자 제외)**| 사내 침해사고 분석 보고서, 타겟 공격 지표 | 사내 한정 |
| **TLP:AMBER** | 수신 조직 및 관련 업무 협력사/고객사 내부 | 일반 침해 지표(IoC), 악성코드 분석서 | Need-to-know |
| **TLP:GREEN** | **산업군 커뮤니티, ISAC 회원사, 협력 보안 기관** | 광범위하게 유포 중인 피싱 도메인, 랜섬웨어 IP| Community |
| **TLP:CLEAR** | **일반 대중, 언론, 웹사이트 공개 가능** | 공식 보안 권고문, 패치 공지 | Public (구 TLP:WHITE) |

#### 한줄 요약
- TLP:RED(개인 한정), AMBER(조직 한정), GREEN(커뮤니티 공유), CLEAR(전체 공개)로 분류된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OASIS STIX/TAXII v2.1 및 FIRST TLP v2.0**: 사이버 위협 인텔리전스 표현, 전송 및 공유 통제 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 검증되지 않은 CTI 피드를 방화벽에 무조건 자동 연동하여 **정상 공용 클라우드 IP가 차단되어 대국민 웹 서비스 접속 장애 발생** | **TIP 플랫폼 내 내부 화이트리스트 필터링 및 2개 이상 독립 CTI 교차 검증 점수가 90점 이상인 지표만 자동 배포 강제** | 정상 서비스 오탐 차단 100% 방지 및 안정적 운영 달성 |
| 수년간 누적된 수백만 건의 만료된 IoC가 방화벽에 잔존하여 **방화벽 세션 테이블 고갈 및 패킷 처리 지연 성능 저하 발생** | **지표 유형별 유효 시효(TTL: IP 14일, 도메인 30일)를 적용하고, 지표 감쇄(Decay) 모델을 통해 만료 지표 자동 삭제 파이프라인 구축** | 방화벽 룰셋 경량화 및 장비 가용성 100% 보존 |
| 내부에서 분석한 고위험 침해 지표(IoC)를 외부 기관에 공유했다가 **공격자가 역탐지 사실을 인지하고 C2 인프라를 전면 은폐 도주** | **FIRST TLP 2.0 가이드라인 준수, 분석 보고서에 TLP:RED 및 AMBER+STRICT를 메타데이터로 강제 태깅하여 자동 공유 차단** | 첩보 무단 유출 원천 방지 및 공격 추적성 유지 |

#### 한줄 요약
- 화이트리스트와 교차 검증으로 오탐을 막고, TTL 시효 만료로 룰셋을 정화하며, TLP 2.0으로 기밀 유출을 방어한다.

## Ⅶ. 결론

- 글로벌 위협 첩보를 표준화된 기계 언어로 실시간 교환하고 보안 장비에 자동 적용하여 공격자의 공격 비용을 극대화하는 **사이버 위협 인텔리전스 및 방어 자동화(OASIS STIX/TAXII 2.1 / FIRST TLP 2.0 / Aging Decay)의 핵심 중추 파이프라인**으로 확고히 자리 잡았으며, 공격 표면 관리(EASM) 및 자동화 대응(SOAR), 생성형 위협 분석과 융합되는 가운데, 실무 엔터프라이즈 CTI 파이프라인 구축 시에는 **STIX 2.1 기반 멀티소스 피드 정규화 및 내부 화이트리스트 교차 검증을 통한 오탐 0% 보증, TAXII 2.1 기반 방화벽·EDR 1초 내 자동 차단 배포, 지표 유형별 TTL 및 지수 감쇄(Decay) 모델을 통한 만료 룰 자동 회수(Purge)**를 결합하여 완벽한 CTI 자동화 거버넌스를 완성

#### 한줄 요약
- STIX/TAXII 2.1 표준과 품질 평가 및 TLP 2.0 거버넌스를 통해 완벽한 CTI 자동화 파이프라인을 완성한다.
