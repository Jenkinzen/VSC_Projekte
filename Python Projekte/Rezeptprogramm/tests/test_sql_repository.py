import pytest
import rezeptliste_model as model
from rezeptliste_repository import SqlRezeptRepository
import sqlite3


@pytest.fixture
def test_rezept():
    return model.Rezept("Test_Rezept 1",[model.Zutaten("Test_Zutat 1","Test_Menge 1","Test_Einheit 1"),model.Zutaten("Test_Zutat 2","Test_Menge 2","Test_Einheit 2")],"Test_Zubereitung 1","Test_Gang 1","Test_Notizen 1")


@pytest.fixture
def sql_repo():
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")

    repo = SqlRezeptRepository(connection)
    repo.create_tables()

    yield repo

    connection.close()