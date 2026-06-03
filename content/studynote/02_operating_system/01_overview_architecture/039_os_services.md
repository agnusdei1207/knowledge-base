+++
title = "039. OS 서비스 (Operating System Services)"
date = 2026-03-04

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

> **핵심 인사이트**
> 1. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 사용자/애플리케이션을 위한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(UI, 프로그램 실행, I/O, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 통신, 에러 처리)와 시스템 효율을 위한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/), 로깅, [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·보안)로 구분되며, 이 모두가 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))을 통해 제공된다.
> 2. 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))은 사용자 모드(User Mode) 애플리케이션이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) Mode) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 요청하는 유일한 합법적 진입점으로, CPU의 모드 전환 메커니즘이 보안의 핵심 경계를 형성한다.
> 3. OS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 아키텍처는 모놀리식 vs 마이크로커널의 근본 트레이드오프를 결정 — 모놀리식은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간에서 직접 실행(빠름), 마이크로커널은 사용자 공간 서버로 분리(안전·이식성).

---

## I. OS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

```
OS 서비스 두 가지 범주:

사용자를 위한 서비스:
  1. 사용자 인터페이스 (UI)
     CLI, GUI, 터치 인터페이스
     
  2. 프로그램 실행
     프로그램 로드, 실행, 종료
     
  3. I/O 작업
     파일/장치 I/O 추상화
     
  4. 파일 시스템 조작
     파일 생성/읽기/쓰기/삭제, 권한 관리
     
  5. 통신
     프로세스 간 통신 (IPC), 네트워크
     
  6. 오류 탐지 및 처리
     하드웨어/소프트웨어 오류 감지

시스템 효율을 위한 서비스:
  7. 자원 할당 (CPU, 메모리, I/O)
  8. 로깅 및 계정 관리
  9. 보호 및 보안
```

> 📢 **섹션 요약 비유**: OS는 호텔 — 고객 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(프로그램 실행, I/O)와 내부 관리([자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/), 보안)를 동시에 운영.

---

## II. 시스템 콜 인터페이스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">시스템 콜 (System Call):</div>
<div class="kb-diagram-note">사용자 모드 -&gt; 커널 모드 전환 메커니즘</div>
<div class="kb-diagram-note">방법: trap/int 명령어 (x86: int 0x80 또는 syscall)</div>
<div class="kb-diagram-note">계층 구조:</div>
<div class="kb-diagram-note">애플리케이션</div>
<div class="kb-diagram-tree-item" style="--depth:2">표준 라이브러리 (libc: printf, fopen)</div>
<div class="kb-diagram-tree-item" style="--depth:3">시스템 콜 래퍼 (write, open)</div>
<div class="kb-diagram-tree-item" style="--depth:4">커널 (파일 시스템, 장치 드라이버)</div>
<div class="kb-diagram-note">시스템 콜 종류:</div>
<div class="kb-diagram-note">프로세스 제어: fork, exec, exit, waitpid</div>
<div class="kb-diagram-note">파일 관리: open, read, write, close</div>
<div class="kb-diagram-note">장치 관리: ioctl, read, write</div>
<div class="kb-diagram-note">정보 유지: getpid, alarm, sleep</div>
<div class="kb-diagram-note">통신: socket, send, recv, pipe</div>
<div class="kb-diagram-note">예: C에서 printf 호출 시:</div>
<div class="kb-diagram-note">printf() -&gt; write() 시스템 콜 -&gt; 커널 write</div>
<div class="kb-diagram-tree-item" style="--depth:1">파일 디스크립터(stdout) -&gt; 터미널 드라이버</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 시스템 콜은 은행 창구 — 고객(앱)은 창구(시스템 콜)를 통해서만 금고([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)/하드웨어)에 접근, 직접 접근 불가.

---

## III. 사용자 모드 vs [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">듀얼 모드 (Dual Mode) 동작:</div>
<div class="kb-diagram-note">사용자 모드 (User Mode):</div>
<div class="kb-diagram-note">제한된 권한</div>
<div class="kb-diagram-note">하드웨어 직접 접근 불가</div>
<div class="kb-diagram-note">메모리 보호 (자신의 공간만)</div>
<div class="kb-diagram-note">커널 모드 (Kernel Mode / Supervisor Mode):</div>
<div class="kb-diagram-note">모든 하드웨어 접근 가능</div>
<div class="kb-diagram-note">모든 메모리 접근 가능</div>
<div class="kb-diagram-note">보호 레지스터/포트 접근 가능</div>
<div class="kb-diagram-note">전환:</div>
<div class="kb-diagram-note">사용자 -&gt; 커널: 시스템 콜, 인터럽트, 예외</div>
<div class="kb-diagram-note">커널 -&gt; 사용자: 시스템 콜 반환, 인터럽트 처리 완료</div>
<div class="kb-diagram-note">CPU 모드 비트:</div>
<div class="kb-diagram-note">x86: CPL (Current Privilege Level) 0~3</div>
<div class="kb-diagram-note">Ring 0: 커널 (가장 높은 권한)</div>
<div class="kb-diagram-note">Ring 3: 사용자 애플리케이션</div>
<div class="kb-diagram-note">ARM: EL (Exception Level) 0~3</div>
<div class="kb-diagram-note">EL0: 앱, EL1: OS 커널</div>
<div class="kb-diagram-note">EL2: 하이퍼바이저, EL3: 보안 모니터</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 모드 전환은 일반 직원(User)이 금고실([Kernel](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)) 진입 시 보안 카드 태그 — 통과 후 권한 확대, 나올 때 다시 제한.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). OS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">서비스 제공 방식 비교:</div>
<div class="kb-diagram-note">모놀리식 커널 (Monolithic):</div>
<div class="kb-diagram-note">모든 OS 서비스를 커널 공간에서 실행</div>
<div class="kb-diagram-note">서비스 간 직접 함수 호출 (빠름)</div>
<div class="kb-diagram-note">예: Linux, BSD</div>
<div class="kb-diagram-note">단점: 한 드라이버 버그 -&gt; 시스템 전체 충돌</div>
<div class="kb-diagram-note">마이크로커널 (Microkernel):</div>
<div class="kb-diagram-note">최소 커널 (IPC, 메모리 관리, 스케줄링만)</div>
<div class="kb-diagram-note">파일 시스템, 드라이버 -&gt; 사용자 공간 서버</div>
<div class="kb-diagram-note">예: QNX, seL4, macOS(Mach 기반)</div>
<div class="kb-diagram-note">단점: IPC 오버헤드로 느림</div>
<div class="kb-diagram-note">하이브리드:</div>
<div class="kb-diagram-note">Windows: 마이크로커널 아이디어 + 성능상</div>
<div class="kb-diagram-note">executive 서비스는 커널 모드에서 실행</div>
<div class="kb-diagram-note">macOS: Mach 마이크로커널 + BSD 레이어</div>
<div class="kb-diagram-note">엑소커널/유니커널:</div>
<div class="kb-diagram-note">라이브러리 OS: 애플리케이션이 직접 하드웨어 추상화</div>
<div class="kb-diagram-note">컨테이너/VM 경량화 (Unikraft)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 모놀리식은 백화점(모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 한 건물), 마이크로커널은 쇼핑몰 입점 구조(각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 독립 매장) — 빠름 vs 안전성 트레이드오프.

