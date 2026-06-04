---
title: "617. I/O 성능 병목 (Bottleneck) 탐색법 (iostat, vmstat)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: I/O [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 (Bottleneck) 탐색법 (iostat, vmstat)은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘에서 핵심 흐름을 결정하는 개념으로, 시스템이 무엇을 먼저 관리하고 어떤 순서로 제어할지를 분명하게 만든다.
> 2. **가치**: 이 개념을 이해하면 자원 효율, [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/), 안정성 사이의 균형을 더 정확하게 설명할 수 있고, 캐시 미스 오버헤드 측정 분석망 구조 적용로 이어지는 이유도 자연스럽게 파악된다.
> 3. **판단 포인트**: 멀티코어 확장성 병목 (Amdahl's Law) 및 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [락 경합](/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/) 진단과의 관계를 함께 봐야 I/O [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 (Bottleneck) 탐색법 (iostat, vmstat)을 단순 정의가 아니라 실제 설계·운영 판단 기준으로 사용할 수 있다.

---

## Ⅰ. 개요 및 필요성

### êë ë ìì
I/O ìë ëëì ììíì ëìíëíëCPUìëëëìììë. ììíì ìì ìë ìêìì I/O ëêê ììíë ëìì ëììë I/O ëëì ìêíëë ëìë.

I/O ëëì ìì ììì ëìê êë:
- **ëìí ììì ìë ìë íê**: HDDì ëëì ìí ìê(íì ìê + íì ìì)
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a> ìíëë ìì</strong>: RAID5/6ì íëí êìì ëë ìê ëë
- **íìììí ëíëìíìì**:ìíëí
- **ëë ëìì í êì íê**: ëìì ìë êëí I/O ìì ì ìí
- **ëíìí ëìí íí**: ëìë ëìí ìì ì ëíìí ëìí êê

### ì I/O ëë ëìì ììíê
CPUìëê ìëë ëìë, ëìíëìëììíêì ëìíëìì ìë, íì ìë, êì ëì, ë ëëëìI/Oì ëêíëë, I/O ëëì íêíë ììíì íìë ìëììëì êëí ì ìë.

```
[ììí ìì ìë ìê ëì]

[CPU ëìë íëêëì êì]
ìì ìê = 100%
|| CPU ìë (100%)
|                              |

[CPU + I/O íí íëêëì êì]
ìì ìê = 100%
|| CPU ìë (30%)
|| I/O ëê (70%)
|             ìêì I/O ëë!

[I/O ëë íê í]
ìì ìê = 43%
|| CPU ìë (30%)  <- ììê ëì
|| I/O ëê (13%)   <- 70%ìì 13%ë êì!
|             I/O ììíë ìì ìêì 57% ëìë!
```

**[ëììêë íì]** I/O ëë íêì"ëëìíêì"ì ëìí ì ìë.ëìí ììëCPU(ìê)ì ìëë ëëëI/O(ëë)ê ëëìëìììë

- **ìì ëì**: I/O ëëì "êì ëë ëì"ì êë. ìììì ììì ëëêê ìëë ëëë( CPU ), ëë ìëì ìêë(ëìí ìëë) ëë êì ëíë(ëíìí ëìí) íìëì ìëì ììë ëì ëíë.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### I/O ìí êìì ê êìë ëë íìí

```
[]
  > [File System Layer]  <- ëíëìí ìì, ìê, ëí ìì
        > [Block Layer]    <- I/O ìììë, í êë
              > [SCSI/NVMe Layer]  <- ëìí ìíëë, í êì
                    > [Physical Disk]  <- ìì ëìí read/write

ê êìë ëë íìí:

[File System êì]
- ëíëìí ìê/ìê ìì ìì (íííì)
- íìììí ëí ìì ëì ->ëìì
- ìê êí (fs-wide inode mutex ë)

[Block Layer]
- I/O ìììë ìí (noop, cfq, deadline, mq-deadline)
- í êì (queue depth) ìí
- ëë (unbalanced I/O ëì)

[ëìí ìíëë]
- RAID íëí êì (RAID5/6 ìê)
- ìíëë ìì Hit/Miss
- SSDì êì FTL(Flash Translation Layer) ìëíë

[ëë ëìí]
- HDD: íì ìê (seek time) + íì ìì (rotational latency)
- SSD: NAND íëì I/O ìê ( erase + program)
```

### I/O ëë ìë ëê êì

| ëê | ëì êì | íì ìí |
|---|---|---|
| **iostat** | ëë ëìì + ëìí | tps, KB_read/s, KB_wrtn/s, await, %util |
| **iotop** | íëììë | ëìí I/O ììëë íëìì ìë |
| **pidstat** | íëììë | PIDë I/O íê |
| **blktrace** | ëë ëìì | êë I/O ììì [latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) ëí |
| **bpftrace** | ëë êì | ìë íì ììì ìì ìì |
| **perf** | CPU + I/O | [CPI](/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/), I/O êë íëìì ìëí |

### iostat ìì ìí íë

```
Device  tps    kB_read/s  kB_wrtn/s  kB_read  kB_wrtn  await  %util
sda    154.32    1234.56     567.89   123456   56789   12.34  45.67

[ìí ìë]
tps (Transactions Per Second): ìë ìëëë I/O ìì ì
kB_read/s: ìë ìì íëëìí
kB_wrtn/s: ìë ì íëëìí
await: I/O ìììì ëìíì ëëê ìëêììíê ëê ìê (ëëì)
%util: ëìí ììë (100%ë ëìí íí!)
```

**ëë íë êì**:
- **%util > 80%**: ëìí íí -> ìê I/O ììì ëêíì í
- **await > 100ms**: ëì ëë ëìí ìë -> HDDì êì typical, SSDëë ëì ìì
- **avgqu-sz (ëê í íê) > 4**: ëì I/Oê íìì ëê ì -> ëë íì

```
[ëë íë íë]

%utilì 80% ìììê?
 ì: ëìíê ëëìë
     ìê ëìì ëëë -> ìê ììí (ìì, ëë ahead)
     ìê ëìì ëëë -> ìê ììí (ëì ìê, SSD ëì)

 ìëì: CPUë ëíìí ìì íì
     CPU %iowaitê ëìê?
         ì: I/O ëêë CPUê ëê ìí -> I/O ëëìë
     CPU ììê ëìê?
          ì: CPU ëëìë
```

**[ëììêë íì]** iostatì %utilì"êìëë ííë"ê êë. 80% ìíìë ìëì ìííê íëìë, 80% ììì ëë ìë ìì êêì ìììê ìëê ëëìë. 100%ì ìëë êìëëê ìì ííëì ìë ìë ìììì ëíë.

### [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) vs [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) ëë íì ëê

| ìí | [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/)) | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)) |
|---|---|---|---|
| **ìì ìê ìë** | 100~200 MB/s | 500~550 MB/s | 3,000~7,000 MB/s |
| **ìì ìê ìë** | 100~200 MB/s | 400~500 MB/s | 2,000~6,000 MB/s |
| **ìê ìììê** | 5~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ms | 0.05~0.1 ms | 0.01~0.05 ms |
| **ìê ìììê** | 5~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) ms | 0.05~0.1 ms | 0.01~0.05 ms |
| **ëë** | íì ìê + íì | [SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/) ëìí + ìíëë | í êì ([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) Depth) |
| **ëë íêì** | SSDë êì | NVMeë êì | í êì ììí |

