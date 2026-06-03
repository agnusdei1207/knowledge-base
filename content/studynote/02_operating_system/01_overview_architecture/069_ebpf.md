+++
title = "69. BPF (Berkeley Packet Filter) / eBPF (Extended BPF) - 커널 내 샌드박스 프로그램"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: eBPF(Extended BPF)는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스코드를 수정하지 않고도 커널 공간에서 안전하게 실행되는 샌드박스형 프로그램 프레임워크다.
> 2. **가치**: 네트워킹, 관측성(Observability), 보안, 트레이싱을 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수정 없이 동적으로 확장할 수 있어 운영 위험 없이 강력한 기능을 얻는다.
> 3. **판단**: 검증기(Verifier)와 제한된 실행 모델(루프 제한, 메모리 안전성)이 안전성의 핵심이며, LKM 대비 훨씬 낮은 위험으로 커널 수준의 기능을 구현한다.

---

## Ⅰ. 개요 및 필요성

BPF(Berkeley Packet Filter)는 1992년 로렌스 버클리 연구소(LBL)에서 효율적인 패킷 필터링을 위해 개발된 기술이다. 초기에는 `tcpdump`와 같은 패킷 캡처 도구가 모든 패킷을 사용자 공간으로 복사한 뒤 필터링하는 비효율적인 방식을 사용했다. BPF는 필터 프로그램을 커널 공간에서 직접 실행함으로써 불필요한 패킷을 커널 단계에서 버릴 수 있게 했다. 이를 통해 사용자 공간으로 전달되는 데이터량을 대폭 줄이고, 패킷 필터링 성능을 획기적으로 향상시켰다.

2014년 Alexei Starovoitov가 BPF를 근본적으로 재설계하여 eBPF(Extended BPF)를 리눅스 커널 3.18에 도입했다. eBPF는 단순한 패킷 필터를 넘어, 커널의 거의 모든 지점에 프로그램을 붙일(attach) 수 있는 범용 커널 확장 프레임워크로 진화했다. 네트워킹, 관측성(Observability), 보안, 성능 분석 등 다양한 분야에서 커널 수정 없이 강력한 기능을 구현할 수 있다.

현재 eBPF는 Linux 커뮤니티에서 가장 혁신적인 기술 중 하나로 평가받는다. Cilium(네트워킹), Falco(보안), BCC/bpftrace(관측성), Katran(로드밸런싱) 등 오픈소스 프로젝트들이 eBPF를 핵심으로 삼고 있다. Meta, Netflix, Google, Cloudflare 등 대형 기업들이 핵심 인프라에 eBPF를 활용한다.

- **📢 섹션 요약 비유**: 안전한 유리창 너머로 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안을 들여다보고 제어하는 망원경이다. 직접 들어가는 위험 없이 원하는 것을 볼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### eBPF 전체 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">사용자 공간(User Space)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C 코드 → LLVM/Clang 컴파일 → eBPF 바이트코드</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BPF 시스템 콜(bpf()) → 커널 전달</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BPF Map 조작(데이터 읽기/쓰기)</div></div>
<div class="kb-diagram-note">↓ sys_bpf()</div>
<div class="kb-diagram-note">커널 공간(Kernel Space)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Verifier (검증기)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 안전성 검사</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 무한 루프 불가 (유계 루프만 허용)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 초기화되지 않은 메모리 접근 금지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 권한 검사 (CAP_BPF 필요)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 스택 크기 제한 (512 Bytes)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 검증 통과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">JIT 컴파일러 (Just-In-Time)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 네이티브 기계어 변환</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Hook Points (연결 지점)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- kprobe / kretprobe (커널 함수 진입/반환)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- tracepoint (정적 추적 지점)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- XDP (eXpress Data Path - NIC 수준)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- tc (Traffic Control - 네트워크 스택)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- socket filter</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- cgroup (컨테이너 자원 제어)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- LSM hook (보안 정책)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BPF Maps (상태 저장 공유 메모리)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Hash Map / Array Map / Ring Buffer / LRU Map ...</div></div>
</div>
</div>



### 핵심 구성 요소 상세

| 구성 요소 | 역할 | 비고 |
| :--- | :--- | :--- |
| eBPF 바이트코드 | LLVM이 컴파일한 가상 명령어 집합 | 64비트 RISC 형태 |
| Verifier(검증기) | 프로그램 안전성 정적 분석 | 실행 전 전수 경로 검사 |
| JIT Compiler | 바이트코드 → 네이티브 기계어 | x86, ARM64, RISC-V 지원 |
| Hook Point | 프로그램을 연결할 커널 이벤트 지점 | 수백 개 지점 지원 |
| BPF Map | 커널↔사용자 공간 데이터 공유 저장소 | 퍼시스턴트 데이터 |
| BPF Helper | 커널이 제공하는 안전한 API 함수 | 약 200여 개 |
| libbpf | 사용자 공간 BPF 로딩 라이브러리 | CO-RE 지원 |

