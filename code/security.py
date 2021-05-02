from user import User

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = { u.username: u for u in users }

userid_mapping = { u.id: u for u in users}

# authenticating the user
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user
    
# identity takes the payload, which is the content of jwt-token
def identity(payload):
    user_id = payload['identity'] # getting the user id from that payload# getting the user id from that payload
    return userid_mapping.get(user_id, None)
