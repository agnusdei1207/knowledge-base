+++
title = "040. AMI / Pseudoternary (교류 마크 반전 / 의사 삼진 부호)"
date = 2026-03-30

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

> **핵심 인사이트**
> 1. [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/)(Alternate Mark Inversion, 교류 마크 반전)는 0을 0전압, 1을 +V와 -V 교번()으로 표현하는 삼진 부호 방식으로, DC 성분 제거와 단일 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [오류 탐지](/knowledge-base/studynote/02_operating_system/01_overview_architecture/040_error_detection/)(연속 동극성 위반 검출)라는 두 가지 효과를 동시에 달성한다.
> 2. Pseudoternary(의사 삼진 부호)는 AMI의 역() — 1을 0전압, 0을 ±V 교번으로 표현하며, 동일한 수학적 특성을 가지지만 1이 많은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 환경에서 유리하다.
> 3. [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/) 계열 라인 코딩은 ISDN BRI(기본 속도 인터페이스) 표준 코딩으로 채택됐으며, 이후 B8ZS·HDB3 등 연속 0 처리 개선 버전으로 발전하여 E1/T1 디지털 전화망의 기반이 됐다.

---

## Ⅰ. 라인 코딩 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

```
라인 코딩 (Line Coding) 분류:

단극성 (Unipolar):
0: 0V / 1: +5V
DC 성분 있음, 간단하지만 실용성 낮음

양극성 (Bipolar):
세 가지 전압 레벨 사용 (0, +V, -V)
AMI, Pseudoternary 포함

이극성 (Bipolar) 아닌 NRZ/RZ:
NRZ-L: 레벨로 인코딩
NRZ-I: 전이(Transition)로 인코딩
맨체스터: 클럭 내장

AMI vs Pseudoternary:
AMI: 0 = 0V, 1 = +V/-V 교번
Pseudoternary: 0 = +V/-V 교번, 1 = 0V
```

> 📢 **섹션 요약 비유**: 라인 코딩은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전선에 싣는 "언어 선택" — AMI는 1을 번갈아 +/-로 말하는 특별한 언어.

---

## Ⅱ. [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/) 인코딩 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">AMI (Alternate Mark Inversion):</div>
<div class="kb-diagram-note">규칙:</div>
<div class="kb-diagram-note">비트 0 -&gt; 전압 0</div>
<div class="kb-diagram-note">비트 1 -&gt; 이전 1과 반대 극성 (+V or -V 교번)</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">데이터: 1 0 0 1 0 1 1 0 1</div>
<div class="kb-diagram-note">전압: +V 0 0 -V 0 +V -V 0 +V</div>
<div class="kb-diagram-note">파형:</div>
<div class="kb-diagram-note">+V _ _ _ _ _</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0</div><div class="kb-diagram-cell">_____</div><div class="kb-diagram-cell">_____</div><div class="kb-diagram-cell">_____</div><div class="kb-diagram-cell">_</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">-V</div></div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">1. DC 성분 0: +V와 -V 교번 -&gt; 평균 0V</div>
<div class="kb-diagram-note">2. 오류 탐지: 연속 동극성 (예: +V 다음 +V) = 위반 신호</div>
<div class="kb-diagram-note">3. 대역폭: NRZ-L 대비 낮은 주파수 성분</div>
</div>
</div>



> 📢 **섹션 요약 비유**: AMI는 1을 "위, 아래, 위, 아래"처럼 번갈아 전달하는 지그재그 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — 모두 같은 방향이면 오류 경보!

---

## Ⅲ. AMI의 한계와 개선: B8ZS, HDB3



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">AMI 한계:</div>
<div class="kb-diagram-note">연속 0이 많으면 전압 변동 없음</div>
<div class="kb-diagram-tree-item" style="--depth:0">수신기 동기(Clock Recovery) 어려움</div>
<div class="kb-diagram-tree-item" style="--depth:0">장거리 전송 시 타이밍 손실</div>
<div class="kb-diagram-note">B8ZS (Bipolar with 8 Zeros Substitution):</div>
<div class="kb-diagram-note">8개 연속 0 -&gt; 특수 패턴으로 치환</div>
<div class="kb-diagram-note">치환 패턴: 000+-0-+ (이전 펄스 +일 때)</div>
<div class="kb-diagram-note">000-+0+- (이전 펄스 -일 때)</div>
<div class="kb-diagram-note">북미 T1 (DS1, 1.544 Mbps)에 사용</div>
<div class="kb-diagram-note">HDB3 (High Density Bipolar 3):</div>
<div class="kb-diagram-note">4개 연속 0 -&gt; 특수 패턴 치환</div>
<div class="kb-diagram-note">유럽 E1 (2.048 Mbps)에 사용</div>
<div class="kb-diagram-note">비교:</div>
<div class="kb-diagram-note">AMI: 단순, 동기화 불안정</div>
<div class="kb-diagram-note">B8ZS: T1 표준, 8개 연속 0 처리</div>
<div class="kb-diagram-note">HDB3: E1 표준, 4개 연속 0 처리</div>
</div>
</div>



> 📢 **섹션 요약 비유**: B8ZS/HDB3는 오래 침묵하면 "가짜 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)"를 넣어 시계가 계속 돌아가게 유지하는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 도우미.

---

