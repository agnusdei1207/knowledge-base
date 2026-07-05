---
title: "쿠버네티스 보안 (Kubernetes Security)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-security"
weight: 66
---

## 1. 한눈에 이해하기 (Core Intuition)
- **정의**: 수천 개의 컨테이너(Docker)를 자동으로 띄우고 지우며 지휘하는 **'쿠버네티스(K8s) 오케스트레이션 엔진' 자체의 취약점과 설정 오류를 방어하여 클러스터 전체가 장악되는 것을 막는 특화된 보안 체계**입니다.
- **필요성**: 쿠버네티스는 너무나 방대하고 복잡해서 기본 설정(Default)대로 켜면 대문이 활짝 열려있습니다. 해커가 컨테이너 1개를 뚫는 건 단순한 강도지만, 쿠버네티스 마스터 노드(API 서버)를 뚫으면 수천 대의 서버를 자기 맘대로 조종하는 '신(God)의 권한'을 갖게 되므로 완벽한 통제가 필요합니다.
- **핵심 직관**: **"도시(클러스터) 전체를 통제하는 시청 제어실 방어"**. 
  - 개별 컨테이너 보안이 "집집마다 도어락 달기"라면, 쿠버네티스 보안은 "도시의 신호등, 전력망, 경찰서 통신망을 통째로 쥐고 있는 시청 제어실(마스터 노드)을 테러리스트로부터 사수하는 것"입니다.

## 2. 왜 중요한가? (Background & Value)
- **등장 배경**: 쿠버네티스가 전 세계 퍼블릭/프라이빗 클라우드의 사실상(De facto) 표준이 되면서, 해커들의 최우선 타깃이 되었습니다. 해커들은 K8s의 복잡한 권한 설정(RBAC) 오류나 대시보드(Dashboard) 취약점을 노려 대규모 가상화폐 채굴기(Cryptojacking)를 띄워 수십억 원의 피해를 입히고 있습니다.
- **가치**: 한 번 뚫리면 전체 서버 인프라가 초토화되는 끔찍한 연쇄 반응(Blast Radius)을 막고, 안전한 클라우드 네이티브 워크로드를 운영하기 위한 최상위 생존 필수 요건입니다.

## 3. 어떻게 작동하는가? (Mechanism)
쿠버네티스 보안은 **제어 평면(마스터) 방어**와 **데이터 평면(노드/파드) 통제**로 나뉩니다.

1. **마스터 노드 보호 (API Server 통제)**
   - K8s의 모든 명령은 API 서버(`kube-apiserver`)로 들어옵니다. 
   - 이 API 포트를 외부 인터넷에 절대 노출하지 않고 프라이빗 망으로 숨깁니다.
   - 접근할 때 다중 인증(MFA)을 적용하고, "개발자 A는 파드(Pod)를 '조회'만 가능하고 '삭제'는 불가능하다"는 **RBAC (역할 기반 접근 제어)** 를 촘촘하게 설정합니다.
2. **파드(Pod)와 네트워크 격리 (Network Policies)**
   - K8s는 기본적으로 A파드와 B파드가 자유롭게 대화할 수 있습니다. (위험!)
   - **네트워크 정책(Network Policy)** 을 써서 "프론트엔드 파드는 DB 파드에 직접 말 걸지 마라"라고 방화벽 룰을 세밀하게(마이크로세그멘테이션) 쳐서 횡적 이동을 막습니다.
3. **작업자 노드 및 Kubelet 방어**
   - 실제로 컨테이너가 도는 워커 노드(Worker Node)의 핵심 에이전트인 `kubelet`의 인증 없는(Anonymous) 접속을 막고, 노드 간 통신을 암호화(mTLS)합니다.
4. **시크릿(Secret) 관리**
   - K8s 안에 DB 비밀번호를 저장할 때 평문(Base64)으로 저장하지 않고, 암호화 플러그인(KMS)이나 HashiCorp Vault 외부 저장소에 안전하게 연동시킵니다.

