from fastapi import FastAPI
from app.routers import expenses

app = FastAPI(title="BudgetFlow API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(expenses.router)