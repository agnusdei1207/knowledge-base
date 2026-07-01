---
title: "EDR 엔드포인트 탐지·대응 (EDR Endpoint Detection and Response)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 54
---

# 📖 【암기용】 개념 완전 이해

> 목적: EDR을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: PC, 서버, 워크로드에서 프로세스·파일·레지스트리·네트워크 행위를 수집해 공격을 탐지하고 격리·조사하는 체계
- **왜 필요한가**: 백신은 파일 서명 중심이라 무파일 공격, PowerShell 악용, 정상 도구를 쓰는 living-off-the-land 공격을 놓칠 수 있다.
- **핵심 직관**: 범인을 얼굴 사진만으로 찾는 대신, 어떤 명령을 실행했고 어떤 파일을 만들었으며 어느 서버로 접속했는지 시간순 동선을 추적한다.

## 깊이 이해
- **배경·문제의식**: 랜섬웨어와 APT는 정상 계정과 관리 도구를 악용한다. 실행 파일이 악성으로 분류되지 않아도 프로세스 트리, 명령행, 네트워크 연결을 보면 공격 흐름이 나타난다.
- **작동 원리**: 엔드포인트 에이전트가 process tree, command line, file hash, registry change, network connection을 수집한다. 탐지 후 host isolation, process kill, file quarantine, IOC sweep을 실행한다.
- **비유**: CCTV가 사무실 안 행동을 기록해 "문을 열었다"가 아니라 "어떤 PC에서 어떤 프로그램이 어떤 문서를 암호화했는가"를 추적하는 방식이다.
- **구체 예시**: `winword.exe`가 매크로로 `powershell.exe`를 실행하고 외부 IP 연결 후 500개 파일 확장자를 변경하면 ransomware behavior로 판단하고 60초 이내 네트워크 격리한다.
- **흔한 오해·주의점**: EDR은 백신의 이름만 바꾼 제품이 아니다. 사전 차단보다 사후 탐지, 타임라인 조사, IOC sweep, 원격 대응이 핵심이다.

## 연결 개념
- Antivirus/NGAV - 파일·행위 차단 계층, EDR의 선행 통제
- MITRE ATT&CK - 프로세스 행위를 공격 기술로 분류하는 기준
- XDR - EDR 이벤트를 네트워크·메일·클라우드 이벤트와 결합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: EDR 답안은 process tree, containment, IOC sweep을 중심으로 탐지와 대응 지표를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: EDR은 엔드포인트 행위 데이터를 지속 수집해 침해를 탐지하고 원격 격리·조사·복구를 수행하는 체계이다.
> 2. **가치**: 무파일 공격, 랜섬웨어, 정상 도구 악용처럼 파일 서명만으로 식별하기 어려운 공격을 프로세스 행위로 추적한다.
> 3. **판단 포인트**: 에이전트 coverage, process tree 정확도, containment 시간, IOC sweep 범위, MTTD·MTTR을 함께 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 엔드포인트 행위 탐지 이해 확인 | process tree, command line, file hash, registry, network connection | 백신과 동일 개념으로만 설명 |
| 랜섬웨어·APT 대응 절차 확인 | host isolation, process kill, quarantine, IOC sweep | 탐지 후 격리·확산 차단 누락 |
| 운영 지표 판단 확인 | agent coverage 95%, MTTD 10분, containment 5분 | 에이전트 부하·예외 관리 누락 |

> 요약: EDR 문제는 단말 행위 수집에서 원격 격리와 IOC 확산 조사까지 연결하는 대응 체계를 요구한다.

---

## Ⅰ. 개요 및 필요성

EDR은 단말 행위 탐지·대응이다. 랜섬웨어, 무파일 공격, 정상 관리 도구 악용 공격은 파일 서명 중심 통제만으로 식별 지연이 발생한다. EDR은 프로세스 트리와 행위 타임라인으로 침해 원인을 추적하고 확산을 차단한다.

---

## Ⅱ. 구조 및 구성요소

