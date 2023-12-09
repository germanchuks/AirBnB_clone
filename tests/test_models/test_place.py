#!/usr/bin/python3
"""Defines unittests for models/place.py.

Classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
from models.place import Place
import unittest
import models
from datetime import datetime
import os
from time import sleep


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests to evaluate Place class instantiation."""

    def test_instantiation_with_no_args(self):
        self.assertEqual(Place, type(Place()))

    def test_instantiation_with_kwargs_sets_attributes_correctly(self):
        curr_datetime = datetime.today()
        datetime_iso = curr_datetime.isoformat()
        obj_1 = Place(id="1-a-2-b", created_at=datetime_iso,
                      updated_at=datetime_iso)
        self.assertEqual(obj_1.id, "1-a-2-b")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_instantiation_with_None_kwargs_raises_type_error(self):
        with self.assertRaises(TypeError):
            Place(updated_at=None, created_at=None, id=None)

    def test_city_id_is_public_class_attribute_string_type(self):
        obj_1 = Place()
        self.assertIn("city_id", dir(obj_1))
        self.assertNotIn("city_id", obj_1.__dict__)
        self.assertEqual(str, type(Place.city_id))

    def test_user_id_is_public_class_attribute_string_type(self):
        obj_1 = Place()
        self.assertIn("user_id", dir(obj_1))
        self.assertNotIn("user_id", obj_1.__dict__)
        self.assertEqual(str, type(Place.user_id))

    def test_name_is_public_class_attribute_string_type(self):
        obj_1 = Place()
        self.assertIn("name", dir(obj_1))
        self.assertNotIn("name", obj_1.__dict__)
        self.assertEqual(str, type(Place.name))

    def test_description_is_public_class_attribute_string_type(self):
        obj_1 = Place()
        self.assertIn("description", dir(obj_1))
        self.assertNotIn("desctiption", obj_1.__dict__)
        self.assertEqual(str, type(Place.description))

    def test_number_rooms_is_public_class_attribute_int_type(self):
        obj_1 = Place()
        self.assertIn("number_rooms", dir(obj_1))
        self.assertNotIn("number_rooms", obj_1.__dict__)
        self.assertEqual(int, type(Place.number_rooms))

    def test_number_bathrooms_is_public_class_attribute_int_type(self):
        obj_1 = Place()
        self.assertIn("number_bathrooms", dir(obj_1))
        self.assertNotIn("number_bathrooms", obj_1.__dict__)
        self.assertEqual(int, type(Place.number_bathrooms))

    def test_max_guest_is_public_class_attribute_int_type(self):
        obj_1 = Place()
        self.assertIn("max_guest", dir(obj_1))
        self.assertNotIn("max_guest", obj_1.__dict__)
        self.assertEqual(int, type(Place.max_guest))

    def test_price_by_night_is_public_class_attribute_int_type(self):
        obj_1 = Place()
        self.assertIn("price_by_night", dir(obj_1))
        self.assertNotIn("price_by_night", obj_1.__dict__)
        self.assertEqual(int, type(Place.price_by_night))

    def test_latitude_is_public_class_attribute_float_type(self):
        obj_1 = Place()
        self.assertIn("latitude", dir(obj_1))
        self.assertNotIn("latitude", obj_1.__dict__)
        self.assertEqual(float, type(Place.latitude))

    def test_longitude_is_public_class_attribute_float_type(self):
        obj_1 = Place()
        self.assertIn("longitude", dir(obj_1))
        self.assertNotIn("longitude", obj_1.__dict__)
        self.assertEqual(float, type(Place.longitude))

    def test_amenity_ids_is_public_class_attribute_list_type(self):
        obj_1 = Place()
        self.assertIn("amenity_ids", dir(obj_1))
        self.assertNotIn("amenity_ids", obj_1.__dict__)
        self.assertEqual(list, type(Place.amenity_ids))

    def test_new_instance_is_stored_in_objects_dict(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str_type(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime_type(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime_type(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_multiple_place_have_unique_ids(self):
        obj_1 = Place()
        obj_2 = Place()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_multiple_place_have_different_created_at(self):
        obj_1 = Place()
        sleep(0.025)
        obj_2 = Place()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_multiple_place_have_different_updated_at(self):
        obj_1 = Place()
        sleep(0.025)
        obj_2 = Place()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_str_representation_includes_instance_id_and_timestamps(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = Place()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("[Place] (1-a-2-b)", obj_str)
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'updated_at': " + datetime_repr, obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)


class TestPlaceSave(unittest.TestCase):
    """Unittests to evaluate save method of the Place class."""

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

    def test_save_with_argument_raises_type_error(self):
        obj_1 = Place()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_updates_file_with_instance_id(self):
        obj_1 = Place()
        obj_1.save()
        obj_id = "Place." + obj_1.id
        with open("file.json") as f:
            self.assertIn(obj_id, f.read())

    def test_save_increases_updated_at(self):
        obj_1 = Place()
        sleep(0.025)
        updated_time_old = obj_1.updated_at
        obj_1.save()
        self.assertLess(updated_time_old, obj_1.updated_at)

    def test_multiple_saves_increase_updated_at(self):
        obj_1 = Place()
        sleep(0.025)
        updated_time_old = obj_1.updated_at
        obj_1.save()
        updated_time_new = obj_1.updated_at
        self.assertLess(updated_time_old, updated_time_new)
        sleep(0.025)
        obj_1.save()
        self.assertLess(updated_time_new, obj_1.updated_at)


class TestPlaceToDict(unittest.TestCase):
    """Unittests to evaluate to_dict method of the Place class."""

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_with_argument_raises_type_error(self):
        obj_1 = Place()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_contains_default_keys(self):
        obj_1 = Place()
        self.assertIn("id", obj_1.to_dict())
        self.assertIn("__class__", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())

    def test_to_dict_contains_custom_attributes(self):
        obj_1 = Place()
        obj_1.name = "Michael"
        obj_1.hobby = "Blogging"
        obj_1.year = 2023
        self.assertEqual("Michael", obj_1.name)
        self.assertEqual(2023, obj_1.year)
        self.assertIn("hobby", obj_1.to_dict())

    def test_to_dict_datetime_are_string_type(self):
        obj_1 = Place()
        pl_dict = obj_1.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output_matches_expected_dictionary(self):
        curr_datetime = datetime.today()
        obj_1 = Place()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'id': '1-a-2-b',
            '__class__': 'Place',
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat(),
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)

    def test_to_dict_differs_from_instance_dictionary(self):
        obj_1 = Place()
        self.assertNotEqual(obj_1.to_dict(), obj_1.__dict__)


if __name__ == "__main__":
    unittest.main()
