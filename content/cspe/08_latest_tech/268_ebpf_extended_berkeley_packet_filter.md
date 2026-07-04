---
title: "eBPF 확장 BPF (Extended Berkeley Packet Filter)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 268
---

# 📖 【암기용】 개념 완전 이해

> 목적: eBPF를 커널을 직접 수정하지 않고 검증된 작은 프로그램을 커널 훅에서 실행하는 기술로 이해하게 만든다.

## 한눈에
- **개요**: 커널 이벤트 지점에 검증된 프로그램을 붙여 네트워크, 보안, 관측성 기능을 수행하는 실행 기술
- **왜 필요한가**: 커널 모듈은 권한과 장애 위험이 크고, 사용자 공간 에이전트만으로는 패킷·시스템콜·스케줄링 정보를 세밀하게 보기 어렵다.
- **핵심 직관**: 도로 전체를 뜯어고치지 않고 검문소마다 검증된 작은 규칙표를 붙여 통과 여부와 기록을 처리하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 커널 수준 네트워크·보안 처리는 낮은 지연과 상세 이벤트 접근이 필요하지만 커널 패치와 모듈 배포는 장애 반경이 크다.
- **작동 원리**: eBPF 프로그램은 verifier 검증을 통과한 뒤 JIT 또는 인터프리터로 실행되며, map을 통해 사용자 공간과 상태를 공유한다.
- **비유**: 건물 관리 규칙을 건물 구조 변경 없이 각 출입문 센서에 배포하는 방식이다.
- **구체 예시**: XDP hook에서 DDoS 패킷을 NIC 수신 직후 차단하거나 kprobe에서 특정 시스템콜 호출 횟수를 집계한다.
- **흔한 오해·주의점**: eBPF는 단순 패킷 필터가 아니다. 네트워킹, tracing, security, observability에 활용되지만 verifier 제약과 커널 버전 차이를 고려해야 한다.

## 연결 개념
- Cilium — eBPF 기반 Kubernetes 네트워킹·보안 구현
- Cloud Native Observability — 커널 이벤트 기반 telemetry 수집
- XDP — 네트워크 드라이버 초기 지점에서 패킷을 처리하는 hook

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: eBPF는 hook, verifier, map, helper, user space loader를 함께 설명해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: eBPF는 커널 훅에서 검증된 프로그램을 실행해 네트워크·보안·관측성 처리를 수행하는 기술임.
> 2. **가치**: 커널 수정 없이 XDP, tc, kprobe, tracepoint 등에서 패킷과 시스템 이벤트를 처리함.
> 3. **판단 포인트**: verifier 제약, 커널 버전, 권한 모델, map 메모리 사용량을 기준으로 적용해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 커널 확장 구조 이해 확인 | hook, verifier, helper, map | 커널 모듈과 동일하게 설명 |
| 적용 영역 확인 | XDP, tracing, security, observability | 패킷 필터 용도로만 한정 |
| 운영 리스크 판단 확인 | 커널 호환성, 권한, verifier reject | 검증 없는 커널 실행으로 오기술 |

> 요약: 이 문제는 eBPF가 안전 검증을 거쳐 커널 이벤트 지점에서 동작하는 구조를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 검증형 커널 훅 프로그램
- 배경: 커널 모듈은 장애 반경이 크고 사용자 공간 에이전트는 커널 이벤트 접근 범위가 제한됨.
- 필요성: 네트워크 정책, 런타임 보안, 분산 관측성을 커널 수정 없이 적용해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Space Loader -> eBPF Verifier -> JIT / Interpreter -> Kernel Hook
Kernel Hook -> eBPF Program -> Helper Function / Map -> Event Output
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Hook | 프로그램 실행 지점 제공 | XDP, tc, kprobe, tracepoint |
| Verifier | 프로그램 안전성 검증 | bounded loop, memory access 검사 |
| Map | 커널·사용자 공간 상태 공유 | hash, array, ring buffer |
| Helper | 제한된 커널 기능 호출 | helper별 사용 가능 hook 제한 |

