from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/", response_model=list[ExpenseOut])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.get("/", response_model=list[ExpenseOut])
def get_expenses(
    db: Session = Depends(get_db),
    category: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
    skip: int = 0,
    limit: int = Query(10, le=100),
):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    sort_column = getattr(Expense, sort_by, Expense.id)
    if order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, update: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()