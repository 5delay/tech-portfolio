### 1. Overview
> 💡 Docker와 Docker Compose를 활용하여 Frontend와 Backend 개발 환경을 분리, 통합 실행 및 개발이 가능한 환경을 구축

<br/> 

### 2. Configuration

◼︎ **Architecture**
```text
./
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   └── src/
│
└── docker-compose.yml
```

◼︎ **Backend (Node.js)**
* Node.js 20 기반 실행 환경 구성
* API 서버 실행 및 데이터 처리 환경 구축
* 4500번 포트 개방

◼︎ **Frontend (React.js)**
* Node.js 18 기반 실행 환경 구성
* React 개발 환경 구축
* 사용자 인터페이스 및 API 요청 환경 구축
* 3800번 포트 개방

◼︎ **Docker Compose**
* Frontend와 Backend 컨테이너를 통합 관리

<br/> 

### 3. Execution
```bash
docker compose up --build -d
```