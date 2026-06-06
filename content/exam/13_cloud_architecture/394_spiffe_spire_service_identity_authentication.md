---
title: "SPIFFE SPIRE Service Identity Authentication"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SPIFFE(공급망·런타임에 무관한 모든 워크로드에 발급되는 암호학적 신원 표준)와 SPIRE(SPIFFE Reference Implementation, 이 표준을 노드/워크로드 어테스테이션으로 구현한 런타임)는 IP·호스트명·클라우드 벤더 의존성을 제거한 **SVID(SPIFFE Verifiable Identity Document, 보통 X.509-SVID 또는 JWT-SVID)**를 통해 `spiffe://<trust_domain>/<workload_path>` 형태의 검증 가능한 신원을 워크로드에 동적 발급·자동 회전하는 시스템이다.
> 2. **가치**: 컨테이너·멀티클러스터·하이브리드 클라우드 환경에서 mTLS를 수동 설정 없이 자동 적용 가능(제로트러스트), Vault/Isteady/Consul 등 기존 시스템 대비 인증서 발급·폐기·회전 오버헤드를 **수십 초 단위 TTL(예: 1시간) 자동화**로 해소, 페더레이션을 통해 이기종 신뢰 도메인 간 상호 신뢰를 OIDC 또는 번들 교환으로 가능하게 함.
> 3. **판단 포인트**: 사이드카 vs 노드 에이전트 배치 모델, **어테스테이션 신뢰 경계(노드->에이전트->워크로드의 2-체인 검증)**, 페더레이션 토폴로지(메시 vs 스타), SVID TTL/회전 주기와 KeyManager HSM 연동, 기존 PKI/IAM과의 공존 전략이 핵심 결정 변수.

---

## Ⅰ. 개요 및 필요성

전통적인 서비스 인증은 IP·호스트명·포트에 의존하거나, X.509 인증서를 한 번 발급받아 만료 시점에 일괄 갱신하는 **장기 유효기간(Long-lived Credential)** 방식이었다. 그러나 컨테이너 오케스트레이션(Kubernetes, Nomad), 서버리스, 멀티클러스터, 마이크로서비스가 보편화되면서 다음 문제가 대두되었다.

- **휘발성 신원(ephemeral identity)**: Pod는 수십 초~수 분 단위로 IP가 변경되며, 무중단 배포(rolling update) 시 새 인스턴스가 즉시 통신을 시작해야 한다.
- **다중 신뢰 도메인**: AWS EKS, GCP GKE, 온프레미스 OpenShift가 동시에 존재할 때 통합된 신원 체계를 만들 수 없다.
- **과도한 권한**: 클라우드 IAM 역할(IAM Role for Service Accounts, IRSA·Workload Identity 등)에 의존하면 특정 클라우드에 종속되며, 메타데이터 API 노출 위험이 있다.
- **Zero Trust 요구**: NIST SP 800-207, KISA 클라우드 보안 가이드라인 등에서 "네트워크 위치가 아닌 신원·워크로드 속성으로 인증하라"는 요건이 강조된다.

SPIFFE는 2017년 Scytale(현 SPIFFE Maintainers) 주도로 시작되어 CNCF Incubating(2020) -> **Graduated(2024)** 프로젝트로 승격되었고, SPIRE는 이를 **플러그인 기반 어테스테이션**과 **KeyManager 플러그인**으로 실제 운영 환경에 배포 가능한 형태로 구현한 런타임이다.

```text
[기존 방식: 호스트/IP 기반 신원]
+--------+       +--------+        +--------+
|  HostA |       |  HostB |        |  HostC |
|10.0.0.1|<----->|10.0.0.2|<------>|10.0.0.3|
+--------+  ACL  +--------+  iptables  +--------+
   ^ IP 변경 시 모든 ACL/방화벽 룰 수동 갱신 필요
   ^ 컨테이너 재시작 -> 신원 단절 -> mTLS 핸드셰이크 실패

[SPIFFE/SPIRE 방식: 신원(Identity) 기반, 위치/네트워크에 비의존]
                                +----------------+
                                |   SPIRE Server |
                                |  (SVID 서명/   |
                                |  정책 관리)    |
                                +-------+--------+
                                        | mTLS (gRPC)
                +-----------------------+-----------------------+
                |                                               |
          +-----v-----+                                   +-----v-----+
          |SPIRE Agent|                                   |SPIRE Agent|
          | (Node X)  |                                   | (Node Y)  |
          +-----+-----+                                   +-----+-----+
                | UDS(/run/spire/sockets/agent.sock)            |
        +-------+-------+                              +-------+-------+
        |       |       |                              |       |       |
      [PodA] [PodB] [PodC]                          [PodD] [PodE] [PodF]
      SVID: spiffe://prod/ns/team-a/sa/checkout     SVID: spiffe://prod/ns/team-b/sa/order
        -> Workload가 시작 시 Agent에 자기 selector(예: k8s:ns:team-a, k8s:sa:checkout)를
          제시하고 Server가 검증한 SVID(X.509, TTL=1h)를 즉시 발급
        -> 다른 워크로드는 SVID의 SAN(Subject Alternative Name, URI:spiffe://...)을
          신뢰하여 네트워크 위치 무관 mTLS 가능
```

