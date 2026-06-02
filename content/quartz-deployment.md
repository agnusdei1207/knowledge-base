# 🌐 Quartz를 이용한 사내 위키 웹 사이트 배포 가이드

Quartz는 Foam 마크다운 저장소를 활용해 초고속 웹 브라우저 뷰어를 만들어주는 최적의 동반자입니다.

---

## 🛠️ GitHub Actions를 이용한 무상 배포 (정석)

GitHub Pages를 통해 별도의 웹서버를 구축하지 않고도 무료로 실시간 위키 사이트를 배포할 수 있습니다.

1. **레포지토리 설정 변경:** 
   * GitHub 레포지토리 Settings -> Pages 탭 진입
   * Build and deployment -> Source를 **GitHub Actions**로 변경
2. **GitHub Workflow 파일 생성:**
   * `.github/workflows/deploy.yml` 파일 생성 (자동 생성 스크립트 실행 시 셋팅 가능)
3. **배포 확인:**
   * 이제 마크다운 문서를 쓰고 깃허브에 `git push`하기만 하면 약 1분 뒤에 `https://<organization>.github.io/<repository>` 경로에 검색과 인터랙티브 노드 그래프가 연동된 고급 웹 위키가 즉시 배포됩니다!

---

## 🐳 Docker Compose를 이용한 초경량 로컬 프리뷰 실행 (Zero-Install)

로컬 서버 또는 사내 가상머신(VM)에서 실시간 그래프와 검색창이 있는 웹 위키를 띄워 테스트하거나 전사에 직접 호스팅할 수 있습니다.

이 방식은 질문자님의 로컬 폴더에 `node_modules`나 `package.json` 같은 **개발용 찌꺼기 파일을 단 한 개도 만들지 않고**, 도커 내부에서 모든 빌드 및 서빙을 동적으로 처리하는 초경량 정석 방식입니다.

### 1. 로컬 실행 방법
1. 저장소 폴더(마크다운 문서와 `docker-compose.yml`이 있는 곳)로 진입합니다.
   ```bash
   cd /home/user/knowledgebase
   ```
2. Docker Compose 명령어를 실행하여 컨테이너를 백그라운드에서 구동합니다.
   ```bash
   docker compose up -d
   ```
3. 도커 컨테이너가 가동되는 동안 내부적으로 다음 작업이 자동으로 일어납니다.
   * 초경량 Node.js 환경에서 Quartz 공식 엔진 최신 코드를 실시간으로 복제(Clone)합니다.
   * 로컬의 `./content` 폴더(문서)와 `./quartz.config.yaml`(설정)을 도커 내부로 마운트/주입합니다.
   * 필요한 플러그인과 의존성을 설치한 후 로컬 웹 서버를 구동합니다.

### 2. 웹 접속 및 확인
* 컨테이너가 시작되고 약 30초~1분 뒤 브라우저를 열고 다음 주소로 접속합니다.
  ```text
  http://localhost:8080   (또는 http://<사내서버IP>:8080)
  ```
* 짠! 마크다운 문서 내용과 오른쪽의 실시간 3D 노드 링크 그래프가 연동된 고급 사내 위키 웹사이트를 즉시 확인하실 수 있습니다.

### 3. 컨테이너 중지 방법
테스트를 마치고 서버를 내리고 싶다면 아래 명령어를 입력하세요.
```bash
docker compose down
```

