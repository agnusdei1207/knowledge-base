---
title: "STIX·TAXII 위협 공유 (STIX TAXII)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 45
---

# 📖 【암기용】 개념 완전 이해

> 목적: STIX·TAXII 위협 공유를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: STIX는 위협 정보를 표현하는 구조화 포맷, TAXII는 이를 교환하는 전송 프로토콜
- **왜 필요한가**: CTI를 PDF나 메일로 공유하면 IoC, 공격 그룹, 관계, 신뢰도, TLP가 시스템에 바로 반영되지 않는다. STIX/TAXII는 자동 수집과 배포를 가능하게 한다.
- **핵심 직관**: STIX는 택배 상자의 표준 라벨이고, TAXII는 그 상자를 주고받는 배송 규칙임.

## 깊이 이해
- **배경·문제의식**: 위협 공유는 조직 간 표현 방식이 다르면 자동화가 어렵다. 같은 IP라도 출처, 관측 시간, 관련 악성코드, TLP가 빠지면 오탐 차단이 생긴다.
- **작동 원리**: STIX 객체(indicator, malware, attack-pattern, relationship, sighting 등)로 정보를 구조화하고, TAXII server의 collection을 통해 client가 조회·수신한다.
- **비유**: 병원 처방전을 표준 코드로 쓰고 전자문서망으로 교환해야 약국 시스템이 자동 처리하는 것과 같다.
- **구체 예시**: 랜섬웨어 캠페인의 malicious domain indicator, malware 객체, ATT&CK attack-pattern, relationship, confidence 85, TLP:AMBER 마킹을 STIX bundle로 만들고 TAXII collection에 배포한다.
- **흔한 오해·주의점**: STIX와 TAXII는 같은 것이 아니다. STIX는 내용 형식, TAXII는 전달 방식이며, 신뢰도·TLP·만료일 검증 없이 자동 차단하면 오탐 피해가 발생한다.

## 연결 개념
- CTI - STIX/TAXII로 표현·전송되는 위협 인텔리전스
- MISP - STIX/TAXII 연동 가능한 위협 공유 플랫폼
- SIEM/SOAR - 수신한 indicator를 탐지 룰과 대응 playbook으로 적용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: STIX/TAXII 답안은 구조화 포맷, 전송 프로토콜, 신뢰도, TLP, SOC 적용 지표를 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: STIX는 CTI 객체 표현 표준이고 TAXII는 CTI 교환을 위한 API 기반 전송 프로토콜임.
> 2. **가치**: 위협 정보를 indicator, malware, attack-pattern, relationship으로 구조화해 SIEM, EDR, SOAR에 자동 배포함.
> 3. **판단 포인트**: 자동 공유보다 confidence, TLP, valid_until, 출처 신뢰도, 오탐 차단 통제를 함께 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 표준 구조 이해 확인 | STIX 객체와 TAXII collection/API 구분 | STIX와 TAXII를 같은 기술로 설명 |
| 위협 공유 운영 확인 | 신뢰도, TLP, 만료일, 출처 검증 | IoC 자동 차단만 제시 |
| SOC 연동 판단 확인 | SIEM/EDR/SOAR 배포와 오탐 지표 | 공유 플랫폼 이름만 나열 |

> 요약: STIX/TAXII 문제는 CTI를 표준 포맷으로 만들고 TLP·신뢰도 기준으로 전송·적용하는 운영 통제까지 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: CTI 표현·전송 표준
- 배경: PDF, CSV, 메일 기반 위협 공유는 IoC 관계, 신뢰도, TLP, 만료일을 자동 처리하기 어렵고 SOC 반영 지연을 만든다.
- 필요성: STIX 2.x 객체와 TAXII 2.x HTTPS collection을 사용하고 confidence, TLP, valid_until 검증 후 SIEM·EDR·SOAR에 배포해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
CTI Producer -> STIX Bundle -> TAXII Server/Collection
-> TAXII Client -> TIP/SIEM/EDR/SOAR -> 탐지/차단/헌팅
  / confidence, TLP, valid_until, source 검증
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| STIX Object | indicator, malware, attack-pattern 등 표현 | JSON, relationship, sighting 포함 |
| TAXII Service | API root, collection, manifest, object 제공 | HTTPS, 인증, access control |
| Trust Marking | confidence, TLP, marking-definition | 공유 범위와 자동 적용 기준 |
| SOC Consumer | TIP, SIEM, EDR, SOAR 연동 | 룰 배포, 차단, 헌팅 쿼리 전환 |

