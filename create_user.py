from sqlmodel import Session, select
from app.database import engine
from app.models import User
from app.auth import get_password_hash
with Session(engine) as session:
existing = session.exec(select(User).where(User.email == "test@example.com")).first()
if not existing:
user = User(
email="test@example.com",
hashed_password=get_password_hash("password123"),
is_active=True
)
session.add(user)
session.commit()
print("Test user created successfully!")
else:
print("Test user already exists.")
