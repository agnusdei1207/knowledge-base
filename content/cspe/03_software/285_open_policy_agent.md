---
title: "OPA 정책 엔진 (Open Policy Agent)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 285
---

# 📖 【암기용】 개념 완전 이해

> 목적: OPA 정책 엔진을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: OPA(Open Policy Agent)는 **Policy as Code**를 구현하는 범용 **정책 결정 엔진**(PDP, Policy Decision Point)이다 — 인가·배포·네트워크 정책을 코드(Rego)로 작성해 어떤 시스템에서도 같은 방식으로 평가한다.
- **왜 필요한가**: 마이크로서비스마다, Kubernetes마다, API Gateway마다 정책을 각자의 언어와 형식(if문, YAML, 방화벽 룰)으로 흩어 두면 정책이 바뀔 때마다 여러 곳을 손대야 하고 감사도 어렵다. OPA는 "정책을 판단하는 곳(PDP)"을 하나로 모으고, "실제로 막는 곳(PEP, Policy Enforcement Point)"은 각 시스템에 남긴다.
- **핵심 직관**: OPA는 심판이고 Rego 정책은 경기 규칙집이다. 선수(서비스·Kubernetes)는 "이런 상황인데 되나요?"라는 사실만 심판에게 보내고, 심판은 규칙집을 펴서 허용·거부만 판정해 돌려준다. 심판은 선수를 직접 잡아 끌어내지 않는다 — 퇴장시키는 건 경기 진행요원(집행 지점)의 몫이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Policy as Code | 정책을 텍스트 코드로 작성해 버전 관리·테스트·리뷰하는 방식 — OPA가 구현하는 상위 패러다임 | 판례가 아니라 성문법으로 관리 |
| PDP / PEP | 정책을 **판단**하는 곳(Policy Decision Point=OPA)과 실제로 **집행**하는 곳(Policy Enforcement Point=Gateway·Kubernetes)의 역할 분리 | 판사(PDP)와 집행관(PEP) |
| Rego | OPA 전용 선언형 정책 언어 — "이 조건이면 deny"를 규칙으로 적는다 | 법 조문 |
| Input | 매 요청마다 OPA에 전달하는 JSON — 누가, 무엇을, 어떤 리소스에 하려는지 | 심판에게 제출하는 상황 설명서 |
| Data Document | 정책 평가에 참조하는 정적 데이터(역할 목록, 예외 리스트) — input과 별개로 미리 로드해 둔다 | 규칙집에 딸린 부록 명단 |
| Decision API | input과 정책을 평가해 allow/deny/reason을 반환하는 OPA의 REST 엔드포인트 | 심판의 판정 방송 |
| Bundle | Rego 정책과 data document를 묶어 배포하는 단위 | 개정된 규칙집 한 세트 |
| Admission Controller | Kubernetes가 리소스를 실제로 만들기 직전에 외부(OPA)에 "이거 만들어도 되나요?" 물어보는 webhook 지점 | 입국 심사대 |

## 깊이 이해

### 왜 "정책 결정"과 "정책 집행"을 나누는가
- 인증(내가 누구인지 확인)은 IdP가, 인가·정책 판단(내가 이걸 해도 되는지)은 OPA가, 실제 차단은 API Gateway나 Kubernetes API 서버가 담당하도록 3단으로 나눈다. 이렇게 나누면 정책 하나(예: "latest 태그 금지")를 바꿀 때 OPA에 새 Rego bundle 하나만 배포하면 되고, Gateway·Kubernetes·CI 어디에서 이 정책을 쓰든 로직을 중복 구현할 필요가 없다.

