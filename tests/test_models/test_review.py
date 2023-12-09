#!/usr/bin/python3
"""Defines unittests for models/review.py.

Classes:
        TestReviewInstantiation
        TestReviewSave
        TestReviewToDict
"""
import unittest
import models
from models.review import Review
from datetime import datetime
import os
from time import sleep


class TestReviewInstantiation(unittest.TestCase):
    """Unittests to evaluate the Review class instantiation."""

    def test_instantiation_with_no_args(self):
        self.assertEqual(Review, type(Review()))

    def test_instantiation_with_kwargs(self):
        curr_datetime = datetime.today()
        dt_iso = curr_datetime.isoformat()
        obj_1 = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(obj_1.id, "345")
        self.assertEqual(obj_1.created_at, curr_datetime)
        self.assertEqual(obj_1.updated_at, curr_datetime)

    def test_instantiation_with_None_kwargs_raises_TypeError(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_new_instances_are_stored(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_str_type(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_datetime_type(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_datetime_type(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_string_type_public_class_attribute(self):
        obj_1 = Review()
        self.assertIn("place_id", dir(obj_1))
        self.assertNotIn("place_id", obj_1.__dict__)
        self.assertEqual(str, type(Review.place_id))

    def test_user_id_is_string_type_public_class_attribute(self):
        obj_1 = Review()
        self.assertIn("user_id", dir(obj_1))
        self.assertNotIn("user_id", obj_1.__dict__)
        self.assertEqual(str, type(Review.user_id))

    def test_text_is_string_type_public_class_attribute(self):
        obj_1 = Review()
        self.assertIn("text", dir(obj_1))
        self.assertNotIn("text", obj_1.__dict__)
        self.assertEqual(str, type(Review.text))

    def test_unique_ids_for_multiple_reviews(self):
        obj_1 = Review()
        obj_2 = Review()
        self.assertNotEqual(obj_1.id, obj_2.id)

    def test_different_created_at_for_multiple_reviews(self):
        obj_1 = Review()
        sleep(0.025)
        obj_2 = Review()
        self.assertLess(obj_1.created_at, obj_2.created_at)

    def test_different_updated_at_for_two_reviews(self):
        obj_1 = Review()
        sleep(0.025)
        obj_2 = Review()
        self.assertLess(obj_1.updated_at, obj_2.updated_at)

    def test_string_representation(self):
        curr_datetime = datetime.today()
        datetime_repr = repr(curr_datetime)
        obj_1 = Review()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_str = obj_1.__str__()
        self.assertIn("'updated_at': " + datetime_repr, obj_str)
        self.assertIn("'created_at': " + datetime_repr, obj_str)
        self.assertIn("'id': '1-a-2-b'", obj_str)
        self.assertIn("[Review] (1-a-2-b)", obj_str)


class TestReviewSave(unittest.TestCase):
    """Unittests to evaluate the Save method of the Review class."""

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

    def test_save_updates_file(self):
        obj_1 = Review()
        obj_1.save()
        obj_id = "Review." + obj_1.id
        with open("file.json") as f:
            self.assertIn(obj_id, f.read())

    def test_save_with_argument_raises_type_error(self):
        obj_1 = Review()
        with self.assertRaises(TypeError):
            obj_1.save(None)

    def test_save_changes_updated_at_for_one_instance(self):
        obj_1 = Review()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        self.assertLess(first_updated_at, obj_1.updated_at)

    def test_save_changes_updated_at_for_multiple_instances(self):
        obj_1 = Review()
        sleep(0.025)
        first_updated_at = obj_1.updated_at
        obj_1.save()
        second_updated_at = obj_1.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.025)
        obj_1.save()
        self.assertLess(second_updated_at, obj_1.updated_at)


class TestReviewToDict(unittest.TestCase):
    """Unittests to evaluate the to_dict method of the Review class."""

    def test_to_dict_with_argument_raises_type_error(self):
        obj_1 = Review()
        with self.assertRaises(TypeError):
            obj_1.to_dict(None)

    def test_to_dict_returns_dictionary(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_default_keys(self):
        obj_1 = Review()
        self.assertIn("__class__", obj_1.to_dict())
        self.assertIn("created_at", obj_1.to_dict())
        self.assertIn("updated_at", obj_1.to_dict())
        self.assertIn("id", obj_1.to_dict())

    def test_to_dict_includes_added_attributes(self):
        obj_1 = Review()
        obj_1.name = "Michael"
        obj_1.year = 2023
        self.assertEqual("Michael", obj_1.name)
        self.assertIn("year", obj_1.to_dict())

    def test_to_dict_output_matches_expected(self):
        curr_datetime = datetime.today()
        obj_1 = Review()
        obj_1.id = "1-a-2-b"
        obj_1.created_at = obj_1.updated_at = curr_datetime
        obj_dict = {
            'id': '1-a-2-b',
            'created_at': curr_datetime.isoformat(),
            'updated_at': curr_datetime.isoformat(),
            '__class__': 'Review',
        }
        self.assertDictEqual(obj_1.to_dict(), obj_dict)


if __name__ == "__main__":
    unittest.main()
