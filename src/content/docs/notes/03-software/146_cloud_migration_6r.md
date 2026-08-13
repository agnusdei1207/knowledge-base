---
sidebar:
  order: 146
  label: "146. 클라우드 마이그레이션 6R (Cloud Migration 6R)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 마이그레이션 6R (Cloud Migration 6R)"
date: "2026-08-14T01:36:00+09:00"
tags: ["notes-software"]
weight: 146
extra:
  question_no: "146"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "이전 방식 선택과 단계별 위험 통제가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Cloud Migration 6R Framework**: AWS가 정립한 기업 레거시 시스템의 클라우드 이관 및 현대화 6대 전략 (Rehost, Replatform, Refactor/Re-architect, Repurchase, Retain, Retire).
- **Rehost (Lift-and-Shift)**: 기존 레거시 앱과 OS를 코드 변경 0% 상태로 클라우드 가상머신(EC2)으로 그대로 뜬 떠옮기는 전략.
- **Replatform (Lift-Shift-and-Tweak)**: 앱 코드는 보존하되, DB나 미들웨어를 클라우드 관리형 서비스(RDS, ElastiCache)로 부분 교체하는 전략.
- **Refactor / Re-architect (Cloud-Native)**: 클라우드 네이티브 아키텍처(MSA, Serverless, Container)로 앱 코드를 전면 재개발 및 재설계하는 최고 난이도 전략.

</details>

- 정의/개념: 워크로드별 이전 방식을 분류하는 **Cloud Migration 6R**
- 배경/필요성: 일괄 재개발은 **비용•일정•전환 위험**을 과도하게 증가

#### 한줄 요약

- 워크로드별 업무 가치와 기술 제약을 평가하여 재호스팅·리팩터링·재구매·유지·폐기 중 적합한 이전 전략을 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Repurchase, Retain, Retire**: SW 완제품(SaaS) 교체(Repurchase), 당장 이관 없이 레거시 보존(Retain), 무의미 시스템 파기(Retire).

</details>

- **Rehost**는 변경을 줄여 이전하나 기술 부채 잔존
- **Replatform**은 일부 계층을 관리형 서비스로 교체
- **Refactor**는 Cloud-Native 구조로 재설계
- **Repurchase•Retain•Retire**로 교체•유지•폐기

#### 한줄 요약

- 급히 비워야 할 짐은 그대로 옮기고 오래 쓸 설비는 고쳐 옮기되, 전원선으로 연결된 장비처럼 함께 움직여야 할 시스템은 같은 웨이브로 묶는다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Migration Wave**: 의존성이 얽힌 시스템들을 그룹핑(Wave 1, Wave 2)하여 순차적으로 마이그레이션을 가동하는 스케줄링 기법.

</details>

| 구성요소 | 책임 |
|---|---|
| Rehost | **구조 변경 최소화**와 신속 이전 |
| Replatform | 애플리케이션을 유지하며 **플랫폼 개선** |
| Refactor | 장기 가치에 맞춘 **구조 재설계** |
| Repurchase | 기존 기능을 **SaaS로 대체** |
| Retain | 규제•의존성 때문에 **현 환경 유지** |
| Retire | 사용 가치가 없는 **자산 종료** |

#### 한줄 요약

- 자산 목록과 연결 지도를 평가표에 겹쳐 본 뒤, 각 시스템의 처리 방법과 함께 움직일 웨이브를 정하고 실패하면 돌아올 조건까지 붙인다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Migration Assessment Tree**: 시스템 가치, 기술 노후도, 데이터 주권을 측정하여 6R 중 최적 경로로 분류하는 의사결정 로직.

</details>

```text
[워크로드 평가]
 ├─ 미사용 ─────────────── [Retire]
 ├─ 이전 제약 큼 ───────── [Retain]
 ├─ SaaS 대체 적합 ─────── [Repurchase]
 ├─ 기한 우선 ──────────── [Rehost]
 ├─ 일부 관리형 전환 ───── [Replatform]
 └─ 장기 가치•변경 여력 ── [Refactor]
```

### 동작 원리

- **미사용**: 업무 가치와 실제 사용량을 확인해 Retire
- **이전 제약 큼**: 규제•장비•의존성을 확인해 Retain
- **SaaS 대체 적합**: 기능•전환 비용을 비교해 Repurchase
- **기한 우선**: 변경 여력이 작으면 Rehost
- **현대화 범위**: 부분 개선은 Replatform, 재설계는 Refactor

#### 한줄 요약

- 연결된 장비를 한 차량에 묶고 도착지에서 작동과 자료를 확인한 뒤, 검사표를 통과하면 사용처를 바꾸고 실패하면 원래 장소로 돌린다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Modernization Level**: Rehost (0% 현대화) $\rightarrow$ Replatform (30% 현대화) $\rightarrow$ Refactor (100% Cloud-Native 현대화).

</details>

| 비교 항목 | Rehost (Lift-and-Shift) | Replatform (Lift-and-Tweak) | Refactor (Cloud-Native) |
|:---|:---|:---|:---|
| **이관 속도** | 변경이 적어 빠름 | 부분 변경으로 중간 | 재설계로 장기화 가능 |
| **코드 변경 범위**| 최소 | 플랫폼 연동부 중심 | 구조 전반 변경 |
| **Cloud-Native 혜택**| 제한적 | 관리형 계층 활용 | **탄력성•복원력** 최적화 |
| **초기 이관 비용**| 상대적으로 낮음 | 중간 | 개발 범위에 따라 높음 |

#### 한줄 요약

- 이사 기한이 급하면 그대로 옮기고 장기 가치가 크면 고쳐 옮기며, 규제 때문에 못 옮기면 남기고 쓰지 않는 시스템은 연결 관계를 확인한 뒤 종료한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Cutover Strategy (전환 전략)**: 레거시에서 클라우드로 최종 스위칭 시 빅뱅(Big Bang) 전환과 단계적(Phased Rollout) 전환 선택.

</details>

| 3대 마이그레이션 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. All-Refactor Fallacy** | 모든 서비스를 다 MSA 재개발하려다 예산 오버 | **Rehost로 일단 빠르게 옮긴 후 차근차근 Refactor**|
| **2. Unknown Dependency** | 알려지지 않은 서버 간 조용한 의존성으로 다운 | **AWS Application Discovery Service로 의존성 시각화** |
| **3. Data Migration Sync** | 이관 도중 발생한 DB 델타 데이터 유실 | **AWS DMS (Data Migration Service) CDC 실시간 동기화**|

> 사례: **삼성전자 / KB국민은행 AWS 마이그레이션 6R 프레임워크 적용 사례**

#### 한줄 요약

- 자산 인벤토리와 의존성 맵을 함께 확인하고 연관 워크로드를 같은 웨이브로 묶은 뒤, 성공 기준을 통과한 시스템만 원 환경에서 해제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **6R Framework 수립 기준(6R Migration Standards)**: Business Value, Effort, Rehost/Replatform/Refactor 분류 및 Wave 스케줄링에 의거한 체계.

</details>

- 기한 우선은 **Rehost**, 장기 가치 우선은 Replatform•Refactor 선택

#### 한줄 요약

- 이사 기한과 장기 사용 가치를 함께 보고 짐마다 옮길 방법을 고른 뒤, 서로 연결된 장비는 같은 웨이브로 묶는다.
