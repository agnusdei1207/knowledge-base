---
title: "OPA Gatekeeper 정책 엔진 (OPA Gatekeeper)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 124
---
# 📖 【암기용】 개념 완전 이해

> 목적: OPA Gatekeeper를 처음 보는 사람도 Kubernetes 정책 엔진이 배포를 어떻게 통제하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.
## 한눈에
- **개요**: OPA Gatekeeper는 Kubernetes Admission 단계에서 정책을 검사해 위험한 리소스 생성을 차단하거나 감사하는 Policy as Code 도구임
- **왜 필요한가**: Kubernetes는 YAML 하나로 privileged Pod, hostPath mount, latest image, 과도한 권한을 만들 수 있다. 사람의 리뷰만으로 모든 배포를 검사하면 누락이 발생한다.
- **핵심 직관**: 건물 출입구에서 방문 신청서를 규정표와 대조해 출입 허용, 경고, 반려를 자동 결정하는 보안 접수대임
## 깊이 이해
- **배경·문제의식**: 플랫폼팀은 "root 컨테이너 금지", "리소스 제한 필수", "approved registry만 허용" 같은 규칙을 모든 네임스페이스에 동일하게 적용해야 한다. Gatekeeper는 이 규칙을 코드로 관리하고 API Server 요청 시점에 자동 평가한다.
- **작동 원리**: 정책 로직은 ConstraintTemplate에 Rego로 작성하고, 적용 대상·파라미터·enforcementAction은 Constraint에 작성한다. Admission Webhook이 create/update 요청을 받아 OPA로 평가하고 deny, warn, dryrun 결과를 반환한다. Audit 기능은 이미 존재하는 리소스의 위반도 주기적으로 찾는다.
- **비유**: 계약서 표준 조항을 템플릿으로 만들고, 각 부서별 예외 조건을 붙여 전자결재에서 자동 검토하는 방식임
- **구체 예시**: `K8sRequiredLabels` ConstraintTemplate으로 `owner`, `data-class` 라벨을 강제하고, `prod` 네임스페이스에서 누락 리소스 생성을 deny 처리함
- **흔한 오해·주의점**: Gatekeeper는 런타임 침입 탐지 도구가 아니다. 생성·수정 요청을 사전에 제어하고 기존 리소스를 감사하는 정책 집행 계층임
## 연결 개념
- OPA/Rego — 범용 정책 엔진과 정책 언어
- Kubernetes Admission Controller — API 요청 승인 전 정책 검사 지점
- Policy as Code — 정책을 Git, CI, 리뷰, 배포 파이프라인으로 관리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Gatekeeper는 YAML 검증기가 아니라 Kubernetes API 요청을 정책 코드로 통제하고 audit 결과를 운영 증거로 남기는 Admission Governance 체계로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OPA Gatekeeper는 Kubernetes Admission Webhook과 OPA 정책 엔진을 결합해 리소스 생성·수정 요청을 Constraint 정책으로 평가하는 Policy as Code 도구이다.
> 2. **가치**: privileged Pod, hostPath, latest image, 필수 라벨 누락, Registry 위반을 배포 전에 deny·warn·dryrun으로 통제한다.
> 3. **판단 포인트**: ConstraintTemplate, Constraint, Rego, enforcementAction, audit, 예외 만료와 성능 지표를 함께 제시해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Kubernetes 정책 집행 구조 이해 확인 | Admission Webhook, OPA, ConstraintTemplate, Constraint | Rego 문법만 길게 설명 |
| 보안 거버넌스 설계 역량 확인 | deny/warn/dryrun, audit, exception, namespace scope | 정책 예시 없이 개념 나열 |
| 운영 영향 판단 확인 | API Server 지연, 정책 충돌, 예외 만료, 감사 지표 | 모든 정책을 deny로 시작 |

> 요약: Gatekeeper 답안은 정책 정의, Admission 평가, 감사, 예외 운영을 하나의 통제 흐름으로 구성해야 한다.

---

## Ⅰ. 개요 및 필요성

OPA Gatekeeper는 Kubernetes 정책 집행 엔진이다.
클러스터에서는 YAML 배포 하나로 권한·네트워크·이미지·라벨 정책 위반이 발생할 수 있음.
따라서 Admission 단계에서 정책을 코드로 평가하고 위반 요청은 차단·경고·감사해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
kubectl/CI -> Kubernetes API Server -> Admission Webhook -> Gatekeeper/OPA
  / ConstraintTemplate: Rego logic and schema
  / Constraint: target, parameter, enforcementAction
Gatekeeper/OPA -> deny/warn/dryrun -> Audit Violations -> SIEM/Ticket
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Admission Webhook | API Server 요청을 Gatekeeper로 전달 | create/update/delete 정책 평가 |
| ConstraintTemplate | Rego 정책 로직과 입력 스키마 정의 | 재사용 가능한 정책 템플릿 |
| Constraint | 적용 대상, 파라미터, enforcementAction 지정 | namespaceSelector, matchKinds |
| Audit Controller | 기존 리소스를 주기적으로 평가 | violation을 Constraint 상태에 기록 |
| Policy Library | 표준 정책 샘플 제공 | required labels, allowed repos, PSP 대체 |
| Exception Process | 예외 승인과 만료 관리 | 30일 만료, 승인자, 근거 기록 |