## 4. 실전 활용 및 예시 (Real-world Application)
- **구체적 사례**: 
  - **OPA Gatekeeper (입장 통제관)**: K8s에 새로운 컨테이너(파드)를 띄워달라는 명령이 들어올 때, OPA(Open Policy Agent)라는 문지기가 검사합니다. "어? 이 파드는 해킹에 취약한 Root 권한(Privileged)을 달라고 하네? 승인 거부(Deny)!" 라며 애초에 클러스터에 올라오지 못하게 입구 컷을 해줍니다. (이것을 Admission Controller라고 부릅니다).
- **주의점 및 흔한 오해**: 
  - "AWS EKS나 구글 GKE 같은 매니지드(Managed) K8s를 쓰니까 안전하겠지?" $\rightarrow$ **반만 맞습니다.** 마스터 노드는 클라우드 회사가 지켜주지만(책임 공유 모델), 그 위에 올라가는 파드의 보안 설정, 권한 쪼개기(RBAC), 네트워크 정책은 전적으로 '고객(회사)'이 직접 세팅하고 방어해야 합니다.

## 5. 핵심 비교 및 연결 개념 (Relation)
- **컨테이너 보안 vs 쿠버네티스 보안**:
  - **컨테이너 보안**: 도커(Docker) 이미지 자체의 버그, 어플리케이션 소스코드 취약점을 찾는 "내용물 검사".
  - **쿠버네티스 보안**: 그 도커들을 수만 개 돌리는 오케스트레이션 "운영 체제(OS) 판 자체"의 설정 오류와 권한을 쪼개고 지키는 "통제 환경 검사".

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **쿠버네티스 보안** | 쿠버네티스 보안 (Kubernetes Security)의 핵심 개념 | 이 주제의 본질 |

---


# ✍️ 단답형 / 서술형 시험장 출격 준비

### Ⅰ. 핵심 인사이트
- **본질**: 컨테이너 오케스트레이션의 표준인 쿠버네티스(Kubernetes) 환경에서 제어 평면(Control Plane) API 보안, 노드 및 파드(Pod)의 최소 권한 구성, 마이크로세그멘테이션(Network Policy)을 통해 워크로드의 가용성을 유지하면서 횡적 확산(Lateral Movement)을 억제하는 클라우드 네이티브 보안 체계.
- **가치**: K8s의 높은 유연성과 플랫 네트워크(Flat Network)라는 기본 속성이 가져오는 거대한 공격 표면(Attack Surface)을 선언적(Declarative) 보안 정책(Policy as Code)으로 제어하여 대규모 보안 침해(Blast Radius) 리스크를 최소화함.
- **판단 포인트**: K8s 보안의 핵심 아키텍처는 **API Server**에 대한 강력한 인증/인가(RBAC) 체계와, 배포 파이프라인의 최종 문지기 역할을 하는 **Admission Controller (승인 컨트롤러)** 의 유기적 결합에 있음.

### Ⅱ. K8s 아키텍처별 취약점 및 통제 방안 (The 4C's - Cluster 레이어 중심)
**1. Control Plane (제어 평면) 통제**
- **kube-apiserver**: 모든 명령의 허브. 외부 퍼블릭 인터넷 노출을 절대 금지(프라이빗 엔드포인트 구성). OIDC/SAML과 연동하여 강력한 인증 적용.
- **etcd**: K8s 클러스터의 모든 상태와 시크릿(Secrets) 정보가 저장되는 핵심 Key-Value 스토어. 암호화(Encryption at Rest) 설정이 필수이며, API Server 외에는 접근하지 못하도록 통신 격리(mTLS).
- **인가 (RBAC)**: "개발자는 Dev 네임스페이스(Namespace)에서만 작업 가능"하도록 Role과 RoleBinding을 최소 권한 원칙(PoLP)에 기반해 세분화.

