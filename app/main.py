from fastapi import FastAPI
from app.db_init import init_db
from app.seeds.seed_roles import seed_roles
from app.routers import auth_router

def create_app():
    app = FastAPI()
    init_db()
    seed_roles()
    app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voley Tracker API"}