```text
Endpoint Agent -> Telemetry 수집 -> 행위 분석 -> Alert/Timeline -> Response Action
                              / process tree
                              / IOC sweep
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 에이전트 | 프로세스, 파일, 레지스트리, 네트워크 행위 수집 | CPU 3% 이하, coverage 95% 이상 |
| 분석 엔진 | rule, behavior, ML, MITRE ATT&CK 매핑 | T1059 PowerShell 등 기술 단위 분류 |
| 조사 콘솔 | process tree, timeline, file hash, IOC 검색 | 사건 재구성 시간 30분 이내 |
| 대응 모듈 | host isolation, process kill, quarantine, rollback | containment 5분 이내 목표 |

> 요약: EDR은 에이전트 telemetry, 행위 분석, 타임라인 조사, 원격 대응으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
행위 수집 -> 프로세스 트리 생성 -> 이상 행위 탐지 -> 호스트 격리 -> IOC sweep -> 복구 검증
                         / command line 분석
                         / hash reputation 조회
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프로세스, 명령행, 파일, 레지스트리, 네트워크 telemetry 수집 | agent coverage 95% 이상 |
| 2 | parent-child process tree와 MITRE ATT&CK 기술 매핑 | 주요 기술 T1059·T1027 탐지 |
| 3 | 랜섬웨어, credential dumping, C2 연결 탐지 | MTTD 10분 이내, 오탐률 5% 이하 |
| 4 | host isolation, process kill, IOC sweep, quarantine 실행 | containment 5분 이내 |

> 요약: EDR은 단말 행위를 시간순으로 연결해 공격 프로세스를 식별하고 원격 대응으로 확산을 차단한다.

---

## Ⅳ. 특징

| 구분 | 백신/NGAV | EDR | 판단 포인트 |
|:---|:---|:---|:---|
| 탐지 기준 | 파일 서명, 평판, 사전 차단 | 프로세스 행위, 타임라인, 위협 헌팅 | 무파일 공격 대응 |
| 데이터 범위 | 파일·실행 이벤트 중심 | command line, registry, network, memory 일부 | telemetry 보존 30~90일 |
| 대응 범위 | 삭제, 격리 중심 | host isolation, IOC sweep, 원격 조사 | containment 5분 이내 |
| 운영 지표 | 탐지 건수 | MTTD, MTTR, coverage, 오탐률 | agent coverage 95% 이상 |

> 요약: EDR은 백신의 파일 차단 한계를 단말 행위 타임라인과 원격 대응으로 보완한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | EDR | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | AV/NGAV 단독 | agent telemetry와 중앙 분석 | 서버·PC 관리 자산 500대 이상 |
| 비용/처리 | 낮은 저장량, 낮은 조사 정보 | telemetry 저장·분석 비용 발생 | 보존 30일 이상 필요 |
| 운영/위험 | 차단 후 상세 원인 추적 한계 | timeline 조사와 IOC sweep 가능 | 랜섬웨어 확산 리스크 높을 때 |

> 요약: EDR은 단말 수가 많고 랜섬웨어·APT 조사 요구가 큰 조직에서 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 에이전트 누락 | 미관리 단말, 서버 예외 | CMDB 대조, 배포율 95% 이상 SLA | agent coverage 95% 이상 |
| 업무 영향 | 격리 오탐, 프로세스 종료 오탐 | risk score 90 이상 자동 격리, 승인 기반 예외 | 오탐 격리 1% 이하 |
| 회피 공격 | EDR tampering, log 삭제 | tamper protection, 로컬 관리자 권한 제한 | agent disable event 0건 |

> 요약: EDR 운영 리스크는 에이전트 누락, 대응 오탐, 회피 공격이며 coverage와 tamper protection으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 | 랜섬웨어 MTTD 10분 이내 | 파일 암호화 시뮬레이션 |
| 대응 | containment 5분, MTTR 4시간 이내 | host isolation 실행 로그 |
| 커버리지 | PC·서버 agent coverage 95% 이상 | CMDB 대 EDR 콘솔 대조 |

> 요약: EDR 도입 효과는 탐지 건수가 아니라 격리 시간, IOC sweep 범위, 에이전트 coverage로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. PC·서버 CMDB와 EDR 콘솔을 대조해 agent coverage 95% 이상, 중요 서버 100% 배포 달성
2. ransomware, credential dumping, PowerShell abuse rule을 MITRE ATT&CK T1059·T1003 기준으로 우선 적용
3. host isolation 5분 이내, IOC sweep 30분 이내, 복구 후 hash·process 재발 여부 24시간 모니터링

**결론 (2줄):**
- 기술사 판단: 랜섬웨어와 무파일 공격 리스크가 높으면 EDR을 우선 적용하고, 관리되지 않는 자산이 많으면 NDR로 탐지 공백을 보완한다
- 향후 방향: EDR은 XDR로 확장되어 단말 행위를 네트워크, 메일, 클라우드 이벤트와 상관분석하는 구조로 발전한다

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "EDR을 설명하시오", "기술하시오" | telemetry 수집, process tree, 격리 흐름 | 백신·NGAV와 차이 |
| 요구사항 명시형 | "랜섬웨어 대응 방안을 제시하시오", "설계하시오" | containment, IOC sweep, 복구 검증 | MTTD·containment·coverage 기준 |

> 요약: 설명형은 엔드포인트 행위 분석, 방안형은 랜섬웨어 격리와 확산 조사 지표 중심으로 목차를 전환한다.
