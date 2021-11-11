import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routes.tasks_routes import tasks as tasksRouter
from routes.user_routes import auth as authRouter
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client_url = os.getenv("CLIENT_URL")
origins = [client_url, "http://localhost", "http://localhost:8080", "http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(authRouter)
app.include_router(tasksRouter)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TASKI APP",
        version="1.0.0",
        description="Task management application",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/")
def root():
    return []

# DB config
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")


register_tortoise(
    app,
    db_url= os.getenv("DATABASE_URL"),
    modules={"models": ["models.task_model", "models.user_model"]},
    generate_schemas=True,
    add_exception_handlers=True
)