> 요약: eBPF는 loader가 프로그램을 적재하고 verifier 검증 후 hook에서 map·helper와 함께 실행된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로그램 작성 -> bytecode 컴파일 -> loader 적재
-> verifier 검증 -> hook 연결 -> 이벤트 발생
-> eBPF 실행 -> map 갱신 / event 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | C/Rust 기반 eBPF 코드를 bytecode로 컴파일 | ELF section |
| 2 | loader가 커널에 프로그램과 map 생성 요청 | syscall 성공 |
| 3 | verifier가 메모리 접근과 종료 가능성 검사 | verifier pass |
| 4 | hook 이벤트에서 프로그램 실행 후 결과 기록 | drop count, event count |

> 요약: eBPF는 적재 전 검증을 통과한 프로그램만 커널 hook에서 실행되며 map을 통해 결과를 전달한다.

---

## Ⅳ. 특징

| 구분 | 커널 모듈 | eBPF | 판단 기준 |
|:---|:---|:---|:---|
| 배포 방식 | 커널 확장 모듈 | verifier 통과 프로그램 | 장애 반경 |
| 안전 장치 | 개발자 책임 중심 | verifier, helper 제한 | 메모리 접근 검증 |
| 적용 위치 | 넓은 커널 내부 | 지정 hook 중심 | hook 제공 여부 |
| 운영 제약 | 커널 ABI 영향 | 커널 버전·BTF 차이 | 배포 대상 kernel matrix |

> 요약: eBPF는 커널 모듈보다 실행 범위를 제한해 운영 위험을 낮추지만 hook과 verifier 제약을 받는다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | user-space agent | kernel hook eBPF | syscall·packet 수준 이벤트 필요 |
| 비용/성능 | context switch 발생 | 커널 경로에서 처리 | 패킷 처리 지연 예산 |
| 운영/위험 | 배포 단순 | kernel capability 필요 | 권한·호환성 관리 |

> 요약: 커널 이벤트를 세밀하게 처리해야 하면 eBPF, 애플리케이션 지표만 필요하면 user-space agent가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| verifier reject | 포인터·루프·helper 제약 위반 | CO-RE, verifier log 분석 | load failure rate |
| 커널 호환성 | BTF·helper 지원 차이 | kernel matrix 테스트 | supported kernel ratio |
| 권한 오남용 | CAP_BPF, privileged pod 사용 | RBAC, admission policy | privileged workload count |

> 요약: eBPF 리스크는 검증 실패, 커널 호환성, 권한 오남용이며 배포 전 matrix와 권한 정책으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적재 성공 | 대상 노드 load failure 0건 | loader log |
| 처리량 | packet drop 정책 정확도 | XDP/tc counter |
| 관측성 | event loss 허용 범위 이내 | ring buffer lost event |

> 요약: eBPF 운영은 적재 성공률, hook 처리 결과, 이벤트 손실률을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. XDP/tc는 네트워크 정책과 DDoS 필터링에, kprobe/tracepoint는 런타임 관측성과 보안 탐지에 분리 적용함.
2. CO-RE와 BTF 기반 빌드로 커널 구조체 차이를 흡수하고 대상 kernel matrix를 CI에 포함함.
3. privileged 권한을 최소화하고 eBPF loader 전용 ServiceAccount와 admission policy를 분리함.

**결론 (2줄):**
- 기술사 판단: 커널 이벤트 기반 통제가 필요하면 eBPF를 선택하고, 앱 계층 지표 수집만 필요하면 OpenTelemetry agent로 충분함.
- 향후 방향: eBPF는 Kubernetes CNI, runtime security, observability의 공통 기반 기술로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "eBPF를 설명하시오" | verifier 적재와 hook 실행 흐름 | 커널 모듈 대비 차이 |
| 요구사항 명시형 | "클라우드 네이티브 보안 방안을 제시하시오" | XDP·tracepoint 적용 절차 | 권한·호환성·이벤트 손실 리스크 |

> 요약: 설명형은 실행 구조를, 보안·운영형은 hook 선택과 권한 통제를 중심으로 작성한다.
