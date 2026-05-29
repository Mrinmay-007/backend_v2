

# schemas.py

# ===================== FIXED IMPORT =====================
from pydantic import (
    BaseModel,
    StrictStr,
    validator,
    model_validator   # ✅ FIXED
)
# ========================================================

from typing import List, Optional
from datetime import date, time


# ======================================
#       Database Schema
# ======================================

class Department(BaseModel):
    Did: Optional[int] = None
    dep: StrictStr
    role: StrictStr

    @validator('dep')
    def dep_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('Department must contain only alphabetic characters')
        return v

    @validator('role')
    def role_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('Role must contain only alphabetic characters')
        return v

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class Teacher(BaseModel):
    Tid: Optional[int]
    Did: Optional[int]
    name: str
    name_code: str
    email: str
    pw: Optional[str] = None
    role: Optional[str]

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class Student(BaseModel):
    Sid: Optional[int]
    Did: Optional[int]
    dep: Optional[str] = None
    name: str
    email: str
    pw: Optional[str] = None
    u_roll: str
    c_roll: Optional[str] = None
    year: int
    sem: int
    role: str

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class Subject(BaseModel):
    Sub_id: Optional[int]
    Did: Optional[int] = None
    dep: Optional[str] = None
    sub_name: str
    sub_code: str
    year: int
    sem: int

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class SubjectTeacher(BaseModel):
    STid: Optional[int]
    Sub_id: Optional[int]
    Tid: Optional[int]

    sub_name: Optional[str]
    sub_code: Optional[str]
    dep: Optional[str]
    year: Optional[int]
    sem: Optional[int]
    name_code: Optional[str]
    name: Optional[str]
    subject: Optional[str]
    teacher: Optional[str]

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class Slot(BaseModel):
    Sl_id: Optional[int]
    start: time
    end: time
    sl_name: str

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class Routine(BaseModel):
    STid: int
    Sl_id: int
    Did: Optional[int]
    dep: str
    day: str


class Notice(BaseModel):
    N_id: Optional[int]
    Tid: Optional[int]
    Did: Optional[int]
    content: Optional[str] = None
    file: Optional[str] = None
    file_type: Optional[str] = None
    email: str

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


    # ===================== FIXED AREA =====================
    @model_validator(mode="after")
    def check_content_or_file(self):
        if not self.content and not self.file:
            raise ValueError("Either content or file must be provided")
        return self
    # ======================================================


class Attendance(BaseModel):
    Aid: Optional[int] = None
    Sub_id: Optional[int] = None
    Sid: Optional[int] = None
    Tid: int
    date: date
    status: str

    # ===================== FIXED =====================
    class Config:
        from_attributes = True
    # ================================================


class AttendanceUpdate(BaseModel):
    new_status: str


# ==============================================
#    Authentication
# ==============================================

class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class ResetPwRequest(BaseModel):
    old_pw: str
    new_pw: str
