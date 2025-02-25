from bson import ObjectId

class User:
    def __init__(self, full_name: str, email: str, hashed_password: str):
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password
        self.id = ObjectId()

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "_id": str(self.id)
        }
    
class ArtItem:
    def __init__(self, title: str, artist: str, price: float, description: str, imageUrl: str):
        self.title = title
        self.artist = artist
        self.price = price
        self.description = description
        self.imageUrl = imageUrl
        self.id = ObjectId()

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "price": self.price,
            "description": self.description,
            "imageUrl": self.imageUrl,
            "_id": str(self.id)
        }
