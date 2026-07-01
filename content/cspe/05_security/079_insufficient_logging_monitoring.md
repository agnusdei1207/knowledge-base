---
title: "로깅·모니터링 불충분 (Insufficient Logging Monitoring)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 79
---

# 📖 【암기용】 개념 완전 이해

> 목적: 로깅·모니터링 불충분을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 침해 징후를 기록·탐지·대응할 로그와 경보 체계가 부족한 상태
- **왜 필요한가**: 공격은 로그인 실패, 권한 변경, 데이터 대량 조회, 비정상 API 호출 같은 흔적을 남긴다. 로그가 없으면 MTTD와 MTTR을 측정할 수 없음.
- **핵심 직관**: 건물에 CCTV와 출입기록이 없으면 도난 사실, 침입 경로, 피해 범위를 모두 추정으로 처리하게 됨.

## 깊이 이해
- **배경·문제의식**: 많은 시스템은 에러 로그만 남기고 audit event를 남기지 않는다. 로그인 성공·실패, 관리자 권한 변경, API token 발급, 데이터 export, 보안정책 변경은 침해 조사에 필수임.
- **작동 원리**: 수집 대상 이벤트를 정의하고 중앙 SIEM으로 전송한다. timestamp 동기화, tamper-proof storage, correlation rule, alert triage, incident ticket으로 탐지와 대응을 연결함.
- **비유**: 병원 응급실에서 환자 기록, 검사 시간, 투약 이력이 빠지면 치료 결과를 설명할 수 없듯 보안도 사건 타임라인이 없으면 복구 판단이 흔들림.
- **구체 예시**: 관리자 계정에서 10분 내 5회 MFA 실패 후 해외 IP 로그인, 1GB customer export가 발생하면 SIEM correlation rule로 high alert를 만들고 15분 내 조사 티켓을 생성함.
- **흔한 오해·주의점**: 로그를 많이 저장하는 것만으로 충분하지 않다. 어떤 이벤트를 audit event로 볼지, 보존기간, 무결성, 경보 임계값, 담당자 조치 SLA가 있어야 함.

## 연결 개념
- SIEM - 로그 수집, 상관분석, 경보 생성
- SOAR - 경보 triage와 대응 playbook 자동화
- MTTD/MTTR - 탐지와 복구 시간을 측정하는 운영 지표

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 로깅 부족 답안은 로그 저장 나열이 아니라 audit event 정의, SIEM 탐지, 위변조 방지, MTTD/MTTR 개선 흐름을 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Insufficient Logging Monitoring은 침해 탐지와 사후조사에 필요한 audit event, 중앙 수집, 경보, 대응 지표가 빠진 상태임.
> 2. **가치**: SIEM, EDR, tamper-proof logs, correlation rule로 MTTD와 MTTR을 측정 가능한 값으로 낮춤.
> 3. **판단 포인트**: 무엇을 기록할지, 어디서 탐지할지, 누가 몇 분 내 대응할지, 로그 무결성을 어떻게 검증할지 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 로그 설계 역량 확인 | 인증, 권한, 관리자 행위, 데이터 export, 정책 변경 audit event | 웹서버 access log만 기재 |
| 탐지·대응 연계 확인 | SIEM correlation, alert triage, incident ticket, SOAR | 로그 수집과 모니터링을 분리해 작성 |
| 운영 지표 판단 확인 | MTTD, MTTR, 보존기간, tamper-proof, clock sync | 보존·무결성·시간동기화 누락 |

> 요약: 이 문제는 로그 양이 아니라 침해 타임라인을 재구성하고 경보에서 대응까지 이어지는 운영 체계를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 탐지·추적 공백 취약점
- 배경: 인증, 권한, 데이터 접근, 관리자 행위가 audit event로 남지 않으면 침해 범위 산정과 책임 추적이 어려움.
- 필요성: OWASP ASVS, MITRE ATT&CK, SIEM 상관분석, 로그 무결성 보관, 탐지 후 대응 SLA 24시간 이내 기준을 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Audit Event 정의 -> 애플리케이션/인프라 로그 -> 중앙 수집 -> SIEM 분석 -> 경보/티켓 -> 대응/재검증
  / auth, admin, data export, config change
  / WORM, hash chain, NTP, retention
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Audit Event | 침해 판단에 필요한 이벤트 정의 | login, MFA fail, privilege change, export |
| Log Pipeline | 수집, 정규화, timestamp 동기화 | syslog, Fluent Bit, OpenTelemetry |
| SIEM/Detection | 상관분석, 임계값, 위협 탐지 | Sigma, YARA-L, UEBA |
| Evidence Store | 위변조 방지와 보존 | WORM, object lock, hash, 180일 이상 |