> 요약: STIX는 객체 구조, TAXII는 collection 기반 전송, SOC는 수신 정보를 검증해 탐지·차단에 적용함.

---

## Ⅲ. 동작원리 및 흐름도

```text
위협 정보 생성 -> STIX 객체 작성 -> TLP/confidence 부여
-> TAXII collection 게시 -> client 수신 -> 검증 후 SOC 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | IoC, TTP, 관계 정보를 STIX bundle로 작성 | object type, id, created, modified |
| 2 | 신뢰도와 공유 등급 부여 | confidence 0~100, TLP:AMBER 등 |
| 3 | TAXII collection에 게시·조회 | auth, collection id, manifest |
| 4 | TIP/SIEM/EDR에 배포 전 검증 | dedup, valid_until, false positive |

> 요약: STIX/TAXII 운영은 구조화, 신뢰도 부여, API 전송, 소비자 검증의 순서로 진행됨.

---

## Ⅳ. 특징

| 구분 | 비정형 공유 | STIX/TAXII 공유 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 표현 | PDF, CSV, 메일 | STIX JSON 객체와 관계 | STIX 2.x |
| 전송 | 수동 다운로드 | TAXII collection API | TAXII 2.x, HTTPS |
| 통제 | 공유 범위 불명확 | TLP, confidence, marking | TLP:RED/AMBER/GREEN/CLEAR |
| 한계 | 자동화 곤란 | 품질 낮은 feed는 오탐 유발 | false positive rate 10% 이하 |

> 요약: STIX/TAXII는 CTI 자동화를 위한 표준이지만 품질 검증 없이 차단 정책에 연결하면 오탐 리스크가 발생함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 공유 형식 | CSV, PDF, 메일 | STIX 객체와 relationship | 공격자-악성코드-기법 관계 표현 필요 |
| 전송 방식 | 포털 수동 조회 | TAXII API collection | 실시간 수집과 자동 배포 필요 |
| 적용 통제 | 운영자 수동 판단 | confidence, TLP, valid_until 정책 | 자동 차단 전 품질 기준 필요 |

> 요약: 관계형 CTI와 자동 배포가 필요할 때 STIX/TAXII를 적용하고, 차단 전 품질 정책을 둬야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 차단 | 저신뢰 indicator 자동 배포 | confidence 70 이상, valid_until 필수 | false positive rate 10% 이하 |
| 정보 유출 | TLP 위반 공유 | marking-definition 검증, RBAC | TLP violation 0건 |
| 중복·충돌 | 여러 feed의 동일 IoC 불일치 | dedup, source priority, last_seen 관리 | duplicate ratio 5% 이하 |

> 요약: STIX/TAXII 리스크는 오탐, TLP 위반, 중복 충돌이며 신뢰도·접근통제·중복 제거로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수집 품질 | confidence 70 이상 객체 80% | TIP validation report |
| 배포 지연 | critical indicator 4시간 내 SIEM 반영 | TAXII ingest time, SIEM deploy time |
| 적용 성과 | CTI hit 중 incident 전환률 5% 이상 | alert disposition, case link |

> 요약: STIX/TAXII 성과는 수집 품질, 배포 지연, incident 전환률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 표준 수집: TAXII 2.x collection을 TIP에 연동하고 STIX indicator, malware, attack-pattern, relationship 객체를 정규화함.
2. 품질 통제: confidence 70 이상, TLP 허용 범위, valid_until 존재, source reliability 기준을 통과한 객체만 SIEM/EDR에 배포함.
3. SOC 적용: indicator는 차단·탐지 룰, attack-pattern은 ATT&CK hunting query, relationship은 incident graph로 전환하고 hit count를 주간 검토함.

**결론 (2줄):**
- 기술사 판단: STIX/TAXII는 위협 공유 자동화 표준이며, 자동 차단은 신뢰도·TLP·만료일 기준을 통과한 경우에만 적용해야 함.
- 향후 방향: MISP, TIP, SIEM, SOAR 연계를 통해 CTI 수집부터 대응 playbook 실행까지 4시간 이내 처리 체계를 구축해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "STIX/TAXII를 설명하시오" | STIX 객체 작성과 TAXII 전송 흐름 | 비정형 공유와 표준 공유 차이 |
| 요구사항 명시형 | "위협 공유 체계를 설계하시오", "운영 방안을 제시하시오" | confidence, TLP, valid_until 검증 후 SOC 배포 | 오탐률, 배포 지연, incident 전환률 |

> 요약: 설명형은 포맷과 프로토콜 구분, 설계형은 신뢰도·TLP 기반 자동 배포 통제를 중심으로 작성함.
