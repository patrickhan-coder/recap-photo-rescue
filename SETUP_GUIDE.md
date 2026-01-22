# 🚀 Re:Cap 웹 버전 설치 가이드

## 1단계: Python 패키지 설치

터미널을 열고 아래 명령어를 **한 줄씩** 실행하세요:

```bash
# 현재 폴더로 이동
cd /Users/wonjunpatrickhan/claude-code

# 필요한 패키지 모두 설치 (30초~1분 소요)
pip install -r requirements.txt
```

## 2단계: Replicate API 키 발급받기

### 1) Replicate 웹사이트 접속
- 브라우저에서 이동: https://replicate.com
- 우측 상단 **"Sign in"** 클릭
- GitHub 계정으로 로그인 (무료!)

### 2) API 키 복사
- 로그인 후, 우측 상단 프로필 아이콘 클릭
- **"API tokens"** 선택
- 또는 직접 이동: https://replicate.com/account/api-tokens
- **"Create token"** 버튼 클릭
- 생성된 키를 복사 (예: `r8_xxxxxxxxxxxxxxxxxxxxx`)

### 3) .env 파일 만들기
- VSCode에서 현재 폴더에 `.env` 파일 생성
- 아래 내용을 붙여넣고, `your_api_key_here` 부분에 복사한 키를 넣으세요:

```
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx
```

⚠️ **주의:** 키는 절대 공유하지 마세요! (GitHub에 올리지 말 것)

## 3단계: 완료 확인

터미널에서 아래 명령어를 실행해서 에러가 없으면 성공!

```bash
python -c "import fastapi, replicate; print('✅ 설치 완료!')"
```

---

다음 단계로 `main.py` 작성을 진행하세요! 🎉
