---
title: "Cilium CNI (Cilium)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 185
---

# 📖 【암기용】 개념 완전 이해

> 목적: Cilium CNI를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Cilium은 **eBPF**를 데이터 플레인으로 쓰는 **Kubernetes CNI**(Container Network Interface)로, IP 대신 **보안 아이덴티티**(label 기반)로 네트워크 정책을 적용하고 **kube-proxy를 대체**하는 서비스 로드밸런싱과 관측(Hubble)을 함께 제공한다.
- **왜 필요한가**: 컨테이너 환경은 Pod가 끊임없이 재생성·재배치돼 IP가 수시로 바뀌므로, IP 기반 방화벽 규칙만으로는 "이 서비스가 누구인지"를 안정적으로 표현할 수 없다.
- **핵심 직관**: 단순 도로망이 아니라, 차량(패킷)의 신분증·목적지·운행 기록까지 커널 센서(eBPF)로 즉시 확인하는 클러스터 네트워크다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| CNI (Container Network Interface) | Kubernetes Pod에 네트워크를 붙여주는 표준 플러그인 인터페이스 — Cilium이 구현하는 **역할** | 건물에 전기·수도를 연결하는 배관 표준 |
| eBPF | Cilium의 데이터 플레인을 이루는 커널 내 프로그램 실행 기술 (184 참고) | Cilium이 도로에 심는 센서 기술 자체 |
| Cilium Agent | 노드마다 실행되며 Kubernetes API를 감시해 정책을 eBPF 프로그램·map으로 컴파일하는 데몬 | 각 동네 파출소 |
| Security Identity | Pod IP가 아니라 label 조합(예: `app=frontend`)에 부여하는 숫자 ID — IP가 바뀌어도 정책이 유지되는 핵심 | 주소가 아니라 직원증 번호로 신원 확인 |
| CiliumNetworkPolicy | identity 기반으로 L3/L4/L7(HTTP 메서드·경로 등)까지 표현하는 확장 네트워크 정책 | 부서·직급·방문 목적까지 규정한 출입 규칙 |
| kube-proxy replacement | iptables 기반 kube-proxy 대신 eBPF map 조회로 서비스 로드밸런싱을 수행하는 기능 | 순차 확인 명부 대신 즉시 조회되는 색인 |
| Hubble | Cilium이 수집한 flow(연결 단위 로그)를 시각화하고 drop 원인을 보여주는 관측 도구 | 교통 CCTV와 사고 기록 열람 시스템 |
| TC / XDP hook | 패킷 처리 eBPF 프로그램이 부착되는 커널 위치 (184 참고) | 패킷이 실제로 검문받는 지점 |

## 깊이 이해

### iptables 방식의 한계 (수치로 이해)
- 전통 CNI(Flannel, 초기 Calico)는 kube-proxy가 Service를 iptables 규칙 체인으로 구현한다. 규칙은 **순차 매칭**(선형 탐색)이라서 서비스·엔드포인트 수가 늘수록 매 패킷마다 확인해야 할 규칙 수가 비례해 늘어난다. 서비스가 수천 개인 대형 클러스터에서는 iptables 규칙이 수만 줄에 달해 규칙 갱신 자체가 지연되고 패킷 처리 지연도 커진다.
- Cilium은 이를 eBPF map의 **해시 조회**(hash lookup)로 대체한다. 규칙 수가 늘어도 조회는 거의 일정한 시간(대략 O(1))에 끝나므로, 서비스·엔드포인트가 늘어나는 대규모 클러스터에서 성능 저하 폭이 훨씬 작다.

### Security Identity가 IP 대신 신원을 쓰는 이유
- Pod는 재시작·스케일링마다 새 IP를 받는다. "10.0.3.15를 허용"이라는 규칙은 몇 분 뒤 다른 Pod가 그 IP를 재사용하면 의도와 다른 트래픽을 허용할 위험이 있다.
- Cilium Agent는 Pod의 label 조합(예: `app=payment, env=prod`)마다 고유한 숫자 identity를 부여하고, 패킷 헤더 확장 필드(또는 터널 인캡슐레이션)에 이 identity를 실어 나른다. 목적지 노드의 eBPF 프로그램은 IP가 아니라 **identity 값**으로 "이 패킷이 payment 서비스에서 왔다"를 확인한다 — Pod가 재배치돼 IP가 바뀌어도 label이 같으면 identity와 정책은 그대로 유지된다.

