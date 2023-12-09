#!/usr/bin/python3
"""Base Module that defines all common attributes/methods for other classes"""

import models
from datetime import datetime
import uuid


class BaseModel:
    """The Base class for all other classes."""

    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseModel instance.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            # Store new instances
            models.storage.new(self)

        else:
            # Remove __class__ from kwargs
            kwargs.pop('__class__', None)

            date_fmt = "%Y-%m-%dT%H:%M:%S.%f"

            # Convert created_at and updated_at to datetime objects
            kwargs['created_at'] = datetime.strptime(
                kwargs['created_at'], date_fmt)

            kwargs['updated_at'] = datetime.strptime(
                kwargs['updated_at'], date_fmt)

            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def __repr__(self):
        """Returns string repr"""
        return (self.__str__())

    def save(self):
        """Update the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance."""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__

        if isinstance(obj_dict['created_at'], datetime):
            obj_dict['created_at'] = obj_dict['created_at'].isoformat()

        if isinstance(obj_dict['updated_at'], datetime):
            obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()

        return (obj_dict)
