from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES ( %(fname)s, %(lname)s, %(eml)s, NOW(), NOW() );"
        return connectToMySQL('users_schema').query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL('users_schema').query_db(query, data)

    @classmethod
    def updated(cls, data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(eml)s, updated_at = NOW() WHERE id=%(id)s"
        return connectToMySQL('users_schema').query_db(query, data)

    @classmethod
    def display_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL('users_schema').query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['fname']) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last Name must be at least 2 characters")
            is_valid = False
        if len(data['eml']) < 12:
            flash("Email Address must be at least 12 characters")
            is_valid = False
        return is_valid
