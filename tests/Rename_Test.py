import unittest
from mo_sql_parsing import parse
import src.SQL_To_JSON.renameSQL as ren
import src.Creates_To_JSON.Creates_Json as create


class Rename_Test(unittest.TestCase):

    def test_addId(self):
        res = ren.rename_json(parse("SELECT nombre FROM Persona"), create.create_tables_json(
            ["create table Persona(nombre varchar2(30) primary key);"]))
        # formato parse
        expected = {'select': {'value': 'Persona1.nombre'},
                    'from': {'value': 'Persona',
                             'name': 'Persona1'}}
        # formato sql_to_json
        # expected =

        self.assertEqual(res, expected)

    def test_Persona(self): # falla, porque detecta Persona.nombre como renombramiento que no encuentra
        res = ren.rename_json(parse("SELECT Persona.nombre FROM Persona"), create.create_tables_json(
            ["create table Persona(nombre varchar2(30) primary key);"]))
        # formato parse
        expected = {'select': {'value': 'Persona1.nombre'},
                    'from': {'value': 'Persona',
                             'name': 'Persona1'}}
        # formato sql_to_json
        # expected =

        self.assertEqual(res, expected)

    def test_p(self):
        res = ren.rename_json(parse("SELECT p.nombre FROM Persona p"), create.create_tables_json(
            ["create table Persona(nombre varchar2(30) primary key);"]))
        # formato parse
        expected = {'select': {'value': 'Persona1.nombre'},
                    'from': {'value': 'Persona',
                             'name': 'Persona1'}}
        # formato sql_to_json
        # expected =

        self.assertEqual(res, expected)

    def test_pj(self):
        res = ren.rename_json(parse("SELECT p.nombre FROM Jugador j join persona p"), create.create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ]))
        # formato parse
        expected = {'select': {'value': 'persona1.nombre'},
                    'from': [{'value': 'Jugador',
                              'name': 'Jugador1'},
                             {'join': {'value': 'persona',
                                       'name': 'persona1'
                                       }
                              }
                             ]
                    }
        # formato sql_to_json
        # expected =

        self.assertEqual(res, expected)

    def test_sameRename(self):
        self.assertRaises(ren.ErrorRenameSQL, ren.rename_json, parse("SELECT p.nombre FROM Jugador p join persona p"), create.create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ]))

    def test_ambColumn(self): #esta realmente no es de renombramiento
        self.assertRaises(ren.ErrorRenameSQL, ren.rename_json, parse("SELECT nombre, dni FROM Jugador  join persona "), create.create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(nombre varchar2(30),dni varchar2(30) primary key);" ]))



if __name__ == "__main__":
    unittest.main()