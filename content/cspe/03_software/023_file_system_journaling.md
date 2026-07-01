---
title: "파일 시스템 저널링 (File System Journaling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 23
---

# 📖 【암기용】 개념 완전 이해

> 목적: 파일 시스템 저널링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 파일 시스템 변경 내용을 실제 반영 전에 로그로 기록해 장애 후 일관성을 복구하는 기법
- **왜 필요한가**: 파일 쓰기 중 전원이 꺼지면 디렉터리, inode, 데이터 블록 중 일부만 반영될 수 있다. 저널링은 완료 여부를 로그로 남겨 손상 범위를 줄인다.
- **핵심 직관**: 은행 장부에 거래 예정 내역을 먼저 적고, 실제 계좌 반영 후 완료 표시를 찍는 방식이다.

## 깊이 이해
- **배경·문제의식**: 대용량 디스크에서 전통적 fsck는 전체 메타데이터를 검사해 수십 분이 걸릴 수 있다. 저널링은 변경 단위만 재실행 또는 취소해 부팅 복구 시간을 줄인다.
- **작동 원리**: 트랜잭션 시작 후 변경 메타데이터 또는 데이터를 journal 영역에 기록하고 commit record를 쓴다. 장애 후 mount 시 commit된 트랜잭션은 replay하고 미완료 트랜잭션은 폐기한다.
- **비유**: 택배 송장을 먼저 등록하고 물건 이동을 처리한 뒤 배송 완료를 찍는다. 중간에 중단되면 송장을 보고 어느 단계까지 처리했는지 판단한다.
- **구체 예시**: ext4 ordered mode는 데이터 블록을 먼저 디스크에 쓰고 메타데이터를 저널에 기록한다. data mode는 데이터까지 저널에 써 복구 일관성은 높지만 쓰기 증폭이 커진다.
- **흔한 오해·주의점**: 저널링은 백업이 아니다. 삭제나 잘못된 덮어쓰기를 되돌리는 기능이 아니라 장애 순간 파일 시스템 구조 일관성을 보장하는 기능이다.

## 연결 개념
- WAL(Write-Ahead Logging) — DB 트랜잭션 로그와 유사한 장애 복구 원리
- fsck — 저널링이 없거나 손상 범위가 클 때 사용하는 검사 도구
- copy-on-write — 저널 대신 새 블록에 쓰고 포인터를 교체하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 저널링은 복구 기법 이름이 아니라 writeback·ordered·data mode의 일관성 수준과 지연시간 트레이드오프를 구분해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 파일 시스템 저널링은 변경 내용을 journal에 선기록한 뒤 실제 영역에 반영하여 장애 후 replay/rollback을 가능하게 하는 기법이다.
> 2. **가치**: 전체 디스크 fsck 대신 커밋된 트랜잭션만 복구해 부팅 복구 시간을 분 단위에서 초 단위로 줄인다.
> 3. **판단 포인트**: writeback, ordered, data mode는 데이터 일관성, 쓰기 지연, 쓰기 증폭이 서로 다르다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 장애 일관성 이해 확인 | transaction, journal, commit, replay | 저널을 백업·버전관리로 설명 |
| 모드별 차이 판단 확인 | writeback/ordered/data와 지연시간·일관성 비교 | ordered mode의 데이터 선쓰기 누락 |
| 실무 운영 관점 확인 | fsck 시간, fsync latency, write amplification | SSD 수명·지연시간 영향 미제시 |

> 요약: 이 문제는 저널링 동작 순서와 모드별 트레이드오프를 장애 복구 지표로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

파일 시스템 저널링은 변경 내용을 로그에 기록해 장애 후 일관성을 회복하는 기법이다. 전원 장애 중 파일 쓰기가 중단되면 메타데이터와 데이터 반영 순서가 어긋난다. 저널링은 commit 여부를 기준으로 replay 또는 폐기해 fsck 범위를 줄인다.

---

## Ⅱ. 구조 및 구성요소

