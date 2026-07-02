from fastapi import FastAPI

app = FastAPI(title="BudgetFlow API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/expenses")
def get_expenses():
    return [
        {"id": 1, "amount": 250.0, "category": "Food", "date": "2026-07-01"},
        {"id": 2, "amount": 1200.0, "category": "Rent", "date": "2026-07-01"},
    ]