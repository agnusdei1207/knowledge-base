+++
weight = 117
title = "117. K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: K8s Network Policy는 **Pod 간 네트워크 트래픽을 라벨 기반으로 허용/거부**하는 선언적 방화벽 규칙이며, 마이크로 세그멘테이션(Micro-segmentation)을 통해 클러스터 내부 **East-West 트래픽을 제어**한다.
> 2. **가치**: 기본 K8s는 **모든 Pod 간 통신이 허용(Flat Network)**되므로, 하나의 Pod가 침투당하면 클러스터 전체가 위험하다. Network Policy로 **"frontend → backend만 허용, backend → DB만 허용"**처럼 최소 권한을 적용한다.
> 3. **판단 포인트**: Network Policy는 **CNI 플러그인(Calico·Cilium)이 실제 적용**하며, 기본 CNI(Flannel)는 Network Policy를 지원하지 않는다. Cilium의 L7(HTTP/gRPC) 정책이 차세대 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Network Policy 예시                                │
├───────────────────────────────────────────────────────┤
│  [기본: Flat Network — 모든 Pod 간 통신 허용]         │
│   frontend ←→ backend ←→ db ←→ 모든 Pod             │
│   → 1개 Pod 침투 시 전체 위험                        │
│                                                       │
│  [Network Policy 적용: 마이크로 세그멘테이션]         │
│   frontend → backend:8080 ✅                         │
│   backend → db:5432 ✅                               │
│   frontend → db:5432 ❌ (차단)                       │
│   외부 → frontend:443 ✅ (Ingress)                   │
│   → 최소 권한, 횡이동(Lateral Movement) 차단         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Flat Network는 모든 방 문이 열린 건물이고, Network Policy는 각 방에 카드키(라벨)가 있어야만 들어갈 수 있는 보안 건물이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Network Policy 구성 요소

| 요소 | 설명 |
|:---|:---|
| **podSelector** | 정책이 적용될 대상 Pod (라벨) |
| **policyTypes** | Ingress(수신) / Egress(발신) |
| **ingress.from** | 트래픽을 허용할 소스 (Pod/Namespace/CIDR) |
| **egress.to** | 트래픽을 허용할 목적지 |
| **ports** | 허용할 포트/프로토콜 |

### CNI 플러그인별 지원

| CNI | L3/L4 Policy | L7 Policy | eBPF |
|:---|:---|:---|:---|
| **Flannel** | ✗ | ✗ | ✗ |
| **Calico** | ✅ | 일부 | 옵션 |
| **Cilium** | ✅ | **✅ (HTTP/gRPC)** | **✅** |

- **📢 섹션 요약 비유**: Calico는 IP·포트 기반 방화벽(L4)이고, Cilium은 URL 경로까지 검사하는 WAF 수준(L7)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 기본 (정책 없음) | L3/L4 Policy | L7 Policy |
|:---|:---|:---|:---|
| **제어 수준** | 없음 | IP·포트 | **HTTP 경로·메서드** |
| **횡이동** | 가능 | **차단** | **정밀 차단** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기본 정책: Default Deny
```yaml
# 모든 Ingress 차단 → 필요한 것만 허용 (화이트리스트)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

---

## Ⅴ. 기대효과 및 결론

| 지표 | 정책 없음 | Network Policy | 개선 |
|:---|:---|:---|:---|
| 횡이동 위험 | 100% | **차단** | 제로 트러스트 |
| 공격 표면 | 전체 Pod | **최소 권한** | 90% 축소 |

Network Policy는 **K8s 제로 트러스트의 기초**이며, Cilium eBPF 기반 L7 정책으로 Service Mesh 수준의 보안을 달성하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **마이크로 세그멘테이션** | Network Policy가 구현하는 보안 원칙 |
| **Calico** | L3/L4 Network Policy CNI |
| **Cilium** | L7 (HTTP/gRPC) Policy, eBPF 기반 |
| **제로 트러스트** | Network Policy가 기여하는 보안 아키텍처 |
| **Service Mesh** | L7 트래픽 제어의 상위 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Flat Network (K8s 기본 — 모든 Pod 간 통신 허용)]
    │
    ▼
[K8s Network Policy (2017) — L3/L4 Pod 간 격리]
    │
    ▼
[Calico (2018~) — BGP 기반 L3/L4 정책]
    │
    ▼
[Cilium (2020~) — eBPF 기반 L7 정책]
    │
    ▼
[현재: Cilium Service Mesh — Network Policy + L7 관측성 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K8s 기본은 모든 방 문이 열려있는 **자유로운 건물**이에요.
2. Network Policy는 각 방에 **카드키(라벨)**가 있어야만 들어갈 수 있게 해요.
3. 덕분에 나쁜 사람(공격자)이 한 방에 들어와도 **다른 방으로 못 가서** 피해가 줄어요!
