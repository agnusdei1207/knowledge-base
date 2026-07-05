---
title: 고성능 컴퓨팅 HPC 아키텍처 (HPC Architecture)
date: 2026-07-05
tags: [cspe-hardware]
weight: 69
---

## Ⅰ. 개요
- 정의: 대규모 과학 기술 계산을 위해 다수의 컴퓨터 자원을 결합한 고성능 시스템
- 배경: 기상 예측, 신약 개발 등 거대 데이터 처리를 위한 병렬 연산 수요 증가
- 출제 의도: 클러스터 구조, 병렬 처리 알고리즘 및 인터커넥트 기술 이해 측정

## Ⅱ. 구성요소
- ASCII 구조도
  [ Master Node ] <--- 관리 ---> [ Compute Cluster ]
        |                              |
  [ Interconnect ] <--- RDMA --------> [ Storage System ]
  (Infiniband)                        (Parallel FS)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Compute Node | 실제 연산을 수행하는 CPU/GPU 탑재 서버 | 작업 숙련공 |
| Interconnect | 노드 간 저지연/고속 데이터 전송 네트워크 | 초고속 통로 |
| Parallel FS | 여러 노드가 동시에 접근 가능한 파일 시스템 | 공용 창고 |

- > 요약: 수천 개의 노드가 하나의 시스템처럼 동작하는 단일 시스템 이미지 구현

## Ⅲ. 절차
- ASCII 흐름도
  [Job Submit] -> [Scheduler] -> [Resource Alloc] -> [Parallel Run]

1. 작업 제출: 사용자가 배치 스케줄러(Slurm 등)에 작업 요청
2. 스케줄링: 가용 자원을 확인하여 최적의 연산 노드 할당
3. 병렬 실행: MPI(Message Passing Interface) 등을 통해 노드 간 협업
4. 결과 수집: 연산 결과를 통합 저장소에 기록 및 사용자 통보

- > 요약: 분할 정복(Divide and Conquer) 기반의 대규모 병렬 처리 프로세스

## Ⅳ. 문제점
- 통신 병목: 노드 수 증가 시 네트워크 지연으로 인한 효율성 저하(Scalability)
- 전력 및 냉각: 엄청난 전력 소모와 그에 따른 발열 관리 비용 증대

## Ⅴ. 개선방안
- 저지연 네트워크: Infiniband, RoCE 도입으로 통신 오버헤드 최소화
- 가속기 활용: GPU, NPU 도입을 통한 전력 대비 성능 극대화(Green HPC)

## Ⅵ. 전망
- 로드맵: Exascale(10^18) 시대 진입에 따른 하이브리드 아키텍처 보편화
- CSF: 하드웨어 성능을 100% 활용하기 위한 병렬 프로그래밍 소프트웨어 최적화
