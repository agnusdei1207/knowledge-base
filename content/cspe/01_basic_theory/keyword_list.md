---
title: "Keyword List"
date: "2026-07-05"
tags:
  - "cspe-basic-theory"
weight: 50
---

<컴퓨터 기초이론 키워드 목록 (80제)>
컴퓨터시스템응용기술사 시험 출제동향 기반으로 엄선한 컴퓨터 기초이론 핵심 키워드입니다.

---

## 1. 알고리즘 및 자료구조 (18개)
1. 알고리즘 시간복잡도·공간복잡도 (Time/Space Complexity) — 알고리즘 수행시간·메모리 사용량을 입력 크기 함수로 분석하는 기법 [출제:131회]
2. 빅오 표기법 (Big-O Notation) — 최악의 경우 성능 상한을 나타내는 점근 표기법 [출제:131회]
3. 정렬 알고리즘 비교 — 퀵·병합·힙·버블 (Sorting Algorithms) — 다양한 정렬 기법의 시간복잡도·안정성·공간 효율 비교 [출제:122,131회]
4. 이진 탐색 (Binary Search) — 정렬된 배열에서 중간값 비교를 반복하여 O(log n)에 탐색하는 알고리즘
5. 해시 테이블 (Hash Table) — 해시 함수를 이용해 키-값 쌍을 O(1)에 저장·조회하는 자료구조
6. 연결 리스트 (Linked List) — 노드가 포인터로 연결된 선형 자료구조, 삽입·삭제 O(1)
7. 스택·큐·덱 (Stack Queue Deque) — LIFO·FIFO·양방향 입출력 선형 자료구조
8. 트리 구조 — B-Tree·AVL·Red-Black (Tree Data Structures) — 균형 탐색 트리의 구조·회전·삽입·삭제 연산 [출제:122,137회]
9. 이진트리 순회 — 전위·중위·후위 (Binary Tree Traversal) — 이진트리 노드 방문 순서에 따른 세 가지 순회 방식 [출제:126회]
10. 그래프 탐색 — BFS·DFS (Graph Traversal) — 너비 우선·깊이 우선으로 그래프 전체를 방문하는 탐색 기법
11. 최단 경로 — 다익스트라·벨만-포드·플로이드 (Shortest Path) — 가중 그래프에서 최단 경로를 구하는 대표 알고리즘
12. 최소 신장 트리 — 크루스칼·프림 (Minimum Spanning Tree) — 모든 정점을 최소 비용으로 연결하는 부분 그래프 알고리즘
13. 동적 프로그래밍 (Dynamic Programming) — 부분 문제 결과를 저장하여 중복 계산을 피하는 최적화 기법
14. 분할 정복 (Divide and Conquer) — 문제를 하위 문제로 분할·정복·결합하여 해결하는 알고리즘 설계 전략
15. 탐욕 알고리즘 (Greedy Algorithm) — 각 단계에서 지역 최적 선택을 반복하여 전역 최적에 도달하는 기법
16. 백트래킹 (Backtracking) — 해 공간 탐색 중 조건 위반 시 되돌아가며 탐색하는 기법
17. 몬테카를로 방법 (Monte Carlo Method) — 무작위 샘플링으로 수학적·물리적 문제의 근사해를 구하는 확률적 방법 [출제:131회]
18. 몬테카를로 트리탐색 MCTS (Monte Carlo Tree Search) — 시뮬레이션 기반 트리 탐색으로 게임·의사결정에 활용하는 기법 [출제:135회]

## 2. 계산 이론 (5개)
19. NP-완전 문제 (NP-Complete) — 다항 시간 내 검증 가능하지만 풀이 시간이 비결정론적인 문제 클래스
20. 오토마타 이론 — DFA·NFA (Automata Theory) — 유한 상태 기계를 통해 언어 인식·계산 능력을 분석하는 이론
21. 정규 언어·문법 (Regular Language and Grammar) — 정규 표현식·유한 오토마타로 정의되는 가장 단순한 언어 클래스
22. 문맥 자유 문법 (Context-Free Grammar) — 프로그래밍 언어 구문 정의에 사용되는 생성 문법
23. 튜링 머신 (Turing Machine) — 계산 가능성의 수학적 모델, 모든 알고리즘을 표현할 수 있는 추상 기계 [출제:129회]

