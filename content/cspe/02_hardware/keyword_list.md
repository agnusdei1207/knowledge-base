---
title: "Keyword List"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 50
---

<하드웨어 시스템 키워드 목록 (110제)>
컴퓨터시스템응용기술사 시험 출제동향 기반으로 엄선한 하드웨어 시스템 핵심 키워드입니다.

---

## 1. CPU 아키텍처 (16개)
1. 컴퓨터 구조 개요 (Von Neumann vs Harvard Architecture) — 폰 노이만과 하버드 아키텍처의 구조적 차이 비교
2. CPU 구성 (CPU Components) — ALU·CU·레지스터·버스 등 CPU 핵심 구성요소
3. 명령어 집합 (ISA RISC CISC) — RISC와 CISC 명령어 집합 구조 비교 [출제:124회]
4. RISC-V 오픈 ISA (RISC-V) — 개방형 명령어 집합 아키텍처 표준 [출제:127회]
5. ARM 프로세서 아키텍처 (ARM Architecture) — ARM 프로세서의 동작 모드와 아키텍처 특성 [출제:126회]
6. x86-64 아키텍처 (x86-64 Architecture) — 인텔·AMD의 64비트 확장 아키텍처
7. 파이프라이닝 기본 구조 5단계 (Pipelining) — IF·ID·EX·MEM·WB 5단계 파이프라인 [출제:122회]
8. 파이프라인 해저드 (Pipeline Hazards) — 데이터·제어·구조적 해저드 유형과 해결 기법 [출제:122,135회]
9. 파이프라인 포워딩·분기 예측 (Pipeline Forwarding Branch Prediction) — 해저드 해결을 위한 포워딩과 분기 예측 기법 [출제:122회]
10. 슈퍼스칼라 아키텍처 (Superscalar) — 다중 실행 유닛을 통한 명령어 수준 병렬 처리 [출제:136회]
11. VLIW 아키텍처 (VLIW) — 컴파일러 기반 병렬 명령어 패킹 구조 [출제:136회]
12. 비순서 실행·레지스터 리네이밍 (Out-of-Order Execution Register Renaming) — 실행 순서 재배치와 WAR/WAW 해저드 제거 기법 [출제:136회]
13. 명령어 수준 병렬성 ILP (Instruction-Level Parallelism) — 명령어 간 병렬 실행 가능성 분석 [출제:136회]
14. 멀티코어 프로세서 (Multicore Processor) — 단일 칩 내 다수 코어 집적 구조 [출제:132회]
15. 폴락의 법칙 (Pollack's Rule) — 트랜지스터 수 대비 성능 향상 한계 법칙 [출제:132회]
16. 하이퍼스레딩·SMT (Simultaneous Multithreading) — 단일 코어에서 다중 스레드 동시 실행 기술 [전망]

## 2. 메모리 시스템 (19개)
17. 캐시 메모리 구조 (Cache Memory Mapping) — 직접·연관·집합 연관 매핑 방식 비교 [출제:120,125,131,132,134,135회]
18. 캐시 쓰기 정책 (Cache Write Policy) — Write-Through와 Write-Back 정책 비교 [출제:129회]
19. 캐시 일관성 프로토콜 (Cache Coherence Protocol) — MESI·MOESI 프로토콜 동작 원리 [출제:123,135회]
20. 버스 스누핑·디렉터리 기반 일관성 (Bus Snooping Directory Coherence) — 멀티프로세서 캐시 일관성 유지 방식 [출제:123회]
21. TLB 변환 색인 버퍼 (Translation Lookaside Buffer) — 가상→물리 주소 변환 캐시 [출제:135회]
22. 가상 메모리 (Virtual Memory Paging Segmentation) — 페이징과 세그멘테이션 기반 가상 메모리 관리 [출제:120,121,125회]
23. 페이지 교체 알고리즘 (Page Replacement) — OPT·FIFO·LRU·LFU 알고리즘 비교 [출제:121회]
24. 세그멘테이션 (Segmentation) — 세그먼트 단위 메모리 관리 기법 [출제:126회]
25. MMU 메모리 관리 장치 (Memory Management Unit) — 하드웨어 기반 주소 변환 장치 [출제:135회]
26. NUMA 비균등 메모리 접근 (Non-Uniform Memory Access) — 멀티프로세서 환경의 비대칭 메모리 접근 구조 [출제:127회]
27. 메모리 계층 구조 (Memory Hierarchy) — 레지스터~디스크까지 계층적 메모리 구성 [출제:123회]
28. DRAM vs SRAM (DRAM SRAM) — 휘발성 메모리 유형별 구조·속도·용도 비교 [출제:125회]
29. DDR SDRAM·갱신 방식 (DDR SDRAM Refresh) — DDR 세대별 특성과 리프레시 방식 [출제:129회]
30. 메모리 인터리빙 (Memory Interleaving) — 다중 메모리 뱅크 병렬 접근 기법
31. NVDIMM 비휘발성 메모리 (NVDIMM Non-Volatile DIMM) — 비휘발성 DIMM 기술로 전원 차단 시 데이터 보존 [전망]
32. 퍼시스턴트 메모리 (Persistent Memory) — 바이트 단위 접근 가능한 비휘발성 메모리 기술 [전망]
33. HBM 고대역폭 메모리 (High Bandwidth Memory) — TSV 기반 고대역폭 3D 적층 메모리 [출제:129,131회]
34. HBM3E (HBM3E) — 차세대 고대역폭 메모리 확장 규격 [전망]
35. HBM4 (HBM4) — 4세대 고대역폭 메모리 표준 [전망]

## 3. 버스 및 I/O (10개)
36. I/O 인터페이스 (I/O Interface) — 폴링·인터럽트·DMA·채널 I/O 방식 비교 [출제:128,132회]
37. 인터럽트 처리 방식 (Interrupt Handling) — 벡터·데이지체인 인터럽트 처리 기법 [출제:128,132회]
38. DMA 직접 메모리 접근 (Direct Memory Access) — CPU 개입 없는 메모리-장치 간 직접 전송 [출제:128회]
39. 버스 중재 방식 (Bus Arbitration) — 중앙집중·분산 버스 사용권 할당 기법 [출제:128회]
40. 3-상태 버퍼·트라이스테이트 (Tri-State Buffer) — 버스 공유를 위한 3-상태 출력 회로 [출제:129회]
41. 버스 대역폭·전송률 계산 (Bus Bandwidth) — 버스 클럭·폭 기반 전송률 산정 방법
42. AMBA 버스 프로토콜 (AMBA Bus Protocol) — ARM 기반 SoC 온칩 버스 표준 프로토콜
43. NVMe·PCIe 인터페이스 (NVMe PCIe) — 고속 SSD 연결을 위한 NVMe/PCIe 인터페이스
44. PCIe 스위칭 아키텍처 (PCIe Switching) — PCIe 스위치 기반 다중 장치 연결 구조
45. 고속 직렬 인터페이스 (High-Speed Serial Interface) — USB·Thunderbolt 등 고속 직렬 통신 인터페이스

## 4. 저장 장치 (7개)
46. SSD FTL 플래시 변환 계층 (Flash Translation Layer) — 논리-물리 블록 매핑 관리 계층 [출제:128회]
47. NAND 플래시·3D V-NAND (NAND Flash 3D V-NAND) — 수직 적층 플래시 메모리 기술 [출제:126회]
48. RAID 레벨 0·1·5·6·10 비교 (RAID Levels) — 디스크 어레이 레벨별 성능·신뢰성 비교 [출제:125,131,136회]
49. RAID 컨트롤러·JBOD (RAID Controller JBOD) — RAID 컨트롤러와 단순 디스크 연결(JBOD) 비교
50. 광 저장 장치 (Optical Storage) — CD·DVD·Blu-ray 등 광학 매체 기반 저장 장치
51. 스토리지 계층 — DAS·NAS·SAN (Storage DAS NAS SAN) — 직접·네트워크·SAN 스토리지 아키텍처 비교
52. 스토리지 가상화 (Storage Virtualization) — 물리적 스토리지 자원의 논리적 추상화 기술

## 5. 특수 프로세서 및 AI 가속기 (11개)
53. GPU 아키텍처·SIMT 모델 (GPU SIMT) — GPU의 SIMT 실행 모델과 병렬 처리 구조 [출제:124,126,134,136회]
54. CUDA 병렬 컴퓨팅 (CUDA Parallel Computing) — NVIDIA GPU 병렬 프로그래밍 플랫폼 [출제:135회]
55. TPU 텐서 처리 장치 (Tensor Processing Unit) — 구글 맞춤형 AI 행렬 연산 가속기 [출제:126,134,136회]
56. NPU 신경망 처리 장치 (Neural Processing Unit) — 딥러닝 추론 전용 가속 프로세서 [출제:126,134,135,136,137,138회]
57. Edge TPU (Edge TPU) — 엣지 디바이스용 경량 AI 추론 프로세서 [출제:138회]
58. AI 가속기 비교 (AI Accelerator Comparison) — CPU·GPU·NPU·FPGA·ASIC 가속기 특성 비교 [출제:126,134,136,137회]
59. SOC 시스템온칩 (System on Chip) — CPU·GPU·메모리 등 통합 단일 칩 [출제:128회]
60. FPGA AI 가속 (FPGA AI Acceleration) — 현장 프로그래머블 게이트 어레이 기반 AI 가속 [출제:126,134회]
61. ASIC AI 가속 (ASIC AI Acceleration) — 주문형 반도체를 활용한 AI 전용 가속 [출제:126,134회]
62. 병렬 컴퓨터 분류 — Flynn 분류 (Flynn's Taxonomy) — SISD·SIMD·MISD·MIMD 분류 체계 [출제:131,134회]
63. SIMD·MIMD 프로세서 (SIMD MIMD) — 단일/다중 명령·데이터 스트림 처리 구조 [출제:131,134회]

## 6. 임베디드 시스템 (9개)
64. 임베디드 시스템 구조 (Embedded System Architecture) — 특정 기능 전용 하드웨어·소프트웨어 통합 시스템 [출제:137회]
65. RTOS 실시간 운영체제 (Real-Time Operating System) — 실시간 태스크 스케줄링 기반 운영체제 [출제:137회]
66. 하드·소프트 실시간 (Hard Soft Real-Time) — 데드라인 엄격도에 따른 실시간 시스템 분류 [출제:137회]
67. 인터럽트 레이턴시·우선순위 역전 (Interrupt Latency Priority Inversion) — 인터럽트 응답 시간과 우선순위 역전 문제 [출제:137회]
68. 마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor) — MCU와 MPU의 구조적 차이 및 용도 비교
69. SoC AI 온디바이스 칩 (SoC On-Device AI Chip) — 엣지 AI 처리를 위한 시스템온칩 설계 [출제:134,135회]
70. JTAG 디버깅 인터페이스 (JTAG) — 임베디드 시스템 테스트·디버깅 표준 인터페이스 [출제:126회]
71. CAN 버스 통신 (CAN Bus) — 차량·산업용 직렬 통신 프로토콜 [출제:129회]
72. AUTOSAR 소프트웨어 플랫폼 (AUTOSAR) — 자동차 전장 소프트웨어 표준 플랫폼 [출제:138회]

## 7. 서버 및 고가용성 (12개)
73. 데이터 센터 서버 아키텍처 (Data Center Server Architecture) — 대규모 서버 인프라 설계 및 구성
74. 블레이드 서버·랙 서버 (Blade Server Rack Server) — 서버 폼팩터별 특성과 집적 밀도 비교
75. 멀티소켓 서버·SMP (Multi-Socket Server SMP) — 대칭적 다중 프로세서 서버 구조
76. 전원 공급 장치·UPS (Power Supply UPS) — 무정전 전원공급 장치와 이중화 전원 설계 [출제:126회]
77. 데이터 센터 등급 — TIA-942 Tier 1~4 (Data Center Tier) — 가용성 등급별 데이터 센터 인프라 기준 [출제:129회]
78. 냉각 시스템 (Cooling System) — 공랭·수랭·액침냉각 등 열관리 기술
79. 전력 사용 효율 PUE (Power Usage Effectiveness) — 데이터 센터 전력 효율 지표 [출제:138회]
80. 물 사용 효율 WUE (Water Usage Effectiveness) — 데이터 센터 수자원 사용 효율 지표 [출제:138회]
81. 하드웨어 가상화 (Hardware Virtualization) — VT-x·AMD-V 하드웨어 가상화 지원 기술 [출제:137회]
82. IOMMU (IOMMU) — I/O 장치의 메모리 접근 가상화 및 보호 장치
83. 서버 가상화 — Type 1·Type 2 하이퍼바이저 (Hypervisor Types) — 베어메탈·호스티드 하이퍼바이저 비교 [출제:128,131,132,137회]
84. 벡터 프로세서 (Vector Processor) — 벡터 연산 전용 대규모 병렬 데이터 처리 장치

## 8. 하드웨어 보안 (6개)
85. ARM TrustZone 보안 익스텐션 (ARM TrustZone) — Secure/Normal 월드 분리 기반 보안 아키텍처 [출제:138회]
86. Secure Boot 보안 부팅 (Secure Boot) — 부팅 체인 무결성 검증 보안 메커니즘 [출제:138회]
87. 펌웨어 보안 취약점 (Firmware Security) — 펌웨어 레벨 공격 벡터와 방어 기법 [출제:138회]
88. 하드웨어 보안 모듈 HSM (Hardware Security Module) — 암호키 관리·생성 전용 보안 하드웨어
89. PUF 물리적 복제 불가 함수 (Physical Unclonable Function) — 칩 고유 물리적 특성 기반 인증 기술 [출제:125회]
90. 디바이스 DNA (Device DNA) — 반도체 제조 편차를 이용한 고유 식별 기술 [출제:125회]

## 9. 반도체 및 패키징 (7개)
91. Chiplet 칩렛 (Chiplet) — 이종 다이 조합 기반 모듈형 반도체 설계 [출제:131회]
92. UCIe 칩렛 인터커넥트 (Universal Chiplet Interconnect Express) — 칩렛 간 표준 인터커넥트 규격 [전망]
93. 3D 적층 메모리 (3D Stacked Memory) — TSV 기반 수직 적층 메모리 패키징 기술 [출제:126회]
94. CXL 컴퓨트 익스프레스 링크 (Compute Express Link) — CPU-장치 간 캐시 일관성 지원 인터커넥트 [출제:129회]
95. CXL 메모리 풀링 (CXL Memory Pooling) — CXL 기반 메모리 자원 공유·풀링 기술 [전망]
96. NVLink 고속 인터커넥트 (NVLink) — NVIDIA GPU 간 고속 데이터 전송 링크 [출제:138회]
97. InfiniBand (InfiniBand) — HPC·AI 클러스터용 초고속 네트워크 인터커넥트 [출제:138회]

## 10. 차세대 컴퓨팅 (13개)
98. 양자 컴퓨팅 큐비트 (Quantum Computing Qubit) — 양자 비트 기본 개념과 양자 게이트 [출제:126,129,135,136회]
99. 초전도·이온 트랩 양자 프로세서 (Quantum Processor Technologies) — 초전도·이온 트랩 방식 양자 프로세서 비교 [출제:135회]
100. 양자 얽힘·중첩 (Quantum Entanglement Superposition) — 양자역학 기본 원리와 컴퓨팅 응용 [전망]
101. 양자 오류 정정 — 표면 코드 (Quantum Error Correction Surface Code) — 양자 오류 정정을 위한 표면 코드 기법 [출제:138회]
102. 논리 큐비트 vs 물리 큐비트 (Logical vs Physical Qubit) — 오류 정정된 논리 큐비트와 물리 큐비트 관계 [출제:138회]
103. PIM 메모리 내 처리 (Processing-in-Memory) — 메모리 칩 내부 연산 처리 기술 [출제:129,131회]
104. PNM 메모리 근접 처리 (Processing Near Memory) — 메모리 인접 프로세서 배치 아키텍처 [출제:131회]
105. 인메모리 컴퓨팅 (In-Memory Computing) — 메모리 내 직접 연산으로 데이터 이동 최소화 [전망]
106. 뉴로모픽 컴퓨팅 (Neuromorphic Computing) — 뇌 신경망 모사 비폰노이만 컴퓨팅 아키텍처 [출제:128회]
107. 데이터 흐름 컴퓨터 (Dataflow Computer) — 데이터 의존성 기반 비순차 실행 아키텍처 [전망]
108. 광 인터커넥트 (Optical Interconnect) — 광신호 기반 칩 간·보드 간 초고속 통신 [전망]
109. 인터커넥트 토폴로지 (Interconnect Topology Fat Tree Torus) — 팻트리·토러스 등 대규모 시스템 연결 구조 [출제:138회]
110. 하드웨어 성능 카운터·PMU (Hardware Performance Counter PMU) — CPU 성능 모니터링 유닛과 하드웨어 이벤트 카운터