### Rego 정책이 실제로 어떻게 생겼는가 — 워크드 예제
- Kubernetes admission에서 "latest 태그 이미지 금지" 정책은 대략 이렇게 작성한다.
```
package kubernetes.admission

deny[msg] {
  input.request.kind.kind == "Pod"
  image := input.request.object.spec.containers[_].image
  endswith(image, ":latest")
  msg := "latest 태그 이미지는 배포할 수 없습니다"
}
```
- 흐름: 새 Pod 생성 요청이 오면(1) Kubernetes API 서버가 admission webhook으로 요청 JSON을 OPA에 보낸다(2) OPA는 이 JSON을 `input`으로 받아 위 규칙을 평가한다(3) 컨테이너 이미지가 `nginx:latest`면 `deny` 규칙이 참이 되어 msg가 채워지고, OPA는 "거부, 사유: latest 태그 금지"를 반환한다(4) Kubernetes API 서버는 이 결정을 받아 실제로 Pod 생성을 막는다 — 여기서 "막는 행위"는 OPA가 아니라 Kubernetes(PEP)가 한다.

### 왜 속도가 설계 이슈가 되는가
- OPA는 매 요청(API 호출, Pod 생성)마다 호출되므로 결정 지연이 곧 서비스 지연이 된다. 예컨대 API Gateway가 초당 수천 건의 요청마다 원격 OPA 서버를 호출하면 네트워크 왕복이 병목이 된다. 그래서 실무에서는 OPA를 sidecar로 각 서비스 옆에 붙이거나, bundle을 로컬에 미리 캐시해 두어 판정을 메모리 내 연산으로 끝내고 p95 응답을 10ms 이하로 유지한다.

### 흔한 오해
- OPA는 로그인·비밀번호 검증 같은 인증(Authentication) 시스템이 아니다. "이 사용자는 누구다"라는 사실이 이미 확정된 뒤, "이 사용자가 이 행위를 해도 되는가"를 판단하는 인가(Authorization)·정책 계층이다. 인증까지 OPA가 한다고 서술하면 역할을 잘못 이해한 것이다.

## 연결 개념
- Policy as Code - 정책을 버전 관리하고 테스트하는 방식
- Kubernetes Admission Control - 배포 전 리소스 검증 지점
- Zero Trust - 요청별 정책 평가와 최소 권한

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: OPA를 도구명으로만 설명하지 말고 Policy as Code, Rego, decision API, admission control, 감사 추적 관점으로 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OPA는 JSON 입력과 Rego 정책을 평가해 허용·거부 결정을 반환하는 범용 정책 엔진이다.
> 2. **가치**: 정책을 코드화해 버전 관리, 테스트, 감사, 배포 자동화를 가능하게 한다.
> 3. **판단 포인트**: 인증은 IdP, 정책 결정은 OPA, 정책 집행은 애플리케이션·Gateway·Kubernetes가 맡도록 분리한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Policy as Code 이해 확인 | Rego, input, data, decision API | OPA를 단순 RBAC 도구로 축소 |
| 클라우드 네이티브 통제 판단 확인 | Kubernetes admission, CI policy check | 런타임 인가와 배포 전 검증 구분 누락 |
| 보안 운영 적용 역량 확인 | 정책 테스트, audit log, 예외 승인 | 정책 충돌과 성능 지연 위험 누락 |

> 요약: OPA 답안은 정책 결정과 집행을 분리하고, 정책을 코드로 검증·감사하는 구조를 보여야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: OPA는 범용 정책 결정 엔진이다.
- 배경: 마이크로서비스와 Kubernetes 환경에서는 인가, 배포 제한, 데이터 접근 정책이 여러 계층에 분산된다.
- 필요성: Rego 기반 Policy as Code로 정책 변경 이력, 테스트, 감사 추적을 관리해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client/System -> Input JSON -> OPA Decision API -> Rego Policy -> Allow/Deny
                                 +-> Data Document
                                 +-> Audit Log
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Input | 사용자, 리소스, 행위, 환경 정보 전달 | JSON 구조 |
| Rego Policy | 허용·거부 조건 선언 | unit test, version control |
| Data Document | 조직, 권한, 예외 목록 저장 | bundle로 배포 |
| Decision API | 정책 평가 결과 반환 | allow, deny, reason |
| Enforcement Point | 결과를 실제 차단·허용 | API Gateway, Envoy, Kubernetes |

