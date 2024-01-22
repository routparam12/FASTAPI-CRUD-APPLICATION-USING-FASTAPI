from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, sessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    Session= sessionLocal()
    try:
        yield Session
    finally:
        Session.close()

app= FastAPI()


fakeDatabase ={
    1:{'task':'clean car'},
    2:{'task':'write blog'},
    3:{'task':'start stream'}

}
@app.get("/")
def getItems(session:Session= Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get('/{id}')
def getitem(id:int,session:Session= Depends(get_session)):
    item =session.query(models.Item).get(id)
    return fakeDatabase[id]



#option 1

# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":item.task}
#     return fakeDatabase


# option 2
@app.post("/")
def addItem(item:schemas.Item,session:Session= Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#option 3
# @app.post("/")
# def addItem(body =Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":body['task']}
#     return fakeDatabase

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session:Session= Depends(get_session)):
    itemObj = session.query(models.Item).get(id)
    itemObj.task =item.task
    session.commit()
    return itemObj


@app.delete("/{id}")
def deleteItem(id:int, session:Session= Depends(get_session)):
    itemObj=session.query(models.Item).get(id)
    session.delete(itemObj)
    session.commit()
    session.close()
    return 'item was deleted ..'
