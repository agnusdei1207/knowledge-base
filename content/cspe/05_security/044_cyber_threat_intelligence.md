---
title: "사이버 위협 인텔리전스 CTI (Cyber Threat Intelligence)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 44
---

# 📖 【암기용】 개념 완전 이해

> 목적: 사이버 위협 인텔리전스 CTI를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 공격자, 동기, TTP, IoC, 취약점 정보를 의사결정 가능한 보안 정보로 가공한 것
- **왜 필요한가**: 보안팀은 매일 수천 개 IoC와 취약점 알림을 받는다. CTI는 우리 조직에 중요한 위협을 PIR 기준으로 골라 탐지·차단·패치 우선순위로 바꾼다.
- **핵심 직관**: 날씨 데이터가 아니라 "내일 이 지역에 폭우가 오니 지하 주차장을 막아라"는 행동 지침이 인텔리전스임.

## 깊이 이해
- **배경·문제의식**: raw feed는 IP, 도메인, 해시 목록일 뿐이다. 출처 신뢰도, 시간성, 관련 산업, 공격 그룹, 실제 탐지 가능성을 평가해야 SOC가 쓸 수 있다.
- **작동 원리**: 요구사항(PIR) 정의, 수집, 처리, 분석, 배포, 피드백의 intelligence cycle로 운영한다. 수준은 strategic, tactical, operational, technical로 나뉜다.
- **비유**: 신문 기사 더미에서 내 회사의 해외 공장, VPN 장비, 협력사와 관련된 기사만 골라 대응 일정으로 바꾸는 작업과 같다.
- **구체 예시**: "국내 제조업 VPN 취약점 악용" CTI가 들어오면 strategic은 경영 리스크, tactical은 ATT&CK T1133, operational은 캠페인 일정, technical은 IP·도메인·YARA로 분리한다.
- **흔한 오해·주의점**: CTI는 피드 구독 자체가 아니다. 신뢰도, TLP, 만료일, 탐지 룰 전환, 차단 영향 평가가 있어야 함.

## 연결 개념
- STIX/TAXII - CTI를 구조화해 자동 공유하는 표준
- MITRE ATT&CK - CTI의 TTP를 공통 기법으로 매핑
- SOC/SIEM/SOAR - CTI를 탐지 룰과 대응 playbook으로 실행

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CTI 답안은 strategic/tactical/operational/technical, PIR, CTI 품질, SOC 적용 지표를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CTI는 raw threat data를 조직 의사결정과 탐지·대응에 쓸 수 있게 분석한 위협 정보임.
> 2. **가치**: PIR 기반으로 위협 우선순위를 정하고 IoC, TTP, 취약점, 공격 그룹 정보를 SOC 조치로 전환함.
> 3. **판단 포인트**: feed 수량보다 출처 신뢰도, 시간성, 관련성, false positive, 탐지 룰 전환률을 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CTI 계층 이해 확인 | strategic, tactical, operational, technical | IoC 목록과 CTI를 동일시 |
| 운영 적용 판단 확인 | PIR, intelligence cycle, SOC 배포 | 피드 구독만 답안에 제시 |
| 품질 관리 역량 확인 | 신뢰도, TLP, freshness, false positive | 출처·만료·검증 기준 누락 |

> 요약: CTI 문제는 데이터를 분석해 조직 우선순위와 SOC 행동으로 바꾸는 능력을 묻는 문제임.

---

## Ⅰ. 개요 및 필요성

- 개요: 의사결정형 위협 정보
- 배경: raw feed는 IP·도메인·해시 목록에 가깝고, 조직 자산·산업·지역·공격 그룹 맥락이 없으면 오탐 차단과 정보 과부하를 유발함.
- 필요성: CTI는 PIR, confidence 0~100, TLP, valid_until 기준으로 탐지·차단·패치·경영 보고에 배포해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
PIR -> 수집 -> 처리/정규화 -> 분석 -> 배포 -> 피드백
  / Strategic, Tactical, Operational, Technical CTI
  / SIEM, EDR, SOAR, Vulnerability Management 적용
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| PIR | 조직이 답해야 할 우선 정보 요구 | 산업, 자산, 지역, 공격 그룹 기준 |
| CTI 유형 | 전략·전술·운영·기술 계층 분리 | 경영 보고부터 IoC 차단까지 범위 차이 |
| 품질 속성 | 신뢰도, 관련성, 시간성, TLP | confidence, source, valid_until |
| 배포 채널 | SIEM, EDR, SOAR, ISAC, MISP | STIX/TAXII, API, report |

