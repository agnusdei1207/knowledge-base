---
title: "SSD FTL 플래시 변환 계층 (Flash Translation Layer)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 38
extra:
  question_no: "038"
  exam_status: "기출"
  exam_history: "128회"
---

## 미리 알고가기

- FTL은 호스트가 보는 LBA를 NAND 실제 위치인 PBA로 바꾸는 계층임
- NAND는 덮어쓰기가 안 되고 page 단위 쓰기와 block 단위 erase가 분리되어 있음
- 가비지 컬렉션과 wear leveling 품질이 SSD 성능과 수명을 좌우함

## Ⅰ. 개요

- **정의/개념**: FTL은 SSD 컨트롤러 내부에서 논리 블록 주소를 NAND 물리 주소로 매핑하고, out-of-place update, 가비지 컬렉션, wear leveling을 수행해 NAND의 물리 제약을 호스트로부터 숨기는 핵심 제어 계층임
- **배경/필요성**: NAND는 덮어쓰기 불가·수명 제한·오류 축적 특성을 가지므로, 이를 직접 노출하면 범용 블록 장치처럼 쓰기 어렵기 때문에 중간 번역 계층이 필요함

## Ⅱ. 특징

- 호스트는 일반 블록 장치처럼 접근하지만 내부에서는 새 위치 쓰기와 재매핑이 수행됨
- 매핑 granularity에 따라 DRAM 사용량과 random write 성능이 달라짐
- 가비지 컬렉션과 wear leveling이 동시에 돌아가므로 장기 지연 안정성이 핵심 품질 지표임
- 전원 장애 시 매핑 메타데이터 보호가 안 되면 데이터 무결성 문제가 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 페이지 매핑 | 블록 매핑 | 하이브리드 매핑 |
|:---|:---|:---|:---|
| 매핑 단위 | 세밀한 page 단위로 관리함 | 큰 block 단위로 관리함 | hot data는 page, bulk data는 block 수준으로 혼합함 |
| 장점 | random write와 유연성이 높음 | 매핑 테이블 메모리가 작음 | 성능과 메모리 사용의 균형을 잡기 쉬움 |
| 한계 | DRAM 메타데이터 비용이 큼 | 병합 비용과 write amplification이 커질 수 있음 | 정책이 복잡하고 튜닝 난도가 높음 |
| 적합 환경 | 고성능 엔터프라이즈 SSD | 저가형 단순 장치 | 범용 SSD |

> 요약: 페이지 매핑은 성능, 블록 매핑은 메모리 절감, 하이브리드 매핑은 균형에 초점이 있음.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Address Mapping Table | LBA와 PBA 관계를 저장해 논리 주소 접근을 실제 NAND 위치로 변환함 |
| Garbage Collector | 무효 page를 정리해 free block을 확보하고 배경 쓰기 부하를 조절함 |
| Wear Leveling Engine | 특정 block에 쓰기가 몰리지 않게 분산시켜 SSD 수명을 늘림 |
| Metadata Protection and Buffer | DRAM 캐시·저널링·power loss protection을 활용해 매핑 정보를 안전하게 유지함 |

```text
+-------------+     +------------------+     +------------------+
| Host LBA    | --> | FTL Mapping      | --> | NAND Blocks      |
+-------------+     +------------------+     +------------------+
                         |         |
                         v         v
                    +--------+ +--------+
                    | GC     | | WL     |
                    +--------+ +--------+
```

> 요약: FTL은 LBA-PBA 매핑, GC, wear leveling, 메타데이터 보호로 NAND 제약을 숨김.

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
| 쓰기 요청 수신   | --> | 새 page 할당    | --> | 매핑 테이블 갱신   | --> | 기존 page 무효화  | --> | 배경 GC 수행    |
+-------------+     +-------------+     +-------------+     +-------------+     +-------------+
```

1. **쓰기 요청 수신**: 호스트가 특정 LBA에 데이터를 기록하려고 함
2. **새 page 할당**: FTL이 비어 있는 물리 page를 새로 선택함
3. **매핑 테이블 갱신**: LBA가 새 PBA를 가리키도록 바꿈
4. **기존 page 무효화**: 이전 위치 데이터는 stale 상태로 남김
5. **배경 GC 수행**: 무효 page가 많은 block을 정리해 free space를 회복함

> 요약: FTL은 새 page에 쓰고 매핑을 갱신한 뒤 stale page를 GC로 정리함.

## Ⅵ. 실무 적용 및 유의점

1. GC와 병합 작업이 많아지면 write amplification이 커지므로 over-provisioning과 TRIM을 활용하고 write amplification factor, free block ratio로 확인함
2. 배경 정리 작업이 사용자 I/O와 겹치면 tail latency가 악화되므로 idle-time GC와 QoS-aware scheduling을 적용하고 p99 latency, steady-state IOPS로 확인함
3. 전원 장애 시 매핑 메타데이터가 손상되면 namespace 가시성이 깨질 수 있으므로 PLP와 metadata journaling을 적용하고 metadata recovery time, unsafe shutdown loss rate로 확인함

## Ⅶ. 결론

FTL은 SSD 내부 번역기를 넘어 성능, 수명, 무결성을 함께 조정하는 제어 계층이며, SSD 판단은 NAND 종류보다 FTL 정책 품질에 좌우됨.

## 작성 근거(검토용)

- FTL은 주소 변환뿐 아니라 out-of-place update, GC, wear leveling, 메타데이터 보호로 설명함
- 모호한 표현은 write amplification factor, p99 latency, metadata recovery time으로 구체화함
- 결론은 NAND 종류보다 FTL 정책 품질로 정리함