### 정책 적용을 구체 예로 보기
- 예: `app=frontend` Pod는 `app=payment` Pod의 443/TCP만 호출하도록 CiliumNetworkPolicy를 정의하면, Agent는 이를 컴파일해 eBPF map에 "frontend identity → payment identity, port 443 허용, 나머지 deny"로 반영한다. frontend가 payment의 8080 포트를 시도하면 애플리케이션에 도달하기 전에 커널 단에서 drop되고, Hubble이 `policy_deny` 이유와 함께 flow를 기록한다.
- L7까지 확장하면 "GET /api/v1/orders만 허용, POST는 차단"처럼 HTTP 메서드·경로 단위 정책도 가능하다 — 이 경우 Envoy 유사 프록시가 개입해 L7 파싱을 수행하므로 순수 eBPF만으로 처리하는 L3/L4보다 오버헤드가 크다.

### kube-proxy replacement 동작
- kube-proxy replacement를 켜면 ClusterIP·NodePort 트래픽도 iptables NAT 체인을 거치지 않고 eBPF 프로그램이 소켓 레벨(socket hook) 또는 TC 레벨에서 곧바로 목적지 Pod IP로 변환(DNAT)한다. 홉이 줄어드는 만큼 서비스 호출 지연이 줄고, kube-proxy 자체가 필요 없어져 운영 구성요소도 하나 줄어든다.

### 비유와 흔한 오해
- **비유**: 출입문에서 주소만 보는 경비가 아니라, 직원증·부서·방문 목적·이동 기록까지 확인하는 보안 게이트다.
- **오해**: "Cilium = 그냥 또 다른 CNI"라는 생각은 범위를 축소한 것이다. 기본 Pod 네트워킹 위에 kube-proxy replacement, identity 기반 L3~L7 정책, Hubble 관측, 일부 서비스 메시 유사 기능(mTLS, L7 라우팅)까지 포함하는 통합 네트워킹 계층이며, 그만큼 커널 버전 요구사항과 운영 복잡도도 함께 커진다.

## 연결 개념
- Kubernetes NetworkPolicy - Cilium이 확장하는 표준 정책 모델의 기반
- eBPF - Cilium 데이터 플레인의 기반 기술 (184 참고)
- Service Mesh(Istio) - L7 정책·관측 영역에서 기능이 일부 겹치는 비교 대상

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Cilium 답안은 CNI 설치가 아니라 eBPF data plane, identity policy, kube-proxy replacement, Hubble 지표를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cilium은 eBPF 기반 data plane으로 Kubernetes pod 네트워킹, policy enforcement, load balancing, observability를 제공하는 CNI임.
> 2. **가치**: label 기반 identity와 커널 경로 정책 적용으로 L3/L4/L7 네트워크 통제와 flow 관측을 결합함.
> 3. **판단 포인트**: 커널 버전, kube-proxy replacement, policy drop, p99 지연, Hubble flow coverage를 기준으로 적용해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CNI 역할 이해 확인 | pod IP, routing, policy, service load balancing | 단순 네트워크 플러그인으로 축소 |
| eBPF 적용 이해 확인 | TC/XDP hook, identity, BPF map | iptables와 차이 누락 |
| 운영 판단 확인 | Hubble, drop reason, kernel 호환 | 도입 효과만 나열 |

> 요약: 이 문제는 Cilium을 eBPF 기반 Kubernetes 네트워크·보안·관측 통합 계층으로 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: eBPF 기반 Kubernetes CNI
- 배경: pod 이동과 서비스 확장이 빈번한 환경에서 IP·iptables 중심 정책은 추적과 운영 비용이 증가한다.
- 필요성: label identity 기반 정책과 eBPF data plane으로 L3/L4/L7 통제와 flow 관측을 결합한다.

---

## Ⅱ. 구조 및 구성요소

