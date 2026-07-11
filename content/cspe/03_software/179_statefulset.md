---
title: "StatefulSet (StatefulSet)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 179
extra:
  question_no: "179"
  exam_status: "기출"
  exam_history: "133회"
---

## 미리 알고가기

- StatefulSet은 Pod마다 고정 ordinal·네트워크 이름·스토리지 관계를 유지하는 워크로드 객체임
- ordinal은 `이름-0`, `이름-1`처럼 Pod의 순서와 식별자를 나타내는 번호임
- Headless Service는 ClusterIP 없이 StatefulSet Pod별 DNS 레코드를 제공함
- volumeClaimTemplates는 각 ordinal에 대응하는 PVC를 생성해 Pod 교체 후에도 다시 연결함
- OrderedReady는 낮은 ordinal부터 생성하고 앞 Pod가 Ready가 된 뒤 다음 Pod를 생성함
- 기본 동작에서는 StatefulSet이나 Pod를 삭제해도 연결된 PVC가 자동 삭제되지 않음
- UpdateStrategy partition은 지정 ordinal 미만의 Pod를 현재 버전으로 유지함

## 작성 근거(검토용)

- StatefulSet의 핵심은 상태 보유 자체보다 네트워크·스토리지 식별자의 지속성이므로 이를 중심에 둠
- Deployment와 식별·네트워크 이름·스토리지·생성 순서·갱신·적합 조건을 비교함
- 제목부터 결론까지 5회 전수 검수하여 Pod 교체와 PVC 보존의 관계를 확인함

## Ⅰ. 개요

- **정의/개념**: StatefulSet은 Pod별 고정 ordinal·DNS·PVC와 순서 있는 생성·갱신·축소를 관리하는 워크로드 제어기임
- **배경/필요성**: 복제본마다 식별자와 데이터를 유지해야 하는 분산 시스템을 운영하기 위해 지속 네트워크·스토리지 관계가 필요함

## Ⅱ. 특징

- Pod 이름과 Headless Service DNS가 ordinal에 따라 재생성 후에도 동일하게 유지됨
- volumeClaimTemplates가 Pod별 PVC를 만들고 같은 ordinal의 대체 Pod에 다시 연결함
- OrderedReady 정책은 생성·확장 시 낮은 ordinal의 Ready 상태를 다음 생성 조건으로 사용함
- RollingUpdate는 높은 ordinal부터 Pod를 교체하며 partition으로 갱신 범위를 나눌 수 있음

## Ⅲ. StatefulSet과 Deployment 비교

| 판단 기준 | StatefulSet | Deployment |
|:---|:---|:---|
| 복제본 식별 | ordinal 기반의 고정 이름 | 상호 교환 가능한 임의 이름 |
| 네트워크 이름 | Headless Service로 Pod별 DNS 유지 | Service가 복제본 집합을 하나의 주소로 제공 |
| 스토리지 관계 | Pod별 PVC를 같은 ordinal에 재연결 | 복제본별 고정 PVC 관계를 제공하지 않음 |
| 생성·축소 순서 | OrderedReady에서 순서 보장 | 복제본 간 생성·삭제 순서에 의존하지 않음 |
| 롤링 갱신 | 높은 ordinal부터 순서대로 교체 | 가용·초과 복제본 비율로 병렬 교체 |
| 적합 조건 | 고정 ID·Pod별 데이터·순서가 필요 | 복제본이 상호 교환 가능한 무상태 서비스 |

> 요약: StatefulSet은 복제본별 지속 식별자와 순서를 제공하고 Deployment는 교환 가능한 복제본을 관리함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| StatefulSet Controller | 원하는 복제본과 ordinal별 Pod·PVC 상태를 조정함 |
| Headless Service | 각 Pod의 고정 DNS 이름과 Endpoint를 제공함 |
| Pod ordinal | 생성·갱신·축소 순서와 네트워크·스토리지 ID를 연결함 |
| volumeClaimTemplates | ordinal마다 PVC를 생성하고 Pod 교체 후 재사용함 |
| PV·StorageClass | Pod별 데이터를 영속 볼륨에 저장하고 동적으로 제공함 |
| UpdateStrategy·Partition | 순차 교체 방식과 갱신 대상 ordinal 범위를 정함 |

```text
Headless Service -> app-0, app-1, app-2
                       |      |      |
                     pvc-0  pvc-1  pvc-2
```

> 요약: 같은 ordinal의 DNS 이름·Pod·PVC가 하나의 지속 식별 관계를 이룸.

## Ⅴ. 생성·갱신 흐름

```text
app-0·PVC 생성 -> app-0 Ready -> app-1·PVC 생성 -> 전체 Ready -> 높은 ordinal부터 갱신
```

1. **첫 복제본 생성**: Controller가 `app-0`과 대응 PVC를 만들고 볼륨을 연결함
2. **준비 상태 확인**: `app-0`이 Ready가 될 때까지 다음 ordinal 생성을 대기함
3. **순차 확장**: 같은 방식으로 높은 ordinal의 Pod와 PVC를 차례로 생성함
4. **순차 갱신**: RollingUpdate에서 높은 ordinal부터 새 명세로 교체하고 Ready를 확인함
5. **축소·재생성**: 높은 ordinal부터 제거하며 다시 만들 때 기존 PVC를 같은 ordinal에 연결함

> 요약: 앞 ordinal의 Ready 상태가 다음 생성 조건이며 같은 ordinal은 기존 네트워크·스토리지 ID를 재사용함.

## Ⅵ. 실무 사례

1. 분산 DB 복제본은 ordinal별 DNS·PVC를 유지하고 재가입시간·볼륨 재연결 오류를 확인함
2. 메시지 브로커는 UpdateStrategy partition을 적용하고 Ready 전환 시간·미갱신 Pod 수를 확인함

## Ⅶ. 결론

- StatefulSet은 복제본별 지속 ID·스토리지와 순차 변경이 필요한 워크로드에 적용해야 함
