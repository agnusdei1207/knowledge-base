---
title: "불변 인프라 (Immutable Infrastructure)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 219
---

# 📖 【암기용】 개념 완전 이해

> 목적: 불변 인프라를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 운영 중인 서버를 수정하지 않고 새 이미지·새 인스턴스로 교체하는 인프라 운영 방식
- **왜 필요한가**: 운영 서버에 직접 패치하면 환경 차이, 구성 편류, 재현 불가 장애가 발생함
- **핵심 직관**: 고장 난 부품을 현장에서 수리하지 않고 검증된 새 부품으로 통째 교체하는 방식임

## 깊이 이해
- **배경·문제의식**: 전통 서버 운영은 SSH 접속, 수동 패치, 설정 변경이 누적되어 dev/stage/prod 차이를 만든다. 장애 분석 시 "무엇이 바뀌었는지" 추적이 어렵다.
- **작동 원리**: 애플리케이션과 런타임을 이미지로 빌드하고, 배포 시 기존 인스턴스를 변경하지 않는다. 새 버전을 검증한 뒤 트래픽을 전환하고 기존 버전은 폐기한다.
- **비유**: 식당 메뉴판을 손으로 계속 고치는 대신 새로 인쇄한 메뉴판을 검수 후 교체하는 방식임
- **구체 예시**: AMI 또는 컨테이너 이미지를 SHA256 digest로 고정하고, blue-green 배포로 5분 내 rollback 가능하게 구성한다.
- **흔한 오해·주의점**: 불변 인프라는 백업을 하지 않는다는 뜻이 아니다. 상태 데이터는 DB·Object Storage·Volume으로 분리하고 인스턴스는 언제든 폐기 가능하게 만든다.

## 연결 개념
- IaC - 인프라 상태를 코드로 선언
- Blue-Green Deployment - 새 인프라로 트래픽 전환
- Container Image - 불변 배포 단위

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 불변 인프라는 서버 운영 방식 변화이며, 이미지 검증·상태 분리·교체 배포·rollback 지표가 답안 핵심이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Immutable Infrastructure는 운영 서버를 직접 변경하지 않고 검증된 새 아티팩트로 교체하는 배포·운영 모델이다.
> 2. **가치**: 구성 편류, 수동 변경, 재현 불가 장애를 줄이고 배포와 rollback을 표준 절차로 만든다.
> 3. **판단 포인트**: 상태 분리, 이미지 서명, 취약점 스캔, blue-green/canary 전환, drift 탐지가 함께 필요하다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 운영 모델 이해 확인 | mutable vs immutable, image, replacement, drift | 단순 컨테이너 사용으로만 설명 |
| 배포·복구 판단 확인 | blue-green, canary, rollback, 상태 분리 | DB schema와 persistent data 분리 누락 |
| 보안·감사 통제 확인 | image signing, SBOM, CVE scan, change audit | SSH 금지와 예외 접근 통제 누락 |

> 요약: 불변 인프라는 직접 수정 금지 원칙을 이미지·배포·감사 체계로 구현하는 운영 패턴이다.

---

## Ⅰ. 개요 및 필요성

불변 인프라는 운영 서버를 수정하지 않는 배포 모델이다. 서버 내 수동 변경은 구성 편류와 재현 불가 장애를 만든다. 이미지 기반 교체, 상태 분리, 자동 rollback을 통해 변경을 추적 가능한 단위로 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> Build Pipeline -> Immutable Image
-> Security Scan/Sign -> Provision New Instance
-> Traffic Switch -> Old Instance Terminate
State Data -> DB/Object Storage/Volume
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Immutable Image | 애플리케이션·런타임 포함 배포 단위 | AMI, OCI image, VM template |
| Provisioner | 새 인프라 생성 | Terraform, Packer, Kubernetes |
| Traffic Switch | 새 버전으로 요청 전환 | blue-green, canary, weighted routing |
| State Store | 상태 데이터 외부화 | DB, S3, PVC, managed service |

