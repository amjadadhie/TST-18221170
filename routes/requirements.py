from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import json
from models.requirements import DataListrik, DataCuaca
from models.users import UserJSON
from routes.auth import get_current_user

# Load data from the JSON file
with open("data/requirement.json", "r") as json_file:
    data = json.load(json_file)

dataListrik = data.get("data_listrik", [])
dataCuaca = data.get("data_cuaca", [])

umum_router = APIRouter(tags=["Umum"])
administrator_router = APIRouter(tags=["Administrator Only"])


#GET
@umum_router.get("/data_listrik", response_model=List[DataListrik])
async def retrieve_all_data_listrik() -> List[DataListrik]:
    return dataListrik

@umum_router.get("/data_cuaca", response_model=List[DataCuaca])
async def retrieve_all_data_cuaca() -> List[DataCuaca]:
    return dataCuaca


# getter data_listrik and data_cuaca by username
@umum_router.get("/data_listrik/{username}", response_model=List[DataListrik])
async def retrieve_data_listrik_by_username(username: str) -> List[DataListrik]:
    return [req for req in dataListrik if req.get("username") == username]

@umum_router.get("/data_cuaca/{username}", response_model=List[DataCuaca])
async def retrieve_data_cuaca_by_username(username: str) -> List[DataCuaca]:
    return [req for req in dataCuaca if req.get("username") == username]

#----------------------------------------------------------------#

#POST

@administrator_router.post("/data_listik",  response_model=DataListrik)
async def create_data_listrik(
    data_listrik: DataListrik,
    user: UserJSON = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create new data"
        )
    new_data_listrik = {
        "username": data_listrik.username,
        "tanggal": data_listrik.tanggal,
        "jam": data_listrik.jam,
        "jumlahListrik": data_listrik.jumlahListrik
    }
    dataListrik.append(new_data_listrik)
    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_listrik"] = dataListrik
        json.dump(data, json_file, indent=4)
    return new_data_listrik

@administrator_router.post("/data_cuaca",  response_model=DataCuaca)
async def create_data_cuaca(
    data_cuaca: DataCuaca,
    user: UserJSON = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create new data"
        )
    new_data_cuaca = {
        "username": data_cuaca.username,
        "waktu": data_cuaca.waktu,
        "kelembaban": data_cuaca.kelembaban
    }
    dataCuaca.append(new_data_cuaca)
    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_cuaca"] = dataCuaca
        json.dump(data, json_file, indent=4)
    return new_data_cuaca


#----------------------------------------------------------------#

# #PUT
@administrator_router.put("/edit_listrik", response_model=DataListrik)
async def update_data_listrik(
    data_listrik: DataListrik,
    user: UserJSON = Depends(get_current_user)
):
    existing_data_listrik = next((req for req in dataListrik if req.get("id") == id), None)

    if not existing_data_listrik:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data with supplied username does not exist"
        )
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this data"
        )

    # Update the fields, except 'username' and 'id'
    for key, value in data_listrik.dict().items():
        if key not in ["id", "username"]:
            existing_data_listrik[key] = value

    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_listrik"] = dataListrik

    return DataListrik(**existing_data_listrik)

@administrator_router.put("/edit_cuaca", response_model=DataCuaca)
async def update_data_cuaca(
    data_cuaca: DataCuaca,
    user: UserJSON = Depends(get_current_user)
):
    existing_data_cuaca = next((req for req in dataCuaca if req.get("id") == id), None)

    if not existing_data_cuaca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data with supplied username does not exist"
        )
    
    if  not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this data"
        )

    # Update the fields, except 'username' and 'id'
    for key, value in data_cuaca.dict().items():
        if key not in ["id", "username"]:
            existing_data_cuaca[key] = value

    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_cuaca"] = dataCuaca

    return DataCuaca(**existing_data_cuaca)

#----------------------------------------------------------------#

#DELETE
@administrator_router.delete("delete_listrik/{username}")
def delete_data_listrik(username: str, user: UserJSON = Depends(get_current_user)):
    existing_data_listrik = next((req for req in dataListrik if req.get("username") == username), None)

    if  not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this data"
        )

    if not existing_data_listrik:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data with supplied username does not exist"
        )

    dataListrik.remove(existing_data_listrik)

    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_listrik"] = dataListrik
        json.dump(data, json_file, indent=4)

    return existing_data_listrik

@administrator_router.delete("delete_cuaca/{username}")
async def delete_data_cuaca(username: str, user: UserJSON = Depends(get_current_user)):
    existing_data_cuaca = next((req for req in dataCuaca if req.get("username") == username), None)

    if  not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit this data"
        )

    if not existing_data_cuaca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data with supplied username does not exist"
        )

    dataCuaca.remove(existing_data_cuaca)

    # Write the updated data to the JSON file
    with open("data/requirement.json", "w") as json_file:
        data["data_cuaca"] = dataCuaca
        json.dump(data, json_file, indent=4)

    return existing_data_cuaca    
#----------------------------------------------------------------#
