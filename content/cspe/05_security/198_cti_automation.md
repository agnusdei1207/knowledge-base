---
title: "인텔리전스 기반 CTI 자동화 (CTI Automation)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 198
---

# 📖 【암기용】 개념 완전 이해

> 목적: CTI 자동화를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 위협 인텔리전스를 STIX/TAXII, TIP, SIEM, SOAR로 자동 수집·정규화·배포하는 운영 체계
- **왜 필요한가**: IP, domain, hash, TTP, 취약점 정보가 수동 보고서로 머물면 차단과 탐지 룰 반영이 늦어진다. 자동화는 confidence, TLP, valid_until을 기준으로 쓸 수 있는 정보만 SOC 조치로 전환함.
- **핵심 직관**: 뉴스 기사를 사람이 모두 읽는 대신, 내 회사 관련 기사만 점수화해 경보 룰과 차단 목록으로 자동 전달하는 필터와 배관임.

## 깊이 이해
- **배경·문제의식**: CTI feed는 양이 많고 IoC 만료 시간이 짧다. OASIS STIX는 CTI 표현 형식, TAXII는 HTTPS 기반 교환 API를 제공해 조직 간 공유와 도구 연동을 기계 처리 가능하게 함.
- **작동 원리**: source를 수집하고 STIX object로 정규화한다. confidence, TLP 2.0, valid_from, valid_until, ATT&CK mapping을 평가한 뒤 SIEM Sigma 룰, EDR block, SOAR playbook, vulnerability SLA로 배포함.
- **비유**: 물류 창고에서 바코드가 없는 물품은 분류가 늦다. STIX/TAXII는 위협 정보에 바코드와 운송 규격을 붙여 창고, 매장, 계산대가 같은 정보를 읽게 하는 표준임.
- **구체 예시**: 랜섬웨어 캠페인의 C2 domain이 TAXII collection으로 들어오면 TIP가 confidence 85, TLP:AMBER, ATT&CK T1071로 저장하고 4시간 내 SIEM 탐지 룰과 DNS 차단 후보를 생성함.
- **흔한 오해·주의점**: 자동 수집은 자동 차단과 다르다. confidence 70 미만, 만료 IoC, 업무 도메인 충돌, TLP:RED 정보는 자동 배포에서 제외해야 함.

## 연결 개념
- STIX/TAXII - CTI 구조화와 자동 교환 표준
- TIP/MISP - CTI 수집, 중복 제거, scoring, 배포 플랫폼
- SOAR - CTI hit를 대응 플레이북으로 전환

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CTI 자동화 답안은 feed 연동이 아니라 품질 평가, TLP 통제, STIX/TAXII, ATT&CK 매핑, 룰 전환률을 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CTI 자동화는 위협 정보를 표준 형식과 API로 수집·평가·배포해 탐지와 대응에 연결하는 체계임.
> 2. **가치**: critical IoC 4시간 내 배포, 룰 전환률 30%, false positive 10% 이하를 목표로 SOC 조치 시간을 줄임.
> 3. **판단 포인트**: STIX/TAXII, TLP 2.0, confidence, valid_until, ATT&CK mapping, 자동 차단 승인 기준을 함께 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CTI 운영 자동화 이해 확인 | STIX object, TAXII collection, TIP, SIEM/SOAR 배포 | CTI feed 구매와 동일시 |
| 품질 통제 확인 | confidence, source reliability, freshness, TLP, false positive | 수집량만 많게 쓰고 검증 기준 누락 |
| 보안 운영 연결 확인 | Sigma/YARA 룰, EDR 차단, 취약점 우선순위 | 보고서 생성으로 답안 종료 |

> 요약: 이 문제는 CTI를 표준화해 탐지·차단·패치로 전환하는 자동 운영 설계를 요구함.

---

## Ⅰ. 개요 및 필요성

CTI 자동화는 위협정보 운영 배관임. STIX/TAXII와 TIP를 통해 IoC, TTP, 취약점 정보를 수집·검증하고 SIEM, EDR, SOAR, 취약점 관리로 배포한다. 피드 과부하와 만료 IoC 오탐을 막기 위해 품질 점수와 공유등급 통제가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
CTI Source -> TAXII/API Ingestion -> TIP Normalization
  / Scoring/TLP/Freshness -> ATT&CK Mapping
  / SIEM Rule -> EDR Block -> SOAR Playbook -> Feedback
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Source | OSINT, ISAC, vendor, internal IR 정보 제공 | source reliability, collection scope |
| STIX/TAXII | CTI 표현과 HTTPS 교환 표준 | STIX 2.1, TAXII 2.1, collection API |
| TIP | 중복 제거, scoring, TLP, 만료 관리 | MISP, OpenCTI, commercial TIP |
| Detection Pipeline | Sigma, YARA, SIEM, EDR 룰 생성 | ATT&CK tactic/technique mapping |
| Feedback Loop | hit count, false positive, analyst verdict 반영 | confidence 재계산, feed 품질 평가 |

