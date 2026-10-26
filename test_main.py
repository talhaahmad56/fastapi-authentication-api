USER = {
    "username" : "testuser",
    "email" : "test@gmail.com",
    "password" : "password123"
    }

def register_login(clients , user = USER):
    clients.post("/register" , json = user)
    response = clients.post("/login" , data = {
        "username" : user["username"],
        "password" : user["password"],
    })

    token = response.json()["access_token"]
    return {"authorization" :f"Bearer {token}"}


def test_register(clients):
    response = clients.post("/register" , json = USER)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "hashed_password" not in data


def test_register_duplicate_username(clients):
    clients.post("/register" , json = USER)
    response = clients.post("/register" , json = USER)

    assert response.status_code == 409

def test_login_successfull(clients):
    clients.post("/register" , json = USER)
    response = clients.post("/login" , data = {
        "username" : "testuser",
        "password" : "password123",
    })

    assert response.status_code == 200

    assert "access_token" in response.json()

def test_login_wrong_password(clients):
    clients.post("/register" , json = USER)
    response = clients.post("/login" , data = {
        "username" : "testuser",
        "password" : "wrongpassword",
    })

    assert response.status_code == 401

def test_me_without_token(clients):
    response = clients.get("/me")
    assert response.status_code == 401

def test_me_with_token(clients):
    headers = register_login(clients)
    response = clients.get("/me" , headers = headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_username(clients):
    headers = register_login(clients)
    response = clients.patch("/update" , json={"username" : "newname" , "email" : "newmail@gmail.com"} , headers = headers)
    assert response.status_code == 200
    assert response.json()["username"] == "newname"
    assert response.json()["email"] == "newmail@gmail.com"  

def test_taken_username_email(clients):
    headers =  register_login(clients)
    others = {"username" : "other" , "email" : "other@gmail.com" , "password" : "password123"}
    clients.post("/register" , json = others)
    response = clients.patch("/update" , json={"username" : "other" , "email" : "other@gmail.com"} , headers = headers)
    assert response.status_code == 409    

def test_delete(clients):
    headers = register_login(clients)
    response = clients.delete("/delete" , headers = headers)
    assert response.status_code == 204     




    