- **ìì ëì**: I/O ëë ìëì "ëë ììì"ì êë. êêì"ììì ì ììì"ëê íë, restoranìì ëìëì(ììí ì), ëëììììì(I/O ìë), ëëìì ëíëì(ëíìí/ëìí ëë) ê êêì ììíì"ìëì ëìê ëìíëì"ë íìíì íë.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### I/O ëë vs CPU ëë: ìíí ìëì ììì

| ìì | ìì ìì | ìì ìì | êê |
|---|---|---|---|
| CPU %iowait ëì | I/O ëë | ììëë CPUê I/O ëêê ìë ëë ëê ìí | ìëë ììí |
| ìëë ëì | ëìí ëë | ëíìí ëìí íí | ëìí êì |
| ìë ìì | CPU ëì | I/O ëê í íì | CPU ì |

```
[ìíí ëë ìë êì]

ëê 1: ììí ìì íì
 uptime (ëí íê)
 vmstat 1 (CPU, I/O, ëëë ìí)
 iostat -x 1 (ëìí ììë, ìë ìê)

ëê 2: CPU vs I/O ëë êë
 vmstatìì CPUë ììë ëì
     us (user) + sy (system) ëì -> CPU ëì
     wa (wait I/O) ëì -> I/O ëê

 iostatìì ëìí ììë ëì
      %util 80% ìì -> ëìí íí
      %util 80% ëë -> ëë êì ëì

ëê 3: ìì ìì íì
 iotop: ìë íëììê I/Oë êì ëì ëììíëì
 blktrace: I/O ììë latency ëí
 bpftrace: ìë ëë I/O ìë íì ìì
```

