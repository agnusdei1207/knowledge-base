+++
title = "76. 시스템 전원 상태 (S-States, S0~S5)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: S-States(System Power States)는 [ACPI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/)가 정의한 시스템 전체 전원 상태로, S0(완전 동작)에서 S5(완전 종료)까지 전력 소비와 복귀 지연의 트레이드오프를 표현한다.
> 2. **가치**: S3(Suspend to RAM), S4(Hibernate), S5(Soft Off)는 각각 다른 전력/복구 특성을 제공하여 배터리 효율과 사용자 경험을 함께 최적화한다.
> 3. **판단 포인트**: Modern Standby(S0 Low Power Idle)는 S3의 완전한 대체가 아니라 S0 내부에서의 저전력 운영 모드이므로, 펌웨어와 드라이버 호환성을 함께 확인해야 한다.

---

## Ⅰ. 개요 및 필요성

컴퓨터를 오래 쓰지 않을 때 어떻게 해야 할까? 계속 켜두면 전력이 낭비되고, 완전히 끄면 다시 켤 때 오래 걸린다. 이 딜레마를 해결하기 위해 ACPI는 S-States라는 시스템 전원 상태 체계를 정의했다.

S-States는 컴퓨터의 "잠자는 방식"을 단계별로 정의한다. 노트북 덮개를 닫을 때 S3(RAM에 저장하고 빠르게 복귀)를 사용할지, S4(디스크에 저장하고 완전 절전)를 사용할지, 아니면 S5(전원 끄기)를 선택할지는 상황에 따라 다르다. 배터리가 충분하다면 S3로 빠른 복귀를, 장시간 미사용이라면 S4나 S5를 선택한다.

현대 모바일 기기에서는 Modern Standby(Connected Standby, S0ix)가 점점 S3를 대체하고 있다. 스마트폰처럼 절전 중에도 알림을 받아야 하는 장치는 S3 대신 S0 내부의 저전력 상태를 유지하면서 선택적으로 네트워크를 사용한다. 이 모드는 "항상 연결(Always Connected)" 특성을 제공한다.

- **📢 섹션 요약 비유**: 사람도 낮잠, 깊은 잠, 완전 수면이 다르다. 눈을 감는 정도에 따라 깨는 속도와 필요한 에너지가 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### S-States 전체 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시스템 전원 상태 (S-States) 전환 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">S0 (Working)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S0ix (Modern Standby): S0 내부 저전력 대기</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 네트워크 연결 유지, 알림 수신 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S1 (Power on Suspend): 레거시, CPU/RAM 전원 유지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S2 (Suspend): 레거시, CPU 꺼짐, RAM 유지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S3 (Suspend to RAM, STR):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── RAM만 전원 유지 (내용 보존)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── CPU, 장치 대부분 전원 OFF</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 복귀: 수 초 이내 (RAM에서 로드)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S4 (Suspend to Disk, Hibernate):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── RAM 내용을 디스크에 저장 (hiberfil.sys/swap)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 전원 거의 완전 차단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 복귀: 수십 초 (디스크에서 로드)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── S5 (Soft Off):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 완전 종료, 데이터 미보존</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 최소 대기 전력 (WoL 등 일부 유지)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── 복귀: 전체 부팅 (30초~수 분)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">G3 (Mechanical Off): 물리적 전원 차단, 완전 리셋</div></div>
</div>
</div>



### S-States 상세 비교표

| 상태 | 이름 | RAM 상태 | CPU 상태 | 전력 소비 | 복귀 시간 | Wake Source |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S0 | Working | 활성 | 실행 중 | 최고 | 즉시 | - |
| S0ix | Modern Standby | 일부 유지 | 저전력 | 낮음 | ~1초 | 네트워크, 타이머 |
| S1 | CPU Stop Grant | 유지 | 클럭 중지 | 조금 낮음 | 수 ms | 모든 소스 |
| S2 | (레거시) | 유지 | 전원 OFF | 낮음 | 수 초 | 제한적 |
| S3 | Suspend to RAM | 유지(전원) | OFF | 매우 낮음 | ~2초 | 전원 버튼, WoL |
| S4 | Hibernate | 디스크에 저장 | OFF | 거의 없음 | 30~60초 | 전원 버튼 |
| S5 | Soft Off | 없음 | OFF | 최소 대기 | 전체 부팅 | 전원 버튼, WoL |
| G3 | Mech. Off | 없음 | OFF | 없음 | 전체 부팅+ | 전원 버튼만 |