### BPF Map 주요 타입

| Map 타입 | 설명 | 용도 |
| :--- | :--- | :--- |
| BPF_MAP_TYPE_HASH | 해시 테이블 | IP 주소 매핑, 카운터 |
| BPF_MAP_TYPE_ARRAY | 고정 인덱스 배열 | 통계, 상태 저장 |
| BPF_MAP_TYPE_RINGBUF | 링 버퍼 (커널→사용자) | 이벤트 스트리밍 |
| BPF_MAP_TYPE_PERF_EVENT_ARRAY | perf 이벤트 배열 | 성능 데이터 수집 |
| BPF_MAP_TYPE_LPM_TRIE | 최장 접두사 매칭 트리 | IP 라우팅 |
| BPF_MAP_TYPE_SOCKMAP | 소켓 맵 | 소켓 리다이렉트 |

### eBPF 프로그램 예시 (bpftrace)

```
# 커널 함수 실행 횟수 추적
bpftrace -e 'kprobe:do_sys_open { @[comm] = count(); }'

# 네트워크 패킷 지연 측정
bpftrace -e 'kprobe:tcp_sendmsg { @start[tid] = nsecs; }
             kretprobe:tcp_sendmsg /@start[tid]/
             { @ns = hist(nsecs - @start[tid]); delete(@start[tid]); }'
```

- **📢 섹션 요약 비유**: 놀이기구에 타기 전에 안전 점검(검증기)을 통과해야 하는 것처럼, eBPF 프로그램도 커널에서 실행되기 전에 반드시 안전 검사를 통과해야 한다.

---

## Ⅲ. 비교 및 연결

### eBPF vs LKM 비교

| 항목 | eBPF | LKM |
| :--- | :--- | :--- |
| 실행 공간 | 커널 내 샌드박스 | 커널 공간(Ring 0 직접) |
| 안전성 | Verifier가 정적 보장 | 버그 시 커널 패닉 가능 |
| 기능 복잡도 | 제한적 (단순 로직) | 매우 복잡한 구현 가능 |
| 개발 용이성 | 높음 (C + libbpf) | 중간 (커널 내부 지식 필요) |
| 권한 요구 | CAP_BPF (비root 가능) | root 필요 |
| 주요 용도 | 관측성, 보안, 네트워킹 | 드라이버, 파일시스템 |
| 재부팅 | 불필요 | 불필요 |
| 커널 ABI 의존 | CO-RE로 완화 | 강한 의존성 |

### eBPF 활용 사례

| 분야 | 도구/프로젝트 | 설명 |
| :--- | :--- | :--- |
| 네트워킹 | Cilium | 쿠버네티스 CNI, XDP 기반 로드밸런싱 |
| 보안 | Falco, Tetragon | 런타임 위협 탐지 |
| 관측성 | BCC, bpftrace | 커널 함수 추적, 성능 분석 |
| 성능 분석 | BPF perf tools | CPU, 메모리, I/O 프로파일링 |
| 로드밸런싱 | Katran (Meta) | L4 로드밸런서 |
| 방화벽 | XDP drop | 초고속 패킷 드롭 |

### BPF vs eBPF 진화

| 항목 | 고전 BPF (cBPF) | eBPF |
| :--- | :--- | :--- |
| 도입 | 1992 (BSD), 1997 (Linux) | 2014 (Linux 3.18) |
| 목적 | 패킷 필터링 | 범용 커널 확장 |
| 레지스터 | 2개 | 11개 |
| 맵(Map) | 없음 | 다양한 맵 타입 |
| JIT | 제한적 | x86/ARM64/RISC-V 지원 |
| Hook 지점 | 소켓 필터만 | 수백 개 지점 |

eBPF는 커널을 고치지 않고도 확장할 수 있어 운영 부담이 적다. 그러나 Verifier의 제약(루프 횟수 제한, 스택 크기 제한)으로 인해 복잡한 로직 구현에는 한계가 있다.

- **📢 섹션 요약 비유**: 벽에 구멍을 내지 않고 무선 카메라를 설치하는 방식이다. 벽(커널)을 손상시키지 않고도 원하는 정보를 얻을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. Verifier가 통과하도록 루프를 유계(bounded) 형태로 작성했는가?
2. BPF Map의 타입을 용도에 맞게 선택했는가? (Hash vs Array vs RingBuf)
3. CO-RE(Compile Once, Run Everywhere)를 활용해 커널 버전 이식성을 확보했는가?
4. 적절한 Hook 지점을 선택했는가? (XDP는 NIC 수준, tc는 소프트웨어 스택)
5. BPF Helper 함수를 통해서만 커널 자원에 접근하는가?
6. eBPF 프로그램의 성능 영향(오버헤드)을 측정했는가?
7. 보안 정책상 CAP_BPF 권한 부여가 적절한가?
8. 커널 버전 호환성(최소 커널 버전)을 확인했는가?

### 안티패턴

