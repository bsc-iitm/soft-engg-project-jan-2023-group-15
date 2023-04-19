import json
from main import app

def test_login():
    data = {
        "obj_data": {
            "user": {
                "displayName": "Test Name",
                "photoURL": "photo URL",
                "email": "test@example.com",
                "uid": "exampleuid"
            }
        }
    }
    response = app.test_client().post("/api/login", json=json.dumps(data))
    json_response = response.get_json()
    assert json_response is not None