> 요약: CTI는 PIR을 기준으로 수집·분석·배포되고, 품질 속성과 배포 채널이 함께 관리되어야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
정보 요구 정의 -> 외부/내부 데이터 수집 -> 중복 제거/정규화
-> 신뢰도·관련성 분석 -> SOC 룰/차단 배포 -> 피드백 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PIR과 수집 범위 정의 | crown jewel, 산업, 지역, 기술 스택 |
| 2 | OSINT, ISAC, vendor, dark web, 내부 IR 수집 | source reliability, TLP |
| 3 | IoC/TTP/취약점 분석과 우선순위화 | confidence 0~100, freshness |
| 4 | SIEM 룰, EDR 차단, 패치 계획으로 배포 | hit count, false positive, SLA |

> 요약: CTI는 요구사항에서 시작해 품질 평가를 거친 뒤 탐지·차단·패치 조치로 끝나는 intelligence cycle임.

---

## Ⅳ. 특징

| 구분 | Raw Threat Feed | CTI | 수치·로그 포인트 |
|:---|:---|:---|:---|
| 형태 | IP, domain, hash 목록 | 맥락·신뢰도·대응 권고 포함 | confidence 0~100 |
| 기준 | 공급자 제공량 | PIR과 조직 관련성 | relevance score |
| 적용 | 단순 차단 | SIEM 룰, hunting, patch 우선순위 | rule conversion rate |
| 한계 | 오탐·만료 IoC | 분석 인력과 피드백 필요 | false positive rate 10% 이하 |

> 요약: CTI는 feed 수량이 아니라 맥락, 신뢰도, 조직 관련성, 실행 가능성으로 평가해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 의사결정 | 취약점 CVSS 순위 | PIR 기반 위협 우선순위 | 실제 노출 자산과 exploit activity 연결 |
| 탐지 단위 | IoC 차단 | IoC + TTP + 캠페인 | 변종 대응과 헌팅 필요 시 |
| 공유 방식 | PDF 보고서 | STIX/TAXII, MISP, API | 자동 수집·검증·배포 필요 시 |

> 요약: CTI는 취약점, IoC, 공격 그룹 정보를 조직 위험 기준으로 재정렬할 때 적용 가치가 있음.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 차단 | 만료·저신뢰 IoC 배포 | confidence 임계값 70 이상, valid_until 적용 | false positive rate 10% 이하 |
| 정보 과부하 | PIR 없는 feed 수집 | PIR별 owner와 use case 지정 | unused feed ratio |
| 민감정보 노출 | TLP·공유 범위 미준수 | TLP:RED/AMBER/GREEN/CLEAR 마킹 | TLP violation 0건 |

> 요약: CTI 리스크는 오탐, 정보 과부하, 공유 통제 실패이며 신뢰도·PIR·TLP로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 품질 | confidence 70 이상 feed 우선 배포 | TIP score, analyst review |
| 활용 | CTI의 탐지 룰 전환률 30% 이상 | SIEM/EDR rule backlog |
| 시간성 | critical IoC 4시간 내 배포 | ingestion timestamp, deploy timestamp |

> 요약: CTI 운영 성과는 품질 점수, 룰 전환률, 배포 지연시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. PIR 수립: 산업, 핵심 자산, 해외 사업장, VPN·메일·클라우드 스택을 기준으로 분기별 PIR 10개 이하를 정의함.
2. 품질 관리: feed별 source reliability, confidence 0~100, valid_until, TLP를 기록하고 confidence 70 미만 IoC는 자동 차단에서 제외함.
3. SOC 연계: CTI를 ATT&CK ID, Sigma 룰, EDR 차단, SOAR playbook, 취약점 패치 SLA와 연결해 hit count와 false positive를 검토함.

**결론 (2줄):**
- 기술사 판단: CTI는 feed 구매가 아니라 PIR 기반 분석과 SOC 실행 지표로 가치가 검증됨.
- 향후 방향: STIX/TAXII, TIP, XDR 연계를 통해 CTI 수집부터 탐지 룰 배포까지 4시간 이내 자동화를 목표로 해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CTI를 설명하시오" | intelligence cycle과 CTI 4계층 | raw feed와 CTI 차이, 품질 속성 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 체계를 설계하시오" | PIR, 품질 평가, SIEM/EDR 배포 흐름 | confidence, TLP, 룰 전환률, 배포 SLA |

> 요약: 설명형은 CTI 개념과 계층, 운영형은 PIR과 품질 기반 SOC 적용을 중심으로 작성함.
