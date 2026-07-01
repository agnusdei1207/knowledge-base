---
title: "사이버 킬체인 (Cyber Kill Chain)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 41
---

# 📖 【암기용】 개념 완전 이해

> 목적: 사이버 킬체인을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 공격자가 목표를 정찰하고 침투해 목적을 달성하기까지의 공격 생명주기 모델
- **왜 필요한가**: 침해는 한 번의 이벤트가 아니라 정찰, 무기화, 전달, 실행, 설치, C2, 목적 달성의 연속 행위다. 각 단계의 로그와 차단점을 알면 공격이 끝나기 전 중단시킬 수 있다.
- **핵심 직관**: 공격을 열차 노선처럼 보고, 역마다 검문소를 세워 다음 단계로 넘어가지 못하게 막는 사고방식임.

## 깊이 이해
- **배경·문제의식**: 전통 보안은 악성코드 탐지처럼 단일 시점에 집중했다. APT는 피싱 성공 후 권한 상승, 내부 이동, 데이터 유출을 며칠 이상 이어가므로 단계별 관측 지점이 필요하다.
- **작동 원리**: Cyber Kill Chain은 Reconnaissance, Weaponization, Delivery, Exploitation, Installation, C2, Actions on Objectives로 공격 흐름을 나눈다. SOC는 각 단계에 로그 소스와 차단 통제를 배치한다.
- **비유**: 택배 사기범을 잡을 때 발송 준비, 배송 경로, 수령, 내부 반출을 따로 추적하는 것과 같다. 마지막 반출만 보면 이전 흔적을 놓친다.
- **구체 예시**: spear phishing 메일 수신, 악성 매크로 실행, scheduled task 등록, HTTPS C2 60초 beacon, 야간 3GB 압축 전송이 연결되면 kill chain 전 단계가 성립한다.
- **흔한 오해·주의점**: Kill Chain은 공격자 이름이나 도구 목록이 아니다. 단계별 차단점과 탐지 커버리지를 설계하는 방어 모델임.

## 연결 개념
- APT - 장기 표적 공격을 kill chain 단계로 해석
- MITRE ATT&CK - kill chain 단계를 tactic, technique, procedure로 세분화
- SIEM/EDR/NDR - 단계별 로그 수집과 상관분석 수행

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Kill Chain 답안은 7단계 암기보다 단계별 차단점, 로그 소스, 탐지 커버리지, ATT&CK 연계를 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cyber Kill Chain은 공격 생명주기를 7단계로 분해해 각 단계에서 탐지와 차단을 설계하는 보안 운영 모델임.
> 2. **가치**: 초기 정찰·전달 단계에서 차단하면 C2, 내부 이동, 데이터 유출까지 이어지는 침해 범위를 줄일 수 있음.
> 3. **판단 포인트**: 단계명 나열이 아니라 로그 소스, 차단 통제, IoC/TTP 구분, MTTD/MTTR 지표를 연결해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공격 생명주기 이해 확인 | 7단계와 단계별 차단점 | 단계명만 나열하고 로그·통제 누락 |
| 보안 운영 설계 역량 확인 | EDR, SIEM, NDR, mail gateway, proxy 로그 연결 | 방화벽 차단만 제시 |
| APT 대응 관점 확인 | IoC 차단과 TTP 탐지, ATT&CK 매핑 | kill chain과 ATT&CK을 같은 모델로 혼동 |

> 요약: 이 문제는 공격 단계를 쪼개 각 단계에서 무엇을 보고 어디서 끊을지 쓰는 문제임.

---

## Ⅰ. 개요 및 필요성

Cyber Kill Chain은 공격 생명주기다. APT는 정찰부터 데이터 유출까지 여러 단계를 거치므로 마지막 악성코드 제거만으로 재침투를 막기 어렵다. 단계별 로그 소스와 차단 통제를 배치해 침해 진행을 중간에 중단해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Recon -> Weaponize -> Deliver -> Exploit -> Install -> C2 -> Objective
  / Mail, Proxy, DNS, EDR, NDR, DLP 로그
  / 차단: 필터링, 패치, 격리, sinkhole, 계정 reset
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Recon/Weaponize | 표적 정보 수집, 악성 문서·도구 준비 | OSINT, leaked credential, exploit kit |
| Deliver/Exploit | 피싱, 웹, 공급망으로 전달 후 취약점 실행 | mail log, WAF, EDR process tree |
| Install/C2 | 지속성 확보와 명령 채널 유지 | service, scheduled task, DNS/HTTPS beacon |
| Objective | 정보 탈취, 파괴, 랜섬웨어 실행 | DLP, DB audit, file server access |

