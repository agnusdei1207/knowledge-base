---
title: "eBPF 네트워크 관측 (eBPF)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 184
---

# 📖 【암기용】 개념 완전 이해

> 목적: eBPF 네트워크 관측을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 커널 이벤트 지점에 검증된 작은 프로그램을 붙여 패킷, syscall, 지연을 낮은 침습도로 관측하는 기술
- **왜 필요한가**: 컨테이너와 마이크로서비스 환경은 프로세스 수명과 네트워크 경로가 짧아 전통 에이전트만으로 원인 추적이 어렵다.
- **핵심 직관**: 도로 위 차량을 세우지 않고 도로 센서가 번호, 속도, 흐름을 실시간 기록하는 방식이다.

## 깊이 이해
- **배경·문제의식**: tcpdump, sidecar, library instrumentation은 지점별 사각지대가 있다. 커널은 네트워크, 파일, syscall의 공통 경로이므로 관측 위치로 적합하다.
- **작동 원리**: eBPF bytecode는 verifier 검증을 통과한 뒤 kprobe, tracepoint, XDP, TC hook에 부착되고, map과 ring buffer로 사용자 공간에 데이터를 전달한다.
- **비유**: 병원에서 환자마다 설문지를 받는 대신 주요 출입문, 검사실, 처방 창구에 센서를 설치해 흐름을 기록하는 방식이다.
- **구체 예시**: Kubernetes 노드에서 TCP retransmit, DNS latency, HTTP status를 eBPF로 수집해 pod label 기준 p95 지연과 drop count를 추적한다.
- **흔한 오해·주의점**: eBPF는 커널 모듈보다 제약이 적지만 무제한 실행이 아니다. verifier 제한, 커널 버전 차이, map 메모리, 권한(CAP_BPF) 관리가 필요하다.

## 연결 개념
- Cilium - eBPF 기반 CNI와 네트워크 정책
- OpenTelemetry - eBPF 관측 데이터를 trace, metric과 연계
- 컨테이너 보안 - runtime detection과 syscall 관측

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: eBPF 답안은 커널 hook, verifier, map, 네트워크 관측 지표, 권한 리스크를 함께 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: eBPF는 커널 hook 지점에서 검증된 프로그램을 실행해 네트워크와 시스템 이벤트를 실시간 수집하는 커널 확장 기술임.
> 2. **가치**: 애플리케이션 코드 변경 없이 TCP, DNS, HTTP, syscall 지표를 pod, process, namespace 단위로 관측함.
> 3. **판단 포인트**: verifier 통과, hook 위치, 커널 버전, map 메모리, CAP_BPF 권한, p95 지연과 drop count를 기준으로 운영해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 커널 기반 관측 원리 확인 | hook, verifier, BPF map, ring buffer | 패킷 캡처 도구로만 설명 |
| 클라우드 네이티브 적용 확인 | pod label, service flow, XDP/TC | 애플리케이션 로그와 혼동 |
| 운영 리스크 판단 확인 | 권한, 커널 호환성, 오버헤드 | 무침습·무비용으로 단정 |

> 요약: 이 문제는 eBPF를 관측 위치와 검증 메커니즘 중심으로 설명해야 함.

---

## Ⅰ. 개요 및 필요성

eBPF는 커널 내 관측 실행 기술임. 컨테이너 환경은 프로세스와 네트워크 경로가 동적으로 변해 기존 로그 중심 방식만으로 병목 원인을 찾기 어렵다. eBPF는 커널 이벤트 지점에서 패킷, syscall, 지연, drop을 수집해 서비스 단위 원인 분석을 지원한다.

---

## Ⅱ. 구조 및 구성요소

