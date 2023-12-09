#!/usr/bin/python3
"""Module to serialize instances to a JSON file
and deserialize JSON file to instances"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to
    instances."""
    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel,
                  "User": User,
                  "Place": Place,
                  "City": City,
                  "State": State,
                  "Amenity": Amenity,
                  "Review": Review}

    def all(self):
        """Returns the dictionary __objects."""
        return (FileStorage.__objects)

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file `__file_path`."""
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(FileStorage.__objects, file,
                      default=lambda o: o.to_dict())

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path) as file:
                FileStorage.__objects = json.load(file)
        except Exception:
            pass
