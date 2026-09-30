from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Transaction
from schemas import TransactionCreate, ReviewUpdate


app = FastAPI(
    title="Risk Radar API",
    version="1.0"
)


# Allow the React frontend to connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database when the server starts
@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {
        "message": "Risk Radar API is running"
    }


# Get all transactions
@app.get("/transactions")
def get_transactions(
    session: Session = Depends(get_session)
):
    transactions = session.exec(
        select(Transaction)
    ).all()

    return transactions


# Get only flagged transactions
@app.get("/transactions/flagged")
def get_flagged_transactions(
    session: Session = Depends(get_session)
):
    transactions = session.exec(
        select(Transaction).where(Transaction.flagged == True)
    ).all()

    return transactions


# Create a new transaction
@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session)
):
    # Temporary risk calculation.
    # Member 1's fraud rule engine will replace this later.

    risk_score = 0
    risk_level = "LOW"
    flagged = False
    triggered_rules = []

    # Temporary test rule
    if transaction.amount > 100000:
        risk_score += 50
        triggered_rules.append("unusual_amount")

    # Decide risk level
    if risk_score >= 70:
        risk_level = "HIGH"
        flagged = True

    elif risk_score >= 40:
        risk_level = "MEDIUM"
        flagged = True

    # Create database transaction
    db_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        timestamp=transaction.timestamp,
        latitude=transaction.latitude,
        longitude=transaction.longitude,
        risk_score=risk_score,
        risk_level=risk_level,
        flagged=flagged,
        triggered_rules=",".join(triggered_rules),
        review_status="PENDING"
    )

    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)

    return db_transaction


# Review a transaction
@app.patch("/transactions/{transaction_id}/review")
def review_transaction(
    transaction_id: int,
    review: ReviewUpdate,
    session: Session = Depends(get_session)
):
    transaction = session.get(
        Transaction,
        transaction_id
    )

    # Transaction doesn't exist
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    # Only these two statuses are allowed
    allowed_statuses = [
        "REVIEWED",
        "CLEARED"
    ]

    if review.review_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid review status"
        )

    transaction.review_status = review.review_status

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction