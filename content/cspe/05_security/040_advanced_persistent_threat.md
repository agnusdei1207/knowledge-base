---
title: "APT 고급 지속 위협 (Advanced Persistent Threat)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 40
---

# 📖 【암기용】 개념 완전 이해

> 목적: APT 고급 지속 위협을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 특정 조직을 장기간 표적으로 삼아 은닉, 내부 이동, 정보 탈취를 수행하는 지능형 공격
- **왜 필요한가**: APT는 단발성 악성코드 감염이 아니라 정찰, 침투, 거점 확보, 권한 상승, 데이터 유출을 수주에서 수개월 동안 반복한다.
- **핵심 직관**: 도둑이 문을 부수고 나가는 것이 아니라 건물 안에 몰래 사무실을 만들고 출입카드를 복제해 필요한 자료를 조금씩 가져가는 방식임.

## 깊이 이해
- **배경·문제의식**: 국가 지원 조직, 산업 스파이, 고도 범죄 조직은 특정 기업·기관의 기술, 군사, 개인정보를 목표로 삼는다. 방화벽 경계만으로는 내부 거점화와 자격증명 탈취를 막기 어렵다.
- **작동 원리**: 공격자는 공개 정보 수집, spear phishing, zero-day 또는 공급망 침투로 들어온 뒤 persistence, privilege escalation, lateral movement, C2, exfiltration을 수행한다.
- **비유**: 외부 침입보다 내부 직원처럼 행동하는 위조 신분자가 더 탐지하기 어렵다. 출입 기록, 이동 경로, 자료 반출량을 함께 봐야 한다.
- **구체 예시**: 공격자가 피싱 첨부파일로 초기 실행 후 PowerShell, scheduled task, Kerberoasting, SMB lateral movement, HTTPS C2, 야간 2GB 압축 파일 전송을 수행하면 단일 로그로는 탐지가 어렵다.
- **흔한 오해·주의점**: APT는 특정 악성코드 이름이 아니다. 공격 캠페인, 행위 전술, 장기 은닉, 목표 지향성을 포함한 침해 유형임.

## 연결 개념
- Cyber Kill Chain - 정찰부터 목적 달성까지 공격 생명주기
- MITRE ATT&CK - 공격 전술·기법·절차를 매핑하는 지식체계
- EDR/SIEM/CTI - 행위 탐지, 로그 상관분석, 위협 인텔리전스 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: APT 답안은 장기 은닉, kill chain, ATT&CK, EDR/SIEM/CTI, 침해 지표, 복구·재발 방지를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: APT는 특정 표적을 대상으로 장기간 은닉하며 정찰, 침투, 내부 이동, 정보 탈취를 수행하는 목표 지향 공격임.
> 2. **가치**: 대응은 단일 악성코드 제거가 아니라 kill chain 단계별 탐지, 가정 침해, 위협 사냥, 계정·네트워크 통제임.
> 3. **판단 포인트**: MITRE ATT&CK 매핑, EDR/SIEM 상관분석, CTI, C2 차단, 계정 reset, 데이터 유출 확인을 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| APT 특성 이해 확인 | 고도성, 지속성, 표적성, 장기 은닉 | 일반 악성코드·DDoS와 동일시 |
| 공격 생명주기 판단 확인 | Kill Chain, ATT&CK 전술, C2, lateral movement | 정찰·내부 이동·유출 단계 누락 |
| 보안 운영 역량 확인 | EDR, SIEM, CTI, threat hunting, IR | 보안 장비 목록만 나열 |

> 요약: APT 문제는 장기 은닉 공격의 단계별 탐지와 조직적 대응 체계를 요구함.

---

## Ⅰ. 개요 및 필요성

APT는 장기 표적형 침해이다. 특정 조직의 핵심 자산을 목표로 정찰, 침투, 거점 확보, 권한 상승, 내부 이동, 정보 유출을 지속 수행함. 경계 방어만으로는 탐지가 늦어지므로 EDR, SIEM, CTI, Zero Trust 기반 상시 감시가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
공격자 -> 정찰 -> 초기 침투 -> 거점 확보 -> 권한 상승
-> 내부 이동 -> C2 통신 -> 데이터 수집/유출
방어: EDR -> SIEM -> CTI -> Threat Hunting -> IR/복구
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 정찰·초기 침투 | OSINT, spear phishing, 취약점 exploit | 사용자·협력사 표적화 |
| 지속성·권한 상승 | service, scheduled task, credential dump | 장기 은닉, 관리자 권한 획득 |
| 내부 이동·C2 | SMB/RDP/PowerShell 이동, HTTPS/DNS C2 | 정상 트래픽 위장 |
| 탐지·대응 | EDR, SIEM, CTI, threat hunting | ATT&CK 기법 매핑 |

> 요약: APT는 공격 생명주기와 방어 운영 체계를 함께 보아야 탐지 공백을 줄일 수 있음.

