#!/usr/bin/python3
"""Defines unittests for models/user.py.

Classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
from models.user import User
from datetime import datetime
from time import sleep
import unittest
import models
import os


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_instantiation_without_args(self):
        self.assertEqual(User, type(User()))

    def test_user_instantiation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            User(created_at=None, updated_at=None, id=None)

    def test_user_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_unused_args_do_not_affect_user_instance(self):
        obj_1 = User(None)
        self.assertNotIn(None, obj_1.__dict__.values())

    def test_user_instantiation_with_kwargs(self):
        curr_datetime = datetime.today()
        datetime_iso = curr_datetime.isoformat()
        obj_1 = User(created_at=datetime_iso,
                     updated_at=datetime_iso, id="1-a-2-b")
        self.assertEqual(obj_1.id, "1-a-2-b")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_user_id_is_str_type(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_datetime_type(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_datetime_type(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_str_type(self):
        self.assertEqual(str, type(User.email))

    def test_first_name_is_str_type(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_str_type(self):
        self.assertEqual(str, type(User.last_name))

    def test_password_is_str_type(self):
        self.assertEqual(str, type(User.password))

    def test_two_users_unique_ids(self):
        obj_1 = User()
        obj_2 = User()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_two_users_have_different_created_at(self):
        obj_1 = User()
        sleep(0.025)
        obj_2 = User()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_two_users_have_different_updated_at(self):
        obj_1 = User()
        sleep(0.025)
        obj_2 = User()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_user_string_representation(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = User()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("[User] (1-a-2-b)", obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'updated_at': " + datetime_repr, obj_str)


class TestUserSave(unittest.TestCase):
    """Unittests to evaluate save method of the class."""

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

    def test_save_with_non_dict_argument_raises_type_error(self):
        obj_1 = User()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_updates_file_contents(self):
        obj_1 = User()
        obj_1.save()
        obj_1 = "User." + obj_1.id
        with open("file.json") as f:
            self.assertIn(obj_1, f.read())

    def test_save_once_updates_updated_at(self):
        obj_1 = User()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_updated_at, obj_1.updated_at)

    def test_save_twice_updates_updated_at(self):
        obj_1 = User()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        second_updated_at = obj_1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_updated_at, obj_1.updated_at)


class TestUserToDict(unittest.TestCase):
    """Unittests to evaluate to_dict method of the User class."""

    def test_to_dict_returns_dictionary(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_with_non_dict_argument_raises_type_error(self):
        obj_1 = User()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_contains_expected_keys(self):
        obj_1 = User()
        self.assertIn("id", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())
        self.assertIn("__class__", obj_1.to_dict())

    def test_added_attributes_are_included(self):
        obj_1 = User()
        obj_1.name = "German"
        obj_1.hobby = "Coding"
        obj_1.year = 2023
        self.assertEqual("German", obj_1.name)
        self.assertIn("hobby", obj_1.to_dict())
        self.assertEqual(2023, obj_1.year)

    def test_datetime_attributes_are_strings(self):
        obj_1 = User()
        obj_dict = obj_1.to_dict()
        self.assertEqual(str, type(obj_dict["id"]))
        self.assertEqual(str, type(obj_dict["updated_at"]))
        self.assertEqual(str, type(obj_dict["created_at"]))

    def test_output_matches_expected(self):
        curr_datetime = datetime.today()
        obj_1 = User()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            '__class__': 'User',
            'id': '1-a-2-b',
            'updated_at': curr_datetime.isoformat(),
            'created_at': curr_datetime.isoformat(),
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main()
