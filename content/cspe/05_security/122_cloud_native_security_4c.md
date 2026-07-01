---
title: "클라우드 네이티브 보안 4C (Cloud Native Security 4C)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 122
---
# 📖 【암기용】 개념 완전 이해

> 목적: 클라우드 네이티브 보안 4C를 처음 보는 사람도 계층형 방어 구조를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.
## 한눈에
- **개요**: 4C는 Cloud, Cluster, Container, Code 네 계층으로 클라우드 네이티브 보안을 나누는 모델임
- **왜 필요한가**: Kubernetes 보안 사고는 애플리케이션 취약점 하나로 끝나지 않는다. 클라우드 IAM, 클러스터 RBAC, 컨테이너 이미지, 코드 취약점이 연결되면 권한 상승과 데이터 접근으로 이어진다.
- **핵심 직관**: 건물 부지, 출입 게이트, 사무실 금고, 문서 내용처럼 바깥 계층부터 안쪽 계층까지 각각 잠금장치가 필요하다는 의미임
## 깊이 이해
- **배경·문제의식**: 컨테이너는 배포 단위를 작게 만들지만 공격면도 나눈다. 취약한 코드가 컨테이너 탈출, ServiceAccount 토큰 탈취, 클라우드 메타데이터 접근으로 이어질 수 있어 한 계층 통제만으로 사고를 제한하기 어렵다.
- **작동 원리**: Cloud 계층은 IAM, VPC, KMS, 감사로그를 통제한다. Cluster 계층은 API Server, RBAC, Admission, NetworkPolicy를 관리한다. Container 계층은 이미지 서명, 취약점 스캔, Runtime Policy를 적용한다. Code 계층은 SAST, SCA, Secret Scan, Secure Coding으로 결함을 줄인다.
- **비유**: 창고 보안에서 부지 울타리, 출입 게이트, 보관함 잠금, 물품 라벨을 각각 관리하는 것과 같음. 물품 라벨만 정확해도 울타리가 열려 있으면 절도 가능성이 남는다.
- **구체 예시**: 취약한 Log4j 패키지가 Code 계층에서 탐지되지 않고, root 컨테이너 실행, ClusterRole 과다 권한, S3 읽기 권한까지 연결되면 원격 코드 실행이 클라우드 데이터 유출로 확장됨
- **흔한 오해·주의점**: 4C는 보안 제품 목록이 아니다. 계층별 공격면과 통제를 빠뜨리지 않도록 답안 구조를 잡는 기준임

## 연결 개념
- Defense in Depth — 계층별 통제 중복으로 단일 실패 지점 축소
- Kubernetes RBAC/Admission Control — Cluster 계층의 핵심 통제
- CNAPP — CSPM, CWPP, CIEM, IaC Scan을 4C 전반에 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 4C는 "클라우드 보안 계층"을 나열하는 답안이 아니라, 각 계층의 공격면·통제·검증 지표를 연결해 방어 공백을 줄이는 모델로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 보안 4C는 Cloud, Cluster, Container, Code 계층별 공격면과 통제 항목을 분리해 설계하는 계층형 보안 모델이다.
> 2. **가치**: 코드 취약점, 이미지 취약점, 클러스터 권한, 클라우드 IAM을 한 사고 경로로 보고 통제 누락 지점을 찾는다.
> 3. **판단 포인트**: 각 계층에 예방, 탐지, 대응 지표를 배치하고 API Server, RBAC, 이미지 서명, SCA, 감사로그를 빠뜨리지 않아야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 클라우드 네이티브 공격면 이해 확인 | Cloud, Cluster, Container, Code 4계층과 상호 의존 | 컨테이너 보안만 설명 |
| Kubernetes 보안 설계 역량 확인 | RBAC, Admission, NetworkPolicy, Pod Security, 감사로그 | 쿠버네티스 구성요소 나열 후 통제 기준 누락 |
| DevSecOps 적용 판단 확인 | SAST, SCA, 이미지 스캔, IaC, 런타임 탐지 | 개발 단계와 운영 단계를 분리해 단절 |

> 요약: 4C 답안은 계층별 통제 항목과 사고 경로를 연결해 보안 공백을 식별하는 구조여야 한다.

---

## Ⅰ. 개요 및 필요성

4C는 클라우드 네이티브 계층형 보안 모델이다.
Kubernetes 환경은 클라우드 IAM, 클러스터 제어면, 컨테이너 이미지, 애플리케이션 코드가 연결됨.
한 계층의 통제 누락이 다른 계층 권한 상승으로 확장되므로 계층별 예방·탐지·대응 설계가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Cloud -> Cluster -> Container -> Code
  / IAM, Network, KMS, Audit
  / API Server, RBAC, Admission, NetworkPolicy
  / Image, Runtime, Registry, Secrets
  / SAST, SCA, Secret Scan, Secure Coding
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Cloud | 계정, 네트워크, KMS, 로깅 기반 통제 | IAM 최소 권한, VPC, CloudTrail |
| Cluster | Kubernetes 제어면과 리소스 정책 통제 | RBAC, Admission, Pod Security |
| Container | 이미지, 레지스트리, 런타임 실행 통제 | SBOM, 서명, rootless, seccomp |
| Code | 애플리케이션 결함과 의존성 위험 축소 | SAST, SCA, Secret Scan |
| Governance | 정책, 예외, 증거, SLA 관리 | CIS Benchmark, NIST 800-190 매핑 |

