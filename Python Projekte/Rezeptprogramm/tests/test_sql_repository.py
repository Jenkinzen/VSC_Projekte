import pytest
import rezeptliste_model as model
from rezeptliste_repository import SqlRezeptRepository
import sqlite3 as sql


@pytest.fixture
def test_rezept():
    return model.Rezept("Test_Rezept 1",[model.Zutaten("Test_Zutat 1","Test_Menge 1","Test_Einheit 1"),model.Zutaten("Test_Zutat 2","Test_Menge 2","Test_Einheit 2")],"Test_Zubereitung 1","Test_Gang 1","Test_Notizen 1")


@pytest.fixture
def sql_repo():
    connection = sql.connect(":memory:",check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = ON",)

    sql_repo = SqlRezeptRepository(connection)

    yield sql_repo

    connection.close()

def test_add_and_all(sql_repo,test_rezept):
    created_recipe = sql_repo.add(test_rezept)

    sql_repo.all()

    assert len(sql_repo.all()) == 1