```text
Kernel Hook -> eBPF Program -> Verifier -> BPF Map/Ring Buffer -> User Agent -> Backend
  / Network: XDP/TC/socket
  / Trace: kprobe/tracepoint
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Hook Point | 관측 또는 제어 위치 | XDP, TC, kprobe, tracepoint |
| Verifier | 안전성 검증 | loop, memory access 제한 |
| BPF Map | 커널과 사용자 공간 데이터 공유 | hash, array, LRU map |
| User Agent | metric, log, trace 변환 | Prometheus, OTLP 전송 |

> 요약: eBPF는 커널 hook에 프로그램을 붙이고 map을 통해 사용자 공간 관측 시스템으로 데이터를 전달함.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로그램 작성 -> bytecode 로드 -> verifier 검증 -> hook attach -> event 수집 -> map 저장 -> backend 전송
  / 검증 실패 -> load 거부
  / map 초과 -> drop 또는 eviction
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | eBPF 프로그램 컴파일과 로드 | CO-RE, BTF 호환 |
| 2 | verifier가 메모리와 종료성 검증 | load reject 0건 |
| 3 | XDP, TC, kprobe에 attach | attach success 100% |
| 4 | event를 map과 ring buffer에 저장 | lost event 비율 |
| 5 | agent가 지표를 backend로 전송 | p95 지연, drop count |

> 요약: eBPF는 검증, 부착, 수집, 전달의 순서로 동작하며 검증 실패 시 커널 적재가 차단됨.

---

## Ⅳ. 특징

| 구분 | 기존 에이전트/sidecar | eBPF 관측 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 관측 위치 | 애플리케이션·프록시 | 커널 공통 경로 | 코드 변경 0건 |
| 범위 | 언어별 계측 필요 | process, pod, socket 단위 | coverage 95% 이상 |
| 처리 | 사용자 공간 수집 | 커널 event 수집 | CPU overhead 5% 이하 목표 |
| 제약 | SDK 배포 부담 | 커널 버전·권한 제약 | kernel 5.x, CAP_BPF |

> 요약: eBPF는 코드 수정 없는 관측 범위를 제공하지만 커널 호환성과 권한 통제가 전제임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SDK instrumentation | kernel-level 관측 | 다언어 서비스와 legacy binary |
| 비용/처리 | sidecar hop | hook event 처리 | CPU overhead 5% 이하 |
| 운영/위험 | 배포 단위 많음 | 노드 agent 중심 | 커널 호환성 관리 가능 여부 |

> 요약: 다언어·legacy·컨테이너 혼재 환경에서 eBPF 관측의 적용 가치가 큼.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 커널 호환 실패 | BTF, helper 차이 | CO-RE, 지원 커널 매트릭스 | attach failure |
| 데이터 손실 | ring buffer 포화 | buffer sizing, sampling | lost event 비율 |
| 권한 남용 | CAP_BPF, privileged agent | RBAC, node taint, audit | privileged agent 수 |

> 요약: eBPF 리스크는 커널 호환, event 손실, 권한 남용을 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리 | CPU overhead 5% 이하 | node exporter, perf |
| 관측 | flow coverage 95% 이상 | service map, trace 비교 |
| 품질 | lost event 1% 이하 | agent metric |

> 요약: eBPF 관측은 overhead, coverage, lost event를 함께 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 관측 대상 선정: TCP retransmit, DNS latency, HTTP status, syscall event를 pod label과 namespace 기준으로 수집
2. 운영 기준 설정: CPU overhead 5% 이하, lost event 1% 이하, flow coverage 95% 이상을 rollout gate로 지정
3. 권한 통제: CAP_BPF와 privileged agent를 전용 namespace, RBAC, nodeSelector, audit log로 제한

**결론 (2줄):**
- 기술사 판단: 다언어 MSA와 legacy binary가 혼재하면 eBPF 관측, 비즈니스 span 의미가 필요하면 SDK 계측을 병행함
- 향후 방향: eBPF, OpenTelemetry, Cilium Hubble이 네트워크와 애플리케이션 관측을 연결하는 표준 조합이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "eBPF를 설명하시오", "기술하시오" | verifier, hook attach, map 전달 흐름 | SDK·sidecar 대비 관측 위치 차이 |
| 요구사항 명시형 | "관측성 방안을 제시하시오", "설계하시오" | TCP/DNS/HTTP 지표 수집 경로 | overhead, coverage, 권한 통제 기준 |

> 요약: 설명형은 커널 실행 원리, 설계형은 관측 지표와 운영 리스크 중심으로 전환함.
