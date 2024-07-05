"""
Configuration settings for the application.
"""

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'XsdcMOlGTo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_DATABASE = False  # Default value

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True
    USE_DATABASE = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    DEBUG = True
    TESTING = True
    USE_DATABASE = True  # Enable database in testing

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    DEBUG = False
    USE_DATABASE = True  # Enable database in production

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
