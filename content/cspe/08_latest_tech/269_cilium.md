---
title: "Cilium (Cilium)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 269
---

# 📖 【암기용】 개념 완전 이해

> 목적: Cilium을 eBPF를 활용해 Kubernetes 네트워킹, 보안 정책, 관측성을 제공하는 클라우드 네이티브 네트워크 플랫폼으로 이해하게 만든다.

## 한눈에
- **개요**: eBPF 기반으로 Pod 네트워킹, NetworkPolicy, L7 policy, observability를 제공하는 Kubernetes CNI
- **왜 필요한가**: iptables 기반 kube-proxy와 전통 CNI는 서비스 수가 많아질수록 정책·추적·보안 가시성 관리가 복잡해진다.
- **핵심 직관**: 컨테이너 네트워크의 교통 신호와 CCTV를 커널 안의 검증된 프로그램으로 배치하는 방식이다.

## 깊이 이해
- **배경·문제의식**: Kubernetes 환경은 Pod IP가 자주 바뀌고 서비스 호출이 많아 identity 기반 정책과 패킷 경로 관측이 필요하다.
- **작동 원리**: Cilium agent가 Kubernetes API를 감시하고 eBPF map과 프로그램을 갱신해 라우팅, 로드밸런싱, 정책 집행을 수행한다.
- **비유**: 건물 출입카드 ID를 기준으로 층별 접근과 이동 기록을 관리하는 보안 관제 시스템과 유사하다.
- **구체 예시**: `frontend` Pod는 `backend`의 443 포트만 호출하도록 정책을 적용하고 Hubble로 HTTP error와 service map을 확인한다.
- **흔한 오해·주의점**: Cilium은 단순 CNI가 아니다. kube-proxy replacement, network policy, service mesh, Hubble observability까지 선택적으로 제공한다.

## 연결 개념
- eBPF — Cilium 데이터 경로의 핵심 실행 기술
- Service Mesh — Cilium이 sidecarless 방식으로 확장하는 영역
- Cloud Native Observability — Hubble 기반 서비스 흐름 관측

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Cilium은 eBPF data path, identity 기반 정책, Hubble 관측성을 함께 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cilium은 eBPF 기반 Kubernetes 네트워킹·보안·관측성 플랫폼임.
> 2. **가치**: IP 변화가 잦은 Pod 환경에서 identity 기반 정책과 커널 수준 data path를 제공함.
> 3. **판단 포인트**: kernel 지원, CNI 전환 절차, 기존 NetworkPolicy 호환성, Hubble 운영 범위를 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| eBPF 기반 CNI 이해 확인 | agent, eBPF map, identity, datapath | Cilium을 일반 overlay CNI로만 설명 |
| 보안 정책 이해 확인 | L3/L4/L7 policy, workload identity | IP 기반 ACL만 나열 |
| 관측성 판단 확인 | Hubble, flow log, service map | 모니터링 기능 누락 |

> 요약: 이 문제는 Cilium이 Kubernetes 네트워크 경로와 정책 집행을 eBPF로 처리하는 구조를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: eBPF 기반 Kubernetes CNI
- 배경: Pod IP 변동과 서비스 수 증가로 IP 기반 정책과 iptables rule 관리가 복잡해짐.
- 필요성: identity 기반 보안 정책, kube-proxy 대체, flow observability를 하나의 네트워크 계층에서 제공해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Kubernetes API -> Cilium Agent -> eBPF Program / Map -> Node Datapath
Pod -> Cilium Datapath -> Service / Pod / External Network
Cilium Datapath -> Hubble -> Flow Log / Service Map
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Cilium Agent | 정책·endpoint 상태를 eBPF에 반영 | 노드 단위 daemon |
| eBPF Datapath | 라우팅·로드밸런싱·정책 집행 | kube-proxy replacement 가능 |
| Identity | label 기반 보안 ID 부여 | IP 변화와 정책 분리 |
| Hubble | flow visibility와 service map 제공 | L3/L4/L7 관측 지원 |

