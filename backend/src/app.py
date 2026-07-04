from fastapi.middleware.cors import CORSMiddleware

from .routes import user_route
from .routes import message_route
from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import chat_route

app = FastAPI(
    tittle="The unnoficial world cup chatbot",
    description="Multi user chatbot with session autentication using gemini and langchain", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # a origem do seu frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router)
app.include_router(chat_route.router)
app.include_router(message_route.router)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)