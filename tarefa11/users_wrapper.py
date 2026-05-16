import requests

API_URL = "https://jsonplaceholder.typicode.com/users"

def list():
    request = requests.get(f"{API_URL}")
    if request.status_code == 200:
        return request.json()
    else:
        return False
    
def create(user_data):
    request = requests.post(f"{API_URL}", json=user_data)
    if request.status_code == 201:
        return request.json()
    else:
        return False
    
def read(user_id):
    request = requests.get(f"{API_URL}{user_id}")
    if request.status_code == 200:
        return request.json()
    else:
        return False
    
def update(user_id, user_data):
    request = requests.put(f"{API_URL}{user_id}", json=user_data)
    if request.status_code == 200:
        return request.json()
    else:
        return False
    
def delete(user_id):
    request = requests.delete(f"{API_URL}{user_id}")
    if request.status_code == [204, 204]:
        return True
    else:
        return False