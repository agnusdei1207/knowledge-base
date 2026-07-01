---
title: "SIEM 보안 이벤트 집계 분석 (SIEM)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 48
---

# 📖 【암기용】 개념 완전 이해

> 목적: SIEM을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 여러 시스템의 보안 로그를 수집, 정규화, 상관분석해 침해 징후를 탐지하는 플랫폼
- **왜 필요한가**: 방화벽, 서버, EDR, IAM 로그를 따로 보면 공격 흐름이 보이지 않는다. SIEM은 분산 로그를 공통 스키마로 묶어 규칙과 시간 관계로 분석함.
- **핵심 직관**: CCTV, 출입기록, 결제기록을 한 타임라인에 놓아야 의심 행동을 찾을 수 있는 것과 같음.

## 깊이 이해
- **배경·문제의식**: 보안 사고는 단일 이벤트보다 여러 약한 신호의 조합으로 드러난다. 실패 로그인, VPN 접속, 권한 상승, 외부 전송이 각각은 정상처럼 보여도 시간 순서로 묶으면 침해 징후가 됨.
- **작동 원리**: log source에서 이벤트를 수집하고 parser가 필드를 추출한다. 정규화 스키마로 host, user, src_ip, event_type을 맞춘 뒤 correlation rule, threshold, UEBA, CTI match로 경보를 생성함.
- **비유**: 여러 언어로 적힌 사건 기록을 같은 양식으로 번역한 뒤, 동일 인물·시간·장소 기준으로 수사 파일을 만드는 과정임.
- **구체 예시**: 10분 내 AD 실패 로그인 20회, 성공 로그인 1회, 신규 관리자 그룹 추가, 외부 1GB 전송이 동일 계정에서 발생하면 SIEM은 계정 탈취 경보를 생성함.
- **흔한 오해·주의점**: SIEM은 로그 저장소만이 아니다. parser 품질, rule tuning, 자산 중요도, 경보 triage가 없으면 저장 비용만 증가함.

## 연결 개념
- SOC - SIEM 경보를 분석하고 대응하는 운영 조직
- SOAR - SIEM 경보를 티켓과 자동 조치로 연결
- UEBA - 사용자·엔티티 행동 기준선으로 SIEM 탐지 정밀도 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SIEM 답안은 log source, parser, normalization, correlation, rule tuning, ticket 연계를 로그 수집-정규화-상관분석-MTTD 흐름으로 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SIEM은 이기종 로그를 정규화하고 상관분석해 침해 징후를 경보로 생성하는 보안 분석 플랫폼임.
> 2. **가치**: SOC가 단일 장비 경보가 아닌 사용자, 자산, 네트워크, 시간 관계 기반으로 사고 우선순위를 판단하게 함.
> 3. **판단 포인트**: 로그 소스 커버리지, parser 오류율, correlation rule 품질, tuning, MTTD를 함께 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SIEM 구조 이해 확인 | log source, collector, parser, normalization, correlation | 로그 저장소 기능만 설명 |
| 탐지 품질 판단 확인 | rule tuning, threshold, CTI match, UEBA 연계 | 룰 개수 증가를 탐지 품질로 단정 |
| SOC 운영 연계 확인 | alert, case, ticket, MTTD, false positive | 경보 후 티켓·대응 누락 |

> 요약: SIEM 문제는 로그 파이프라인과 상관분석 품질을 운영 지표로 설명하는 능력을 요구함.

---

## Ⅰ. 개요 및 필요성

SIEM은 보안 로그 상관분석 플랫폼임. 이기종 보안 장비와 업무 시스템 로그를 수집해 공통 필드로 정규화하고 공격 시나리오 기반 경보를 생성함. SOC는 SIEM을 통해 MTTD, 오탐률, 로그 수집률을 관리함.

---

## Ⅱ. 구조 및 구성요소

