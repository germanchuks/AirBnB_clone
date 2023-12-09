#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from datetime import datetime


def parse(arg):
    """Identifies and extract tokens using regular expresion"""
    match_update = re.match(r"(\w+) \"([\w-]+)\", ({.*})", arg)
    if match_update:
        class_name = match_update.group(1)
        uuid = match_update.group(2)
        attributes = match_update.group(3)
        return [f"{class_name}", uuid, eval(attributes)]
    else:
        match_brackets = re.search(r"\[(.*?)\]", arg)
        match_curly_braces = re.search(r"\{(.*?)\}", arg)
        if match_curly_braces is None and match_brackets is None:
            return [token.strip(",") for token in split(arg)]
        else:
            first_bracket = match_curly_braces if (match_curly_braces and
                                                   match_curly_braces.start()
                                                   < match_brackets.start()) \
                else match_brackets
            lexer = split(arg[:first_bracket.start()])
            tokens = [token.strip(",") for token in lexer]
            tokens.append(first_bracket.group())
            return tokens


class HBNBCommand(cmd.Cmd):
    """Entry point of the HBnB Command Interpreter."""

    prompt = "(hbnb) "
    __all_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Empty line executes nothing."""
        pass

    def default(self, arg):
        """Default cmd commands for invalid inputs"""
        arg_dict = {
            "show": self.do_show,
            "destroy": self.do_destroy,
            "all": self.do_all,
            "update": self.do_update,
            "count": self.do_count
        }

        parts = re.split(r'\.|\(', arg)

        if len(parts) == 3 and parts[1] in arg_dict:
            command, parameter = parts[1], parts[2][:-1]
            call = f"{parts[0]} {parameter}"
            return arg_dict[command](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the ID.
        Usage: create <class name>"""
        try:
            if not arg:
                raise SyntaxError()

            args_list = arg.split(" ")

            kwargs = {}
            for item in args_list[1:]:
                key, value = item.split("=")
                value = value.strip('"').replace("_", " ") \
                    if value[0] == '"'else eval(value)
                kwargs[key] = value

            class_name = args_list[0]
            if class_name not in HBNBCommand.__all_classes:
                raise NameError()

            new_inst = eval(class_name)(**kwargs) if kwargs else \
                eval(class_name)()
            storage.new(new_inst)
            print(new_inst.id)
            new_inst.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints string representation of an instance based on class name
        and ID. Usage: show <class name> <id> or <class name>.show(<id>)"""
        argl = parse(arg)
        obj_stored = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__all_classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif f"{argl[0]}.{argl[1]}" not in obj_stored:
            print("** no instance found **")
        else:
            key = f"{argl[0]}.{argl[1]}"
            print(obj_stored[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id> or <class name>.destroy(<id>)"""
        argl = parse(arg)
        obj_stored = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__all_classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif f"{argl[0]}.{argl[1]}" not in obj_stored.keys():
            print("** no instance found **")
        else:
            key = f"{argl[0]}.{argl[1]}"
            del obj_stored[key]
            storage.save()

    def do_all(self, arg):
        """Retrieves all instances of a class. Usage: all or all <class name>
        or <class name>.all()."""
        argl = parse(arg)
        stored_objects = storage.all()
        if len(argl) > 0 and argl[0] not in HBNBCommand.__all_classes:
            print("** class doesn't exist **")
        else:
            if len(argl) > 0:
                class_name = argl[0]
                class_instances = {key: value for key, value in
                                   stored_objects.items() if
                                   key.startswith(class_name)}
                if not class_instances:
                    print("** no instances found **")
                else:
                    print(class_instances)
            else:
                print(stored_objects)

    def do_update(self, arg):
        """Updates an instance based on the class name and ID by adding or
        updating attributes. Usage: update <class> <id> <attribute_name>
        <attribute_value> or <class>.update(<id>, <attribute_name>,
        <attribute_value>) or <class>.update(<id>, <dictionary>)"""
        argl = parse(arg)
        obj_stored = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__all_classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if f"{argl[0]}.{argl[1]}" not in obj_stored.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3 and type(argl[2]) != dict:
            print("** value missing **")
            return False

        if len(argl) == 4:
            obj_key = f"{argl[0]}.{argl[1]}"
            obj_dict = obj_stored[obj_key]
            attr_name = argl[2]
            attr_val = argl[3]

            if attr_name in ["id", "created_at", "updated_at"]:
                return

            if hasattr(obj_dict, attr_name):
                attr_present = getattr(obj_dict, attr_name)
                attr_type = type(attr_present)
                try:
                    setattr(obj_dict, attr_name, attr_type(attr_val))
                except (ValueError, TypeError):
                    setattr(obj_dict, attr_name, str(attr_val))
            else:
                setattr(obj_dict, attr_name, str(attr_val))

            obj_dict.updated_at = datetime.now().isoformat()

        if len(argl) == 3 and type(argl[2]) == dict:
            obj_key = f"{argl[0]}.{argl[1]}"
            attribute_dict = argl[2]
            obj_dict = obj_stored[obj_key]

            for attr_name, attr_val in attribute_dict.items():
                if attr_name in ["id", "created_at", "updated_at"]:
                    return
                if hasattr(obj_dict, attr_name):
                    attr_present = getattr(obj_dict, attr_name)
                    attr_type = type(attr_present)
                    try:
                        setattr(obj_dict, attr_name, attr_type(attr_val))
                    except Exception:
                        setattr(obj_dict, attr_val)
                else:
                    setattr(obj_dict, attr_name, attr_val)

            obj_dict.updated_at = datetime.now().isoformat()

        storage.save()

    def do_count(self, arg):
        """Retrieves the number of instances of a class.
        Usage: count <class name> or <class name>.count()"""
        argl = parse(arg)
        if not argl:
            print("** class name missing **")
            return
        elif not argl[0] in HBNBCommand.__all_classes:
            print("** class doesn't exist **")
            return
        else:
            count = 0
            class_instances = {key: value for key, value in
                               storage.all().items()
                               if key.startswith(argl[0])}
            count = len(class_instances)
            print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
