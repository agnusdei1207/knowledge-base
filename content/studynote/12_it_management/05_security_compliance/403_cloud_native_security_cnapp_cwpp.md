---
title: "403. 클라우드 네이티브 보안 CNAPP CWPP (Cloud Native Security CNAPP CWPP)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CNAPP(Cloud-Native Application Protection Platform)은 CSPM·CWPP·CIEM·CDR을 단일 데이터 그래프(Single Data Graph)로 통합해 IaC부터 런타임 컨테이너·서버리스·PaaS 워크로드까지 "Build -> Deploy -> Operate" 전 사이클의 가시성과 제어를 제공하며, CWPP는 그 중 **워크로드 내부(Host/Container/K8s Node/Serverless Function)** 의 취약점·드리프트·행위기반 위협을 eBPF/런타임 센서로 탐지·차단하는 핵심 계층이다.
> 2. **가치**: 컨테이너 이미지 CVE 평균 1,200건/이미지, K8s API 서버 익스퍼린저 노출 72시간 내 크롤링, 클라우드 자격증명 유출 후 4분 내 자동 암호화폐 채굴기를 배포하는 현실에서, CNAPP 통합 플랫폼은 MTTD(Mean Time To Detect)를 평균 65% 단축하고 MTTR을 40% 절감하며, CWPP 단독으로는 도달 불가능한 **공급망(Supply Chain)·인프라 코드(Terraform/Helm/Kustomize)** 레이어의 시프트-레프트(Shift-Left) 보안을 실현한다.
> 3. **판단 포인트**: **에이전트 vs 에이전트리스**, **SaaS-native vs Self-hosted**, **단일 벤더 통합(예: Prisma Cloud, Wiz) vs Best-of-Breed(CSPM은 Wiz + CWPP는 Aqua)**, 그리고 **SBOM/SLSA Level 3 확보를 위한 CI/CD Hook 위치(사전 이미지 스캔 vs Admission Controller 거부)** 가 핵심 의사결정 트리이며, 멀티클라우드(AWS+Azure+GCP) + 온프레미스 K8s를 동시 운영 시 CNAPP 도입의 ROI가 극대화된다.

---

## Ⅰ. 개요 및 필요성

클라우드 네이티브(Cloud Native)란 CNCF(Cloud Native Computing Foundation)가 정의한 바에 따라 **컨테이너, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infrastructure), 선언형 API(Declarative API)** 를 통해 "느슨하게 결합되고, 탄력적이며, 관리 가능한 관측 가능한 애플리케이션"을 구축하는 접근 방식이다. 이러한 패러다임 전환은 2015년경 Docker/Kubernetes가 보편화되면서 시작되어, 2024년 기준 전 세계 컨테이너화 워크로드의 89%가 Kubernetes 위에서 운영되며, 평균 엔터프라이즈는 1,400개 이상의 컨테이너 이미지(개발·스테이징·운영 합산)를 보유한다.

하지만 이러한 동적·분산 환경은 전통적인 경계 기반 보안(Perimeter Security)을 무력화시켰다. 2023년 IBM X-Force Threat Intelligence Index에 따르면, 클라우드 환경 침해 사고의 **83%가 잘못 구성된 클라우드 설정(Misconfiguration)** 으로 발생하며, Unit 42(Palo Alto Networks)의 2024 Cloud Threat Report는 공격자가 노출된 S3 버킷·잘못 구성된 Kubernetes API 서버·과도한 권한의 서비스 어카운트(Service Account) 자격증명을 발견 후 **평균 4분 이내**에 암호화폐 채굴기 또는 랜섬웨어를 배포한다고 경고한다. GitGuardian의 2023 State of Secrets Sprawl Report는 공개 GitHub 저장소에서 **1,000만 건 이상의 클라우드 자격증명(API Key, Token, Access Key)** 이 유출되었음을 확인했다.

**기존 보안 체계의 한계**는 명확하다. 전통적인 CSPM(Cloud Security Posture Management)은 클라우드 제어판(Control Plane) — 예: AWS IAM, Security Group, S3 Bucket Policy — 만 점검하며 워크로드 내부의 프로세스·네트워크 콜·파일 시스템 이벤트는 보지 못한다. 반대로传统的 EDR(Endpoint Detection & Response)은 물리적/가상 머신의 행위 기반 탐지에 특화되어 있어, 12초 수명의 컨테이너, eBPF 기반 시스템 콜, Serverless Function의 콜드 스타트 환경에서는 무용지물이다. 또한 **수천 개의 IaC(Infrastructure as Code) 템플릿**과 **수만 개의 컨테이너 이미지 레이어**를 사람이 수동으로 검토하는 것은 불가능에 가깝다.

CNAPP는 이러한 **사일로(Silo)화된 보안 도구의 통합**을 통해, 코드 작성 시점(Pre-commit/IDE/CI)부터 런타임까지 일관된 보안 정책과 가시성을 제공하기 위해 등장했으며, 2021년 Gartner가 처음 명명하여 2024년 8월 기준 CNAPP 시장이 **연평균 24.7% 성장하여 2028년 125억 달러 규모**에 이를 것으로 전망된다.

