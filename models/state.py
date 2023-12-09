#!/usr/bin/python3
"""Defines States and inherits from the BaseModel class"""

from models.base_model import BaseModel


class State(BaseModel):
    """State class - subclass of the BaseModel"""
    name = ""
