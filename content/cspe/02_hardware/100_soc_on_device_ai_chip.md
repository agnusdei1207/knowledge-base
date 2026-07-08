---
title: "SoC AI 온디바이스 칩 (SoC On-Device AI Chip)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 100
extra:
  question_no: "100"
  exam_status: "기출"
  exam_history: "134회, 135회"
---

## 미리 알고가기

- SoC는 CPU와 GPU와 NPU와 메모리와 I/O를 하나의 칩에 통합한 구조임
- 온디바이스 AI는 클라우드 전송 없이 단말 내부에서 추론을 수행하는 방식임
- TOPS 수치는 참고 지표일 뿐 실제 성능은 메모리와 전력과 모델 호환성이 좌우함

## Ⅰ. 개요

- **정의/개념**: SoC AI 온디바이스 칩은 CPU와 GPU와 NPU와 메모리 서브시스템과 보안 블록을 단일 칩에 통합해 단말 내부에서 AI 추론을 수행하도록 설계한 시스템 반도체임
- **배경/필요성**: 모바일과 차량과 IoT 단말은 지연과 네트워크 비용과 개인정보 문제 때문에 클라우드 의존을 줄여야 하므로, 제한된 전력과 열 예산 안에서 AI 추론을 처리할 수 있는 전용 칩 구성이 필요함

## Ⅱ. 특징

- NPU 중심으로 추론을 오프로딩해 CPU 대비 전력 효율을 높임
- 메모리 대역폭과 on-chip buffer 구조가 실제 추론 지연을 크게 좌우함
- 모델 연산자 호환성과 quantization 지원 수준이 활용 범위를 결정함
- secure boot와 모델 보호와 OTA 업데이트 체계가 제품 수명주기 품질을 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | 클라우드 AI 처리 | 온디바이스 AI SoC |
|:---|:---|:---|
| 지연 | 네트워크 왕복에 영향 받음 | 단말 내부에서 즉시 응답 가능 |
| 개인정보 | 원본 데이터 외부 전송 부담 큼 | 로컬 처리로 노출 범위 축소 가능 |
| 연산 자원 | 대규모 서버 자원 활용 가능 | 전력과 열과 메모리 제약이 큼 |
| 운영 포인트 | 서버 확장성과 비용 관리 | 모델 경량화와 칩 호환성 관리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| CPU and GPU | 전처리와 후처리와 범용 제어를 맡아 NPU가 처리하지 않는 작업을 보완함 |
| NPU | CNN과 Transformer 연산을 높은 전력 효율로 처리하며 실제 온디바이스 추론 성능의 중심이 됨 |
| Memory Subsystem | 가중치와 activation 공급을 담당해 연산기보다 먼저 병목이 되기 쉬운 핵심 경로임 |
| Security and Power Block | 모델 보호와 무결성 검증과 DVFS 제어를 담당해 보안성과 배터리 수명을 동시에 좌우함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 모델 준비      | --> | 칩 맞춤 최적화 | --> | 추론 실행      | --> | 결과/업데이트  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **모델 준비**: 목표 정확도와 입력 크기와 지연 요구에 맞는 모델을 선정함
2. **칩 맞춤 최적화**: quantization과 operator mapping으로 모델을 NPU 형식에 맞춤 변환함
3. **추론 실행**: NPU와 메모리와 DMA와 CPU가 협력해 추론 파이프라인을 수행함
4. **결과 및 업데이트**: 후처리와 보안 검증과 OTA 모델 갱신을 운영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: NPU가 지원하지 않는 연산자가 많으면 CPU fallback 비율이 커져 지연과 전력 소모가 급증할 수 있음
   - 해결방안: 타깃 NPU 연산자 집합에 맞춘 모델 설계를 적용하고 NPU execution coverage와 fallback ratio로 검증함
2. 문제: 높은 TOPS를 가져도 메모리 이동과 발열 제약이 크면 실제 추론 처리량이 기대에 못 미칠 수 있음
   - 해결방안: quantization과 buffer reuse와 DVFS 튜닝을 적용하고 inferences per watt와 thermal throttling rate로 검증함
3. 문제: 단말 내부에 모델과 입력 데이터가 남아 있으면 추출과 변조와 적대적 입력 위험이 커질 수 있음
   - 해결방안: secure boot와 model encryption과 무결성 검증을 운영하고 model tamper detection rate와 update success rate로 검증함

## Ⅶ. 적용 사례

- 스마트폰 생성형 AI 기능에서는 모델을 NPU 친화적으로 양자화하고 확인 지표는 latency와 NPU execution coverage임
- 엣지 카메라 분석 장치에서는 영상 전처리와 추론을 파이프라인화하고 확인 지표는 inferences per watt와 thermal throttling rate임
- 차량용 보조 인식 장치에서는 보안 부팅과 OTA 모델 갱신을 결합하고 확인 지표는 update success rate와 model tamper detection rate임

## Ⅷ. 결론

온디바이스 AI SoC는 TOPS 경쟁보다 모델 호환성, 메모리 경로, 전력과 보안 업데이트 체계를 얼마나 균형 있게 통합했는지가 실질 가치임.
