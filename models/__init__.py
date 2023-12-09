#!/usr/bin/python3
"""Package initialization for the models directory."""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