> 요약: Kill Chain은 공격 흐름을 7단계로 나누고, 각 단계에 관측 로그와 차단 지점을 배치하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
위협 정보 수집 -> 단계별 이벤트 수집 -> kill chain 단계 매핑
-> 상관분석 룰 실행 -> 차단/격리/복구 -> 커버리지 갭 보완
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 정찰·전달 이벤트 식별 | phishing report, proxy deny, exposed asset |
| 2 | 실행·설치 행위 확인 | EDR alert, process tree, event 4688 |
| 3 | C2·목적 달성 징후 분석 | DNS beacon, rare domain, outbound GB/day |
| 4 | 차단·복구와 재탐지 수행 | host isolation, IOC sweep, rule hit count |

> 요약: Kill Chain 운영은 이벤트를 단계에 매핑하고, 상관분석 후 차단 결과를 커버리지로 되먹임하는 흐름임.

---

## Ⅳ. 특징

| 구분 | 이벤트 중심 대응 | Kill Chain 기반 대응 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| 분석 단위 | 단일 알림 | 7단계 공격 흐름 | 단계별 rule coverage |
| 차단 시점 | 감염 후 조치 | Delivery, Exploit, C2 단계 조기 차단 | MTTD 24시간 이하 |
| 탐지 기준 | 해시·IP IoC | IoC + TTP + 행위 시퀀스 | EDR, DNS, proxy 상관 |
| 한계 | 단계 맥락 부족 | 내부 이동 세부 기법은 ATT&CK 보완 필요 | coverage gap count |

> 요약: Kill Chain은 공격 진행 순서를 보여주고, ATT&CK은 각 단계의 세부 TTP를 보완함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 범위 | IoC 블랙리스트 | 단계별 생명주기 차단 | APT 캠페인 추적 필요 시 |
| 세분성 | ATT&CK technique 상세 | 7단계 거시 흐름 | 임원 보고·IR 타임라인 작성 |
| 운영 | 장비별 알림 처리 | SOC playbook 단계 매핑 | SIEM 상관분석 룰 30개 이상 운영 |

> 요약: Kill Chain은 침해 흐름 설명과 차단점 설계에 적합하고, 상세 탐지는 ATT&CK 매트릭스로 보완함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단계 누락 | 일부 로그 미수집 | mail, proxy, DNS, EDR, firewall 로그 1년 보존 | log source coverage 95% |
| 오탐 과다 | 단일 IoC 기반 룰 | 2개 이상 로그 소스 상관 조건 적용 | false positive rate 10% 이하 |
| 후행 대응 | C2 이후 탐지 | Delivery/Exploit 단계 룰 우선 배치 | pre-compromise detection ratio |

> 요약: 운영 리스크는 로그 공백, 오탐, 후행 탐지이며 로그 커버리지와 단계별 룰로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 커버리지 | 7단계 중 6단계 이상 룰 보유 | SIEM rule mapping |
| 대응 시간 | MTTD 24시간, MTTR 72시간 | incident timeline |
| 차단 성과 | C2 이전 차단 비율 60% 이상 | IR case review |

> 요약: Kill Chain 성숙도는 단계별 룰 보유, 탐지 시간, C2 이전 차단 비율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 로그 설계: mail gateway, proxy, DNS, EDR, NDR, DLP 로그를 1년 보존하고 kill chain 7단계 필드로 SIEM 태깅함.
2. 차단 설계: Delivery는 SPF/DKIM/DMARC, Exploit은 CVSS 9.0 이상 7일 내 패치, C2는 DNS sinkhole과 egress filtering 적용함.
3. SOC 운영: 분기 1회 kill chain tabletop, 월 1회 rule coverage 점검, IR 종료 후 단계별 탐지 공백을 백로그로 등록함.

**결론 (2줄):**
- 기술사 판단: Kill Chain은 APT 흐름 설명에 우선 적용하고, 세부 탐지는 ATT&CK TTP와 SIEM 룰로 확장해야 함.
- 향후 방향: XDR 기반 로그 통합과 CTI 자동 매핑으로 C2 이전 차단 비율을 SOC 핵심 지표로 관리해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Cyber Kill Chain을 설명하시오" | 7단계 흐름과 단계별 로그 소스 | ATT&CK과의 역할 차이, 적용 사례 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "탐지 체계를 설계하시오" | 단계별 차단점, SIEM/EDR/NDR 상관분석 | MTTD, C2 이전 차단율, 커버리지 지표 |

> 요약: 설명형은 생명주기, 방안형·설계형은 단계별 차단점과 운영 지표를 중심으로 전개함.