**2. Data Plane (데이터 평면/Worker Node) 통제**
- **kubelet**: 노드의 캡틴 역할. `anonymous-auth=false`로 설정하여 익명 접속을 차단.
- **Pod Security (파드 권한 통제)**: 기존 PSP(Pod Security Policy)가 폐지되고, 현재는 **PSA(Pod Security Admission)** 또는 서드파티 OPA/Kyverno를 사용하여 **Privileged(루트) 파드 실행 금지**, Host Network 네임스페이스 공유 금지 등의 보안 샌드박싱(Sandboxing) 강제.

**3. Network (통신 평면) 통제**
- 기본적으로 모든 파드 간 통신이 열려 있는(Default Allow All) 위험을 막기 위해 **Network Policy** 객체를 생성. (L3/L4 수준의 클러스터 내부 방화벽).
- (예) `namespace: database` 라벨이 붙은 파드는 오직 `namespace: backend`에서 오는 트래픽의 3306 포트만 허용(Allow)하고 나머지는 모두 드롭(Drop)하는 **Zero Trust 마이크로세그멘테이션** 구현.

### Ⅲ. 배포 제어의 핵심: Admission Control (승인 제어)
사용자가 K8s API를 찔러 파드 생성을 요청할 때, RBAC 검사를 통과하더라도 마지막으로 정책을 검사하는 관문.
1. **Mutating Admission (변형)**: 파드가 클러스터에 맞지 않는 설정(예: 보안 컨텍스트 누락)을 가지면, 관리자가 정의한 안전한 값으로 강제로 고쳐줌(Mutate).
2. **Validating Admission (검증)**: 기업의 규정(예: "모든 이미지는 사내 내부 프라이빗 레지스트리에서만 가져와야 함")에 어긋나는 파드 생성 요청을 거부(Deny)함.
- **구현 도구**: OPA(Open Policy Agent) Gatekeeper, Kyverno. (이 과정을 **Policy as Code** 라 칭함).

### Ⅳ. K8s 시크릿 (Secrets) 관리 아키텍처 제언
- **문제점**: K8s의 기본 Secret 객체는 단순히 Base64로 인코딩된 평문(Plaintext)이라, etcd가 털리거나 RBAC가 잘못 뚫리면 누구나 패스워드를 읽을 수 있음.
- **해결책**: 외부의 전용 KMS(Key Management Service)나 **HashiCorp Vault**, AWS Secrets Manager와 K8s를 연동(CSI Secrets Store Provider)하여, 파드 내부에는 메모리 단에서만 휘발성으로 시크릿을 노출시키는 동적 시크릿 주입 아키텍처 구현 필수.

### Ⅴ. 결론 및 실무적 판단 포인트
- 인프라 아키텍트는 K8s 클러스터를 설계할 때 단일 거대 클러스터(Monolithic)를 쪼개어, 개발(Dev)/운영(Prod) 및 업무 중요도에 따라 물리적 클러스터를 분리하거나 최소한 **강력한 네임스페이스(Namespace) 격리**를 기본 철학으로 가져가야 합니다. K8s의 기본 설정(Default)은 '보안'이 아니라 '편의'에 맞춰져 있음을 명심해야 합니다.

### 💡 문제 유형별 목차 전환 포인트
- **[컨테이너 오케스트레이션(Kubernetes) 핵심 취약점 및 통제 방안 묻는 유형]**: Ⅰ과 Ⅱ번을 중심으로 Control Plane(마스터)의 API 및 RBAC 통제와, Data Plane(파드)의 권한 축소/격리 방안을 입체적으로 기술.
- **[K8s 내부 횡적 이동(Lateral Movement) 차단 및 정책 강제화 전략]**: Ⅱ-3항의 Network Policy(마이크로세그멘테이션)와 Ⅲ번의 Admission Controller(OPA)를 강조하여, 제로 트러스트(Zero Trust) 사상이 K8s 아키텍처에 어떻게 기술적으로 구현(Policy as Code)되는지 서술.
