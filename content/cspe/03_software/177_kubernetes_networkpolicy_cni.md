---
title: "쿠버네티스 NetworkPolicy·CNI (Kubernetes NetworkPolicy CNI)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 177
---

# 📖 【암기용】 개념 완전 이해

> 목적: Kubernetes NetworkPolicy와 CNI를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: CNI는 Pod 네트워크를 연결하고, NetworkPolicy는 Pod 간 허용 트래픽을 선언하는 정책
- **왜 필요한가**: 기본 Kubernetes 네트워크는 Pod 간 통신을 넓게 허용하므로 업무, 보안 등급, 네임스페이스 기준의 흐름 통제가 필요하다.
- **핵심 직관**: CNI는 도로를 깔고, NetworkPolicy는 어느 차량이 어느 구역으로 갈 수 있는지 정하는 통행 규칙이다.

## 깊이 이해
- **배경·문제의식**: Kubernetes는 모든 Pod가 서로 통신할 수 있다는 모델을 전제로 한다. 그러나 운영 환경에서는 결제, 관리자, 데이터베이스 Pod가 임의 접근을 허용하면 침해 확산 경로가 커진다.
- **작동 원리**: CNI 플러그인은 Pod IP 할당, route, bridge, overlay, eBPF datapath를 구성한다. NetworkPolicy는 podSelector, namespaceSelector, ipBlock, ingress/egress rule로 허용 흐름을 선언하며 Calico, Cilium 같은 CNI가 실제 적용한다.
- **비유**: 사무실 네트워크에서 케이블과 스위치가 CNI이고, 출입 카드 권한표가 NetworkPolicy이다.
- **구체 예시**: `frontend` Pod는 `backend:8080`만 호출하고, `backend`는 `db:5432`만 접근하도록 egress rule을 만들면 lateral movement 경로를 줄일 수 있다.
- **흔한 오해·주의점**: NetworkPolicy 객체만 만들면 항상 적용되는 것은 아니다. 사용하는 CNI가 NetworkPolicy enforcement를 지원해야 한다.

## 연결 개념
- Pod Networking - Pod IP, Service, Endpoint 연결 모델
- Zero Trust - 명시적 허용 기반 동서 트래픽 통제
- Service Mesh - L7 인증과 암호화 통제 보완

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NetworkPolicy와 CNI 답안은 네트워크 연결 기능과 정책 집행 기능을 분리해 작성해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CNI는 Pod 네트워크 구현체, NetworkPolicy는 Pod ingress/egress 허용 규칙임.
> 2. **가치**: namespace, label, IP block 기준으로 동서 트래픽을 제한해 침해 확산 경로를 축소함.
> 3. **판단 포인트**: 정책은 선언이고 집행은 CNI가 담당하므로 Calico, Cilium 등 enforcement 지원 여부를 확인해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Kubernetes 네트워킹 이해 확인 | Pod IP, CNI, Service, NetworkPolicy | Service와 NetworkPolicy 혼동 |
| 보안 통제 설계 확인 | default deny, least privilege, ingress/egress | 정책 객체만 생성하면 적용된다고 단정 |
| 운영 검증 역량 확인 | connectivity test, flow log, drop metric | 정책 검증 방법 누락 |

> 요약: 이 문제는 CNI 연결 구조와 NetworkPolicy 집행 조건을 동시에 제시해야 함.

---

## Ⅰ. 개요 및 필요성

NetworkPolicy는 Pod 트래픽 허용 정책임. Kubernetes 기본 모델은 Pod 간 통신을 폭넓게 허용하므로 업무별 트래픽 경계를 정의해야 한다. CNI는 이 정책을 실제 데이터 경로에 적용하는 네트워크 구현 계층이다.

---

## Ⅱ. 구조 및 구성요소

