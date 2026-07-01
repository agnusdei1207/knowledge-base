---
title: "능동적 방어 전략 (Active Cyber Defense)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 197
---

# 📖 【암기용】 개념 완전 이해

> 목적: 능동적 방어 전략을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 위협과 취약점을 실시간으로 발견, 탐지, 분석, 완화하는 동기화된 방어 역량
- **왜 필요한가**: 방화벽과 백신만 기다리는 수동 방어는 침해 후 발견 시간이 길어진다. 능동적 방어는 threat hunting, deception, adversary engagement로 공격자의 정찰·이동·탈취를 조기에 드러냄.
- **핵심 직관**: 건물에 CCTV만 두는 것이 아니라 가짜 금고, 미끼 문서, 순찰, 비상 대응팀을 배치해 침입자의 행동을 관찰하고 시간을 빼앗는 방식임.

## 깊이 이해
- **배경·문제의식**: APT는 정상 계정, living-off-the-land, 저속 이동으로 탐지를 회피한다. NIST 용어의 active cyber defense는 discover, detect, analyze, mitigate를 실시간으로 묶어 수동 감시 지연을 줄임.
- **작동 원리**: 공격면을 파악하고 고가치 자산 주변에 canary token, honey account, deception host를 둔다. EDR, NDR, SIEM 로그로 의심 행위를 hunting하고, MITRE Engage 관점으로 denial, deception, adversary engagement를 계획함.
- **비유**: 낚싯줄에 방울을 달아 물고기 움직임을 감지하듯, 실제 업무와 무관한 미끼 계정 사용을 즉시 침해 신호로 판단함.
- **구체 예시**: 도메인 관리자처럼 보이는 honey account가 Kerberoasting 시도에 등장하면 1분 내 high severity 경보를 만들고, 해당 호스트 EDR 격리와 계정 reset을 실행함.
- **흔한 오해·주의점**: 능동적 방어는 hack back이 아님. 조직 내부와 허가된 범위에서 deception, hunting, containment를 수행하며 외부 시스템 침투나 보복 공격은 법적 위험을 만든다.

## 연결 개념
- MITRE Engage - deception과 adversary engagement 계획 프레임워크
- Threat Hunting - 가설 기반으로 숨어 있는 공격 활동을 탐색
- Deception Technology - canary token, honey credential, decoy host로 침해 신호 생성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 능동적 방어는 선제 대응을 말하되 법적 경계, deception 설계, hunting 지표, ATT&CK 매핑을 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Active Cyber Defense는 위협을 실시간으로 발견, 탐지, 분석, 완화하는 동기화된 방어 전략임.
> 2. **가치**: deception과 hunting으로 공격자의 dwell time을 줄이고 MTTD 30분, containment 1시간 목표를 관리함.
> 3. **판단 포인트**: hack back 제외, 내부 허가 범위, 법무 검토, ATT&CK coverage, 오탐 처리 기준을 명시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 수동 방어와 차이 확인 | hunting, deception, denial, engagement, containment | 공격자 보복·외부 침투로 오해 |
| 설계 역량 확인 | crown jewel 주변 미끼 계정, decoy, canary, 로그 연계 | 제품명 나열 후 운영 절차 누락 |
| 법·윤리 경계 확인 | 내부 권한 범위, 승인, 개인정보, 증거 보존 | hack back을 대응 방안으로 제시 |

> 요약: 이 문제는 선제 탐지와 교란을 내부 통제 범위에서 설계하는 판단력을 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: 침투 진행을 선제 관측하는 방어
- 배경: 경보 발생 후 처리 방식은 정상 계정 악용, lateral movement, 내부 정찰 단계의 행위 증거를 놓칠 수 있다.
- 필요성: MITRE ATT&CK 기반 threat hunting, deception, 자동 containment로 TTP 관측과 대응 시간을 측정한다.

---

## Ⅱ. 구조 및 구성요소

```text
Crown Jewel -> Attack Surface Mapping -> Deception Asset
  / Hunting Hypothesis -> SIEM/EDR/NDR Detection
  / Response Playbook -> Containment -> Legal/Audit Review
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Attack Surface Map | 외부 노출, 계정, 중요 자산 식별 | EASM, CMDB, IAM 데이터 |
| Deception Asset | decoy host, honey account, canary token 배치 | 정상 업무 사용 0건 기준 |
| Hunting Analytics | ATT&CK TTP 가설 기반 탐색 | T1003, T1021, T1558 등 |
| Response Control | EDR 격리, 계정 잠금, 네트워크 차단 | 승인과 rollback 조건 필요 |
| Legal/Audit Guardrail | 허가 범위, 개인정보, 증거 보존 통제 | 외부 침투·보복 행위 제외 |

> 요약: 능동적 방어는 공격면 파악, 미끼 자산, hunting, containment, 법적 통제를 한 구조로 묶음.

---

## Ⅲ. 동작원리 및 흐름도

```text
공격면 분석 -> 미끼 계정/문서/호스트 배치 -> 행위 로그 수집
-> ATT&CK 기반 hunting -> 침해 의심 점수화
-> 격리/차단/증거 보존 -> 교훈 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 중요 자산과 lateral movement 경로 식별 | crown jewel 100% 매핑 |
| 2 | honey credential, decoy share, canary file 배치 | 정상 접근 0건, 경보 test 월 1회 |
| 3 | SIEM, EDR, NDR로 TTP 기반 hunting | ATT&CK coverage 80% 이상 |
| 4 | high fidelity 경보 발생 시 containment | MTTD 30분 이하, 격리 1시간 이하 |
| 5 | 증거 보존과 법무·개인정보 검토 | chain of custody 기록 100% |

