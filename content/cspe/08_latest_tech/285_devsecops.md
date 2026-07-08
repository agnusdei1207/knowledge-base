---
title: "DevSecOps (DevSecOps)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 285
extra:
  question_no: "285"
  exam_status: "기출"
  exam_history: "128회, 134회, 135회, 136회"
---

## 미리 알고가기

- DevSecOps는 보안을 개발과 배포 파이프라인 초기에 통합하는 운영 접근임
- 보안팀을 추가하는 개념이 아니라 파이프라인 자체가 보안 검증을 내장하도록 만드는 것이 핵심임
- shift left와 policy as code와 지속 검증이 핵심 키워드임

## Ⅰ. 개요

- **정의/개념**: DevSecOps는 소프트웨어 개발과 배포와 운영 전 과정에 보안 검증과 정책 통제를 자동화해 보안을 별도 마지막 단계가 아니라 지속적 파이프라인 기능으로 내재화하는 접근임
- **배경/필요성**: 클라우드 네이티브와 빠른 배포 문화에서는 릴리스 직전 보안 점검만으로 취약점과 설정 오류를 통제하기 어려워 개발 초기에 보안을 통합해야 함

## Ⅱ. 특징

- 보안 검증을 CI CD 파이프라인에 자동 삽입함
- 코드와 이미지와 인프라와 런타임 전 구간을 대상으로 삼음
- 보안팀과 개발팀이 공통 정책과 도구를 공유함
- 지나친 차단 정책은 개발 속도 저하와 우회 사용을 유발할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | DevSecOps | DevOps | 전통적 보안 심사 |
|:---|:---|:---|:---|
| 보안 위치 | 개발 초기부터 전 과정 | 보안은 외부 연계 가능 | 배포 전후 별도 점검 |
| 자동화 수준 | 높음 | 중간 | 낮음 |
| 출시 속도 | 통제된 빠름 | 빠름 | 느림 |
| 핵심 가치 | 보안 내재화 | 배포 민첩성 | 심사 중심 통제 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Secure Coding and PR Gate | 코드 리뷰와 정적 분석과 비밀 탐지를 통해 개발 초기부터 취약점을 걸러내는 검증 계층임 |
| Pipeline Security Scan | 의존성 취약점과 컨테이너 이미지와 IaC 구성을 자동 검사하는 CI CD 보안 계층임 |
| Policy as Code | 권한과 네트워크와 배포 기준을 코드 규칙으로 정의해 일관되게 적용하는 통제 계층임 |
| Runtime Protection | 운영 중 이상 행위와 설정 드리프트를 감지해 배포 후 보안 리스크를 줄이는 런타임 계층임 |
| Feedback Loop | 취약점과 사고와 개발 속도 지표를 함께 보며 정책을 조정하는 개선 계층임 |

```text
+---------+    +----------------+    +----------------+    +----------------+
| Dev Code| -> | CI Security    | -> | Policy Gate    | -> | Runtime Guard  |
+---------+    +----------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 코드 작성    | -> | 자동 스캔    | -> | 정책 판정    | -> | 안전 배포    | -> | 운영 감시    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **코드 작성**: 개발자가 기능과 인프라 코드를 작성함
2. **자동 스캔**: SAST와 SCA와 secret scan을 수행함
3. **정책 판정**: 정책 위반과 위험도를 평가함
4. **안전 배포**: 기준을 통과한 변경만 배포함
5. **운영 감시**: 런타임 이상과 취약점 후속 조치를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 보안 도구가 많아도 기준과 우선순위가 없으면 경고 피로만 높아지고 실제 취약점 조치율은 낮아질 수 있음
   - 해결방안: risk based triage와 severity threshold tuning을 적용하고 false positive rate와 critical issue remediation lead time으로 검증함
2. 문제: 보안 검사가 파이프라인 속도를 과도하게 늦추면 개발팀이 우회 경로를 찾게 될 수 있음
   - 해결방안: fast fail scan layering과 developer friendly remediation guide를 적용하고 pipeline latency overhead와 policy bypass rate로 검증함
3. 문제: 코드 수준 검증만 강조하면 운영 설정 드리프트와 런타임 위협을 놓칠 수 있음
   - 해결방안: runtime security integration과 drift detection policy를 적용하고 runtime attack detection rate와 config drift incident count로 검증함

## Ⅶ. 적용 사례

- 보안 파이프라인이 위험도 기반 선별을 운영하며 확인 지표는 false positive rate와 critical issue remediation lead time임
- 개발 플랫폼이 빠른 실패 계층 검사를 적용하며 확인 지표는 pipeline latency overhead와 policy bypass rate임
- 클라우드 운영팀이 런타임 보안과 드리프트 탐지를 결합하며 확인 지표는 runtime attack detection rate와 config drift incident count임

## Ⅷ. 결론

DevSecOps는 보안을 추가 단계가 아니라 파이프라인 능력으로 만드는 접근이므로 자동화 품질과 개발자 수용성과 런타임 연계를 함께 설계해야 함.