**[ëììêë íì]** I/O ëë ìëì"ìë ìí ìë"ê êë. íìêì(CPU íê), X-ray(ëìí íê), ììë(ëíìí íê) ë ìë êìë íì ìíììë íëíì"ìì ìì"ì ì ì ìë. í êì êìëìë íëíë ìëë ìëë íê ë ì ìë.

### íìììíë I/O íì

| íìììí | êì | ìì | ìíí ìì |
|---|---|---|---|
| **Ext4** | ëì ííì, ìëë | ìë | ëì ìë, êêì |
| **XFS** | í íì, ëë ìë | ëíëìí ìì ìëíë | ëìíëìì, [HPC](/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/) |
| **ZFS** | ëìí ëêì, ìëì | ëëë ìë í | ëì, íì ìë |
| **Btrfs** | ìì, ìëìê | ìì maturity ëì | êë íê |

- **ìì ëì**: íìììí ìíì"ëìì ëë êê ìí"ê êë. ëêìëìXFSìSDAìêê ëë ëêë ìë êìë,ì ëê íìììíì ìííì íë.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### ìë ìëëì: ëìíëìì ìë ìë ìí íê

**ìí**:ë ìëì ìíëì ìí êì ìëê ìì ëëìê ììë.ìí ëìíê ëìììë ìëìììëìííìë.

**ìë êì**:
1. `iostat -x 1` ìí -> ëìí %utilê 95%ë íí
2. `iotop` -> mysql/mariadb íëììêì ëëëì
3. `blktrace`ë ìì ëì -> ìì íêê ëëë 4KB~16KB ( ëìí ìê)
4. `perf stat -a -e block:block_rq_issue`ë ëì -> ëì ìì 4KB ìê ìì ëì

**ìì**:ìí ìëê ìë êì ììì ëì ììëìê êìëë ëììíì.

**ëìì**:
1. ëëíìëëëí ëëëì (Buffer Pool íë)
2. ìí ìëìë í íìë íìì sequential readë ëê
3. InnoDB ìììì `innodb_flush_method = O_DIRECT` ììíì OS ìì ìí

**êê**: ëìí %utilê 95%ìì 30%ë êì, ìë ìëê íê 80% íì

### ëì ìíëìí

- **ëìí íí ìë íì**: iostatìì %utilê 80%ë ëìë ëìíê ëëìë.
- **ìê vs ìê ëì ëì**: ìê ëìì ëìë ìì ìì, ìê ëìì ëìë ìê ììí
- **íëììë I/O ëì**: iotopìë ìë íëììê êì ëì I/Oë ëìíëì íì
- **ìì íì ëëìì**: ëì ìì ìì íììíë ìëíëê íëë, íëë íìêë ìíëì íì

### ìííí

- **"%utilì ëìë I/O ëëì ìëë" íë**: %utilì ëìë await(ìë ìê)ê ëìë ëìí ììì ìë ìë ëìê ìì ì ìë.
- <strong><a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> ëìëìë ëë ëë íê</strong>: SSDë ëëìë,ìì ëìíë I/O ìììììì ììë ììí ëëì ë ì ìë.
- **ììëìë íêíë í**: ìì ííìì ëìë(= ìì íëëì ëëë íêëì ììë) ìíëììììë ëìí ëì ìë ììë ëììêíì íë.

- **ìì ëì**: I/O ëë íêì "ëì êí íì íê"ê êë. Royceíë([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) êì)ëìëìê ëë(ìì ì ìê) ë ëíë. ììì(ìì), ìë ííì ììê(ìì ììí), ëëìëë íìììë ëëë êììë.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

### ìë/ìì êëíê

| êë | I/O ëë ëíê | I/O ëë íê í |
|---|---|---|
| **íê ìë ìê** | 500ms | 50ms |
| **ìëë (QPS)** | 100 req/s | 1,000 req/s |
| **CPU íì** | I/O ëêë ëë | CPUê ìì ììì íì |
| **íëìì íìë** | ëìí íí, CPU ìì | êí ìí íì |

### ëë ìë
[NVMe-oF](/studynote/02_operating_system/08_storage_and_io_systems/499_nvme_over_fabrics/)(ëíìíë íí [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/)), ìííììë ìíëì(ìíëììì ìì ìì), êëê [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) êë I/O íí ìì ëì ëë I/O ëë íêì ìëì ëíì ë êìë.

### ìê íì
- <strong>Linux iostat <a href="/studynote/04_software_engineering/06_software_architecture/378_software_documentation/">documentation</a></strong>: [https](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)://man7.org/linux/man-pages/man1/iostat.1.html
- <strong>blktrace <a href="/studynote/04_software_engineering/06_software_architecture/378_software_documentation/">documentation</a></strong>: [https](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)://wiki.btrfs.org/wiki/ blktrace
- <strong>NIST <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> 800-88</strong>: ìíëì ìíí êìëëì

