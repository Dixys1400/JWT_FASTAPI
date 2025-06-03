from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import SignInSchema, SignUpSchema
from jwtsign import  decode, sign, hash_password, verify_password
from models import User, Base




app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def sign_up(request: SignUpSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=request.name,
        email=request.email,
        hashed_password=hash_password(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": sign(user.email), "token_type": "bearer"}


@app.post("/signin")
def sign_in(request: SignInSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": sign(user.email), "token_type": "bearer"}


@app.get("me")
def get_me(decoded: dict = Depends(decode), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == decoded["email"]).first()
    return {"name": user.name, "email": user.email}


@app.post("/authtest")
def auth_test(decoded: str = Depends(decode)):
    return decoded