#!/usr/bin/python3
"""Defines Amenities and inherits from the BaseModel class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class - subclass of the BaseModel"""
    name = ""