```text
Application Write -> Page Cache -> Journal Area -> Commit Record -> Home Location
  / Metadata Journal: inode, bitmap, directory
  / Data Journal: file data included
  / Recovery: replay committed transaction
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Journal Area | 변경 트랜잭션 임시 기록 | 순차 쓰기 중심 |
| Transaction | 여러 메타데이터 변경의 원자 단위 | begin, update, commit |
| Commit Record | 완료 여부 판단 기준 | 장애 후 replay 조건 |
| Checkpoint | 저널 내용을 실제 위치에 반영 | journal 공간 회수 |
| Recovery Logic | mount 시 journal 검사 | 미완료 트랜잭션 폐기 |

> 요약: 저널링은 journal area, transaction, commit record, checkpoint, recovery logic으로 변경 일관성을 보장한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> 트랜잭션 생성 -> 저널 기록 -> commit 기록
  -> 실제 위치 반영 -> 장애 발생 시 journal replay / discard
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 파일 쓰기 요청을 트랜잭션으로 묶음 | transaction size, dirty page |
| 2 | 변경 메타데이터 또는 데이터를 journal에 기록 | sequential write latency |
| 3 | commit record를 기록해 완료 표시 | fsync latency |
| 4 | checkpoint로 home location에 반영 | checkpoint interval |
| 5 | 장애 후 commit 기준으로 replay 또는 폐기 | recovery time, fsck error |

> 요약: 저널링은 선기록, 커밋, 체크포인트, 복구 순서로 동작하며 commit record가 장애 복구 기준이다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| writeback | 데이터 순서 보장 약함 | 메타데이터만 저널 | 지연시간 우선, stale data 위험 |
| ordered | 데이터 선쓰기 후 메타데이터 저널 | ext4 기본 모드 | 균형형, 일반 서버 |
| data | 데이터와 메타데이터 모두 저널 | 데이터 일관성 우선 | 쓰기 2회, write amplification 증가 |
| fsck | 전체 구조 검사 | journal replay | 대용량 볼륨 복구 시간 단축 |

> 요약: ordered mode는 일반 서버의 기본 선택이며, data mode는 일관성 요구가 큰 소규모 중요 파일에 제한 적용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 전체 fsck | journal replay | TB급 볼륨 복구 시간 요구 |
| 비용/성능 | 즉시 home write | journal+checkpoint | fsync p95 50ms 이하 여부 |
| 운영/위험 | 데이터 손상 후 수동 복구 | commit 기반 자동 복구 | RTO 10분 이하 시스템 |

> 요약: 저널링은 RTO와 fsync 지연을 함께 비교해 모드와 체크포인트 주기를 정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 쓰기 지연 증가 | journal 기록 후 실제 반영 | ordered mode, journal size 조정 | fsync p95 50ms 이하 |
| SSD 쓰기 증폭 | data mode에서 중복 기록 | data mode 범위 제한, NVMe endurance 확인 | TBW 사용률 월 2% 이하 |
| journal 손상 | 저장장치 오류·캐시 flush 실패 | barriers, UPS, RAID write cache 보호 | journal error 0건 |

> 요약: 저널링 리스크는 지연시간과 쓰기 증폭이므로 fsync, TBW, journal error로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 복구/RTO | mount recovery 60초 이하 | 장애 주입 테스트 |
| 성능/지연 | fsync p95 50ms 이하, iowait 10% 이하 | fio, iostat |
| 무결성 | fsck error 0건, journal replay 성공률 100% | boot log, smartctl |

> 요약: 저널링 도입 효과는 복구 시간, fsync 지연, 무결성 오류 지표로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 일반 Linux 서버는 ext4 ordered mode를 기본값으로 두고 commit interval 5초, barrier 활성화 상태를 점검한다.
2. DB 파일은 DB 자체 WAL과 파일 시스템 저널 중복을 고려해 데이터 파일과 WAL 파일을 별도 볼륨으로 분리한다.
3. 장애 주입 테스트로 전원 차단 후 mount recovery 60초 이하, fsck error 0건 기준을 검증한다.

**결론 (2줄):**
- 기술사 판단: 일반 서버는 ordered mode, 메타데이터 일관성만 필요한 로그성 워크로드는 writeback, 데이터 일관성 우선 소규모 영역은 data mode를 선택한다.
- 향후 방향: 저널링은 COW, snapshot, checksum과 결합해 복구 시간과 무결성 검증을 동시에 제공하는 구조로 발전한다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "저널링을 설명하시오" | transaction, commit, replay 흐름 | writeback·ordered·data 특징 |
| 요구사항 명시형 | "비교하시오", "운영 방안을 제시하시오" | 모드별 지연·복구 흐름 | fsync, RTO, SSD 수명 기준 |

> 요약: 설명형은 복구 원리를, 비교·운영형은 저널 모드 선택과 지표 기반 통제를 중심으로 작성한다.
