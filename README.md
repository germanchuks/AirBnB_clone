# AirBnB clone - The console

## Description
This project is a Python command interpreter designed for managing objects within the AirBnB project. It allows users to create, retrieve, update, and delete objects, perform operations on objects, and handle various tasks related to object management. The interpreter is implemented using the cmd module in Python.

### File Usage
File Name | Description
--- | ---
[console.py](https://github.com/germanchuks/monty/blob/master/console.py) | ...


### Execution
Execute the `console.py` script to start the command interpreter:
```
$ ./console.py
```

### Usage
Interactive Mode:
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
```

Non-Interactive Mode:
```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) EOF
```

### Examples
Retrieve information about specific command:
```
$ ./console.py
(hbnb) help help
List available commands with "help" or detailed help with "help cmd".
```

Retrieve the number of instances of a class:
```
$ ./console.py
(hbnb) User.count()
2
```

Retrieve an instance based on its ID:
```
$ ./console.py
(hbnb) User.show("246c227a-d5c1-403d-9bc7-6a47bb9f0f68")
[User] (246c227a-d5c1-403d-9bc7-6a47bb9f0f68) {'first_name': 'Betty', 'last_name': 'Bar', 'created_at': datetime.datetime(2017, 9, 28, 21, 12, 19, 611352), 'updated_at': datetime.datetime(2017, 9, 28, 21, 12, 19, 611363), 'password': '63a9f0ea7bb98050796b649e85481845', 'email': 'airbnb@mail.com', 'id': '246c227a-d5c1-403d-9bc7-6a47bb9f0f68'}
```

Destroy an instance based on ID:
```
$ ./console.py
(hbnb) User.count()
2
(hbnb) User.destroy("246c227a-d5c1-403d-9bc7-6a47bb9f0f68")
(hbnb) User.count()
1
```

### Testing
Execute the following command to run provided tests:
```
echo "python3 -m unittest discover tests" | bash
```

## Authors
* **Michael Chukwunwe** (https://github.com/stuckwithprogression)
* **German Daniel** (https://github.com/germanchuks)
