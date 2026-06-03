+++
title = "043. 보호와 보안 (Protection & Security)"
date = 2026-04-05

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

> **핵심 인사이트**
> 1. OS에서 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)([Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/))는 "합법적인 사용자가 리소스에 올바르게 접근하도록 제어"하는 메커니즘이고, 보안([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))은 "외부 위협으로부터 시스템을 방어"하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) — 두 개념은 목적과 대상이 다르며 계층적으로 보안이 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 포함한다.
> 2. [보호 도메인](/knowledge-base/studynote/02_operating_system/10_security/572_protection_domain/)([Protection Domain](/knowledge-base/studynote/02_operating_system/10_security/572_protection_domain/))과 접근 행렬([Access Matrix](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/))은 OS [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)의 이론적 기반으로, 주체(Subject)-객체(Object)-권한(Right)의 삼각 관계를 체계적으로 모델링하며 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)([Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))과 Capability List로 구현된다.
> 3. 링 구조(Ring [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))는 x86 CPU의 권한 레벨(Ring 0~3)을 통해 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Ring 0)과 사용자 프로그램(Ring 3)을 분리하는 하드웨어 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘으로, 특권 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 실행, 메모리 접근, I/O 제어를 계층적으로 제어한다.

---

## Ⅰ. [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) vs 보안 개념 구분



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">보호 (Protection):</div>
<div class="kb-diagram-note">목적: 프로세스/사용자 간 리소스 격리 및 접근 제어</div>
<div class="kb-diagram-note">대상: 내부 위협 (프로그램 오류, 권한 오남용)</div>
<div class="kb-diagram-note">메커니즘: 하드웨어 + OS 커널 기능</div>
<div class="kb-diagram-note">예: 프로세스 A가 프로세스 B의 메모리 접근 방지</div>
<div class="kb-diagram-note">보안 (Security):</div>
<div class="kb-diagram-note">목적: 시스템 전체를 외부 위협으로부터 방어</div>
<div class="kb-diagram-note">대상: 외부 위협 (해커, 악성코드, DoS)</div>
<div class="kb-diagram-note">메커니즘: 인증, 암호화, 방화벽, 감사</div>
<div class="kb-diagram-note">예: 네트워크 침입 탐지, 악성코드 차단</div>
<div class="kb-diagram-note">계층 관계:</div>
<div class="kb-diagram-note">보안 (Security) ⊃ 보호 (Protection)</div>
<div class="kb-diagram-note">외부 위협 방어 (보안)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">내부 접근 제어 (보호)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">하드웨어 격리 (링 구조, MMU)</div>
<div class="kb-diagram-note">OS 보안 요구사항 (CIA):</div>
<div class="kb-diagram-note">C - Confidentiality (기밀성): 인가된 자만 읽기</div>
<div class="kb-diagram-note">I - Integrity (무결성): 인가된 방식으로만 수정</div>
<div class="kb-diagram-note">A - Availability (가용성): 서비스 지속 제공</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) vs 보안은 건물 내부 잠금 vs 외벽 보안 — [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)는 내부 회의실 문 잠금(내부 격리), 보안은 외부 침입자 방어(외벽, [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)).

---