```text
+-----------------------------------------------------------------------------+
|              클라우드 네이티브 환경의 공격 표면(Attack Surface)             |
+-----------------------------------------------------------------------------+
|                                                                             |
|   +--------------+    +--------------+    +--------------+                  |
|   |  Source Code |---->|  CI/CD Pipe  |---->|   Registry   |                  |
|   |  (Git Repo)  |    |  (Jenkins,   |    |  (Harbor,    |                  |
|   |  + Secrets   |    |   GitLab,    |    |   ECR, ACR)  |                  |
|   +--------------+    |   ArgoCD)    |    +--------------+                  |
|         |             +--------------+            |                         |
|         |   IaC Scan       |  Image Scan          | Admission Ctrl          |
|         v                  v                      v                         |
|   +----------------------------------------------------------+              |
|   |              Kubernetes Cluster (Runtime)                |              |
|   |   +----------+  +----------+  +----------+              |              |
|   |   |   Pod    |  |   Pod    |  |   Pod    |   eBPF 런타임  |              |
|   |   |  /app1   |  |  /app2   |  |  /app3   |   센서 계층    |              |
|   |   +----------+  +----------+  +----------+              |              |
|   |         |             |             |                    |              |
|   |         +-------------+-------------+                    |              |
|   |                       | eBPF Syscall Tracing            |              |
|   |                       v                                  |              |
|   |              +------------------+                        |              |
|   |              |  CNAPP Control   |  <--- CSPM/CIEM/CDR    |              |
|   |              |     Plane        |      통합 분석 엔진     |              |
|   |              +------------------+                        |              |
|   +----------------------------------------------------------+              |
|                                                                             |
|   [위험 지점]                                                               |
|   1. 코드 내 하드코딩된 AWS_ACCESS_KEY_ID -> 유출 시 4분 내 오용              |
|   2. CVE-2024-21626 (runc) -> 컨테이너 탈출로 호스트 권한 획득               |
|   3. K8s RBAC 와일드카드(*) 권한 -> 클러스터 전체 장악                        |
|   4. 공개 S3 버킷 + 익명 READ -> 데이터 유출                                 |
|   5. Supply Chain 공격 (예: 3월 2024 XZ Utils 백도어) -> 빌드 시 침투         |
+-----------------------------------------------------------------------------+
```

기존 패러다임 대비 CNAPP/CWPP가 등장한 배경은 세 가지 패러다임 전환으로 요약된다. 첫째, **"인프라 -> 코드"** 로의 전환: 클라우드 자원이 수동 클릭이 아닌 Terraform/CloudFormation/Pulumi 같은 선언적 코드로 정의됨에 따라 보안 점검이 IaC 스캔(Terraform Plan 단계, Checkov/Tfsec/Trivy 통합)으로 자동화되어야 한다. 둘째, **"장기 운영 VM -> 단기 수명 컨테이너"** 로의 전환: 컨테이너의 평균 수명(Median Lifetime)이 5~12초에 불과하여, IP 기반 화이트리스팅·파일 해시 기반 평판 시스템·행위 기반 머신러닝이 필수적이다. 셋째, **"수동 사고 대응 -> 자동화된 방어"** 로의 전환: 4분 내 발생하는 자동화 공격에 대응하기 위해, Admission Controller(Kyverno/OPA Gatekeeper) 기반 정책 차단, Service Mesh(Istio/Linkerd) 기반 mTLS 강제, GitOps 기반 자동 롤백이 요구된다.

- **📢 섹션 요약 비유**: 클라우드 네이티브 환경을 **"끊임없이 움직이는 컨베이어 벨트 위의 도시"** 에 비유할 수 있다. 전통 보안은 성벽과 문지기였다면, CNAPP/CWPP는 도시의 모든 도로·건물·시민의 실시간 CCTV, 출입 명부, 위조 지폐 감별기, 그리고 범죄자 행동을 학습한 AI 경찰이 통합된 **"스마트 시티 보안관제 시스템"** 이다. 컨베이어 벨트(컨테이너)는 5초마다 새 택배를 가져오고, 일부는 위험물(SQL Injection, 악성코드), 일부는 훼손된 포장(취약한 라이브러리), 일부는 위조 송장(잘못된 클라우드 설정)을 가지고 오기 때문에, 그 흐름 자체를 실시간으로 감시해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CNAPP는 Gartner가 정의한 바에 따라 **4개의 핵심 모듈과 2개의 부가 모듈**로 구성된다. **CSPM**(Cloud Security Posture Management, 클라우드 설정 오류 점검), **CWPP**(Cloud Workload Protection Platform, 워크로드 런타임 보호), **CIEM**(Cloud Infrastructure Entitlement Management, 클라우드 권한/자격증명 관리), **CDR**(Cloud Detection & Response, 클라우드 행위 기반 탐지·대응)이 4대 핵심이며, 여기에 **ASPM**(Application Security Posture Management, 애플리케이션 보안 관리)과 **IaC Scanning**이 부가적으로 통합된다. 이 모든 모듈이 **단일 데이터 그래프(Single Data Graph)** — 노드(클라우드 자산·사용자·워크로드)와 엣지(관계·의존성·네트워크 경로)로 구성된 그래프 데이터베이스 — 를 공유하여, **"이 S3 버킷은 누구의 것 -> 어떤 서비스가 접근 -> 어떤 컨테이너에서 실행 -> 어떤 이미지로 빌드 -> 어떤 IaC에서 정의"** 라는 단방향 추적(Lineage Tracking)을 가능케 한다.

