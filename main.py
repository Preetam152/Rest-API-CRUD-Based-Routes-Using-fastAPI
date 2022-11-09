from fastapi import FastAPI, Depends
import uvicorn
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 
from basiclogging import logging_config

app = FastAPI()


Base.metadata.create_all(engine)

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
def getItem(session : Session = Depends(get_session)):
    item: session.query(models.Item).all()
    return item

@app.get("/{id}")
def getItem(id:int, session:Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item 

#option #1
# @app.post("/")
# def addItem(name:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"name":name}
#     return fakeDatabase

@app.post("/")
def addItem(item:schemas.Item, session : Session = Depends(get_session)):
    item = models.Item(name = item.name) 
    session.add(item)
    session.commit()
    session.refresh(item)

    return item 

#Option #3
# @app.post("/")
# def addItem(body = Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"name":body['name']}
#     return fakeDatabase

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=logging_config)

