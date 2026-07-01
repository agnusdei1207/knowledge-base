---
title: "CVE·CVSS 취약점 채점 (CVE CVSS)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 62
---

# 📖 【암기용】 개념 완전 이해

> 목적: CVE와 CVSS를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: CVE는 취약점 이름표, CVSS는 취약점 심각도 계산 체계
- **왜 필요한가**: 조직은 매일 다수의 취약점 알림을 받는다. 공통 식별자와 점수 체계가 있어야 제품, 패치, 자산, SLA를 같은 기준으로 연결할 수 있다.
- **핵심 직관**: CVE는 환자 등록번호이고, CVSS는 증상의 심각도를 표준 항목으로 점수화한 진단표임.

## 깊이 이해
- **배경·문제의식**: 벤더마다 취약점 명칭이 다르면 동일 이슈를 추적하기 어렵다. CVE는 `CVE-YYYY-NNNN` 형식으로 식별자를 부여하고, CVSS는 공격 벡터와 영향도를 수치로 표현한다.
- **작동 원리**: CVSS 3.1은 Base, Temporal, Environmental로 구성된다. CVSS 4.0은 Attack Requirements, Safety, Automatable, Recovery 등 운영 판단 요소를 세분화한다.
- **비유**: 같은 화재라도 건물 종류와 사람 밀집도에 따라 대응 우선순위가 달라진다. CVSS Base는 불의 크기, Environmental은 우리 건물의 피해 가능성을 반영한다.
- **구체 예시**: CVSS 9.8 RCE라도 내부망 개발 서버면 30일 SLA가 가능할 수 있고, CVSS 7.5라도 인터넷 노출 VPN과 KEV 등재가 있으면 7일 이내 조치가 필요함.
- **흔한 오해·주의점**: CVSS는 위험도 전체가 아니다. 자산 중요도, exploit 공개, KEV, EPSS, 보상 통제, 업무 영향이 함께 반영되어야 한다.

## 연결 개념
- NVD - CVE, CVSS, CPE, CWE 정보를 제공하는 공개 취약점 DB
- EPSS/KEV - 실제 exploit 가능성과 알려진 악용 여부를 보완
- Patch Management - CVSS를 패치 SLA와 예외 승인으로 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CVE/CVSS 답안은 식별자와 점수 설명에서 끝내지 말고 자산 중요도, EPSS/KEV, 패치 SLA, 재검증으로 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CVE는 취약점 공통 식별자이고 CVSS는 공격 난이도와 영향도를 표준 지표로 산정하는 채점 체계임.
> 2. **가치**: 서로 다른 벤더·스캐너·티켓·패치 정보를 하나의 취약점 단위로 묶어 우선순위와 SLA를 설정함.
> 3. **판단 포인트**: CVSS Base/Temporal/Environmental, CVSS 3.1/4.0 차이, KEV/EPSS, asset criticality를 함께 써야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 표준 식별·채점 체계 이해 확인 | CVE ID, CNA, CVSS Base·Temporal·Environmental | CVE와 CVSS를 같은 개념으로 설명 |
| 취약점 우선순위 판단 확인 | CVSS 3.1/4.0, exploit maturity, environmental score | Base score만으로 패치 순위 단정 |
| 운영 연계 역량 확인 | KEV/EPSS, 인터넷 노출, 자산 등급, 패치 SLA, retest | 조치·재검증·예외 승인 누락 |

> 요약: CVE/CVSS 문제는 표준 점수를 조직 위험 점수와 패치 SLA로 변환하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

CVE는 취약점 ID, CVSS는 점수 체계이다. 취약점이 많아질수록 동일 이슈 식별, 영향 제품 추적, 우선순위 조정이 필요하다. CVE/CVSS는 NVD, 스캐너, ITSM, 패치 관리의 공통 언어로 사용됨.

---

## Ⅱ. 구조 및 구성요소

