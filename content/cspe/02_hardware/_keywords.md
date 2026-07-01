---
title: "하드웨어 시스템 키워드 워크리스트"
date: "2026-07-01"
tags:
  - "cspe-keywords"
weight: 1
---

# 2. 하드웨어 시스템 출제동향 키워드 (목표 140개)

> 출처: 120~138회 기출 + frequency.md + 공식 8대영역 + 전망. 개인 학습 목록 미사용.

001. 컴퓨터 구조 개요 — 폰 노이만 vs 하버드 아키텍처 (Von Neumann vs Harvard Architecture)
002. CPU 구성 — ALU·CU·레지스터·버스 (CPU Components)
003. 명령어 집합 — RISC vs CISC (ISA RISC CISC) [출제:124회]
004. RISC-V 오픈 ISA (RISC-V) [출제:127회]
005. ARM 프로세서 아키텍처·동작 모드 (ARM Architecture) [출제:126회]
006. x86-64 아키텍처 (x86-64 Architecture)
007. 파이프라이닝 기본 구조 5단계 (Pipelining) [출제:122회]
008. 파이프라인 해저드 — 데이터·제어·구조 (Pipeline Hazards) [출제:122,135회]
009. 파이프라인 포워딩·분기 예측 (Pipeline Forwarding Branch Prediction) [출제:122회]
010. 슈퍼스칼라 아키텍처 (Superscalar) [출제:136회]
011. VLIW 아키텍처 (VLIW) [출제:136회]
012. 비순서 실행·레지스터 리네이밍 (Out-of-Order Execution Register Renaming) [출제:136회]
013. 명령어 수준 병렬성 ILP (Instruction-Level Parallelism) [출제:136회]
014. 멀티코어 프로세서 (Multicore Processor) [출제:132회]
015. 폴락의 법칙 (Pollack's Rule) [출제:132회]
016. 하이퍼스레딩·SMT (Simultaneous Multithreading) [전망]
017. 캐시 메모리 구조 — 직접·연관·집합 연관 매핑 (Cache Memory Mapping) [출제:120,125,131,132,134,135회]
018. 캐시 쓰기 정책 — Write-Through vs Write-Back (Cache Write Policy) [출제:129회]
019. 캐시 일관성 프로토콜 — MESI·MOESI (Cache Coherence Protocol) [출제:123,135회]
020. 버스 스누핑·디렉터리 기반 일관성 (Bus Snooping Directory Coherence) [출제:123회]
021. TLB 변환 색인 버퍼 (Translation Lookaside Buffer) [출제:135회]
022. 가상 메모리 — 페이징·세그멘테이션 (Virtual Memory Paging Segmentation) [출제:120,121,125회]
023. 페이지 교체 알고리즘 — OPT·FIFO·LRU·LFU (Page Replacement) [출제:121회]
024. 세그멘테이션 (Segmentation) [출제:126회]
025. MMU 메모리 관리 장치 (Memory Management Unit) [출제:135회]
026. NUMA 비균등 메모리 접근 (Non-Uniform Memory Access) [출제:127회]
027. 메모리 계층 구조 (Memory Hierarchy) [출제:123회]
028. DRAM vs SRAM (DRAM SRAM) [출제:125회]
029. DDR SDRAM·갱신 방식 (DDR SDRAM Refresh) [출제:129회]
030. HBM 고대역폭 메모리 (High Bandwidth Memory) [출제:129,131회]
031. HBM3E (HBM3E) [전망]
032. HBM4 (HBM4) [전망]
033. PIM 메모리 내 처리 (Processing-in-Memory) [출제:129,131회]
034. PNM 메모리 근접 처리 (Processing Near Memory) [출제:131회]
035. CXL 컴퓨트 익스프레스 링크 (Compute Express Link) [출제:129회]
036. CXL 메모리 풀링 (CXL Memory Pooling) [전망]
037. NVMe·PCIe 인터페이스 (NVMe PCIe)
038. SSD FTL 플래시 변환 계층 (Flash Translation Layer) [출제:128회]
039. NAND 플래시·3D V-NAND (NAND Flash 3D V-NAND) [출제:126회]
040. RAID 레벨 0·1·5·6·10 비교 (RAID Levels) [출제:125,131,136회]
041. 광 저장 장치 (Optical Storage)
042. I/O 인터페이스 — 폴링·인터럽트·DMA·채널 I/O (I/O Interface) [출제:128,132회]
043. 인터럽트 처리 방식 — 벡터·데이지체인 (Interrupt Handling) [출제:128,132회]
044. DMA 직접 메모리 접근 (Direct Memory Access) [출제:128회]
045. 버스 중재 방식 (Bus Arbitration) [출제:128회]
046. 3-상태 버퍼·트라이스테이트 (Tri-State Buffer) [출제:129회]
047. SOC 시스템온칩 (System on Chip) [출제:128회]
048. FPGA AI 가속 (FPGA AI Acceleration) [출제:126,134회]
049. ASIC AI 가속 (ASIC AI Acceleration) [출제:126,134회]
050. GPU 아키텍처·SIMT 모델 (GPU SIMT) [출제:124,126,134,136회]
051. CUDA 병렬 컴퓨팅 (CUDA Parallel Computing) [출제:135회]
052. TPU 텐서 처리 장치 (Tensor Processing Unit) [출제:126,134,136회]
053. NPU 신경망 처리 장치 (Neural Processing Unit) [출제:126,134,135,136,137,138회]
054. Edge TPU (Edge TPU) [출제:138회]
055. AI 가속기 비교 — CPU·GPU·NPU·FPGA·ASIC (AI Accelerator Comparison) [출제:126,134,136,137회]
056. NVLink 고속 인터커넥트 (NVLink) [출제:138회]
057. InfiniBand (InfiniBand) [출제:138회]
058. Chiplet 칩렛 (Chiplet) [출제:131회]
059. UCIe 칩렛 인터커넥트 (Universal Chiplet Interconnect Express) [전망]
060. 뉴로모픽 컴퓨팅 (Neuromorphic Computing) [출제:128회]
061. 인메모리 컴퓨팅 (In-Memory Computing) [전망]
062. 병렬 컴퓨터 분류 — Flynn 분류 (Flynn's Taxonomy) [출제:131,134회]
063. SIMD·MIMD 프로세서 (SIMD MIMD) [출제:131,134회]
064. 벡터 프로세서 (Vector Processor)
065. 데이터 센터 서버 아키텍처 (Data Center Server Architecture)
066. 블레이드 서버·랙 서버 (Blade Server Rack Server)
067. 전원 공급 장치·UPS (Power Supply UPS) [출제:126회]
068. 데이터 센터 등급 — TIA-942 Tier 1~4 (Data Center Tier) [출제:129회]
069. 냉각 시스템 — 공랭·수랭·액침냉각 (Cooling System)
070. 전력 사용 효율 PUE (Power Usage Effectiveness) [출제:138회]
071. 물 사용 효율 WUE (Water Usage Effectiveness) [출제:138회]
072. 임베디드 시스템 구조 (Embedded System Architecture) [출제:137회]
073. RTOS 실시간 운영체제 (Real-Time Operating System) [출제:137회]
074. 하드·소프트 실시간 (Hard Soft Real-Time) [출제:137회]
075. 인터럽트 레이턴시·우선순위 역전 (Interrupt Latency Priority Inversion) [출제:137회]
076. ARM TrustZone 보안 익스텐션 (ARM TrustZone) [출제:138회]
077. JTAG 디버깅 인터페이스 (JTAG) [출제:126회]
078. CAN 버스 통신 (CAN Bus) [출제:129회]
079. AUTOSAR 소프트웨어 플랫폼 (AUTOSAR) [출제:138회]
080. Secure Boot 보안 부팅 (Secure Boot) [출제:138회]
081. 펌웨어 보안 취약점 (Firmware Security) [출제:138회]
082. 하드웨어 보안 모듈 HSM (Hardware Security Module)
083. PUF 물리적 복제 불가 함수 (Physical Unclonable Function) [출제:125회]
084. 디바이스 DNA (Device DNA) [출제:125회]
085. 양자 컴퓨팅 큐비트 (Quantum Computing Qubit) [출제:126,129,135,136회]
086. 초전도·이온 트랩 양자 프로세서 (Quantum Processor Technologies) [출제:135회]
087. 양자 얽힘·중첩 (Quantum Entanglement Superposition) [전망]
088. 양자 오류 정정 — 표면 코드 (Quantum Error Correction Surface Code) [출제:138회]
089. 논리 큐비트 vs 물리 큐비트 (Logical vs Physical Qubit) [출제:138회]
090. 메모리 인터리빙 (Memory Interleaving)
091. 버스 대역폭·전송률 계산 (Bus Bandwidth)
092. 데이터 흐름 컴퓨터 (Dataflow Computer) [전망]
093. AMBA 버스 프로토콜 (AMBA Bus Protocol)
094. PCIe 스위칭 아키텍처 (PCIe Switching)
095. 스토리지 계층 — DAS·NAS·SAN (Storage DAS NAS SAN)
096. 스토리지 가상화 (Storage Virtualization)
097. NVDIMM 비휘발성 메모리 (NVDIMM Non-Volatile DIMM) [전망]
098. 퍼시스턴트 메모리 (Persistent Memory) [전망]
099. 마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)
100. SoC AI 온디바이스 칩 (SoC On-Device AI Chip) [출제:134,135회]
101. 하드웨어 가상화 — VT-x·AMD-V (Hardware Virtualization) [출제:137회]
102. IOMMU (IOMMU)
103. 서버 가상화 — Type 1·Type 2 하이퍼바이저 (Hypervisor Types) [출제:128,131,132,137회]
104. 고속 직렬 인터페이스 — USB·Thunderbolt (High-Speed Serial Interface)
105. 광 인터커넥트 (Optical Interconnect) [전망]
106. 3D 적층 메모리 (3D Stacked Memory) [출제:126회]
107. 하드웨어 성능 카운터·PMU (Hardware Performance Counter PMU)
108. RAID 컨트롤러·JBOD (RAID Controller JBOD)
109. 멀티소켓 서버·SMP (Multi-Socket Server SMP)
110. 인터커넥트 토폴로지 — 팻트리·토러스 (Interconnect Topology Fat Tree Torus) [출제:138회]
