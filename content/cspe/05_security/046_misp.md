---
title: "MISP 위협 공유 플랫폼 (MISP)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 46
---

# 📖 【암기용】 개념 완전 이해

> 목적: MISP 위협 공유 플랫폼을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 침해 지표와 위협 맥락을 Event 단위로 구조화해 조직 간 공유하는 오픈소스 CTI 플랫폼
- **왜 필요한가**: 악성 IP 하나만 전달하면 재사용이 어렵다. 공격 캠페인, TTP, 신뢰도, TLP, 관계 객체를 함께 공유해야 SOC 탐지 규칙과 차단 정책으로 연결됨.
- **핵심 직관**: 보안 사고 메모를 엑셀로 돌리는 대신, 사건 카드에 증거, 태그, 공개 범위, API 연동을 붙여 여러 기관이 같은 언어로 쓰는 방식임.

## 깊이 이해
- **배경·문제의식**: 위협 정보는 조직마다 포맷이 다르면 수작업 정리가 필요하고, 오탐 IoC가 방화벽·SIEM에 투입되어 운영 리스크가 생김. MISP는 event, attribute, object, tag, galaxy, sharing group으로 맥락을 표준화함.
- **작동 원리**: 분석자는 침해 사건을 Event로 생성하고 IP, URL, hash, domain을 Attribute로 등록한다. File, network connection 같은 Object로 관계를 묶고, TLP:AMBER 등 Tag로 공유 범위를 지정한 뒤 REST API, STIX export, TAXII 연계로 배포함.
- **비유**: 병원에서 환자 증상만 말하면 진단이 어렵지만, 검사 수치, 감염 경로, 격리 등급, 전원 가능 병원을 함께 적은 의무기록은 즉시 조치로 이어짐.
- **구체 예시**: 랜섬웨어 캠페인 Event에 SHA-256 hash 12개, C2 domain 4개, MITRE ATT&CK T1486, TLP:AMBER, confidence 80을 등록하고 SIEM watchlist와 EDR blocklist로 동기화함.
- **흔한 오해·주의점**: MISP는 SIEM이 아니다. 로그를 실시간 수집·상관분석하는 도구가 아니라, 검증된 CTI를 저장·공유·배포하는 플랫폼임.

## 연결 개념
- STIX/TAXII - MISP 데이터를 표준 위협 인텔리전스 형식과 전송 방식으로 교환
- CTI - 위협 정보를 수집, 평가, 배포하는 보안 운영 기능
- SIEM/SOAR - MISP IoC를 탐지 규칙과 자동 대응 플레이북으로 사용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: MISP 답안은 event/attribute/object/tag/TLP/API/STIX export를 반드시 포함하고, CTI 공유가 SIEM 탐지와 SOAR 대응으로 이어지는 구조를 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MISP는 침해 사건을 Event로 묶고 Attribute, Object, Tag, Galaxy로 위협 맥락을 구조화하는 CTI 공유 플랫폼임.
> 2. **가치**: IoC를 TLP, confidence, sharing group과 함께 배포해 SOC가 watchlist, correlation rule, blocklist로 재사용하도록 함.
> 3. **판단 포인트**: STIX export, REST API, 동기화 정책, 오탐 검증, 수명주기 관리를 함께 써야 단순 IoC 목록 답안을 피함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CTI 공유 구조 이해 확인 | Event, Attribute, Object, Tag, TLP, Galaxy | MISP를 로그 분석 장비로 오인 |
| 표준 연계 역량 확인 | REST API, STIX 2.x export, TAXII 연계, sync server | IoC 수동 입력 절차만 서술 |
| 운영 통제 판단 확인 | confidence, false positive, expiry, sharing group | 검증 없는 자동 차단 권고 |

> 요약: MISP 문제는 위협 정보를 구조화하고 공유 범위와 신뢰도를 통제해 SOC 탐지로 연결하는 능력을 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: CTI 공유 플랫폼
- 배경: 침해 지표를 IP·해시 목록으로만 전달하면 사건 맥락, 신뢰도, 공개 범위, ATT&CK 관계가 사라져 SOC 재사용이 어려움.
- 필요성: MISP는 Event, Attribute, Object, Tag, TLP를 구조화하고 sync lag 10분 이하 기준으로 SIEM·SOAR·EDR에 배포해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Analyst -> Event 생성 -> Attribute/Object 등록 -> Tag/TLP 지정
        -> Galaxy/ATT&CK 매핑 -> API/STIX export -> SIEM/SOAR/EDR 연동
        +-> Sharing Group/Sync Server로 공유 범위 통제
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Event | 침해 사건, 캠페인, 분석 단위 | 날짜, 조직, distribution, threat level 포함 |
| Attribute | IP, domain, URL, hash, email 등 관측값 | to_ids 값으로 탐지 투입 여부 결정 |
| Object | file, process, network connection 관계 묶음 | 단일 IoC보다 맥락 표현 |
| Tag/TLP/Galaxy | 분류, 공개 범위, ATT&CK·위협그룹 매핑 | TLP:RED/AMBER/GREEN/WHITE |
| API/STIX Export | 외부 시스템 연계 | REST API, STIX 2.x, JSON, CSV |

