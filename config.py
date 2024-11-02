import os
import psycopg2

class Config:
    SECRET_KEY = 'HondVanKat'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/ComradHub'
    SQLALCHEMY_TRACK_MODIFICATIONS = False