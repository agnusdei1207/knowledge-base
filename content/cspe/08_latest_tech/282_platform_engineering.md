---
title: "Platform Engineering 플랫폼 엔지니어링 (Platform Engineering)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 282
extra:
  question_no: "282"
  exam_status: "기출"
  exam_history: "135회"
  exam_note: "전망"
---

## 미리 알고가기

- Platform Engineering은 개발자가 반복적으로 필요로 하는 인프라와 운영 기능을 제품처럼 제공하는 엔지니어링 접근임
- DevOps를 대체한다기보다 개발자 경험을 높이기 위해 플랫폼 팀이 제품 관점으로 구현하는 흐름에 가깝움
- 핵심 산출물은 IDP와 golden path와 셀프서비스 자동화임

## Ⅰ. 개요

- **정의/개념**: Platform Engineering은 개발자와 서비스 팀이 공통적으로 사용하는 배포와 관측과 보안과 런타임 기능을 내부 플랫폼으로 제품화하여 셀프서비스 방식으로 제공하는 엔지니어링 접근임
- **배경/필요성**: 클라우드 네이티브 도입이 확산되면서 팀마다 인프라를 중복 구성하면 속도와 품질과 보안 표준이 동시에 무너져 내부 플랫폼 전문화가 필요해짐

## Ⅱ. 특징

- 개발자 경험을 제품 관점에서 설계함
- 공통 기능을 golden path로 표준화해 반복 작업을 줄임
- 셀프서비스 자동화로 배포 속도와 일관성을 높임
- 플랫폼 자체도 사용자 피드백과 제품 지표로 지속 개선해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Platform Engineering | 전통적 인프라 운영팀 | DevOps 문화 |
|:---|:---|:---|:---|
| 제공 방식 | 내부 플랫폼 제품 | 요청 기반 지원 | 협업 원칙과 자동화 |
| 개발자 경험 | 핵심 목표 | 부차적 | 중요하지만 간접적 |
| 표준화 수준 | 높음 | 중간 | 조직별 편차 큼 |
| 대표 산출물 | IDP, templates, APIs | 운영 절차 | 자동화 문화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Platform Team | 개발자 내부 고객을 대상으로 플랫폼 기능을 설계하고 운영하는 제품형 엔지니어링 팀임 |
| Golden Path Template | 표준 배포와 보안과 관측 구성을 미리 조합해 빠른 시작 경로를 제공하는 템플릿 계층임 |
| Self Service Interface | 개발자가 티켓 없이 직접 환경과 배포와 리소스를 요청할 수 있게 하는 포털이나 API임 |
| Shared Runtime and Tooling | Kubernetes와 CI CD와 secrets와 observability 같은 공통 런타임 자원을 제공하는 기반 계층임 |
| Feedback and Product Metrics | 플랫폼 사용성과 채택률과 실패율을 측정해 개선 우선순위를 정하는 제품 운영 계층임 |

```text
+----------------+    +-------------------+    +----------------+
| Platform Team  | -> | Self Service IDP  | -> | Dev Teams      |
+----------------+    +-------------------+    +----------------+
        |                     |
        v                     v
  Golden Path            Shared Runtime
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요구 수집    | -> | 플랫폼 기능화 | -> | 셀프서비스 제공 | -> | 개발팀 사용   | -> | 피드백 개선    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요구 수집**: 개발팀의 반복 요구와 병목을 파악함
2. **플랫폼 기능화**: 공통 기능을 표준 컴포넌트와 자동화로 만든다
3. **셀프서비스 제공**: 포털이나 API로 쉽게 노출함
4. **개발팀 사용**: 팀이 플랫폼을 통해 배포와 운영을 수행함
5. **피드백 개선**: 사용성 지표를 바탕으로 플랫폼을 고도화함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 플랫폼 팀이 개발자 요구를 모른 채 기능만 늘리면 채택률이 낮아지고 우회 사용이 늘어날 수 있음
   - 해결방안: product discovery loop와 developer experience metric을 적용하고 platform adoption rate와 bypass workflow ratio로 검증함
2. 문제: golden path가 지나치게 경직되면 다양한 서비스 요구를 수용하지 못해 개발 속도를 오히려 늦출 수 있음
   - 해결방안: opinionated default with escape hatch를 적용하고 exception request lead time와 standard path usage ratio로 검증함
3. 문제: 플랫폼이 커질수록 운영 책임이 집중되어 팀 자체가 병목이 될 수 있음
   - 해결방안: API first automation과 federated ownership model을 적용하고 platform team ticket load와 self service completion rate로 검증함

## Ⅶ. 적용 사례

- 내부 플랫폼 팀이 제품 탐색 루프를 운영하며 확인 지표는 platform adoption rate와 bypass workflow ratio임
- 멀티서비스 조직이 escape hatch 정책을 적용하며 확인 지표는 exception request lead time와 standard path usage ratio임
- 대규모 기업이 API 우선 자동화를 강화하며 확인 지표는 platform team ticket load와 self service completion rate임

## Ⅷ. 결론

Platform Engineering은 인프라를 제품으로 전환하는 접근이므로 표준화만큼 개발자 경험과 채택률을 함께 지표화해야 성공함.
