from fastapi import FastAPI
from routes.requirements import umum_router, administrator_router, raka_router
from routes.auth import auth_router

app = FastAPI()

app.include_router(auth_router)  # Include the authentication router
app.include_router(umum_router, prefix="/umum")
app.include_router(administrator_router, prefix="/administrator")
app.include_router(raka_router, prefix="/raka")