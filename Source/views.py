# views.py
# handles application routing

from models.py import Base User
from flask import Flask, jsonify, request, url_for, abort