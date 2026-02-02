import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY=os.getenv('SECRET_KEY')
    UPLOAD_PATH=os.path.dirname(os.path.abspath(__file__)) + '/uploads'
    