### S3 (Suspend to RAM) 동작 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">S0 → S3 전환 시:</div>
<div class="kb-diagram-note">1. OS가 모든 프로세스 상태를 RAM에 유지</div>
<div class="kb-diagram-note">2. 각 장치의 D-state를 D3(OFF)로 전환</div>
<div class="kb-diagram-note">3. CPU 주변 장치 전원 차단</div>
<div class="kb-diagram-note">4. RAM만 Self-Refresh 전원 유지</div>
<div class="kb-diagram-note">5. Platform EC(Embedded Controller)가 Wake 이벤트 감시</div>
<div class="kb-diagram-note">S3 → S0 복귀 시:</div>
<div class="kb-diagram-note">1. Wake 이벤트 감지 (전원 버튼, WoL, 타이머 등)</div>
<div class="kb-diagram-note">2. CPU 전원 복귀, 부팅 과정 일부 생략</div>
<div class="kb-diagram-note">3. RAM 내용 그대로 복원</div>
<div class="kb-diagram-note">4. 각 장치 D-state 복귀</div>
<div class="kb-diagram-note">5. 사용자에게 즉시 화면 표시</div>
</div>
</div>



### S4 (Hibernate) 동작 메커니즘



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">S0 → S4 전환 시:</div>
<div class="kb-diagram-note">1. OS가 RAM 전체 내용을 파일에 기록</div>
<div class="kb-diagram-tree-item" style="--depth:1">Windows: hiberfil.sys (RAM 크기만큼)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Linux: swap 파티션 (CONFIG_HIBERNATION)</div>
<div class="kb-diagram-note">2. 모든 장치 전원 차단</div>
<div class="kb-diagram-note">3. 시스템 완전 종료</div>
<div class="kb-diagram-note">S4 → S0 복귀 시:</div>
<div class="kb-diagram-note">1. 전원 버튼으로 부팅</div>
<div class="kb-diagram-note">2. BIOS/UEFI 초기화</div>
<div class="kb-diagram-note">3. OS 부트로더가 hibernate 이미지 감지</div>
<div class="kb-diagram-note">4. 이미지를 RAM으로 복원</div>
<div class="kb-diagram-note">5. 종료 전 상태 그대로 복귀</div>
</div>
</div>



- **📢 섹션 요약 비유**: S3는 얕은 낮잠(눈 감고 있지만 소리에 바로 깸), S4는 깊은 수면(노트에 꿈 내용 적어두고 완전히 잠), S5는 완전히 잠들어 아무것도 없는 상태다.

---

## Ⅲ. 비교 및 연결

### S3, S4, S5, Modern Standby 비교

| 비교 항목 | S3 (STR) | S4 (Hibernate) | S5 (Soft Off) | Modern Standby (S0ix) |
| :--- | :--- | :--- | :--- | :--- |
| 메모리 보존 | RAM 전원 유지 | 디스크에 저장 | 없음 | RAM 일부 유지 |
| 복귀 속도 | 매우 빠름 (~2초) | 보통 (30~60초) | 느림 (전체 부팅) | 즉시 (~1초) |
| 전력 절감 | 높음 | 매우 높음 | 최고 | 높음 |
| 네트워크 연결 | 없음 | 없음 | 없음 | 가능 (선택적) |
| 배터리 지속 | 수 일 | 무한 (전원 없음) | 무한 | 수 일~주 |
| 주요 사용 | 노트북 덮개 닫기 | 장시간 미사용 | 완전 종료 | 스마트폰/태블릿 |

### D-States (장치 전원 상태)와의 관계

| 시스템 S-State | 장치 D-State | 의미 |
| :--- | :--- | :--- |
| S0 | D0 | 장치 완전 동작 |
| S0 | D1/D2 | 장치 저전력 (일부 기능 유지) |
| S3 | D3hot | 장치 전원 최소, 버스 전원 유지 |
| S4/S5 | D3cold | 장치 완전 전원 차단 |

### Wake Source 관리

| Wake Source | 지원 S-State | 설명 |
| :--- | :--- | :--- |
| 전원 버튼 | S3, S4, S5 | 가장 기본적인 Wake Source |
| Wake-on-LAN (WoL) | S3, S5 | 네트워크 패킷으로 원격 기동 |
| USB 장치 (키보드/마우스) | S3 | 입력 시 복귀 |
| RTC 타이머 | S3, S4 | 예약 시간에 자동 복귀 |
| Bluetooth/WiFi | S0ix | Modern Standby에서 알림 수신 |

- **📢 섹션 요약 비유**: 집 전체를 끄는 것(S5)과 방 하나만 끄는 것(D-state)은 다르다. 시스템 전원과 장치 전원을 따로 이해해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. 대상 플랫폼에서 S3와 S4가 실제로 지원되는가? (Modern 시스템은 S3를 S0ix로 대체)
2. S4(Hibernate)를 위한 저장 공간이 충분한가? (최소 RAM 크기만큼 필요)
3. Wake-on-LAN, 전원 버튼, RTC 타이머 등 Wake source가 올바르게 설정됐는가?
4. S3 → S0 복귀 시 모든 장치(GPU, NIC, USB)가 정상 복귀하는가?
5. BIOS/UEFI 설정의 전원 정책이 OS 정책과 충돌하지 않는가?
6. Modern Standby(S0ix) 전환 시 모든 드라이버가 ACPI D-state를 지원하는가?
7. 서버 환경에서 ACPI S-state와 IPMI/BMC 원격 관리가 충돌하지 않는가?
8. 장시간 S3 상태 유지 시 배터리 소진으로 인한 데이터 손실 방지책이 있는가?

