# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        SymbolTable.py
FECHA:          02.10.2011
AUTORES:        Marcelino Aitor Concepcion Barandela
                Andres Gonzalez Placeres
                Joram Real Gómez
E-MAILS:        alu0100220919@alumnado.ull.es
                alu0100247671@alumnado.ull.es
                alu0100226300@alumnado.ull.es
ASIGNATURA:     Compiladores
DESCRIPCION:    Practica 3
                Diseño e implementacion de un analizador lexico para PASCAL-
COMENTARIOS:    
*************************************************************************** """

from Tokens import Tokens
from SymbolTableValue import SymbolTableValue

keywords = [
    'and',
    'array',
    'begin',
    'const',
    'div',
    'do',
    'else',
    'end',
    'if',
    'mod',
    'not',
    'of',
    'or',
    'procedure',
    'program',
    'record',
    'then',
    'type',
    'var',
    'while'
]

standard_identifiers = [
    'integer',
    'boolean',
    'false',
    'true',
    'read',
    'write'
]

# Clase que define la tabla de simbolos y sus metodos para acceder a ella y modificarla
class SymbolTable:    

    lexeme_id_table = dict()
    id_symbol_table = dict()
    table_size = 0;
    id_count = 1;


    # Inicia la tabla de simbolos con las palabras clave y los identificadores estandard    
    def __init__(self): 
        for keyword in keywords:
            token_id = Tokens.get_id(keyword)
            if token_id != -1:
                self.install_keyword(keyword, token_id)

        for standard_id in standard_identifiers:
            self.install_id(standard_id, 0, 0)


    # Retorna la posicion del lexema en la tabla o -1 si no lo encuentra  
    def has_lexeme(self,lexeme):
        lexeme = lexeme.upper()
        if lexeme in self.lexeme_id_table:
            return self.lexeme_id_table[lexeme]
        else:
            return -1

    # Inserta un simbolo en la tabla. No comprueba si ya existe un valor en esa posicion            
    def insert_symbol(self,symbol):
        
        self.id_symbol_table[self.table_size] = symbol
        self.lexeme_id_table[symbol.lexeme] = self.table_size
        
        #print str(self.table_size) + ' ' + str(self.id_symbol_table[self.table_size])
        
        self.table_size += 1
        
        return self.table_size - 1

    # Inserta una palabra clave en la tabla y devuelve su posicion en esta.
    def install_keyword(self, lexeme, token_id):
        lexeme = lexeme.upper()
        found_index = self.has_lexeme(lexeme)
        
        if found_index == -1:
            return self.insert_symbol(SymbolTableValue(lexeme, 0, token_id, 0, 0))
        return found_index

    # Inserta un identificador en la tabla y devuelve su posicion. Si existe un
    # identificador con identico lexema, solo devuelve su posicion.
    def install_id(self, lexeme, line, column):
        lexeme = lexeme.upper()
        found_index = self.has_lexeme(lexeme)
        
        if found_index == -1:
            symbol = SymbolTableValue(lexeme, self.id_count, -1, line, column)
            self.id_count += 1
            return self.insert_symbol(symbol)
        return found_index    

    # Comprueba si el contenido de una referencia a la tabla, es una palabra clave
    def is_keyword(self, ref):
        if ref in self.id_symbol_table:
            return self.id_symbol_table[ref].token_id
        return -1