> 요약: 4C는 Cloud에서 Code까지 계층별 공격면을 구분하고 각 계층에 기술 통제와 운영 증거를 배치한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 식별 -> 4C 계층 매핑 -> 계층별 통제 적용
-> CI/CD 검증 -> Admission 차단 -> Runtime 탐지
-> 로그 수집/티켓 조치 -> 지표 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 워크로드와 데이터 민감도 식별 | 개인정보·결제정보 등급 태깅 |
| 2 | Cloud/Cluster/Container/Code 통제 매핑 | 계층별 필수 통제 1개 이상 |
| 3 | CI/CD에서 SAST·SCA·이미지 스캔 수행 | Critical CVE 0건, Secret 0건 |
| 4 | Admission에서 권한·이미지·Pod 정책 검사 | Privileged Pod 0건, root 실행 0건 |
| 5 | Runtime 이벤트와 클라우드 로그 분석 | Falco 경보, API Audit Log, SIEM 연동 |

> 요약: 4C는 개발 단계 검증, 배포 시 차단, 실행 중 탐지를 이어 계층별 통제 공백을 줄인다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 4C 모델 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 범위 | 컨테이너 이미지 스캔 중심 | Cloud부터 Code까지 계층화 | 4계층 통제 커버리지 100% |
| 책임 | 보안팀 사후 점검 | Dev, Platform, SecOps 공동 책임 | Pull Request·Admission·Runtime 단계 분리 |
| 통제 시점 | 운영 배포 후 탐지 | Build, Deploy, Run 전 과정 | Critical CVE 배포 차단 0건 유지 |
| 한계 | 계층 간 증거 단절 | CNAPP·SIEM 연동 필요 | 예외 만료 30일, 감사로그 1년 보관 |

> 요약: 4C는 단일 도구가 아니라 빌드부터 런타임까지 계층별 통제 책임과 지표를 나누는 설계 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 4C 모델 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 이미지 취약점 스캔 단독 | Cloud/Cluster/Container/Code 방어 계층 | Kubernetes 운영 클러스터 3개 이상 |
| 비용/성능 | 점검 도구별 개별 운영 | CI/CD, Admission, Runtime 통합 | 배포 차단 기준과 예외 SLA 필요 시 |
| 운영/위험 | 사후 취약점 조치 | 사전 차단+실행 탐지+감사 증거 | 규제 워크로드, 멀티테넌트 클러스터 |

> 요약: 운영 클러스터와 규제 워크로드가 늘어나면 이미지 스캔 단독보다 4C 기반 통제 매핑이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 계층 공백 | Code만 검사하고 Cloud IAM 누락 | 4C 체크리스트와 소유자 지정 | 계층별 미할당 통제 0건 |
| 권한 상승 | 과도 RBAC, ServiceAccount 토큰 노출 | 최소 권한, 토큰 자동 마운트 제한 | ClusterRoleBinding 예외 0건 |
| 취약 이미지 배포 | Registry 스캔·서명 누락 | Trivy, Cosign, Admission 차단 | Critical CVE 이미지 0건 |
| 런타임 미탐지 | 빌드 시점 점검에 의존 | Falco, Audit Log, SIEM 룰 | 미분류 경보 24시간 내 triage |

> 요약: 4C 운영 리스크는 계층 공백과 권한 상승이며 소유자·정책·런타임 탐지 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Cloud 통제 | Root Key 0건, KMS 100%, 감사로그 1년 | CSPM, CloudTrail, IAM Access Analyzer |
| Cluster 통제 | Privileged Pod 0건, RBAC 예외 30일 만료 | OPA Gatekeeper, kube-apiserver audit |
| Container 통제 | Critical CVE 0건, 이미지 서명 100% | Trivy, SBOM, Cosign 검증 |
| Code 통제 | Secret 0건, SCA Critical 0건 | SAST, SCA, Secret Scan |

> 요약: 4C 도입 효과는 계층별 금지 기준 0건과 서명·암호화·로그 보관률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 1단계: Cloud 계층에서 IAM 최소 권한, VPC 분리, KMS 암호화 100%, 감사로그 1년 보관 기준 수립
2. 2단계: Cluster 계층에서 RBAC 검토, Pod Security Standard, NetworkPolicy, OPA Gatekeeper로 Privileged Pod 0건 유지
3. 3단계: Container/Code 계층에서 Trivy Critical CVE 0건, Cosign 서명 100%, SAST·SCA·Secret Scan을 Pull Request에 배치

**결론 (2줄):**
- 기술사 판단: 단일 서비스 소규모 환경은 이미지 스캔과 RBAC로 시작하고, 멀티클러스터·규제 워크로드는 4C 기반 통합 통제가 필요함
- 향후 방향: CNAPP, SBOM, eBPF 런타임 탐지, Policy as Code를 결합해 계층별 통제 증거를 자동 수집해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "클라우드 네이티브 보안 4C를 설명하시오" | 4계층 통제 흐름과 CI/CD·Admission·Runtime 연결 | 계층별 책임과 방어 심층 구조 |
| 요구사항 명시형 | "Kubernetes 보안 설계 방안을 제시하시오", "컨테이너 보안과 비교하시오" | 요구 계층별 통제 매핑과 배포 차단 기준 | RBAC, 이미지 서명, CVE 0건, 런타임 탐지 방안 |

> 요약: 설명형은 4계층 모델을 넓게 쓰고, 설계형은 Cloud부터 Code까지 통제 기준과 지표를 배치한다.
