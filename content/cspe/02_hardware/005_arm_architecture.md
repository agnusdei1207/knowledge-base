---
title: "ARM 프로세서 아키텍처·동작 모드 (ARM Architecture)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 5
extra:
  question_no: "005"
  exam_status: "기출"
  exam_history: "126회"
---

## 미리 알고가기

- ARM은 저전력 RISC 계열 아키텍처로 모바일·임베디드 시장의 주류임
- AArch32와 AArch64, 사용자·커널 권한 모드 구분이 핵심임
- 성능보다 전력 효율과 생태계 최적화가 강점임

## Ⅰ. 개요

- **정의/개념**: ARM 아키텍처는 저전력과 단순 파이프라인 효율을 기반으로 발전한 RISC ISA 계열로, AArch32와 AArch64 실행 상태와 다양한 권한 모드를 통해 모바일·임베디드·서버 환경을 지원하는 프로세서 구조임
- **배경/필요성**: 배터리 기반 기기와 대규모 SoC 환경에서는 절대 성능뿐 아니라 와트당 성능과 통합 IP 생태계가 중요하므로 저전력 지향 ISA가 필요해짐

## Ⅱ. 특징

- 고정 길이 명령어와 간결한 실행 구조로 전력 효율이 높음
- Thumb와 AArch64 등 코드 밀도와 확장성을 함께 제공함
- 권한 모드와 예외 레벨 구조가 OS·하이퍼바이저 설계를 지원함
- 고성능 영역으로 갈수록 마이크로아키텍처 복잡도는 RISC 단순성만으로 설명되지 않음

## Ⅲ. 종류 및 비교

| 판단 기준 | ARM | x86-64 |
|:---|:---|:---|
| ISA 성격 | RISC 중심 | CISC 중심 |
| 강점 | 저전력·SoC 통합 | 레거시 호환성과 고성능 |
| 코드 밀도 | Thumb 등으로 보완 | 높은 편 |
| 대표 시장 | 모바일·임베디드·확대 중인 서버 | PC·서버 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Execution State | AArch32와 AArch64가 명령어 폭과 레지스터 모델을 결정함 |
| Exception Level | EL0~EL3 권한 구조가 사용자·커널·하이퍼바이저·보안 모드를 나눔 |
| Register Set | 범용 레지스터와 special register가 호출 규약과 성능 특성을 좌우함 |
| Extension Path | NEON과 SVE 같은 확장이 멀티미디어와 벡터 처리 성능을 강화함 |

```text
+----------------+     +----------------+     +--------------+
| Execution State | --> | Register Set   | --> | Extension    |
+----------------+     +----------------+     +--------------+
      |
      v
+----------------+
| Exception Level |
+----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 실행 상태 선택   | --> | 권한 모드 진입    | --> | 명령어 수행     | --> | 예외 처리      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **실행 상태 선택**: AArch32 또는 AArch64 환경을 정함
2. **권한 모드 진입**: EL 수준에 맞는 제어 권한을 확보함
3. **명령어 수행**: 일반 연산과 벡터 확장을 수행함
4. **예외 처리**: 인터럽트와 예외를 해당 레벨에서 처리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 32비트와 64비트 상태가 혼재하면 포팅과 ABI 호환성이 복잡해질 수 있음
   - 해결방안: target ABI를 명확히 고정하고 compatibility defect count와 porting lead time으로 검증함
2. 문제: 저전력 최적화만 강조하면 고성능 워크로드에서 메모리와 벡터 성능 병목이 드러날 수 있음
   - 해결방안: workload별 core type과 vector extension을 조정하고 perf per watt와 vector utilization로 검증함
3. 문제: 권한 모드와 보안 확장을 잘못 구성하면 하이퍼바이저와 보안 영역 분리가 약해질 수 있음
   - 해결방안: privilege design review를 수행하고 isolation violation count와 secure boot pass rate로 검증함

## Ⅶ. 적용 사례

- 모바일 AP 포팅에서는 ABI를 고정하고, compatibility defect count와 porting lead time로 결과를 확인함
- 엣지 AI SoC에서는 벡터 확장을 조정하고, perf per watt와 vector utilization로 결과를 확인함
- 보안 민감 임베디드 장치에서는 권한 설계를 검토하고, isolation violation count와 secure boot pass rate로 결과를 확인함

## Ⅷ. 결론

ARM 아키텍처의 경쟁력은 단순 RISC라서가 아니라 전력 효율과 실행 모드와 SoC 생태계를 함께 최적화해 다양한 장치에 맞춘다는 데 있음.
