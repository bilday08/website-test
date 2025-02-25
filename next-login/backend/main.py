from fastapi import FastAPI, HTTPException, Depends
# Here is the hotfix I applied for the import error. Please adjust it to match the path on your machine.
import sys
sys.path.append('/Users/hanhphan/Documents/website-test/next-login/backend')
import schemas
import security
import database
import models
from pymongo.errors import DuplicateKeyError
from fastapi.middleware.cors import CORSMiddleware
from schemas import UserLogin
from bson import ObjectId
import stripe
from datetime import datetime

app = FastAPI()

stripe.api_key = "sk_test_51QwM41QRi83qAOuAOKtaFX8dTyjN74nrz8EkVkFGWo5Ts5UpvSBIiHroBHwpBC7LdaxKJMmo6dvWjIC8lzxS2qIi003cf5mQvr"

def get_db():
    return database.db
    
def create_payment_intent(amount: int, currency: str = "usd"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return intent.client_secret
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")

# Endpoint registration
@app.post("/register")
def register(user: schemas.UserCreate, db = Depends(get_db)):
    """
    API handles the user registration process.

    Args:
        user (schemas.UserCreate): The user data to be used for creating a new user. 
                                   This includes the user's email, full name, and password.
        db (type, optional): The database connection to be used for inserting the new user. 

    Returns:
        - On success: A JSON object with the message "User registered successfully".
        - On failure (email already exists): An HTTPException with a 400 status code and an appropriate error message.
    """
    db_user = db.users.find_one({"email": user.email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.hash_password(user.password)
    
    new_user = models.User(
        email=user.email,
        full_name=user.full_name, 
        hashed_password=hashed_password
    )
    try:
        db.users.insert_one(new_user.to_dict())
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return {"message": "User registered successfully"}

# Endpoint Login
@app.post("/login")
def login(user: UserLogin, db = Depends(get_db)):
    """
    API endpoint for user login.

    This endpoint validates the user's email and password, and if successful, generates a JWT token for authentication.

    Args:
        user (UserLogin): The user's login credentials, including email and password
        db (_type_, optional): The database connection, injected by FastAPI's dependency system. 
                               Defaults to Depends(get_db), which fetches the database connection.

    Returns:
        dict: A dictionary containing the generated JWT token if the login is successful.
    """
    db_user = db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not security.verify_password(user.password, db_user['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = security.create_jwt(user.email)
    return {"token": token}

# Endpoint requires JWT
@app.get("/profile")
def profile(token: str, db = Depends(get_db)):
    """
    API endpoint to retrieve the user's profile information.

    This endpoint verifies the provided JWT token, retrieves the user's email from the token, and returns the user's profile information (email).

    Args:
        token (str): The JWT token used for authentication. It is expected to be provided in the request.
        db (Depends): The database connection, injected by FastAPI's dependency system.

    Returns:
        dict: A dictionary containing the user's email if the token is valid and the user exists.
    """
    email = security.verify_jwt(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_user = db.users.find_one({"email": email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"email": db_user['email']}

# Endpoint purchase
@app.post("/purchase")
def purchase_art_item(art_id: str, token: str, db = Depends(get_db)):
    """
    API to handle the purchase of an art item.
    
    Args:
        art_id (str): The ID of the art item to purchase.
        token (str): The JWT token used for authentication.
        db (Depends): The database connection, injected by FastAPI's dependency system.
    
    Returns:
        Success message if the purchase is successful.
    """
    email = security.verify_jwt(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    art_item = db.art_items.find_one({"_id": ObjectId(art_id)})
    if not art_item:
        raise HTTPException(status_code=404, detail="Art item not found")
    
    try:
        payment_intent = create_payment_intent(amount=int(art_item['price'] * 100))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment failed: {str(e)}")

    order = {
        "art_item_id": art_item["_id"],
        "user_email": email,
        "status": "Completed",
        "payment_status": "Paid",
        "purchase_date": datetime.utcnow()
    }
    
    db.orders.insert_one(order)
    
    return {
        "message": f"The purchase of '{art_item['title']}' by {art_item['artist']} has been successfully completed!",
        "client_secret": payment_intent 
    }


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)