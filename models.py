from pydantic import BaseModel


class Register(BaseModel):
    title: str
    name: str
    email: str
    phone_number: int
    course_type: str
    confirm_type: str
    hour_appointment: str
