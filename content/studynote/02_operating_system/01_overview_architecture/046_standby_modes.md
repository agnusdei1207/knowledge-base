+++
title = "046. 대기 모드 — OS Standby & Sleep Modes"
date = 2026-04-05

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

> **핵심 인사이트**
> 1. 대기 모드(Standby/Sleep Mode)는 OS가 시스템 전력을 절감하면서도 빠른 복귀를 보장하는 전력 관리 상태 — [ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/)(Advanced Configuration and [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Interface) 표준이 S0(완전 활성)부터 S5(소프트 파워오프)까지 6단계를 정의한다.
> 2. CPU P-State와 C-State는 OS 전력 관리의 핵심 — C-State는 CPU 유휴 시 코어별 절전(C0~C10), P-State는 [DVFS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/469_dvfs/)(Dynamic [Voltage](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) Frequency Scaling)로 성능-전력 균형을 조절하며 Linux의 cpufreq 드라이버가 이를 제어한다.
> 3. 현대 OS의 전력 관리는 반응성과 효율의 트레이드오프 — Windows Modern Standby(S0ix)는 스마트폰처럼 네트워크 연결을 유지하면서 저전력을 달성하나, 배경 프로세스 관리가 불충분하면 배터리 드레인 문제가 발생한다.

---

## Ⅰ. [ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) 전력 상태



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ACPI (Advanced Configuration and Power Interface):</div>
<div class="kb-diagram-note">OS와 하드웨어 간 전력 관리 표준</div>
<div class="kb-diagram-note">Intel/Microsoft/Toshiba 공동 개발 (1996)</div>
<div class="kb-diagram-note">글로벌 시스템 상태 (G-States):</div>
<div class="kb-diagram-note">G0: 활성 (Working)</div>
<div class="kb-diagram-note">G1: 슬리핑 (Sleeping) → S1~S4</div>
<div class="kb-diagram-note">G2: 소프트 파워오프 (Soft Off) → S5</div>
<div class="kb-diagram-note">G3: 메카니컬 파워오프 (전원 완전 차단)</div>
<div class="kb-diagram-note">슬리핑 상태 (S-States):</div>
<div class="kb-diagram-note">S0: 완전 활성 (Full Working)</div>
<div class="kb-diagram-note">S1 (Power on Suspend):</div>
<div class="kb-diagram-note">CPU 캐시 플러시, CLK 정지</div>
<div class="kb-diagram-note">RAM 유지, 빠른 복귀</div>
<div class="kb-diagram-note">소비전력: 약간 감소</div>
<div class="kb-diagram-note">S2: CPU 전원 OFF, 메모리 유지</div>
<div class="kb-diagram-note">S3 (Suspend to RAM, STR):</div>
<div class="kb-diagram-note">RAM 유지, 나머지 OFF</div>
<div class="kb-diagram-note">복귀 시간: 수초</div>
<div class="kb-diagram-note">대부분 노트북의 "슬립" 모드</div>
<div class="kb-diagram-note">소비전력: 1~2W</div>
<div class="kb-diagram-note">S4 (Suspend to Disk, STD, Hibernation):</div>
<div class="kb-diagram-note">RAM → 디스크 저장 → 전원 OFF</div>
<div class="kb-diagram-note">복귀 시간: 수십초 (디스크에서 로드)</div>
<div class="kb-diagram-note">소비전력: 0W (전원 OFF)</div>
<div class="kb-diagram-note">S5 (Soft Off):</div>
<div class="kb-diagram-note">시스템 종료 (WOL 대기 가능)</div>
<div class="kb-diagram-note">소비전력: &lt; 1W</div>
<div class="kb-diagram-note">Windows 대응:</div>
<div class="kb-diagram-note">S3 → 절전 (Sleep)</div>
<div class="kb-diagram-note">S4 → 최대 절전 (Hibernate)</div>
<div class="kb-diagram-note">Modern Standby → S0ix</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/) S-State는 회사 퇴근 단계 — S0=열심히 일하는 중, S1=잠깐 자리 비움, S3=퇴근(짐 두고), S4=완전 퇴근([PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 끔), S5=전원 off. 빠른 복귀 vs 완전 절전 트레이드오프!

---

## Ⅱ. CPU C-State와 P-State



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CPU 절전 상태 (C-States):</div>
<div class="kb-diagram-note">각 CPU 코어의 유휴(Idle) 절전 단계</div>
<div class="kb-diagram-note">C-State 계층:</div>
<div class="kb-diagram-note">C0: 활성 (Active, 명령 실행 중)</div>
<div class="kb-diagram-note">C1: Halt (클럭 게이팅, 즉시 복귀)</div>
<div class="kb-diagram-note">C1E: C1 + 전압 감소</div>
<div class="kb-diagram-note">C3: Sleep (캐시 플러시)</div>
<div class="kb-diagram-note">C6: Deep Power Down (코어 전원 OFF 일부)</div>
<div class="kb-diagram-note">C7: Enhanced Deep Power Down</div>
<div class="kb-diagram-note">C10: 가장 깊은 절전 (최신 CPU)</div>
<div class="kb-diagram-note">진입: OS 스케줄러 유휴 감지 → Halt 명령</div>
<div class="kb-diagram-note">복귀 지연:</div>
<div class="kb-diagram-note">C1: &lt;1 μs, C3: &lt;100 μs, C6: &lt;1 ms, C10: &lt;10ms</div>
<div class="kb-diagram-note">CPU P-State (성능 상태):</div>
<div class="kb-diagram-note">DVFS: 전압+주파수 동적 조절</div>
<div class="kb-diagram-note">P0: 최고 주파수/전압 (최대 성능)</div>
<div class="kb-diagram-note">P1, P2, ...: 낮은 주파수/전압</div>
<div class="kb-diagram-note">전력: P ≈ α × C × V² × f</div>
<div class="kb-diagram-note">V 20% 감소 → 전력 36% 감소 (V² 효과)</div>
<div class="kb-diagram-note">Linux cpufreq 드라이버:</div>
<div class="kb-diagram-note">Governor (정책):</div>
<div class="kb-diagram-tree-item" style="--depth:1">performance: 항상 최고 주파수</div>
<div class="kb-diagram-tree-item" style="--depth:1">powersave: 항상 최저 주파수</div>
<div class="kb-diagram-tree-item" style="--depth:1">ondemand: 부하에 따라 동적 (기본)</div>
<div class="kb-diagram-tree-item" style="--depth:1">schedutil: CFS 스케줄러 연계 (현대적)</div>
<div class="kb-diagram-note">확인: cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor</div>
<div class="kb-diagram-note">변경: echo schedutil &gt; .../scaling_governor</div>
<div class="kb-diagram-note">Package C-State:</div>
<div class="kb-diagram-note">모든 코어 C-State 진입 시 패키지(CPU 전체) 절전</div>
<div class="kb-diagram-note">PC0, PC2, PC6, PC8, PC10 등</div>
</div>
</div>



> 📢 **섹션 요약 비유**: C-State는 공장 가동 단계 — C0(풀가동), C1(일시정지), C6(라인 셧다운). 주문 없으면(유휴) 라인 끄고 절전!

---

## Ⅲ. Modern Standby (S0ix)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Modern Standby (Windows S0ix):</div>
<div class="kb-diagram-note">스마트폰처럼 네트워크 연결 유지하면서 저전력</div>
<div class="kb-diagram-note">기존 S3 대비:</div>
<div class="kb-diagram-note">S3: 네트워크 완전 차단 → 이메일/알림 수신 불가</div>
<div class="kb-diagram-note">S0ix: 저전력 상태에서 Wi-Fi 유지 → 알림 수신</div>
<div class="kb-diagram-note">S0ix 동작:</div>
<div class="kb-diagram-note">디스플레이 꺼짐 → 화면 전원 OFF</div>
<div class="kb-diagram-note">→ 앱 정지 (일시 중단)</div>
<div class="kb-diagram-note">→ CPU C10 절전</div>
<div class="kb-diagram-note">→ Wi-Fi 저전력 수신 유지 (Wi-Fi DTIM)</div>
<div class="kb-diagram-note">→ 이메일 도착 → CPU 웨이크업 → 처리 → 다시 C10</div>
<div class="kb-diagram-note">목표 전력: &lt; 5~10 mW (화면 꺼진 상태)</div>
<div class="kb-diagram-note">S0ix 문제:</div>
<div class="kb-diagram-note">배경 프로세스 미관리 → 전력 소모</div>
<div class="kb-diagram-note">배터리 드레인 원인:</div>
<div class="kb-diagram-tree-item" style="--depth:1">전력 비효율 드라이버 깨어남</div>
<div class="kb-diagram-tree-item" style="--depth:1">백그라운드 앱 웨이크락 남용</div>
<div class="kb-diagram-note">진단 도구:</div>
<div class="kb-diagram-note">powercfg /sleepstudy → 수면 품질 리포트</div>
<div class="kb-diagram-note">powercfg /energy → 전력 이슈 진단</div>
<div class="kb-diagram-note">Linux: 유사 개념</div>
<div class="kb-diagram-note">SATA Link Power Management</div>
<div class="kb-diagram-note">PCIe ASPM (Active State Power Management)</div>
<div class="kb-diagram-note">Suspend-to-Idle (s2idle): S0ix 유사</div>
<div class="kb-diagram-note">Android Doze 모드:</div>
<div class="kb-diagram-note">S0ix와 유사한 모바일 개념</div>
<div class="kb-diagram-note">화면 꺼짐 + 일정 시간 후 Doze 진입</div>
<div class="kb-diagram-note">네트워크 제한 + CPU 활동 제한</div>
<div class="kb-diagram-note">유지보수 윈도우(Maintenance Window)에서만 동기화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Modern Standby는 스마트워치 대기 모드 — 손목에 차고 있어도 배터리 오래가면서 카카오 알림(네트워크)은 계속 받아요!

---

## Ⅳ. OS 전력 관리 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">OS 전력 관리 소프트웨어 스택:</div>
<div class="kb-diagram-note">Linux 전력 관리:</div>
<div class="kb-diagram-note">사용자공간: powertop, tlp, laptop-mode-tools</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">커널 전력 관리 서브시스템:</div>
<div class="kb-diagram-tree-item" style="--depth:1">pm-utils</div>
<div class="kb-diagram-tree-item" style="--depth:1">/sys/power/ 인터페이스</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">디바이스 드라이버 PM 콜백:</div>
<div class="kb-diagram-tree-item" style="--depth:1">suspend(), resume()</div>
<div class="kb-diagram-tree-item" style="--depth:1">runtime_suspend(), runtime_resume()</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">하드웨어: ACPI, 칩셋</div>
<div class="kb-diagram-note">Linux Runtime PM:</div>
<div class="kb-diagram-note">장치 사용 없을 때 자동 절전</div>
<div class="kb-diagram-note">USB 마우스: 움직임 없으면 USB 포트 절전</div>
<div class="kb-diagram-note">SATA 드라이브: 활동 없으면 스핀다운</div>
<div class="kb-diagram-note">커널 코드 패턴:</div>
<div class="kb-diagram-note">pm_runtime_put_autosuspend(dev) → 절전</div>
<div class="kb-diagram-note">pm_runtime_get_sync(dev) → 깨우기</div>
<div class="kb-diagram-note">Windows 전력 계획:</div>
<div class="kb-diagram-note">균형 (Balanced): 성능-전력 균형</div>
<div class="kb-diagram-note">고성능 (High Performance): 절전 없음</div>
<div class="kb-diagram-note">절전 (Power Saver): 최대 절전</div>
<div class="kb-diagram-note">Modern Standby 정책:</div>
<div class="kb-diagram-note">PowerCfg /setactive &lt;GUID&gt;</div>
<div class="kb-diagram-note">Connected Standby vs Disconnected</div>
<div class="kb-diagram-note">macOS:</div>
<div class="kb-diagram-note">App Nap: 포커스 없는 앱 자동 제한</div>
<div class="kb-diagram-note">Power Nap: 슬립 중 이메일 동기화</div>
<div class="kb-diagram-note">Compressed Memory: 절전 RAM 사용</div>
</div>
</div>



> 📢 **섹션 요약 비유**: OS 전력 관리는 스마트 사무실 — 아무도 없으면(유휴) 에어컨·조명 자동 끄기(C-State), 퇴근 전 프린터 대기 모드(S3), 주말엔 전원 차단(S5)!

---

## Ⅴ. 실무 시나리오 — 배터리 드레인 진단

```
노트북 배터리 빠른 방전 문제 해결:

현상:
  Surface Pro 9 슬립 상태에서
  8시간 동안 배터리 40% 소모 (비정상)
  정상: < 5%

진단:

1. powercfg /sleepstudy 실행:
   수면 보고서 생성 (HTML)
   
   의심 항목:
   - 총 드레인: 8시간 × 480mA = 과다
   - 배터리 드레인 상위 드라이버 표시

2. powercfg /energy 실행:
   에너지 효율 보고서
   
   발견:
   - Bluetooth 드라이버: 과도한 활동
   - Intel Display Driver: S0ix 진입 방해

3. 이벤트 뷰어 분석:
   전원 이벤트 로그
   웨이크 소스 분석

수정:
  블루투스 드라이버 업데이트
  디스플레이 드라이버 업데이트
  
  레지스트리:
  HKLM\SYSTEM\CurrentControlSet\Control\Power
  DisconnectedStandbyEnabled = 1
  
  결과:
  슬립 중 8시간 드레인: 40% → 4% (정상화)

서버 전력 최적화 (다른 시나리오):
  데이터센터 서버 전력 관리
  IPMI/BMC: C-State 조정
  BIOS: C-State 깊이 설정
  OS: cpufreq governor 최적화
  
  효과: 서버 1대 절전 상태 10~20W 절감
  1000대 × 20W = 20kW = 연 1,750만원 절감
```

> 📢 **섹션 요약 비유**: 배터리 드레인 진단은 전기 누수 찾기 — powercfg는 전력계, 이상한 드라이버([블루투스](/knowledge-base/studynote/03_network/12_iot_wpan_edge/605_bluetooth_ieee_802_15_1_piconet_scatternet/))가 잠자는 동안 몰래 전기 쓰는 것을 잡아내요!

---

## 📌 관련 개념 맵

```
OS 대기 모드
+-- ACPI S-States
|   +-- S3 (Suspend to RAM)
|   +-- S4 (Hibernate)
|   +-- Modern Standby (S0ix)
+-- CPU 절전
|   +-- C-States (C0~C10)
|   +-- P-States (DVFS)
+-- OS 구현
|   +-- Linux cpufreq, runtime PM
|   +-- Windows 전력 계획
|   +-- Android Doze
+-- 진단
    +-- powercfg /sleepstudy
    +-- powertop (Linux)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[ACPI 표준 제정 (1996)]
Intel/MS/Toshiba
S0~S5 표준화
      |
      v
[멀티코어 C-State (2007~)]
인텔 Core 시리즈
패키지 C-State 도입
      |
      v
[Connected Standby / S0ix (2012)]
Windows 8 Surface
스마트폰식 대기 모드
      |
      v
[현재: Modern Standby 성숙]
Windows 11 최적화
Android Doze 고도화
      |
      v
[미래: AI 전력 예측]
사용 패턴 학습 → 선제적 절전
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 대기 모드는 컴퓨터 졸기 — S3는 "잠깐 조는 것"(금방 깨어남), S4는 "푹 자는 것"(느리게 깨어남). 많이 잘수록 배터리 절약!
2. C-State는 CPU 쉬는 정도 — C0=열심히 일하기, C6=점심 휴식(전원 끄기). 쉬는 동안 전기 절약!
3. Modern Standby는 스마트폰 대기 — 화면은 꺼졌어도 카톡 알림은 와요! 노트북이 스마트폰처럼 저전력 유지하며 연결!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 46 / 800

← **이전**: [045. 클러스터 시스템 — Cluster System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/045_cluster_system/)
**다음**: [047. DLM — 분산 잠금 관리자](/knowledge-base/studynote/02_operating_system/01_overview_architecture/047_dlm/) →

---
