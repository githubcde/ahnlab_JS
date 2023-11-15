import uuid
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: str

class OverviewResponse(BaseModel):
    message: str

class StatisticsResponse(BaseModel):
    total_items: int
    # 여기에 다른 통계 데이터를 추가할 수 있습니다.

class RecommendationResponse(BaseModel):
    items: List[Item]

# CSV 데이터를 저장할 전역 변수를 초기화합니다.
catalog_data = None

# CSV 파일 로딩 함수
@app.on_event("startup")
async def load_catalog_data():
    global catalog_data
    catalog_file = './data/OutdoorClothingCatalog_1000.csv'  # 실제 경로로 변경 필요
    catalog_data = pd.read_csv(catalog_file)

# 상품 정보 개괄을 제공하는 엔드포인트
@app.get("/api/overview", response_model=OverviewResponse)
async def get_overview():
    return OverviewResponse(message="안녕하세요. 아웃도어 전문 매장입니다. 현재 저희는 다양한 제품을 다루고 있으며, 필요한 제품을 자동으로 안내해드리고 있습니다.")

# 상품 통계 정보를 제공하는 엔드포인트
@app.get("/api/statistics", response_model=StatisticsResponse)
async def get_statistics():
    total_items = len(catalog_data)
    return StatisticsResponse(total_items=total_items)

# 제품 추천을 제공하는 엔드포인트
@app.get("/api/recommendation", response_model=RecommendationResponse)
async def get_recommendation():
    recommended_items = catalog_data.sample(n=5)
    recommendations = recommended_items[['name', 'description']].to_dict(orient='records')
    return RecommendationResponse(items=[Item(name=item['name'], description=item['description']) for item in recommendations])

# 토큰 발급 엔드포인트 (예시로 추가됨, 실제 로직 구현 필요)
@app.get("/api/new_token")
async def new_token():
    token = str(uuid.uuid4())
    # 여기에 토큰을 저장하고 관리하는 로직을 추가합니다.
    return {"token": token}

# 프롬프트 처리 엔드포인트 (예시로 추가됨, 실제 로직 구현 필요)
@app.post("/api/prompt")
async def process_prompt(prompt: str, token: str):
    # 여기에 토큰을 검증하고 프롬프트를 처리하는 로직을 추가합니다.
    return {"result": "여기에 처리된 프롬프트 결과를 반환합니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)