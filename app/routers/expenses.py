from fastapi import APIRouter, HTTPException
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Temporary in-memory storage — replaced by a real DB tomorrow
expenses_db = [
    {"id": 1, "amount": 250.0, "category": "Food", "date": "2026-07-01"},
    {"id": 2, "amount": 1200.0, "category": "Rent", "date": "2026-07-01"},
]
next_id = 3

@router.get("/", response_model=list[ExpenseOut])
def get_expenses():
    return expenses_db

@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    for e in expenses_db:
        if e["id"] == expense_id:
            return e
    raise HTTPException(status_code=404, detail="Expense not found")

@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseCreate):
    global next_id
    new_expense = {"id": next_id, **expense.model_dump()}
    expenses_db.append(new_expense)
    next_id += 1
    return new_expense

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, update: ExpenseUpdate):
    for e in expenses_db:
        if e["id"] == expense_id:
            e.update(update.model_dump(exclude_unset=True))
            return e
    raise HTTPException(status_code=404, detail="Expense not found")

@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    for i, e in enumerate(expenses_db):
        if e["id"] == expense_id:
            expenses_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Expense not found")