+++
title = "펌웨어 (Firmware)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

> **핵심 인사이트 3줄**
> 1. 펌웨어(Firmware)는 하드웨어에 내장된 소프트웨어로, [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/)/Flash에 저장되어 기기 전원 투입 시 가장 먼저 실행되는 저수준 제어 코드다.
> 2. BIOS → [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) → Secure Boot로 발전하며, 부트 프로세스·하드웨어 초기화·드라이버 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층을 제공한다.
> 3. [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·임베디드 환경에서 펌웨어 보안 취약점은 [공급망 공격](/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/)([Supply Chain Attack](/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/))의 가장 깊은 침투 경로가 된다.

---

## Ⅰ. 펌웨어의 정의와 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

펌웨어(Firmware)는 **하드웨어를 직접 제어하기 위해 [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/)·Flash·EEPROM에 내장된 소프트웨어**다. 하드웨어(HW)와 소프트웨어(SW)의 중간 계층으로, 기기가 켜지면 CPU가 가장 먼저 실행하는 코드다.

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)         | 저장 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)         | 예시                           |
|-------------|------------------|-------------------------------|
| 마스크 [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/)   | 제조 시 고정      | 오래된 가전 제어 IC            |
| EEPROM      | 전기 소거/재기록   | 시리얼 번호·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 저장           |
| Flash 펌웨어 | OTA 업데이트 가능 | [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) BIOS, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러        |
| 임베디드 OS  | Flash + RAM       | 스마트TV Android/Tizen         |

📢 **섹션 요약 비유**: 펌웨어는 가전제품 설명서가 기기 안에 인쇄된 것과 같다. 꺼내서 수정하기 어렵지만, 요즘은 인터넷으로 업데이트도 된다.

---

## Ⅱ. BIOS → [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) 발전과 부트 프로세스

### BIOS (Basic Input/Output System) 한계

- 16비트 리얼 모드, 1MB 주소 공간 제한
- [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)([Master Boot Record](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)) 기반: 최대 2TB, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 4개
- 텍스트 인터페이스, 드라이버 내장 불가

### [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) (Unified Extensible Firmware Interface) 특징

