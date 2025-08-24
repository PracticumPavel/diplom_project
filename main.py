from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud
import uvicorn


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/items/")
async def create_item(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_item(db, name, description)
    items = crud.get_items(db)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
