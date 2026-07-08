---
title: "RAID 컨트롤러·JBOD (RAID Controller JBOD)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 108
extra:
  question_no: "108"
  exam_status: "미출제"
---

## 미리 알고가기

- RAID 컨트롤러는 여러 디스크를 논리 볼륨으로 묶어 보호와 캐시 기능을 제공함
- JBOD는 디스크를 개별 장치로 노출해 상위 소프트웨어가 직접 관리하게 함
- 핵심 차이는 데이터 보호 책임을 어느 계층이 지는가임

## Ⅰ. 개요

- **정의/개념**: RAID 컨트롤러는 디스크 집합을 논리 RAID 볼륨으로 구성해 미러링과 패리티와 캐시와 재구성을 하드웨어에서 처리하는 장치이고, JBOD는 디스크를 개별 장치로 그대로 노출하는 구성 방식임
- **배경/필요성**: 단일 서버는 단순한 보호와 부팅 구성이 필요할 수 있지만 분산 스토리지는 상위 소프트웨어가 복제와 장애 배치를 직접 통제해야 하므로, 제어 책임 위치를 구분해 선택해야 함

## Ⅱ. 특징

- RAID 컨트롤러는 OS 관점에서 단순한 볼륨 제공과 캐시 가속이 가능함
- JBOD는 디스크 가시성이 높아 SDS와 분산 스토리지에 유리함
- RAID는 컨트롤러 장애와 메타데이터 종속 위험이 있고 JBOD는 운영 소프트웨어 책임이 커짐
- 선택 기준은 성능보다 복구 절차와 장애 도메인과 운영 자동화 수준임

## Ⅲ. 종류 및 비교

| 판단 기준 | RAID 컨트롤러 | JBOD |
|:---|:---|:---|
| 디스크 노출 | 논리 RAID 볼륨 | 개별 물리 디스크 |
| 보호 기능 | 미러, 패리티, rebuild, 캐시 제공 | 상위 소프트웨어가 직접 수행 |
| 장점 | 단순 운영과 부트 볼륨 구성 용이 | 투명성, 유연성, 벤더 종속 완화 |
| 주의점 | 컨트롤러 장애와 메타데이터 의존 | 복제와 장애 처리 체계 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| RAID Engine | stripe와 mirror와 parity 계산을 수행해 디스크 집합을 하나의 논리 저장장치처럼 보이게 함 |
| Cache and Power Protection | write-back 성능을 높이되 정전 시 데이터 무결성을 지키는 핵심 보호 장치가 됨 |
| HBA or JBOD Path | 디스크를 가공 없이 노출해 상위 소프트웨어가 배치와 복제를 직접 결정하게 함 |
| Upper Storage Software | JBOD 환경에서 복제와 scrub과 재배치를 담당해 실제 보호 수준을 결정함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 디스크 인식    | --> | 구성 방식 선택 | --> | 볼륨/디스크 노출 | --> | 장애 복구      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **디스크 인식**: 컨트롤러나 HBA가 연결된 디스크 상태를 파악함
2. **구성 방식 선택**: RAID 레벨 또는 JBOD 노출 정책을 정함
3. **볼륨 또는 디스크 노출**: RAID는 논리 볼륨을, JBOD는 개별 디스크를 OS에 제공함
4. **장애 복구**: rebuild나 재복제나 spare 정책으로 장애 후 복구를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: RAID 컨트롤러 장애와 전용 메타데이터 의존성이 겹치면 교체 복구가 지연될 수 있음
   - 해결방안: dual controller와 metadata export 절차를 준비하고 controller failover success rate와 recovery time으로 검증함
2. 문제: write-back cache 보호가 부족하면 정전 시 패리티 불일치와 데이터 손실이 발생할 수 있음
   - 해결방안: BBU 또는 supercap 상태 감시를 운영하고 cache protection status와 consistency check pass rate로 검증함
3. 문제: JBOD 환경에서 상위 소프트웨어 장애 처리 정책이 약하면 디스크 장애가 서비스 손실로 바로 이어질 수 있음
   - 해결방안: 자동 재복제와 failure domain 정책을 적용하고 degraded recovery time과 replica health rate로 검증함

## Ⅶ. 적용 사례

- 단일 서버 부트 볼륨에서는 RAID 1 구성을 사용하고 확인 지표는 rebuild time과 cache protection status임
- 분산 스토리지 노드에서는 JBOD를 사용해 디스크를 직접 노출하고 확인 지표는 degraded recovery time과 disk visibility rate임
- 장비 교체 훈련에서는 컨트롤러 교체와 메타데이터 복구 절차를 시험하고 확인 지표는 controller failover success rate와 recovery time임

## Ⅷ. 결론

RAID 컨트롤러와 JBOD의 선택은 디스크를 어떻게 묶느냐보다 데이터 보호와 복구 책임을 하드웨어와 소프트웨어 중 어디에 둘지 정하는 문제임.