## 3. 수 체계 및 디지털 논리 (6개)
24. 수 체계 변환 — 이진·8진·16진 (Number System Conversion) — 컴퓨터 내부 데이터 표현을 위한 진법 간 변환
25. 부동소수점 표현 — IEEE 754 (Floating Point IEEE 754) — 실수의 부호·지수·가수 기반 이진 표현 국제 표준
26. 2의 보수·부호 표현 (Two's Complement) — 음수를 이진수로 표현하는 보수 체계
27. 논리 게이트·부울 대수 (Logic Gates and Boolean Algebra) — AND·OR·NOT 등 기본 논리 연산과 부울 함수 간소화
28. 조합 논리 회로 — 가산기·멀티플렉서 (Combinational Logic) — 현재 입력만으로 출력이 결정되는 논리 회로
29. 순서 논리 회로 — 플립플롭·레지스터 (Sequential Logic) — 이전 상태를 기억하여 출력이 결정되는 논리 회로

## 4. 정보이론 및 코딩 (5개)
30. 해밍 코드·오류 검출·정정 (Hamming Code Error Detection) — 패리티 비트를 이용한 1비트 오류 검출·정정 코드 [출제:125회]
31. 정보이론 — 엔트로피·채널 용량·섀넌 한계 (Information Theory Shannon) — 정보량 측정과 통신 채널의 이론적 최대 전송률 [출제:135회]
32. 허프만 코딩 (Huffman Coding) — 빈도 기반 가변 길이 코드를 생성하는 무손실 압축 알고리즘
33. 런랭스 인코딩 (Run-Length Encoding) — 연속 반복 데이터를 횟수·값 쌍으로 압축하는 기법
34. 소스 코딩 vs 채널 코딩 (Source Coding vs Channel Coding) — 데이터 압축(소스 코딩)과 오류 정정(채널 코딩)의 비교 [출제:129회]

## 5. 수학 기초 (11개)
35. 행렬 연산 — 행렬 곱·역행렬·전치 (Matrix Operations) — 선형대수의 기본 연산, AI·그래픽스 핵심 수학
36. 선형 변환 (Linear Transformation) — 벡터 공간 간 구조를 보존하는 함수, 행렬로 표현
37. 고유값·고유벡터 (Eigenvalue Eigenvector) — 선형 변환에서 방향이 변하지 않는 벡터와 그 배율
38. 확률 기초 — 베이즈 정리 (Bayes Theorem) — 사전 확률로부터 사후 확률을 갱신하는 조건부 확률 정리
39. 확률 분포 — 정규·이항·포아송 (Probability Distribution) — 확률 변수의 값 분포를 나타내는 대표적 확률 분포
40. 가설 검정·신뢰 구간 (Hypothesis Testing Confidence Interval) — 통계적 유의성 판단과 모수 추정 범위 설정
41. 회귀 분석 (Regression Analysis) — 독립 변수와 종속 변수 간 관계를 모델링하는 통계 기법
42. 클러스터링 — K-Means·DBSCAN (Clustering) — 유사 데이터를 그룹화하는 비지도 학습 알고리즘
43. 주성분 분석 PCA (Principal Component Analysis) — 고차원 데이터의 분산을 최대화하는 축으로 차원 축소
44. 유사도 측정 — 코사인·자카드·유클리드 (Similarity Measures) — 벡터·집합 간 거리 및 유사도를 정량화하는 척도 [출제:128회]
45. 교차 검증 K-Fold (Cross Validation K-Fold) — 데이터를 K개 폴드로 나눠 모델 성능을 평가하는 기법 [출제:128회]

## 6. 기계학습 및 딥러닝 (20개)
46. 과적합·과소적합·편향-분산 트레이드오프 (Overfitting Bias-Variance Tradeoff) — 모델 일반화 성능에 영향을 미치는 학습 오류 유형과 균형
47. 활성화 함수 — ReLU·Sigmoid·Tanh (Activation Functions) — 신경망 비선형성을 부여하는 함수 [출제:120회]
48. 역전파 알고리즘 (Backpropagation) — 출력 오차를 역방향으로 전파하여 가중치를 갱신하는 학습 알고리즘
49. 경사하강법 — SGD·Adam·AdaGrad (Gradient Descent) — 손실 함수의 기울기를 따라 최적 파라미터를 탐색하는 최적화 기법
50. 손실 함수 — Cross-Entropy·MSE (Loss Functions) — 예측값과 실제값 간 오차를 정량화하는 목적 함수
51. 배치 정규화 (Batch Normalization) — 미니배치 단위로 입력을 정규화하여 학습 안정성을 높이는 기법
52. 드롭아웃 (Dropout) — 학습 시 무작위로 뉴런을 비활성화하여 과적합을 방지하는 정규화 기법
53. 합성곱 신경망 CNN (Convolutional Neural Network) — 필터 기반 특징 추출로 이미지 인식에 특화된 신경망 [출제:120,128회]
54. 순환 신경망 RNN·LSTM·GRU (Recurrent Neural Network) — 시퀀스 데이터 처리에 특화된 순환 구조 신경망 [출제:121회]
55. 오토인코더 (Autoencoder) — 입력을 압축·복원하여 특징을 학습하는 비지도 신경망 [출제:131회]
56. GAN 생성적 적대 신경망 (Generative Adversarial Network) — 생성자와 판별자가 경쟁하며 데이터를 생성하는 모델 [출제:122회]
57. 전이 학습 (Transfer Learning) — 사전 학습된 모델의 지식을 새 과제에 재활용하는 기법 [출제:123,131회]
58. 지도 학습·비지도 학습·강화 학습 분류 (Learning Paradigms) — 레이블 유무·보상 체계에 따른 기계학습 패러다임 분류 [출제:120회]
59. 결정 트리 (Decision Tree) — 특징 기반 분기 규칙으로 분류·회귀를 수행하는 트리 모델
60. 랜덤 포레스트 (Random Forest) — 다수의 결정 트리를 앙상블하여 예측 정확도를 높이는 기법
61. SVM 서포트 벡터 머신 (Support Vector Machine) — 최대 마진 초평면으로 분류하는 지도 학습 모델 [출제:132회]
62. 나이브 베이즈 분류 (Naive Bayes Classifier) — 특징 독립 가정 하에 베이즈 정리를 적용하는 확률 분류기
63. 앙상블 학습 — 배깅·부스팅·스태킹 (Ensemble Learning) — 다수 모델을 결합하여 성능을 향상시키는 학습 전략
64. XGBoost·LightGBM (XGBoost LightGBM) — 그래디언트 부스팅 기반 고성능 앙상블 프레임워크 [전망]
65. 추천 시스템 — 협업 필터링·콘텐츠 기반 (Recommendation System) — 사용자 행동·콘텐츠 유사도 기반 개인화 추천 기법 [출제:131회]

## 7. 자연어 처리 및 컴퓨터 비전 (6개)
66. 자연어 처리 — 토크나이징·형태소 분석 (NLP Tokenization) — 텍스트를 의미 단위로 분리하는 NLP 전처리 기법
67. 단어 임베딩 — Word2Vec·GloVe (Word Embedding) — 단어를 밀집 벡터로 변환하여 의미적 유사도를 표현하는 기법
68. BERT 사전학습 모델 (BERT Pre-trained Model) — 양방향 트랜스포머 기반 대규모 사전학습 언어 모델 [출제:121회]
69. GPT 언어 모델 (GPT Language Model) — 자기회귀 트랜스포머 기반 텍스트 생성 대규모 언어 모델 [출제:124,127회]
70. 객체 탐지 — YOLO·R-CNN (Object Detection) — 이미지에서 객체 위치와 클래스를 실시간 검출하는 기법 [출제:126회]
71. 이미지 분류 — ResNet·VGG·EfficientNet (Image Classification) — 심층 CNN 기반 이미지 범주 분류 모델 [출제:120회]

## 8. 프로그래밍 언어 및 컴파일러 (3개)
72. 형식 언어 이론 (Formal Language Theory) — 문법·오토마타로 언어를 정의·분류하는 이론적 체계
73. 컴파일러 구조 — 어휘·구문·의미 분석 (Compiler Structure) — 소스 코드를 기계어로 변환하는 컴파일러의 다단계 구조
74. 파서 — LL·LR (Parser LL LR) — 문맥 자유 문법 기반 구문 분석기의 하향식·상향식 기법

## 9. 고급 알고리즘 (6개)
75. 재귀 알고리즘·마스터 정리 (Recursive Algorithm Master Theorem) — 재귀 관계식의 시간복잡도를 체계적으로 분석하는 정리
76. 암호 수학 — 이산 대수·RSA 원리 (Cryptography Mathematics) — 공개키 암호체계의 수학적 기반 원리 [출제:128회]
77. P vs NP 문제 (P vs NP Problem) — 다항 시간 풀이와 검증의 동치 여부에 관한 미해결 난제
78. 근사 알고리즘 (Approximation Algorithm) — NP-난해 문제에 대해 최적해에 근접한 해를 다항 시간에 구하는 알고리즘
79. 병렬 알고리즘 — PRAM 모델 (Parallel Algorithm PRAM) — 다수 프로세서를 활용한 동시 연산 알고리즘 모델
80. 양자 알고리즘 — 쇼어·그로버 (Quantum Algorithm Shor Grover) — 양자 컴퓨팅 기반 소인수분해·탐색 알고리즘 [전망]