> 요약: 로깅 체계는 audit event, 수집 파이프라인, SIEM 탐지, 증적 저장소로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
보안 이벤트 발생 -> 로그 생성/마스킹 -> 중앙 전송 -> 정규화/상관분석
  / 실패 로그인, 권한 변경, 대량 조회
경보 생성 -> triage -> incident ticket -> 조치 -> postmortem
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션과 인프라에서 audit event 생성 | 필수 이벤트 누락 0건 |
| 2 | 중앙 로그 저장소로 암호화 전송과 시간 동기화 | NTP drift 1초 이하 |
| 3 | SIEM correlation rule과 UEBA로 경보 생성 | high alert MTTD 15분 |
| 4 | 티켓, SOAR playbook, 사후분석으로 조치 | MTTR 4시간, RCA 5영업일 |

> 요약: 이벤트 생성부터 SIEM 경보와 티켓 조치까지 이어져야 모니터링이 대응 체계로 작동함.

---

## Ⅳ. 특징

| 구분 | 단순 로그 저장 | 보안 모니터링 체계 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 이벤트 | 에러·access 중심 | 인증, 권한, 데이터, 관리자 행위 | 필수 audit event 100% |
| 분석 | 사후 검색 | correlation, UEBA, threat rule | high MTTD 15분 |
| 보관 | 로컬 파일 | 중앙 WORM/object lock | 보존 180일 이상 |
| 대응 | 담당자 수동 확인 | ticket, SOAR, SLA | MTTR 4시간 |

> 요약: 로깅·모니터링은 저장소가 아니라 이벤트 정의, 탐지 규칙, 무결성 보관, 대응 SLA의 조합임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 서버별 로컬 로그 | 중앙 SIEM, data lake, WORM | 시스템 10대 이상 또는 규제 데이터 보유 |
| 비용/성능 | 전체 debug log 저장 | audit event 중심 샘플링·보존등급 | 저장비용과 조사 필요성 균형 |
| 운영/위험 | 경보 후 수동 대응 | SOAR playbook, on-call, SLA | high alert 24x7 대응 필요 |

> 요약: 로그 저장 비용은 audit event 우선순위와 보존등급으로 통제하고 high alert는 SLA 기반 대응으로 연결함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 탐지 누락 | audit event 미정의 | 보안 이벤트 카탈로그, test event | 필수 이벤트 누락 0건 |
| 로그 위변조 | 로컬 저장, 관리자 삭제 가능 | WORM, object lock, hash chain | 무결성 검증 실패 0건 |
| 경보 피로 | 임계값 부정확, 중복 rule | tuning, severity matrix, suppression | false positive 20% 이하 |

> 요약: 탐지 누락, 위변조, 경보 피로는 이벤트 카탈로그와 WORM, rule tuning으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 시간 | high severity MTTD 15분 | SIEM alert timestamp |
| 복구 시간 | high severity MTTR 4시간 | incident ticket |
| 증적 품질 | 보존 180일, NTP drift 1초 이하 | WORM audit, NTP monitor |

> 요약: 성공 여부는 MTTD, MTTR, 증적 보존·시간동기화 품질로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 이벤트 설계: 로그인 성공·실패, MFA 실패, 권한 변경, 관리자 API, 데이터 export, 보안정책 변경을 audit event로 정의하고 PII는 redaction함.
2. 탐지 운영: Fluent Bit/OpenTelemetry로 중앙 수집, SIEM correlation rule, UEBA, SOAR ticket 생성을 연결하고 high alert MTTD 15분을 기준으로 둠.
3. 증적 보존: WORM/object lock, hash 검증, NTP 동기화, 180일 이상 보존을 적용하고 MTTR 4시간, RCA 5영업일을 운영 지표로 관리함.

**결론 (2줄):**
- 기술사 판단: 인증·권한·데이터 접근 이벤트가 없는 시스템은 침해 대응 불가 영역이므로 서비스 오픈 전 필수 audit event를 완료해야 함.
- 향후 방향: 로깅·모니터링은 SIEM 중심에서 EDR, XDR, UEBA, SOAR를 결합한 탐지-대응 자동화로 전환되어야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "로깅·모니터링 불충분을 설명하시오" | 이벤트 생성, 수집, SIEM 탐지, 대응 흐름 | 단순 저장과 보안 모니터링 차이 |
| 요구사항 명시형 | "개선 방안을 제시하시오", "운영 체계를 설계하시오" | audit event, MTTD/MTTR, tamper-proof logs | SIEM/SOAR, 보존기간, 경보 튜닝 |

> 요약: 설명형은 탐지 공백 구조를, 운영형은 감사 이벤트와 MTTD/MTTR 개선 지표를 중심으로 구성함.
