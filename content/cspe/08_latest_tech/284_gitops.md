---
title: "GitOps (GitOps)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 284
extra:
  question_no: "284"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- GitOps는 Git 저장소를 운영 시스템의 단일 진실 원천으로 삼아 배포와 변경을 자동 동기화하는 운영 방식임
- 선언형 인프라와 pull 기반 반영이 핵심 특징임
- 단순 CI CD 도구 사용과 달리 운영 상태와 Git 상태 일치성 유지가 중심 목표임

## Ⅰ. 개요

- **정의/개념**: GitOps는 애플리케이션과 인프라의 선언형 구성을 Git에 저장하고 운영 시스템이 이를 기준으로 자동 동기화하게 만들어 변경 이력과 운영 상태를 일관되게 관리하는 운영 방식임
- **배경/필요성**: 복잡한 클라우드 네이티브 환경에서 수동 배포와 드리프트가 반복되면서 선언형 구성과 감사 가능성이 높은 자동 운영 모델이 요구됨

## Ⅱ. 특징

- Git이 승인과 변경 이력과 배포 기준점 역할을 함
- 선언형 매니페스트와 pull 기반 동기화로 운영 안정성을 높임
- 변경 추적과 롤백과 감사 대응이 쉬움
- 비선언형 자원과 긴급 수동 변경 관리가 과제로 남음

## Ⅲ. 종류 및 비교

| 판단 기준 | GitOps | Push Based CI CD | Manual Ops |
|:---|:---|:---|:---|
| 변경 기준점 | Git 저장소 | 배포 도구 실행 | 운영자 판단 |
| 감사 가능성 | 높음 | 중간 | 낮음 |
| 상태 일치 관리 | 강함 | 제한적 | 낮음 |
| 긴급 변경 유연성 | 낮음 | 중간 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Git Repository | 선언형 매니페스트와 정책과 환경 구성을 저장해 단일 진실 원천 역할을 하는 저장소임 |
| Reconciliation Controller | 운영 클러스터 상태를 Git과 비교해 차이가 나면 자동으로 일치시키는 동기화 제어기임 |
| Policy Gate | 머지 승인과 보안 검증과 정책 검사를 통해 잘못된 변경이 반영되지 않게 하는 검증 계층임 |
| Runtime Target | Kubernetes 클러스터 같은 실제 운영 대상 환경으로 Git 상태를 적용받는 실행 공간임 |
| Drift Detector | 수동 변경이나 비정상 상태를 감지해 Git 기준과의 불일치를 찾아내는 감시 계층임 |

```text
+--------------+    +------------------+    +----------------+
| Git Repo     | -> | Reconciliation   | -> | Runtime Target |
+--------------+    +------------------+    +----------------+
        ^                     |
        |_____________________|
             Drift Detection
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 변경 커밋    | -> | 리뷰와 승인  | -> | 자동 동기화  | -> | 상태 비교    | -> | 드리프트 수정  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **변경 커밋**: 운영 변경을 Git에 기록함
2. **리뷰와 승인**: 코드 리뷰와 정책 검사를 통과함
3. **자동 동기화**: 컨트롤러가 운영 환경에 반영함
4. **상태 비교**: 실제 상태와 Git 상태를 계속 비교함
5. **드리프트 수정**: 차이가 나면 자동 복원하거나 경보를 보냄

## Ⅵ. 문제점 및 해결 방안

1. 문제: 긴급 수동 변경이 자주 발생하면 Git 상태와 운영 상태가 쉽게 어긋나 신뢰성이 약해질 수 있음
   - 해결방안: break glass workflow와 drift reconciliation policy를 적용하고 out of band change count와 drift recovery time으로 검증함
2. 문제: 선언형으로 표현되지 않는 자원은 GitOps 범위 밖에 남아 운영 복잡도를 키울 수 있음
   - 해결방안: declarative coverage expansion과 exception registry를 적용하고 declarative asset coverage와 unmanaged resource ratio로 검증함
3. 문제: Git 리포지터리 구조와 환경 분리가 부정확하면 멀티환경 운영에서 변경 충돌이 자주 발생할 수 있음
   - 해결방안: environment repo strategy와 promotion pipeline design을 적용하고 config conflict rate와 promotion lead time으로 검증함

## Ⅶ. 적용 사례

- 운영 클러스터가 긴급 변경 워크플로우를 적용하며 확인 지표는 out of band change count와 drift recovery time임
- 플랫폼 팀이 선언형 범위를 확장하며 확인 지표는 declarative asset coverage와 unmanaged resource ratio임
- 멀티환경 배포 체계가 환경 분리 전략을 사용하며 확인 지표는 config conflict rate와 promotion lead time임

## Ⅷ. 결론

GitOps는 배포 자동화보다 운영 일치성 관리가 본질이므로 Git을 진실 원천으로 유지할 수 있는 선언형 범위와 예외 관리가 중요함.
