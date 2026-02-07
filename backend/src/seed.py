from sqlmodel import Session, create_engine, select
from src.models import User
from src.db import DATABASE_URL

engine = create_engine(DATABASE_URL)

def seed():
    with Session(engine) as session:
        # Admin
        admin = session.exec(select(User).where(User.email == "admin@example.com")).one_or_none()
        if not admin:
            admin = User(email="admin@example.com", name="Admin User", role="admin")
            session.add(admin)
            print("Created admin user")
        
        # Student
        student = session.exec(select(User).where(User.email == "student@example.com")).one_or_none()
        if not student:
            student = User(email="student@example.com", name="Student User", role="student")
            session.add(student)
            print("Created student user")
            
        # Staff
        staff = session.exec(select(User).where(User.email == "staff@example.com")).one_or_none()
        if not staff:
            staff = User(email="staff@example.com", name="Staff User", role="staff")
            session.add(staff)
            print("Created staff user")
            
        session.commit()

if __name__ == "__main__":
    seed()
