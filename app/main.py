from fastapi import FastAPI
from app.sqs_consumer import start_consumer_in_background

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!"}

@app.get("/test")
async def test():
    return {"message": "test"}


# ▶️ 앱 시작 시 자동으로 실행되는 이벤트 핸들러
@app.on_event("startup")
def startup_event():
    # ▶️ 백그라운드에서 SQS consumer 시작
    start_consumer_in_background()