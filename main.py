from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

# ! TIPE DATA
class DataCuaca(BaseModel):
    username: str
    waktu: str
    kelembaban: int

class DataUser(BaseModel):
    username: str
    password: str

class DataListrik(BaseModel):
    username: str
    tanggal: str
    jam: int
    jumlahListrik: float

# ! READ FILE
json_filename = "Data.json"
with open(json_filename, "r") as read_file: 
    data = json.load(read_file)

# ! FASTAPI
app = FastAPI()

#! Routing data_cuaca
@app.post("/data_cuaca")
async def create_data_cuaca(data_cuaca: DataCuaca):
    data['data_cuaca'].append(data_cuaca.dict())
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)
    return data_cuaca

@app.get("/data_cuaca")
async def get_data_cuaca():
    return data['data_cuaca']

@app.get("/data_cuaca/{username}")
async def get_data_cuaca(username: str):
    for cuaca in data['data_cuaca']:
        if cuaca["username"] == username:
            return cuaca
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/data_cuaca/{username}")
async def delete_data_cuaca(username: str):
    for cuaca in data['data_cuaca']:
        if cuaca["username"] == username:
            data['data_cuaca'].remove(cuaca)
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/data_cuaca")
async def update_data_cuaca(data_cuaca: DataCuaca):
    for cuaca in data['data_cuaca']:
        if cuaca["username"] == data_cuaca.username:
            cuaca["waktu"] = data_cuaca.waktu
            cuaca["kelembaban"] = data_cuaca.kelembaban
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")


#! Routing data_user
@app.post("/data_user")
async def create_data_user(data_user: DataUser):
    data['data_user'].append(data_user.dict())
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)
    return data_user

@app.get("/data_user")
async def get_data_user():
    return data['data_user']

@app.get("/data_user/{username}")
async def get_data_user(username: str):
    for user in data['data_user']:
        if user["username"] == username:
            return user
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/data_user/{username}")
async def delete_data_user(username: str):
    for user in data['data_user']:
        if user["username"] == username:
            data['data_user'].remove(user)
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/data_user")
async def update_data_user(data_user: DataUser):
    for user in data['data_user']:
        if user["username"] == data_user.username:
            user["password"] = data_user.password
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

#! Routing data_listrik
@app.post("/data_listrik")
async def create_data_listrik(data_listrik: DataListrik):
    data['data_listrik'].append(data_listrik.dict())
    with open(json_filename, "w") as write_file:
        json.dump(data, write_file, indent=4)
    return data_listrik

@app.get("/data_listrik")
async def get_data_listrik():
    return data['data_listrik']

@app.get("/data_listrik/{username}")
async def get_data_listrik(username: str):
    for listrik in data['data_listrik']:
        if listrik["username"] == username:
            return listrik
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/data_listrik/{username}")
async def delete_data_listrik(username: str):
    for listrik in data['data_listrik']:
        if listrik["username"] == username:
            data['data_listrik'].remove(listrik)
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/data_listrik")
async def update_data_listrik(data_listrik: DataListrik):
    for listrik in data['data_listrik']:
        if listrik["username"] == data_listrik.username:
            listrik["tanggal"] = data_listrik.tanggal
            listrik["jam"] = data_listrik.jam
            listrik["jumlahListrik"] = data_listrik.jumlahListrik
            with open(json_filename, "w") as write_file:
                json.dump(data, write_file, indent=4)
            return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")



