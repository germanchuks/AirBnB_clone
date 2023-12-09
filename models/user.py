#!/usr/bin/python3
"""Defines Users and inherits from the BaseModel class"""

from models.base_model import BaseModel


class User(BaseModel):
    """User class - subclass of the BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