- **ìì ëì**: I/O ëë íêì "ëë ìê íìí"ì êë. íëìëëê(íëìì ì)ìê ëë íëë ëíê(ìííìì ììí)ëë êë ììíìíë(ìì, ìì) ìì ëë ìëê ëìììë íìëë.

---

> 1. **ëì**: I/O ìë ëëìë ììíì ìì ìëë([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))ì ëìí, ëíìí, íìììí ë I/O subsystemì ìë ëëì ìíëë íììë, CPUë ëëëëë I/O ëêê ìì ìì ìêì ëëëì ììíë êìê ëì ííë.
> 2. **êì**: I/O ëëì ìíí íìíë, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ëì, [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) êì ëê, ëëê I/O ìì, ìì ìë ìë ë ìë íìê êì íêììì íëí ì ìë.
> 3. **ìí**: I/O ëë ëìì íìììí(Ext4, XFS, ZFS), ëë ëìì, SCSI/[NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) ëëìë, ëíìí ìí ë ìë êìì êì ììëë, ê êìë ëê(iostat, perf, bpftrace ë)ëììí íí ëìì íìíë.

---

| êë ëì | êê ë ìëì ìë |
|---|---|
| **ëìí ìììë** | I/O ììì ëìíì ëëê ì ìì ìëíë ìêëììë, ìêëì ìíì ëë ëë íì ëë ìíêëíë. |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/">RAID</a></strong> | ìë ëìíë íëì ëëì ëëìë êìíë êìë, ìê ìëì íëí êì ìëíëê ëìí ì ìë. |
| <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a></strong> | [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ëìì ìì ìêëë êì [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ìííììë, [SATA](/studynote/01_computer_architecture/08_io_storage_systems/341_sata/) SSDëëì ìì ìêì ìêíë. |
| <strong><a href="/studynote/02_operating_system/09_file_system/554_fuse_filesystem_in_userspace/">FUSE</a></strong> | ììì êêìì íìììíìêíí ì ìëìë, ìë ìì ìì ììí ìíëìëí ì ìë. |

---

1. I/O ëëì "íê êì ëë ëì"ì êë.ìê ììì ëë ëëìë( CPU ), ëë ìê 1ëëìë(ëìí ìëë) ìì êìì ê ìì ìëìëë.
2. êëë ëë ìê 10ëë ëìëë( [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) êì), ê ìê ëë ììê 100êëë(ìì íìë) ììí ëë ìêì ìë êëë.
3. êëì êì ëëì "ìëë ììì í êëì ëì í ëì ëëíê(íì íìê), ê íêëë ëëë ëë(ìì)"ì êìíë, ì ëìë ëëë êëë íì íìììë êìë ì ìë!

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 네트워크/보안/모니터링 이벤트 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안전 훅 매커니즘 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 멀티코어 확장성 병목 (Amdahl's Law) 및 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [락 경합](/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/) 진단 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 캐시 미스 오버헤드 측정 분석망 구조 적용 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 모바일 OS 특징 (Android vs iOS 아키텍처 비교) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[멀티코어 확장성 병목 (Amdahl's Law) 및 커널 락 경합 진단]
    |
    v
[I/O 성능 병목 (Bottleneck) 탐색법 (iostat, vmstat)]
    |
    +---> [캐시 미스 오버헤드 측정 분석망 구조 적용]
    +---> [모바일 OS 특징 (Android vs iOS 아키텍처 비교)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. I/O [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 (Bottleneck) 탐색법 (iostat, vmstat)은 컴퓨터가 누가 들어와도 되는지와 무엇을 막아야 하는지 정하는 문지기 규칙이에요.
2. 먼저 멀티코어 확장성 병목 (Amdahl's Law) 및 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [락 경합](/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/) 진단을 이해하면 I/O [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 (Bottleneck) 탐색법 (iostat, vmstat)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 I/O [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목 (Bottleneck) 탐색법 (iostat, vmstat)을 잘 알면 나중에 캐시 미스 오버헤드 측정 분석망 구조 적용도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 617 / 800

<- **이전**: [616. 멀티코어 확장성 병목 (Amdahl's Law) 및 커널 락 경합 진단](/studynote/02_operating_system/10_security/616_amdahl_law_multicore_scaling/)
**다음**: [618. 캐시 미스 오버헤드 측정 분석망 구조 적용 (Cache Miss Overhead)](/studynote/02_operating_system/10_security/618_cache_miss_overhead/) ->

---
