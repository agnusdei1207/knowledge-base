---
title: "SLSA 공급망 보안 프레임워크 (Supply-chain Levels for Software Artifacts)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 301
extra:
  question_no: "301"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- SLSA는 소프트웨어가 어떤 과정으로 안전하게 만들어졌는지를 검증하는 공급망 보안 성숙도 체계임
- SBOM이 구성요소 목록을 보여준다면 SLSA는 빌드 과정의 무결성과 출처 증명을 다룸
- Level이 높아질수록 소스 통제와 빌드 격리와 provenance 신뢰성이 강화됨

## Ⅰ. 개요

- **정의/개념**: SLSA는 소스 변경부터 빌드와 서명과 배포 전 검증까지의 공급망 전 과정을 통제해 소프트웨어 아티팩트의 출처와 무결성을 단계별로 보장하는 보안 프레임워크임
- **배경/필요성**: SolarWinds와 오픈소스 오염 사례처럼 개발 파이프라인과 의존성 체인이 공격 표면이 되면서 결과물뿐 아니라 생성 과정 자체를 증명하는 체계가 필요해짐

## Ⅱ. 특징

- 소스와 빌드와 provenance를 한 흐름으로 묶어 공급망 보안을 공정 단위로 관리함
- Level 기반 성숙도 체계라 조직이 현재 통제 수준과 목표 수준을 단계적으로 설계하기 좋음
- 빌드 격리와 서명과 검증 정책이 연결되어 배포 전 차단 통제로 쓰기 적합함
- SBOM과 결합하면 무엇이 들어갔는지와 어떻게 만들어졌는지를 함께 검증할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | SLSA | SBOM | SSDF |
|:---|:---|:---|:---|
| 핵심 초점 | 빌드 과정 무결성과 출처 증명 | 구성요소와 버전 목록 | 보안 개발 활동 지침 |
| 주요 산출물 | Level 달성 상태와 provenance | SPDX, CycloneDX 문서 | 개발 통제 절차 |
| 적용 시점 | 소스부터 배포 직전까지 | 빌드와 배포 시점 | 개발 전 주기 |
| 운영 가치 | 변조 방지와 배포 게이트 | 영향 분석과 공급망 가시성 | 보안 프로세스 정립 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Integrity Control | 승인된 변경만 병합되도록 코드 리뷰와 브랜치 보호와 커밋 신뢰를 관리해 공급망 출발점의 오염을 줄이는 통제 계층임 |
| Isolated Build Platform | 재현 가능하고 격리된 빌드 환경을 제공해 임의 스크립트 개입과 빌드 서버 변조 위험을 낮추는 실행 계층임 |
| Provenance Attestation | 어떤 소스와 빌드 환경과 절차로 결과물이 생성되었는지 서명된 메타데이터로 남겨 배포 전 검증 근거를 만드는 증명 계층임 |
| Artifact Signing and Verification | 생성된 산출물과 provenance를 함께 검증해 신뢰되지 않은 결과물이 저장소나 배포 경로에 진입하지 못하게 하는 검문 계층임 |
| Policy Gate | 서비스 중요도별로 요구 SLSA 수준과 예외 조건을 정의해 실제 배포 승인 기준으로 연결하는 운영 통제 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Source Ctrl | -> | Isolated CI | -> | Provenance  | -> | Policy Gate |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 변경 승인    | -> | 격리 빌드    | -> | 출처 증명 생성 | -> | 서명/검증    | -> | 배포 승인    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **변경 승인**: 승인된 소스와 리뷰 이력을 기준으로 빌드 대상을 확정함
2. **격리 빌드**: 재현 가능한 CI 환경에서 빌드를 수행함
3. **출처 증명 생성**: 소스와 빌더와 의존성 정보를 provenance로 기록함
4. **서명 및 검증**: 산출물과 provenance를 서명하고 정책 기준으로 검증함
5. **배포 승인**: 요구 Level을 충족한 결과물만 저장소와 운영 환경으로 이동시킴

## Ⅵ. 문제점 및 해결 방안

1. 문제: 빌드 자동화와 출처 증명이 일부 파이프라인에만 적용되면 공급망 전체 신뢰 수준이 가장 약한 구간에 의해 무너질 수 있음
   - 해결방안: tier based rollout과 mandatory provenance gate를 적용하고 protected pipeline coverage와 unsigned artifact rejection rate로 검증함
2. 문제: 격리되지 않은 빌드 환경에서 공용 비밀값과 임시 스크립트가 섞이면 provenance가 있어도 결과물 무결성을 신뢰하기 어려워짐
   - 해결방안: hermetic build hardening과 ephemeral runner policy를 적용하고 secret exposure incident count와 reproducible build success rate로 검증함
3. 문제: 공급자와 수요자가 요구하는 SLSA 수준이 다르면 조달과 배포 과정에서 보안 기준 충돌이 반복될 수 있음
   - 해결방안: supplier assurance baseline과 criticality based level mapping을 적용하고 vendor compliance alignment rate와 exception approval count로 검증함

## Ⅶ. 적용 사례

- 금융권 DevSecOps 파이프라인이 필수 provenance 검증을 운영하며 확인 지표는 protected pipeline coverage와 unsigned artifact rejection rate임
- 플랫폼 조직이 밀폐형 빌드 러너를 도입하며 확인 지표는 secret exposure incident count와 reproducible build success rate임
- 조달 보안 체계가 서비스 중요도별 SLSA 기준을 적용하며 확인 지표는 vendor compliance alignment rate와 exception approval count임

## Ⅷ. 결론

SLSA는 결과물 보안이 아니라 생성 과정 신뢰를 통제하는 체계이므로 Level 정의와 provenance 검증을 실제 배포 게이트에 연결해야 효과가 남음.
