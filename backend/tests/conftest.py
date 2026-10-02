import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["COOKIE_SECURE"] = "false"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.models import City, Country, Region
engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
@pytest.fixture(autouse=True)
def database():
    Base.metadata.create_all(engine)
    with TestingSession() as db:
        country=Country(id=1,name="Yemen",code="YE",enabled=True); region=Region(id=1,country_id=1,name="Sana'a",enabled=True); city=City(id=1,region_id=1,name="Sana'a",enabled=True)
        db.add_all([country,region,city]); db.commit()
    yield
    Base.metadata.drop_all(engine)
def override_db():
    with TestingSession() as db: yield db
app.dependency_overrides[get_db] = override_db
@pytest.fixture
def client(): return TestClient(app)
