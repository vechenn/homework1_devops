from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

# Путь /
@app.get('/', summary='Root')
def root():
    return {"string": "My name is Aslambek Gaitukaev"}

# Путь /post
@app.post('/post',response_model=Timestamp, summary='Get Post')
def post():
    post_db.append(Timestamp(id=post_db[-1].id + 1, timestamp=post_db[-1].timestamp + 1))
    return post_db[-1]

# Получение списка собак с возможностью получения списка собак определенной породы
@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dog(kind: DogType = None):
    if kind is None:
        return dogs_db.values()
    else:
        return [i for i in dogs_db.values() if i.kind == kind]

# Запись собак, в случае наличия данного pk вывод ошибки 409 (из чата)
# Подразумевается, что ключ и pk всегда равны
@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in [i.pk for i in dogs_db.values()]:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists')
    else:
        num = dog.pk
        dogs_db.update({num: dog})
        return dog

# Получение собаки по pk, в случае отсутствия PK вывод ошибки 409
# Подразумевается, что ключ и pk всегда равны
@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409,
                            detail='No such PK in database')
    else:
        return dogs_db[pk]
    
# Обновление информации о собаке, в случае отсутствия PK вывод ошибки 409
# Подразумевается, что ключ и pk всегда равны
@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog):
    if pk != dog.pk:
        raise HTTPException(status_code=409,
                            detail='Both PK must be same')
    elif pk not in dogs_db.keys():
        raise HTTPException(status_code=409,
                            detail='No such PK in database')
    else:
        dogs_db[pk].name = dog.name
        dogs_db[pk].kind = dog.kind
        return dog