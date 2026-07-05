---
title: "깃옵스 (GitOps)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 61
---

## 핵심 인사이트 (3줄 요약)
- 인프라와 애플리케이션의 '원하는 상태(Desired State)'를 Git 저장소에 선언적으로 저장하고, 이를 단일 진실 공급원(SSOT)으로 삼는 운영 철학.
- K8s 클러스터 내에 떠 있는 에이전트(ArgoCD 등)가 Git을 계속 감시(Pull)하다가, 변경 사항이 생기면 클러스터 상태를 Git과 똑같이 동기화(Sync)함.
- 기존 CI 서버가 외부에서 K8s에 직접 배포하던 Push 방식의 보안 위험을 제거하고, 롤백(Rollback)을 단순히 Git Commit 복원(Revert)으로 해결하는 차세대 CD 표준.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | Weaveworks에서 2017년에 창안한 개념으로, Kubernetes 환경에 최적화된 지속적 배포(CD) 및 인프라 관리 방법론 | "자동 배송 시스템" |
| **필요성** | 기존에는 Jenkins(CI 서버)가 클러스터의 관리자 권한(Kubeconfig)을 통째로 들고 밖에서 안으로 밀어 넣는(Push) 방식이... | "자동 품질 검사 라인" |
| **Push vs Pull 방식** | - **기존 (CIOps / Push)**: CI 서버 ➡️ `kubectl apply` ➡️ K8s 클러스터 | "자동 품질 검사 라인" |
| **GitOps (Pull)** | K8s 내부의 Controller(ArgoCD) ➡️ Git 저장소를 주기적으로 `git pull` ➡️ 상태 동기화 | "자동 배송 시스템" |
| **선언적 인프라** | YAML 파일로 "어떤 상태가 되어야 하는지"만 Git에 명시하면, GitOps 에이전트가 알아서 그 상태를 만듦 | "경험으로 배우는 프로그램" |
| **App Repo와 Config Repo의 분리** | 실무에서는 소스코드가 있는 Git(App Repo)과 K8s 배포 YAML이 있는 Git(Config Repo)을 반드시 분리해야 함 | "경험으로 배우는 프로그램" |
| **깃옵스** | 깃옵스 (GitOps)의 핵심 개념 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성
- **개요**: Weaveworks에서 2017년에 창안한 개념으로, Kubernetes 환경에 최적화된 지속적 배포(CD) 및 인프라 관리 방법론.
- **필요성**: 기존에는 Jenkins(CI 서버)가 클러스터의 관리자 권한(Kubeconfig)을 통째로 들고 밖에서 안으로 밀어 넣는(Push) 방식이라 보안에 취약했음. 또한 누군가 수동으로 서버 설정을 바꾸면, 코드 저장소와 실제 서버 상태가 달라지는 '구성 표류(Configuration Drift)'가 발생해 장애 추적이 불가능했음.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **Push vs Pull 방식**:
  - **기존 (CIOps / Push)**: CI 서버 ➡️ `kubectl apply` ➡️ K8s 클러스터
  - **GitOps (Pull)**: K8s 내부의 Controller(ArgoCD) ➡️ Git 저장소를 주기적으로 `git pull` ➡️ 상태 동기화.
- **선언적 인프라**: YAML 파일로 "어떤 상태가 되어야 하는지"만 Git에 명시하면, GitOps 에이전트가 알아서 그 상태를 만듦.

```text
[ GitOps 아키텍처 (Pull 모델) ]

 [ 개발자/운영자 ] 
      ⬇️ (1. YAML 수정 후 PR & Merge)
 [ Config Git Repository ] ⬅️ ⬅️ ⬅️ ⬅️ ⬅️ ⬅️ ⬅️ (2. Git 저장소 감시 / Pull)
 (Single Source of Truth)                       | 
                                                |
 ----------------(방화벽/VPC)--------------------|-----------------
 [ Kubernetes Cluster ]                         |
                                                v
   +-------------------+              +-----------------------+
   |  실제 동작 중인   | <==(3. Sync)== | GitOps Operator (ArgoCD)|
   |  App 및 Pods      |              | (Git과 K8s 상태 비교)   |
   +-------------------+              +-----------------------+
```
---
## Ⅲ. 비교 및 연결
| 구분 | 전통적 파이프라인 (Push 기반 CD) | GitOps (Pull 기반 CD) |
|---|---|---|
| **진실의 원천 (SSOT)**| 배포 서버(Jenkins)의 스크립트 | 오직 Git 저장소 (선언적 YAML) |
| **보안 (Credential)** | CI 서버가 K8s 최고 권한(Secret)을 가져야 함 | K8s 내부가 Git의 읽기 권한만 가지면 됨 (안전) |
| **구성 표류(Drift)** | 누군가 수동 개입하면 파악 불가 | 에이전트가 불일치 감지 즉시 Git 상태로 복원 (Self-healing) |
| **장애 복구 (Rollback)**| 이전 빌드 번호 찾아서 다시 배포 파이프라인 실행 | `git revert` 명령어 한 번이면 K8s가 알아서 롤백 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **App Repo와 Config Repo의 분리**: 실무에서는 소스코드가 있는 Git(App Repo)과 K8s 배포 YAML이 있는 Git(Config Repo)을 반드시 분리해야 함. 합쳐놓으면 CI 빌드 시마다 배포 설정이 바뀌어 무한 루프(Trigger Loop)에 빠질 수 있음.
- **접근 통제 (Auditing)**: 서버에 직접 SSH로 접속하거나 `kubectl`을 날릴 권한을 모든 개발자에게서 뺏고, 오직 Git Pull Request(PR)의 코드 리뷰와 Merge 승인을 통해서만 배포가 이루어지게 강제(Zero Trust)하는 것이 GitOps 거버넌스의 핵심.
---
## Ⅴ. 기대효과 및 결론
- "Git이 곧 인프라다." 장애가 발생해도 Git의 커밋 히스토리만 보면 누가, 언제, 무엇을 바꿨는지 완벽히 추적(Audit) 가능하며, 복원 또한 즉각적임.
- 인프라 프로비저닝(IaC)부터 애플리케이션 배포까지 모든 클라우드 운영 행위를 '개발자의 익숙한 도구(Git)' 하나로 통일시킨 혁명적인 패러다임 전환임.
---
### 📌 관련 개념 맵
- IaC (Infrastructure as Code) ➡️ 선언적 배포 ➡️ GitOps (ArgoCD, Flux) ➡️ K8s 생태계

### 📈 관련 키워드 및 발전 흐름도
- 수동 서버 세팅 ➡️ Chef/Puppet (명령형 IaC) ➡️ Terraform (선언형 IaC) ➡️ GitOps (CD의 선언적 자동화)

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 방을 치울 때 엄마가 직접 들어와서 "책상 닦아! 장난감 넣어!"라고 소리쳐야(Push) 했어요.
2. 깃옵스(GitOps)는 방문에 '방의 완성된 사진(Git)'을 붙여두는 거예요.
3. 그러면 방 안에 있는 청소 로봇(ArgoCD)이 사진을 계속 쳐다보다가(Pull), 어질러진 장난감을 발견하면 사진과 똑같아질 때까지 알아서 청소(Sync)를 한답니다!
