from fastapi import FastAPI
from api.v1.routes import user


app = FastAPI(title="MyCryptPass API")
app.include_router(user.app)