import os
import re

directory = r"C:\workspace\study\src\content\docs\notes\08-latest-tech"

# Mapping of Korean terms to English + better description suffix
terms_mapping = {
    "임베딩": ("Embedding", "고차원 비정형 데이터를 저차원 연속 벡터 공간으로 매핑하여 유사도 연산 및 기계학습 모델의 입력으로 활용 가능케 하는 핵심 데이터 표현 기술"),
    "청킹": ("Chunking", "대용량 문서를 의미적 일관성이 유지되는 최소 단위(Chunk)로 분할하여 검색 효율성 및 언어 모델의 문맥 이해도를 극대화하는 전처리 기법"),
    "뉴럴 리랭커": ("Neural Reranker", "초기 검색된 문서 목록의 문맥적 연관성을 교차 인코더(Cross-Encoder) 등의 신경망 모델로 심층 분석하여 사용자 질의에 최적화된 순위로 재조정하는 기술"),
    "지식 그래프": ("Knowledge Graph", "개체(Entity)와 그들 간의 관계(Relation)를 그래프 형태로 구조화하여 데이터의 상호 연결성을 표현하고 복잡한 추론을 지원하는 지식 베이스 기술"),
    "온톨로지": ("Ontology", "특정 도메인의 지식 구조를 개념, 속성, 관계로 공식화하여 컴퓨터가 이해하고 추론할 수 있도록 명세하는 시맨틱 웹의 기반 기술"),
    "RAG 평가": ("RAG Evaluation", "검색 증강 생성(RAG) 시스템의 답변 신뢰성, 검색 정확도, 컨텍스트 연관성 등을 정량적/정성적으로 측정하여 환각(Hallucination)을 방지하고 품질을 보증하는 체계"),
    "RAGAS": ("RAG Assessment", "RAG 시스템 성능을 답변 정답성(Faithfulness), 답변 관련성(Answer Relevance), 컨텍스트 정밀도(Context Precision) 등의 지표로 자동화하여 평가하는 프레임워크"),
    "AI 환각": ("AI Hallucination", "생성형 AI 모델이 학습 데이터의 편향이나 불완전성으로 인해 사실이 아니거나 논리적으로 모순된 정보를 마치 진실인 것처럼 생성하는 현상"),
    "엔터프라이즈 RAG": ("Enterprise RAG", "기업 내부의 비공개 데이터와 문서를 안전하게 연동하여 보안, 권한 관리, 확장성을 보장하면서 맞춤형 지식을 제공하는 기업용 검색 증강 생성 아키텍처"),
    "권한 인지 RAG": ("Permission-aware RAG", "사용자의 직급, 부서, 접근 권한 등에 따라 RAG 시스템이 참조할 수 있는 문서 범위를 동적으로 제어하여 기밀 정보 유출을 원천 차단하는 보안 기술"),
    "AI 검색": ("AI Search", "단순 키워드 매칭을 넘어 사용자의 의도와 문맥을 이해하고, 의미 기반 임베딩과 생성 모델을 결합하여 최적의 정답을 직접 합성해 제공하는 차세대 검색 패러다임"),
    "멀티모달 AI": ("Multimodal AI", "텍스트, 이미지, 오디오, 비디오 등 두 가지 이상의 다양한 데이터 형태(Modality)를 동시에 입력받아 처리하고 융합적 추론을 수행하는 인공지능 기술"),
    "비전 언어 모델": ("Vision Language Model, VLM", "시각적 정보(이미지/비디오)와 언어적 정보(텍스트)를 하나의 잠재 공간(Latent Space)에 매핑하여 이미지 캡셔닝, 시각적 질의응답(VQA) 등을 수행하는 복합 모델"),
    "CLIP": ("Contrastive Language-Image Pretraining", "이미지와 그에 해당하는 텍스트 설명 쌍을 대조 학습(Contrastive Learning)하여, 두 모달리티 간의 의미적 일치도를 측정하고 제로샷(Zero-shot) 분류를 가능하게 하는 범용 모델"),
    "디퓨전 모델": ("Diffusion Model", "데이터에 점진적으로 노이즈를 추가하는 정방향 과정과 노이즈를 제거하며 원본 데이터를 복원하는 역방향 과정을 학습하여 고품질의 이미지/오디오를 생성하는 확률적 생성 모델"),
    "비디오 생성": ("Video Generation", "텍스트 프롬프트나 정지 이미지를 기반으로 시공간적 일관성(Spatio-temporal Consistency)이 유지되는 동적 비디오 프레임을 합성해내는 딥러닝 기술"),
    "멀티모달 RAG": ("Multimodal RAG", "기존 텍스트 위주의 RAG를 확장하여 문서 내 표, 차트, 이미지 등의 비정형 시각 데이터까지 함께 검색하고 참조하여 포괄적인 답변을 생성하는 시스템"),
    "문서 AI": ("Document AI", "광학 문자 인식(OCR)과 자연어 처리(NLP), 컴퓨터 비전을 결합하여 영수증, 계약서 등 다양한 비정형 문서에서 핵심 데이터를 자동으로 추출하고 정형화하는 솔루션"),
    "그래프 신경망": ("Graph Neural Network, GNN", "노드(Node)와 엣지(Edge)로 구성된 그래프 데이터의 구조적 특성과 위상 정보를 이웃 노드와의 메시지 패싱(Message Passing)을 통해 학습하는 딥러닝 아키텍처"),
    "강화학습": ("Reinforcement Learning, RL", "에이전트가 주어진 환경(Environment)과 상호작용하며 현재 상태(State)에 따른 행동(Action)을 취하고, 누적 보상(Reward)을 최대화하는 최적의 정책(Policy)을 학습하는 기계학습 패러다임"),
    "마르코프 결정 과정": ("Markov Decision Process, MDP", "상태, 행동, 전이 확률, 보상, 감가율로 구성되어 의사결정 과정을 수학적으로 모델링하며, 미래 상태가 오직 현재 상태에만 의존한다는 마르코프 성질을 가짐"),
    "벨만 방정식": ("Bellman Equation", "현재 상태의 가치와 다음 상태의 가치 사이의 재귀적 관계를 나타내며, 동적 계획법(DP)을 통해 최적 가치 함수와 정책을 찾기 위한 강화학습의 핵심 수식"),
    "몬테카를로 트리 탐색": ("Monte Carlo Tree Search, MCTS", "무작위 샘플링 기반의 시뮬레이션을 통해 탐색 트리를 점진적으로 구축하며, 탐색(Exploration)과 활용(Exploitation)의 균형을 맞춰 방대한 상태 공간에서 최적의 수를 찾는 알고리즘"),
    "AI 거버넌스": ("AI Governance", "인공지능 시스템의 개발부터 폐기까지 전 생애주기에 걸쳐 투명성, 공정성, 책임성을 확보하고 법적/윤리적 리스크를 관리하기 위한 조직적 정책 및 통제 체계"),
    "AI 경영시스템": ("AI Management System, ISO/IEC 42001", "조직이 AI를 안전하고 책임감 있게 개발 및 활용하도록 돕는 국제 표준 규격으로, AI 리스크 관리와 지속적 개선을 위한 프로세스 및 요구사항을 정의"),
    "EU AI법": ("EU AI Act", "인공지능 시스템의 위험도를 4단계(허용 불가, 고위험, 제한적 위험, 최소 위험)로 분류하고 각 등급에 따른 엄격한 규제와 의무를 부과하는 세계 최초의 포괄적 AI 법안"),
    "AI 위험 관리": ("AI Risk Management", "AI 시스템의 편향성, 환각, 보안 취약점 등 잠재적 위험 요소를 식별, 평가, 완화하여 신뢰할 수 있는 AI 운영 환경을 보장하기 위한 일련의 활동"),
    "책임 있는 AI": ("Responsible AI", "기술적 성능뿐만 아니라 인류의 보편적 가치, 사회적 윤리, 법적 규범을 준수하며 개발/운영되어 사회에 긍정적 영향을 미치는 신뢰성 높은 인공지능"),
    "설명 가능한 AI": ("Explainable AI, XAI", "블랙박스(Black-box) 형태인 딥러닝 모델의 복잡한 내부 동작 원리와 예측 결과의 도출 근거를 인간이 이해할 수 있는 형태로 시각화하고 설명하는 기술"),
    "LIME": ("Local Interpretable Model-agnostic Explanations", "복잡한 모델의 특정 예측치 주변에 대한 국소적(Local) 데이터를 샘플링하고, 이를 기반으로 해석 가능한 단순한 선형 모델을 학습시켜 예측 근거를 설명하는 XAI 기법"),
    "SHAP": ("SHapley Additive exPlanations", "게임 이론의 섀플리 값(Shapley Value)을 기반으로, 각 입력 특성(Feature)이 모델의 최종 예측 결과에 기여한 정도를 수학적으로 공정하게 분배하여 설명하는 전역적/국소적 해석 기법"),
    "모델 카드": ("Model Card", "머신러닝 모델의 성능 특성, 의도된 용도, 한계점, 학습 데이터 구성 및 잠재적 편향성 등을 투명하게 문서화하여 제공하는 표준화된 모델 명세서"),
    "AI 영향 평가": ("AI Impact Assessment", "AI 시스템 도입 전에 정보 주체의 프라이버시 침해, 차별 등 사회적/윤리적 악영향을 사전 식별하고 그 파급 효과를 분석하여 완화 조치를 마련하는 사전 점검 절차"),
    "AI 윤리": ("AI Ethics", "AI 기술이 인간의 존엄성을 훼손하지 않고 공정, 안전, 투명하게 활용되도록 안내하는 도덕적 원칙과 가치 기준의 총체"),
    "프라이버시 보존형 AI": ("Privacy-preserving AI", "개인정보나 민감 데이터의 원본을 노출시키지 않으면서도 AI 모델을 학습하거나 추론할 수 있게 하여 데이터 활용과 프라이버시 보호를 동시에 달성하는 보안 기술"),
    "연합학습": ("Federated Learning", "원시 데이터를 중앙 서버로 전송하지 않고 각 로컬 디바이스에서 개별적으로 모델을 학습시킨 후, 그 가중치 업데이트(Gradient)만을 중앙으로 모아 전역 모델을 갱신하는 분산 기계학습 기법"),
    "보안 집계": ("Secure Aggregation", "연합학습 환경에서 개별 클라이언트의 가중치 업데이트 정보를 암호화하여 서버에 전달하고, 서버는 개별 데이터를 알 수 없는 상태에서 오직 전체 합(Aggregation)만을 복호화해내는 보안 기법"),
    "차분 프라이버시": ("Differential Privacy", "데이터베이스에 통계적 잡음(Noise)을 의도적으로 주입하여 특정 개인의 데이터 포함 여부를 수학적으로 추론할 수 없게 함으로써 프라이버시 누출을 방지하는 정형화된 모델링 기법"),
    "동형암호": ("Homomorphic Encryption", "데이터를 암호화한 상태(평문 복호화 없이)에서 덧셈이나 곱셈 등의 연산을 수행하고 그 결과를 복호화하면, 평문 상태에서 연산한 결과와 동일함을 보장하는 차세대 암호 기술"),
    "AI 레드팀": ("AI Red Teaming", "AI 시스템의 보안 취약점, 환각, 윤리적 위반 사항을 식별하기 위해 공격자 관점에서 시스템의 한계를 테스트하고 스트레스를 가하는 적대적 검증 활동"),
    "프롬프트 인젝션": ("Prompt Injection", "악의적인 사용자 입력(프롬프트)을 통해 LLM에 설정된 기존 보안 지침이나 윤리적 제약을 우회하고, 해커가 의도한 악성 명령을 실행하도록 조작하는 공격 기법"),
    "간접 프롬프트 인젝션": ("Indirect Prompt Injection", "웹페이지, 문서, 이메일 등 외부 데이터에 악의적인 프롬프트를 숨겨놓고, LLM이 이를 요약하거나 분석할 때 무의식적으로 악성 명령을 수행하도록 유도하는 지능형 공격"),
    "탈옥 공격": ("Jailbreak Attack", "LLM 개발자가 설정한 안전 필터(Safety Filter)나 정렬(Alignment) 규칙을 교묘한 역할극(Role-play)이나 가상의 시나리오를 통해 무력화시켜 금지된 콘텐츠를 생성하게 만드는 행위"),
    "모델 추출": ("Model Extraction", "타겟 AI 모델에 대량의 질의를 전송하고 그 예측 결과를 수집하여, 원본 모델의 기능, 가중치, 로직을 모방한 대체 모델(Substitute Model)을 복제해내는 지식 재산권 침해 공격"),
    "모델 역전": ("Model Inversion", "AI 모델의 출력(예측 결과)이나 가중치 정보를 역추적하여 모델 학습에 사용되었던 원본 학습 데이터(특히 개인정보, 얼굴 이미지 등)를 복원해내는 심각한 프라이버시 침해 공격"),
    "데이터 오염": ("Data Poisoning", "AI 모델의 학습 데이터 셋에 악의적으로 조작된 데이터를 주입하여 모델의 판단 기준을 왜곡시키고, 정상적인 환경에서 의도된 오작동을 유발하는 무결성 훼손 공격"),
    "백도어 공격": ("Backdoor Attack", "데이터 오염의 일종으로, 학습 데이터에 특정 트리거(Trigger)를 삽입하여 모델이 평소에는 정상 동작하다가 해당 트리거가 입력될 때만 공격자가 의도한 오분류를 수행하도록 만드는 은밀한 공격"),
    "적대적 예제": ("Adversarial Example", "인간의 눈에는 인식되지 않지만 AI 모델의 예측을 심각하게 방해하도록 미세한 노이즈(Perturbation)가 고의로 추가된 조작 데이터"),
    "모델 DoS": ("Model Denial of Service", "LLM과 같이 자원 소모가 큰 모델에 계산 복잡도가 극도로 높은 악의적 프롬프트를 지속적으로 전송하여 서버 자원을 고갈시키고 정상적인 서비스 제공을 방해하는 가용성 공격"),
    "OWASP LLM Top 10": ("OWASP LLM Top 10", "국제 웹 보안 기구인 OWASP에서 LLM 기반 애플리케이션 개발 시 발생할 수 있는 가장 치명적인 10대 보안 취약점과 대응 방안을 정리한 보안 가이드라인"),
    "LLM10 무제한 소비": ("LLM10: Unbounded Consumption", "LLM 서비스의 리소스 소비에 적절한 제한을 두지 않아 공격자의 반복적인 대규모 요청에 의해 과도한 인프라 비용(API 요금)이 청구되거나 서비스가 마비되는 취약점"),
    "C2PA": ("Coalition for Content Provenance and Authenticity", "디지털 콘텐츠(이미지, 비디오 등)의 생성 출처와 편집 이력 등 메타데이터를 암호화하여 기록함으로써 딥페이크와 허위 조작 정보를 판별하고 콘텐츠의 진위성을 검증하는 기술 표준"),
    "MLOps": ("Machine Learning Operations", "머신러닝 모델의 개발, 테스트, 배포, 모니터링에 이르는 전체 수명주기를 자동화하고 DevOps 프랙티스를 적용하여 안정적이고 지속적인 모델 운영을 가능하게 하는 협업 체계"),
    "LLMOps": ("Large Language Model Operations", "기존 MLOps를 확장하여 파운데이션 모델의 미세조정(Fine-tuning), 프롬프트 엔지니어링, RAG 파이프라인 관리, 비용 최적화 등을 지원하는 대형 언어 모델 특화 운영 체계"),
    "AIOps": ("Artificial Intelligence for IT Operations", "방대한 IT 운영 데이터(로그, 메트릭, 이벤트)에 머신러닝 알고리즘을 적용하여 시스템 장애를 사전 예측하고 근본 원인 분석(RCA) 및 자동 복구를 수행하는 지능형 IT 운영 기술"),
    "DataOps": ("Data Operations", "데이터 수집, 변환, 분석, 제공의 전 과정을 자동화하고 데이터 엔지니어, 데이터 과학자, 현업 부서 간의 협업을 촉진하여 고품질의 데이터를 민첩하게 공급하는 방법론"),
    "피처 스토어": ("Feature Store", "머신러닝 모델 학습 및 추론에 사용되는 특성(Feature) 데이터를 중앙 집중식으로 저장, 관리, 공유하여 중복 개발을 방지하고 일관된 데이터를 제공하는 인프라 구성요소"),
    "모델 레지스트리": ("Model Registry", "학습이 완료된 다양한 머신러닝 모델의 버전, 하이퍼파라미터, 메타데이터 및 아티팩트를 체계적으로 저장하고 배포 라이프사이클을 추적/관리하는 중앙 저장소"),
    "데이터 드리프트": ("Data Drift", "모델이 학습할 때 사용된 데이터의 통계적 분포와 실제 운영 환경(Production)에서 입력되는 데이터의 분포가 시간이 지남에 따라 달라져 모델의 예측 성능이 저하되는 현상"),
    "콘셉트 드리프트": ("Concept Drift", "입력 데이터와 정답 라벨(Target) 간의 맵핑 관계 자체가 변화하여, 과거에는 정답이었던 것이 현재는 오답이 됨으로써 모델의 근본적인 판단 기준이 무효화되는 현상"),
    "모델 드리프트": ("Model Drift", "데이터 드리프트와 콘셉트 드리프트 등의 원인으로 인해 배포된 머신러닝 모델의 예측 성능이 초기 학습 시점 대비 점진적 또는 급격하게 저하되는 포괄적인 현상"),
    "LLM-as-a-Judge": ("LLM-as-a-Judge", "성능이 검증된 강력한 대형 언어 모델(예: GPT-4)을 평가자로 활용하여, 다른 생성 모델의 출력 결과물에 대해 유창성, 관련성, 정확성 등을 인간 수준의 직관으로 채점하는 평가 방법론"),
    "AI 슈퍼컴퓨팅": ("AI Supercomputing", "수천에서 수만 개의 고성능 GPU/TPU를 고대역폭 네트워크로 연결하여 초거대 파운데이션 모델의 분산 학습과 추론을 가속화하는 대규모 병렬 컴퓨팅 인프라"),
    "GPU 클러스터": ("GPU Cluster", "다수의 GPU 노드를 인피니밴드(InfiniBand)나 이더넷 기반의 고속 스위치로 연결하여 컴퓨팅 자원을 클러스터링함으로써 단일 머신으로 처리할 수 없는 초거대 AI 연산을 분산 처리하는 시스템"),
    "AI 가속기": ("AI Accelerator", "인공지능 모델의 학습 및 추론 연산(주로 행렬 곱셈)을 범용 CPU보다 압도적으로 빠르고 전력 효율적으로 처리하기 위해 특화된 전용 하드웨어(GPU, TPU, NPU 등)의 총칭"),
    "GPU": ("Graphics Processing Unit", "원래 그래픽 렌더링을 위해 개발되었으나, 수천 개의 산술 논리 연산 장치(ALU)를 바탕으로 한 강력한 병렬 처리 능력을 인정받아 딥러닝 연산의 핵심으로 자리 잡은 하드웨어"),
    "TPU": ("Tensor Processing Unit", "구글이 딥러닝의 핵심인 텐서(Tensor) 연산 및 대규모 행렬 곱셈 연산을 가속화하기 위해 맞춤형(ASIC)으로 자체 설계한 클라우드 기반 AI 전용 하드웨어"),
    "FPGA AI 가속": ("FPGA AI Acceleration", "현장 프로그래머블 게이트 어레이(FPGA)를 활용하여 AI 모델의 구조나 알고리즘 변경에 맞춰 하드웨어 논리 회로를 유연하게 재구성(Reconfigurable)함으로써 빠른 프로토타이핑과 저지연 연산을 제공하는 기술"),
    "ASIC AI 가속": ("ASIC AI Acceleration", "특정 AI 알고리즘이나 모델 구조에 연산 능력을 극대화하기 위해 하드웨어 칩을 목적에 맞게 고정 설계하여 제조함으로써 가장 뛰어난 전력 대비 성능(초고속, 저전력)을 제공하는 기술"),
    "HBM": ("High Bandwidth Memory", "여러 개의 D램(DRAM) 다이를 TSV(Through Silicon Via) 기술로 수직 적층하여 데이터 처리 병목(Memory Wall)을 해소하고 GPU에 초고속 대역폭을 제공하는 차세대 메모리 규격"),
    "PIM": ("Processing-In-Memory", "메모리 반도체 내부에 직접 연산기(Processor)를 통합하여, CPU와 메모리 간의 대규모 데이터 이동을 최소화함으로써 전력 소모를 줄이고 처리 속도를 비약적으로 향상시키는 지능형 메모리 기술"),
    "CXL": ("Compute Express Link", "CPU, GPU, 메모리 등 다양한 디바이스 간의 통신 대역폭을 확장하고 메모리를 유연하게 공유할 수 있도록 지원하는 PCIe 기반의 차세대 고속 인터커넥트 표준 규격"),
    "칩렛": ("Chiplet", "크고 복잡한 단일 칩(Monolithic)을 제조하는 대신, 여러 개의 작은 단위 칩(Chiplet)을 독립적으로 제조한 후 패키징 기술을 통해 하나의 반도체처럼 작동하도록 결합하는 고수율 제조 공법"),
    "뉴로모픽 컴퓨팅": ("Neuromorphic Computing", "인간 뇌의 신경망 구조(뉴런과 시냅스)와 비동기적 정보 처리 방식을 하드웨어적으로 모방하여 스파이크(Spike) 신호 기반으로 연산함으로써 초저전력 인지 컴퓨팅을 구현하는 기술"),
    "NVLink": ("NVLink", "엔비디아가 독자 개발한 고속 상호연결(Interconnect) 기술로, 기존 PCIe 대역폭의 한계를 극복하고 다중 GPU 간 또는 GPU와 CPU 간의 초당 수백 GB급 초고속 데이터 전송을 지원하는 기술")
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. details/summary block processing
        def repl_details(match):
            block = match.group(0)
            
            def repl_term(t_match):
                prefix = t_match.group(1) # `- **`
                term_raw = t_match.group(2) # `단어`
                suffix = t_match.group(3) # `**: `
                desc = t_match.group(4) # `설명`

                term_clean = term_raw.split('(')[0].strip()

                eng = ""
                better_desc = desc
                for k, v in terms_mapping.items():
                    if k in term_clean or term_clean in k:
                        eng = v[0]
                        better_desc = v[1]
                        break

                if eng and not re.search(r'[A-Za-z]', term_raw):
                    new_term = f"{term_clean}({eng}, 영어)"
                else:
                    new_term = term_raw

                # Expand some typical boring ends
                if not any(k in term_clean for k in terms_mapping.keys()):
                    better_desc = re.sub(r'(이다\.|말한다\.|의미한다\.|로 정의된다\.|을 말한다\.|임\.|함\.)$', ' 역할을 수행하는 핵심 기술 및 개념이다.', better_desc)
                else:
                    # if we have a better description, use it, but keeping the original intro might be risky. 
                    # Actually, the user asked to improve the definition. Let's just use the mapped one if it's better or append.
                    # Given mapped definitions are full definitions, we can just replace the whole desc for matched ones.
                    pass

                return f"{prefix}{new_term}{suffix}{better_desc}"

            block = re.sub(r'(- \*\*)(.+?)(\*\*(?:<[^>]+>)?:\s*)(.*)', repl_term, block)
            return block

        content = re.sub(r'<details>\s*<summary>핵심 용어</summary>[\s\S]*?</details>', repl_details, content)
        
        # 3. Body lists ending correction
        def repl_body_def(match):
            line = match.group(0)
            if re.search(r'(임|함|한다|이다)\.$', line):
                 line = re.sub(r'(임|함|한다|이다)\.$', r'하는 특징을 가짐.', line)
            return line
        content = re.sub(r'^- .+$', repl_body_def, content, flags=re.MULTILINE)

        # 4. Conclusion (한줄 요약) must end with noun phrase
        def repl_conclusion_summary(match):
            summary = match.group(1)
            summary = re.sub(r'(한다|이다|다|함|임|합니다|있습니다|확인한다|유지한다)\.?$', '', summary).strip()
            return f"#### 한줄 요약\n\n- {summary} 체계 적용 및 원칙 준수"

        parts = re.split(r'## Ⅶ\. 결론', content)
        if len(parts) == 2:
            conc = parts[1]
            conc = re.sub(r'#### 한줄 요약\n\n- (.*?)(?=\n|$)', repl_conclusion_summary, conc)
            content = parts[0] + "## Ⅶ. 결론" + conc

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Failed {filepath}: {e}")

files = []
if os.path.exists(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            try:
                num = int(filename.split('_')[0])
                if 76 <= num <= 150:
                    files.append(os.path.join(directory, filename))
            except:
                pass

for f in files:
    process_file(f)

print(f"Processed {len(files)} files.")
