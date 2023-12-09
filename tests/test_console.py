#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompt
    TestHBNBCommand_help_cmd
    TestHBNBCommand_exit_cmd
    TestHBNBCommand_create_cmd
    TestHBNBCommand_show_cmd
    TestHBNBCommand_all_cmd
    TestHBNBCommand_destroy_cmd
    TestHBNBCommand_update_cmd
    TestHBNBCommand_count_cmd
"""
import unittest
from models.engine.file_storage import FileStorage
from unittest.mock import patch
from models import storage
from console import HBNBCommand
from io import StringIO
import os
import console


class TestHBNBCommand_prompt(unittest.TestCase):
    """Unittests to evaluate HBNB command interpreter prompt."""

    @classmethod
    def setUpClass(self):
        """Set up test"""
        self.typing = console.HBNBCommand()

    @classmethod
    def tearDownClass(self):
        """Remove temporary file.json."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_console_docstrings(self):
        """Test docstrings exist in console.py"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)


class TestHBNBCommand_help_messages(unittest.TestCase):
    """Unittests for HBNB command interpreter help messages."""

    def test_help(self):
        expected_output = ("Documented commands (type help <topic>):\n"
                           "========================================\n"
                           "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_quit(self):
        expected_output = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_EOF(self):
        expected_output = """EOF command to exit the program"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_create(self):
        expected_output = ("""Creates a new instance of BaseModel, saves it and prints the ID.
        Usage: create <class name>""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_show(self):
        expected_output = ("""Prints string representation of an instance based on class name
        and ID. Usage: show <class name> <id> or <class name>.show(<id>)""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_all(self):
        expected_output = ("""Retrieves all instances of a class. Usage: all or all <class name>
        or <class name>.all().""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            actual_output = f.getvalue().strip()
            self.assertIn(expected_output, actual_output)

    def test_help_destroy(self):
        expected_output = ("""Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id> or <class name>.destroy(<id>)""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_update(self):
        expected_output = ("""Updates an instance based on the class name and ID by adding or
        updating attributes. Usage: update <class> <id> <attribute_name>
        <attribute_value> or <class>.update(<id>, <attribute_name>,
        <attribute_value>) or <class>.update(<id>, <dictionary>)""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_help_count(self):
        expected_output = ("""Retrieves the number of instances of a class.
        Usage: count <class name> or <class name>.count()""")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(expected_output, f.getvalue().strip())


class TestHBNBCommand_exit_cmd(unittest.TestCase):
    """Unittests to evaluate HBNB command interpreter exit command."""

    def test_quit(self):
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create_cmd(unittest.TestCase):
    """Unittests to evaluate create command from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_with_missing_class(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_create_with_unknown_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create UnknownClass"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_create_with_invalid_syntax(self):
        expected_output = "*** Unknown syntax: Amenity.create()"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.create()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_create_with_valid_classes(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"BaseModel.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"User.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"State.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"Amenity.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"Place.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"Review.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(f.getvalue().strip()))
            expected_key = f"City.{f.getvalue().strip()}"
            self.assertIn(expected_key, storage.all().keys())


class TestHBNBCommand_show_cmd(unittest.TestCase):
    """Unittests to evaluate show command of the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_with_unknown_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show UnknownClass"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("UnknownClass.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_show_with_no_id(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_show_with_no_id_parenthesis_fmt(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_show_with_unknown_id(self):
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show User 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show State 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Review 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show City 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show Place 1-a-2-b"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_show_with_unknown_id_parenthesis_fmt(self):
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1-a-2-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_show_with_valid_id(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"User.{valid_id}"]
            cmd_str = f"show User {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"BaseModel.{valid_id}"]
            cmd_str = f"show BaseModel {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"State.{valid_id}"]
            cmd_str = f"show State {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Review.{valid_id}"]
            cmd_str = f"show Review {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Place.{valid_id}"]
            cmd_str = f"show Place {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"City.{valid_id}"]
            cmd_str = f"show City {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Amenity.{valid_id}"]
            cmd_str = f"show Amenity {valid_id}"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

    def test_show_with_valid_id_parenthesis_fmt(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"User.{valid_id}"]
            cmd_str = f"User.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"BaseModel.{valid_id}"]
            cmd_str = f"BaseModel.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"State.{valid_id}"]
            cmd_str = f"State.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Review.{valid_id}"]
            cmd_str = f"Review.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Place.{valid_id}"]
            cmd_str = f"Place.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"City.{valid_id}"]
            cmd_str = f"City.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()[f"Amenity.{valid_id}"]
            cmd_str = f"Amenity.show({valid_id})"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(new_obj.__str__(), f.getvalue().strip())


class TestHBNBCommand_destroy_cmd(unittest.TestCase):
    """Unittests to evaluate destroy command of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def test_destroy_with_no_class(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_unknown_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy UnknownClass"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("UnknownClass.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_no_id(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_no_id_parenthesis_fmt(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_unknown_id(self):
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy User 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy State 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy City 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 2-a-b"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_unknown_id_parenthesis_fmt(self):
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(2-a-b)"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_destroy_with_existing_instance(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["User.{}".format(valid_id)]
            cmd_str = "show User {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["BaseModel.{}".format(valid_id)]
            cmd_str = "destroy BaseModel {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["State.{}".format(valid_id)]
            cmd_str = "show State {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Review.{}".format(valid_id)]
            cmd_str = "show Review {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Amenity.{}".format(valid_id)]
            cmd_str = "show Amenity {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Place.{}".format(valid_id)]
            cmd_str = "show Place {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["City.{}".format(valid_id)]
            cmd_str = "show City {}".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

    def test_destroy_with_existing_instance_parenthesis_fmt(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["User.{}".format(valid_id)]
            cmd_str = "User.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["BaseModel.{}".format(valid_id)]
            cmd_str = "BaseModel.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["State.{}".format(valid_id)]
            cmd_str = "State.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Review.{}".format(valid_id)]
            cmd_str = "Review.destory({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Amenity.{}".format(valid_id)]
            cmd_str = "Amenity.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["Place.{}".format(valid_id)]
            cmd_str = "Place.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            new_obj = storage.all()["City.{}".format(valid_id)]
            cmd_str = "City.destroy({})".format(valid_id)
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertNotIn(new_obj, storage.all())


class TestHBNBCommand_all_cmd(unittest.TestCase):
    """Unittests to evaluate all command of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_all_with_unknown_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all UnknownClass"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("UnknownClass.all()"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_all_with_valid_and_existing_class(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", f.getvalue().strip())
            self.assertNotIn("BaseModel", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertNotIn("User", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", f.getvalue().strip())
            self.assertNotIn("State", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", f.getvalue().strip())
            self.assertNotIn("City", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", f.getvalue().strip())
            self.assertNotIn("Amenity", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", f.getvalue().strip())
            self.assertNotIn("City", f.getvalue().strip())

    def test_all_with_valid_and_existing_class_parenthesis_fmt(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", f.getvalue().strip())
            self.assertNotIn("BaseModel", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertNotIn("User", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", f.getvalue().strip())
            self.assertNotIn("State", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", f.getvalue().strip())
            self.assertNotIn("City", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", f.getvalue().strip())
            self.assertNotIn("Amenity", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", f.getvalue().strip())
            self.assertNotIn("City", f.getvalue().strip())


class TestHBNBCommand_update_cmd(unittest.TestCase):
    """Unittests to evaluate update command of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_with_no_class(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(".update()"))

    def test_update_with_unknown_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update UnknownClass"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("UnknownClass.update()"))

    def test_update_with_no_id(self):
        expected_output = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_update_with_unknown_id(self):
        expected_output = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update State 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Review 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update City 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update Place 1-2-3"))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_update_with_no_attribute(self):
        expected_output = "** attribute name missing **"

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update User {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update BaseModel {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update State {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update Review {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update Amenity {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update City {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            valid_id = f.getvalue().strip()
            cmd_str = f"update Place {valid_id}"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_update_with_no_attribute_value(self):
        expected_output = "** value missing **"

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update User {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update BaseModel {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update State {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update Review {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update Amenity {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update City {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            valid_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            cmd_str = f"update Place {valid_id} attr_name"
            self.assertFalse(HBNBCommand().onecmd(cmd_str))
            self.assertEqual(expected_output, f.getvalue().strip())

    def test_update_with_valid_class_id_attribute_name_and_value(self):
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            valid_id = f.getvalue().strip()
        cmd_str = f"update User {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"User.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            valid_id = f.getvalue().strip()
        cmd_str = f"update BaseModel {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"BaseModel.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            valid_id = f.getvalue().strip()
        cmd_str = f"update State {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"State.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            valid_id = f.getvalue().strip()
        cmd_str = f"update Review {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"Review.{valid_id}"].__dict__
        self.assertTrue("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            valid_id = f.getvalue().strip()
        cmd_str = f"update Amenity {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"Amenity.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            valid_id = f.getvalue().strip()
        cmd_str = f"update City {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"City.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            valid_id = f.getvalue().strip()
        cmd_str = f"update Place {valid_id} attr_name 'attr_value'"
        self.assertFalse(HBNBCommand().onecmd(cmd_str))
        obj_dict = storage.all()[f"Place.{valid_id}"].__dict__
        self.assertEqual("attr_value", obj_dict["attr_name"])


class TestHBNBCommand_count_cmd(unittest.TestCase):
    """Unittests to evaluate count command of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_with_no_class(self):
        expected_value = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(".count()"))
            self.assertEqual(expected_value, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count"))
            self.assertEqual(expected_value, f.getvalue().strip())

    def test_count_with_unknown_class(self):
        expected_value = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("UnknownClass.count()"))
            self.assertEqual(expected_value, f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count UnknownClass"))
            self.assertEqual(expected_value, f.getvalue().strip())

    def test_count_with_valid_and_existing_class(self):
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count User"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count BaseModel"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count State"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count Review"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count Amenity"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count Place"))
            self.assertEqual("2", f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count City"))
            self.assertEqual("2", f.getvalue().strip())


if __name__ == "__main__":
    unittest.main()