- **eBPF를 LKM 대체제로 완전히 동일시하는 오해**: eBPF는 복잡한 드라이버나 파일시스템을 구현하는 데 적합하지 않다. LKM이 필요한 영역과 eBPF가 적합한 영역을 구분해야 한다.
- **Verifier 통과만을 목표로 코드 왜곡**: 검증을 위해 실제 로직을 비틀어 작성하면 유지보수가 불가능해진다. 설계 단계에서 eBPF의 제약을 반영해야 한다.
- **무분별한 Hook 남발**: 너무 많은 kprobe를 달면 모든 해당 함수 호출 시 성능 오버헤드가 발생한다. 필요한 최소 Hook만 사용해야 한다.
- **커널 버전 의존 코드 하드코딩**: 구조체 오프셋을 직접 하드코딩하면 커널 버전 변경 시 동작하지 않는다. BTF(BPF Type Format)와 CO-RE를 활용해야 한다.

기술사 관점에서는 eBPF를 "커널 내 안전 실행 프레임워크"로 설명하되, BPF 바이트코드-검증기-JIT-Hook-Map의 전체 파이프라인과 LKM 대비 안전성 향상의 이유를 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: 안전장치(Verifier)가 있는 커널 전용 작업대다. 누구나 도구를 사용할 수 있지만, 위험한 도구는 처음부터 못 쓰도록 막혀 있다.

---

## Ⅴ. 기대효과 및 결론

eBPF 도입으로 얻을 수 있는 효과는 운영 측면과 기술 측면 모두에서 크다. 운영 측면에서는 커널 수정 없이 네트워크 정책, 보안 규칙, 성능 분석 코드를 동적으로 배포/제거할 수 있어 배포 위험이 LKM 대비 현저히 낮다. 개발 속도도 빨라진다. 기술 측면에서는 XDP를 활용하면 DPDK(커널 우회 패킷 처리) 수준의 패킷 처리 성능을 일반 커널 스택에서 달성할 수 있다. DDoS 방어, 초저지연 로드밸런싱 등이 eBPF로 구현 가능해진다.

쿠버네티스 환경에서 Cilium은 eBPF를 활용해 기존 iptables 기반 네트워크 정책보다 수십 배 빠른 처리를 달성했다. 보안 관측성 분야에서는 Falco와 Tetragon이 시스템 콜 수준의 위협 행위를 실시간으로 탐지한다.

미래에는 eBPF가 리눅스를 넘어 Windows 커널에도 적용되는 방향으로 Microsoft가 연구 중이다. "모든 커널 확장은 eBPF로"라는 방향성이 시스템 소프트웨어 분야의 주류 트렌드가 될 것으로 전망된다. 결론적으로 eBPF는 커널 내 안전한 실행 환경을 제공하여, 기존 LKM이 가지던 안전성 위험을 획기적으로 낮추면서도 강력한 커널 수준 기능을 제공하는 혁신적인 프레임워크다.

- **📢 섹션 요약 비유**: 안전하게 커널을 더 똑똑하게 만드는 도구다. 마치 스마트폰 앱처럼, 커널 기능을 안전하게 확장하고 제거할 수 있는 앱 스토어와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 고전 BPF | eBPF의 전신, 패킷 필터링 전용 |
| LKM | eBPF의 더 위험한 대안, 복잡한 기능에 사용 |
| XDP | eBPF의 NIC 수준 Hook, 초고속 패킷 처리 |
| kprobe/tracepoint | 커널 함수 추적 Hook 지점 |
| Cilium | eBPF 기반 쿠버네티스 네트워킹 |
| BTF/CO-RE | eBPF 이식성 프레임워크 |
| 관측성(Observability) | eBPF의 핵심 활용 영역 |
| JIT | eBPF 바이트코드를 네이티브 코드로 변환 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">tcpdump 비효율 (사용자 공간 필터링)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BPF 등장 (1992, 커널 내 패킷 필터)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">리눅스 BPF 도입 (1997, Linux 2.1.75)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">eBPF 탄생 (2014, Linux 3.18, 범용 확장)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Maps, Helper, JIT 강화 (2015~2018)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">BTF (BPF Type Format) 도입 → CO-RE 지원</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Cilium, BCC, bpftrace 에코시스템 성장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">LSM BPF, fentry/fexit 고급 Hook 추가</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Windows eBPF 연구, 범용 커널 확장 표준화</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 커널(컴퓨터 두뇌) 안에서 일어나는 일을 안전한 유리창 너머로 볼 수 있어요.
2. 검문소(Verifier)를 통과한 안전한 프로그램만 커널 안에서 실행될 수 있어요.
3. eBPF는 그 검문소가 있는 특별한 안경이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 800

← **이전**: [68. 동적 커널 패치 (Live Patching) - kpatch, kGraft](/knowledge-base/studynote/02_operating_system/01_overview_architecture/068_live_patching/)
**다음**: [70. 하드웨어 추상화 계층 (HAL, Hardware Abstraction Layer)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/070_hal/) →

---
