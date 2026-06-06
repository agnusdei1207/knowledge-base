---
title: "156. Source Coding"
date: "2026-04-21"
tags:
  - "studynote-algorithm"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 섀넌의 소스 부호화 정리는 *[엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) H(X)가 무손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 절대 하한*임을 증명 — 어떤 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)도 평균 H(X) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)/심볼 미만으로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)할 수 없다.
> 2. **가치**: 허프만 (Huffman) 코딩은 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)에 1 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 이내로 근접하고, 산술 부호화는 임의로 가깝게 접근하며, LZ 계열은 점근적으로 최적이다.
> 3. **판단 포인트**: 무손실과 손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 경계 — 레이트-왜곡 이론 (Rate-Distortion Theory) 이 허용 왜곡 D 아래에서 달성 가능한 최소 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)율 R(D)를 정의한다.

---

## Ⅰ. 개요 및 필요성

**소스 부호화 정리 (Source Coding Theorem, 또는 섀넌 제1 정리)**:

"독립 동일 분포 (i.i.d.) [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)원 X를 무손실로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)할 때, 심볼당 평균 코드 길이 L̄은 반드시 H(X) 이상이다. 반면, H(X) + ε [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)/심볼로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)하는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 항상 존재한다."

```
H(X) ≤ L̄ < H(X) + ε   (임의로 작은 ε > 0에 대해 달성 가능)
```

이 정리는 두 방향으로 동시에 증명된다:
- **불가능성**: L̄ < H(X) [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)은 정보 손실 없이 불가
- **달성 가능성**: H(X) + ε 이내의 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 방법 존재

📢 **섹션 요약 비유**: 소스 부호화 정리는 "짐 싸기 한계"다 — 여행 가방(코드)에 짐(정보)을 아무리 효율적으로 넣어도 짐 자체의 정보량([엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/)) 만큼은 반드시 넣어야 하며, 그것보다 작게는 절대 불가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주요 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

```
평균 코드 길이 L̄
         |
H(X)+1   +------------ 허프만 코딩 ----------------
H(X)+0.1 +------------ 산술 부호화 ---------------
H(X)+ε   +------------ LZ 계열 (점근적) ---------
H(X)     +------------ 이론 하한 -----------------
         |
         +--------------------------------------►
                        블록 길이 n -> ∞
```

### [허프만 코딩](/studynote/08_algorithm_stats/05_string/100_huffman_coding/) ([Huffman Coding](/studynote/08_algorithm_stats/05_string/100_huffman_coding/)) 예시

[확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 분포: A(0.5), B(0.25), C(0.125), D(0.125)

[엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/): H = -(0.5·log0.5 + 0.25·log0.25 + 0.125·log0.125 + 0.125·log0.125)
         = 0.5·1 + 0.25·2 + 0.125·3 + 0.125·3 = 1.75 bits

허프만 트리 구성:

```
심볼:  A(0.5)  B(0.25)  C(0.125)  D(0.125)

단계1:        C+D -> 0.25
단계2:     B + 0.25 -> 0.5
단계3:  A + 0.5 -> 1.0 (루트)

코드: A->0, B->10, C->110, D->111

평균 코드 길이: 0.5×1 + 0.25×2 + 0.125×3 + 0.125×3 = 1.75 bits
-> 엔트로피와 완전히 동일!
```

| 심볼 | [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) | 코드 | 길이 |
|:---:|:---:|:---:|:---:|
| A | 0.500 | 0 | 1 |
| B | 0.250 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 2 |
| C | 0.125 | 110 | 3 |
| D | 0.125 | 111 | 3 |

허프만의 성질: H(X) ≤ L̄_Huffman < H(X) + 1

### [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)별 비교

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 방식 | 한계 도달 | 속도 |
|:---|:---|:---:|:---|
| [허프만 코딩](/studynote/08_algorithm_stats/05_string/100_huffman_coding/) | 심볼별 가변 길이 코드 | H + 1 이내 | 빠름 |
| 산술 부호화 | 구간 분할 | H + ε | 느림 |
| LZ77 | 슬라이딩 윈도우 사전 | 점근적 H | 빠름 |
| LZ78/LZW | 동적 사전 | 점근적 H | 빠름 |
| DEFLATE | LZ77 + 허프만 | 실용적 최적 | 빠름 |
| Brotli | LZ77 + 허프만 + [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 모델 | 더 높은 비율 | 느림 |
| Zstandard (zstd) | ANS + 허프만 + LZ | 고속 + 고비율 | 매우 빠름 |

📢 **섹션 요약 비유**: [허프만 코딩](/studynote/08_algorithm_stats/05_string/100_huffman_coding/)은 "자주 쓰는 단어에 짧은 줄임말"을 배정하는 것이다 — "국제연합"을 "UN"으로, "[인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)"을 "[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"로 쓰는 것처럼 빈도 높은 심볼에 짧은 코드를 준다.

---

## Ⅲ. 비교 및 연결

### 손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)과 레이트-왜곡 이론

무손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)의 하한 = H(X). 하지만 약간의 왜곡(오차)을 허용하면?

**레이트-왜곡 이론 (Rate-Distortion Theory)**:

```
R(D) = min_{P(X̂|X): E[d(X,X̂)]≤D} I(X;X̂)
```

D: 최대 허용 왜곡, R(D): 그에 대응하는 최소 필요 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)율

