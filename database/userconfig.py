from hashlib import sha3_512

class User:
    def __init__(self,username, email, password):
        
        self.username = username
        self.email = email
        self.password = sha3_512(str(password).encode()).hexdigest()

    def get_data(self):
        user_dict = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'tasks': {
                
            }
        }

        return user_dict
