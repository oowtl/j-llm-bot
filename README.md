# j-llm-bot

LLM chat bot to use Crew AI

## 1. 프로젝트 세팅

## 2. 프로젝트 구성

- 가상환경 설정 => Docker Container 설정 (개념 : 공간을 분리해서 따로 관리하겠다.)
- python 3.8으로 개발을 했는데 배포할 서버가 3.3 버전이라면??
  - 이건.. 배포할 때 알 수 있다..
  - 그런데 이걸 로컬에서 작업하는 환경과 호스트 서버에서 작업하는 환경을 일치시켜줘야 한다.
    - 이 작업을 Docker에서 하는 것이 맞지만.. 이번에는 venv 에서 하는 것으로 한다.

```terminal
# 가상환경 실행
python3.12 -m venv .venv

# 실행 mac
source .venv/bin/activate
```

## 3. 프로젝트

### 3-1. Ollama 모델 + CrewAI

(1) Ollama 다운로드
(2) ollama 를 통해서 llm 다운로드

> ollama pull llama3.1
> ollama pull phi3:3.8b
>
> ollama run phi3:3.8b

### 3-2. CrewAI 사용하기

- 언어 모델의 API 를 관리해준다.

> pip install crewai crewai-tools
> pip install langchain-ollama

1. 실행순서 관리

### 3-2. Flask 사용해서 기본적인 챗봇

# RAG : 확장하는 기능 => PDF, DB 에서 들고와서 답변하는 기능

DB 와 연동 가능, 외부 API 불러와서 사용 가능