> 요약: Gatekeeper는 템플릿과 제약 조건을 분리해 Admission 요청과 기존 리소스 감사에 동일 정책을 적용한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
정책 작성 -> ConstraintTemplate 등록 -> Constraint 적용
-> API Server 요청 수신 -> Admission Webhook 호출
-> OPA 정책 평가 -> deny/warn/dryrun 응답
-> Audit Controller 기존 리소스 점검 -> 위반 조치
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 보안 요구사항을 Rego 정책으로 작성 | 단위 테스트 통과율 100% |
| 2 | ConstraintTemplate CRD와 Constraint 배포 | dryrun 7일 후 deny 전환 |
| 3 | Admission 요청을 OPA 입력 객체로 평가 | p95 admission latency 100ms 이하 |
| 4 | 위반 요청 deny/warn/dryrun 처리 | prod namespace Critical 정책 deny |
| 5 | Audit 결과를 티켓·SIEM으로 전송 | violation 24시간 내 담당자 지정 |

> 요약: Gatekeeper는 정책을 먼저 dryrun으로 검증한 뒤 deny로 전환하고 Admission 지연과 violation 지표를 함께 관리한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | OPA Gatekeeper | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 정책 방식 | 문서·수동 리뷰 | Rego 기반 Policy as Code | Git 리뷰 2인 승인 |
| 집행 시점 | 배포 후 점검 | Admission 단계 deny/warn/dryrun | prod deny, dev warn |
| 감사 범위 | 신규 배포 중심 | 기존 리소스 audit 가능 | 24시간 주기 audit |
| 한계 | 정책 없음 | Rego 복잡도, API 지연, 예외 관리 필요 | p95 100ms, 예외 30일 만료 |

> 요약: Gatekeeper는 정책을 코드와 Admission 제어로 전환하지만 정책 테스트와 지연 관리가 필수이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | OPA Gatekeeper | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | kubectl 리뷰, CI lint | API Server Admission 통제 | 멀티팀 클러스터, prod namespace 운영 |
| 비용/성능 | 리뷰 비용 증가 | 정책 평가 지연 추가 | p95 admission latency 100ms 이하 허용 |
| 운영/위험 | 정책 누락·사람 의존 | dryrun, warn, deny 단계 적용 | 규제 워크로드와 감사 증거 필요 시 |

> 요약: 멀티팀 Kubernetes 환경에서는 수동 리뷰보다 Gatekeeper Admission 정책이 반복 위반을 배포 전 차단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 업무 중단 | deny 정책을 검증 없이 적용 | dryrun 7일, warn 전환, 영향 분석 | deny 전환 후 실패율 1% 이하 |
| 정책 충돌 | 팀별 Constraint 중복 | 정책 카탈로그, 우선순위, 소유자 지정 | 중복 정책 0건 |
| API 지연 | 복잡한 Rego, 외부 호출 의존 | 단순 입력 평가, 캐시, 정책 최적화 | p95 100ms 이하 |
| 예외 남용 | namespace 예외 장기 유지 | 예외 승인자·사유·만료일 필수 | 만료 초과 예외 0건 |

> 요약: Gatekeeper 리스크는 deny 오작동, 정책 충돌, API 지연, 예외 남용이며 단계 전환과 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 커버리지 | prod 필수 정책 20개 이상 | Constraint 목록, CIS Benchmark 매핑 |
| 위반 처리 | Critical violation 24시간 내 조치 | Audit 결과, 티켓 SLA |
| Admission 지연 | p95 100ms 이하, timeout 0건 | API Server metric, webhook metric |
| 예외 관리 | 예외 30일 만료, 승인자 100% 기록 | exception CRD, Git 이력 |

> 요약: Gatekeeper 운영 성과는 정책 커버리지, 위반 SLA, Admission 지연, 예외 만료 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 1단계: required labels, allowed registries, privileged Pod 금지, hostPath 제한 등 필수 정책 20개를 dryrun으로 7일 운영
2. 2단계: prod namespace는 Critical 정책 deny, dev namespace는 warn 적용하고 p95 admission latency 100ms 이하 유지
3. 3단계: Audit violation을 SIEM·티켓 시스템에 전송하고 예외 승인자, 사유, 30일 만료일을 Git으로 관리

**결론 (2줄):**
- 기술사 판단: 단일 팀 테스트 클러스터는 CI lint로 시작 가능하나, 멀티팀 운영 클러스터는 Gatekeeper Admission 정책이 필요함
- 향후 방향: Gatekeeper, Kyverno, Sigstore, SBOM 증거를 결합해 Kubernetes 공급망 정책을 코드 기반으로 운영해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OPA Gatekeeper를 설명하시오", "Policy as Code를 기술하시오" | ConstraintTemplate, Constraint, Admission 평가 흐름 | deny/warn/dryrun, audit, 정책 코드화 |
| 요구사항 명시형 | "Kubernetes 정책 통제 방안을 제시하시오", "Admission Controller를 설계하시오" | dryrun에서 deny 전환, p95 지연, 예외 만료 | 필수 정책 20개, 위반 SLA, 운영 리스크 대응 |

> 요약: 설명형은 구조와 원리를 쓰고, 설계형은 정책 전환 절차와 운영 지표를 답안 중심에 둔다.
