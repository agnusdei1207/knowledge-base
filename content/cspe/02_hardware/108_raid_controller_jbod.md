---
title: "RAID 컨트롤러·JBOD (RAID Controller JBOD)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 108
---

# RAID 컨트롤러·JBOD (RAID Controller JBOD)

## 미리 알고가기

- RAID(Redundant Array of Independent Disks) 컨트롤러: 여러 디스크를 RAID 논리 볼륨으로 구성하고 캐시·재구성·오류 처리를 담당하는 장치임
- JBOD(Just a Bunch Of Disks): 디스크를 RAID로 묶지 않고 개별 디스크로 노출하는 방식임
- HBA(Host Bus Adapter): 스토리지 장치를 호스트에 연결하고 주로 패스스루 역할을 수행하는 어댑터임
- SDS(Software-Defined Storage): 스토리지 보호·배치·운영 기능을 소프트웨어로 구현하는 방식임
- Rebuild: 장애 디스크 교체 후 패리티나 미러를 이용해 데이터를 복원하는 과정임
- OS(Operating System): 스토리지 장치를 인식하고 파일시스템·드라이버를 통해 사용하는 운영체제임

## 1. 개요

- **정의/개념**: RAID 컨트롤러는 다수 디스크를 논리 RAID 볼륨으로 묶어 성능·가용성·캐시 기능을 제공하는 제어 장치이고, JBOD는 디스크를 개별 장치로 노출해 상위 소프트웨어가 직접 관리하도록 하는 구성임.
- **배경/필요성**: 서버 스토리지는 디스크 장애, 쓰기 캐시, 재구성, 성능 균형을 관리해야 함. 하드웨어 RAID는 컨트롤러가 이를 숨겨 단순화하고, JBOD는 소프트웨어 정의 스토리지나 분산 파일시스템이 디스크를 직접 제어할 수 있게 함.
- **비유**: RAID 컨트롤러는 여러 창고를 하나의 대형 창고처럼 관리하는 관리자이고, JBOD는 창고마다 개별 주소를 공개해 중앙 시스템이 직접 배치하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스토리지 제어 책임 위치 판단 | hardware RAID, cache, rebuild, HBA/JBOD, SDS | JBOD를 RAID 0과 동일시 |

> 요약: RAID 컨트롤러와 JBOD의 차이는 디스크 보호와 배치 결정을 컨트롤러가 숨기는지, 상위 소프트웨어에 맡기는지임.

## 2. 특징 및 비교

| 판단 기준 | RAID 컨트롤러 | JBOD/HBA |
|:---|:---|:---|
| 디스크 노출 | RAID 볼륨 하나 또는 여러 LUN(Logical Unit Number)으로 노출 | 개별 물리 디스크로 노출 |
| 보호 기능 | 미러, 패리티, 캐시, rebuild를 컨트롤러가 처리 | 분산 파일시스템과 SDS가 처리 |
| 장점 | OS 단순화, boot volume, write-back cache 활용 | 투명성, 유연한 배치, 벤더 종속 감소 |
| 위험 | 컨트롤러 장애와 proprietary metadata 의존 | 소프트웨어 운영 역량과 디스크 장애 처리 필요 |

> 요약: RAID 컨트롤러는 단순성과 하드웨어 보호, JBOD는 투명성과 소프트웨어 제어를 선택하는 구조임.

- **적용 조건**: 데이터 보호 책임을 컨트롤러와 상위 소프트웨어 중 어디에 둘지 먼저 정해야 함
- **선택 지표**: rebuild time, cache protection, disk visibility를 함께 확인해야 함
- **운영 관점**: 장애 교체 절차와 metadata 호환성이 복구 가능성을 좌우함

## 3. 구성요소/구조

