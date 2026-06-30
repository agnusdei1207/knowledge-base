---
title: "01 컴퓨터구조 기출-grounded 키워드 워크리스트"
date: "2026-06-30"
tags:
  - "exam-keywords"
  - "cspe"
  - "keyword-worklist"
weight: 1
---

# 01 컴퓨터구조 기출-grounded 키워드 워크리스트 (목표 ~90개)
> 출처: 120~138회 컴퓨터시스템응용기술사 기출 대조 + content/exam/cs/keyword_list.md + frequency.md + keyword-universe.md + 출제 전망.

## 챕터: 01_overview
001. 부울대수·카르노맵
002. 조합/순차 논리회로
003. 플립플롭
004. 2의 보수
005. 부동소수점(IEEE 754·FP32/FP16/bfloat16) [출제:137회]
006. 오버플로우·언더플로우
007. 해밍코드
008. CRC·체크섬
009. 빅/리틀 엔디안
010. ALU
011. 폰 노이만 아키텍처·병목현상
012. 하버드 아키텍처
013. CPI·IPC·MIPS·FLOPS
014. 성능방정식
015. 암달의 법칙(Amdahl's Law)
016. 구스타프슨의 법칙
017. 무어의 법칙·데나드 스케일링
018. SPEC 벤치마크
019. ISA
020. 주소지정방식
021. RISC vs CISC
022. x86·ARM·RISC-V [출제:137회]
023. SIMD(AVX·NEON)
024. 명령어 사이클
025. 하드와이어드/마이크로프로그래밍 제어
026. 명령어 파이프라이닝(IF·ID·EX·MEM·WB)
027. 파이프라인 해저드(구조·데이터·제어)
028. RAW·WAR·WAW
029. 데이터 포워딩
030. 파이프라인 스톨
031. 분기예측(정적·동적·BTB·BHT)
032. 수퍼스칼라
033. 비순차실행(OoO)
034. 레지스터 리네이밍
035. 토마술로 알고리즘
036. ROB
037. VLIW
038. 메모리 계층구조
039. 참조의 지역성(시간·공간)
040. SRAM·DRAM·DDR
041. 캐시메모리(L1/L2/L3) [출제:125,131,132,134회]
042. 적중률·AMAT
043. 캐시 사상(직접·완전연관·집합연관) [출제:125,131,132,134회]
044. 캐시미스 3C [출제:125,131,132,134회]
045. 교체알고리즘(LRU·LFU·FIFO)
046. 쓰기정책(Write-Through·Write-Back)·더티비트
047. 프리패칭
048. 가상메모리·MMU [출제:125,135회]
049. 페이징·페이지테이블
050. TLB [출제:125,135회]
051. 세그멘테이션
052. 단편화(내부·외부)
053. 요구페이징·페이지폴트
054. 페이지교체(OPT·LRU·클럭)
055. 스래싱·워킹셋
056. 플린의 분류법(SISD·SIMD·MIMD)
057. 벡터 프로세서
058. 공유/분산 메모리
059. UMA·NUMA
060. SMP
061. 클러스터·그리드 컴퓨팅
062. TLP·DLP
063. 멀티코어·big.LITTLE
064. 동시멀티스레딩(SMT·하이퍼스레딩)
065. 캐시 일관성(Cache Coherence) [출제:125,131,132,134회]
066. 스누핑·디렉터리 프로토콜
067. MESI/MOESI
068. 거짓공유(False Sharing)
069. 메모리 일관성 모델
070. Test-and-Set·CAS
071. 메모리 배리어
072. 인터럽트·DMA [출제:128,132회]
073. 폴링
074. HDD(탐색시간)·SSD(웨어레벨링·FTL)
075. RAID(0·1·5·6·10)
076. SAN·NAS·DAS [출제:138회]
077. NVMe·NVMe-oF
078. PCIe·RDMA [출제:137회]
079. GPU·CUDA·SIMT [출제:126,134,136,137회]
080. NPU·TPU(시스톨릭 어레이) [출제:126,134,135,136,137,138회]
081. 텐서코어
082. PIM(Processing-In-Memory)·메모리월 [출제:129,131회]
083. CXL·메모리풀링 [출제:129회] [전망]
084. HBM·칩렛 [출제:129,131,138회] [전망]
085. ECC메모리
086. DVFS
087. TEE(TrustZone·SGX)·Secure Boot
088. 사이드채널공격(Spectre·Meltdown·Rowhammer)
089. 뉴로모픽 컴퓨팅 [출제:128회]

## 챕터: 02_data_representation_arithmetic
090. FRAM 강유전체 RAM (Ferroelectric RAM) [출제:138회]

## 챕터: 03_architecture_basics_performance
091. CPU 레지스터와 상태 레지스터 (CPU Register and Status Register) [출제:138회]
092. ROM 종류 PROM EPROM EEPROM Flash (Read Only Memory) [출제:138회]

## 챕터: 09_system_bus_interconnects
093. 시스템 버스와 버스 중재 (System Bus and Bus Arbitration) [출제:137회]

## 챕터: 08_io_storage_systems
094. DMA SG-DMA RDMA 비교 (DMA SG-DMA RDMA) [출제:137회]
095. IOMMU 입출력 메모리 관리장치 (I/O Memory Management Unit) [출제:137회]

## 챕터: 12_accelerators_ai_hardware
096. SNN 스파이킹 신경망 하드웨어 (Spiking Neural Network Hardware) [출제:138회]

> 생성 기준: 총 96개. 목표 수는 시험 출제 가능성 기준의 운영 상한이며, 지엽 키워드는 제외한다.
