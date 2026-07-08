---
title: "CSPM 클라우드 보안형상관리 (Cloud Security Posture Management)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 298
extra:
  question_no: "298"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- CSPM은 클라우드 계정과 자원의 설정 상태를 점검해 보안 오구성을 찾는 도구 영역임
- 런타임 위협 대응보다 posture와 compliance 가시화가 핵심 역할임
- CNAPP의 하위 기능으로 포함되는 경우가 많지만 독립 개념으로 구분 가능함

## Ⅰ. 개요

- **정의/개념**: CSPM은 클라우드 계정과 서비스와 리소스 구성 상태를 지속 점검해 잘못된 보안 설정과 규정 위반과 과도한 노출을 식별하는 보안 관리 체계임
- **배경/필요성**: 퍼블릭 클라우드 자원은 생성 속도가 빨라 작은 설정 오류 하나가 대규모 노출 사고로 이어지기 쉬워 지속적인 posture 점검 체계가 필요해짐

## Ⅱ. 특징

- 클라우드 설정 오류와 규정 위반 탐지에 강함
- 멀티클라우드 자산을 한 화면에서 볼 수 있음
- 자동 교정과 정책 검증으로 운영 표준화에 기여함
- 실제 런타임 공격 탐지와 워크로드 내부 위협 대응은 제한적임

## Ⅲ. 종류 및 비교

| 판단 기준 | CSPM | CWPP | CNAPP |
|:---|:---|:---|:---|
| 초점 | 설정 상태와 posture | 워크로드 런타임 보호 | 통합 플랫폼 |
| 대표 대상 | 계정, 스토리지, 네트워크, IAM | VM, 컨테이너, 서버리스 | posture, workload, identity |
| 강점 | misconfiguration 탐지 | 런타임 위협 탐지 | 상관 분석 |
| 한계 | 런타임 가시성 부족 | posture 범위 제한 | 운영 범위 큼 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Asset Discovery | 클라우드 계정과 리소스를 수집해 posture 분석 대상 자산을 최신 상태로 유지하는 탐색 계층임 |
| Policy Rule Set | 공개 버킷과 과도한 권한처럼 탐지해야 할 보안 기준을 정의하는 정책 집합임 |
| Compliance Mapping | 국내외 규제와 내부 기준을 posture 정책과 연결해 감사 대응성을 높이는 매핑 계층임 |
| Remediation Workflow | 경고를 티켓과 자동 수정과 승인 절차로 연결해 실제 조치를 유도하는 대응 계층임 |
| Risk Dashboard | 자산 노출도와 규정 위반 상태를 시각화해 우선순위를 정하게 하는 가시화 계층임 |

```text
+-------------+    +----------------+    +----------------+    +----------------+
| Asset Disc. | -> | Policy Check   | -> | Compliance Map | -> | Remediation    |
+-------------+    +----------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 자산 수집    | -> | 설정 점검    | -> | 위반 식별    | -> | 자동/수동 수정 | -> | 재검사와 보고  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **자산 수집**: 계정과 리소스 구성을 읽어옴
2. **설정 점검**: 정책 기준과 현재 설정을 비교함
3. **위반 식별**: 잘못된 구성과 규정 위반을 탐지함
4. **자동과 수동 수정**: 위험도에 따라 조치함
5. **재검사와 보고**: posture 상태 변화를 추적함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 정책이 많아도 자산 탐색 범위가 불완전하면 중요한 노출 자산을 놓칠 수 있음
   - 해결방안: continuous asset discovery와 account onboarding control을 적용하고 asset coverage ratio와 unmanaged account count로 검증함
2. 문제: posture 경고가 과도하면 운영팀이 실제 고위험 설정을 우선 조치하지 못할 수 있음
   - 해결방안: risk based prioritization과 contextual suppression policy를 적용하고 alert fatigue index와 high risk remediation rate로 검증함
3. 문제: 자동 수정이 무분별하면 서비스 가용성을 해치거나 팀 간 충돌을 유발할 수 있음
   - 해결방안: change reviewed auto remediation과 rollback safe policy를 적용하고 remediation induced incident rate와 rollback success rate로 검증함

## Ⅶ. 적용 사례

- 멀티클라우드 조직이 연속 자산 탐색을 운영하며 확인 지표는 asset coverage ratio와 unmanaged account count임
- 보안 운영팀이 위험도 기반 우선순위를 적용하며 확인 지표는 alert fatigue index와 high risk remediation rate임
- 자동 교정 체계가 변경 검토 절차를 포함하며 확인 지표는 remediation induced incident rate와 rollback success rate임

## Ⅷ. 결론

CSPM은 클라우드 오구성을 조기에 잡는 핵심 도구이므로 탐색 범위와 우선순위 품질과 안전한 수정 절차를 함께 관리해야 함.
