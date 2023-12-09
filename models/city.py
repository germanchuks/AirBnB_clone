#!/usr/bin/python3
"""Defines Cities and inherits from the BaseModel class"""

from models.base_model import BaseModel


class City(BaseModel):
    """City class  - subclass of the BaseModel"""
    state_id = ""
    name = ""
