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