```text
취약점 발견 -> CVE ID 부여 -> CVSS 채점 -> 조직 위험 보정 -> SLA/조치
  / Base, Temporal, Environmental
  / KEV, EPSS, asset criticality, exposure
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| CVE ID | 취약점 공통 식별자 제공 | CNA가 할당, 중복 추적 방지 |
| CVSS Base | 공격 벡터와 영향도 고정 특성 점수화 | AV, AC, PR, UI, Scope, CIA |
| Temporal | exploit maturity와 remediation 수준 반영 | exploit code 공개 여부 |
| Environmental | 조직 자산 중요도와 보상 통제 반영 | 업무 중요도, 망 노출, 규제 영향 |
| Risk Context | KEV, EPSS, 인터넷 노출, asset criticality 결합 | SLA와 예외 승인 입력 |

> 요약: CVE가 취약점을 식별하고 CVSS가 기본 심각도를 제공하며, 조직 위험은 환경 보정과 exploit 정보로 확정됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
스캐너/벤더 권고 -> CVE 매핑 -> CVSS Base 확인
  / CVSS 3.1, CVSS 4.0
Temporal/Environmental 보정 -> KEV/EPSS 결합 -> SLA 지정 -> 패치/재검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 스캐너 결과와 벤더 권고를 CVE ID로 정규화 | 중복 티켓 5% 이하 |
| 2 | CVSS 3.1 Base 또는 CVSS 4.0 Base 지표 확인 | 점수·vector string 기록 |
| 3 | exploit maturity, remediation level, report confidence 반영 | exploit 공개 여부 증거 |
| 4 | 자산 중요도, 인터넷 노출, 보상 통제, 규제 영향 반영 | environmental score 산정 |
| 5 | KEV/EPSS와 결합해 SLA, 패치, 예외, retest 수행 | critical 7일, high 30일 |

> 요약: CVSS 점수는 Base에서 시작하되 실제 운영 순위는 Temporal, Environmental, KEV/EPSS 결합 후 결정됨.

---

## Ⅳ. 특징

| 구분 | CVE | CVSS | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 취약점 식별 | 취약점 심각도 채점 | ID vs score 구분 |
| 형식 | CVE-YYYY-NNNN | 0.0~10.0, vector string | 9.0 이상 critical |
| 운영 입력 | 제품·버전·패치 매핑 | Base/Temporal/Environmental | SLA 7/30/90일 |
| 한계 | 영향도 판단 불가 | 자산 맥락 미포함 가능 | KEV/EPSS 보완 필요 |

> 요약: CVE는 추적 기준이고 CVSS는 심각도 기준이며, 패치 우선순위는 조직 환경 점수로 보정해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 벤더별 취약점명 | CVE 기반 단일 ID | 다중 스캐너·다중 제품 운영 |
| 비용/성과 | 발견 순서대로 패치 | CVSS+EPSS+KEV 기반 SLA | backlog 1,000건 이상 |
| 운영/위험 | Base score 단독 | environmental score 보정 | 중요 자산·인터넷 노출 차등 |

> 요약: 취약점 규모가 커질수록 CVE 정규화와 CVSS 보정이 패치 우선순위의 기준이 됨.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 우선순위 오류 | CVSS Base 단독 사용 | KEV, EPSS, 노출도, 자산 등급 결합 | critical miss 0건 |
| 중복 티켓 | 스캐너별 이름 불일치 | CVE ID, CPE, package purl 정규화 | duplicate rate 5% 이하 |
| 조치 지연 | owner·SLA 부재 | ITSM 자동 배정, 7/30/90일 SLA | SLA compliance 95% |

> 요약: CVE/CVSS 운영 리스크는 점수 오해와 중복·지연이며, 정규화와 SLA 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 데이터 품질 | CVE 매핑률 95%, vector 기록 100% | 스캐너, SBOM, NVD API |
| 우선순위 | KEV 항목 7일 이내 조치 | ITSM, KEV feed, EPSS |
| 재검증 | retest pass 95%, 예외 만료 90일 | 재스캔, 예외 대장 |

> 요약: CVE/CVSS 성과는 점수 산정 자체가 아니라 매핑률, SLA 준수율, 재검증 통과율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 정규화: Nessus, OpenVAS, SCA, CSPM 결과를 CVE ID, CPE, package URL 기준으로 통합하고 중복 티켓을 5% 이하로 관리함.
2. 우선순위: CVSS 3.1/4.0 Base에 Temporal, Environmental, KEV, EPSS, 인터넷 노출, 자산 등급을 결합해 critical 7일, high 30일 SLA를 지정함.
3. 폐루프: 패치 완료는 재스캔 pass, 버전 증거, 예외 승인, 만료일 등록을 충족할 때만 종료 처리함.

**결론 (2줄):**
- 기술사 판단: CVSS 9.8 내부 개발 서버보다 CVSS 7.5 인터넷 노출 VPN과 KEV 등재 항목을 먼저 조치해야 함.
- 향후 방향: CVSS 4.0, EPSS, SBOM, VEX를 결합해 취약점 점수를 제품·자산·공급망 위험으로 확장해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CVE와 CVSS를 설명하시오" | CVE 할당, CVSS 3.1/4.0 점수 산정 흐름 | CVE와 CVSS 차이, Base/Temporal/Environmental |
| 요구사항 명시형 | "우선순위 방안을 제시하시오", "비교하시오" | KEV/EPSS, 자산 중요도, SLA 변환 | Base score 단독 한계와 environmental 보정 |

> 요약: 설명형은 표준 구성, 운영형·방안형은 점수 보정과 패치 SLA 연결을 중심으로 작성함.