> 요약: 불변 인프라는 이미지, 프로비저닝, 트래픽 전환, 상태 분리로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Change Commit -> Build Image -> Test/Scan/Sign
-> Create New Runtime -> Health Check
-> Shift Traffic -> Monitor SLO -> Terminate Old Runtime
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 코드와 설정을 이미지로 빌드 | digest 고정, SBOM 생성 |
| 2 | 테스트·CVE 스캔·서명 | critical CVE 0건 |
| 3 | 새 인프라 생성과 health check | readiness 100%, p95 기준 충족 |
| 4 | 트래픽 전환과 구버전 폐기 | rollback 5분 이내 |

> 요약: 운영 변경은 빌드된 아티팩트를 검증하고 새 런타임으로 교체하는 단일 흐름으로 통제된다.

---

## Ⅳ. 특징

| 구분 | Mutable Infrastructure | Immutable Infrastructure | 판단 수치 |
|:---|:---|:---|:---|
| 변경 방식 | 운영 서버 직접 수정 | 새 이미지·인스턴스 교체 | SSH 변경 0건 목표 |
| 재현성 | 서버별 상태 차이 가능 | image digest로 동일 환경 | drift 0건 |
| 복구 | 현장 수정·수동 복원 | 이전 이미지로 rollback | rollback 5분 이내 |
| 보안 | 수동 패치 이력 분산 | scan/sign/audit 중앙화 | critical CVE 0건 |

> 요약: 불변 인프라는 직접 수정 대신 검증된 교체를 통해 재현성과 감사성을 확보한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Immutable Infrastructure | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 장기 운영 서버 | 폐기 가능한 runtime | auto scaling, container 환경 |
| 비용/성능 | 현장 패치 시간 | 빌드·배포 pipeline 시간 | 배포 10분 이하, rollback 5분 이하 |
| 운영/위험 | 구성 편류 | 이미지 공급망 리스크 | signing, SBOM, registry ACL |

> 요약: 배포 빈도와 환경 재현성이 요구될수록 불변 인프라가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 상태 손실 | 로컬 디스크 저장 | 상태 외부화, backup policy | local write audit 0건 |
| 이미지 취약점 | base image CVE | Trivy/Grype scan, patch rebuild | critical CVE 0건 |
| 교체 실패 | health check 부족 | canary, readiness, automatic rollback | failed rollout rate |

> 요약: 상태 분리, 이미지 보안, rollout 검증이 불변 인프라의 주요 통제이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 변경 통제 | SSH 직접 변경 0건 | IAM log, session manager |
| 배포 복구 | rollback 5분 이내 | CI/CD metric |
| 구성 편류 | drift 0건 | Terraform plan, config scanner |

> 요약: 직접 변경, rollback 시간, drift 건수로 운영 성숙도를 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Packer/OCI image로 런타임을 고정하고 digest, SBOM, cosign 서명을 배포 승인 조건으로 설정
2. Terraform/Kubernetes로 새 인프라를 생성한 뒤 blue-green 또는 canary 5% 트래픽부터 SLO 확인
3. 상태는 RDS, Object Storage, PVC로 분리하고 운영 서버 SSH는 break-glass 승인과 1시간 만료로 제한

**결론 (2줄):**
- 기술사 판단: 배포 빈도 주 1회 이상 또는 운영 편류가 반복되면 불변 인프라, 레거시 장비는 변경 동결·자동화부터 적용
- 향후 방향: GitOps, image signing, policy-as-code와 결합해 공급망 보안까지 포함한 운영 모델로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "불변 인프라를 설명하시오" | 이미지 빌드와 교체 배포 흐름 | mutable 대비 특징 |
| 요구사항 명시형 | "배포 안정화 방안을 제시하시오" | scan, sign, canary, rollback 절차 | drift·SSH·CVE 지표 |

> 요약: 설명형은 운영 모델 차이, 방안형은 배포·보안·복구 통제를 중심으로 전환한다.