```text
Kubernetes API -> Cilium Agent -> eBPF Program/Map -> Pod Network/Service LB
  / Policy: identity, L3/L4/L7
  / Observe: Hubble flow, drop reason
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Cilium Agent | 정책 변환과 eBPF program 관리 | node 단위 daemon |
| eBPF Data Plane | 패킷 포워딩, 정책, 로드밸런싱 | TC/XDP hook |
| Security Identity | label 기반 서비스 정체성 | IP 변경과 분리 |
| Hubble | flow 관측과 drop 원인 확인 | UI, relay, metric |

> 요약: Cilium은 Kubernetes API의 label과 정책을 eBPF data plane으로 변환해 패킷 처리와 관측을 수행함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Pod 생성 -> label identity 할당 -> policy compile -> eBPF map 갱신 -> packet 처리 -> Hubble flow 기록
  / 허용 조건 일치 -> forwarding
  / 정책 위반 -> drop reason 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Pod와 label을 감지해 identity 할당 | identity sync 100% |
| 2 | NetworkPolicy와 CiliumPolicy 해석 | policy import error 0건 |
| 3 | eBPF map에 정책과 service entry 반영 | map pressure 측정 |
| 4 | packet을 TC/XDP hook에서 처리 | drop count, latency |
| 5 | Hubble이 flow와 drop reason 수집 | flow coverage 95% 이상 |

> 요약: Cilium은 identity 기반 정책을 eBPF map에 반영하고 커널 경로에서 허용·차단·관측을 수행함.

---

## Ⅳ. 특징

| 구분 | iptables 기반 CNI | Cilium CNI | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 정책 기준 | IP, port 중심 | label identity 중심 | pod 이동 시 정책 유지 |
| data plane | iptables rule 탐색 | eBPF map lookup | service 수 증가 영향 측정 |
| 관측 | 별도 도구 필요 | Hubble flow 내장 | drop reason 확인 |
| 확장 | kube-proxy 의존 | kube-proxy replacement 가능 | p99 service latency |

> 요약: Cilium은 identity 정책과 eBPF 처리로 Kubernetes 네트워크 정책과 관측을 같은 계층에서 수행함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Flannel/Calico iptables | Cilium eBPF | 정책 수와 service 수 증가 환경 |
| 비용/처리 | rule chain 증가 | map lookup | p99 latency와 CPU 측정 |
| 운영/위험 | 별도 observability | Hubble 통합 | flow 기반 장애 분석 필요 |

> 요약: 정책과 서비스 규모가 큰 클러스터는 Cilium이 적합하나 커널 지원과 운영 역량을 사전 확인해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 커널 기능 부족 | eBPF helper, BTF 미지원 | 지원 버전 표준화 | node compatibility |
| 정책 오탐 | label selector 오류 | dry-run, staged policy | drop reason count |
| map pressure | endpoint, service 증가 | map size tuning | BPF map usage |

> 요약: Cilium 리스크는 커널 호환, 정책 정확도, BPF map 용량으로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 네트워크 | p99 latency 기준선 대비 10ms 이하 증가 | Hubble, Prometheus |
| 정책 | 의도치 않은 drop 0건 | Hubble drop reason |
| 운영 | flow coverage 95% 이상 | Hubble relay, UI |

> 요약: Cilium 운영 품질은 지연, drop reason, flow coverage로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 도입 전 점검: 노드 커널 5.x, BTF, CAP_BPF, kube-proxy replacement 가능 여부를 클러스터별로 확인
2. 정책 전환: namespace 단위 default deny 후 L3/L4 허용 정책부터 적용하고 L7 HTTP 정책은 핵심 API에 한정
3. 관측 운영: Hubble로 flow coverage 95% 이상, 의도치 않은 drop 0건, p99 latency 증가 10ms 이하를 관리

**결론 (2줄):**
- 기술사 판단: label 기반 정책과 flow 관측이 필요한 Kubernetes 환경은 Cilium, 단순 overlay 네트워크는 경량 CNI를 선택함
- 향후 방향: eBPF 기반 CNI, kube-proxy replacement, mesh-lite 기능이 클라우드 네이티브 네트워킹의 운영 축이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Cilium을 설명하시오", "기술하시오" | identity, policy compile, eBPF map 처리 흐름 | iptables CNI 대비 차이 |
| 요구사항 명시형 | "Kubernetes 네트워크를 설계하시오", "비교하시오" | policy, kube-proxy replacement, Hubble 관측 | 커널 조건, drop, latency 기준 |

> 요약: 설명형은 eBPF CNI 구조, 설계형은 정책과 관측 지표 중심으로 전환함.