## Ⅱ. [보호 도메인](/knowledge-base/studynote/02_operating_system/10_security/572_protection_domain/)과 접근 행렬



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">보호 도메인 (Protection Domain):</div>
<div class="kb-diagram-note">주체(Subject)가 가진 권한 집합</div>
<div class="kb-diagram-note">도메인 D = { (객체, 권한) 쌍의 집합 }</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">Domain 1 (root): { (file1, rw), (file2, rwx), (mem, rw) }</div>
<div class="kb-diagram-note">Domain 2 (user): { (file1, r), (file3, rw) }</div>
<div class="kb-diagram-note">접근 행렬 (Access Matrix):</div>
<div class="kb-diagram-note">행: 도메인 (주체)</div>
<div class="kb-diagram-note">열: 객체 (파일, 포트, 메모리 세그먼트)</div>
<div class="kb-diagram-note">셀: 허용 권한 집합</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파일A</div><div class="kb-diagram-cell">파일B</div><div class="kb-diagram-cell">프린터</div><div class="kb-diagram-cell">세그먼트1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도메인1</div><div class="kb-diagram-cell">rw</div><div class="kb-diagram-cell">rwx</div><div class="kb-diagram-cell">print</div><div class="kb-diagram-cell">rw</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도메인2</div><div class="kb-diagram-cell">r</div><div class="kb-diagram-cell">r</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도메인3</div><div class="kb-diagram-cell">rx</div><div class="kb-diagram-cell">print</div></div>
<div class="kb-diagram-note">구현 방법:</div>
<div class="kb-diagram-note">1. ACL (Access Control List) — 열 기준:</div>
<div class="kb-diagram-note">파일A: { (도메인1, rw), (도메인2, r) }</div>
<div class="kb-diagram-note">장점: 객체별 접근자 목록 관리 쉬움</div>
<div class="kb-diagram-note">단점: 특정 주체의 모든 권한 확인 어려움</div>
<div class="kb-diagram-note">2. Capability List — 행 기준:</div>
<div class="kb-diagram-note">도메인1: { (파일A, rw), (파일B, rwx), (프린터, print) }</div>
<div class="kb-diagram-note">장점: 주체 관점에서 권한 관리</div>
<div class="kb-diagram-note">단점: 권한 취소(revoke) 어려움</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 접근 행렬은 학교 열쇠 관리 장부 — ACL은 "이 강의실에 들어갈 수 있는 사람" 목록, Capability는 "이 사람이 열 수 있는 강의실" 목록.

---

## Ⅲ. 링 구조 (Ring [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">x86 CPU 링 구조 (Privilege Levels):</div>
<div class="kb-diagram-note">Ring 0 — 커널 모드 (Kernel Mode):</div>
<div class="kb-diagram-note">최고 권한</div>
<div class="kb-diagram-note">모든 명령어 실행 가능</div>
<div class="kb-diagram-note">하드웨어 직접 접근</div>
<div class="kb-diagram-note">OS 커널, 디바이스 드라이버 핵심 부분</div>
<div class="kb-diagram-note">Ring 1, 2 — (현재 대부분 미사용):</div>
<div class="kb-diagram-note">원래 OS 서비스, 드라이버용</div>
<div class="kb-diagram-note">현대 OS: Ring 0/3 양분 구조</div>
<div class="kb-diagram-note">Ring 3 — 사용자 모드 (User Mode):</div>
<div class="kb-diagram-note">최소 권한</div>
<div class="kb-diagram-note">특권 명령어 실행 불가</div>
<div class="kb-diagram-note">I/O 직접 접근 불가</div>
<div class="kb-diagram-note">일반 응용 프로그램</div>
<div class="kb-diagram-note">권한 이동:</div>
<div class="kb-diagram-note">Ring 3 → Ring 0:</div>
<div class="kb-diagram-note">시스템 콜 (INT, SYSCALL 명령어)</div>
<div class="kb-diagram-note">예외 처리 (Exception Handler)</div>
<div class="kb-diagram-note">인터럽트 (Interrupt)</div>
<div class="kb-diagram-note">Ring 0 → Ring 3:</div>
<div class="kb-diagram-note">IRET, SYSRET 명령어</div>
<div class="kb-diagram-note">스케줄러에 의한 사용자 프로세스 복귀</div>
<div class="kb-diagram-note">보호 메커니즘:</div>
<div class="kb-diagram-note">특권 명령어: Ring 0에서만 실행</div>
<div class="kb-diagram-note">(LGDT, LIDT, IN/OUT, HLT, MOV CR0 등)</div>
<div class="kb-diagram-note">메모리: 페이지 테이블로 Ring 3 접근 격리</div>
<div class="kb-diagram-note">I/O: IOPL(I/O Protection Level) 비트로 제어</div>
<div class="kb-diagram-note">가상화와 Ring:</div>
<div class="kb-diagram-note">VMware/VirtualBox: Ring -1 (Hypervisor)</div>
<div class="kb-diagram-note">Intel VT-x: VMX root/non-root 모드</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사(기본 임무만). 계급 외 명령 실행 → 즉시 처벌(예외 발생).

