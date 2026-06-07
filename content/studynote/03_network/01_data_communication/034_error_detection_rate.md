---
title: "034. Error Detection Rate"
date: "2026-03-04"
tags:
  - "studynote-network"
weight: 34
---
> **핵심 인사이트 3줄**
> 1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 오류 검출은 [패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/)(1비트 추가), [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)([Cyclic Redundancy Check](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/), 순환 잉여 검사), [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)([Hamming Code](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)) 3가지 방식이 계층별로 활용되며, 검출 능력과 오버헤드가 상충한다.
> 2. CRC는 GF(2) [다항식](/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) 나눗셈으로 나머지를 FCS(Frame Check Sequence)로 추가해 연속 버스트 오류를 강력히 검출하며, [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)-32)·[USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)·[HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/) 등 대부분의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층 표준에 사용된다.
> 3. [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)는 오류 위치까지 특정해 <strong>단일 <a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 오류를 자동 수정(SEC·Single Error Correction)</strong>하는 유일한 방식으로, [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 메모리·[RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/)·위성 통신에 핵심 기술이다.

---

## Ⅰ. [패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/) ([Parity Bit](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/))

[패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)에 1비트를 추가해 1의 개수를 짝수/홀수로 맞춘다.

| 종류         | 규칙                     | 검출 능력           |
|-----------|--------------------------|-------------------|
| [짝수 패리티](/studynote/01_computer_architecture/02_data_representation_arithmetic/108_even_parity/) | 1의 개수를 짝수로 맞춤    | 홀수 개수 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류  |
| [홀수 패리티](/studynote/01_computer_architecture/02_data_representation_arithmetic/109_odd_parity/) | 1의 개수를 홀수로 맞춤    | 홀수 개수 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류  |

**한계**: 짝수 개의 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 동시에 오류 시 검출 불가 (2비트 오류는 못 잡음)

📢 **섹션 요약 비유**: 패리티는 계산서 합계 확인이다 — 금액 합계(1의 개수)가 짝수여야 하는데 홀수가 되면 오류가 있다는 것을 안다.

---

## Ⅱ. [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) ([Cyclic Redundancy Check](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/))

[CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)([Cyclic Redundancy Check](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/), 순환 잉여 검사)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [다항식](/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/)으로 나눠 나머지(FCS)를 전송한다.

### [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) 동작 원리

```
송신측:
  원본 데이터 M(x): 1101011011
  생성 다항식 G(x): 10011 (CRC-4)
  -> 데이터에 0000 추가 (G 차수만큼)
  -> M(x) × x^n을 G(x)로 XOR 나눗셈
  -> 나머지 R(x) = FCS (프레임에 추가)

수신측:
  수신 데이터 + FCS를 G(x)로 나눔
  -> 나머지 = 0 : 오류 없음
  -> 나머지 ≠ 0 : 오류 검출
```

### 주요 [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) 표준

| 표준       | [다항식](/studynote/03_network/04_data_link_layer_error/195_polynomial_generator_crc/) 차수 | 검출 가능 오류         | 사용처             |
|---------|---------|---------------------|--------------------|
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)-8   | 8비트    | 단일+연속 8비트 오류  | 센서·[직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 통신      |
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)-16  | 16비트   | 연속 16비트 오류      | [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/), Modbus        |
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)-32  | 32비트   | 연속 32비트 오류      | [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/), ZIP, PNG |
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)-CCITT | 16비트 | [HDLC](/studynote/03_network/04_data_link_layer_error/216_hdlc_high_level_data_link_control/)·X.25 표준      | 통신 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)       |

