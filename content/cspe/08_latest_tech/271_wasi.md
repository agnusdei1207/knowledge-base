---
title: "WASI 웹어셈블리 시스템 인터페이스 (WebAssembly System Interface)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 271
---

# 📖 【암기용】 개념 완전 이해

> 목적: WASI를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: WebAssembly(Wasm)가 브라우저 밖에서도 파일, 네트워크 등 운영체제 자원을 안전하게 쓸 수 있게 해주는 표준 인터페이스
- **왜 필요한가**: Wasm은 샌드박스 안에서만 돌아가서 외부와 단절되어 있다. 서버나 엣지에서 돌리려면 파일 읽기나 시간 측정 같은 "시스템 호출"이 필요한데, 이를 브라우저 종속성 없이 표준화한 것이 WASI다.
- **핵심 직관**: Wasm을 위한 "POSIX" 같은 운영체제 추상화 계층이다. 어디서나 돌아가는(Write Once, Run Anywhere) 안전한 서버사이드 실행 환경을 만든다.

## 깊이 이해
- **배경·문제의식**: 기존 Wasm은 브라우저의 JavaScript API에 의존했다. 하지만 클라우드 네이티브, 서버리스 환경에서 Wasm을 쓰려면 플랫폼(OS)에 독립적인 표준 입출력 방식이 절실했다.
- **작동 원리**: **Capability-based Security** 모델을 따른다. 프로그램이 파일 전체에 접근하는 게 아니라, 특정 파일 핸들(권한)만 넘겨받아 동작한다. WASI-libc를 통해 C/C++ 등의 코드를 Wasm으로 컴파일하면 OS 레벨 호출이 WASI 호출로 치환되어 런타임(Wasmtime 등)에서 실행된다.
- **비유**: 해외 여행(Wasm 실행)을 가는데, 각 나라 언어(OS별 API)를 배우는 대신 "공용 수동태(WASI)"를 써서 통역사(런타임)를 통해 의사소통하는 것과 같다. 또한 통역사는 허락된 주제(Capability)만 통역해준다.
- **구체 예시**: `wasi-libc`를 사용해 작성된 Rust 코드를 `wasm32-wasi` 타겟으로 빌드하면, 리눅스에서도 윈도우에서도 동일한 `.wasm` 파일로 파일 입출력이 가능하다.
- **흔한 오해·주의점**: WASI는 운영체제가 아니다. Wasm 런타임과 외부 세계를 잇는 "규약"일 뿐이다.

## 연결 개념
- WebAssembly (Wasm) — 실행 바이너리 포맷
- Wasmtime, Wasmer — WASI를 지원하는 대표적 런타임
- POSIX — 전통적인 OS 인터페이스 표준 (WASI가 지향하는 모델)
- Component Model — WASI 프리뷰 2의 핵심 아키텍처

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: WASI를 단순 API 집합이 아닌, Wasm의 비브라우저 확장과 보안 모델(Capability-based) 관점에서 서술한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WASI는 WebAssembly 가상머신이 호스트 운영체제의 자원(I/O, File, Net)에 접근할 수 있도록 정의된 플랫폼 독립적 시스템 인터페이스 표준이다.
> 2. **가치**: 경량 샌드박스 보안과 하드웨어 네이티브에 근접한 성능을 결합하여, 컨테이너를 대체하거나 보완하는 클라우드 네이티브 실행 환경을 제공한다.
> 3. **판단 포인트**: 기존 POSIX와 달리 기능 기반 보안(Capability-based Security)을 채택하여 공급망 공격 리스크를 원천 차단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Wasm의 서버사이드 확장 원리 이해 확인 | Capability-based Security, 플랫폼 독립성, WASI Preview 2(Component Model) | 단순히 "Wasm용 API"라고만 서술 (보안 모델 누락) |
| 클라우드 네이티브 기술 변화 인지 확인 | Docker와 비교(경량성, 기동속도), 서버리스 적용 사례 | Wasm이 JS를 대체하는 기술로만 한정하여 서술 |
| 표준화 동향 및 보안 메커니즘 확인 | Bytecode Alliance, wit(Wasm Interface Type), 모듈 격리 | 런타임(Wasmtime)과 인터페이스(WASI)를 혼동 |

> 요약: Wasm의 이식성을 브라우저 밖(Non-Web)으로 확장하는 핵심 규격이며, 보안과 표준 인터페이스가 논점이다.

---

## Ⅰ. 개요 및 필요성

- 정의: WebAssembly가 호스트 OS의 파일 시스템, 네트워크, 시간 등에 접근하기 위해 정의된 이식 가능한 시스템 인터페이스 표준
- 배경: Wasm은 브라우저 내 JS API 의존적이었으나, 클라우드·엣지 컴퓨팅 확산을 위해 플랫폼 독립적 실행 환경 규격이 필요
- 필요성: 컨테이너 대비 10~100배 빠른 기동속도와 경량 메모리 점유를 구현하여 서버리스 및 마이크로서비스 효율 극대화

---

## Ⅱ. 구조 및 구성요소

