#!/usr/bin/python3
"""Defines Reviews and inherits from the BaseModel class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class - subclass of the BaseModel"""
    place_id = ""
    user_id = ""
    text = ""
