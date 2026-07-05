---
title: "TLB 변환 색인 버퍼 (Translation Lookaside Buffer)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 21
---

## Ⅰ. 개요
- **정의**: 가상 주소에서 물리 주소로의 변환 결과를 캐싱하는 MMU 내부 고속 하드웨어 캐시임
- **배경/필요성**: 가상 메모리 환경에서 매 메모리 접근마다 페이지 테이블을 참조하면 메모리 접근이 2회로 늘어나 성능 병목이 발생함
- **비유**: 자주 거는 전화번호를 단축번호로 저장해 두고, 두꺼운 전화번호부를 매번 뒤지지 않는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 가상 메모리 성능 최적화 원리 | TLB Hit/Miss 흐름과 EAT 산출 | 주소 변환만 서술하고 보호 기능 누락 금지 |
| MMU(025 참조)와의 협력 구조 | CAM 기반 병렬 검색과 ASID 활용 | TLB를 SW 캐시로 오해하는 서술 금지 |
| 성능 병목 진단 능력 | TLB Thrashing과 Huge Page 대응 | 적중률만 언급하고 미스 페널티 분석 누락 금지 |

> 요약: 가상-물리 주소 변환을 MMU 내 CAM 캐시로 가속하여 메모리 접근 지연을 최소화하는 장치임

## Ⅱ. 구성요소
```text
CPU --- VPN+Offset ---> +----------+
                        |   TLB    |--- Hit ---> PFN+Offset ---> 물리 주소
                        | (CAM)    |
                        +----------+
                            |
                          Miss
                            |
                            v
                     Page Table (DRAM)
                            |
                            v
                     PFN 획득 + TLB 갱신
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| CAM(Content Addressable Memory) | VPN을 입력하면 모든 엔트리를 1클럭에 병렬 비교하여 PFN을 반환하는 특수 메모리 소자 | 도서관 전자 검색 시스템 |
| VPN/PFN 매핑 엔트리 | 가상 페이지 번호와 물리 프레임 번호의 쌍을 저장하는 레코드 | 전화번호부의 이름-번호 쌍 |
| ASID(Address Space ID) | 엔트리에 프로세스 식별 태그를 부여하여 컨텍스트 스위칭 시 TLB Flush를 방지하는 필드 | 단축번호에 붙인 소유자 이름표 |
| Valid/Dirty 비트 | 엔트리 유효 여부와 해당 페이지 수정 여부를 표시하는 상태 플래그 | 메모장 항목의 유효/수정 체크 표시 |

> 요약: CAM 기반 병렬 검색, VPN-PFN 매핑, ASID 태그, 상태 비트로 구성됨

## Ⅲ. 절차
```text
VPN 입력 --> TLB 병렬 검색 --> Hit? --Yes--> 권한 검사 --> 물리 주소 출력
                                |
                               No
                                |
                                v
                         Page Table Walk --> PFN 획득 --> TLB 갱신 --> 물리 주소 출력
```
- 1단계: CPU가 가상 주소를 발행하면 MMU(025 참조)가 VPN을 추출하여 TLB에 전달함
- 2단계: TLB가 CAM 회로로 모든 엔트리를 병렬 비교하여 Hit/Miss를 판정함
- 3단계: Miss 시 Page Table Walker가 DRAM의 페이지 테이블을 다단계 순회하여 PFN을 획득하고, 결과를 TLB에 갱신함
- 4단계: Hit 또는 갱신 완료 후 PFN+Offset을 결합하여 물리 주소를 생성하고, 권한 비트(R/W/X)를 검증함

> 요약: VPN 추출 -> CAM 병렬 검색 -> Miss 시 페이지 테이블 순회 -> 물리 주소 생성의 4단계로 동작함

## Ⅳ. 문제점
- TLB Thrashing: 워킹셋이 TLB 용량(수백 엔트리)을 초과하면 지속적 Miss가 발생하여 매 접근마다 DRAM 페이지 테이블 순회 비용이 추가됨
- 컨텍스트 스위칭 Flush: ASID 미지원 환경에서 프로세스 전환 시 TLB 전체를 무효화하면 전환 직후 Cold Miss가 집중 발생함
- 멀티코어 일관성 부하: 각 코어가 독립 TLB를 보유하므로 페이지 테이블 변경 시 TLB Shootdown IPI(Inter-Processor Interrupt) 오버헤드가 코어 수에 비례하여 증가함

> 요약: 용량 한계에 의한 Thrashing, 프로세스 전환 시 Flush, 멀티코어 일관성 비용이 주요 문제임

## Ⅴ. 개선방안
1. 단기: Huge Page(2MB/1GB) 적용으로 한 엔트리가 커버하는 주소 범위를 확대하여 TLB Thrashing을 완화함
2. 중기: ASID/PCID 하드웨어를 활용하여 프로세스별 엔트리를 태그로 구분함으로써 컨텍스트 스위칭 시 Flush를 제거함
3. 장기: 코어 간 TLB 일관성 프로토콜을 배치 처리(Batched Shootdown)로 전환하고, 하드웨어 브로드캐스트 무효화 회로를 도입하여 IPI 횟수를 감소시킴

> 요약: Huge Page, ASID/PCID, 배치 Shootdown으로 각 문제를 단계적으로 해소함

## Ⅵ. 전망
- 발전 방향: L1/L2 멀티레벨 TLB 계층화, CXL 메모리 확장 환경에서의 원격 TLB 관리 기술이 부상함
- 기술사적 판단: 가상화 환경에서 EPT/NPT(Extended/Nested Page Table) 이중 변환 부하를 TLB가 흡수하는 구조 설계가 필수적임
- 기술사 제언: TLB 적중률 모니터링(`perf stat` 등)을 통해 워킹셋 크기와 TLB 용량의 균형을 정량적으로 관리할 것을 권고함
