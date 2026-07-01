---
title: "MITRE ATT&CK 프레임워크 (MITRE ATT&CK)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 42
---

# 📖 【암기용】 개념 완전 이해

> 목적: MITRE ATT&CK을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 실제 공격자 행위를 전술, 기법, 절차로 정리한 공개 지식체계
- **왜 필요한가**: 해시·IP 같은 IoC는 바뀌기 쉽지만, 자격증명 탈취, PowerShell 실행, lateral movement 같은 TTP는 공격 습관으로 반복된다.
- **핵심 직관**: 도둑의 얼굴보다 침입 방식, 이동 경로, 훔치는 순서를 기록해 다음 침입을 알아보는 지도임.

## 깊이 이해
- **배경·문제의식**: 보안 장비 알림은 제품별 표현이 달라 조직 전체 탐지 공백을 보기 어렵다. ATT&CK은 공격 행위를 공통 언어로 표준화해 SOC, IR, Red Team, 경영 보고를 연결한다.
- **작동 원리**: 전술(Tactic)은 공격 목적, 기법(Technique)은 목적 달성 방법, 절차(Procedure)는 실제 공격자가 수행한 구체 행위다. 탐지 룰과 로그 소스를 기법에 매핑해 coverage matrix를 만든다.
- **비유**: 축구 전술판에서 "득점"이 전술, "측면 돌파"가 기법, "7번 선수가 오른쪽에서 컷백"이 절차인 것과 같다.
- **구체 예시**: T1059 Command and Scripting Interpreter는 PowerShell, cmd, bash 실행을 포함한다. EDR event 4688과 PowerShell 4104 로그로 탐지하고, 허용 목록 기반으로 오탐을 줄인다.
- **흔한 오해·주의점**: ATT&CK은 보안 제품 인증표가 아니다. 매트릭스 색칠보다 실제 로그 소스, 탐지 룰, 대응 playbook 존재 여부가 중요함.

## 연결 개념
- Cyber Kill Chain - 공격 흐름의 큰 단계 제공
- Threat Hunting - ATT&CK 기법을 가설로 삼아 수동 탐색 수행
- CTI - 공격 그룹과 캠페인의 TTP를 ATT&CK 기법으로 매핑

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: ATT&CK 답안은 tactic/technique/procedure, coverage matrix, 로그 소스, 탐지 룰 품질을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MITRE ATT&CK은 실제 공격자 TTP를 전술, 기법, 절차로 체계화한 지식 기반임.
> 2. **가치**: SOC 탐지 룰, 위협 헌팅, Red Team 검증, CTI 분석을 공통 언어와 coverage matrix로 연결함.
> 3. **판단 포인트**: 기법명 암기가 아니라 로그 소스, 탐지 로직, 오탐률, 탐지 공백 보완 계획을 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ATT&CK 구조 이해 확인 | tactic, technique, sub-technique, procedure 구분 | kill chain 7단계와 동일시 |
| SOC 적용 역량 확인 | coverage matrix, log source, detection rule | 매트릭스 색칠만 제시 |
| 탐지 품질 판단 확인 | false positive, rule tuning, purple team 검증 | 제품명·프레임워크명 나열 |

> 요약: ATT&CK 문제는 공격 행위를 공통 언어로 매핑하고 실제 탐지 커버리지를 증명하는 답안이 필요함.

---

## Ⅰ. 개요 및 필요성

MITRE ATT&CK은 TTP 지식체계다. APT와 랜섬웨어는 도구를 바꾸어도 권한 상승, 방어 회피, 내부 이동 절차를 반복한다. SOC는 ATT&CK으로 로그와 탐지 룰을 매핑해 탐지 공백을 수치화해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Threat Actor -> Tactic -> Technique -> Procedure
  / Log Source -> Detection Rule -> Coverage Matrix -> Response Playbook
  / CTI, Red Team, Threat Hunting 검증
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Tactic | 공격자의 단계별 목적 | Initial Access, Execution, Defense Evasion |
| Technique/Sub-technique | 목적 달성 방법 | T1059, T1003 등 식별자 기반 관리 |
| Procedure | 특정 그룹의 실제 실행 절차 | 명령행, 도구, 파일 경로, 레지스트리 |
| Coverage Matrix | 기법별 탐지·대응 현황 | 로그 소스, 룰, playbook, owner 표시 |

> 요약: ATT&CK은 목적-방법-실행 절차를 표준화하고, 이를 탐지 룰과 coverage matrix로 운영화함.

---

