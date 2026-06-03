+++
title = "332. CWPP 런타임 워크로드 보호 (CWPP Cloud Workload Protection Platform Falco eBPF seccomp Container Escape)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CWPP (Cloud Workload [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Platform, [클라우드 워크로드 보호 플랫폼](/knowledge-base/studynote/15_devops_sre/05_devsecops/255_cwpp_cloud_workload_protection_platform/))은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 함수 등 런타임 워크로드에서 이상 행동을 실시간 탐지하고 차단하는 보안 솔루션이다. 이미지 취약점은 CWPP 이전에 [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/)/SAST로 처리하고, 런타임에서 발생하는 예상치 못한 행동은 CWPP가 담당한다.
> 2. <strong>Falco와 <a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a></strong>: Falco는 리눅스 시스템 콜([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))을 실시간 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링해 이상 행동(비정상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근, 네트워크 연결, [권한 상승](/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/))을 탐지한다. [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) ([Extended Berkeley Packet Filter](/knowledge-base/studynote/15_devops_sre/03_sre_observability/147_ebpf_kernel_observability_cilium/))를 사용하면 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 없이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 가시성을 확보하고, seccomp으로 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 허용된 시스템 콜만 사용하도록 제한한다.
> 3. **판단 포인트**: [Container Escape](/knowledge-base/studynote/15_devops_sre/05_devsecops/252_container_escape_vm_gvisor_kata/)([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 탈출)는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에서 호스트 OS로 접근하는 심각한 보안 사고다. CWPP는 이런 탈출 시도를 시스템 콜 패턴으로 탐지한다. 2018년 Tesla [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경의 크립토마이닝 사례가 CWPP 필요성을 보여준다.

---

## Ⅰ. 개요 및 필요성

[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지가 안전하게 빌드되더라도, 런타임에서 공격자가 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 침해할 수 있다. 환경변수로 주입된 [시크릿](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)이 노출되거나, 취약한 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)의 메모리 익스플로잇으로 임의 코드가 실행될 수 있다.

2018년 Tesla 사례: [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 대시보드가 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 없이 노출 -> 공격자가 크립토마이닝 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 배포 -> AWS에서 수만 달러의 컴퓨팅 비용 발생. CWPP가 있었다면 비정상적인 CPU 사용과 외부 통신이 즉시 탐지되었을 것이다.

> 📢 **섹션 요약 비유**: CWPP는 건물 내 개인 보안 요원이다. 누군가가 허가 없이 금고실(민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 접근하거나 비상구로 탈출을 시도하면 즉시 제지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CWPP 탐지 구조 (Falco)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컨테이너 내 프로세스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(App, Shell, Network 등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시스템 콜 (syscall)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">v</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">eBPF / Kernel Module 훅</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- execve, open, connect, ptrace 등 감시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">v</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Falco 룰 엔진</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 규칙 매칭 -&gt; 경보/차단/대응</div></div>
</div>
</div>



Falco 룰 예시 (YAML):
```yaml
- rule: Terminal shell in container
  desc: 컨테이너 내 터미널 쉘 실행 탐지
  condition: container and proc.name = bash
  output: "컨테이너에서 bash 실행 탐지"
  priority: WARNING
```

> 📢 **섹션 요약 비유**: Falco는 건물 내 모든 문과 창문에 센서를 붙인 것이다. 누군가 비정상적인 경로(터미널 접근, 루트 권한 획득)를 사용하면 즉시 경보가 울린다.

---

## Ⅲ. 비교 및 연결

| 기술 | 역할 | 방식 |
|:---|:---|:---|
| [seccomp](/knowledge-base/studynote/02_operating_system/01_overview_architecture/080_seccomp/) | 시스템 콜 제한 | 허용 목록 기반 필터링 |
| [AppArmor](/knowledge-base/studynote/02_operating_system/10_security/584_apparmor/) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/네트워크 접근 제어 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (강제 접근 제어) |
| Falco | 런타임 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) | 시스템 콜 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 |
| [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 가시성 확보 | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 훅 |

[Container Escape](/knowledge-base/studynote/15_devops_sre/05_devsecops/252_container_escape_vm_gvisor_kata/) 탐지 예시:
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에서 /proc/1/ns 접근 -> 호스트 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 탈출 시도
- [docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/).sock [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 후 [docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) run 실행 -> [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 호스트 제어

> 📢 **섹션 요약 비유**: seccomp은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에게 이 동작들만 할 수 있다는 면허증이다. 면허에 없는 동작은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 즉시 거부한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### CWPP 구현 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Falco가 [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) DaemonSet으로 모든 노드에 배포되어 있는가?
2. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지가 루트(root)로 실행되지 않는가 (non-root 사용자)?
3. [seccomp](/knowledge-base/studynote/02_operating_system/01_overview_architecture/080_seccomp/) 프로파일로 불필요한 시스템 콜이 제한되어 있는가?
4. [Container Escape](/knowledge-base/studynote/15_devops_sre/05_devsecops/252_container_escape_vm_gvisor_kata/) 탐지 룰이 활성화되고 SIEM에 연동되어 있는가?

### 위협 유형별 탐지

- **크립토마이닝**: 비정상적 외부 IP 연결, CPU 과부하
- **역방향 쉘**: 비정상적 네트워크 바인딩, 쉘 [프로세스 생성](/knowledge-base/studynote/02_operating_system/02_process_thread/104_process_creation/)
- <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/356_privilege_escalation/">권한 상승</a></strong>: [setuid](/knowledge-base/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 실행, ptrace 호출
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 유출</strong>: 비정상적 대용량 외부 전송

> 📢 **섹션 요약 비유**: CWPP는 은행 내부의 이상 행동 탐지 시스템이다. 직원이 갑자기 금고에 접근하거나 대량의 현금을 이동시키면 즉시 보안팀에 알린다.

---

## Ⅴ. 기대효과 및 결론

CWPP 도입으로 런타임 공격을 수분~수초 내에 탐지하고 대응할 수 있다. Tesla 사례처럼 발견이 늦어져 수만 달러 피해를 입는 상황을 방지한다.

CWPP의 핵심은 <strong>"알려지지 않은 위협(Unknown Threat)도 시스템 콜 패턴으로 탐지한다"</strong>는 것이다. 새로운 취약점이나 공격 기법이 나와도, 이상한 시스템 콜은 항상 발생하기 때문에 탐지된다.

> 📢 **섹션 요약 비유**: CWPP는 지문 인식이 아니라 걸음걸이로 신원을 파악하는 시스템이다. 공격자가 신분증을 위조해도(코드 우회), 비정상적인 행동 패턴(시스템 콜)으로 탐지된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| CWPP (Cloud Workload [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) Platform) | 런타임 워크로드 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| Falco | 시스템 콜 기반 런타임 탐지 |
| [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) ([Extended Berkeley Packet Filter](/knowledge-base/studynote/15_devops_sre/03_sre_observability/147_ebpf_kernel_observability_cilium/)) | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 가시성 |
| [seccomp](/knowledge-base/studynote/02_operating_system/01_overview_architecture/080_seccomp/) | 시스템 콜 허용 목록 필터링 |
| [Container Escape](/knowledge-base/studynote/15_devops_sre/05_devsecops/252_container_escape_vm_gvisor_kata/) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에서 호스트 OS 탈출 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">VM 기반 보안 컨테이너 보안 등장 eBPF 기반 현대 CWPP</div>
<div class="kb-diagram-note">호스트 기반 IDS -&gt; Docker/K8s 런타임 위협 -&gt; eBPF 커널 레벨 탐지</div>
<div class="kb-diagram-note">AV/에이전트 중심 Falco 오픈소스 등장 Cilium + Falco 통합</div>
<div class="kb-diagram-note">정적 시그니처 seccomp/AppArmor 강화 CNAPP으로 통합</div>
<div class="kb-diagram-note">Tesla 크립토마이닝 사례 AI 기반 이상 탐지</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. CWPP는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안에서 일어나는 모든 행동을 지켜보는 CCTV예요. 이상한 행동을 하면 바로 경보가 울려요.
2. seccomp은 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)에게 이것만 할 수 있어라는 면허증이에요. 면허에 없는 것은 아예 시도조차 할 수 없어요.
3. eBPF는 건물 바닥에 내장된 센서예요. 위층에서 무슨 일이 일어나도 바닥 진동으로 즉시 감지할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 332 / 373

← **이전**: [331. CSPM 클라우드 보안 형상 관리 (CSPM Cloud Security Posture Management CIS Benchmark](/knowledge-base/studynote/15_devops_sre/05_devsecops/331_cspm/)
**다음**: [333. CNAPP 클라우드 통합 보안 플랫폼 (CNAPP Cloud Native Application Protection Platform](/knowledge-base/studynote/15_devops_sre/05_devsecops/333_cnapp/) →

---