```
R(D)
   ^
   |╲
   |  ╲
   |    ╲
   |      -----
   +-----------► D
  D=0   D 증가시 R 감소

D=0: R = H(X) (무손실)
D->∞: R -> 0 (극단 손실)
```

📢 **섹션 요약 비유**: 레이트-왜곡 트레이드오프는 "사진 화질 vs [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기"다 — 화질(D 낮음)을 높이면 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(R)이 커지고, 허용 화질 저하(D 높음)를 늘리면 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 작아진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실제 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 파이프라인 (DEFLATE = ZIP, PNG, gzip)

```
원본 데이터
     |
     v LZ77 (중복 제거)
길이-오프셋 쌍
     |
     v 허프만 코딩 (심볼 인코딩)
압축 비트스트림
     |
     v 컨테이너 포맷 (.zip, .png, .gz)
최종 파일
```

### 영역별 채택 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기술

| 분야 | 기술 | 방식 |
|:---|:---|:---|
| 텍스트/[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | gzip, brotli, zstd | LZ + 허프만 (무손실) |
| 이미지 정지 | JPEG (DCT), PNG (DEFLATE) | 손실/무손실 |
| 동영상 | H.264, H.265, AV1 | 모션 보상 + DCT (손실) |
| 오디오 | MP3, AAC, Opus | 심리음향 모델 (손실) |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | GZIP + [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 손실 허용 |

### 기술사 판단 포인트

1. <strong>"무손실 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> 이론 한계는?"</strong> -> [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) H(X) [bits/symbol]
2. <strong>"<a href="/studynote/08_algorithm_stats/05_string/100_huffman_coding/">허프만 코딩</a>이 최적인가?"</strong> -> 심볼 수 무한 시 아님, 산술 부호화가 더 가까움
3. **"JPEG는 무손실인가?"** -> 기본은 DCT 손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) (JPEG 2000 웨이블릿도 손실)

📢 **섹션 요약 비유**: DEFLATE(LZ77+허프만)는 "두 단계 짐 싸기"다 — 먼저 중복 물건을 없애고(LZ77), 나머지를 무게 순으로 효율 포장한다(허프만).

---

## Ⅴ. 기대효과 및 결론

소스 부호화 정리는 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기술의 <strong>절대 기준점</strong>이다. 현대 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)들이 이 한계에 얼마나 가깝게 도달했는지를 평가하는 척도로 활용된다.

신경망 기반 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) (Neural [Compression](/studynote/08_algorithm_stats/09_info_theory/159_compression/)) 은 비선형 표현 학습으로 기존 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 능가하기 시작했다:
- <strong>학습 기반 이미지 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> (Learned Image <a href="/studynote/08_algorithm_stats/09_info_theory/159_compression/">Compression</a>)</strong>: VGG/[ResNet](/studynote/10_ai/04_ai_ops_ethics/287_resnet_skip_connection/) [인코더](/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/) + [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) 모델 + [디코더](/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)
- JPEG와 H.265를 동일 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)율에서 시각 품질 면에서 능가

📢 **섹션 요약 비유**: 신경망 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)은 "[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 포장 전문가"다 — 고전 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 수학 공식으로 짐 쌌다면, AI는 경험으로 인간이 어떤 부분에 덜 민감한지 학습해 더 효율적으로 포장한다.

---

### 📌 관련 개념 맵

| 개념 | 수식 | 연결 |
|:---|:---|:---|
| 소스 부호화 정리 | H(X) ≤ L̄ | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 하한 |
| [허프만 코딩](/studynote/08_algorithm_stats/05_string/100_huffman_coding/) | L̄ < H(X) + 1 | 빈도 기반 가변 길이 코드 |
| 산술 부호화 | L̄ -> H(X) | 전체 메시지를 단일 수로 |
| LZ77/LZW | 점근적 H(X) | 실용 무손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) |
| 레이트-왜곡 R(D) | 손실 허용 시 최소 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)율 | JPEG, MP3, H.265 |

### 📈 관련 키워드 및 발전 흐름도

```text
[정보 이론 (Information Theory)]
    |
    v
[엔트로피 (Entropy)]
    |
    v
[소스 코딩 (Source Coding)]
    |
    v
[무손실 압축 (Lossless Compression)]
    |
    v
[손실 압축 (Lossy Compression)]
    |
    v
[채널 코딩 (Channel Coding)]
```

정보 이론의 [엔트로피](/studynote/08_algorithm_stats/09_info_theory/151_entropy/) 개념이 소스 코딩 원리로 구체화되어 무손실·손실 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 기술로 발전하는 흐름이다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/studynote/08_algorithm_stats/09_info_theory/151_entropy/">엔트로피</a> = 짐 최소 무게</strong>: 아무리 잘 개도 짐의 정보만큼의 무게는 가져가야 한다.
2. **허프만 = 자주 쓰는 단어 줄임말**: "반갑습니다"->"반갑", "안녕하세요"->"안녕"처럼 자주 나오는 것에 짧은 코드.
3. <strong>손실 <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> = 살짝 흐릿한 사진</strong>: 완벽한 원본 대신 눈에 덜 띄는 부분을 조금 희생해 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 작게 만든다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 156 / 175

<- **이전**: [6. 채널 용량 (Channel Capacity) — 샤논 용량 공식](/studynote/08_algorithm_stats/09_info_theory/155_channel_capacity/)
**다음**: [8. 채널 부호화 정리 (Channel Coding Theorem) — 샤논 한계](/studynote/08_algorithm_stats/09_info_theory/157_channel_coding/) ->

---
