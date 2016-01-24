from system.core.model import Model

import re
class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()

    def register_user(self,user_info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not user_info['name']:
            errors.append('Name cannot be empty')

        if len(user_info['name']) < 3:
            errors.append('Name must be longer than 3 character')
        if not user_info['alias']:
            errors.append('Alias cannot be empty')
        # if len(user_info['alias']) < 3:
        #     errors.append('Last Name must be longer than 3 character')
        if not user_info['email']:
            errors.append('Email field cannot be empty')
        if not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email not a valid format')
        if not user_info['password']:
            errors.append('Password field cannot be empty')
        if len(user_info['password']) < 5:
            errors.append('Password must be longer than 4 characters')
        if not user_info['confirm_password']:
            errors.append('Confirm Password field cannot be empty')
        if user_info['password'] != user_info['confirm_password']:
            errors.append('Passwords do not match')
            print errors
        if errors:
            return {'status': False, 'errors' : errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(user_info['password'])
            query = "INSERT INTO users (name,alias,email,password,created_at,updated_at) VALUES (%s,%s,%s,%s,NOW(),NOW())"
            data = [user_info['name'],user_info['alias'],user_info['email'],hashed_pw]

            self.db.query_db(query,data)

            get_user = "Select * From users Order By id DESC LIMIT 1"
            user = self.db.query_db(get_user)
            return {'status' : True , 'user' : user[0]}

    def login_user(self,user_info):
        errors = []
        if not user_info['password']:
            errors.append('Password Cannot be empty')

        if not user_info['email']:
            errors.append('Email Cannot be empty')

        if errors:
            return {'status' : False, 'errors': errors}
        else:
            query = 'Select * From users Where email = %s'
            data = [user_info['email']]
            user = self.db.query_db(query,data)

            if len(user) > 0:
                if self.bcrypt.check_password_hash(user[0]['password'], user_info['password']):
                    return {'status' : True, 'user' : user[0]}
                else:
                    errors.append('Password or Email is Invalid')
                    return {'status' : False, 'errors': errors}
            else:
                errors.append('Email was not found')
                return {'status' : False, 'errors': errors}
