---
title: 뉴로모픽 컴퓨팅 (Neuromorphic Computing)
date: 2026-07-05
tags: [cspe-hardware]
weight: 81
---

## Ⅰ. 개요
- 정의: 인간 뇌의 뉴런과 시냅스 구조를 모방하여 초저전력으로 연산을 수행하는 하드웨어
- 배경: 폰 노이만 아키텍처의 병목(Memory Wall) 해결 및 에너지 효율적 AI 처리 필요
- 출제 의도: SNN(Spiking Neural Network) 원리 및 비폰노이만 구조의 특성 이해

## Ⅱ. 구성요소
- ASCII 구조도
  [ Neuron ] <--- [ Synapse (Weight) ] <--- [ Neuron ]
      |                 |                    |
  (Integration)     (Conductance)       (Spike Train)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Neuron | 신호를 통합하여 임계치를 넘으면 스파이크 발생 | 스위치 보드 |
| Synapse | 뉴런 간 연결 강도(가중치)를 저장 및 조절 | 수도꼭지 밸브 |
| SNN | 시간에 따른 이벤트(Spike) 기반의 정보 처리 모델 | 모스 부호 통신 |

- > 요약: 연산과 저장이 한 곳에서 이루어지는 프로세싱-인-메모리(PIM) 지향

## Ⅲ. 절차
- ASCII 흐름도
  [Input Spike] -> [Synaptic Weighting] -> [Membrane Potential] -> [Firing]

1. 인코딩: 입력 데이터를 시계열성 스파이크 신호로 변환
2. 가중치 적용: 시냅스 소자를 통과하며 신호 강도 조절 (메모리 병목 없음)
3. 전위 축적: 수신 뉴런의 막 전위(Potential)가 누적됨
4. 출력 발화: 전위가 임계값 도달 시 다음 뉴런으로 스파이크 전송

- > 요약: 데이터가 있을 때만 동작하는 이벤트 중심(Event-driven) 저전력 연산

## Ⅳ. 문제점
- 학습 알고리즘 부재: 기존 오차역전파(Backpropagation) 적용이 어려워 학습 효율 저하
- 표준화 미흡: 하드웨어 구조별 상이한 프로그래밍 모델로 인한 생태계 확장 한계

## Ⅴ. 개선방안
- 하이브리드 모델: 학습은 DNN(GPU), 추론은 SNN(뉴로모픽)으로 분리 운영
- 신소재 소자: 멤리스터(Memristor) 등 뇌 가소성을 모방한 차세대 반도체 소자 적용

## Ⅵ. 전망
- 로드맵: 에지(Edge) 기기의 초저전력 상시 모니터링(Always-on) 핵심 칩으로 성장
- CSF: 온칩 학습(On-chip Learning) 기능 강화를 통한 자가 진화형 AI 하드웨어 구현