| 항목         | BIOS          | [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/)                    |
|-------------|---------------|-------------------------|
| 주소 공간    | 1MB           | 17.2억 TB (64비트)       |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 방식  | [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)           | [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) (최대 128개)         |
| [보안 부팅](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/)    | 없음           | [Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 지원         |
| GUI         | 텍스트         | 그래픽 UI + 마우스 지원   |
| 부트 속도   | 느림           | Fast Boot, [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 직접 지원 |

### 부트 시퀀스

```
전원 ON → POST(Power-On Self Test) → UEFI 초기화
   → 부트 디바이스 선택 → 부트로더(GRUB2/Windows Boot Manager)
   → 커널 로드 → OS 초기화
```

📢 **섹션 요약 비유**: UEFI는 낡은 흑백 TV 리모컨(BIOS)을 스마트폰 앱으로 교체한 것과 같다. 기능도 많고 빠르지만 보안 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)도 더 복잡해졌다.

---

## Ⅲ. Secure Boot와 신뢰 체인 (Chain of Trust)

```
┌─────────────────────────────────────────────────────────┐
│                   Secure Boot 흐름                       │
│  UEFI Firmware → 서명 검증 → 부트로더 서명 확인          │
│                           → 커널 서명 확인               │
│                           → 드라이버 서명 확인           │
│                    서명 불일치 → 부팅 거부                │
└─────────────────────────────────────────────────────────┘
```

**[TPM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/) ([Trusted Platform Module](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/))과 결합**

- [TPM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/) 2.0: 플랫폼 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 측정(PCR), 키 저장, [BitLocker](/knowledge-base/studynote/09_security/04_endpoint_security/397_bitlocker_windows_fde/) 연동
- 측정 부팅([Measured Boot](/knowledge-base/studynote/09_security/18_iot_ot_physical/919_measured_boot/)): 각 단계 해시를 TPM에 기록 → 원격 증명

📢 **섹션 요약 비유**: Secure Boot는 콘서트 입장 검표와 같다. 티켓(서명) 없는 코드는 무대(OS)에 들어올 수 없고, TPM은 입장자 명단을 봉인 보관한다.

---

## Ⅳ. 임베디드·[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 펌웨어 아키텍처

### 임베디드 펌웨어 구조

```
┌────────────────────────────────┐
│   애플리케이션 레이어           │
├────────────────────────────────┤
│   HAL (Hardware Abstraction    │
│        Layer, 하드웨어 추상화) │
├────────────────────────────────┤
│   드라이버 레이어               │
├────────────────────────────────┤
│   부트로더 / BSP               │
├────────────────────────────────┤
│   MCU / SoC 하드웨어           │
└────────────────────────────────┘
```

### OTA ([Over-The-Air](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) 펌웨어 업데이트

| 방식       | 특징                       | 위험 요소              |
|-----------|---------------------------|----------------------|
| A/B [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 업데이트 실패 시 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능   | 2배 Flash 용량 필요   |
| 단일 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 용량 효율적                | 업데이트 실패 시 벽돌  |
| 델타 업데이트 | 변경 부분만 전송           | 패치 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 복잡         |

📢 **섹션 요약 비유**: OTA 업데이트는 비행 중인 비행기 엔진 교체와 같다. A/B [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 예비 엔진을 미리 장착해두고 교체 후 구 엔진을 제거하는 방식이다.

---

## Ⅴ. 펌웨어 보안 취약점과 대응

### 주요 공격 유형

| 공격           | 설명                          | 사례                    |
|---------------|-------------------------------|------------------------|
| [부트킷](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/)         | [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/)·[UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)          | BlackLotus (2023)       |
| [공급망 공격](/knowledge-base/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/)    | 제조 단계 악성 펌웨어 삽입     | SolarWinds [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)       |
| 다운그레이드   | 취약한 구버전으로 강제 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)    | BootHole 취약점         |
| JTAG 덤프      | 물리 접근으로 Flash 내용 추출  | 임베디드 기기 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)     |

### 대응 방안

```
Secure Boot + TPM 측정 부팅
   ↓
펌웨어 서명 검증 (PKI 기반)
   ↓
OTA 암호화 전송 (TLS/DTLS)
   ↓
쓰기 방지 레지스터 설정 (Write-Protect)
   ↓
정기 취약점 스캔 (SBOM 기반)
```

📢 **섹션 요약 비유**: 펌웨어 보안은 건물 지하 금고와 같다. 아무리 위층 보안이 강해도 지하 금고(펌웨어)가 뚫리면 건물 전체가 위험해진다.

---

## 📌 관련 개념 맵

```
펌웨어 (Firmware)
├── 저장 매체
│   ├── ROM (Read Only Memory)
│   ├── EEPROM
│   └── Flash Memory
├── PC 플랫폼
│   ├── BIOS (Basic Input/Output System)
│   ├── UEFI (Unified Extensible Firmware Interface)
│   └── Secure Boot
├── 신뢰 기반
│   ├── TPM (Trusted Platform Module)
│   ├── Chain of Trust (신뢰 체인)
│   └── 측정 부팅 (Measured Boot)
└── 임베디드
    ├── HAL (Hardware Abstraction Layer)
    ├── BSP (Board Support Package)
    └── OTA (Over-The-Air) 업데이트
```

---

## 📈 관련 키워드 및 발전 흐름도

```
┌─────────────────────────────────────────────────────────────────┐
│                 펌웨어 기술 발전 흐름                            │
├──────────────┬──────────────────────┬───────────────────────────┤
│ 1980년대     │ BIOS (ROM 내장)      │ 16비트, 텍스트 기반        │
│ 1990년대     │ Flash BIOS           │ 업데이트 가능 펌웨어       │
│ 2000년대     │ UEFI 표준화 (2006)   │ 64비트, GPT, Secure Boot  │
│ 2010년대     │ TPM 2.0 + 측정 부팅  │ 하드웨어 신뢰 체인         │
│ 2020년대     │ OTA·IoT 펌웨어 보안  │ SBOM, 공급망 보안 강화     │
└──────────────┴──────────────────────┴───────────────────────────┘

핵심 키워드 연결:
펌웨어 → UEFI → Secure Boot → TPM → 측정 부팅
  ↓         ↓          ↓        ↓
Flash     GPT/MBR    PKI 서명  PCR 레지스터
  ↓
OTA 업데이트 → A/B 파티션 → 롤백 보장
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 펌웨어는 장난감 로봇 안에 인쇄된 설명서다 — 버튼을 누르면 어떻게 움직일지 알려주는 기본 지침이 들어있다.
2. UEFI는 낡은 종이 설명서를 스마트폰 앱으로 바꾼 것이다 — 그림도 보이고 터치로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)도 할 수 있다.
3. Secure Boot는 집 열쇠 잠금 장치다 — 맞는 열쇠(서명)만 문을 열 수 있고, 복사 열쇠는 거부된다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 32 / 800

← **이전**: [31. SYSGEN — 시스템 생성과 OS 구성](/knowledge-base/studynote/02_operating_system/01_overview_architecture/031_sysgen/)
**다음**: [컨텍스트 (Context) / 컨텍스트 스위칭 (Context Switching)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) →

---
