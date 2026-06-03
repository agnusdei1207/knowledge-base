---
title: 📦 tarball이 뭔지 1분 만에 이해하기
tags:
- study
---

> **결론부터: ZIP 같은 거예요. 끝.** (더 자세히 보고 싶으면 아래로)

관련 문서:
- [[quartz-deployment]]
- [[tech-stack]]

---

## 🗜️ tarball = ZIP의 사촌

| 압축 방식 | 어디서 많이 쓰나 | 확장자 |
|---|---|---|
| **ZIP** | 윈도우, 일반인 | `.zip` |
| **tarball** | 리눅스, 개발자, 서버 | `.tar`, `.tar.gz`, `.tgz` |
| 7z, rar | 둘 다 | `.7z`, `.rar` |

**다 똑같은 거예요.** "여러 파일을 하나로 묶고, 작게 줄이고, 나중에 다시 풀 수 있게" 만든 거.

---

## 🏷️ 왜 이름이 "tarball"이냐

옛날 옛적에 (1970년대쯤) 컴퓨터는 데이터를 **테이프**에 저장했어요.

```
┌──────────────────────────┐
│  [□□□□□□□□□□]            │  ← 자기 테이프
│   ↑                      │
│  데이터가 이렇게 줄줄    │
│  저장됨                  │
└──────────────────────────┘
```

그때 "테이프에 데이터 저장" = **T**ape **Ar**chive = **`tar`**

나중에 디스크로 옮겨와도 이름이 그대로 살아남음. 그리고 묶인 파일이 "공처럼 둥글다" 해서 **`tarball`**이라고 부르게 됨.

> 📼 **tar** = Tape Archive의 줄임말
> ⚽ **tarball** = tar로 묶인 "공"

---

## 🤔 ZIP이랑 뭐가 달라?

솔직히 말하면 **기능은 거의 같음**. 다른 점:

| | ZIP | tarball (tar.gz) |
|---|---|---|
| 압축 | ✅ 함 | ✅ 함 (gzip 같이 쓰면) |
| 묶기만 (압축 X) | 가능 | 가능 (`.tar`만) |
| 윈도우 기본 | ✅ 예 | ❌ 아니오 |
| 리눅스 기본 | ⚠️ 따로 설치 | ✅ 기본 내장 |
| **GitHub 다운로드** | 가끔 | **거의 항상** |
| 용량 효율 | 좋음 | 약간 더 좋음 |

→ 둘 다 **같은 목적**. 환경에 따라 다 쓰는 것뿐.

---

## 🛠️ 실전에서 어디 봤냐면

### 1. GitHub에서 소스코드 다운받을 때
브라우저로 ZIP 받는 거 말고, 터미널에서:
```bash
curl -L https://github.com/누구/quartz/archive/refs/heads/v5.tar.gz -o quartz.tar.gz
tar -xzf quartz.tar.gz
```
→ 이게 **tarball 다운로드 + 압축 해제**.

### 2. 우리 [[quartz-deployment]] 스크립트
```bash
QUARTZ_TARBALL_URL="https://github.com/jackyzha0/quartz/archive/refs/heads/${QUARTZ_REF}.tar.gz"

curl -fsSL "$QUARTZ_TARBALL_URL" | tar -xz -C "$TMP_DIR" --strip-components=1
```
이 한 줄이 하는 일:
1. GitHub에서 `.tar.gz` 파일 받음
2. 화면에 출력 안 함 (`-fsSL`)
3. 바로 `tar`한테 파이프 ( `|` )
4. `tar`가 압축 풀어서 폴더에 풀어놓음

→ **tarball 없으면 빌드 자동화가 안 돌아갑니다.** 핵심 부품.

### 3. Docker 이미지, Node.js 패키지, Python 패키지
- Docker 이미지는 사실 tarball이 여러 개 묶인 거
- npm 패키지 = `.tgz` = tarball
- PyPI 패키지 = `.whl` = 사실 zip이지만 같은 개념

---

## 📋 자주 보는 tarball 명령어 5개

```bash
# 1. 만들기 (폴더 → tarball)
tar -czf 이름.tar.gz 폴더명
#    czf = Create, gZip, File

# 2. 풀기 (tarball → 폴더)
tar -xzf 이름.tar.gz
#    xzf = eXtract, gZip, File

# 3. 내용물만 보기 (풀지 않고)
tar -tzf 이름.tar.gz
#    tzf = lisT, gZip, File

# 4. ZIP 풀기 (참고로)
unzip 이름.zip

# 5. GitHub에서 직접 받기
curl -L https://github.com/.../archive/refs/heads/main.tar.gz | tar -xz
```

**기억법**:
- `c` = **C**reate (만들기)
- `x` = e**X**tract (풀기)
- `t` = lis**T** (목록)
- `z` = g**z**ip (압축 형식)
- `f` = **F**ile (파일 이름)

---

## 🆚 비유 정리

| 일상 | 컴퓨터 |
|---|---|
| 📦 택배 상자 | tarball |
| 🎁 선물 포장지 | 압축 알고리즘 |
| 📋 송장 | 메타데이터 (파일 목록) |
| 🔪 가위 | `tar` 명령어 |
| 📮 택배 기사 | `curl` / `wget` |

---

## ❓ 자주 헷갈리는 것

**Q. `.tar`, `.tar.gz`, `.tgz` 다 뭐가 달라?**
> - `.tar` = 묶기만 함 (압축 X)
> - `.tar.gz` = 묶고 gzip으로 압축
> - `.tgz` = `.tar.gz`의 줄임말. **같은 거.**

**Q. ZIP이 더 좋은 거 아냐?**
> 기능은 비슷. **리눅스/서버 세계에선 tar.gz가 표준**이라 자연스럽게 많이 보게 됨.

**Q. tarball 열려면 뭘 깔아야 해?**
> 리눅스/맥 = 기본으로 깔려 있음. 윈도우 = `7-Zip`이나 `tar` (Windows 10 이후 기본).

**Q. `tar.gz` 파일 더블클릭하면?**
> - 맥: 자동 압축 해제
> - 윈도우 10/11: `tar -xzf` 또는 7-Zip으로 열기
> - 리눅스: `tar -xzf 파일.tar.gz`

---

## 🎯 한 줄 요약

> **tarball은 ZIP이랑 같은 거. 리눅스에서 더 자주 쓰는 압축 파일. 끝.**

다음에 누가 "이거 tarball로 줄게요" 하면 "ㅇㅋ 알겠습니다" 하면 됩니다.