**📢 섹션 요약 비유**: 기존 방식이 "특정 주소의 특정 집 우편함"으로 편지를 보내는 거라면, SPIFFE는 **"발신자가 누구인지 확인된 인증서를 항상 휴대하고, 받는 사람이 그 인증서만 보고 문을 열어주는 전자여권 시스템"**과 같다. 이사·이사·이사를 반복해도 여권의 신원은 변하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SPIRE는 **Server-Agent 2계층 구조**를 가지며, 모든 통신은 mTLS(자체 CA 기반)로 보호된다. 핵심 데이터 모델은 다음 4가지다.

1. **Trust Domain**: `spiffe://example.com`처럼 신원의 네임스페이스. 서로 다른 트러스트 도메인은 명시적 페더레이션 전에는 서로를 신뢰하지 않는다.
2. **SPIFFE ID**: `spiffe://<trust_domain>/<path>`. 클러스터 내에서는 `spiffe://prod/ns/team-a/sa/checkout`처럼 K8s 네임스페이스·서비스계정 경로를 매핑하는 것이 일반적이다.
3. **SVID(SPIFFE Verifiable Identity Document)**: SPIFFE ID가 포함된 서명된 자격증명. 종류는 **X.509-SVID**(mTLS용, RFC 9440 사양)와 **JWT-SVID**(HTTP/REST/gRPC unary, 단방향) 두 가지.
4. **Selector**: 워크로드의 속성을 표현하는 key=value 쌍(예: `k8s:ns:team-a`, `k8s:sa:checkout`, `unix:uid:1000`, `docker:label:app=payment`). **Registration Entry**는 `SPIFFE ID ↔ Selectors`의 매핑이다.

### 📐 SVID 발급 시퀀스

```text
[Workload]                [SPIRE Agent]                 [SPIRE Server]
    |                          |                              |
    | ① Workload API 호출     |                              |
    | (UDS: agent.sock)       |                              |
    |------------------------->|                              |
    |                          | ② Workload Attestation 요청 |
    |                          |  (자체 수집한 PSPA/Selector  |
    |                          |   후보 전달, e.g.           |
    |                          |   k8s:ns=team-a, sa=checkout|
    |                          |----------------------------->|
    |                          |                              | ③ Registration Entry 조회
    |                          |                              |    -> selectors 매칭되는 ID 탐색
    |                          |                              | ④ CA 서명 키로 X.509-SVID 생성
    |                          |                              |    (SAN:URI=spiffe://prod/...)
    |                          |                              |    Bundle(CA Cert) 동봉
    |                          | <----------------------------|
    |                          | ⑤ SVID + Bundle 반환        |
    | <-------------------------|                              |
    | ⑥ SVID 로컬 디스크/메모리에 보관                        |
    |    mTLS 핸드셰이크 시 즉시 사용                          |
    |                                                           |
    |                          [TTL(예: 1h) 만료 임박 시]      |
    | <-- ⑦ SVID Rotation API (새 X.509 회전) -----------------|
    |                          |                              |
```

### 📐 노드 어테스테이션(Node Attestation)

워크로드 어테스테이션에 앞서, **에이전트가 진짜 해당 노드인지**를 서버가 검증한다.

```text
   +----------------+  부팅 시 SVID 요청  +-----------------+
   |  SPIRE Agent   | ------------------> |   SPIRE Server  |
   |  (Node=worker1)|                     |  (Attestor:     |
   +----------------+  ① join_token +     |   - k8s_psat    |
          ^           Node-attestation    |   - iid           |
          |           증거(예: kubelet     |   - aws_iid       |
          |           부트스트랩 토큰,     |   - gcp_iit       |
          |           TPM endorsement)     |   - azure_msi   |
          |                                |   - join_token) |
          |                                +---------+--------+
          |                                          | ② 검증
          |                                          v
          |                                +-----------------+
          |                                |  Attestor Plugin|
          |                                |  결과 -> true    |
          |                                +---------+--------+
          |                                          | ③ 에이전트 SVID 반환
          | <----------------------------------------+
   v  (이제 Agent는 Server와 mTLS 채널 형성, 모든 후속 RPC 보호)
```

