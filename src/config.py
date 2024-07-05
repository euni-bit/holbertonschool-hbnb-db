"""
Configuration settings for the application.
"""

import os


class Config:
    """
    Base configuration class.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'XsdcMOlGTo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_DATABASE = False  # Default value


class DevelopmentConfig(Config):
    """
    Development configuration class.
    Sets SQLALCHEMY_DATABASE_URI from environment variable or default to sqlite.
    Enables DEBUG and USE_DATABASE.
    """  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True
    USE_DATABASE = True


class TestingConfig(Config):
    """
    Testing configuration class.
    Sets SQLALCHEMY_DATABASE_URI from environment variable or defaults to SQLite.
    Enables DEBUG, TESTING, and USE_DATABASE for testing environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    DEBUG = True
    TESTING = True
    USE_DATABASE = True  # Enable database in testing


class ProductionConfig(Config):
    """
    Production configuration class.
    Sets SQLALCHEMY_DATABASE_URI from environment variable or defaults to SQLite.
    Disables DEBUG and enables USE_DATABASE for production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    DEBUG = False
    USE_DATABASE = True  # Enable database in production


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
