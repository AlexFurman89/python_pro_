from typing import Optional, List, Tuple
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from database import get_session
from models import User, Income, Spend

class UserRepo:
    @staticmethod
    def get_by_email_password(email: str, password: str) -> Optional[Tuple[int, str, str, str]]:
        with get_session() as db:  # type: Session
            user = db.execute(
                select(User).where(User.email == email, User.password == password)
            ).scalar_one_or_none()
            if not user:
                return None
            return (user.id, user.name, user.surname, user.email)

    @staticmethod
    def create(name: str, surname: str, email: str, password: str) -> int:
        with get_session() as db:
            u = User(name=name, surname=surname, email=email, password=password)
            db.add(u)
            db.flush()
            return u.id

class IncomeRepo:
    @staticmethod
    def list_by_user(user_id: int) -> List[Tuple[int, float, str, str]]:
        with get_session() as db:
            rows = db.execute(
                select(Income).where(Income.user_id == user_id).order_by(desc(Income.id))
            ).scalars().all()
            return [(r.id, r.amount, r.description, r.date.isoformat() if r.date else "") for r in rows]

    @staticmethod
    def add(user_id: int, amount: float, description: str = "") -> int:
        with get_session() as db:
            item = Income(user_id=user_id, amount=amount, description=description)
            db.add(item)
            db.flush()
            return item.id

class SpendRepo:
    @staticmethod
    def list_by_user(user_id: int) -> List[Tuple[int, float, str, str]]:
        with get_session() as db:
            rows = db.execute(
                select(Spend).where(Spend.user_id == user_id).order_by(desc(Spend.id))
            ).scalars().all()
            return [(r.id, r.amount, r.description, r.date.isoformat() if r.date else "") for r in rows]

    @staticmethod
    def add(user_id: int, amount: float, description: str = "") -> int:
        with get_session() as db:
            item = Spend(user_id=user_id, amount=amount, description=description)
            db.add(item)
            db.flush()
            return item.id