from fastapi import FastAPI
import requests

app = FastAPI()


def kick(url: str = 'http://people:8000/view/all'):
    resp = requests.get(url=url)
    data = resp.json()
    return data

@app.get("/all")
def getall():
    return kick()

@app.get("/{id}")
def getbyid(url: str, id: int):
    url = url+str(id)
    return kick(url)