SECRET_KEY = "super_secret_key"

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:0000@localhost:5432/microservices_hospital_san_rafael2_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False