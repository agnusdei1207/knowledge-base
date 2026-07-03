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
- **개요**: eBPF(extended Berkeley Packet Filter)는 **커널 확장 기술**로, 커널을 재컴파일하거나 커널 모듈을 적재하지 않고도 **검증된(verified) 소형 프로그램**을 커널의 특정 이벤트 지점(hook)에 안전하게 삽입해 실행하는 기술이다.
- **왜 필요한가**: 컨테이너·마이크로서비스는 프로세스 수명이 짧고 네트워크 경로가 동적으로 바뀌어, tcpdump나 애플리케이션 로그만으로는 병목·장애 원인을 끝까지 추적하기 어렵다.
- **핵심 직관**: 도로 위 차량을 세워 검문하지 않고, 도로 곳곳에 센서를 심어 번호·속도·흐름을 실시간으로 기록하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| eBPF | 검증된 프로그램을 커널 안에서 실행하는 커널 확장 기술 — 이 문서가 다루는 **대상** | 커널 안에 설치하는 안전한 미니 앱 |
| BPF (원조) | 1992년 등장한 네트워크 패킷 필터링 전용 가상머신 — eBPF의 전신 | 원래는 패킷만 거르던 좁은 필터 |
| Verifier | 프로그램을 커널에 적재하기 전 무한루프·잘못된 메모리 접근을 정적으로 검사하는 컴포넌트 | 코드 심사관 — 위험하면 반려 |
| JIT 컴파일러 | 검증 통과한 bytecode를 CPU 네이티브 명령어로 변환해 실행 속도를 높이는 컴포넌트 | 통역 없이 바로 알아듣게 번역 |
| Hook (부착 지점) | 프로그램이 실행되는 커널 이벤트 지점 — kprobe(함수 진입), tracepoint(정적 이벤트), XDP(NIC 드라이버 진입), TC(트래픽 컨트롤), socket | 센서를 설치하는 실제 위치 |
| BPF Map | 커널 프로그램과 사용자 공간 프로세스가 데이터를 주고받는 공유 자료구조(hash, array, LRU 등) | 커널과 사용자 공간이 함께 쓰는 게시판 |
| Ring Buffer | 이벤트를 순서대로 사용자 공간에 스트리밍하는 고성능 버퍼 | 컨베이어 벨트로 이벤트를 실시간 전달 |
| CO-RE / BTF | "Compile Once - Run Everywhere" — 커널 버전이 달라도 재컴파일 없이 동작하게 하는 타입 정보(BTF) 기반 메커니즘 | 어떤 나라에서도 통하는 표준 규격 |

## 깊이 이해

### 왜 커널이 관측 지점으로 적합한가 (배경)
- BPF는 1992년 BSD에서 패킷 필터링 성능을 높이려고 만든 좁은 목적의 가상머신이었다. 2014년 리눅스 3.18에서 범용 레지스터·맵·다양한 hook을 지원하는 **eBPF**로 확장되며, 네트워크뿐 아니라 파일 접근·syscall·함수 호출까지 다룰 수 있게 됐다.
- 네트워크 패킷도, 파일 접근도, 프로세스 syscall도 결국 커널을 반드시 거친다. 애플리케이션마다 다른 언어·프레임워크로 계측(instrumentation)할 필요 없이, 커널이라는 **공통 관측 지점** 하나에 프로그램을 심으면 모든 프로세스의 이벤트를 동일한 방식으로 볼 수 있다.

### Verifier가 안전을 보장하는 방법 (수치로 이해)
- eBPF 프로그램은 커널 모듈처럼 임의 코드를 실행하는 것이 아니라, 적재 전에 verifier가 프로그램을 그래프로 분석해 다음을 검사한다: ① 모든 경로가 유한 시간에 종료되는가(무한루프 금지, 커널 5.3부터 제한적 bounded loop 허용) ② 메모리 접근이 할당된 범위를 벗어나지 않는가 ③ 명령어 수가 한도(커널 버전에 따라 최대 100만 개 수준)를 넘지 않는가.
- 예: 반복 횟수가 입력 크기에 따라 무한정 늘어날 수 있는 코드는 verifier가 "종료를 증명할 수 없다"며 적재 자체를 거부한다. 이 검증 단계 때문에 eBPF는 커널 모듈보다 커널 크래시 위험이 훨씬 낮다 — 단, "무엇이든 가능"이 아니라 "검증 가능한 것만 가능"이라는 제약이 있다.

### XDP로 보는 패킷 처리 속도 (수치 예)
- XDP(eXpress Data Path)는 NIC 드라이버가 패킷을 커널 네트워크 스택(소켓 버퍼 생성 등)에 올리기 **직전**에 eBPF 프로그램을 실행한다. 스택을 거치지 않으므로 일반 iptables 경로 대비 훨씬 빠르게 패킷을 드롭·리다이렉트할 수 있다 — 예: DDoS 방어에서 초당 수백만 패킷(pps) 단위로 악성 트래픽을 커널 스택 진입 전에 차단한다.
- 반면 kprobe·tracepoint는 이미 발생한 커널 함수 호출·이벤트에 부착돼 관측 목적으로 주로 쓰이며, XDP/TC처럼 패킷 자체를 조작하기보다는 syscall 인자, 함수 지연시간(latency) 같은 값을 map에 기록하는 데 쓰인다.

### 데이터가 커널에서 사용자 공간으로 나오는 경로
- 예: Kubernetes 노드에서 TCP 재전송(retransmit)을 관측한다면, TCP 상태 변화 tracepoint에 프로그램을 붙여 재전송이 발생할 때마다 `(source pod, dest pod, timestamp)`를 hash map에 카운트로 누적하거나 ring buffer로 즉시 흘려보낸다. 사용자 공간의 agent(Prometheus exporter 등)가 이를 주기적으로 읽어 pod label 기준 p95 지연과 drop count로 집계한다.

### 비유와 흔한 오해
- **비유**: 병원에서 환자마다 설문지를 받는 대신, 주요 출입문·검사실·처방 창구에 센서를 달아 환자 흐름을 자동으로 기록하는 방식이다.
- **오해**: "eBPF는 커널 모듈보다 안전하니 제약이 없다"는 생각은 틀렸다. verifier의 명령어 수·루프 제한, 커널 버전별 지원 helper 함수 차이, map 메모리 상한, 적재 권한(CAP_BPF 또는 root)이라는 명확한 제약 안에서만 동작한다.

## 연결 개념
- Cilium - eBPF를 데이터 플레인으로 쓰는 대표적 CNI·네트워크 정책 구현체
- Service Mesh(Istio) - 사이드카 프록시 대신 eBPF로 유사 기능을 구현하려는 대안 축
- OpenTelemetry - eBPF가 수집한 이벤트를 trace·metric 표준 포맷으로 연계
- 컨테이너 보안 - syscall 단위 runtime detection(예: Falco)의 기반 기술

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

- 개요: 커널 내 관측 실행 기술
- 배경: 컨테이너 환경은 프로세스와 네트워크 경로가 동적으로 변해 기존 로그 중심 방식만으로 병목 원인을 찾기 어렵다.
- 필요성: XDP, TC, kprobe 지점에서 패킷, syscall, 지연, drop을 수집해 서비스 단위 원인 분석을 지원한다.

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
