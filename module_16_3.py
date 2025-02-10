# Задача "Имитация работы с БД":
from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_users():
    return users

@app.post('/user/{username}/{age}')
async def post_user(username:Annotated[str,Path(min_length=5, max_length=20, description='Enter username', example='Username')],
                    age:Annotated[int, Path(ge=18, le=120, description='Enter age', example='Age')]):
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] =  f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"

@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id:Annotated[str, Path(description='ID')],
                   username:Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='Username')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='Age')]
):
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User not found')
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"

@app.delete('/user/{user_id}')
async def delete_user(user_id:Annotated[str, Path(description='ID')]
):
    if user_id not in users:
        raise HTTPException(status_code=404, detail='User not found')
    del users[user_id]
    return f"User {user_id} has been deleted"