```text
Log Source -> Collector/Agent -> Parser -> Normalization -> Storage
           -> Correlation Rule/CTI/UEBA -> Alert -> Ticket/SOAR
           +-> Dashboard/Report/Compliance Search
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Log Source | FW, WAF, EDR, AD, IAM, Cloud, DB 로그 제공 | 자산 중요도와 수집 우선순위 필요 |
| Collector/Parser | 이벤트 수집, 필드 추출, 시간 보정 | parser error 1% 이하 목표 |
| Normalization | user, host, src_ip, event_type 공통 스키마 | ECS, CEF, LEEF 활용 |
| Correlation Engine | 규칙, 임계치, CTI 매칭, risk scoring | MITRE ATT&CK 매핑 |
| Alert/Case | 경보, 티켓, 증적, 보고서 생성 | SOC triage와 SOAR 연계 |

> 요약: SIEM은 로그 수집부터 경보와 티켓까지 이어지는 분석 파이프라인으로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
이벤트 발생 -> 로그 수집 -> 파싱/정규화 -> 저장/색인
-> 상관분석 규칙 실행 -> risk score 산정 -> alert 생성
-> SOC triage -> rule tuning -> MTTD/오탐률 측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 로그 소스 등록과 수집 상태 확인 | coverage 95%, 수집 지연 5분 이하 |
| 2 | parser로 필드 추출과 정규화 | parser error 1% 이하 |
| 3 | correlation rule, threshold, CTI match 실행 | ATT&CK rule mapping 80% 이상 |
| 4 | 경보 생성과 티켓 연동 | duplicate alert 20% 이하 |
| 5 | 오탐 분석과 룰 튜닝 | false positive 30% 이하 |

> 요약: SIEM은 로그를 정규화한 뒤 규칙과 맥락으로 경보를 만들고 튜닝으로 탐지 품질을 관리함.

---

## Ⅳ. 특징

| 구분 | 로그 관리 중심 | SIEM 분석 중심 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 데이터 | 원본 로그 저장 | 정규화, enrich, index | EPS, 보존 1년 |
| 분석 | 키워드 검색 | correlation, threshold, CTI match | MITRE ATT&CK coverage 80% |
| 운영 | 사후 조회 | 실시간 alert, ticket, dashboard | MTTD 24시간 이하 |
| 품질 | 저장 성공 여부 | parser error, false positive, rule hit | parser error 1% 이하 |

> 요약: SIEM은 로그 보관을 넘어 상관분석과 룰 튜닝으로 SOC 탐지 품질을 좌우함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 탐지 범위 | 장비별 콘솔 | 다중 로그 상관분석 | 계정, 네트워크, 엔드포인트 연계 필요 시 |
| 비용/성능 | 전체 로그 장기 저장 | tiered storage, hot/warm/cold 분리 | EPS 10,000 이상, 보존 1년 요구 |
| 운영/위험 | 기본 룰 의존 | rule tuning, risk scoring, UEBA 연계 | 오탐률 30% 초과 시 튜닝 필요 |

> 요약: SIEM은 로그량과 분석 요구가 동시에 크면 계층형 저장과 룰 튜닝 전략이 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 로그 누락 | collector 장애, agent 미설치 | heartbeat, source inventory, 수집 알림 | coverage 95% 이상 |
| 파싱 오류 | 포맷 변경, timezone 불일치 | parser regression test, NTP 동기화 | parser error 1% 이하 |
| 오탐 폭증 | 임계치·맥락 부재 | severity matrix, suppression, allowlist | false positive 30% 이하 |
| 저장 비용 증가 | EPS 증가와 장기 보존 | hot/warm/cold, 필드 필터링 | GB/day, query p95 5초 이하 |

> 요약: SIEM 운영 리스크는 로그 누락, 파싱 오류, 오탐, 저장 비용이며 수집률과 품질 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수집 상태 | 로그 소스 coverage 95%, 지연 5분 이하 | SIEM health dashboard |
| 탐지 품질 | MTTD 24시간 이하, 오탐 30% 이하 | incident timeline, alert disposition |
| 룰 운영 | 룰 월 1회 리뷰, ATT&CK mapping 80% | rule hit report, purple team |

> 요약: SIEM 성과는 로그 커버리지, MTTD, 오탐률, 룰 매핑률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 로그 설계: AD, IAM, EDR, firewall, proxy, cloud audit를 우선 수집하고 ECS/CEF 기준으로 user, host, src_ip, action 필드를 정규화함.
2. 룰 운영: ATT&CK 기반 correlation rule을 작성하고 월 1회 purple team 결과로 threshold, suppression, risk score를 조정함.
3. SOC 연계: critical alert는 15분 내 티켓 생성, SOAR enrichment, EDR host isolation 승인, 사후 rule tuning까지 case에 기록함.

**결론 (2줄):**
- 기술사 판단: SIEM은 로그 소스 커버리지와 parser 품질을 먼저 확보한 뒤 correlation rule을 확장해야 함.
- 향후 방향: SIEM은 UEBA, XDR, SOAR 연동으로 경보 triage와 대응 자동화까지 연결되는 보안 데이터 허브로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SIEM을 설명하시오", "보안 이벤트 분석을 기술하시오" | 로그 수집, 정규화, 상관분석, 경보 흐름 | 로그 관리와 SIEM 분석의 차이 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "운영 지표를 제시하시오" | 로그 소스, parser, rule tuning, ticket 연동 | coverage, parser error, MTTD, 오탐률 |

> 요약: 설명형은 SIEM 파이프라인을, 운영형은 수집 품질과 룰 튜닝 지표를 중심으로 작성함.