## Ⅲ. 동작원리 및 흐름도

```text
CTI/IR 사례 수집 -> ATT&CK 기법 매핑 -> 로그 소스 확인
-> 탐지 룰 작성 -> 오탐 튜닝 -> Purple Team 검증 -> 공백 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 침해 사례와 CTI에서 TTP 추출 | group, software, campaign tag |
| 2 | TTP를 technique ID로 매핑 | T1059, T1003 등 식별자 |
| 3 | 로그 소스와 탐지 룰 연결 | event 4688, Sysmon, EDR telemetry |
| 4 | Red/Purple Team으로 룰 검증 | detection hit, false positive rate |

> 요약: ATT&CK 운영은 TTP를 기법 ID로 바꾼 뒤 로그와 룰로 검증하는 반복 절차임.

---

## Ⅳ. 특징

| 구분 | IoC 중심 탐지 | ATT&CK 기반 탐지 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| 탐지 대상 | 해시, IP, 도메인 | TTP 행위 패턴 | process, command line, network flow |
| 지속성 | IoC 변경 시 우회 | 기법 반복성 활용 | technique coverage 80% 목표 |
| 운영 산출물 | 차단 목록 | coverage matrix, hunting query | Sigma, YARA, EDR rule |
| 한계 | 변종 대응 취약 | 로그 품질 없으면 색칠표로 전락 | false positive rate 10% 이하 |

> 요약: ATT&CK은 IoC보다 지속되는 공격 행위 탐지에 적합하나 로그 소스와 룰 검증이 없으면 운영 가치가 낮음.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 분석 모델 | Cyber Kill Chain | ATT&CK matrix | 세부 탐지 룰과 헌팅 쿼리 작성 |
| 탐지 단위 | 장비 알림 | TTP technique | 제품별 알림을 공통 기준으로 통합 |
| 검증 방식 | 침해 후 리뷰 | Purple Team exercise | 분기별 탐지 커버리지 검증 |

> 요약: Kill Chain은 흐름 설명, ATT&CK은 세부 TTP 탐지와 검증에 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 매핑 과잉 | 모든 룰을 technique에 억지 연결 | evidence 기반 매핑 승인 절차 | unmapped rule review 월 1회 |
| 탐지 공백 | 로그 소스 미수집 | Sysmon, PowerShell 4104, DNS, proxy 수집 | log source coverage 95% |
| 오탐 증가 | 기법 조건이 넓음 | allowlist, 빈도 기준, 다중 이벤트 상관 | false positive rate 10% 이하 |

> 요약: ATT&CK 운영 리스크는 매핑 품질, 로그 공백, 오탐이며 증거 기반 검토와 룰 튜닝으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 커버리지 | 우선 technique 50개 중 탐지 40개 이상 | ATT&CK navigator, SIEM mapping |
| 탐지 품질 | high severity 룰 precision 90% 목표 | alert disposition 분석 |
| 검증 주기 | 분기 1회 Purple Team | emulation plan, detection report |

> 요약: ATT&CK 성숙도는 우선 기법 커버리지, 알림 정밀도, Purple Team 검증 주기로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 우선순위화: 자사 위협 모델 기준으로 Initial Access, Credential Access, Lateral Movement technique 50개를 선정하고 owner를 지정함.
2. 탐지 구현: event 4688, Sysmon, PowerShell 4104, DNS, proxy, EDR telemetry를 SIEM에 수집하고 Sigma 룰로 technique ID를 태깅함.
3. 검증·개선: 분기 1회 Atomic Red Team 또는 Caldera 기반 에뮬레이션으로 hit rate, false positive rate, MTTD를 측정함.

**결론 (2줄):**
- 기술사 판단: ATT&CK은 보안 장비 목록보다 SOC 탐지 커버리지와 공백 관리를 증명할 때 가치가 있음.
- 향후 방향: CTI, XDR, SOAR를 ATT&CK ID로 연결해 탐지 룰 생성, 헌팅 쿼리, 대응 playbook을 자동 연계해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MITRE ATT&CK을 설명하시오" | tactic, technique, procedure 매핑 흐름 | IoC 중심 탐지와 TTP 중심 탐지 차이 |
| 요구사항 명시형 | "SOC 적용 방안을 제시하시오", "탐지 체계를 설계하시오" | coverage matrix, 로그 소스, 룰 튜닝 | false positive, Purple Team, 지표 관리 |

> 요약: 설명형은 구조를, 운영형·설계형은 커버리지와 탐지 품질 지표를 중심으로 작성함.