> 요약: 능동적 방어는 미끼와 가설 기반 탐지로 공격자의 행동을 드러내고 허가된 대응으로 피해 범위를 줄임.

---

## Ⅳ. 특징

| 구분 | 수동 방어 | 능동적 방어 | 수치·통제 포인트 |
|:---|:---|:---|:---|
| 탐지 관점 | 경보 대기 | hunting, deception, canary 기반 탐지 | MTTD 30분 이하 |
| 공격자 대응 | 침해 후 차단 | 정찰·이동 단계에서 관측과 지연 | dwell time 24시간 이하 |
| 데이터 | 로그 수집 중심 | 미끼 상호작용, TTP, 행위 분석 | false positive 5% 이하 |
| 경계 | 내부 보안 장비 | 내부 허가 범위의 engagement | hack back 0건 |

> 요약: 능동적 방어는 공격자를 외부에서 공격하는 것이 아니라 내부 허가 범위에서 조기 탐지와 교란을 수행함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 탐지 방법 | IoC·시그니처 | TTP hunting, deception signal | IoC 변종 회피가 많은 환경 |
| 적용 위치 | 경계 방어 | crown jewel 주변, AD, cloud IAM | 중요 자산 침해 영향이 큰 경우 |
| 운영 조건 | SOC alert 처리 | hunter, legal, IR, asset owner 협업 | 주 1회 hunting cycle 가능 시 |

> 요약: 능동적 방어는 고가치 자산과 정상 행위 기준이 명확하고 법적 통제 체계가 있을 때 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 법적 위험 | 외부 시스템 접속·보복 행위 | 내부 허가 범위 명시, 법무 승인 | hack back 시도 0건 |
| 오탐 증가 | 미끼 자산 정상 사용 혼재 | naming 통제, 접근권한 분리 | deception false positive 5% 이하 |
| 운영 노출 | 공격자가 decoy 식별 | realistic artifact, 주기적 rotation | decoy fingerprint 개선 월 1회 |
| 개인정보 침해 | 사용자 행위 과수집 | 최소수집, 보존기간 90일, 접근통제 | privacy exception 0건 |

> 요약: 능동적 방어 리스크는 법적 경계, 오탐, decoy 노출, 개인정보이며 승인과 데이터 최소화로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 시간 | MTTD 30분 이하, dwell time 24시간 이하 | SIEM case timeline |
| 탐지 범위 | ATT&CK coverage 80%, crown jewel 100% | coverage matrix |
| 대응 품질 | containment 1시간 이하, 증거 기록 100% | IR ticket, forensic log |

> 요약: 능동적 방어 성과는 탐지 시간, ATT&CK coverage, containment와 증거 품질로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 범위 설정: AD, VPN, cloud IAM, 핵심 DB를 대상으로 내부 허가 범위와 금지 행위를 문서화하고 법무·개인정보 검토를 완료함.
2. 미끼 설계: honey account 10개, canary file 50개, decoy host 3대를 crown jewel 주변에 배치하고 정상 접근 0건 기준을 둠.
3. 운영 측정: ATT&CK T1003/T1021/T1558 hunting을 주 1회 수행하고 MTTD 30분, containment 1시간, false positive 5% 이하를 점검함.

**결론 (2줄):**
- 기술사 판단: 능동적 방어는 hack back이 아니라 deception과 hunting을 내부 통제 범위에서 수행하는 방어 전략임.
- 향후 방향: MITRE Engage, SOAR, XDR을 결합해 공격자 행동 관측부터 containment까지 증거 기반 자동 절차로 전환해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "능동적 방어를 설명하시오", "Active Defense를 기술하시오" | 공격면, deception, hunting, containment 흐름 | 수동 방어와 능동적 방어 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "법적 리스크를 설명하시오" | 범위 승인, 미끼 배치, 증거 보존 절차 | hack back 제외, 개인정보, 오탐 통제 |

> 요약: 설명형은 원리와 구성, 방안형은 법적 경계와 운영 지표 중심으로 목차를 전환함.
