#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""
import unittest
from models.base_model import BaseModel
import models
from datetime import datetime
import os
from time import sleep


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests to evaluate BaseModel Class Instantiation."""

    def test_new_instances_are_stored(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_with_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_kwargs_instantiation(self):
        curr_datetime = datetime.today()
        datetime_iso = curr_datetime.isoformat()
        obj_1 = BaseModel(id="1234", created_at=datetime_iso,
                          updated_at=datetime_iso)
        self.assertEqual(obj_1.id, "1234")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        curr_datetime = datetime.today()
        datetime_iso = curr_datetime.isoformat()
        obj_1 = BaseModel(
            "5", id="12345", created_at=datetime_iso, updated_at=datetime_iso)
        self.assertEqual(obj_1.id, "12345")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_unique_ids(self):
        obj_1 = BaseModel()
        obj_2 = BaseModel()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_created_at_is_type_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_type_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_created_at(self):
        obj_1 = BaseModel()
        sleep(0.5)
        obj_2 = BaseModel()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_updated_at(self):
        obj_1 = BaseModel()
        sleep(0.5)
        obj_2 = BaseModel()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for evaluating the save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        """Set up the class."""
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Tear down after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass

    def test_save_with_invalid_argument(self):
        obj_1 = BaseModel()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_updates_json_file(self):
        obj_1 = BaseModel()
        obj_1.save()
        obj_id = "BaseModel." + obj_1.id
        with open("file.json", "r") as f:
            self.assertIn(obj_id, f.read())

    def test_save_updates_updated_at(self):
        obj_1 = BaseModel()
        sleep(0.025)
        first_update_time = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_update_time, obj_1.updated_at)

    def test_multiple_saves_update_updated_at(self):
        obj_1 = BaseModel()
        sleep(0.025)
        first_update_time = obj_1.updated_at
        obj_1.save()
        second_update_time = obj_1.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_update_time, obj_1.updated_at)


class TestBaseModelToDict(unittest.TestCase):
    """Unittests to evaluate the to_dict method of the BaseModel class."""

    def test_to_dict_raises_error_with_argument(self):
        obj_1 = BaseModel()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_contains_base_keys(self):
        obj_1 = BaseModel()
        self.assertIn("__class__", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("id", obj_1.to_dict())

    def test_to_dict_includes_custom_attributes(self):
        obj_1 = BaseModel()
        obj_1.name = "Daniel"
        obj_1.hobby = "Coding"
        self.assertIn("name", obj_1.to_dict())
        self.assertIn("hobby", obj_1.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        obj_1 = BaseModel()
        bm_dict = obj_1.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_matches_expected_output(self):
        curr_datetime = datetime.today()
        obj_1 = BaseModel()
        obj_1.id = "12345"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'id': '12345',
            '__class__': 'BaseModel',
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat()
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)

    def test_to_dict_returns_dictionary_type(self):
        obj_1 = BaseModel()
        self.assertTrue(dict, type(obj_1.to_dict()))


if __name__ == "__main__":
    unittest.main()
