from pydantic import BaseModel


class Register(BaseModel):
    title: str
    name: str
    email: str
    phone_number: str
    course_type: str
    confirm_type: str
    hour_appointment: str
    agree_term: str
    submit: str | None