### 📐 구성 요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **SPIRE Server** | 정책 저장소·SVID 발급자·페더레이션 허브. 단일 인스턴스 또는 HA 모드(K8s Deployment, 외부 DB: MySQL/PostgreSQL/SQLite). | 자체 CA 키(Software/HSM/Cloud KMS 플러그인)로 X.509-SVID 서명, Registration Entry CRUD, 노드/워크로드 어테스테이터 플러그인 로드, **datastore 캐시**로 인한 hot reload 지원, **Bundle Endpoint(gRPC)**로 신뢰 번들 배포 |
| **SPIRE Agent** | 노드/호스트당 1개 인스턴스. **Workload API** 노출(UDS: `/run/spire/sockets/agent.sock` 또는 Windows Named Pipe `\\.\pipe\spire-agent`). | 부모 프로세스 Supervisor가 자식 프로세스에게만 SVID 핸들오버(소켓 FD 상속)하여 **에이전트와 워크로드 사이에서도 0-trust**, Local CA 캐시(서버 다운 대비 SVID 회전 지속), Workload attestor로 k8s/docker/unix/psat/azure_msi 등 선택 |
| **Workload API** | 클라이언트 라이브러리(`spiffe-go`, `spiffe-cpp`, `spiffe-rs` 등) 또는 **SPIFFE Helper Sidecar**로 접근. | `FetchX509SVID()`, `FetchJWTSVID()`, `FetchJWTSVIDAndBundle()`, `ValidateJWTSVID()` 4개 RPC. 토큰 교체 시 **In-process Streaming**으로 무중단 회전. **SDS(Secret Discovery Service, xDS 표준) 어댑터**로 Envoy에 주입 가능 |
| **OIDC Discovery Provider** | SPIRE를 OIDC IdP로 노출하여 **JWT-SVID 기반 페더레이션** 가능. | `/.well-known/openid-configuration` 엔드포인트, JWKS(JSON Web Key Set) 자동 회전, 클라이언트(`audience`) 단위 서명 키 분리 |
| **SPIRE CSI Driver** | K8s 환경에서 파드별 SVID를 `Secret`/`csi-volume`으로 안전 주입. | `NodePublishVolume` 단계에서 해당 노드 Agent에 Workload API 호출, **Tmpfs 기반 ephemeral mount**로 디스크 누출 방지, kubelet의 `tokenRequest`로 ServiceAccount Token 위조 방지 |
| **KeyManager Plugin** | CA 키의 생성·저장·서명을 외부화. | Software(default), PKCS#11(HSM: Thales/YubiHSM/AWS CloudHSM), AWS KMS, GCP KMS, Vault Transit Secrets Engine. **FIPS 140-2 Level 3** 요구 시 HSM 필수 |

### 📐 핵심 알고리즘/파라미터

- **X.509-SVID**: X.509v3, **URI SAN에 `spiffe://trust_domain/path`**만 포함(국가·조직 등 다른 필드 금지로 사양 단순화), 별도 확장 영역에 **spiffe-agent**·**spiffe-server** 플래그로 발급자 구분, **KeyUsage = DigitalSignature + KeyEncipherment**, **ExtendedKeyUsage = clientAuth, serverAuth**.
- **회전 메커니즘**: TTL 만료 50% 시점부터 Agent가 자발적 회전, SVID는 디스크가 아닌 **메모리 + UDS 핸들**로만 노출, 만료 SVID는 **JIT 폐기**(CRL 없이 모든 클라이언트가 자체 캐시 만료 시 폐기).
- **JWT-SVID**: TTL 기본 5분(상한 없음, 권장 ≤ 1시간), **alg=RS256/PS256/ES256**, 클레임 `sub=spiffe://...`, `aud=<client SPIFFE ID>`, `exp`, `iat`. 액세스 토큰 대체용.
- **어테스테이션 신뢰 단계**: ①Node -> ②Agent(SVID) -> ③Workload(Process-based selector 검증)의 **3-체인 위임**, 어느 한 단계라도 실패 시 SVID 발급 거부.

**📢 섹션 요약 비유**: SPIRE Server는 **여권 발급 본부**, SPIRE Agent는 각 구청 **신분증 발급 창구**, Workload API는 **본인 확인 후 신분증 진열함**이다. 구청은 본부 인증을 받아 창구 신분증을 받고, 시민은 창구에서 본인 확인을 거쳐 여권을 받는다. 여권에 도장(서명)을 찍는 인장은 본부만이 보관한다(HSM/KMS).

---

## Ⅲ. 비교 및 연결

### 📊 SPIFFE/SPIRE vs 대안 기술

| 구분 | **SPIFFE/SPIRE** | **HashiCorp Vault PKI** | **Istio mTLS(SDID)** | **클라우드 IAM(IRSA/Workload Identity)** | **전통적 mTLS(CFSSL/Step-ca)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **신원 모델** | 워크로드 속성 기반 동적(Selector), 위치/네트워크 비의존 | Vault Role 기반 정적, 도메인·IP 의존 | K8s ServiceAccount 기반, Istio Control Plane 의존 | 클라우드 메타데이터
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 394 / 800

<- **이전**: [393. mTLS 상호 인증 서비스 간 암호화](/studynote/13_cloud_architecture/06_exam_summary/393_mtls_mutual_authentication_service_encryption/)
**다음**: [395. 서버리스 FaaS 이벤트 드리븐 아키텍처](/studynote/13_cloud_architecture/06_exam_summary/395_serverless_faas_event_driven_architecture/) ->

---