## Ⅳ. Pseudoternary



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Pseudoternary (의사 삼진 부호):</div>
<div class="kb-diagram-note">규칙 (AMI의 역):</div>
<div class="kb-diagram-note">비트 1 -&gt; 전압 0</div>
<div class="kb-diagram-note">비트 0 -&gt; 이전 0과 반대 극성 교번</div>
<div class="kb-diagram-note">예시:</div>
<div class="kb-diagram-note">데이터: 1 0 0 1 0 1 1 0 1</div>
<div class="kb-diagram-note">전압: 0 +V -V 0 +V 0 0 -V 0</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">AMI와 동일한 DC 0, 오류 탐지 특성</div>
<div class="kb-diagram-note">0이 많은 데이터에서 더 많은 전압 변동</div>
<div class="kb-diagram-tree-item" style="--depth:0">동기화 유리</div>
<div class="kb-diagram-note">ISDN BRI (Basic Rate Interface) 사용:</div>
<div class="kb-diagram-note">S/T 인터페이스: AMI 사용</div>
<div class="kb-diagram-note">U 인터페이스: 2B1Q (4레벨 PAM) 전환</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Pseudoternary는 AMI와 같은 규칙이지만 0과 1 역할만 바꾼 쌍둥이 코딩 — 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 더 자주 오느냐에 따라 유리한 쪽을 선택.

---

## Ⅴ. 실무 시나리오 — ISDN과 디지털 전화망



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">디지털 전화망 라인 코딩 실무:</div>
<div class="kb-diagram-note">T1 (북미 표준, 1.544 Mbps):</div>
<div class="kb-diagram-note">24채널 DS0 (64 kbps) x 24 = 1.536 Mbps + 프레이밍</div>
<div class="kb-diagram-note">라인 코딩: AMI (초기) -&gt; B8ZS (현대)</div>
<div class="kb-diagram-note">물리 매체: 2쌍 꼬임 구리선</div>
<div class="kb-diagram-note">E1 (유럽 표준, 2.048 Mbps):</div>
<div class="kb-diagram-note">30채널 + 2 관리 채널 = 32 x 64 kbps</div>
<div class="kb-diagram-note">라인 코딩: AMI -&gt; HDB3</div>
<div class="kb-diagram-note">ITU-T G.703 표준</div>
<div class="kb-diagram-note">ISDN BRI (Basic Rate Interface):</div>
<div class="kb-diagram-note">2B + D: 2개의 64 kbps 음성/데이터 + 16 kbps 신호</div>
<div class="kb-diagram-note">S/T 인터페이스: AMI 사용</div>
<div class="kb-diagram-note">최대 전송 거리: 1km (증폭기 없이)</div>
<div class="kb-diagram-note">현재 상황:</div>
<div class="kb-diagram-note">ISDN -&gt; ADSL -&gt; VDSL -&gt; 광섬유로 대체</div>
<div class="kb-diagram-note">T1/E1 -&gt; IP화 (VoIP) 진행 중</div>
<div class="kb-diagram-note">그러나 레거시 기업/통신사에서 여전히 사용</div>
</div>
</div>



> 📢 **섹션 요약 비유**: T1/E1은 고속도로 차선처럼 고정 대역폭을 나눠 쓰는 디지털 전화망 — [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/)/HDB3가 각 차선의 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등 역할.

---

## 📌 관련 개념 맵

```
AMI / Pseudoternary
+-- 분류
| +-- 삼진 부호 (Ternary)
| +-- 양극성 (Bipolar) 라인 코딩
+-- 특성
| +-- DC 성분 제거
| +-- 단일 비트 오류 탐지
| +-- 연속 0 동기화 한계
+-- 개선 버전
| +-- B8ZS (T1, 북미)
| +-- HDB3 (E1, 유럽)
+-- 응용
+-- ISDN BRI (S/T 인터페이스)
+-- T1 (1.544 Mbps)
+-- E1 (2.048 Mbps)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[아날로그 전화망 (1870s~)]
연속 아날로그 신호
|
v
[PCM 디지털화 (1937~1960s)]
양자화 + 부호화
|
v
[AMI 라인 코딩 표준화 (1960s)]
T1 시스템 (1962, AT&T)
|
v
[B8ZS / HDB3 (1970~80s)]
연속 0 문제 해결
E1 (ITU-T G.703)
|
v
[ISDN (1988~)]
AMI + B8ZS 복합 사용
|
v
[현재: IP화, 광섬유 대체]
레거시 호환성으로 유지 중
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. AMI는 "1"을 보낼 때마다 위로, 아래로, 위로... 번갈아 가며 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 보내는 방식이에요 — 계속 같은 방향이면 "오류야!"라고 알 수 있어요.
2. 0이 많이 연속되면 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 너무 오래 조용해져서 수신기가 헷갈리는데, B8ZS는 그럴 때 대신 "가짜 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 패턴"을 끼워 넣어줘요.
3. 국제전화나 옛날 인터넷 회선에서 이 방법을 사용해 먼 거리로도 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 정확하게 전달했답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 40 / 1120

← **이전**: [039. 맨체스터 / 차분 맨체스터 인코딩](/knowledge-base/studynote/03_network/01_data_communication/039_맨체스터_차분맨체스터/)
**다음**: [041. 차분 부호화 (Differential Encoding)](/knowledge-base/studynote/03_network/01_data_communication/041_차분_부호화/) →

---
