#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Classes:
    TestFileStorageInstantiation
    TestFileStorageMethods
"""
import os
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.user import User


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests to evaluate instantiation of the FileStorage class."""

    def test_storage_initialization(self):
        self.assertEqual(type(models.storage), FileStorage)

    def test_instantiation_with_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_instantiation_with_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_file_path_is_private_string(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dictionary(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_default_file_path(self):
        file_st = FileStorage()
        self.assertEqual(file_st._FileStorage__file_path, 'file.json')


class TestFileStorageMethods(unittest.TestCase):
    """Unittests to evaluate methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dictionary(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_invalid_argument(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_adds_instances_to_storage(self):
        user = User()
        base_model = BaseModel()
        state = State()
        review = Review()
        amenity = Amenity()
        place = Place()
        city = City()

        models.storage.new(user)
        models.storage.new(base_model)
        models.storage.new(state)
        models.storage.new(review)
        models.storage.new(amenity)
        models.storage.new(place)
        models.storage.new(city)

        self.assertIn("User." + user.id, models.storage.all().keys())
        self.assertIn(user, models.storage.all().values())
        self.assertIn("BaseModel." + base_model.id,
                      models.storage.all().keys())
        self.assertIn(base_model, models.storage.all().values())
        self.assertIn("State." + state.id, models.storage.all().keys())
        self.assertIn(state, models.storage.all().values())
        self.assertIn("Review." + review.id, models.storage.all().keys())
        self.assertIn(review, models.storage.all().values())
        self.assertIn("Amenity." + amenity.id, models.storage.all().keys())
        self.assertIn(amenity, models.storage.all().values())
        self.assertIn("Place." + place.id, models.storage.all().keys())
        self.assertIn(place, models.storage.all().values())
        self.assertIn("City." + city.id, models.storage.all().keys())
        self.assertIn(city, models.storage.all().values())

    def test_save_method_saves_instances_to_file(self):
        user = User()
        base_model = BaseModel()
        state = State()
        review = Review()
        amenity = Amenity()
        place = Place()
        city = City()

        models.storage.new(user)
        models.storage.new(base_model)
        models.storage.new(state)
        models.storage.new(review)
        models.storage.new(amenity)
        models.storage.new(place)
        models.storage.new(city)

        models.storage.save()

        with open("file.json") as f:
            obj_stored = f.read()
            self.assertIn("User." + user.id, obj_stored)
            self.assertIn("BaseModel." + base_model.id, obj_stored)
            self.assertIn("State." + state.id, obj_stored)
            self.assertIn("Review." + review.id, obj_stored)
            self.assertIn("Amenity." + amenity.id, obj_stored)
            self.assertIn("Place." + place.id, obj_stored)
            self.assertIn("City." + city.id, obj_stored)

    def test_new_with_invalid_argument(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_with_invalid_argument(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_with_invalid_argument(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