---

## V. 실무 시나리오 — strace 분석



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">strace: 시스템 콜 추적 도구</div>
<div class="kb-diagram-note">명령:</div>
<div class="kb-diagram-note">strace -e trace=file ls /tmp</div>
<div class="kb-diagram-note">출력 예시:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">execve("/bin/ls",</div><div class="kb-diagram-node">"ls", "/tmp"</div><div class="kb-diagram-note">, ...) = 0</div></div>
<div class="kb-diagram-note">openat(AT_FDCWD, "/tmp", O_RDONLY) = 3</div>
<div class="kb-diagram-note">getdents64(3, ...) = 120</div>
<div class="kb-diagram-note">write(1, "file1.txt file2.txt\n", 20) = 20</div>
<div class="kb-diagram-note">close(3) = 0</div>
<div class="kb-diagram-note">분석:</div>
<div class="kb-diagram-note">1. execve: 프로그램 실행 시스템 콜</div>
<div class="kb-diagram-note">2. openat: /tmp 디렉토리 열기</div>
<div class="kb-diagram-note">3. getdents64: 디렉토리 항목 읽기</div>
<div class="kb-diagram-note">4. write: 화면 출력 (fd=1: stdout)</div>
<div class="kb-diagram-note">5. close: 파일 디스크립터 닫기</div>
<div class="kb-diagram-note">성능 분석:</div>
<div class="kb-diagram-note">strace -c ls</div>
<div class="kb-diagram-tree-item" style="--depth:1">시스템 콜별 호출 횟수/시간 통계</div>
<div class="kb-diagram-tree-item" style="--depth:1">느린 시스템 콜 병목 파악</div>
<div class="kb-diagram-note">실무 활용:</div>
<div class="kb-diagram-note">앱 행(hang) 원인 파악 (어떤 syscall에서 대기?)</div>
<div class="kb-diagram-note">파일 접근 경로 추적</div>
<div class="kb-diagram-note">권한 오류 디버깅 (EPERM, EACCES)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: strace는 앱의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 창구 방문 기록 — "언제, 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를, 얼마나 요청했는지" 전부 기록.

---

## 📌 관련 개념 맵

```
OS 서비스
+-- 사용자 서비스
|   +-- UI, 프로그램 실행, I/O
|   +-- 파일 시스템, 통신, 오류 처리
+-- 시스템 서비스
|   +-- 자원 할당, 로깅, 보호·보안
+-- 구현 메커니즘
|   +-- 시스템 콜 (Trap, Interrupt)
|   +-- 듀얼 모드 (User / Kernel)
+-- 아키텍처
    +-- 모놀리식 (Linux)
    +-- 마이크로커널 (QNX)
    +-- 하이브리드 (Windows)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 OS (1950~60s)]
배치 처리, 모놀리식 구조
      |
      v
[UNIX (1969)]
시스템 콜 인터페이스 표준화
사용자/커널 모드 분리
      |
      v
[마이크로커널 연구 (1980s)]
Mach, L4 - 안정성/이식성
      |
      v
[Linux 모놀리식 성공 (1991~)]
성능 vs 구조의 현실적 선택
      |
      v
[현재: 컨테이너/VM 서비스]
exokernel, unikernel 재등장
eBPF로 커널 기능 동적 확장
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. OS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 호텔처럼 고객(앱)을 위한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 인터넷)와 호텔 내부 관리(자원 배분, 보안)로 나뉘어요.
2. 시스템 콜은 고객이 프런트 데스크([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))에 요청하는 방법 — 직접 금고에 손대지 못하고 반드시 창구를 통해야 해요.
3. strace를 쓰면 앱이 어떤 OS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 몇 번 요청했는지 전부 볼 수 있어서 느린 원인을 찾거나 에러를 디버깅할 때 유용해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 39 / 800

← **이전**: [038. init과 systemd — 부팅 초기화 시스템](/knowledge-base/studynote/02_operating_system/01_overview_architecture/038_init_systemd/)
**다음**: [040. 오류 탐지 (Error Detection)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/040_error_detection/) →

---
