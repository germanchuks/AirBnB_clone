#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Classes:
    TestFileStorageInstantiation
    TestAmenitySave
    TestAmenityToDict
"""
from models.amenity import Amenity
from datetime import datetime
import unittest
import models
import os
from time import sleep


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests to evaluate Amenity class Instantiation."""

    def test_instantiation_with_no_arg(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_invalid_kwargs_raise_error(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_created_at_is_datetime_type(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_datetime_type(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_attribute_exists(self):
        obj_1 = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", obj_1.__dict__)

    def test_unique_ids_for_two_amenities(self):
        obj_1 = Amenity()
        obj_2 = Amenity()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_different_created_at_for_two_amenities(self):
        obj_1 = Amenity()
        sleep(0.025)
        obj_2 = Amenity()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_different_updated_at_for_two_amenities(self):
        obj_1 = Amenity()
        sleep(0.025)
        obj_2 = Amenity()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_unused_args_are_ignored(self):
        obj_1 = Amenity(None)
        self.assertNotIn(None, obj_1.__dict__.values())

    def test_instantiation_with_valid_kwargs(self):
        curr_datetime = datetime.today()
        dt_iso = curr_datetime.isoformat()
        obj_1 = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(obj_1.id, "345")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_str_representation_contains_expected_info(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = Amenity()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("[Amenity] (1-a-2-b)", obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'updated_at': " + datetime_repr, obj_str)


class TestAmenitySave(unittest.TestCase):
    """Unittests to evaluate the save method of the Amenity class."""

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

    def test_save_with_invalid_arg_raises_error(self):
        obj_1 = Amenity()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_updates_json_file(self):
        obj_1 = Amenity()
        obj_1.save()
        obj_id = "Amenity." + obj_1.id
        with open("file.json") as f:
            self.assertIn(obj_id, f.read())

    def test_single_save_updates_updated_at(self):
        obj_1 = Amenity()
        sleep(0.05)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_updated_at, obj_1.updated_at)

    def test_multiple_saves_updates_updated_at(self):
        obj_1 = Amenity()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        second_updated_at = obj_1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_updated_at, obj_1.updated_at)


class TestAmenityToDict(unittest.TestCase):
    """Unittests to evaluate the to_dict method of the Amenity class."""

    def test_to_dict_with_argument_raises_type_error(self):
        obj_1 = Amenity()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_contains_expected_keys(self):
        obj_1 = Amenity()
        self.assertIn("id", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())
        self.assertIn("__class__", obj_1.to_dict())

    def test_to_dict_includes_added_attributes(self):
        obj_1 = Amenity()
        obj_1.name = "Michael"
        obj_1.hobby = "Blogging"
        self.assertEqual("Michael", obj_1.name)
        self.assertIn("hobby", obj_1.to_dict())

    def test_return_type_is_dict(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_datetime_attributes_as_strings(self):
        obj_1 = Amenity()
        am_dict = obj_1.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_output_format(self):
        curr_datetime = datetime.today()
        obj_1 = Amenity()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'id': '1-a-2-b',
            '__class__': 'Amenity',
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat(),
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main()
