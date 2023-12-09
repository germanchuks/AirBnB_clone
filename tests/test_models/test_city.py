#!/usr/bin/python3
"""Defines unittests for models/city.py.

Classes:
        TestCityInstantiation
        TestCitySave
        TestCityToDict
"""
from models.city import City
import unittest
import models
from datetime import datetime
import os
from time import sleep


class TestCityInstantiation(unittest.TestCase):
    """Unittests to evaluate the City class instantiation."""

    def test_instantiation_with_no_args(self):
        self.assertEqual(City, type(City()))

    def test_instantiation_with_kwargs(self):
        curr_datetime = datetime.today()
        dt_iso = curr_datetime.isoformat()
        obj_1 = City(id="1-a-2-b", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(obj_1.id, "1-a-2-b")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_unused_args_do_not_affect_instance(self):
        obj_1 = City(None)
        self.assertNotIn(None, obj_1.__dict__.values())

    def test_instantiation_with_None_kwargs_raises_type_error(self):
        with self.assertRaises(TypeError):
            City(created_at=None, id=None, updated_at=None)

    def test_new_instance_is_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_unique_ids_for_two_cities(self):
        obj_1 = City()
        obj_2 = City()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_different_created_at_for_two_cities(self):
        obj_1 = City()
        sleep(0.025)
        obj_2 = City()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_different_updated_at_for_two_cities(self):
        obj_1 = City()
        sleep(0.025)
        obj_2 = City()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_id_is_str_type(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_datetime_type(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_datetime_type(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_string_type_class_attribute(self):
        obj_1 = City()
        self.assertIn("state_id", dir(obj_1))
        self.assertNotIn("state_id", obj_1.__dict__)
        self.assertEqual(str, type(City.state_id))

    def test_name_is_string_type_class_attribute(self):
        obj_1 = City()
        self.assertIn("name", dir(obj_1))
        self.assertNotIn("name", obj_1.__dict__)
        self.assertEqual(str, type(City.name))

    def test_string_representation(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = City()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'updated_at': " + datetime_repr, obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)
        self.assertIn("[City] (1-a-2-b)", obj_str)


class TestCitySave(unittest.TestCase):
    """Unittests to evaluate the save method of the City class."""

    @classmethod
    def setUp(self):
        """Set up the class."""
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

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

    def test_one_save(self):
        obj_1 = City()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_updated_at, obj_1.updated_at)

    def test_two_saves(self):
        obj_1 = City()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        second_updated_at = obj_1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_updated_at, obj_1.updated_at)

    def test_save_with_arg(self):
        obj_1 = City()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_updates_file(self):
        obj_1 = City()
        obj_1.save()
        cyid = "City." + obj_1.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCityToDict(unittest.TestCase):
    """Unittests to evaluate the to_dict method of the City class."""

    def test_to_dict_with_argument_raises_type_error(self):
        obj_1 = City()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_returns_dictionary(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_default_keys(self):
        obj_1 = City()
        self.assertIn("__class__", obj_1.to_dict())
        self.assertIn("id", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())

    def test_to_dict_includes_added_attributes(self):
        obj_1 = City()
        obj_1.name = "German"
        obj_1.year = 2023
        self.assertEqual("German", obj_1.name)
        self.assertIn("year", obj_1.to_dict())

    def test_to_dict_output_matches_expected_dictionary(self):
        curr_datetime = datetime.today()
        obj_1 = City()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'id': '1-a-2-b',
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat(),
            '__class__': 'City'
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main()
