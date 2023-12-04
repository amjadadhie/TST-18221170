from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import json
from models.requirements import DataListrik, DataCuaca, realEstate
from models.users import UserJSON
from routes.auth import get_current_user
import httpx

# Load data from the JSON file
with open("data/requirement.json", "r") as json_file:
    data = json.load(json_file)

dataListrik = data.get("data_listrik", [])
dataCuaca = data.get("data_cuaca", [])

administrator_router = APIRouter(tags=["CRUD"])
umum_router = APIRouter(tags=["GET"])
raka_router = APIRouter(tags=["Real Estate"])

#GET
@umum_router.get("/data_listrik", response_model=List[DataListrik])
async def retrieve_all_data_listrik() -> List[DataListrik]:
    return dataListrik

@umum_router.get("/data_cuaca", response_model=List[DataCuaca])
async def retrieve_all_data_cuaca() -> List[DataCuaca]:
    return dataCuaca

#API RAKA
#GET ALL REAL ESTATE
@raka_router.get("/real_estate")
async def get_real_estate_data(user: UserJSON = Depends(get_current_user)):
    try:
        # Lakukan permintaan HTTP ke API eksternal
        async with httpx.AsyncClient() as client:
            response = await client.get("https://tst-auth-18221094.victoriousplant-40d1c733.australiaeast.azurecontainerapps.io/getters/realEstate")
        
        # Periksa apakah permintaan berhasil (kode status 200)
        response.raise_for_status()

        # Ubah respons JSON menjadi bentuk yang sesuai dengan model Anda
        external_real_estate_data = response.json()
        
        return external_real_estate_data

    except httpx.HTTPError as e:
        # Tangani kesalahan HTTP jika terjadi
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    except Exception as e:
        # Tangani kesalahan umum jika terjadi
        raise HTTPException(status_code=500, detail=str(e))

# getter data_listrik and data_cuaca by username
@umum_router.get("/data_listrik/{username}", response_model=List[DataListrik])
async def retrieve_data_listrik_by_username(username: str) -> List[DataListrik]:
    return [req for req in dataListrik if req.get("username") == username]

@umum_router.get("/data_cuaca/{username}", response_model=List[DataCuaca])
async def retrieve_data_cuaca_by_username(username: str, user: UserJSON = Depends(get_current_user)) -> List[DataCuaca]:
    # Dapatkan data cuaca sesuai dengan username
    user_data_cuaca = [req for req in dataCuaca if req.get("username") == username]

    return user_data_cuaca
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

#Post Real Estate Data
@raka_router.post("/post/realEstate", response_model= realEstate)
async def add_real_estate(change: realEstate, user: UserJSON = Depends(get_current_user)):
    # Check if the user is an admin or if the requirement belongs to the authenticated user
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a new real estate"
        )
    
    try:
        change_dict = change.dict()
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid input data")

    print(user.friend_token)

    headers = {
        "Authorization" : f"Bearer {user.friend_token}"
    }

    try:
        # Lakukan permintaan HTTP ke API eksternal
        async with httpx.AsyncClient() as client:
            response = await client.post("https://tst-auth-18221094.victoriousplant-40d1c733.australiaeast.azurecontainerapps.io/admin/realEstate", json=change_dict, headers=headers)
        
        # Periksa apakah permintaan berhasil (kode status 200)
        response.raise_for_status()

        # Ubah respons JSON menjadi bentuk yang sesuai dengan model Anda
        external_real_estate_data = response.json()
        
        return external_real_estate_data

    except httpx.HTTPError as e:
        # Tangani kesalahan HTTP jika terjadi
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    except Exception as e:
        # Tangani kesalahan umum jika terjadi
        raise HTTPException(status_code=500, detail=str(e))

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
# PUT real estate
@raka_router.put("/realEstate", response_model=realEstate)
async def update_real_estate(id: int, newData: realEstate, user: UserJSON = Depends(get_current_user)):
    try:
        change_dict = newData.dict()
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid input data")

    url = f"https://tst-auth-18221094.victoriousplant-40d1c733.australiaeast.azurecontainerapps.io/admin/realEstate/{id}"

    headers = {
        "Authorization" : f"Bearer {user.friend_token}"
    }
 
    try:
        # Lakukan permintaan HTTP ke API eksternal
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=change_dict, headers=headers)
        
        # Periksa apakah permintaan berhasil (kode status 200)
        response.raise_for_status()

        # Ubah respons JSON menjadi bentuk yang sesuai dengan model Anda
        external_real_estate_data = response.json()
        
        return external_real_estate_data

    except httpx.HTTPError as e:
        # Tangani kesalahan HTTP jika terjadi
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    except Exception as e:
        # Tangani kesalahan umum jika terjadi
        raise HTTPException(status_code=500, detail=str(e))


# #PUT
@administrator_router.put("/edit_listrik", response_model=DataListrik)
async def update_data_listrik(
    data_listrik: DataListrik,
    user: UserJSON = Depends(get_current_user)
):
    existing_data_listrik = data.get("data_listrik", [])

    for i, existing_data in enumerate(existing_data_listrik):
        if existing_data.get("username") == data_listrik.username:
            # Update the fields, except 'username' and 'id'
            for key, value in data_listrik.dict().items():
                if key not in ["id", "username"]:
                    existing_data[key] = value

            # Write the updated data to the JSON file
            with open('data/requirement.json', "w") as write_file:
                json.dump(data, write_file, indent=4)

            return DataListrik(**existing_data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data listrik not found")

@administrator_router.put("/edit_cuaca", response_model=DataCuaca)
async def update_data_cuaca(
    data_cuaca: DataCuaca,
    user: UserJSON = Depends(get_current_user)
):
    existing_data_cuaca = data.get("data_cuaca", [])

    for i, existing_data in enumerate(existing_data_cuaca):
        if existing_data.get("username") == data_cuaca.username:
            # Update the fields, except 'username' and 'id'
            for key, value in data_cuaca.dict().items():
                if key not in ["id", "username"]:
                    existing_data[key] = value

            # Write the updated data to the JSON file
            with open('data/requirement.json', "w") as write_file:
                json.dump(data, write_file, indent=4)

            return DataListrik(**existing_data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data cuaca not found")

#----------------------------------------------------------------#

#DELETE
@administrator_router.delete("delete_listrik/{username}")
def delete_data_listrik(username: str, user: UserJSON = Depends(get_current_user)):
    existing_data_listrik = next((req for req in dataListrik if req.get("username") == username), None)

    if  not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this data"
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
            detail="You do not have permission to delete this data"
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
