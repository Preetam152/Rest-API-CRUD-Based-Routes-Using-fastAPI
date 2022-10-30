from fastapi import FastAPI, Body, Depends 
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 

Base.metadate.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session

    finally:
        session.close()



app = FastAPI()

fakeDatabase = {
    1:{'name': 'Harry Potter and the Order of the Phoenix'},
    2:{'name': 'The Lord of the Rings: The Fellowship of the Ring'},
    3:{'name': 'Avengers: Endgame'}
}

@app.get("/")
def getItems(session : Session = Depends(get_session)):
    items: session.query(models.Item).all()
    return fakeDatabase

@app.get("/{id}")
def getItem(id:int, session:Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item 

@app.post("/")
def addItem(item:schemas.Item, session : Session = Depends(get_session)):
    item = models.Item(name= item.name) 
    session.add(item)
    session.commit()
    session.refresh()
    
    return item 

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session : Session = Depends(get_session)):
    itemObject= session.query(models.Item).get(id)
    itemObject.name = item.name 
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session : Session = Depends(get_session)):
    itemObject= session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted...'

