
#  models.py


from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, DateTime, Enum, UniqueConstraint, Text, CheckConstraint,LargeBinary
from sqlalchemy.orm import relationship
from db import Base 
from datetime import datetime

class Department(Base):
    __tablename__ = "Department"

    Did = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dep = Column(String(100), nullable=False, unique=True)
    role = Column(Enum('Admin', 'Teacher', 'Student'), nullable=False, index=True)

    teachers = relationship("Teacher", back_populates="department", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="department", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="department", cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="department", cascade="all, delete-orphan")  
    notices = relationship("Notice", back_populates="department", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "Student"

    Sid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Did = Column(Integer, ForeignKey("Department.Did", ondelete="CASCADE"), nullable=False)

    name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    pw = Column(String(255), nullable=False)
    u_roll = Column(String(50), unique=True, nullable=False, index=True)
    c_roll = Column(String(50))
    year = Column(Integer, nullable=False)
    sem = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="students")
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")


class Teacher(Base):
    __tablename__ = "Teacher"

    Tid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Did = Column(Integer, ForeignKey("Department.Did", ondelete="CASCADE"), nullable=False)

    name = Column(String(100), nullable=False, index=True)
    name_code = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    pw = Column(String(255), nullable=False)

    department = relationship("Department", back_populates="teachers")
    subject_teacher = relationship("SubjectTeacher", back_populates="teacher", cascade="all, delete-orphan")
    notices = relationship("Notice", back_populates="teacher", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "Subject"

    Sub_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Did = Column(Integer, ForeignKey("Department.Did", ondelete="CASCADE"), nullable=False)

    sub_name = Column(String(100), nullable=False, index=True)
    sub_code = Column(String(50), unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    sem = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="subjects")
    subject_teachers = relationship("SubjectTeacher", back_populates="subject", cascade="all, delete-orphan") 


class SubjectTeacher(Base):
    __tablename__ = "SubjectTeacher"

    STid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Sub_id = Column(Integer, ForeignKey("Subject.Sub_id", ondelete="CASCADE"), nullable=False)
    Tid = Column(Integer, ForeignKey("Teacher.Tid", ondelete="CASCADE"), nullable=False)

    teacher = relationship("Teacher", back_populates="subject_teacher")
    subject = relationship("Subject", back_populates="subject_teachers")  # ✅ FIXED (match Subject's relationship)
    routines = relationship("Routine", back_populates="subject_teacher", cascade="all, delete-orphan")  # ✅ ADDED (Routine FK fix)
    attendances = relationship("Attendance", back_populates="subject_teacher", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('Sub_id', 'Tid', name='uq_subject_teacher'),
    )


class Slot(Base):
    __tablename__ = "Slot"

    Sl_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)
    # day = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), nullable=False, index=True)
    sl_name = Column(String(50), nullable=False, index=True)

    routines = relationship("Routine", back_populates="slot", cascade="all, delete-orphan")  # ✅ FIXED (Routine FK restore)


class Routine(Base):  
    __tablename__ = "Routine"

    R_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    STid = Column(Integer, ForeignKey("SubjectTeacher.STid", ondelete="CASCADE"), nullable=False)
    Sl_id = Column(Integer, ForeignKey("Slot.Sl_id", ondelete="CASCADE"), nullable=False)
    Did = Column(Integer, ForeignKey("Department.Did", ondelete="CASCADE"), nullable=False)
    day = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), nullable=False, index=True)
    
    subject_teacher = relationship("SubjectTeacher", back_populates="routines")
    slot = relationship("Slot", back_populates="routines")
    department = relationship("Department", back_populates="routines")

    __table_args__ = (
        UniqueConstraint('STid', 'Sl_id', 'Did', name='uq_routine'),
    )


class Attendance(Base):
    __tablename__ = "Attendance"

    A_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    STid = Column(Integer, ForeignKey("SubjectTeacher.STid", ondelete="CASCADE"), nullable=False)
    Sid = Column(Integer, ForeignKey("Student.Sid", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    status = Column(Enum('Present', 'Absent', 'Late'), nullable=False, index=True)

    subject_teacher = relationship("SubjectTeacher", back_populates="attendances")
    student = relationship("Student", back_populates="attendances")

    __table_args__ = (
        UniqueConstraint('STid', 'Sid', 'date', name='uq_attendance'),
    )


   
   
class Notice(Base):
    __tablename__ = "Notice"

    N_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    Tid = Column(Integer, ForeignKey("Teacher.Tid", ondelete="CASCADE"), nullable=False)
    Did = Column(Integer, ForeignKey("Department.Did", ondelete="CASCADE"), nullable=False)

    content = Column(Text, nullable=True)
    file = Column(LargeBinary, nullable=True)
    # file = Column(String(100), nullable=True)
    file_type = Column(String(100), nullable=True)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Constraint: At least one of content or file must be non-null
    __table_args__ = (
        CheckConstraint("content IS NOT NULL OR file IS NOT NULL", name="check_content_or_file"),
    )

    teacher = relationship("Teacher", back_populates="notices")
    department = relationship("Department", back_populates="notices")