---

## Ⅲ. 동작원리 및 흐름도

```text
OSINT 정찰 -> spear phishing/zero-day 침투 -> persistence 등록
-> privilege escalation -> lateral movement -> C2 beacon
-> data staging/exfiltration -> 탐지·격리·계정 reset -> 재발 방지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 표적 정찰과 초기 침투 | mail log, proxy, EDR initial access |
| 2 | 지속성·권한 상승 | event 4672, service 생성, LSASS access |
| 3 | 내부 이동과 자격증명 사용 | event 4624 type 3/10, SMB/RDP, Kerberoasting |
| 4 | C2·데이터 유출 | DNS beacon, HTTPS rare domain, outbound volume |
| 5 | 격리·복구·헌팅 | host isolation, account reset, ATT&CK coverage |

> 요약: APT 탐지는 단일 악성 파일보다 로그인, 프로세스, 네트워크, 데이터 전송 로그의 시간 순서 상관분석이 핵심임.

---

## Ⅳ. 특징

| 구분 | 일반 침해 대응 | APT 대응 체계 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| 목표 | 불특정 감염 | 특정 자산·조직 표적 | crown jewel 자산 목록 |
| 기간 | 단기 이벤트 | 수주~수개월 은닉 | dwell time, beacon 주기 |
| 탐지 | 시그니처·경계 로그 | EDR 행위, SIEM 상관, CTI | ATT&CK coverage 80% 이상 |
| 복구 | 감염 제거 | 계정 reset, 세그먼트 점검, 유출 조사 | 권한 계정 100% 재검증 |

> 요약: APT는 표적성·지속성·은닉성이 핵심이며 행위 기반 탐지와 장기 로그 분석이 필요함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 탐지 | 경계 IDS 중심 | EDR + SIEM + UEBA + CTI | 내부 이동과 계정 오남용 탐지 필요 시 |
| 분석 | IoC 차단 | ATT&CK 기반 TTP 분석 | 해시 변경 변종·fileless 공격 |
| 대응 | 감염 단말 치료 | kill chain 단계별 차단·복구 | 침해 범위가 AD·서버까지 확장된 경우 |

> 요약: APT는 IoC보다 TTP 중심으로 분석해야 변종과 장기 은닉 행위를 추적할 수 있음.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 장기 은닉 | 정상 계정·정상 도구 악용 | UEBA, EDR, PowerShell logging | dwell time 7일 이하 목표 |
| 내부 확산 | AD 권한 탈취 | PAM, MFA, tiered admin, 계정 reset | privileged account review 100% |
| 유출 지속 | 저속 C2·압축 전송 | DLP, proxy, DNS sinkhole, egress control | outbound anomaly, rare domain |
| 재침투 | 웹셸·백도어 잔존 | IOC sweep, webroot hash, credential reset | 동일 TTP 재탐지 0건 |

> 요약: APT 리스크는 은닉, 권한 탈취, 저속 유출, 재침투이며 계정과 로그 중심 통제가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 범위 | ATT&CK coverage 80% 이상 | SIEM rule, EDR detection mapping |
| 대응 시간 | MTTD 24시간, MTTR 72시간 목표 | incident ticket, timeline 분석 |
| 복구·재발 | 권한 계정 reset 100%, 재침투 0건 | AD audit, EDR sweep, CTI 매칭 |

> 요약: APT 운영 성숙도는 ATT&CK 탐지 범위, MTTD/MTTR, 권한 계정 재검증으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 탐지 체계: EDR, SIEM, UEBA, CTI를 연계해 PowerShell, LSASS access, rare domain, lateral movement를 ATT&CK 기법으로 매핑함.
2. 대응 절차: 감염 호스트 격리, C2 도메인 sinkhole, 권한 계정 reset, AD tier 점검, 데이터 유출 범위 산정을 순서대로 수행함.
3. 재발 방지: Zero Trust, PAM, MFA, network segmentation, 로그 보존 1년, 분기 1회 threat hunting으로 장기 은닉을 줄임.

**결론 (2줄):**
- 기술사 판단: APT 대응은 경계 차단보다 내부 가시성, 계정 통제, ATT&CK 기반 threat hunting을 우선해야 함.
- 향후 방향: AI 기반 보안 분석, CTI 자동 매칭, XDR 통합으로 MTTD를 24시간 이하로 관리하는 SOC 운영이 요구됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "APT를 설명하시오" | kill chain과 ATT&CK 단계별 공격 흐름 | 일반 악성코드와 장기 표적 공격 차이 |
| 요구사항 명시형 | "탐지·대응 방안을 제시하시오" | EDR/SIEM/CTI 상관분석, threat hunting | MTTD, MTTR, 계정 reset, 재발 방지 |

> 요약: 설명형은 APT 생명주기를, 방안형은 SOC 탐지·대응 지표를 중심으로 작성함.