```text
Pod -> CNI Plugin -> Pod Network -> Service/Pod
NetworkPolicy -> Selector/Rule -> CNI Enforcement -> Allow/Drop
  / ingress rule
  / egress rule
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| CNI Plugin | Pod IP, route, datapath 구성 | Calico, Cilium, Flannel |
| NetworkPolicy | 허용할 ingress/egress 선언 | L3/L4 중심 |
| Selector | Pod/Namespace 대상 지정 | label 품질 필요 |
| Enforcement | rule을 datapath에 적용 | iptables, eBPF |

> 요약: CNI는 네트워크를 만들고 NetworkPolicy는 label 기반 허용 규칙을 CNI datapath에 적용함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> CNI가 IP/route 설정 -> Policy 생성 -> Selector 매칭 -> datapath rule 적용 -> 트래픽 allow/drop
  / default deny 없음 -> 기존 허용 유지
  / egress rule 누락 -> 외부 호출 차단 가능
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CNI가 Pod 네트워크 인터페이스 구성 | Pod IP 할당 |
| 2 | NetworkPolicy가 대상 Pod selector 지정 | selected pod 수 |
| 3 | ingress/egress 허용 rule 작성 | port, protocol, CIDR |
| 4 | CNI가 rule을 datapath에 적용 | allow/drop counter |
| 5 | 연결 테스트와 flow log 확인 | 실패 경로 식별 |

> 요약: 정책은 selector로 대상을 고르고 CNI가 실제 패킷 허용 또는 차단을 수행함.

---

## Ⅳ. 특징

| 구분 | 기본 Pod 네트워크 | NetworkPolicy+CNI | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 통신 | Pod 간 기본 허용 | 명시 허용 기반 | default deny |
| 기준 | IP 중심 | label, namespace, CIDR | label 표준 |
| 집행 | CNI 구현 의존 | iptables/eBPF | CNI 지원 여부 |
| 한계 | 정책 없음 | L7 세부 제어 제한 | mesh 병행 |

> 요약: NetworkPolicy는 L3/L4 동서 트래픽 통제이며 L7 인증은 Service Mesh 또는 Gateway 정책으로 보완함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | flat Pod network | default deny + allowlist | 민감 업무 분리 |
| 비용/처리 | 보안그룹 외곽 통제 | Pod label 단위 통제 | namespace 10개 이상 |
| 운영/위험 | 침해 확산 경로 큼 | egress 제한과 flow log | lateral movement 통제 |

> 요약: 클러스터 내부 업무 경계가 필요하면 default deny와 업무별 allowlist 정책을 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정책 미적용 | CNI enforcement 미지원 | CNI 기능 검증, conformance test | policy test pass |
| 정상 통신 차단 | egress rule 누락 | staging test, DNS rule 분리 | denied flow 수 |
| label 오염 | selector 기준 불명확 | label taxonomy, admission 검증 | label 위반 0건 |

> 요약: 정책 리스크는 CNI 지원, egress 누락, label 품질에서 발생함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 정책 적용률 | namespace default deny 100% | policy inventory |
| 차단 검증 | 비인가 경로 연결 실패 100% | netshoot test |
| 관측 | drop flow log 수집 | Cilium Hubble, Calico log |

> 요약: NetworkPolicy 성공 여부는 정책 적용률, 비인가 차단 테스트, drop 로그로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 기본 차단: 운영 namespace에 default deny ingress/egress를 적용하고 DNS, registry, monitoring 필수 경로만 허용
2. 업무별 허용: frontend -> backend, backend -> db처럼 label 기반 allowlist를 작성하고 port/protocol을 명시
3. 검증 자동화: CI에서 policy unit test, 배포 후 netshoot 연결 테스트, flow log audit을 수행

**결론 (2줄):**
- 기술사 판단: NetworkPolicy는 선언이고 실제 통제력은 CNI enforcement 지원과 label 품질에 의해 결정됨
- 향후 방향: eBPF 기반 CNI와 Service Mesh 정책이 결합되어 L3/L4와 L7 통제가 함께 운영됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NetworkPolicy와 CNI를 설명하시오" | Pod IP 구성과 정책 적용 흐름 | CNI와 NetworkPolicy 역할 차이 |
| 요구사항 명시형 | "보안 통제 방안을 제시하시오", "설계하시오" | default deny, allowlist, 검증 흐름 | enforcement, egress, flow log 기준 |

> 요약: 설명형은 네트워크 구조, 보안형은 default deny와 검증 지표 중심으로 전환함.