---

## Ⅳ. 보안 위협 유형과 대응



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OS 보안 위협 분류:</div>
<div class="kb-diagram-note">악성코드 (Malware):</div>
<div class="kb-diagram-note">바이러스: 다른 프로그램에 기생, 자기 복제</div>
<div class="kb-diagram-note">웜: 독립 실행, 네트워크 전파</div>
<div class="kb-diagram-note">트로이 목마: 정상 프로그램으로 위장</div>
<div class="kb-diagram-note">랜섬웨어: 파일 암호화 후 몸값 요구</div>
<div class="kb-diagram-note">권한 상승 공격:</div>
<div class="kb-diagram-note">버퍼 오버플로우: 스택 리턴 주소 덮어쓰기</div>
<div class="kb-diagram-note">→ 셸코드 실행 → Root 권한 탈취</div>
<div class="kb-diagram-note">대응: ASLR(주소 공간 레이아웃 랜덤화), DEP(데이터 실행 방지), Stack Canary</div>
<div class="kb-diagram-note">레이스 컨디션 (Race Condition):</div>
<div class="kb-diagram-note">TOCTOU(Time-Of-Check-To-Time-Of-Use)</div>
<div class="kb-diagram-note">권한 확인과 실제 사용 사이의 시간차 악용</div>
<div class="kb-diagram-note">대응: 원자적 연산, 잠금(Lock) 사용</div>
<div class="kb-diagram-note">사이드 채널 공격:</div>
<div class="kb-diagram-note">Spectre, Meltdown (2018):</div>
<div class="kb-diagram-note">CPU 투기적 실행 → 캐시 타이밍 측정 → 비밀 데이터 추출</div>
<div class="kb-diagram-note">대응: OS 패치, KPTI(Kernel Page Table Isolation)</div>
<div class="kb-diagram-note">보안 메커니즘:</div>
<div class="kb-diagram-note">인증 (Authentication): 비밀번호, 생체인식, 2FA</div>
<div class="kb-diagram-note">인가 (Authorization): DAC/MAC/RBAC</div>
<div class="kb-diagram-note">감사 (Auditing): 접근 로그, SIEM</div>
<div class="kb-diagram-note">암호화: 파일 시스템 암호화 (BitLocker, LUKS)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: OS 보안 위협은 건물 침입 방법 — 정문 뚫기([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 우회), 창문 깨기([버퍼 오버플로우](/knowledge-base/studynote/02_operating_system/10_security/591_buffer_overflow/)), 청소부 위장([트로이 목마](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/)), 열쇠 복사(자격증명 도용).

---

## Ⅴ. 실무 시나리오 — Linux [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/)/[AppArmor](/knowledge-base/studynote/02_operating_system/10_security/584_apparmor/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Linux 강제 접근 제어 (MAC) 구현:</div>
<div class="kb-diagram-note">DAC (Discretionary Access Control) 한계:</div>
<div class="kb-diagram-note">파일 소유자가 권한 부여 결정</div>
<div class="kb-diagram-note">root 계정 탈취 시 모든 파일 접근 가능</div>
<div class="kb-diagram-note">→ Linux 전통 rwx 권한의 한계</div>
<div class="kb-diagram-note">MAC (Mandatory Access Control):</div>
<div class="kb-diagram-note">시스템 정책이 모든 접근 제어</div>
<div class="kb-diagram-note">소유자도 정책 외 권한 부여 불가</div>
<div class="kb-diagram-note">SELinux (Security-Enhanced Linux):</div>
<div class="kb-diagram-note">NSA 개발, Red Hat/CentOS/Fedora 기본 탑재</div>
<div class="kb-diagram-note">레이블 기반: 모든 파일/프로세스에 보안 컨텍스트</div>
<div class="kb-diagram-note">컨텍스트 형식: user:role:type:level</div>
<div class="kb-diagram-note">예: system_u:system_r:httpd_t:s0</div>
<div class="kb-diagram-note">정책 유형:</div>
<div class="kb-diagram-note">Enforcing: 정책 위반 = 차단 + 로그</div>
<div class="kb-diagram-note">Permissive: 차단 없음 + 로그만 (개발/디버깅)</div>
<div class="kb-diagram-note">Disabled: 비활성화</div>
<div class="kb-diagram-note">AppArmor (Ubuntu/SUSE):</div>
<div class="kb-diagram-note">경로 기반 프로파일</div>
<div class="kb-diagram-note">더 간단, 관리 편이</div>
<div class="kb-diagram-note">/etc/apparmor.d/usr.sbin.nginx 예시:</div>
<div class="kb-diagram-note">/var/www/html/** r,</div>
<div class="kb-diagram-note">/var/log/nginx/** w,</div>
<div class="kb-diagram-note">network tcp,</div>
<div class="kb-diagram-note">실무 적용:</div>
<div class="kb-diagram-note">웹서버(Apache/Nginx)에 SELinux 프로파일 적용</div>
<div class="kb-diagram-note">→ 웹 디렉토리 외 파일 접근 자동 차단</div>
<div class="kb-diagram-note">→ 명령 실행(system()) 차단</div>
<div class="kb-diagram-note">→ 취약점 악용 시 피해 최소화 (컨테인먼트)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: SELinux는 회사 보안 시스템 — 팀장(root)도 다른 팀 서버실에 못 들어가는 것처럼, 역할(Role)과 유형(Type)으로 최소 권한 강제.

---

## 📌 관련 개념 맵

```
OS 보호 & 보안
+-- 보호 (Protection)
|   +-- 보호 도메인
|   +-- 접근 행렬 (ACL, Capability)
|   +-- 링 구조 (Ring 0~3)
+-- 보안 (Security)
|   +-- CIA (기밀성, 무결성, 가용성)
|   +-- 위협: 버퍼 오버플로우, TOCTOU, 사이드채널
|   +-- 메커니즘: ASLR, DEP, KPTI
+-- MAC 구현
|   +-- SELinux (Red Hat 계열)
|   +-- AppArmor (Ubuntu 계열)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 OS 보호 (1960s~)]
IBM System/360: 특권 모드 도입
멀틱스: 링 구조 최초 구현
      |
      v
[Unix 권한 모델 (1970s)]
DAC: rwx + 소유자/그룹/기타
      |
      v
[보안 확장 (1980s~90s)]
Orange Book (TCSEC): 보안 등급화
NSA: B3급 OS 연구 → SELinux 기반
      |
      v
[Linux 보안 (2000s)]
SELinux (2000, 2003 커널 통합)
AppArmor (2006, Ubuntu 통합)
      |
      v
[현재: 컨테이너 보안]
seccomp: 시스템 콜 필터링
cgroups + namespace: 컨테이너 격리
eBPF: 커널 내 보안 프로그램 실행
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)는 내부 자물쇠, 보안은 외벽 경비원 — 집 안에서 방마다 잠금([보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)), 집 전체를 지키는 경비원(보안)처럼 서로 역할이 달라요!
2. 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사. 사령관 명령을 병사가 내리면 즉시 경고!
3. SELinux는 초엄격 출입증 시스템 — root 계정을 가져도 출입증([SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/))이 없으면 들어갈 수 없어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 43 / 800

← **이전**: [042. 회계 및 로깅 (Accounting and Logging)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/042_accounting_logging/)
**다음**: [044. 셸 — Shell](/knowledge-base/studynote/02_operating_system/01_overview_architecture/044_shell/) →

---
