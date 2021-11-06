import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from config.openapi import custom_openapi
from routes.tasks_routes import tasks as tasksRouter
from routes.user_routes import auth as authRouter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client_url = os.getenv("CLIENT_URL")
origins = [client_url, "http://localhost", "http://localhost:8000"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(authRouter)
app.include_router(tasksRouter)
app.openapi = custom_openapi(app)



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
    db_url=f"postgres://{user}:{password}@{host}:{port}/{db_name}",
    modules={"models": ["models.task_model", "models.user_model"]},
    generate_schemas=True,
    add_exception_handlers=True
)