CWPP는 Gartner의 7계층 모델(2019년 정의, 2023년 개정)에 따라 진화해왔다. 1계층은 **하드웨어/물리 자산**이며, 2계층은 **호스트 기반** (OS·하이퍼바이저·워크로드 런타임), 3계층은 **컨테이너·이미지**, 4계층은 **Kubernetes 워크로드**, 5계층은 **사용자 애플리케이션 코드**, 6계층은 **API·서비스 메시·서비스 간 통신**, 7계층은 **데이터·스토리지**이다. 현대 CWPP는 최소 2~4계층을 모두 커버하며, eBPF(Extended Berkeley Packet Filter) 커널 훅을 통해 **컨텍스트 인지 런타임 보호**를 구현한다.

```text
+-----------------------------------------------------------------------------+
|            CNAPP 통합 아키텍처 (Single Data Graph 관점)                     |
+-----------------------------------------------------------------------------+
|                                                                             |
|  +-----------------  Pre-Deployment (Shift-Left)  -----------------+        |
|  |                                                                 |        |
|  |   [IDE]      [Git Commit]   [CI Build]      [Registry Push]    |        |
|  |     |             |              |                 |            |        |
|  |     v             v              v                 v            |        |
|  |  +------+   +----------+   +----------+    +----------+        |        |
|  |  |Secret|   | IaC Scan |   |SCA + SBOM|    |Image Scan|        |        |
|  |  |Detect|   |(Checkov, |   |(Syft,    |    |(Trivy,   |        |        |
|  |  |(Gitle)|   | Tfsec,   |   | CycloneDX|    | Clair,   |        |        |
|  |  |ask)  |   | KICS)    |   | SPDX)    |    | Grype)   |        |        |
|  |  +------+   +----------+   +----------+    +----------+        |        |
|  |      |            |              |               |              |        |
|  |      +------------+--------------+---------------+              |        |
|  |                              v                                  |        |
|  |                  +--------------------+                         |        |
|  |                  | Policy Engine (OPA)|                         |        |
|  |                  |  + SLSA L3 검증    |                         |        |
|  |                  +--------------------+                         |        |
|  +-----------------------------------------------------------------+        |
|                                  |                                          |
|                                  v   Admission Controller Hook              |
|  +-----------------  Runtime (CWPP 핵심 영역)  --------------------+        |
|  |                                                                  |        |
|  |   +------------------------------------------------------+      |        |
|  |   |             Kubernetes Control Plane                 |      |        |
|  |   |   [API Server] [etcd] [Scheduler] [Controller Mgr]   |      |        |
|  |   |              ^                                        |      |        |
|  |   |              | Audit Log + CIS Bench 검증            |      |        |
|  |   |              v                                        |      |        |
|  |   |   +------------------------------+                   |      |        |
|  |   |   |  Admission Controller        |                   |      |        |
|  |   |   |  (OPA Gatekeeper / Kyverno / |                   |      |        |
|  |   |   |   ValidatingAdmissionPolicy) |                   |      |        |
|  |   +------------------------------+                   |      |        |
|  |              |  Pod 생성 요청 검증                       |      |        |
|  |              v                                          |      |        |
|  |   +------------------------------------------------------+   |      |
|  |   |              Worker Node (K8s Node)                   |   |      |
|  |   |  +---------+ +---------+ +---------+                  |   |      |
|  |   |  | Pod A   | | Pod B   | | Pod C   |                  |   |      |
|  |   |  | +-----+ | | +-----+ | | +-----+ |                  |   |      |
|  |   |  | |App  | | | |App  | | | |App  | |                  |   |      |
|  |   |  | +-----+ | | +-----+ | | +-----+ |                  |   |      |
|  |   |  |  +-----+| |  +-----+| |  +-----+| <-- Sidecar       |   |      |
|  |   |  |  |Side-|| |  |Side-|| |  |Side-||    (eBPF)         |   |      |
|  |   |  |  |car  || |  |car  || |  |car  ||                  |   |      |
|  |   |  |  +-----+| |  +-----+| |  +-----+|                  |   |      |
|  |   |  +---------+ +---------+ +---------+                  |   |      |
|  |   |       |            |            |                       |   |      |
|  |   |       +------------+------------+                       |   |      |
|  |   |                    | eBPF Tracepoint /
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 403 / 800

<- **이전**: [402. DevSecOps 보안 내재화 파이프라인](/studynote/12_it_management/05_security_compliance/402_devsecops_security_integration_pipeline/)
**다음**: [404. API 보안 OAuth JWT 토큰 관리](/studynote/12_it_management/05_security_compliance/404_api_security_oauth_jwt_token_management/) ->

---
