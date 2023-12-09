#!/usr/bin/python3
"""Defines unittests for models/state.py.

Classes:
        TestStateInstantiation
        TestStateSave
        TestStateToDict
"""
import unittest
import models
from models.state import State
from datetime import datetime
import os
from time import sleep


class TestStateInstantiation(unittest.TestCase):
    """Unittests to evaluate the State class instantiation."""

    def test_instantiation_with_no_args(self):
        self.assertEqual(State, type(State()))

    def test_instantiates_with_kwargs(self):
        curr_datetime = datetime.today()
        datetime_iso = curr_datetime.isoformat()
        obj_1 = State(id="1-a-2-b", created_at=datetime_iso,
                      updated_at=datetime_iso)
        self.assertEqual(obj_1.updated_at, curr_datetime)
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.id, "1-a-2-b")

    def test_instantiates_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(created_at=None, updated_at=None, id=None)

    def test_new_instances_are_stored(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_str_type(self):
        self.assertEqual(str, type(State().id))

    def test_name_is_string_type_public_class_attribute(self):
        obj_1 = State()
        self.assertIn("name", dir(obj_1))
        self.assertNotIn("name", obj_1.__dict__)
        self.assertEqual(str, type(State.name))

    def test_multiple_states_have_unique_ids(self):
        obj_1 = State()
        obj_2 = State()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_multiple_states_have_different_created_at(self):
        obj_1 = State()
        sleep(0.025)
        obj_2 = State()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_multiple_states_have_different_updated_at(self):
        obj_1 = State()
        sleep(0.025)
        obj_2 = State()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_string_representation(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = State()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("'updated_at': " + datetime_repr, obj_str)
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)
        self.assertIn("[State] (1-a-2-b)", obj_str)


class TestStateSave(unittest.TestCase):
    """Unittests to evaluate the save method of the State class."""

    @classmethod
    def setUp(self):
        """Set up the class."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Tear down after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_with_invalid_arg(self):
        obj_1 = State()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_one_instance(self):
        obj_1 = State()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_updated_at, obj_1.updated_at)

    def test_save_two_instances(self):
        obj_1 = State()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        second_updated_at = obj_1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_updated_at, obj_1.updated_at)

    def test_save_updates_file_content(self):
        obj_1 = State()
        obj_1.save()
        obj_id = "State." + obj_1.id
        with open("file.json") as f:
            self.assertIn(obj_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Unittests to evaluate to_dict method of the State class."""

    def test_to_dict_returns_dict(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_with_invalid_arg(self):
        obj_1 = State()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_contains_default_keys(self):
        obj_1 = State()
        self.assertIn("id", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())
        self.assertIn("__class__", obj_1.to_dict())

    def test_to_dict_includes_added_attributes(self):
        obj_1 = State()
        obj_1.name = "German"
        obj_1.hobby = "Coding"
        obj_1.year = 2023
        self.assertEqual("German", obj_1.name)
        self.assertEqual(2023, obj_1.year)
        self.assertIn("hobby", obj_1.to_dict())

    def test_to_dict_output_matches_expected(self):
        curr_datetime = datetime.today()
        obj_1 = State()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat(),
            'id': '1-a-2-b',
            '__class__': 'State',
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main()