> 요약: Cilium은 Kubernetes 상태를 eBPF data path로 변환하고 Hubble로 흐름을 관측한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> label 기반 identity 부여 -> 정책 계산
-> eBPF map 갱신 -> 패킷 수신 -> 정책·로드밸런싱 적용
-> flow event 생성 -> Hubble 조회
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Kubernetes endpoint와 label 감지 | endpoint ready |
| 2 | identity와 policy rule 계산 | policy verdict |
| 3 | eBPF map과 program 갱신 | map sync 상태 |
| 4 | 패킷 처리와 flow event 기록 | drop/pass count, flow log |

> 요약: Cilium은 Pod 상태와 label을 정책으로 변환해 eBPF data path에서 패킷 단위로 집행한다.

---

## Ⅳ. 특징

| 구분 | 전통 CNI/iptables | Cilium | 판단 기준 |
|:---|:---|:---|:---|
| 정책 기준 | IP·port 중심 | identity·label 중심 | Pod IP 변동성 |
| data path | iptables rule | eBPF map/program | rule 규모 |
| 관측성 | 별도 agent 의존 | Hubble flow visibility | 서비스 호출 추적 |
| 확장 기능 | CNI 중심 | kube-proxy, mesh, gateway 연계 | 플랫폼 표준화 |

> 요약: Cilium은 identity 기반 정책과 eBPF data path를 결합해 Kubernetes 네트워크 운영 범위를 확장한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Calico/iptables 계열 | Cilium/eBPF | eBPF 지원 kernel |
| 비용/성능 | iptables rule 증가 | map lookup 기반 처리 | service·policy 규모 |
| 운영/위험 | 기존 CNI 성숙도 | CNI 전환과 kernel 의존 | migration window |

> 요약: 대규모 Kubernetes와 identity 정책이 필요하면 Cilium을 검토하고, kernel 제약이 크면 기존 CNI를 유지한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| CNI 전환 장애 | 기존 Pod network 변경 | node pool 단계 전환 | node readiness |
| 커널 미지원 | eBPF helper·BTF 차이 | 지원 kernel matrix 검증 | agent startup failure |
| 정책 오탐 | label·selector 오류 | policy dry-run, Hubble 확인 | denied flow count |

> 요약: Cilium 리스크는 전환 장애, 커널 의존, 정책 오탐이며 단계 전환과 flow 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 네트워크 연결 | pod-to-pod 성공률 100% | connectivity test |
| 정책 집행 | 허용·차단 rule 일치 | Hubble verdict |
| 운영 상태 | agent, operator, Hubble 정상 | health check |

> 요약: Cilium 도입 후 연결성, 정책 verdict, 컴포넌트 상태를 동시에 점검해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 신규 node pool에서 Cilium CNI를 먼저 적용하고 기존 서비스는 namespace 단위로 이동해 연결성을 검증함.
2. label 기반 CiliumNetworkPolicy를 작성하고 Hubble verdict로 허용·차단 결과를 확인함.
3. kube-proxy replacement, Gateway API, service mesh 기능은 기본 CNI 전환 후 별도 단계로 적용함.

**결론 (2줄):**
- 기술사 판단: Kubernetes 네트워크 정책과 flow 관측성이 핵심이면 Cilium을 선택하고, 단순 overlay 요구면 기존 CNI도 가능함.
- 향후 방향: Cilium은 eBPF 기반 네트워킹에서 보안, Gateway, sidecarless mesh까지 통합 플랫폼으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Cilium을 설명하시오" | identity 계산과 eBPF map 갱신 흐름 | 전통 CNI 대비 차이 |
| 요구사항 명시형 | "Kubernetes 네트워크 보안 방안을 제시하시오" | 정책 적용과 Hubble 검증 절차 | 전환·커널·정책 리스크 |

> 요약: 설명형은 CNI 구조를, 보안형은 identity 정책과 flow 검증을 중심으로 작성한다.
