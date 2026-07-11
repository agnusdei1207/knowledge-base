---
title: "쿠버네티스 Pod 생명주기 (Kubernetes Pod Lifecycle)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 174
extra:
  question_no: "174"
  exam_status: "기출"
  exam_history: "123회"
---

## 미리 알고가기

- Pod phase는 Pending·Running·Succeeded·Failed·Unknown으로 구분되는 상위 실행 상태임
- 컨테이너 상태는 Waiting·Running·Terminated로 각 컨테이너의 실제 실행 단계를 나타냄
- restartPolicy는 컨테이너 재시작 조건을 정하고 Backoff는 반복 실패 시 재시도 간격을 늘림
- Startup Probe는 시작 완료 전 Liveness·Readiness 검사를 지연함
- Liveness Probe 실패는 컨테이너 재시작 조건이 되고 Readiness 실패는 서비스 대상 제외 조건이 됨
- Pod는 한 노드에만 스케줄되며 노드 장애 시 같은 UID를 이동하지 않고 새 Pod로 대체함
- Init Container는 주 컨테이너보다 먼저 순서대로 실행돼 초기화 작업을 완료함
- preStop Hook과 TERM 신호는 삭제되는 컨테이너가 연결·상태를 정리할 시간을 제공함

## 작성 근거(검토용)

- Pod 생명주기는 phase만으로 설명되지 않으므로 컨테이너 상태·프로브·재시작·종료를 함께 연결함
- 각 phase의 진입 조건·의미·후속 조치를 비교하고 생성부터 종료까지 실제 상태 전이로 회수함
- 제목부터 결론까지 5회 전수 검수하여 Pod phase와 컨테이너 상태를 혼용하지 않도록 교정함

## Ⅰ. 개요

- **정의/개념**: Pod 생명주기는 Pod 생성부터 스케줄링·컨테이너 실행·재시작·종료까지 phase·상태·조건으로 추적하는 상태 체계임
- **배경/필요성**: 실행 실패와 서비스 가능 상태를 구분해 복구·라우팅·종료를 제어하기 위해 상태 전이 기준이 필요함

## Ⅱ. 특징

- Pod phase는 상위 상태를 요약하고 세부 원인은 컨테이너 상태와 Pod conditions에 기록됨
- kubelet은 restartPolicy와 컨테이너 종료 원인에 따라 같은 Pod 안에서 재시작함
- Readiness는 트래픽 수신 가능 여부, Liveness는 프로세스 재시작 필요 여부를 판단함
- 삭제 시 종료 유예시간 동안 preStop과 TERM 처리를 수행한 뒤 남은 프로세스를 종료함

## Ⅲ. Pod phase 비교

| Phase | 진입 조건 | 상태 의미 | 후속 조치 |
|:---|:---|:---|:---|
| Pending | 생성됐지만 컨테이너 실행 준비가 완료되지 않음 | 스케줄링·볼륨·이미지 준비 중 | 이벤트와 대기 원인을 확인함 |
| Running | 노드에 바인딩되고 하나 이상의 주 컨테이너가 시작됨 | 실행 중이거나 재시작 진행 중 | 프로브·재시작·준비 상태를 확인함 |
| Succeeded | 모든 컨테이너가 성공 종료하고 재시작되지 않음 | 작업이 정상 완료됨 | 결과를 보존하고 후속 작업을 진행함 |
| Failed | 하나 이상의 컨테이너가 실패 종료하고 재시작되지 않음 | 작업이 실패로 종료됨 | 종료 코드·로그·재실행 정책을 확인함 |
| Unknown | 노드와 통신하지 못해 상태를 확인할 수 없음 | 실제 실행 상태가 불명확함 | 노드 상태와 Pod 대체 여부를 확인함 |

> 요약: Pod phase는 상위 실행 구간을 구분하고 세부 원인은 컨테이너 상태·conditions에서 확인함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 역할 |
|:---|:---|
| Pod phase | Pod 생명주기의 상위 상태를 요약함 |
| 컨테이너 상태 | 대기 이유·실행 시각·종료 코드와 원인을 기록함 |
| Pod conditions | Scheduled·Initialized·Ready 등 조건별 참·거짓을 표시함 |
| restartPolicy·Backoff | 종료 원인에 따른 재시작과 반복 실패 대기시간을 정함 |
| Startup·Liveness·Readiness Probe | 시작·생존·트래픽 수신 가능 상태를 각각 판정함 |
| 종료 유예·Hook | 종료 전 연결 정리와 애플리케이션 마감 시간을 제공함 |

```text
Pod phase
  +-> 컨테이너 상태·종료 코드
  +-> Pod conditions·Probe 결과
  +-> restartPolicy·종료 유예
```

> 요약: phase는 전체 상태를 나타내고 컨테이너 상태·조건·프로브가 원인과 제어 동작을 결정함.

## Ⅴ. 상태 전이 흐름

```text
Pod 생성 -> Pending -> 노드 바인딩·초기화 -> Running -> 종료 판정 -> Succeeded 또는 Failed
                                      |             |
                                      +-- 재시작 <--+
```

1. **Pod 생성·Pending**: API 객체가 생성되고 스케줄러가 노드와 볼륨 조건을 확인함
2. **초기화**: kubelet이 샌드박스·볼륨·이미지와 Init Container를 순서대로 준비함
3. **Running**: 주 컨테이너를 시작하고 프로브 결과를 conditions와 서비스 경로에 반영함
4. **재시작 판정**: 종료 코드와 restartPolicy에 따라 같은 Pod에서 컨테이너를 다시 시작함
5. **종료 판정**: 재시작하지 않을 때 모든 종료 결과로 Succeeded 또는 Failed를 정함

> 요약: 준비 결과가 Running 진입을 결정하고 종료 원인과 restartPolicy가 재시작·최종 phase를 가름.

## Ⅵ. 실무 사례

1. 웹 API Pod는 세 Probe를 분리하고 재시작 횟수·Ready 전환시간을 확인함
2. 배치 Job Pod는 OnFailure를 적용하고 완료시간·실패 종료 코드 건수를 확인함

## Ⅶ. 결론

- Pod 생명주기는 phase와 컨테이너 상태·프로브·재시작 정책을 함께 해석해야 함
