from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles  
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict
from langchain_utils.main import pipeline

app = FastAPI()
app.mount("/web", StaticFiles(directory="web"), name="web")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    question: str
    history: List[Dict[str, str]] = []

@app.get("/")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/chat")
async def chat(user_input: UserInput):
    question = user_input.question
    history = user_input.history

    context = ""
    for entry in history:
        context += f"Q: {entry['question']}\nA: {entry['answer']}\n"
    context += f"Q: {question}\nA:"
    output = pipeline(context)
    user_input.history.append({"question": question, "answer": output})
    return {"output": output, "history": user_input.history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
