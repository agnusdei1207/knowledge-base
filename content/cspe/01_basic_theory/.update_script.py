#!/usr/bin/env python3
"""
Batch update CSPE study notes:
1. Add 🔑 핵심 용어 정리 table after --- (after 핵심 인사이트) and before ## Ⅰ. 개요
2. Convert plain-text math to KaTeX LaTeX
"""
import re
import os

BASE = "/home/user/study/content/cspe/01_basic_theory"

# ─── Terminology tables ───────────────────────────────────────────
TERMS = {
    "061_boosting_xgboost.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 부스팅 (Boosting) | 약한 학습기를 순차적으로 결합해 이전 모델의 오차를 보완하는 앙상블 기법 | 오답 노트를 이어받아 틀린 문제만 집중 복습하는 학생들의 릴레이 |
| 잔차 (Residual) | 실제 정답값과 현재 모델 예측값의 차이 | 골프공이 홀컵까지 남은 거리 |
| 그래디언트 부스팅 (GBM) | 손실 함수의 음의 기울기(Gradient) 방향으로 잔차를 줄여가는 부스팅 알고리즘 | 언덕에서 가장 가파른 내리막길을 따라 내려가는 등산객 |
| XGBoost | GBM에 2차 미분·L1/L2 규제·병렬 처리를 추가한 극한 성능의 부스팅 프레임워크 | 터보 엔진과 브레이크를 동시에 장착한 레이싱카 |
| 학습률 (Shrinkage) | 새 나무의 기여를 줄여 과적합을 막는 브레이크 계수 | 서두르지 말고 천천히 걸어가라는 속도 제한 |
| 얼리 스토핑 (Early Stopping) | 검증 성능이 나빠지기 시작하면 학습을 조기 중단하는 기법 | 시험 점수가 더 이상 안 오를 때 공부를 멈추는 전략 |
| LightGBM / CatBoost | XGBoost의 속도·범주형 변수 처리를 개선한 차세대 부스팅 라이브러리 | XGBoost의 후계자들 — 더 빠르고 더 영리한 후배 |

""",
    "062_svm.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 서포트 벡터 (Support Vector) | 결정 경계에 가장 가까이 위치해 마진을 결정짓는 극소수 데이터 포인트 | 고속도로 양쪽 갓길의 가드레일 기둥 |
| 마진 (Margin) | 결정 경계와 서포트 벡터 사이의 최단 거리 | 고속도로의 중앙분리대 폭 |
| 초평면 (Hyperplane) | 고차원 공간에서 두 클래스를 분리하는 결정 경계면 | 사과와 오렌지를 나누는 투명 칸막이 |
| 커널 트릭 (Kernel Trick) | 데이터를 고차원으로 매핑하지 않고도 고차원 분리 효과를 내는 수학적 기법 | 2D 평면의 꼬인 데이터를 3D로 붕 띄워 칼로 자르는 마법 |
| 소프트 마진 (Soft Margin) | 약간의 오분류를 허용하여 과적합을 방지하는 유연한 경계 설정 | 규칙에 약간의 예외를 허용하는 관대한 심판 |
| 파라미터 $C$ | 오분류 허용도와 마진 폭 사이의 트레이드오프를 조절하는 하이퍼파라미터 | 엄격함과 관대함 사이의 다이얼 |

""",
    "063_knn.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| KNN (K-Nearest Neighbors) | 새 데이터와 가장 가까운 $K$개 이웃의 다수결로 분류/예측하는 알고리즘 | 전학생이 가장 친한 친구 $K$명에게 물어보는 다수결 |
| 게으른 학습 (Lazy Learning) | 학습 단계 없이 데이터를 암기만 하고, 추론 시 전수 거리 계산을 수행하는 방식 | 시험 전에 공부 안 하고 시험장에서 교과서를 다 펼쳐보는 학생 |
| 유클리드 거리 (Euclidean Distance) | 두 점 사이의 직선 거리를 구하는 가장 기본적인 거리 척도 | 두 점 사이에 자를 대고 잰 직선 길이 |
| 차원의 저주 (Curse of Dimensionality) | 피처(차원)가 늘어날수록 모든 데이터 간 거리가 비슷해져 분류 성능이 하락하는 현상 | 100차원 허공에서는 모든 별이 비슷한 거리에 있어 가까운 별을 구분 불가 |
| 정규화 (Normalization) | 변수들의 단위와 범위를 통일시켜 거리 계산의 편향을 제거하는 전처리 | 키(cm)와 체중(kg)을 같은 잣대로 통일하는 작업 |
| KD-Tree / Ball Tree | 공간을 분할하여 최근접 이웃 탐색을 고속화하는 인덱싱 자료구조 | 도서관 서가를 분류번호로 나눠 원하는 책을 빨리 찾는 시스템 |

""",
    "064_naive_bayes.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 베이즈 정리 (Bayes' Theorem) | 사전 확률과 우도를 결합해 사후 확률을 역추적하는 조건부 확률 공식 | 결과(증상)를 보고 원인(질병)의 확률을 거꾸로 추리하는 탐정 |
| 조건부 독립 (Conditional Independence) | 피처들이 주어진 클래스 하에서 서로 영향을 주지 않는다는 순진한(Naive) 가정 | 단어들이 서로 아무 상관 없이 독립적으로 나타난다는 억지 가정 |
| 사전 확률 (Prior) | 새 데이터 관찰 전에 이미 알고 있는 기본 확률 | 전체 메일 중 스팸 비율 — 새 메일을 보기도 전에 아는 기본값 |
| 우도 (Likelihood) | 특정 클래스에서 해당 피처가 나타날 확률 | 스팸 메일에서 '무료'라는 단어가 등장할 빈도 |
| 라플라스 스무딩 (Laplace Smoothing) | 한 번도 안 나온 단어의 확률을 0에서 미세 양수로 보정하는 기법 | 곱셈의 0 폭탄을 막기 위해 모든 카운트에 1을 더해주는 구급 처치 |
| 제로 확률 문제 (Zero Probability) | 미관측 단어 하나 때문에 전체 확률이 0으로 붕괴하는 곱셈의 치명적 버그 | 체인 하나만 끊어져도 전체 목걸이가 끊어지는 현상 |

""",
    "065_q_learning.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| Q-러닝 (Q-Learning) | 상태-행동 쌍의 가치(Q-value)를 시행착오로 업데이트하며 최적 정책을 학습하는 강화학습 알고리즘 | 미로에서 메모장에 점수를 적으며 최적 경로를 찾아가는 쥐 |
| Q-테이블 (Q-Table) | 모든 상태와 행동 조합에 대한 기대 보상값을 기록한 표 | 게임 공략집 — 각 상황에서 어느 방향이 최고 점수인지 적힌 표 |
| 할인 계수 ($\\gamma$) | 미래 보상의 현재 가치를 줄이는 0~1 사이의 계수 | 내일의 만 원보다 오늘의 만 원이 더 가치 있다는 시간 가치 |
| 탐험 vs 활용 (Exploration vs Exploitation) | 새로운 행동을 시도할지 vs 이미 아는 최선의 행동을 반복할지의 딜레마 | 아는 맛집만 갈지 vs 새 식당을 개척할지의 고민 |
| Epsilon-Greedy | 확률 $\\epsilon$으로 랜덤 탐험, $1-\\epsilon$으로 최적 활용을 수행하는 행동 선택 전략 | 10번 중 1번은 일부러 모험을 강제하는 규칙 |
| 벨만 방정식 (Bellman Equation) | 현재 Q-값을 즉시 보상 + 미래 최대 Q-값으로 재귀적으로 정의하는 핵심 수식 | "이 자리의 점수 = 당장의 보상 + 다음 최고 자리의 할인된 점수" |

""",
    "066_cryptography_symmetric_asymmetric.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 대칭키 암호 (Symmetric) | 암호화와 복호화에 동일한 비밀키 1개를 사용하는 암호 방식 | 같은 열쇠로 잠그고 여는 자물쇠 |
| 비대칭키 암호 (Asymmetric) | 공개키로 암호화하고 개인키로만 복호화하는 키 쌍 기반 암호 방식 | 누구나 넣을 수 있지만 주인만 열 수 있는 우체통 |
| 키 분배 문제 (Key Distribution) | 대칭키를 도청 위험 없이 상대에게 전달하는 난제 | 비밀 열쇠를 택배로 보낼 때 도둑 맞을 위험 |
| RSA | 큰 소수의 인수분해 난이도에 기반한 대표적 비대칭키 알고리즘 | 두 소수를 곱하긴 쉽지만 결과를 다시 쪼개긴 우주적으로 어려운 수학적 자물쇠 |
| AES (Advanced Encryption Standard) | 미국 정부 표준 128/256비트 블록 대칭키 암호 알고리즘 | 현존 최강의 초고속 디지털 금고 |
| 하이브리드 암호화 (Hybrid) | 비대칭키로 대칭키를 안전하게 교환한 뒤, 대칭키로 데이터를 고속 암호화하는 실무 방식 | 택배 열쇠를 금고(비대칭키)로 보내고, 이후 그 열쇠(대칭키)로 문서를 잠그는 2단계 전략 |

""",
    "067_hash_functions.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 해시 함수 (Hash Function) | 임의 길이의 데이터를 고정 길이의 해시값(다이제스트)으로 변환하는 단방향 함수 | 어떤 과일이든 같은 크기 컵의 주스로 갈아버리는 믹서기 |
| 무결성 (Integrity) | 데이터가 전송·저장 중 변조되지 않았음을 보증하는 보안 속성 | 택배 봉인 스티커 — 뜯긴 흔적이 있으면 위조된 것 |
| 역상 저항성 (Pre-image Resistance) | 해시값으로부터 원본 데이터를 역추적할 수 없는 해시 함수의 핵심 성질 | 갈린 주스를 보고 원래 과일 모양을 복원할 수 없는 것 |
| 충돌 저항성 (Collision Resistance) | 서로 다른 두 입력이 같은 해시값을 가지지 않도록 보장하는 성질 | 지문이 겹치는 사람이 없어야 하는 원칙 |
| 눈사태 효과 (Avalanche Effect) | 입력이 1비트만 바뀌어도 출력 해시값이 50% 이상 완전히 달라지는 성질 | 편지 한 글자만 고쳐도 봉투 색깔이 완전히 바뀌는 마법 잉크 |
| 솔트 (Salt) | 비밀번호에 무작위 문자열을 덧붙여 레인보우 테이블 공격을 무력화하는 기법 | 같은 재료라도 소금을 다르게 넣으면 맛(해시값)이 완전히 달라지는 요리법 |

""",
    "068_digital_signature_pki.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 디지털 서명 (Digital Signature) | 송신자가 개인키로 해시값을 암호화하여 인증·무결성·부인 방지를 증명하는 기술 | 서류에 찍는 인감도장 — 본인만 소유한 도장으로 서명 |
| PKI (공개키 기반 구조) | 공개키의 진위를 제3자(CA)가 보증하는 인증서 발급·관리 인프라 | 동사무소(CA)가 "이 도장은 진짜 이 사람 것"이라고 보증서를 써주는 시스템 |
| CA (인증 기관) | 공개키와 소유자의 신원을 검증하고 디지털 인증서를 발급하는 신뢰 기관 | 여권을 발급해주는 정부 기관 |
| 부인 방지 (Non-repudiation) | 서명자가 나중에 "나 안 했어"라고 부인할 수 없게 만드는 보안 속성 | 자필 서명이 있으니 발뺌 불가능한 계약서 |
| X.509 인증서 | 공개키·소유자 정보·CA 서명을 담은 국제 표준 전자 신분증 포맷 | 사진·이름·관청 직인이 찍힌 신분증 |
| MITM (중간자 공격) | 해커가 통신 중간에 끼어들어 가짜 공개키를 주입하는 공격 | 우편함의 열쇠를 해커가 몰래 바꿔치기하는 사기 |

""",
    "069_tls_ssl_handshake.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| TLS (Transport Layer Security) | 전송 계층에서 암호화·인증·무결성을 제공하는 보안 프로토콜 (SSL의 후속 표준) | 인터넷 통신 전체를 감싸는 투명한 방탄 유리관 |
| 핸드셰이크 (Handshake) | 클라이언트와 서버가 암호 방식 협상, 인증서 검증, 대칭키 교환을 수행하는 초기 협상 과정 | 통화 전 서로 비밀 암호를 정하는 전초 인사 |
| 사이퍼 수트 (Cipher Suite) | 핸드셰이크에서 합의하는 암호화·해시·키 교환 알고리즘의 조합 메뉴 | "우리 무슨 암호 조합으로 통신할까?"를 정하는 메뉴판 |
| 세션키 (Session Key) | 핸드셰이크 후 생성된 일회용 대칭키로, 실제 데이터 암호화에 사용 | 통화할 때만 쓰고 버리는 1회용 비밀 열쇠 |
| PFS (Perfect Forward Secrecy) | 마스터키가 훗날 유출되어도 과거 통신이 복호화되지 않도록 보장하는 속성 | 이번 통화 열쇠는 다음 통화에 절대 재활용하지 않는 원칙 |
| SSL 오프로딩 (Offloading) | TLS 암복호화를 WAS가 아닌 전방 프록시/로드밸런서에서 전담 처리하는 설계 | 보안 검색대를 가게 입구가 아니라 쇼핑몰 정문에서 통합 운영하는 것 |

""",
    "070_ipsec_vpn.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| IPsec | IP 네트워크 계층(L3)에서 패킷의 인증·암호화·무결성을 제공하는 프로토콜 스위트 | IP 패킷 자체를 강철 금고에 넣어 보내는 네트워크 계층 보안 |
| VPN (가상 사설망) | 공용 인터넷 위에 암호화 터널을 뚫어 마치 전용선처럼 사용하는 가상 네트워크 | 고속도로(인터넷) 밑에 몰래 뚫은 비밀 지하 터널 |
| 전송 모드 (Transport Mode) | IP 헤더는 유지하고 페이로드(데이터)만 암호화하는 IPsec 모드 | 편지 내용만 잠그고 봉투 겉면(주소)은 보이게 두는 방식 |
| 터널 모드 (Tunnel Mode) | 원래 IP 헤더까지 통째로 암호화하고 새 IP 헤더를 덧씌우는 IPsec 모드 | 편지를 금고에 넣고 금고에 새 주소표를 붙여 보내는 완전 은닉 |
| ESP (Encapsulating Security Payload) | 데이터 암호화(기밀성)와 인증을 동시에 수행하는 IPsec의 핵심 프로토콜 | 내용물을 숨기면서 동시에 봉인 스티커까지 붙이는 이중 포장 |
| NAT-Traversal (NAT-T) | NAT 환경에서 IPsec 패킷이 차단되지 않도록 UDP로 한 번 더 감싸는 우회 기법 | 검문소를 무사히 통과하기 위해 군복 위에 민간인 옷을 걸치는 위장술 |

""",
    "071_firewall_ids_ips.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 방화벽 (Firewall) | IP/Port 기반 규칙으로 네트워크 트래픽의 출입을 통제하는 L3/L4 보안 장비 | 신분증(IP)과 나이(Port)만 보고 출입을 허가/거부하는 성문 수위 |
| IDS (침입 탐지 시스템) | 패킷 내용을 분석해 해킹 패턴을 탐지하고 관리자에게 경보하는 수동 보안 시스템 | 도둑을 발견하면 사이렌만 울리는 CCTV |
| IPS (침입 방지 시스템) | 해킹 패턴을 탐지하는 즉시 패킷을 차단하는 능동 보안 시스템 | 도둑을 보자마자 몽둥이로 패서 내쫓는 무장 경비원 |
| DPI (Deep Packet Inspection) | 패킷의 헤더뿐 아니라 내용물(Payload)까지 뜯어보는 심층 패킷 분석 기술 | 택배 상자 겉면뿐 아니라 안에 든 물건까지 검사하는 세관 |
| NGFW (차세대 방화벽) | 방화벽+IPS+앱 식별+VPN 등을 한 장비에 통합한 차세대 보안 플랫폼 | 경비·CCTV·금속탐지기를 한 몸에 합체한 올인원 경비 로봇 |
| 시그니처 기반 탐지 | 알려진 해킹 패턴(지문) DB와 대조하여 공격을 식별하는 방식 | 수배 전단지와 얼굴을 대조해 범인을 잡는 방식 |

""",
    "072_ddos_attacks.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| DDoS (분산 서비스 거부) | 수만 대의 좀비 PC가 동시에 타깃 서버에 쓰레기 트래픽을 쏟아붓는 가용성 파괴 공격 | 1만 명의 가짜 손님이 식당을 점거해 진짜 손님이 못 들어오게 하는 물량 공격 |
| 봇넷 (Botnet) | 해커가 악성코드로 감염시켜 원격 조종하는 수만~수십만 대의 좀비 기기 네트워크 | 해커의 명령에 일제히 움직이는 좀비 군단 |
| SYN Flooding | TCP 3-Way Handshake의 SYN만 보내고 완료하지 않아 서버 자원을 고갈시키는 공격 | "안녕" 인사만 10만 번 하고 도망가 서버가 자리만 비워두다 터지는 공격 |
| DRDoS (반사 증폭 공격) | 출발지 IP를 위조해 정상 서버(DNS 등)의 응답을 타깃에 반사시키는 증폭형 공격 | 답장 주소를 타깃으로 위조해 우체국들이 대량 답장을 타깃에 쏟아붓게 만드는 꼼수 |
| 스크러빙 센터 (Scrubbing Center) | 클라우드에서 악성 트래픽을 걸러내고 정상 트래픽만 통과시키는 대규모 세탁 시설 | 오염된 강물을 정수장에서 걸러 깨끗한 물만 집으로 보내는 시설 |
| 블랙홀 라우팅 (Null Routing) | 방어 불가능한 트래픽을 가상 휴지통으로 버려 나머지 인프라를 보호하는 최후 수단 | 둑이 터질 위기에 한쪽 수문을 열어 희생시키는 꼬리 자르기 |

""",
    "073_xss_csrf_sql_injection.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| XSS (Cross-Site Scripting) | 웹 페이지에 악성 자바스크립트를 삽입해 타 사용자의 브라우저에서 실행시키는 공격 | 게시판에 투명 요정을 숨겨두어 클릭한 사람의 열쇠(쿠키)를 훔치는 수법 |
| CSRF (Cross-Site Request Forgery) | 로그인 된 사용자의 권한을 도용해 원치 않는 요청을 서버에 보내는 공격 | 사용자 손을 강제로 잡고 송금 서류에 도장을 찍게 만드는 사기 |
| SQL Injection | 입력 필드에 조작된 SQL 쿼리를 삽입해 DB를 무단 조회·조작하는 공격 | 아이디 칸에 "금고 비밀번호 검사 무시하고 열어라"라는 주문을 써넣는 최면술 |
| Prepared Statement | 쿼리 뼈대를 미리 컴파일하고 입력값을 변수로만 바인딩하는 SQLi 방어 기법 | 서류 양식을 미리 인쇄해두고 빈칸에만 글씨를 쓰게 해 위조를 원천 차단 |
| 이스케이프 (Escape) | 특수 문자를 무해한 문자로 치환하여 코드 실행을 방지하는 입력 소독 기법 | 위험 물질을 무해한 물질로 중화시키는 화학적 소독 |
| WAF (웹 방화벽) | L7 계층에서 웹 공격 패턴을 탐지·차단하는 전문 방화벽 | 웹 전용 보안 검색대 — 위험한 패턴의 택배를 문 앞에서 컷 |

""",
    "074_zero_trust_architecture.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 제로 트러스트 (Zero Trust) | "내부든 외부든 아무도 믿지 말고 매번 검증하라"는 현대 사이버 보안 철학 | 성 안의 모든 문마다 신분증 검사를 하는 초경계 보안 |
| 마이크로 세그멘테이션 | 내부 네트워크를 서버·앱 단위로 잘게 쪼개 횡적 이동을 차단하는 기법 | 성 안의 모든 방마다 별도의 자물쇠를 다는 구조 |
| 횡적 이동 (Lateral Movement) | 내부 네트워크에 침투한 해커가 다른 서버로 수평 확산하는 공격 패턴 | 한 방을 털고 복도를 통해 옆방으로 넘어가는 도둑 |
| 최소 권한 (Least Privilege) | 업무 수행에 딱 필요한 최소한의 접근 권한만 부여하는 원칙 | 인턴에게 전체 금고 열쇠가 아닌 자기 서랍 열쇠만 주는 것 |
| MFA (다중 인증) | 비밀번호 외에 생체·OTP 등 2가지 이상 인증 요소를 요구하는 인증 방식 | 열쇠(비번)와 지문(생체)을 동시에 대야 문이 열리는 이중 잠금 |
| SDP (Software Defined Perimeter) | 인증 전까지 서버를 인터넷에서 완전히 숨기는 제로 트러스트 핵심 구현 기술 | 신분증을 보여줘야만 비로소 가게 입구가 나타나는 은닉 마법 |

""",
    "075_turing_machine_halting_problem.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 튜링 기계 (Turing Machine) | 무한 테이프·읽기/쓰기 헤드·유한 상태 제어기로 구성된 수학적 계산 모델 | 끝없는 두루마리에 연필로 0과 1을 적으며 모든 계산을 해내는 기계 팔 |
| 정지 문제 (Halting Problem) | 임의의 프로그램이 주어진 입력에 대해 종료할지 무한 루프에 빠질지 판별하는 것이 불가능하다는 증명 | "이 프로그램이 끝날지 안 끝날지 미리 맞히는 마법 구슬은 존재할 수 없다" |
| 귀류법 (Proof by Contradiction) | 명제를 거짓이라 가정하고 모순을 도출하여 원래 명제가 참임을 증명하는 논증법 | "만약 할 수 있다고 가정하면 자기 모순에 빠지니, 불가능하다" |
| 보편 튜링 기계 (UTM) | 다른 모든 튜링 기계의 동작을 시뮬레이션할 수 있는 범용 튜링 기계 | 어떤 소프트웨어든 실행하는 범용 컴퓨터의 수학적 조상 |
| 처치-튜링 명제 | 인간이 규칙적으로 계산 가능한 모든 문제는 튜링 기계로도 풀 수 있다는 가설 | "사람이 종이와 연필로 풀 수 있는 문제 = 컴퓨터로 풀 수 있는 문제" |
| 결정 불가능성 (Undecidability) | 어떤 알고리즘으로도 참/거짓을 판정할 수 없는 문제 카테고리 | 아무리 똑똑한 컴퓨터도 영원히 답을 못 내는 질문들의 금지 구역 |

""",
    "076_p_vs_np_problem.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| P 클래스 | 결정론적 튜링 기계로 다항 시간 $O(N^k)$ 내에 풀 수 있는 문제 집합 | 착한 문제 — 공식만 쓰면 합리적 시간 안에 정답이 나오는 시험 문제 |
| NP 클래스 | 정답이 주어지면 다항 시간 내에 검증할 수 있는 문제 집합 | 풀긴 개어려운데, 답안지를 가져오면 1초 만에 채점 가능한 문제 |
| NP-완전 (NP-Complete) | NP 문제 중 가장 어려운 대장급 문제로, 하나만 P로 풀리면 모든 NP가 풀림 | 보스 몬스터 — 이 한 놈만 잡으면 나머지 몬스터가 줄줄이 쓰러짐 |
| NP-난해 (NP-Hard) | NP-완전 이상의 난이도로, 검증조차 다항 시간에 안 될 수 있는 극악 문제 | 정답 확인조차 불가능한 궁극의 난제 |
| 다항 시간 (Polynomial Time) | $O(N^2)$, $O(N^3)$ 등 입력 크기에 비해 적당히 증가하는 연산 시간 | 참을 만한 시간 — 데이터가 늘어도 적당히 느려지는 정도 |
| 휴리스틱 (Heuristic) | NP 문제에 대해 완벽한 정답 대신 빠른 시간 안에 꽤 좋은 근사해를 구하는 전략 | "100점은 포기하고 95점을 1분 만에 내자"는 현실적 타협 |

""",
    "077_von_neumann_architecture.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 폰 노이만 구조 | 프로그램과 데이터를 동일한 메모리에 저장하고 CPU가 순차 실행하는 컴퓨터 아키텍처 | 요리책(프로그램)과 재료(데이터)를 같은 서랍에 넣고 요리사가 꺼내 쓰는 구조 |
| 내장형 프로그램 (Stored Program) | 소프트웨어를 하드웨어 변경 없이 메모리에 적재하여 실행하는 핵심 개념 | 기계를 뜯지 않고 요리법 종이만 바꿔 만능 요리 기계로 쓰는 아이디어 |
| 폰 노이만 병목 (Bottleneck) | CPU와 메모리 사이의 좁은 버스 공유로 데이터 전송 속도가 제한되는 현상 | 왕복 1차선 도로에 수천 대 차가 몰려 정체되는 교통 병목 |
| 시스템 버스 (Bus) | CPU·메모리·I/O 사이에서 데이터·주소·제어 신호를 전달하는 통신 통로 | CPU와 메모리를 잇는 좁은 고속도로 |
| 하버드 구조 | 명령어 메모리와 데이터 메모리를 분리하여 동시 접근을 가능하게 한 아키텍처 | 요리책 서랍과 재료 서랍을 따로 두어 동시에 꺼낼 수 있는 구조 |
| 캐시 메모리 (Cache) | CPU와 RAM 사이의 속도 격차를 줄이기 위해 배치된 초고속 SRAM 버퍼 | CPU 바로 옆에 둔 미니 냉장고 — 자주 쓰는 재료를 꺼내기 쉽게 보관 |

""",
    "078_cpu_scheduling.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| CPU 스케줄링 | 준비 큐의 프로세스들에게 CPU 시간을 배분하는 운영체제의 핵심 교통정리 알고리즘 | 장난감 1대를 유치원생 10명에게 공평하게 나눠주는 선생님의 규칙 |
| 선점형 (Preemptive) | 실행 중인 프로세스를 강제로 중단시키고 다른 프로세스에 CPU를 넘기는 방식 | 시간이 되면 무조건 다음 사람에게 차례를 넘기는 규칙 |
| 라운드 로빈 (Round Robin) | 정해진 시간 할당량(Time Quantum)만큼 돌아가며 CPU를 사용하는 선점형 스케줄링 | 1분씩 정확히 돌아가며 장난감을 쓰는 공평한 시분할 |
| 문맥 교환 (Context Switching) | CPU가 프로세스를 교체할 때 현재 상태를 저장하고 다음 상태를 복원하는 오버헤드 작업 | 장난감을 넘길 때 "어디까지 했는지" 메모를 적고 넘겨받는 사람이 이어하는 과정 |
| 기아 현상 (Starvation) | 우선순위가 낮은 프로세스가 CPU를 영원히 배정받지 못하는 현상 | 줄 맨 뒤에서 새치기 당하며 영원히 밥을 못 먹는 사람 |
| 에이징 (Aging) | 오래 기다린 프로세스의 우선순위를 점진적으로 올려 기아를 방지하는 기법 | 줄을 오래 선 사람의 번호표 순위를 자동으로 올려주는 배려 |

""",
    "079_virtual_memory_paging.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 가상 메모리 (Virtual Memory) | 물리 RAM보다 큰 메모리 공간을 디스크를 활용해 가상으로 제공하는 OS 기술 | 작은 책상에 창고를 연결해 무한한 작업 공간처럼 쓰는 마법 |
| 페이징 (Paging) | 가상·물리 메모리를 고정 크기(4KB 등) 블록으로 잘라 불연속 적재하는 기법 | 책을 4쪽씩 찢어 책상 빈칸에 퍼즐처럼 끼우는 방식 |
| 페이지 테이블 (Page Table) | 가상 주소를 물리 주소로 변환하는 매핑 정보를 담은 주소록 | "1번 페이지 → RAM 3번 프레임"이라고 적힌 번역 사전 |
| 페이지 부재 (Page Fault) | CPU가 요청한 페이지가 RAM에 없어 디스크에서 가져와야 하는 이벤트 | 책상에 필요한 종이가 없어 창고까지 허겁지겁 달려가야 하는 상황 |
| TLB (Translation Lookaside Buffer) | 최근 주소 변환 결과를 캐싱하는 MMU 내부의 초고속 하드웨어 캐시 | 방금 찾아본 주소를 포스트잇에 적어두어 사전을 다시 안 펼쳐도 되는 속도 꼼수 |
| 스래싱 (Thrashing) | RAM 부족으로 페이지 교체가 과도하게 반복되어 CPU가 일 못하고 멈추는 현상 | 책상과 창고를 쉴 새 없이 왕복하다가 정작 일은 한 줄도 못 하는 재앙 |

""",
    "080_quantum_algorithm_shor_grover.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 쇼어 알고리즘 (Shor's Algorithm) | 양자 푸리에 변환을 이용해 큰 수의 소인수분해를 다항 시간 $O(N^3)$에 수행하는 양자 알고리즘 | RSA 금고의 자물쇠(소수 곱)를 양자 마법으로 수초 만에 박살 내는 해킹 무기 |
| 그로버 알고리즘 (Grover's Algorithm) | 비정렬 데이터에서 목표값을 $O(\\sqrt{N})$에 찾는 양자 탐색 알고리즘 | $N$개 상자에서 열쇠를 $\\sqrt{N}$번만에 찾아내는 양자 돋보기 |
| 큐비트 (Qubit) | 0과 1을 확률적으로 동시에 표현하는 양자 정보의 기본 단위 | 앞면과 뒷면이 동시에 존재하는 핑그르르 돌고 있는 동전 |
| 양자 중첩 (Superposition) | 하나의 큐비트가 0과 1의 상태를 동시에 가지는 양자역학 성질 | 관찰하기 전까지 모든 가능성이 겹쳐 있는 슈뢰딩거의 고양이 |
| 양자 얽힘 (Entanglement) | 두 큐비트가 물리적 거리와 무관하게 상태가 즉시 연동되는 양자 현상 | 한 동전이 앞면이면 우주 반대편 동전도 즉시 뒷면으로 확정되는 텔레파시 |
| NISQ (Noisy Intermediate-Scale Quantum) | 현재 수준의 노이즈가 많고 큐비트 수가 제한된 양자 컴퓨터 시대 | 아직 삐걱대고 오류가 많은 양자 컴퓨터의 사춘기 시대 |

""",
    "009_binary_tree_traversal.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 전위 순회 (Pre-order) | 부모 → 왼쪽 → 오른쪽 순서로 방문하는 트리 순회 방식 | 대장이 먼저 출발하고 부하들이 따라가는 선발대 탐색 |
| 중위 순회 (In-order) | 왼쪽 → 부모 → 오른쪽 순서로 방문하며, BST에서는 정렬 순서를 출력 | 사전에서 가나다순(작은 것→큰 것)으로 읽는 것 |
| 후위 순회 (Post-order) | 왼쪽 → 오른쪽 → 부모 순서로 방문하며, 자식을 먼저 처리해야 하는 문제에 적합 | 부하들이 일을 다 끝낸 후 대장이 최종 결산하는 순서 |
| 레벨 순회 (Level-order) | BFS 방식으로 같은 깊이의 노드를 왼쪽에서 오른쪽으로 층별 방문 | 건물을 1층부터 꼭대기까지 한 층씩 올라가며 방 검사 |
| Morris Traversal | 스레디드 링크를 임시 생성하여 $O(1)$ 공간에서 순회하는 기법 | 미로 바닥에 화살표를 그려놓고 나중에 지우는 공간 절약 탐색법 |
| 파스 트리 (Parse Tree) | 유도 과정을 트리로 시각화한 구조로, 순회의 대상 | 문장의 문법 구조를 가계도처럼 펼쳐놓은 나무 |

""",
    "010_graph_traversal.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| BFS (너비 우선 탐색) | 큐를 사용해 시작점에서 가까운 정점부터 층별로 방문하는 그래프 탐색 알고리즘 | 연못에 돌을 던졌을 때 동심원으로 퍼지는 파문 |
| DFS (깊이 우선 탐색) | 스택/재귀를 사용해 한 경로를 끝까지 파고든 후 되돌아오는 그래프 탐색 알고리즘 | 미로에서 한 길을 끝까지 가보고 막히면 돌아오는 탐험가 |
| 방문 배열 (visited) | 각 정점의 방문 여부를 기록해 무한 루프를 방지하는 필수 자료구조 | 갈림길마다 빵 부스러기를 뿌려 이미 온 길인지 확인하는 장치 |
| 역방향 간선 (Back Edge) | DFS 중 조상 정점으로 향하는 간선으로, 사이클 존재의 증거 | 가계도에서 손자가 할아버지를 가리키면 순환 관계가 있다는 증거 |
| 위상 정렬 (Topological Sort) | DAG에서 의존 관계를 만족하는 선형 순서를 구하는 알고리즘 (DFS 후위 역순) | 빌드 순서 — 라이브러리 A가 B에 의존하면 A를 먼저 빌드하는 규칙 |
| 시간 복잡도 $O(V+E)$ | 정점 수 $V$와 간선 수 $E$에 비례하는 BFS/DFS의 수행 시간 | 모든 방(정점)과 복도(간선)를 딱 한 번씩 통과하는 효율 |

""",
    "022_context_free_grammar.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 문맥 자유 문법 (CFG) | 생성 규칙의 좌변이 단일 비단말 기호 하나($A \\to \\alpha$)로 구성된 촘스키 Type 2 형식 문법 | 주변 문맥과 무관하게 어디서든 같은 규칙으로 조립하는 레고 설명서 |
| 비단말 기호 (Non-terminal) | 파생 중간 단계의 추상 범주로, 생성 규칙에 의해 다른 기호열로 치환됨 | 레고 완성품 속의 '서브 어셈블리' — 더 잘게 분해 가능한 중간 부품 |
| 파스 트리 (Parse Tree) | 시작 기호에서 최종 문자열까지의 유도 과정을 트리로 시각화한 구조 | 문장의 구조를 가계도처럼 계층적으로 펼쳐 보여주는 족보 |
| 푸시다운 오토마타 (PDA) | 유한 오토마타에 스택을 추가해 CFG가 정의하는 언어를 인식하는 추상 기계 | 접시를 쌓았다(push) 빼는(pop) 카운터로 괄호 짝을 검증하는 기계 |
| BNF/EBNF | CFG를 실무적으로 표기하는 표준 표기법으로, 프로그래밍 언어 구문 정의에 사용 | 프로그래밍 언어의 문법 규칙을 적어놓은 공식 레시피 문서 |
| LL/LR 파서 | CFG 규칙을 $O(N)$ 시간에 파싱하는 결정론적 구문 분석 알고리즘 | 목차 먼저 보고 읽는(LL) vs 단어를 읽으며 문장을 완성하는(LR) 독서법 |

""",
    "023_turing_machine.md": """
## 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| 튜링 머신 (Turing Machine) | 무한 테이프·읽기/쓰기 헤드·유한 상태 제어기로 구성된 최초의 수학적 범용 계산 모델 | 무한히 긴 줄노트 위에서 규칙표만 보고 연필로 한 칸씩 계산하는 사람 |
| 전이 함수 ($\\delta$) | 현재 상태와 읽은 기호로부터 (새 상태, 쓸 기호, 이동 방향)을 결정하는 계산 규칙 | CPU의 명령어 디코더 — "이 상황에서는 이렇게 해라"는 규칙표 |
| 범용 튜링 머신 (UTM) | 다른 모든 TM의 인코딩을 입력받아 시뮬레이션하는 메타 튜링 머신 | 어떤 프로그램이든 실행하는 범용 컴퓨터의 수학적 원형 |
| 정지 문제 (Halting Problem) | 임의의 프로그램과 입력에 대해 정지 여부를 판정하는 일반 알고리즘은 존재하지 않는다는 증명 | "이 프로그램이 끝날지 무한루프인지" 미리 맞히는 수정구슬은 수학적으로 불가능 |
| 처치-튜링 논제 (Church-Turing Thesis) | 효과적으로 계산 가능한 함수 = 튜링 머신이 계산할 수 있는 함수라는 등가 명제 | 사람이 종이와 연필로 풀 수 있으면 컴퓨터로도 풀 수 있다는 대원칙 |
| 촘스키 계층 (Chomsky Hierarchy) | 형식 문법의 생성력과 오토마타의 계산 능력을 4단계(Type 0~3)로 분류한 체계 | FA(1층) → PDA(2층) → LBA(3층) → TM(최상층)으로 올라갈수록 더 많은 문제를 풀 수 있는 계산 능력의 건물 |

""",
}

def insert_term_table(content, filename):
    """Insert the terminology table after first --- separator and before ## Ⅰ. 개요"""
    table = TERMS.get(filename)
    if not table:
        return content

    # Find the pattern: "---\n\n## Ⅰ." after the 핵심 인사이트 section
    # We want to insert after the first "---" that comes after "핵심 인사이트"
    
    # Find 핵심 인사이트 section
    insight_idx = content.find("핵심 인사이트")
    if insight_idx == -1:
        # Try alternate pattern
        insight_idx = content.find("## 핵심 인사이트")
    if insight_idx == -1:
        return content
    
    # Find the --- after 핵심 인사이트
    separator_idx = content.find("\n---\n", insight_idx)
    if separator_idx == -1:
        return content
    
    # Find ## Ⅰ. after the separator
    section1_idx = content.find("## Ⅰ.", separator_idx)
    if section1_idx == -1:
        return content
    
    # Insert table between --- and ## Ⅰ.
    insert_point = separator_idx + len("\n---\n")
    
    before = content[:insert_point]
    after = content[insert_point:]
    
    # Remove any existing blank lines between --- and ## Ⅰ.
    # and replace with our table
    after = after.lstrip('\n')
    
    return before + table + after


def convert_math(content):
    """Convert plain-text math expressions to KaTeX. Carefully avoid double-conversion."""
    
    # Skip content inside code blocks
    # We'll split by code blocks, process only non-code parts
    parts = re.split(r'(```[\s\S]*?```)', content)
    
    result = []
    for i, part in enumerate(parts):
        if part.startswith('```'):
            result.append(part)
        else:
            result.append(_convert_math_text(part))
    
    return ''.join(result)


def _convert_math_text(text):
    """Convert math in regular text (not code blocks)."""
    
    # Don't touch text already inside $...$ or $$...$$
    # We'll process segments outside of existing LaTeX
    
    # Split by existing $...$ and $$...$$ blocks
    # Regex to find existing LaTeX: $$...$$ or $...$
    # We need to preserve these
    
    segments = []
    last_end = 0
    # Match $$...$$ first, then $...$
    for m in re.finditer(r'\$\$[\s\S]*?\$\$|\$[^$\n]+?\$', text):
        segments.append(('text', text[last_end:m.start()]))
        segments.append(('math', m.group()))
        last_end = m.end()
    segments.append(('text', text[last_end:]))
    
    converted = []
    for seg_type, seg_text in segments:
        if seg_type == 'math':
            converted.append(seg_text)
        else:
            converted.append(_do_math_conversions(seg_text))
    
    return ''.join(converted)


def _do_math_conversions(text):
    """Perform actual math text-to-KaTeX conversions on plain text."""
    
    # O(N), O(N^2), O(N^3), O(n log n), O(2^n), O(N!), O(e^{...}), O(n^{1/3}), O(V+E), etc.
    # Pattern: O(...)  but not already inside $...$
    def convert_big_o(m):
        inner = m.group(1)
        # Convert inner content
        inner = inner.replace('^', '^')
        return '$O(' + inner + ')$'
    
    # Match O(...) with balanced parentheses - simple version
    # Handle patterns like O(N), O(N^2), O(N^3), O(n log n), O(2^n), O(N!), O(V+E)
    text = re.sub(r'(?<!\$)O\(([^)]+)\)(?!\$)', lambda m: '$O(' + m.group(1) + ')$', text)
    
    # Fix O(N^2 \sim N^3) pattern  
    text = re.sub(r'(?<!\$)O\(([^)]*\\sim[^)]*)\)(?!\$)', lambda m: '$O(' + m.group(1) + ')$', text)
    
    # Ω(...) 
    text = re.sub(r'(?<!\$)Ω\(([^)]+)\)(?!\$)', lambda m: '$\\Omega(' + m.group(1) + ')$', text)
    
    # Θ(...)
    text = re.sub(r'(?<!\$)Θ\(([^)]+)\)(?!\$)', lambda m: '$\\Theta(' + m.group(1) + ')$', text)
    
    return text


def process_file(filename):
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Insert terminology table
    content = insert_term_table(content, filename)
    
    # 2. Convert math expressions
    content = convert_math(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Count lines
    lines = content.count('\n') + (0 if content.endswith('\n') else 1)
    print(f"✅ {filename} — {lines} lines")


FILES = [
    "061_boosting_xgboost.md",
    "062_svm.md", 
    "063_knn.md",
    "064_naive_bayes.md",
    "065_q_learning.md",
    "066_cryptography_symmetric_asymmetric.md",
    "067_hash_functions.md",
    "068_digital_signature_pki.md",
    "069_tls_ssl_handshake.md",
    "070_ipsec_vpn.md",
    "071_firewall_ids_ips.md",
    "072_ddos_attacks.md",
    "073_xss_csrf_sql_injection.md",
    "074_zero_trust_architecture.md",
    "075_turing_machine_halting_problem.md",
    "076_p_vs_np_problem.md",
    "077_von_neumann_architecture.md",
    "078_cpu_scheduling.md",
    "079_virtual_memory_paging.md",
    "080_quantum_algorithm_shor_grover.md",
    "009_binary_tree_traversal.md",
    "010_graph_traversal.md",
    "022_context_free_grammar.md",
    "023_turing_machine.md",
]

if __name__ == "__main__":
    for f in FILES:
        try:
            process_file(f)
        except Exception as e:
            print(f"❌ {f} — ERROR: {e}")
    print(f"\nDone! Processed {len(FILES)} files.")
