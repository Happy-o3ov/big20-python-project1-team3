## 🧭 Step-by-Step 협업 가이드

### 1️⃣ 개발 환경 준비

- **Anaconda 설치**

  - [Anaconda 공식 사이트](https://www.anaconda.com/products/distribution)에서 설치

  - 설치 후 `Anaconda Navigator` 또는 `conda` 명령어로 가상환경 생성

    ```bash
    conda create -n project_env python=3.10
    conda activate project_env
    ```

- **VS Code 설치 및 설정**

  - [VS Code 다운로드](https://code.visualstudio.com/)
  - 필수 확장 설치:
    - Python
    - Jupyter
    - GitLens
    - Git Graph (GitLens보다 기능은 적지만 간단히 사용하는데 용이)
    - Pylance (자동완성 및 타입 체크)
    - Prettier(코드 포맷터)

- **Git 설치**

  - [Git 공식 사이트](https://git-scm.com/)에서 설치

  - 설치 후 `git config`로 사용자 정보 설정

    ```bash
    git config --global user.name "English Name"
    git config --global user.email "your_email@example.com"
    ```

- **GitHub 계정 생성 및 연동**

  - [GitHub 가입](https://github.com/)
  - 개인 Access Token 생성 후 VS Code에 연동
  - GitHub Desktop을 사용하면 GUI로 쉽게 관리 가능

------

### 2️⃣ 프로젝트 초기화 및 구조 설정

```bash
mkdir python-data-project
cd python-data-project
git init
```

**디렉토리 구조 예시**:

```
python-data-project/
│
├── data/               # 원본 및 전처리 데이터
│   ├── raw/
│   └── processed/
│
├── notebooks/          # Jupyter 노트북
├── src/                # Python 모듈
│   ├── preprocessing.py
│   ├── modeling.py
│   └── visualization.py
│
├── tests/              # 테스트 코드
├── README.md           # 프로젝트 설명
├── requirements.txt    # 패키지 목록
└── .gitignore          # Git 제외 파일
```

------

### 3️⃣ GitHub 협업 워크플로우

- **브랜치 전략**

  - `main`: 배포용
  - `dev`: 개발용
  - `feature/xxx`: 기능별 작업 브랜치

- **작업 흐름**

  1. `feature/eda` 브랜치 생성

     ```bash
     git checkout -b feature/eda
     ```

  2. 작업 후 커밋

     ```bash
     git add .
     git commit -m "[EDA] 데이터 탐색 기능 추가"
     ```

  3. GitHub에 Push

     ```bash
     git push origin feature/eda
     ```

  4. Pull Request 생성 → 팀원 리뷰 → `dev` 브랜치에 병합

- **이슈 관리**

  - GitHub Issues로 작업 분배
  - 라벨: `bug`, `feature`, `question`, `documentation`

------

### 4️⃣ 표준 코드 규칙 (PEP8 기반)

**코드 스타일을 통일하면 협업이 훨씬 쉬워져요!**

| 항목     | 규칙                                          |
| -------- | --------------------------------------------- |
| 들여쓰기 | 4칸 (Space)                                   |
| 변수명   | 소문자 + 언더스코어 (`user_name`)             |
| 함수명   | 소문자 + 언더스코어 (`clean_data`)            |
| 클래스명 | 대문자 카멜케이스 (`DataCleaner`)             |
| 줄 길이  | 79자 이하                                     |
| 공백     | 연산자 앞뒤, 함수 정의 시 괄호 앞뒤 공백 없음 |
| 주석     | 간결하고 명확하게, `#` 뒤에 한 칸 띄우기      |
| 문서화   | 함수마다 docstring 작성                       |

**예시**:

```python
def clean_data(df):
    """
    결측치 제거 및 이상치 처리 함수
    Args:
        df (DataFrame): 원본 데이터
    Returns:
        DataFrame: 정제된 데이터
    """
    df = df.dropna()
    return df
```

**자동화 도구 추천**:

- `black`: 코드 자동 포맷팅
- `flake8`: 스타일 검사
- `isort`: import 정렬

------

## 📁 1. `.ipynb` 파일은 어디에 둘까?

- `notebooks/` 디렉토리 아래에 기능별로 정리:

  ```
  notebooks/
  ├── 01_eda.ipynb
  ├── 02_preprocessing.ipynb
  ├── 03_modeling.ipynb
  └── 99_experiments.ipynb
  ```

- 파일명은 번호 + 기능명으로 통일 (정렬과 가독성 ↑)

------

## 🔄 2. 실행 순서 문제 방지

- **항상 커널 재시작 후 전체 실행** (`Kernel → Restart & Run All`)
- 셀 실행 순서가 꼬이면 결과가 달라질 수 있어요
- 실행 순서 의존성이 있는 셀은 명확히 주석 처리

------

## 🧪 3. 실험용 노트북과 결과 노트북 분리

- `notebooks/`에는 최종 결과만

- `experiments/` 또는 `sandbox/` 디렉토리에 개인 실험용 노트북 저장

- 예:

  ```
  notebooks/
    └── 03_modeling.ipynb
  experiments/
    └── modeling_test_gyeongju.ipynb
  ```

------

## 🧼 4. 노트북 정리 및 커밋 전 체크리스트

- 출력 결과 모두 지우기 (`Cell → All Output → Clear`)
- 불필요한 셀 삭제
- 마크다운 셀로 설명 추가
- 커밋 전 `.ipynb` diff 확인 (VS Code GitLens 또는 [nbdime](https://nbdime.readthedocs.io/en/latest/))

------

## 🔄 5. `.ipynb` → `.py` 변환 전략

- 안정화된 코드는 `.py` 모듈로 분리 (`src/` 디렉토리로 이동)

- 변환 방법:

  ```bash
  jupyter nbconvert --to script notebooks/03_modeling.ipynb
  ```

- 또는 VS Code에서 "Export as Python Script" 기능 사용


📌 참고: `.ipynb`는 JSON 형식이라 Git에서 diff 확인이 어렵고 충돌이 자주 발생해요. 그래서 핵심 로직은 `.py`로 분리하는 게 좋아요.

---

## **📘6. README.md 템플릿**

\# 📊 프로젝트명: \[과제1 회원관리  \] rh

\#\# 📌 개요  
이 프로젝트는 .....  것입니다.

\#\# 🧑‍💻 팀원  
\- 김데이터 (데이터 수집 및 전처리)  
\- 이분석 (EDA 및 통계 분석)  
\- 박시각 (시각화 및 대시보드)  
\- 최모델 (모델링 및 예측)  
\- 정문서 (문서화 및 발표자료)

\#\# 🏗️ 디렉토리 구조

project-name/ ├── data/ │ ├── raw/ │ └── processed/ ├── notebooks/ ├── src/ │ ├── preprocessing.py │ ├── analysis.py │ └── visualization.py ├── tests/ ├── requirements.txt ├── README.md └── .env

\#\# ⚙️ 설치 방법  
\`\`\`bash  
git clone https://github.com/your-team/project-name.git  
cd project-name  
python \-m venv venv  
source venv/bin/activate  \# Windows: venv\\Scripts\\activate  
pip install \-r requirements.txt

\#\# **📈 주요 기능**

* 데이터 전처리 및 결측치 처리  
* 시계열 분석 및 상관관계 분석  
* 지역별 교통량 시각화  
* 예측 모델 구축 (예: ARIMA, XGBoost)

\#\# **📊 결과 예시**

* 혼잡 시간대 히트맵  
* 지역별 교통량 지도 시각화  
* 예측 정확도 비교 그래프

\#\# **🧪 테스트**

pytest tests/

\#\# **📄 라이선스**

MIT License

\---
---

### 5️⃣ 협업 팁

- **매일 짧은 스탠드업 미팅**: 진행 상황 공유
- **Notion/Google Docs**로 회의록 정리
- **Slack/Discord**로 실시간 소통
- **코드 리뷰 문화**: PR마다 최소 1명 이상 리뷰

