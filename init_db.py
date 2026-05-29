from db import SessionLocal
import models
from methods.hashing import Hash
import json

def insert_defaults():
    db = SessionLocal()
    try:
        with open('pw.json', "r") as file:
            data = json.load(file)

        admin_pw = data.get("admin_password")

        # 1️⃣ Create default department
        dept = db.query(models.Department).filter_by(dep="ADMIN").first()
        if not dept:
            dept = models.Department(dep="ADMIN", role="Admin")
            db.add(dept)
            db.commit()
            db.refresh(dept)
            print("✅ Default department created")

        # 2️⃣ Create default teacher
        default_teacher = db.query(models.Teacher).filter_by(
            name="default", Did=dept.Did
        ).first()

        if not default_teacher:
            teacher = models.Teacher(
                Did=dept.Did,
                name="default",
                name_code="default",
                email="admin@123",
                pw=Hash.bcrypt(admin_pw)
            )
            db.add(teacher)
            db.commit()
            print("✅ Default teacher created")
        else:
            print("ℹ Default teacher already exists")

    finally:
        db.close()