### 안티패턴

- **모든 장치에서 S3가 가능하다고 가정**: 일부 최신 울트라북은 BIOS 설계상 S3 대신 Modern Standby(S0ix)만 지원한다. 플랫폼 스펙을 반드시 확인해야 한다.
- **Hibernate 공간 없이 S4 설정**: Linux에서 swap이 부족하거나, Windows에서 hiberfil.sys 생성 공간이 없으면 S4가 동작하지 않는다. `powercfg /h on`(Windows) 또는 swap 크기 확인(Linux)이 필수다.
- **드라이버 업데이트 후 Resume 테스트 생략**: 새 드라이버는 D-state 전환 지원이 달라질 수 있다. S3/S4 진입 및 복귀 테스트를 반드시 수행해야 한다.
- **배터리 임계값 정책 없이 S3 장기 유지**: S3 상태에서도 RAM 전원 유지를 위해 배터리가 소모된다. 배터리가 방전되면 RAM 내용이 사라진다. S3 상태에서 배터리 임계값 도달 시 자동으로 S4로 전환하는 "Hybrid Sleep" 정책을 설정해야 한다.

기술사 관점에서는 S-States를 "전력 소비와 복귀 지연의 트레이드오프 상태 모델"로 설명하되, 각 상태의 RAM 보존 여부, 복귀 시간, Wake Source, D-State와의 관계를 함께 언급해야 한다.

- **📢 섹션 요약 비유**: 여행 전에 집 불을 끄는 방법을 미리 정해야 한다. 어디까지 끄고 어디는 남길지, 돌아왔을 때 불을 어떻게 켤지를 미리 계획하는 것이 S-State 설계다.

---

## Ⅴ. 기대효과 및 결론

S-States의 올바른 활용은 사용자 경험과 에너지 효율을 동시에 개선한다. 노트북에서 S3를 사용하면 덮개를 닫고 열었을 때 2초 이내에 이전 작업 화면으로 돌아오는 경험이 가능하다. S4는 장기 이동 시 배터리 걱정 없이 작업 내용을 보존한다.

서버 환경에서는 S5 상태에서 Wake-on-LAN(WoL)을 활용하여 원격으로 서버를 부팅하는 관리 효율이 높아진다. 데이터센터에서는 유휴 서버를 S5 상태로 두어 전력 소비를 최소화하고 필요 시 자동 기동하는 전력 관리 전략이 가능하다.

Modern Standby(S0ix)는 스마트폰과 태블릿 경험을 PC에 가져온다. 화면을 끈 상태에서도 네트워크가 연결되어 메일, 캘린더 알림을 실시간으로 받고, 화면을 켜면 즉시 사용 가능한 경험이다. 이는 향후 클라우드 연결 PC의 표준 전원 모델이 될 전망이다.

결론적으로 S-States는 "절전의 깊이"를 설계하는 것으로, "얼마나 오래 끄는가"보다 "어떻게 안전하고 빠르게 다시 켜지는가"를 함께 고려해야 하는 운영 설계다.

- **📢 섹션 요약 비유**: 잘 자는 것만큼 알람이 울리면 바로 일어나는 것이 중요하다. S-States는 절전과 복귀 능력을 함께 설계한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| ACPI | S-States를 정의하는 표준 |
| D-States | 개별 장치 전원 상태, S-State와 연계 |
| C-States | CPU 유휴 절전, S-State와 계층 구분 |
| Modern Standby (S0ix) | S0 내부 저전력 대기 (S3 대체 방향) |
| hiberfil.sys / swap | S4 Hibernate 이미지 저장소 |
| Wake-on-LAN | S3/S5에서 원격 복귀 메커니즘 |
| Hybrid Sleep | S3 + S4 결합 (배터리 방전 대비) |
| 배터리 관리 | S3 장기 유지 시 자동 S4 전환 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">항상 전원 ON (초기 PC)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI S-State 표준 정의 (1996)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">S3 (Suspend to RAM) 주류화 → 빠른 복귀 경험</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">S4 (Hibernate) 정착 → 장기 절전</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hybrid Sleep 도입 (S3 + S4 자동 전환)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Connected Standby / Modern Standby (S0ix) 등장</div>
<div class="kb-diagram-note">→ 스마트폰 경험을 PC로</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Windows 11 / ARM PC: S3 제거, S0ix 단일화</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Always Connected PC 표준화 전망</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. S0는 깨어서 놀고 있는 상태예요.
2. S3는 금방 깨는 낮잠, S4는 꿈 내용을 노트에 적고 자는 깊은 잠, S5는 완전히 잠든 상태예요.
3. 컴퓨터는 상황에 따라 가장 알맞은 잠자기 방법을 고른답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 76 / 800

← **이전**: [75. ACPI (Advanced Configuration and Power Interface)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/075_acpi/)
**다음**: [77. 프로세서 전원 상태 (C-States)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/077_c_states/) →

---
