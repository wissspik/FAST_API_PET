from fastapi import APIRouter

app = APIRouter()

@app.put("/change_password")
async def change_password(password: str) -> None:
    return {'message': 'Password changed.'}