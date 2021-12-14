# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re






EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# model the class after the friend table from our database
class Users:
    def __init__( self , data ):
        #put attributes here
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # 1.Now we use class methods to query our database
    # 2.In our methods, we always need a query
    # 3.we need a variable to hold our results when calling connectToMySQL to our database.query_db(*query*)
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL('log_user_db').query_db(query)
    #     # Create an empty list to append our instances of data
    #     users = []
    #     # Iterate over the db results and create instances of data with cls.
    #     for data in results:
    #         users.append( cls(data) )
    #     return users

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('log_user_db').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('log_user_db').query_db(query, data)
        return cls(results[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, pw) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s);"
        results = connectToMySQL('log_user_db').query_db(query, data)
        return results

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE ### SET ###=%(###)s,###=%(###)s,###=%(###)s WHERE id = %(id)s;" 
    #     return connectToMySQL('NAME_OF_DATA_BASE').query_db(query,data)
            
    # @classmethod
    # def delete(cls, data):
    #     query =  "DELETE FROM ### WHERE id = %(id)s;"
    #     return connectToMySQL('NAME_OF_DATA_BASE').query_db(query,data)

    @staticmethod
    def validate_reg(user):
        is_valid = True
        
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 character.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 character.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("invalid email address!")
            is_valid = False
        if len(user['pw']) < 6:
            flash("password must be at least 6 character.")
            is_valid = False
        return is_valid