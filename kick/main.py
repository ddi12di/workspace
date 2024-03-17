import os
from http import HTTPStatus

from fastapi import FastAPI, Response
import requests

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PEOPLE_URL = os.environ.get('PEOPLE_URL')  # 'http://127.0.0.1:8000/view/all
LOGIN_URL = os.environ.get('LOGIN_URL')  #http://127.0.0.1:8000/view/login_kick

print(PEOPLE_URL)
print(LOGIN_URL)


def kick():
    response = requests.get(url=LOGIN_URL, json={'username': 'thisiskick', 'password': '123'})

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        return Response(status_code=HTTPStatus.UNAUTHORIZED)

    response = response.json()

    token = response['token']

    resp = requests.get(
        url=PEOPLE_URL,
        headers={
            'Authorization': f'Bearer {token}'
        }
    )

    data = resp.json()
    return data


@app.get("/all")
def getall():
    return kick()


@app.get("/{id}")
def getbyid(url: str, id: int):
    url = url+str(id)
    return kick(url)