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

    testrezept = sql_repo.add(test_rezept)

    assert len(sql_repo.all()) == 1

    assert test_rezept.name == "Test_Rezept 1"

    assert len([r.name for r in test_rezept.zutaten]) == 2

    assert testrezept.rezept_id == 1


def test_remove(sql_repo,test_rezept):

    sql_repo.add(test_rezept)

    assert len(sql_repo.all()) == 1

    sql_repo.remove(test_rezept)

    assert len(sql_repo.all()) == 0

def test_update(sql_repo,test_rezept):
    testrezept = sql_repo.add(test_rezept)

    testrezept.name = "Geändertes_Test_Rezept 1"
    testrezept.gang = "Geänderter_Gang 1"
    testrezept.rezept_id = 5

    sql_repo.update(test_rezept)

    assert testrezept.name == "Geändertes_Test_Rezept 1"
    assert testrezept.gang == "Geänderter_Gang 1"
    assert [rezept.rezept_id for rezept in sql_repo.all()] == [1]
    # gleicher test aber einfacher, ohne lc über Index
    assert sql_repo.all()[0].rezept_id == 1