> 요약: OPA는 입력, 정책, 데이터, 결정 API, 집행 지점을 분리해 정책 변경과 실행을 독립적으로 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 발생 -> 속성 추출 -> OPA 질의 -> Rego 평가 -> 결정 반환 -> 허용/차단/기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청의 subject, action, resource 추출 | 필수 속성 누락 0건 |
| 2 | OPA에 input JSON 전달 | API 응답 p95 10ms 이하 |
| 3 | Rego 정책과 data bundle 평가 | 정책 테스트 통과 100% |
| 4 | allow/deny와 reason 반환 | 거부 사유 로그 100% |
| 5 | 집행 지점에서 요청 처리 | 정책 위반 통과 0건 |

> 요약: OPA는 요청 속성을 정책과 대조하고 결정 결과를 집행 지점이 적용하는 방식으로 동작한다.

---

## Ⅳ. 특징

| 구분 | 하드코딩 정책 | OPA Policy as Code | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 정책 위치 | 애플리케이션 내부 | 외부 정책 엔진 | decision API |
| 변경 관리 | 코드 배포 필요 | policy bundle 배포 | Git diff와 review |
| 검증 방식 | 수동 테스트 | Rego unit test | 정책 테스트 통과 100% |
| 적용 범위 | 단일 서비스 | API, Kubernetes, CI, Envoy | 범용 JSON input |

> 요약: OPA는 정책을 애플리케이션에서 분리해 여러 집행 지점에서 같은 규칙을 평가하게 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 코드 내 if문 인가 | OPA 외부 정책 결정 | 서비스 수 10개 이상 |
| 비용/성능 | 서비스별 정책 중복 | 중앙 정책과 분산 집행 | 정책 변경 빈도 월 1회 이상 |
| 운영/위험 | 정책 감사 곤란 | Git 기반 정책 이력과 테스트 | 규제 감사·권한 검토 요구 |

> 요약: 서비스와 정책 변경이 많을수록 OPA로 정책 결정을 분리하는 편이 감사와 일관성 측면에서 유리하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정책 충돌 | Rego 규칙 중복·우선순위 불명확 | policy test, deny reason 표준화 | 정책 테스트 실패 0건 |
| 응답 지연 | 원격 OPA 호출 증가 | sidecar, cache, bundle pre-load | decision p95 10ms 이하 |
| 우회 경로 | 집행 지점 누락 | gateway/admission mandatory 적용 | 미적용 endpoint 0건 |

> 요약: OPA 운영은 정책 품질, decision latency, 집행 지점 누락을 지표로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 품질 | Rego unit test 100% 통과 | `opa test`, CI log |
| 통제 효과 | 정책 위반 배포 0건 | admission audit, CI report |
| 감사 추적 | 정책 변경 PR 100% 리뷰 | Git history, approval log |

> 요약: OPA 도입 효과는 정책 테스트, 위반 차단, 변경 리뷰 추적률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Kubernetes admission에 OPA Gatekeeper를 적용해 privileged container, latest tag, resource limit 누락을 차단함
2. API Gateway나 Envoy ext_authz와 OPA를 연동해 사용자, 역할, 리소스 속성 기반 ABAC 정책을 평가함
3. 정책 저장소를 Git으로 관리하고 `opa test`, policy review, bundle 배포를 CI 파이프라인에 포함함

**결론 (2줄):**
- 기술사 판단: 정책이 서비스별로 중복되면 OPA로 정책 결정을 분리하고, 고빈도 요청은 sidecar와 cache를 적용함
- 향후 방향: OPA는 Kubernetes, API, 데이터 접근 제어를 아우르는 Policy as Code 표준 구성요소로 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OPA 정책 엔진을 설명하시오" | input, Rego, decision API 평가 흐름 | Policy as Code와 적용 범위 |
| 요구사항 명시형 | "Kubernetes 보안 정책 방안을 제시하시오" | admission 요청 평가와 차단 흐름 | Gatekeeper, 정책 테스트, audit 기준 |

> 요약: 설명형은 정책 엔진 구조, 보안형은 배포 차단 정책과 집행 지점 중심으로 전개한다.
