---
title: "Software Supply Chain Security 소프트웨어 공급망 보안 (Software Supply Chain Security)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 302
extra:
  question_no: "302"
  exam_status: "기출"
  exam_history: "134회, 135회"
---

## 미리 알고가기

- 소프트웨어 공급망은 소스 저장소와 의존성 저장소와 빌드 시스템과 배포 경로를 모두 포함함
- 공격자는 최종 서비스보다 개발 도구와 패키지와 업데이트 경로를 먼저 노리는 경우가 많음
- 공급망 보안은 취약점 탐지보다 신뢰 가능한 생성과 배포 통제를 더 넓게 다룸

## Ⅰ. 개요

- **정의/개념**: Software Supply Chain Security는 소스 코드와 외부 의존성과 빌드와 서명과 저장소와 배포 검증을 통합 관리해 소프트웨어가 오염되지 않은 상태로 생성되고 전달되도록 보장하는 보안 체계임
- **배경/필요성**: 오픈소스 활용 증가와 CI CD 자동화 확대로 개발 속도는 높아졌지만 패키지 변조와 계정 탈취와 악성 업데이트가 전체 서비스 신뢰를 흔들면서 종단간 공급망 통제가 필요해짐

## Ⅱ. 특징

- 개발자 단말부터 배포 저장소까지 이어지는 전 경로를 보안 대상에 포함함
- 외부 패키지와 내부 빌드 결과물의 신뢰 검증이 함께 이루어져야 완전성이 생김
- 서명과 provenance와 정책 검증이 배포 승인 조건으로 연결될 때 운영 효과가 커짐
- 도구만 도입해서는 부족하고 조달과 개발 표준과 운영 검문 체계가 함께 맞물려야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Software Supply Chain Security | Traditional AppSec | Vendor Risk Review |
|:---|:---|:---|:---|
| 보호 대상 | 코드, 의존성, 빌드, 배포 경로 | 애플리케이션 취약점 | 외부 공급자 평가 |
| 핵심 통제 | 서명, provenance, 무결성 검증 | SAST, DAST, 취약점 패치 | 계약과 심사 |
| 탐지 시점 | 개발부터 배포 직전까지 | 개발과 운영 테스트 | 도입 전후 점검 |
| 주요 가치 | 결과물 신뢰 사슬 확보 | 기능 취약점 감소 | 공급자 관리 강화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Repository Control | 승인된 변경과 서명과 브랜치 보호를 관리해 내부 코드 변경 경로의 신뢰를 유지하는 시작점임 |
| Dependency and Package Governance | 오픈소스 저장소와 사내 패키지 저장소를 검증해 악성 패키지와 취약 구성요소 유입을 줄이는 외부 연계 통제층임 |
| Secure Build Pipeline | 빌드 자동화와 비밀값 보호와 재현 가능한 실행 환경을 제공해 결과물 생성 구간의 오염 가능성을 낮추는 핵심 공정임 |
| Signing and Artifact Registry | 산출물과 서명을 저장하고 배포 전 검증 근거를 관리해 유통 경로의 무결성을 유지하는 보관 및 배포 계층임 |
| Runtime Verification Gate | 배포 시점에 서명과 provenance와 정책 적합성을 확인해 신뢰되지 않은 결과물이 운영 환경에 들어가지 못하게 하는 최종 검문 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| Source Repo | -> | Dependencies| -> | Build Pipe  | -> | Registry    | -> | Runtime Gate|
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 코드/패키지 검증 | -> | 안전 빌드 수행 | -> | 산출물 서명    | -> | 저장소 등록    | -> | 배포 전 검증  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **코드와 패키지 검증**: 승인된 소스와 허용된 의존성만 빌드 후보로 통과시킴
2. **안전 빌드 수행**: 격리된 CI 환경에서 결과물을 생성함
3. **산출물 서명**: 이미지와 바이너리와 provenance를 함께 서명함
4. **저장소 등록**: 서명된 결과물만 중앙 저장소에 등록함
5. **배포 전 검증**: 운영 환경에서 정책 기준 미충족 산출물을 차단함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 외부 오픈소스와 서드파티 빌드 도구에 대한 가시성이 부족하면 취약 구성요소와 악성 패키지가 내부 파이프라인으로 쉽게 유입될 수 있음
   - 해결방안: curated package policy와 supplier transparency control을 적용하고 approved dependency usage ratio와 unknown package detection count로 검증함
2. 문제: 소스와 빌드와 배포 검증이 서로 다른 도구에 흩어지면 경고는 많아져도 실제 차단 통제가 약해질 수 있음
   - 해결방안: unified policy orchestration과 deployment gate integration을 적용하고 policy enforcement coverage와 release blocked by policy count로 검증함
3. 문제: 서명과 provenance를 운영 배포 단계에서 확인하지 않으면 형식적 생성만 남고 위변조 차단 효과가 사라질 수 있음
   - 해결방안: cluster admission verification과 signed artifact only policy를 적용하고 unsigned deployment attempt count와 verification pass rate로 검증함

## Ⅶ. 적용 사례

- 오픈소스 사용 조직이 승인 패키지 저장소를 운영하며 확인 지표는 approved dependency usage ratio와 unknown package detection count임
- 플랫폼 엔지니어링 팀이 정책 오케스트레이션을 도입하며 확인 지표는 policy enforcement coverage와 release blocked by policy count임
- 쿠버네티스 운영 환경이 서명 검증 기반 배포를 적용하며 확인 지표는 unsigned deployment attempt count와 verification pass rate임

## Ⅷ. 결론

소프트웨어 공급망 보안은 개발 보안의 부속 기능이 아니라 생성과 유통 전체를 검증하는 체계이므로 정책과 서명과 배포 차단을 하나의 통제선으로 설계해야 함.
