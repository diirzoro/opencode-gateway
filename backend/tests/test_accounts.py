def registration():
    return {"username":"owner","email":"admin@example.com","password":"securepass1","phone":"+967123456","postal_code":"00000","country_id":1,"region_id":1,"city_id":1}

def test_register_profile_logout_login_and_admin_list(client):
    response=client.post("/api/auth/register",json=registration()); assert response.status_code==201
    user=response.json(); assert user["trial_remaining_days"]==10; assert user["role"]=="customer"
    assert client.get("/api/profile").json()["country"]=="Yemen"
    assert client.post("/api/auth/logout").status_code==204
    assert client.get("/api/auth/me").status_code==401
    assert client.post("/api/auth/login",json={"identity":"owner","password":"securepass1"}).status_code==200

def test_registration_validation_and_duplicates(client):
    data=registration(); assert client.post("/api/auth/register",json=data).status_code==201
    assert client.post("/api/auth/register",json=data).status_code==409
    bad={**data,"username":"new-user","email":"new@example.com","password":"weak"}
    assert client.post("/api/auth/register",json=bad).status_code==422

def test_customer_cannot_list_admin_users(client):
    data={**registration(),"username":"customer","email":"customer@example.com"}
    assert client.post("/api/auth/register",json=data).status_code==201
    assert client.get("/api/admin/users").status_code==403

def test_location_endpoints(client):
    assert client.get("/api/locations/countries").json()[0]["code"]=="YE"
    assert client.get("/api/locations/countries/1/regions").json()[0]["name"]=="Sana'a"
    assert client.get("/api/locations/regions/1/cities").json()[0]["name"]=="Sana'a"

def test_admin_can_list_registered_users(client):
    from sqlalchemy import select
    from app.models import User
    from conftest import TestingSession
    assert client.post("/api/auth/register",json=registration()).status_code==201
    with TestingSession() as db:
        user=db.scalar(select(User).where(User.email=="admin@example.com")); user.role="admin"; db.commit()
    assert client.post("/api/auth/login",json={"identity":"admin@example.com","password":"securepass1"}).status_code==200
    users=client.get("/api/admin/users"); assert users.status_code==200; assert users.json()[0]["username"]=="owner"
