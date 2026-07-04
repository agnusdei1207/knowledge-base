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
- **개요**: NetworkPolicy·CNI는 Pod 간 통신을 다루는 두 계층으로, **CNI(Container Network Interface)**가 Pod 네트워크 연결 자체를 만들고, 그 위에서 **NetworkPolicy**가 허용된 트래픽만 통과시키는 방화벽 정책을 선언한다.
- **왜 필요한가**: 기본 Kubernetes 네트워크 모델은 모든 Pod가 서로 자유롭게 통신 가능한 flat network를 전제로 한다. 결제·관리자·데이터베이스 Pod까지 임의 접근이 가능하면, 하나가 침해됐을 때 확산 경로가 그대로 넓게 열려 있다.
- **핵심 직관**: CNI는 도로와 배관을 깔아 통신 자체를 가능하게 만드는 인프라이고, NetworkPolicy는 그 도로 위에서 "어느 차량이 어느 구역으로 갈 수 있는지"를 정하는 통행 규칙이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| CNI | Pod에 네트워크 인터페이스와 IP를 부여하고 패킷 경로(datapath)를 구성하는 표준 플러그인 규격 — 이 개념이 속한 **상위 개념** | 도로·배관 공사 |
| NetworkPolicy | 어떤 Pod가 어떤 Pod와 통신 가능한지 선언하는 API 객체(선언일 뿐, 실제 집행자는 아님) — 또 다른 **상위 개념** | 출입 규정 문서 |
| podSelector | 정책을 적용할 대상 Pod를 label로 지정 | 규정이 적용되는 인원 명단 |
| namespaceSelector | 특정 namespace 전체를 대상·출처로 지정 | 특정 부서 전체 |
| ipBlock | CIDR 대역으로 대상을 지정(클러스터 외부 IP 등) | 특정 우편번호 구역 |
| ingress rule | 들어오는(inbound) 트래픽 허용 규칙 | 입장 허용 명단 |
| egress rule | 나가는(outbound) 트래픽 허용 규칙 | 외출 허용 명단 |
| default deny | 정책이 하나라도 selector에 걸리면, 명시되지 않은 트래픽은 전부 차단되는 화이트리스트 원칙 | "명단에 없으면 출입 금지" |
| Enforcement(집행) | 선언된 정책을 실제 패킷 레벨(iptables·eBPF)에서 적용하는 동작 — CNI가 이 기능을 지원해야만 동작함 | 규정을 실제로 검문하는 경비원 |
| Lateral Movement | 공격자가 침해된 Pod를 발판 삼아 내부의 다른 Pod로 옮겨가는 것 | 한 집이 뚫리면 옆집도 뚫리는 것 |

## 깊이 이해

### 왜 기본이 "다 허용"인가 (배경)
- Kubernetes 네트워킹 표준(CNI 모델)은 "모든 Pod가 NAT 없이 서로 직접 통신 가능"을 전제로 설계됐다. 이는 마이크로서비스 간 자유로운 호출을 단순하게 만들지만, 결제나 DB처럼 민감한 Pod까지 아무 Pod에서나 접근 가능하다는 뜻이기도 하다. NetworkPolicy가 없으면 이 flat network가 그대로 보안 노출면이 된다.

### CNI 동작 원리 — 수치로 이해
- Pod가 생성되면 CNI 플러그인이 호출되어 ① 가상 네트워크 인터페이스(veth pair)를 만들고 ② Pod CIDR 대역(예: `10.244.0.0/16`)에서 IP 하나(예: `10.244.1.7`)를 할당하고 ③ 라우팅 테이블이나 오버레이(VXLAN) 경로를 구성한다.
- 구현 방식은 CNI마다 다르다 — Calico는 BGP로 라우팅 정보를 전파하고, Cilium은 eBPF로 커널 레벨에서 패킷을 처리하며, Flannel은 VXLAN 오버레이로 캡슐화한다. 이 구현 차이가 바로 다음의 NetworkPolicy 지원 여부를 가른다.

### default deny 판정 원리 — 수치 워크드 예제
- 정책이 하나도 없으면 모든 Pod 간 통신이 허용된다(flat). `frontend` Pod에 "egress는 `backend:8080`만 허용"이라는 NetworkPolicy를 걸면, 그 순간부터 frontend는 이 규칙에 명시된 목적지 외에는(예: `db:5432` 직접 접근) 나갈 수 없게 된다.
- 즉 default deny는 클러스터 전체에 자동 적용되는 게 아니라 **podSelector에 걸린 Pod에 한해서만** "명시 안 된 것은 거부"로 전환된다는 것이 핵심 판별 원리다.

### Lateral Movement 축소 — 수치로 이해
- 정책이 없을 때 침해된 frontend Pod 1개가 도달 가능한 목적지가 backend 3개, db 2개, admin 1개 등 총 6개라고 하자.
- `frontend → backend:8080만, backend → db:5432만` 허용하는 정책을 걸면, frontend가 도달 가능한 목적지는 6개에서 backend 3개로 줄어들고, backend가 뚫리더라도 다시 db 2개로 제한된다. 이렇게 공격 표면이 계단식으로 축소된다.

### Enforcement 여부 확인하기
- NetworkPolicy 객체는 어떤 CNI를 쓰든 생성 자체는 된다. 하지만 Flannel처럼 NetworkPolicy enforcement를 지원하지 않는 CNI에서는 객체만 존재할 뿐 실제로 아무 트래픽도 차단되지 않는다 — 이것이 가장 흔한 운영 실수다. Calico, Cilium, Weave Net 등은 enforcement를 지원한다.

### 비유
- 사무실 네트워크에서 케이블과 스위치를 까는 것이 CNI이고, 출입 카드 권한표를 만드는 것이 NetworkPolicy다. 권한표만 만들고 카드 리더기(enforcement)가 없는 문이라면, 표를 아무리 정교하게 써도 문은 그냥 열려 있다.

### 흔한 오해·주의점
- NetworkPolicy 객체를 만들었다고 자동으로 보안이 강화되는 것은 아니다. 사용 중인 CNI가 enforcement를 지원하는지, 그리고 대상 Pod에 default deny 정책이 실제로 걸려 있는지를 함께 확인해야 한다.

## 연결 개념
- Service/Ingress(176) — Service로 전달된 트래픽도 결국 이 CNI datapath를 거쳐 Pod에 도달함
- 쿠버네티스 아키텍처(173) — CNI는 Control Plane 밖의 Add-on으로 클러스터 네트워크를 구성
- Zero Trust / Service Mesh — NetworkPolicy는 L3/L4 통제이며, L7 인증·암호화는 Service Mesh가 보완

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

- 개요: NetworkPolicy는 Pod 트래픽 허용 정책임.
- 배경: Kubernetes 기본 모델은 Pod 간 통신을 폭넓게 허용하므로 업무별 트래픽 경계를 지정해야 한다.
- 필요성: CNI 구현 계층에서 ingress, egress, namespace, label 기준의 통신 정책을 데이터 경로에 적용한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