📢 **섹션 요약 비유**: CRC는 비밀번호처럼 체크하는 것이다 — [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 특정 수로 나눈 나머지(FCS)를 함께 보내고, 받는 쪽에서 같은 계산을 해서 나머지가 0이면 이상 없다.

---

## Ⅲ. [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/) ([Hamming Code](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/))

[해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)([Hamming Code](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/))는 <strong>오류 위치 특정 + 자동 수정(SEC)</strong>이 가능한 선형 오류 수정 코드다.

### [패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/) 위치 계산

```
해밍 코드 규칙:
  패리티 비트 위치: 2^0=1, 2^1=2, 2^2=4, 2^3=8, ...

7비트 데이터 + 4개 패리티 -> 11비트 코드:
  비트 위치: 1  2  3  4  5  6  7  8  9  10  11
  역할:      P1 P2 D1 P3 D2 D3 D4 P4 D5 D6  D7
```

### 오류 검출 및 수정

```
P1 검사: 비트 1,3,5,7,9,11
P2 검사: 비트 2,3,6,7,10,11
P3 검사: 비트 4,5,6,7
P4 검사: 비트 8,9,10,11

오류 위치 = P4×8 + P3×4 + P2×2 + P1×1
예: P4=0, P3=1, P2=1, P1=0 -> 위치 = 0+4+2+0 = 6번 비트 오류
```

📢 **섹션 요약 비유**: [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)는 이진수 위치 추적이다 — 여러 검사관([패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/))이 각자 담당 구역의 이상을 보고하면, 보고 패턴으로 정확히 어느 위치에 오류가 있는지 찾는다.

---

## Ⅳ. 검출 방식 비교

| 방식        | 오버헤드 | 검출 능력         | 수정 가능 여부 | 사용처          |
|-----------|------|-----------------|------------|----------------|
| [패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/) | 낮음  | 홀수 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류     | ❌          | 메모리·[직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 통신|
| [CRC](/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/)        | 중간  | 연속 버스트 오류  | ❌          | [이더넷](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)·[USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/)·[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) |
| [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)  | 높음  | 단일+이중 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류| ✅ (단일)   | [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 메모리·[RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) |
| RS 코드   | 높음  | 다중 버스트 오류  | ✅ (다중)   | CD·[RAID 6](/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/)·위성  |

📢 **섹션 요약 비유**: 오류 검출 방식은 보험의 종류다 — 패리티는 간단한 상해보험, CRC는 실손보험(충분한 보상), [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)는 갱새로운 유형의 실손+자동 치료(수정 포함)다.

---

## Ⅴ. [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 메모리 — 서버 인프라 적용

[ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/)([Error-Correcting Code](/studynote/01_computer_architecture/13_reliability_power_management/463_ecc_memory/)) 메모리는 [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)를 기반으로 단일 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류를 자동 수정한다.

```
일반 메모리:   64비트 데이터 (오류 검출·수정 없음)
ECC 메모리:    64비트 데이터 + 8비트 ECC = 72비트
  -> 단일 비트 오류 자동 수정 (SEC)
  -> 이중 비트 오류 검출 (DED: Double Error Detection)
  -> SECDED: Single Error Correct, Double Error Detect
```

📢 **섹션 요약 비유**: [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) 메모리는 자동 교정 기능이 있는 받아쓰기다 — 1글자 실수(단일 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류)는 자동으로 고쳐주고, 2글자 실수는 "다시 받아쓰시오"라고 알려준다.

---

## 📌 관련 개념 맵

```
에러 검출/수정
+-- 검출만 가능
|   +-- 패리티 비트 (홀수 비트 오류)
|   +-- CRC (연속 버스트 오류, 이더넷·USB)
+-- 검출 + 수정 가능
|   +-- 해밍 코드 (SEC·DED, ECC 메모리)
|   +-- Reed-Solomon 코드 (CD·RAID 6)
+-- 응용
    +-- ECC 메모리 (서버용 DIMM)
    +-- RAID 패리티 (RAID 5/6)
    +-- 데이터 링크 계층 (FCS)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              에러 검출/수정 발전 흐름                            |
+--------------+--------------------+-----------------------------+
| 1950년       | 해밍 코드 발표     | Bell Labs, SEC 최초 구현     |
| 1961년       | CRC 제안           | Peterson & Brown, 다항식 기반|
| 1960년대     | Reed-Solomon 코드  | 버스트 오류 수정, CD·위성    |
| 1980년대     | ECC 메모리         | 서버·워크스테이션 표준화     |
| 1995년       | Ethernet CRC-32   | 10/100Mbps 표준 FCS         |
| 2000년대~    | LDPC·Turbo 코드   | 4G·5G·Wi-Fi 채널 코딩       |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
패리티 -> CRC -> 해밍 코드 -> Reed-Solomon
   v        v         v           v
1비트 추가  FCS 추가  오류 위치   다중 수정
   v
ECC 메모리 -> 서버 안정성 -> 데이터 무결성
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [패리티 비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/107_parity_bit/)는 개수 확인이다 — 사탕이 항상 짝수여야 하는데, 받아보니 홀수면 하나가 사라진(오류) 것을 안다.
2. CRC는 비밀 암호 확인이다 — 편지([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 특별한 숫자(FCS)를 적어서 보내고, 받는 쪽이 같은 계산을 해서 맞으면 이상 없다.
3. [해밍 코드](/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)는 오류 GPS다 — 어디가 잘못됐는지 위치까지 알려줘서 자동으로 고칠 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 34 / 1120

<- **이전**: [ENQ / ACK / NAK / EOT 제어 문자](/studynote/03_network/01_data_communication/033_ENQ_ACK_NAK_EOT/)
**다음**: [035. 부호화 — 라인 코딩 & 블록 코딩](/studynote/03_network/01_data_communication/035_부호화_라인_코딩_블록_코딩/) ->

---
