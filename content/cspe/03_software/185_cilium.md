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
- **개요**: eBPF를 활용해 Kubernetes 네트워킹, 네트워크 정책, 관측, 로드밸런싱을 제공하는 CNI
- **왜 필요한가**: 컨테이너 네트워크는 pod가 계속 이동하므로 IP 기반 방화벽만으로 서비스 정체성과 L7 정책을 관리하기 어렵다.
- **핵심 직관**: 단순 도로망이 아니라 차량 신분, 목적지, 운행 기록까지 커널 센서로 확인하는 클러스터 네트워크이다.

## 깊이 이해
- **배경·문제의식**: iptables 기반 kube-proxy와 CNI는 rule 수가 많아질수록 정책 추적과 장애 분석이 어려워진다. 서비스 간 보안은 IP보다 identity와 label 기반이 더 적합하다.
- **작동 원리**: Cilium agent가 pod label을 security identity로 바꾸고, eBPF program을 TC/XDP hook에 적재해 패킷 포워딩, 정책 적용, service load balancing을 수행한다.
- **비유**: 출입문에서 주소만 보는 경비가 아니라 직원증, 부서, 방문 목적, 이동 기록을 함께 확인하는 보안 게이트이다.
- **구체 예시**: `app=frontend` pod는 `app=payment`의 443/TCP만 호출하도록 L3/L4 정책을 적용하고, Hubble로 flow drop 원인을 namespace 단위로 확인한다.
- **흔한 오해·주의점**: Cilium은 CNI만이 아니다. kube-proxy replacement, network policy, Hubble observability, service mesh 일부 기능까지 포함하나 커널 버전과 운영 복잡도를 검토해야 한다.

## 연결 개념
- Kubernetes NetworkPolicy - Cilium 정책 모델의 기본
- eBPF - Cilium data plane 기반
- 서비스 메시 - L7 정책과 관측 일부 영역에서 비교

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

Cilium은 eBPF 기반 Kubernetes CNI임. pod 이동과 서비스 확장이 빈번한 환경에서 IP·iptables 중심 정책은 추적과 운영 비용이 증가한다. Cilium은 label identity 기반 정책과 eBPF data plane으로 네트워크 통제와 관측을 결합한다.

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
