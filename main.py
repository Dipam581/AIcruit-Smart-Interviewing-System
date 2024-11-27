from fastapi import FastAPI, Form, Request
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Register

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")



@app.post("/submit")
async def create_item(request: Request):
    form_data = await request.form()
    form_data_dict = dict(form_data)
    print(form_data_dict)
    return {"message": "Data received successfully", "data": form_data_dict}