```text
User Application (C/C++, Rust, Go)
       | (Standard Library / WASI-libc)
WebAssembly Module (.wasm)
       | (WASI Calls: fd_read, path_open, etc.)
WASI Interface Layer (Abstraction)
       | (Runtime Implementation: Wasmtime, Wasmer)
Host OS (Linux, Windows, macOS, IoT OS)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| WASI-libc | 표준 C 라이브러리를 Wasm용으로 구현 | 시스템 호출을 WASI 함수로 매핑 |
| Wasm 런타임 | WASI 규격을 실제로 호스트 OS API로 구현 | Wasmtime, Wasmer, WAMR 등 |
| wit (Wasm Interface Type) | 컴포넌트 간 인터페이스 정의 언어 | Preview 2부터 도입된 언어 독립 규격 |
| Capability Handle | 특정 자원에 대한 접근 권한 증표 | 파일 경로 대신 파일 디스크립터(fd) 전달 |

> 요약: 상위 애플리케이션의 시스템 호출을 추상화하여, 런타임이 호스트 OS에 맞게 실행하는 계층 구조를 가진다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Build Time: Source Code -> LLVM -> WASI-libc -> Wasm Module
Runtime: Load Wasm -> Grant Capabilities -> Instantiate -> Execute
            |                |
            +-> fd_open ---->+-> Host System Call (open)
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 컴파일 단계 | WASI-libc를 링크하여 OS 의존 코드를 WASI API로 변환 |
| 2 | 권한 부여 (Pre-opening) | 실행 시 런타임이 특정 디렉토리/자원만 모듈에 매핑 (샌드박스) |
| 3 | 인터페이스 호출 | 모듈 내부에서 `fd_read` 등 호출 시 런타임이 가로챔 |
| 4 | 호스트 실행 | 런타임이 호스트 OS의 실제 API(예: `read()`)로 변환 실행 |

> 요약: 컴파일 시 표준 인터페이스로 고정하고, 실행 시 런타임이 허가된 자원에 한해 호스트 API와 연결한다.

---

## Ⅳ. 특징

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 보안성 | Capability-based Security (기능 기반 권한 부여) | 파일 시스템 전체가 아닌 특정 핸들만 접근 |
| 이식성 | 플랫폼 독립 바이너리 (Write Once, Run Anywhere) | 소스 수정 없이 리눅스/윈도우/엣지 동일 실행 |
| 고성능 | 네이티브에 근접한 실행 속도, ms 단위 콜드스타트 | 컨테이너 대비 오버헤드 90% 이상 절감 |
| 확장성 | WASI Preview 2 (Component Model) 지원 | 언어 간 경계를 허무는 모듈 조합 가능 |

> 요약: 강력한 보안(샌드박스)과 플랫폼 독립적 성능을 동시에 확보하여 '제2의 Docker'로 불리는 기술적 토대를 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Docker / Container | WebAssembly + WASI | 선택 기준 |
|:---|:---|:---|:---|
| 격리 단위 | OS 커널 레벨 (Namespace/Cgroup) | 가상머신/샌드박스 레벨 | 멀티테넌시 보안 강도 요구사항 |
| 기동 속도 | 초(Seconds) 단위 | 밀리초(Milliseconds) 단위 | 서버리스, 스케일아웃 민감도 |
| 이식성 | OS/아키텍처 종속적 (Multi-arch 필요) | 아키텍처 완전 독립 | 엣지/IoT 이기종 장치 배포 환경 |

> 요약: 대규모 레거시 앱은 Docker가 유리하나, 고성능 서버리스나 극경량 엣지 환경에서는 WASI 기반 Wasm이 압도적이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 표준 미성숙 | Preview 2 전환기에 따른 API 변화 | Bytecode Alliance 로드맵 준수, 호환 계층 사용 | WASI SDK 버전 일치 여부 |
| 생태계 제약 | 일부 언어(Go, Python)의 Wasm 지원 미흡 | TinyGo, Componentize-Py 등 특화 툴 도입 | 지원 언어 런타임 안정성 |
| 네트워크 제약 | WASI-Sockets 표준화 진행 중 (제한적) | Proxy 모듈 또는 런타임별 특화 확장 사용 | 소켓 통신 오버헤드 및 지원 여부 |

> 요약: 기술 성숙도 단계이므로 Preview 2 표준 준수 여부와 언어별 지원 현황을 면밀히 검토해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 기동 지연 (Cold Start) | 10ms 이하 | 런타임 인스턴스화 시간 측정 |
| 메모리 풋프린트 | 1MB 내외 (Hello World 기준) | 프로세스 RSS(Resident Set Size) 모니터링 |
| 보안 취약점 | 샌드박스 탈출 사례 0건 | CVE 리포트 및 레드팀 테스트 |

> 요약: 성능 지표와 보안 격리 수준을 통해 시스템 도입의 타당성을 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 서버리스 플랫폼: AWS Lambda 또는 Cloudflare Workers에서 WASI 기반 Wasm을 사용하여 콜드스타트 지연을 10ms 미만으로 제어
2. 플러그인 시스템: SaaS 솔루션 내부에 사용자 정의 로직을 실행할 때 WASI 샌드박스를 사용하여 호스트 시스템 오염 없이 안전한 확장 제공
3. 엣지 컴퓨팅: 리소스가 제한된 IoT 게이트웨이에서 WASI를 통해 다양한 언어로 작성된 데이터 전송 로직을 통합 운영

**결론 (2줄):**
- 기술사 판단: WASI는 단순한 인터페이스를 넘어 Wasm의 생태계를 서버와 클라우드로 확장하는 '클라우드 운영체제 표준'의 시발점이다.
- 향후 방향: WASI Preview 2의 Component Model이 안착함에 따라, 레고 블록처럼 모듈을 조합하는 새로운 소프트웨어 아키텍처 패러다임이 확산될 것이다.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WASI에 대해 설명하시오" | 전체 계층 구조와 동작 원리 | 보안성, 이식성 등 주요 특징 |
| 요구사항 명시형 | "Wasm의 서버사이드 확장 방안" | WASI-libc 및 런타임 연동 흐름 | Docker와의 비교 및 도입 시 고려사항 |
| 보안 특화형 | "Wasm의 보안 메커니즘" | Capability-based 권한 제어 원리 | 공급망 보안(SBOM) 연계 및 격리 수준 |
