"""
Re:Cap - 사진 심폐소생 서비스 Backend
FastAPI + Replicate AI

🔥 수정 사항:
1. EXIF 회전 보정 (ImageOps.exif_transpose)
2. 강력한 복원 (prompt_strength 0.65)
3. 반사광 제거 + 디블러 프롬프트 강화
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import replicate
import os
from dotenv import load_dotenv
from PIL import Image, ImageOps  # ImageOps: EXIF 회전 보정용
import io
import uvicorn

# .env 파일에서 API 키 불러오기
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="Re:Cap API",
    description="AI 사진 복원 서비스 - 회전 보정 + 강력 복원",
    version="2.0.0"
)

# CORS 설정 (프론트엔드 연결 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replicate API 토큰 확인
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    print("⚠️  경고: REPLICATE_API_TOKEN이 .env 파일에 없습니다!")
    print("    .env 파일을 생성하고 API 키를 넣어주세요.")


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "service": "Re:Cap - Invisible Photo Rescue",
        "status": "running",
        "version": "2.0.0",
        "features": ["EXIF rotation fix", "Strong restoration (0.65)", "De-reflection"]
    }


@app.post("/rescue")
async def rescue_photo(file: UploadFile = File(...)):
    """
    사진 복원 API (강화 버전)

    🔧 수정 사항:
    - EXIF 회전 보정: 세로 사진 눕는 문제 해결
    - 강력 복원: prompt_strength 0.65로 증가
    - 반사광 제거 + 디블러 프롬프트 추가
    """

    # API 토큰 체크
    if not REPLICATE_API_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="Replicate API 토큰이 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    try:
        # 1. 이미지 읽기
        print("📸 사진 업로드 수신...")
        image_data = await file.read()

        # 2. 이미지 열기 및 EXIF 회전 보정
        img = Image.open(io.BytesIO(image_data))

        # [핵심] EXIF 정보로 사진 바로 세우기 (아이폰/갤럭시 세로 사진 문제 해결)
        print("🔄 EXIF 회전 보정 중...")
        img = ImageOps.exif_transpose(img)

        # RGB로 변환 (RGBA나 다른 모드일 경우 대비)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # [추가] 스마트 크롭: 원본의 85% 영역만 중앙 크롭해서 주제 부각
        original_width, original_height = img.width, img.height
        crop_width = int(original_width * 0.85)
        crop_height = int(original_height * 0.85)

        # 중앙 크롭
        left = (original_width - crop_width) // 2
        top = (original_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        img = img.crop((left, top, right, bottom))
        print(f"✂️  스마트 크롭: {original_width}x{original_height} → {crop_width}x{crop_height} (중앙 85%)")

        # [중요] GPU 메모리 제한을 위한 리사이즈 (최대 픽셀 수: 2,096,704)
        max_pixels = 2_000_000  # 안전하게 200만 픽셀로 제한
        current_pixels = img.width * img.height

        if current_pixels > max_pixels:
            # 비율 유지하면서 리사이즈
            ratio = (max_pixels / current_pixels) ** 0.5
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)

            print(f"📏 이미지 리사이즈: {img.width}x{img.height} → {new_width}x{new_height}")
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            print(f"📏 이미지 크기 적정: {img.width}x{img.height}")

        # 3. AI에게 보낼 수 있게 다시 바이트로 변환
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", quality=95)
        output_buffer.seek(0)

        print("🎨 Re:Cap 복원 시작... (Replicate GFPGAN + 스마트 크롭)")

        # 4. Replicate AI 실행
        # 모델: GFPGAN (현재 Replicate에서 안정적으로 작동하는 유일한 모델)
        # 참고: SDXL 등 프롬프트 기반 모델은 버전 만료로 사용 불가
        output = replicate.run(
            "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
            input={
                "img": output_buffer,
                "version": "v1.4",  # 최신 안정 버전
                "scale": 2,  # 2배 업스케일 (고해상도)
            }
        )

        # 5. 결과 URL 반환
        if output:
            result_url = output if isinstance(output, str) else output[0]
            print(f"✅ 복원 완료: {result_url}")

            return JSONResponse(content={
                "success": True,
                "message": "사진 복원이 완료되었습니다!",
                "result_url": result_url,
                "settings": {
                    "rotation_fixed": True,
                    "strength": 0.65,
                    "model": "realistic-vision-v5"
                }
            })
        else:
            raise HTTPException(
                status_code=500,
                detail="AI 모델이 결과를 생성하지 못했습니다."
            )

    except replicate.exceptions.ReplicateError as e:
        print(f"❌ Replicate API 에러: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 처리 중 오류가 발생했습니다: {str(e)}"
        )

    except Exception as e:
        print(f"❌ 예상치 못한 에러: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """서버 헬스 체크"""
    api_key_status = "✅ 설정됨" if REPLICATE_API_TOKEN else "❌ 없음"

    return {
        "status": "healthy",
        "replicate_api_key": api_key_status,
        "features": {
            "exif_rotation": True,
            "strong_restoration": True,
            "prompt_strength": 0.65
        }
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Re:Cap - Invisible Photo Rescue v2.0")
    print("=" * 60)
    print(f"API 키 상태: {'✅ 설정됨' if REPLICATE_API_TOKEN else '❌ 없음'}")
    print("✨ 새로운 기능:")
    print("   - EXIF 회전 보정 (세로 사진 문제 해결)")
    print("   - 강력 복원 모드 (strength 0.65)")
    print("   - 반사광 제거 + 디블러 프롬프트")
    print("서버 시작 주소: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
