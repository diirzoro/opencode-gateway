from app.security.passwords import hash_password, verify_password
def test_password_hash_is_salted_and_verifiable():
    first=hash_password("securepass1"); second=hash_password("securepass1")
    assert first != second and "securepass1" not in first
    assert verify_password("securepass1",first)
    assert not verify_password("wrong",first)
