# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        Tokens.py
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

class Tokens:

    # Lista de tokens del lenguaje.    
    token_names = [
    'AND',
    'ARRAY',
    'ASTERISK',
    'BECOMES',
    'BEGIN', 
    'COLON',
    'COMMA',
    'CONST',
    'DIV',
    'DO',
    'DOUBLEDOT',
    'ELSE',
    'END',
    'ENDTEXT',
    'EQUAL',
    'GREATER',
    'ID',
    'IF',
    'LEFTBRACKET',
    'LEFTPARENTHESIS',
    'LESS',
    'MINUS',
    'MOD',
    'NOT',
    'NOTEQUAL',
    'NOTGREATER',
    'NOTLESS',
    'NUMERAL',
    'OF',
    'OR',
    'PERIOD', 
    'PLUS',
    'PROCEDURE', 
    'PROGRAM',
    'RECORD',
    'RIGHTBRACKET',
    'RIGHTPARENTHESIS',
    'SEMICOLON', 
    'THEN', 
    'TYPE',
    'TOKEN_ERROR', 
    'VAR',
    'WHILE'
    ]

    name_to_id = dict() # Diccionario que usa un nombre de token como clave y una id de token como valor.
    id_to_name = dict() # Diccionario que usa una id de token como clave y un nombre de token como valor.

    loaded = False	# Indica si los diccionarios han sido creados.


    # Crea los diccionarios
    @staticmethod
    def load():
        
        if not Tokens.loaded:
            index = 0
            
            for s in Tokens.token_names:
                Tokens.name_to_id[s] = index
                Tokens.id_to_name[index] = s
                index += 1
                
            Tokens.loaded = True
            
            Tokens.AND =               Tokens.get_id('AND');
            Tokens.ARRAY =             Tokens.get_id('ARRAY');
            Tokens.ASTERISK =          Tokens.get_id('ASTERISK');
            Tokens.BECOMES =           Tokens.get_id('BECOMES');
            Tokens.BEGIN =             Tokens.get_id('BEGIN');
            Tokens.COLON =             Tokens.get_id('COLON');
            Tokens.COMMA =             Tokens.get_id('COMMA');
            Tokens.CONST =             Tokens.get_id('CONST');
            Tokens.DIV =               Tokens.get_id('DIV');
            Tokens.DO =                Tokens.get_id('DO');
            Tokens.DOUBLEDOT =         Tokens.get_id('DOUBLEDOT');
            Tokens.ELSE =              Tokens.get_id('ELSE');
            Tokens.END =               Tokens.get_id('END');
            Tokens.ENDTEXT =           Tokens.get_id('ENDTEXT');
            Tokens.EQUAL =             Tokens.get_id('EQUAL');
            Tokens.GREATER =           Tokens.get_id('GREATER');
            Tokens.ID =                Tokens.get_id('ID');
            Tokens.IF =                Tokens.get_id('IF');
            Tokens.LEFTBRACKET =       Tokens.get_id('LEFTBRACKET');
            Tokens.LEFTPARENTHESIS =   Tokens.get_id('LEFTPARENTHESIS');
            Tokens.LESS =              Tokens.get_id('LESS');
            Tokens.MINUS =             Tokens.get_id('MINUS');
            Tokens.MOD =               Tokens.get_id('MOD');            
            Tokens.NOT =               Tokens.get_id('NOT');
            Tokens.NOTEQUAL =          Tokens.get_id('NOTEQUAL');
            Tokens.NOTGREATER =        Tokens.get_id('NOTGREATER');
            Tokens.NOTLESS =           Tokens.get_id('NOTLESS');
            Tokens.NUMERAL =           Tokens.get_id('NUMERAL');
            Tokens.OF =                Tokens.get_id('OF');
            Tokens.OR =                Tokens.get_id('OR');
            Tokens.PERIOD =            Tokens.get_id('PERIOD'); 
            Tokens.PLUS =              Tokens.get_id('PLUS');
            Tokens.PROCEDURE =         Tokens.get_id('PROCEDURE'); 
            Tokens.PROGRAM =           Tokens.get_id('PROGRAM');
            Tokens.RECORD =            Tokens.get_id('RECORD');
            Tokens.RIGHTBRACKET =      Tokens.get_id('RIGHTBRACKET');
            Tokens.RIGHTPARENTHESIS =  Tokens.get_id('RIGHTPARENTHESIS');
            Tokens.SEMICOLON =         Tokens.get_id('SEMICOLON'); 
            Tokens.THEN =              Tokens.get_id('THEN'); 
            Tokens.TYPE =              Tokens.get_id('TYPE');
            Tokens.TOKEN_ERROR =       Tokens.get_id('TOKEN_ERROR');
            Tokens.VAR =               Tokens.get_id('VAR');
            Tokens.WHILE =             Tokens.get_id('WHILE');                
                       
        

    # Dada una cadena con el nombre de un token, devuelve su id
    @staticmethod
    def get_id(string):
        Tokens.load()
        upper = string.upper()
        if upper in Tokens.name_to_id:
            return Tokens.name_to_id[upper]
        else:
            return -1
        

    # Dada una id de token, devuelve una cadena con su nombre
    @staticmethod
    def get_name(t_id):
        Tokens.load()
        if t_id in Tokens.id_to_name:
            return Tokens.id_to_name[t_id]
        else:
            return "NOT A TOKEN"
