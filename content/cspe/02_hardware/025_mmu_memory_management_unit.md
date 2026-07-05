---
title: "MMU 메모리 관리 장치 (Memory Management Unit)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 25
---

## Ⅰ. 개요
- **정의**: CPU가 발행한 가상 주소를 물리 주소로 변환하고 접근 권한을 하드웨어 수준에서 검증하는 온칩 프로세싱 유닛임
- **배경/필요성**: 멀티태스킹 환경에서 매 사이클 발생하는 주소 변환과 메모리 보호를 소프트웨어로 처리하면 파이프라인 지연이 발생하므로 전용 하드웨어가 필수적임
- **비유**: 공항 자동 출입국 심사대와 같음. 여권(가상 주소)을 스캔하면 DB(페이지 테이블)와 대조하여 즉시 통과시키거나 자격 미달 시 알람(Fault)을 울림

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 주소 변환 메커니즘 | TLB(021 참조)+Page Table Walk 협력 구조 | 주소 변환 기능만 서술하고 보호 기능 누락 금지 |
| HW/OS 역할 분담 | MMU는 정책 집행(HW), OS는 정책 결정(SW) | MMU가 페이지 테이블을 관리한다고 서술 금지 |
| 보안/가상화 확장 | KPTI, EPT/NPT, IOMMU 등 현대적 확장 | 단일 코어 전통 모델에만 한정 서술 금지 |

> 요약: 가상-물리 주소 변환과 접근 권한 검증을 파이프라인 내에서 수행하는 하드웨어 유닛임

## Ⅱ. 구성요소
```text
CPU Core ---(VA)---> +---------------------+ ---(PA)---> RAM
                     |        MMU          |
                     |  +------+  +------+ |
                     |  | TLB  |  | PTBR | |
                     |  +------+  +------+ |
                     |  +---------------+  |
                     |  | Page Table    |  |
                     |  | Walker        |  |
                     |  +---------------+  |
                     |  +---------------+  |
                     |  | Protection    |  |
                     |  | Logic (R/W/X) |  |
                     |  +---------------+  |
                     +---------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| TLB(021 참조) | 최근 주소 변환 결과를 CAM 방식으로 캐싱하여 1클럭 내 검색을 수행하는 고속 버퍼 | 즐겨찾기 목록 |
| Page Table Walker | TLB Miss 시 PTBR이 가리키는 DRAM 내 다단계 페이지 테이블을 하드웨어적으로 순회하는 회로 | 원본 명부를 찾아 뒤지는 사서 |
| Protection Logic | 페이지 엔트리의 R/W/X 비트와 CPU 특권 레벨(Ring)을 대조하여 위반 시 트랩을 발생시키는 검증 회로 | 보안 등급별 카드키 시스템 |
| PTBR/CR3 | 현재 프로세스의 페이지 테이블 루트 주소를 보관하는 레지스터. 컨텍스트 스위칭 시 OS가 값을 교체함 | 현재 참조할 캐비닛 번호 |

> 요약: TLB, Page Table Walker, Protection Logic, PTBR로 구성되어 변환과 보호를 동시 수행함

## Ⅲ. 절차
```text
VA 수신 --> TLB 검색 --Hit--> 권한 검사 --Pass--> PA 출력
               |                  |
             Miss              Fail
               |                  |
               v                  v
        Page Table Walk     Protection Fault (OS Trap)
               |
               v
        Valid? --No--> Page Fault (OS Trap)
               |
              Yes
               |
               v
        TLB 갱신 + PA 출력
```
- 1단계: CPU가 가상 주소를 발행하면 MMU가 VPN을 추출하여 TLB에 병렬 검색을 수행함
- 2단계: TLB Miss 시 Page Table Walker가 PTBR/CR3을 참조하여 DRAM 내 4~5단계 페이지 테이블을 순회함
- 3단계: 해당 엔트리의 Valid 비트가 0이면 Page Fault, R/W/X 권한이 CPU 모드와 불일치하면 Protection Fault를 발생시켜 OS로 제어권을 넘김
- 4단계: 검증 통과 시 PFN+Offset을 결합한 물리 주소를 메모리 컨트롤러로 전송하고, Miss였던 경우 TLB를 갱신함

> 요약: TLB 검색 -> Miss 시 테이블 순회 -> 유효성/권한 검증 -> 물리 주소 출력의 4단계로 동작함

## Ⅳ. 문제점
- Page Table Walk 지연: TLB Miss 시 DRAM 내 4~5단계 테이블 순회로 수십~수백 사이클의 지연이 발생하여 파이프라인이 정체됨
- 부채널 공격 노출: Meltdown 공격에서 투기적 실행(Speculative Execution) 중 커널 주소의 TLB 엔트리가 유저 모드에 노출되는 취약점이 발생함
- 가상화 이중 변환 부하: VM 환경에서 게스트 가상 주소 -> 게스트 물리 주소 -> 호스트 물리 주소의 2단 변환으로 테이블 순회 횟수가 제곱으로 증가함

> 요약: TLB Miss 지연, 부채널 공격 취약점, 가상화 이중 변환 부하가 주요 문제임

## Ⅴ. 개선방안
1. 단기: Huge Page(2MB/1GB) 적용과 멀티레벨 TLB(L1/L2) 도입으로 테이블 순회 단계를 줄이고 TLB 적중률을 향상시킴
2. 중기: KPTI(Kernel Page Table Isolation) 적용으로 유저/커널 페이지 테이블을 분리하여 투기적 실행 중 커널 주소 노출을 차단함
3. 장기: EPT/NPT(Extended/Nested Page Table) 하드웨어 지원과 IOMMU 연동으로 게스트-호스트 간 변환을 하드웨어가 직접 수행하여 이중 변환 부하를 흡수함

> 요약: Huge Page/멀티레벨 TLB, KPTI, EPT/NPT+IOMMU로 각 문제를 단계적으로 해소함

## Ⅵ. 전망
- 발전 방향: CXL 기반 메모리 풀링 환경에서 원격 메모리 주소 변환을 관리하는 확장 MMU 아키텍처가 부상함
- 기술사적 판단: MMU는 주소 변환기를 넘어 가상화(Nested Paging)와 보안(TrustZone/Enclave)을 하드웨어적으로 앵커링하는 플랫폼 신뢰 기점으로 진화 중임
- 기술사 제언: MMU 성능 카운터(`perf stat`의 dTLB-load-misses 등)를 활용하여 워크로드별 TLB Miss율과 Walk 지연을 정량 분석하고, Huge Page/ASID 설정을 최적화할 것을 권고함
