---
title: "LLM06 Excessive Agency (LLM06 Excessive Agency)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 202
extra:
  question_no: "202"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM06은 모델이 틀릴 수 있다는 사실보다 모델에 너무 큰 권한과 자율성을 준 구조가 더 큰 위험이라는 점을 다룸
- 도구 수와 API 권한과 자동 실행 범위가 넓을수록 프롬프트 인젝션이나 환각의 피해 반경이 커짐
- 최소 권한과 승인 절차와 작업 범위 제한이 핵심 통제 장치임

## Ⅰ. 개요

- **정의/개념**: LLM06 Excessive Agency는 LLM 기반 에이전트가 목적 달성에 필요한 수준을 넘어 과도한 기능과 권한과 자율적 실행 범위를 부여받아 오작동이나 공격 시 대규모 피해를 일으키는 취약점임
- **배경/필요성**: LLM이 메일 발송과 결제 요청과 운영 자동화를 직접 수행하는 구조가 확대되면서 모델 정확도보다 권한 경계 설계가 더 중요한 보안 과제로 부상함

## Ⅱ. 특징

- 동일한 프롬프트 인젝션도 읽기 전용 에이전트보다 쓰기 권한 에이전트에서 훨씬 치명적임
- 도구 호출 수가 많아질수록 공격 표면과 우발적 오작동 범위가 함께 증가함
- 자율 루프가 길수록 인간이 개입할 시점이 줄어들어 탐지와 차단이 늦어짐
- RBAC와 approval gate와 tool scoping이 성숙도 판단의 핵심 지표가 됨

## Ⅲ. 종류 및 비교

| 판단 기준 | LLM06 Excessive Agency | LLM05 Improper Output Handling | 전통적 RPA 자동화 |
|:---|:---|:---|:---|
| 핵심 위험 | 권한 과다와 자율 실행 | 출력 검증 부재 | 규칙 설정 오류 |
| 실패 원인 | tool scope, API privilege, autonomy | sanitize, schema 부족 | 하드코딩된 절차 오설계 |
| 피해 형태 | 송금, 삭제, 발송, 변경 | XSS, RCE, SQLi | 제한적 업무 오류 |
| 우선 대응 | PoLP, HITL, approval gate | parser, sandbox | rule validation |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Agent Planner | 자연어 목표를 작업 단계와 도구 호출 계획으로 바꾸며 잘못된 계획이 직접 실행으로 이어질 수 있는 중심 모듈임 |
| Tool Registry | 에이전트가 접근 가능한 메일과 DB와 결제와 외부 API 목록을 정의하며 공격 표면의 크기를 결정함 |
| Permission Scope | 각 도구에 읽기와 쓰기와 삭제 같은 세분 권한을 부여해 피해 반경을 제한하는 통제 계층임 |
| Approval Gate | 금전 이동과 삭제와 외부 발송 같은 고위험 작업에서 인간 승인이나 추가 검증을 요구하는 안전 장치임 |
| Audit Trail | 어떤 프롬프트와 어떤 도구와 어떤 권한으로 실행되었는지 남겨 사고 원인 추적을 가능하게 함 |

```text
+------------+    +--------------+    +----------------+    +-------------+
| User Goal  | -> | Agent Planner| -> | Tool/Permission| -> | Approval Gate|
+------------+    +--------------+    +----------------+    +-------------+
                                                              |
                                                              v
                                                       +-------------+
                                                       |  Execution  |
                                                       +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 목표 해석    | -> | 도구 선택    | -> | 권한 점검    | -> | 승인 판단    | -> | 실행 및 기록 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **목표 해석**: 에이전트가 사용자의 지시를 세부 작업으로 분해함
2. **도구 선택**: 필요한 API와 플러그인과 내부 시스템 접근 경로를 고름
3. **권한 점검**: 선택된 도구가 현재 범위에서 허용된 작업인지 확인함
4. **승인 판단**: 고위험 행위는 자동 실행 대신 사람 승인이나 다중 정책 검사를 거침
5. **실행 및 기록**: 통과한 작업만 수행하고 모든 근거를 로그에 남김

## Ⅵ. 문제점 및 해결 방안

1. 문제: 읽기만 필요한 에이전트에 쓰기와 삭제 권한까지 부여하면 단일 오판이 대규모 자산 손상으로 확대될 수 있음
   - 해결방안: least privilege와 task scoped credential을 적용하고 privileged action rate와 excessive permission count로 검증함
2. 문제: 승인 없는 자율 실행 루프가 결제나 발송이나 삭제를 자동 처리하면 환각이나 인젝션이 바로 사고로 이어질 수 있음
   - 해결방안: human in the loop와 risk tiered approval gate를 적용하고 manual approval coverage와 autonomous destructive action rate로 검증함
3. 문제: 불필요한 도구를 많이 연결하면 공격 표면이 커지고 보안 검증 누락 지점이 급격히 증가할 수 있음
   - 해결방안: minimal tool registry와 periodic permission review를 적용하고 enabled tool count와 unused privileged tool ratio로 검증함

## Ⅶ. 적용 사례

- 사내 메일 요약 에이전트가 발송 권한 없이 읽기 전용 API만 사용하며 확인 지표는 unauthorized send rate와 summary accuracy임
- 재무 자동화 비서가 송금 요청에 다단계 승인과 금액 한도를 적용하며 확인 지표는 auto transfer block rate와 approval turnaround time임
- 운영 에이전트가 인프라 변경 전 change request와 롤백 계획을 강제하며 확인 지표는 unreviewed change rate와 rollback success rate임

## Ⅷ. 결론

LLM06은 모델 성능 개선만으로 해결되지 않으며 권한 최소화와 승인 체계와 도구 범위 제어를 통해 에이전트의 행동 반경을 구조적으로 줄여야 함.
