from pydantic import BaseModel

class DataListrik(BaseModel):
    username: str
    tanggal: str
    jam: int
    jumlahListrik: float

class DataCuaca(BaseModel):
    username: str
    waktu: str
    kelembaban: int

class realEstate(BaseModel):
    id: int
    name: str
    address: str
    location: str
    price: int
    area: int
    bedroom: int
    bathroom: int
    description: str
    image: str
    type: str
    status: str