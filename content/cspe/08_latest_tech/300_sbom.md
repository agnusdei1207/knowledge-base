---
title: "SBOM 소프트웨어 자재명세서 (Software Bill of Materials)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 300
extra:
  question_no: "300"
  exam_status: "기출"
  exam_history: "134회, 135회"
---

## 미리 알고가기

- SBOM은 소프트웨어를 구성하는 라이브러리와 패키지와 버전과 관계를 목록화한 명세서임
- 공급망 보안과 취약점 대응 속도를 높이는 핵심 기본 자산으로 쓰임
- 목록만 만드는 것으로 끝나지 않고 지속 갱신과 배포 파이프라인 연계가 중요함

## Ⅰ. 개요

- **정의/개념**: SBOM은 소프트웨어를 구성하는 오픈소스와 라이브러리와 모듈과 버전과 의존 관계를 구조적으로 기록해 공급망 보안과 취약점 영향을 추적하게 하는 자재 명세서임
- **배경/필요성**: 공급망 공격과 오픈소스 취약점이 급증하면서 조직은 어떤 소프트웨어에 어떤 구성요소가 포함되어 있는지 빠르게 파악할 수 있는 표준 목록이 필요해짐

## Ⅱ. 특징

- 구성 요소와 버전과 출처를 가시화해 영향 분석을 빠르게 함
- 취약점 공지 발생 시 영향을 받은 시스템을 신속히 찾을 수 있음
- 규제 준수와 고객 신뢰 확보에 도움이 됨
- 정적 목록만 유지하면 실제 배포 상태와 괴리가 생길 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | SBOM | Asset Inventory | Vulnerability Report |
|:---|:---|:---|:---|
| 초점 | 구성요소 목록과 관계 | 자산 식별 | 취약점 결과 |
| 활용 목적 | 영향 추적과 공급망 가시화 | 자산 관리 | 조치 우선순위 |
| 갱신 기준 | 빌드와 배포 시점 | 자산 변경 시점 | 스캔 시점 |
| 핵심 가치 | 구성 요소 투명성 | 소유 자산 파악 | 노출 상태 파악 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Component List | 패키지와 라이브러리와 모듈 이름과 버전을 기록해 소프트웨어 구성의 기본 재료를 보여주는 목록임 |
| Dependency Relationship | 직접 의존성과 전이 의존성을 표현해 취약점 영향 범위를 추적하게 하는 관계 정보임 |
| Source and License Metadata | 공급자와 저장소와 라이선스 정보를 포함해 법적과 공급망 검토를 가능하게 하는 메타데이터임 |
| Build Artifact Link | 어떤 빌드 결과물과 배포 이미지에 이 SBOM이 연결되는지 추적하는 배포 연계 정보임 |
| Verification Workflow | SBOM 생성과 서명과 배포 후 검증을 수행해 명세서 신뢰성을 유지하는 운영 계층임 |

```text
+---------------+    +------------------+    +------------------+
| Components    | -> | Dependencies     | -> | Build Artifact   |
+---------------+    +------------------+    +------------------+
         \__________________________________________/
                    Verification / Metadata
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 빌드 분석    | -> | 구성요소 추출 | -> | 관계 정리    | -> | SBOM 생성    | -> | 배포/검증 연계 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **빌드 분석**: 소스와 패키지 의존성을 스캔함
2. **구성요소 추출**: 이름과 버전과 공급 정보를 수집함
3. **관계 정리**: 직접 의존성과 전이 의존성을 연결함
4. **SBOM 생성**: 표준 형식의 명세서를 만든다
5. **배포와 검증 연계**: 배포 산출물과 연결하고 검증함

## Ⅵ. 문제점 및 해결 방안

1. 문제: SBOM이 빌드 시점 한 번만 생성되고 갱신되지 않으면 실제 운영 산출물과 목록이 어긋날 수 있음
   - 해결방안: pipeline embedded generation과 deployment linkage verification을 적용하고 SBOM freshness score와 artifact match rate로 검증함
2. 문제: 전이 의존성과 런타임 포함 모듈이 누락되면 취약점 영향 분석이 불완전해질 수 있음
   - 해결방안: transitive dependency resolution과 runtime package discovery를 적용하고 dependency completeness rate와 missed vulnerable component count로 검증함
3. 문제: SBOM만 생성하고 취약점 관리와 조달 프로세스에 연결하지 않으면 실질 보안 효과가 제한될 수 있음
   - 해결방안: vulnerability management integration과 supplier review workflow를 적용하고 vulnerability impact triage time와 supplier transparency coverage로 검증함

## Ⅶ. 적용 사례

- CI CD 파이프라인이 SBOM 자동 생성을 운영하며 확인 지표는 SBOM freshness score와 artifact match rate임
- 공급망 보안팀이 전이 의존성 해석을 강화하며 확인 지표는 dependency completeness rate와 missed vulnerable component count임
- 조달과 보안 조직이 취약점 연계 프로세스를 운영하며 확인 지표는 vulnerability impact triage time와 supplier transparency coverage임

## Ⅷ. 결론

SBOM은 공급망 보안의 출발점이므로 목록 생성보다 배포 연계와 완전성 관리와 취약점 대응 연결이 함께 이루어져야 함.