> 요약: CTI 자동화는 표준 수집, 품질 평가, 탐지 배포, 피드백을 하나의 폐루프로 운영함.

---

## Ⅲ. 동작원리 및 흐름도

```text
PIR 정의 -> TAXII/API 수집 -> STIX 정규화 -> 중복 제거
-> confidence/TLP/valid_until 평가 -> 룰·차단 후보 생성
-> 승인 배포 -> hit/오탐 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PIR과 feed source 선정 | feed별 owner, use case 지정 |
| 2 | STIX/TAXII, API, MISP sync로 수집 | ingestion 지연 30분 이하 |
| 3 | confidence, TLP, valid_until, 중복 제거 | confidence 70 이상 우선 |
| 4 | ATT&CK 매핑 후 SIEM/EDR/SOAR 배포 | critical IoC 4시간 내 배포 |
| 5 | hit count, false positive, analyst verdict 반영 | false positive 10% 이하 |

> 요약: CTI 자동화는 PIR에서 시작해 품질 검증을 거친 정보만 보안 도구에 배포하고 운영 결과로 점수를 보정함.

---

## Ⅳ. 특징

| 구분 | 수동 CTI 운영 | CTI 자동화 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 수집 | PDF, 메일, CSV 수동 반영 | STIX/TAXII, API, MISP sync | TAXII 2.1, STIX 2.1 |
| 품질 | 분석가 경험 기반 | confidence, TLP, valid_until scoring | confidence 70 이상 |
| 배포 | 보고서 중심 | SIEM 룰, EDR 차단, SOAR playbook | 4시간 내 critical 배포 |
| 개선 | 사후 회의 중심 | hit count와 오탐 피드백 자동 반영 | false positive 10% 이하 |

> 요약: CTI 자동화는 위협정보를 표준 형식과 품질 기준으로 걸러 보안 도구 실행 항목으로 바꿈.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 공유 방식 | 이메일·PDF 보고서 | TAXII collection, API, MISP sync | 다수 조직·도구 연동 필요 시 |
| 탐지 전환 | 수동 룰 작성 | Sigma/YARA 후보 자동 생성 | 월 1,000개 이상 IoC 처리 |
| 통제 기준 | 전량 수집 | TLP, confidence, freshness 필터 | 오탐·민감정보 공유 위험 존재 시 |

> 요약: CTI 자동화는 피드 양이 많고 탐지 전환 지연이 큰 SOC에서 우선 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 확산 | 저신뢰·만료 IoC 자동 배포 | confidence 70, valid_until, allowlist | false positive 10% 이하 |
| 공유 위반 | TLP:RED/AMBER 정보 무단 배포 | TLP 2.0 policy, recipient control | TLP violation 0건 |
| 탐지 부하 | 룰 과다 배포로 SIEM 비용·지연 증가 | priority queue, TTL, rule pruning | rule latency p95 5분 이하 |
| 공급망 위험 | 외부 feed 조작·poisoning | source reputation, signature, sandbox 검증 | poisoned feed 0건 |

> 요약: CTI 자동화 리스크는 오탐, 공유 위반, 룰 부하, feed poisoning이며 품질 점수와 배포 통제로 줄임.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 시간 | critical IoC 4시간 내 배포 | ingestion/deploy timestamp |
| 활용 | CTI 룰 전환률 30%, hit rate 추적 | TIP, SIEM rule backlog |
| 품질 | false positive 10% 이하, TLP 위반 0건 | analyst verdict, audit log |

> 요약: CTI 자동화 성과는 배포 시간, 룰 전환률, 오탐과 공유 위반 지표로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 표준 수집: OASIS STIX 2.1/TAXII 2.1, MISP sync, vendor API를 TIP에 연결하고 feed별 source reliability와 owner를 지정함.
2. 품질 필터: confidence 70 이상, valid_until 유효, TLP:CLEAR/GREEN 우선, TLP:AMBER는 내부 need-to-know 배포로 제한함.
3. 운영 연계: ATT&CK ID를 붙여 Sigma/YARA/EDR/SOAR 후보를 만들고 critical IoC 4시간, false positive 10% 이하, 룰 전환률 30%를 월간 검토함.

**결론 (2줄):**
- 기술사 판단: CTI 자동화는 feed 수집량보다 품질 필터와 SOC 실행 전환률이 성패를 결정함.
- 향후 방향: AI 기반 요약은 analyst verdict 보조에 쓰고, 차단 배포는 TLP·confidence·승인 정책을 통과한 항목으로 제한해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CTI 자동화를 설명하시오", "STIX/TAXII 활용을 기술하시오" | 수집, 정규화, scoring, 배포, 피드백 흐름 | 수동 CTI와 자동화 차이 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "운영 리스크를 설명하시오" | TLP, confidence, valid_until, 승인 배포 절차 | 오탐, 공유 위반, SIEM 부하 통제 |

> 요약: 설명형은 표준과 흐름, 설계형은 품질 필터와 배포 통제 기준으로 답안을 구성함.
