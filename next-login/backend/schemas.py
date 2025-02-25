from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    email: str

class ArtItemResponse(BaseModel):
    id: str
    title: str
    artist: str
    price: float
    description: str
    imageUrl: str