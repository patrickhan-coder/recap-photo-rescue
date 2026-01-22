# 🎨 Re:Cap - AI 사진 심폐소생 서비스

망친 사진을 AI가 자연스럽게 복원해주는 웹 서비스입니다.

## 📂 파일 구조

```
claude-code/
├── main.py              # FastAPI 백엔드 서버
├── app.html             # 웹 앱 (사진 업로드 & 복원)
├── index.html           # 랜딩 페이지
├── .env                 # API 키 (생성됨 ✅)
├── requirements.txt     # Python 패키지
└── README.md           # 이 파일
```

---

## ⚡ 빠른 시작 (3단계)

### 1️⃣ Python 패키지 설치

터미널을 열고 아래 명령어를 실행하세요:

```bash
cd /Users/wonjunpatrickhan/claude-code
pip install -r requirements.txt
```

⏱️ 약 30초~1분 소요됩니다.

### 2️⃣ 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload
```

✅ 성공하면 이렇게 보입니다:

```
🎨 Re:Cap - Invisible Photo Rescue
============================================================
API 키 상태: ✅ 설정됨
서버 시작 주소: http://localhost:8000
API 문서: http://localhost:8000/docs
============================================================
```

### 3️⃣ 웹 브라우저에서 앱 열기

**Option A) VSCode에서 바로 열기**
- [app.html](app.html) 파일 우클릭 → "Open with Live Server"

**Option B) 터미널에서 열기**
```bash
open app.html
```

**Option C) 브라우저 주소창에 직접 입력**
```
file:///Users/wonjunpatrickhan/claude-code/app.html
```

---

## 🎯 사용 방법

1. 웹 브라우저에서 `app.html` 열기
2. 사진을 **드래그 앤 드롭** 또는 **클릭해서 업로드**
3. "Re:Cap 현상 중..." 메시지가 나타남 (10~30초 소요)
4. 원본과 복원된 사진을 비교
5. 마음에 들면 **다운로드** 버튼 클릭!

---

## 🔧 문제 해결

### ❌ "REPLICATE_API_TOKEN이 설정되지 않았습니다"
→ `.env` 파일이 있는지 확인하세요. 이미 생성되어 있습니다!

### ❌ "ModuleNotFoundError: No module named 'fastapi'"
→ 패키지를 설치하지 않았습니다:
```bash
pip install -r requirements.txt
```

### ❌ "서버에 연결할 수 없습니다"
→ 백엔드 서버가 실행 중인지 확인하세요:
```bash
python main.py
```

### ❌ "CORS 에러"
→ `app.html`을 **파일로 직접 열지 말고**, Live Server를 사용하거나 서버가 실행된 상태에서 접속하세요.

---

## 📖 API 문서

서버가 실행 중일 때, 브라우저에서 접속:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎬 API 엔드포인트

### `POST /rescue`
사진 복원 API

**Request:**
```bash
curl -X POST "http://localhost:8000/rescue" \
  -F "file=@your_photo.jpg"
```

**Response:**
```json
{
  "success": true,
  "message": "사진 복원이 완료되었습니다!",
  "result_url": "https://replicate.delivery/..."
}
```

---

## 💡 Tip

- **첫 실행은 느릴 수 있습니다** (AI 모델 로딩 때문)
- **고해상도 사진일수록 복원 효과가 좋습니다**
- **인물 사진에 최적화**되어 있습니다

---

## 📝 기술 스택

- **Backend**: FastAPI + Uvicorn
- **AI Engine**: Replicate (Stability AI SDXL)
- **Frontend**: HTML5 + Tailwind CSS + Vanilla JS
- **Python**: 3.8+

---

## 🚀 다음 단계

- [ ] Flutter 모바일 앱 개발
- [ ] 여러 장 일괄 처리
- [ ] 복원 강도 조절 슬라이더
- [ ] 사용자 갤러리 기능

---

**Made with ❤️ by Re:Cap Team**