```text
+----------+      +----------------+      +----------+
| Host OS  | ---> | RAID Controller| ---> | Disk set |
+----------+      +----------------+      +----------+
       |                  |                    |
       v                  v                    v
+----------+      +----------------+      +----------+
| HBA mode | ---> | JBOD passthru  | ---> | Disk 0..n|
+----------+      +----------------+      +----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| RAID 엔진 | stripe, mirror, parity, rebuild 연산을 수행함 | 창고 배치 관리자 |
| 캐시·BBU(Battery Backup Unit) | 쓰기 성능과 정전 시 데이터 보호를 담당함 | 임시 보관함과 비상 전원 |
| HBA/JBOD 경로 | 디스크를 변환 없이 호스트에 개별 노출함 | 창고별 직접 출입문 |
| 상위 스토리지 소프트웨어 | 파일시스템이나 SDS가 복제, 패리티, 장애 처리를 담당함 | 중앙 운영 시스템 |

> 요약: RAID 컨트롤러 구성은 보호 기능을 하드웨어에 두고, JBOD 구성은 상위 소프트웨어에 둠.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Discover | ---> | Select   | ---> | Expose   | ---> | Recover  |
+----------+      +----------+      +----------+      +----------+
```

1. **디스크 탐색** — 컨트롤러나 HBA가 연결 디스크 상태, 용량, SMART(Self-Monitoring Analysis and Reporting Technology) 정보를 확인함
2. **구성 선택** — 업무 요구에 따라 RAID level, write cache, JBOD passthrough를 결정함
3. **볼륨·디스크 노출** — RAID는 논리 볼륨을, JBOD는 개별 디스크를 OS에 제공함
4. **장애 관리** — 디스크 장애, rebuild, scrub, spare, 교체 절차를 수행함

> 요약: 구성 선택 이후 RAID는 컨트롤러가, JBOD는 상위 소프트웨어가 장애와 배치를 주도함.

## 4. 문제점 및 개선방안

- **P1 컨트롤러 단일 장애점**: RAID metadata와 cache가 특정 컨트롤러에 의존하면 장애 시 복구가 어려울 수 있음
- **P1 대응**: dual controller, metadata export, 교체 절차, controller firmware 표준화를 적용함 (확인: controller failover test)
- **P2 쓰기 홀·캐시 위험**: write-back cache와 정전 보호가 맞지 않으면 패리티 불일치나 데이터 손실이 발생함
- **P2 대응**: BBU(Battery Backup Unit)/supercap 상태 감시, write-through fallback, patrol read와 consistency check를 운영함 (확인: cache protection status)
- **P3 JBOD 운영 부담**: 디스크가 그대로 노출되어 장애 감지, 복제, 재배치 정책을 소프트웨어가 정확히 수행해야 함
- **P3 대응**: SDS health check, disk inventory, 자동 재복제, failure domain 정책을 적용함 (확인: degraded recovery time)

> 요약: RAID/JBOD 위험은 데이터 보호 책임이 어느 계층에 있는지 불명확할 때 커지므로 컨트롤러와 소프트웨어 책임을 분리해야 함.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 단일 서버 부트 볼륨 | RAID 1 또는 RAID 10을 컨트롤러에서 구성하고 cache 보호와 spare 정책을 운영함 | rebuild time, cache protection status |
| 분산 스토리지 노드 | JBOD/HBA(Host Bus Adapter)로 디스크를 개별 노출하고 SDS(Software-Defined Storage)가 복제와 장애 배치를 수행함 | degraded recovery time, disk visibility |
| 장비 교체 복구 | controller metadata export와 firmware 표준화로 장애 컨트롤러 교체 절차를 검증함 | controller failover test, recovery success rate |

> 요약: 실무에서는 보호 책임을 하드웨어 RAID에 둘지 SDS에 둘지 정하고 복구 지표로 검증해야 함.

## 6. 결론

- **발전 방향**: NVMe(Non-Volatile Memory Express), erasure coding, SDS, disaggregated storage 확산으로 전통 하드웨어 RAID보다 소프트웨어 기반 데이터 보호가 확대됨
- **기술사적 판단**: 선택 기준은 RAID 성능 수치보다 장애 도메인, 복구 시간, 운영 자동화, 벤더 종속 위험이어야 함
- **기술사 제언**: 단일 서버 부트와 단순 업무는 RAID 컨트롤러, 분산 스토리지는 JBOD/HBA 중심으로 표준화하는 이원 전략이 적절함