> 요약: MISP는 Event를 중심으로 지표, 관계, 태그, 공유 정책, API를 결합해 CTI를 운영 가능한 데이터로 전환함.

---

## Ⅲ. 동작원리 및 흐름도

```text
침해 분석 -> Event 작성 -> Attribute 검증 -> Tag/TLP 부여
-> STIX export/API 배포 -> SIEM correlation rule 반영
-> 탐지 결과 피드백 -> false positive/expiry 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IoC와 TTP 수집, 중복 Event 확인 | source, timestamp, confidence |
| 2 | Attribute/Object 등록과 ATT&CK tag 매핑 | to_ids=true, category/type 적합성 |
| 3 | TLP와 sharing group으로 배포 범위 결정 | TLP:AMBER 이하 외부 공유 |
| 4 | API, STIX export로 SIEM/SOAR 연동 | export 성공률 99%, sync lag 10분 이하 |
| 5 | 오탐·만료·피드백 반영 | false positive rate 5% 이하, expiry date |

> 요약: MISP 운영은 수집, 구조화, 공유, 탐지 반영, 피드백 갱신의 폐루프로 동작함.

---

## Ⅳ. 특징

| 구분 | 단순 IoC 목록 | MISP 기반 CTI | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 데이터 구조 | IP·hash 나열 | Event, Attribute, Object 관계 | STIX 2.x export |
| 공유 통제 | 메일·파일 전달 | TLP, distribution, sharing group | TLP:AMBER 기준 외부 공유 |
| 운영 연계 | 수동 차단 | API로 SIEM watchlist, EDR blocklist 반영 | sync lag 10분 이하 |
| 품질 관리 | 출처·만료 불명 | confidence, sighting, expiry 관리 | false positive rate 5% 이하 |

> 요약: MISP는 IoC를 맥락과 통제 속성까지 포함한 CTI 객체로 관리해 탐지 자동화의 입력 품질을 보장함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 공유 방식 | 이메일, CSV, 메신저 | MISP sync, API, STIX export | 다기관 공유와 이력 추적 필요 시 |
| 탐지 연계 | 수동 룰 작성 | to_ids attribute 기반 SIEM 연동 | 일 1,000건 이상 IoC 갱신 |
| 거버넌스 | 담당자 판단 의존 | TLP, sharing group, confidence | 외부 공유 승인 절차 필요 시 |

> 요약: IoC 규모와 공유 조직 수가 증가하면 MISP 기반 구조화와 배포 통제가 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 확산 | 검증 전 to_ids 투입 | confidence 70 이상, sandbox 검증 후 배포 | false positive rate 5% 이하 |
| 정보 과다 공유 | TLP·sharing group 오분류 | TLP 리뷰, 민감 Event 승인 workflow | TLP 위반 0건 |
| 탐지 지연 | API 동기화 실패 | retry, queue, sync health monitoring | sync lag 10분 이하 |
| IoC 노후화 | 만료일·sighting 미관리 | expiry, decay model, sighting 반영 | expired IoC 95% 제거 |

> 요약: MISP의 핵심 리스크는 오탐, 과다 공유, 동기화 지연, 노후 IoC이며 지표 기반 품질 관리가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 공유 품질 | confidence 70 이상 Event 비율 90% | Event metadata audit |
| 연동 성과 | SIEM 반영 IoC 적중률 10% 이상 | alert match, sighting 통계 |
| 운영 통제 | TLP 위반 0건, sync lag 10분 이하 | API log, sharing group audit |

> 요약: MISP 도입 효과는 공유 품질, 탐지 적중률, TLP·동기화 통제로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 데이터 모델: Event 기준으로 campaign, malware, threat actor를 분리하고 Attribute에는 type, category, to_ids, confidence, expiry를 의무 입력함.
2. 연동 체계: REST API와 STIX 2.x export로 SIEM watchlist, SOAR enrichment, EDR blocklist를 10분 주기 동기화함.
3. 품질 통제: TLP 리뷰, sharing group 승인, false positive 피드백, sighting 기반 decay로 만료 IoC를 주 1회 정리함.

**결론 (2줄):**
- 기술사 판단: MISP는 CTI 공유가 2개 조직 이상, 일 1,000건 이상 IoC 갱신, TLP 통제가 필요한 환경에서 우선 적용함.
- 향후 방향: MISP, STIX/TAXII, SOAR playbook 연동으로 위협 공유에서 탐지·대응까지 MTTD 24시간 이하 목표로 운영함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MISP를 설명하시오", "CTI 공유를 기술하시오" | Event, Attribute, Object, Tag, API 동작 흐름 | 단순 IoC 목록과 구조화 CTI 차이 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "STIX/TAXII와 비교하시오" | 공유 범위, STIX export, SIEM/SOAR 연동 | TLP, confidence, 오탐, sync lag 관리 |

> 요약: 설명형은 MISP 객체 모델을, 방안형은 공유 통제와 SOC 연동 지표를 중심으로 작성함.
