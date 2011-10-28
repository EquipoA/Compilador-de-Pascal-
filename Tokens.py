# -*- coding: utf-8 -*-
""" *************************************************************************
FICHERO:        T.py
FECHA:          02.10.2011
AUTORES:        Marcelino Aitor Concepcion Barandela
                Andres Gonzalez Placeres
                Joram Real Gómez
E-MAILS:        alu0100220919@alumnado.ull.es
                alu0100247671@alumnado.ull.es
                alu0100226300@alumnado.ull.es
ASIGNATURA:     Compiladores
DESCRIPCION:    Practica 5
                Diseño e implementacion de un analizador lexico para PASCAL-
COMENTARIOS:    
*************************************************************************** """

class T:

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
        
        if not T.loaded:
            index = 0
            
            for s in T.token_names:
                T.name_to_id[s] = index
                T.id_to_name[index] = s
                index += 1
                
            T.loaded = True
            
            T.AND =               T.get_id('AND');
            T.ARRAY =             T.get_id('ARRAY');
            T.ASTERISK =          T.get_id('ASTERISK');
            T.BECOMES =           T.get_id('BECOMES');
            T.BEGIN =             T.get_id('BEGIN');
            T.COLON =             T.get_id('COLON');
            T.COMMA =             T.get_id('COMMA');
            T.CONST =             T.get_id('CONST');
            T.DIV =               T.get_id('DIV');
            T.DO =                T.get_id('DO');
            T.DOUBLEDOT =         T.get_id('DOUBLEDOT');
            T.ELSE =              T.get_id('ELSE');
            T.END =               T.get_id('END');
            T.ENDTEXT =           T.get_id('ENDTEXT');
            T.EQUAL =             T.get_id('EQUAL');
            T.GREATER =           T.get_id('GREATER');
            T.ID =                T.get_id('ID');
            T.IF =                T.get_id('IF');
            T.LEFTBRACKET =       T.get_id('LEFTBRACKET');
            T.LEFTPARENTHESIS =   T.get_id('LEFTPARENTHESIS');
            T.LESS =              T.get_id('LESS');
            T.MINUS =             T.get_id('MINUS');
            T.MOD =               T.get_id('MOD');            
            T.NOT =               T.get_id('NOT');
            T.NOTEQUAL =          T.get_id('NOTEQUAL');
            T.NOTGREATER =        T.get_id('NOTGREATER');
            T.NOTLESS =           T.get_id('NOTLESS');
            T.NUMERAL =           T.get_id('NUMERAL');
            T.OF =                T.get_id('OF');
            T.OR =                T.get_id('OR');
            T.PERIOD =            T.get_id('PERIOD'); 
            T.PLUS =              T.get_id('PLUS');
            T.PROCEDURE =         T.get_id('PROCEDURE'); 
            T.PROGRAM =           T.get_id('PROGRAM');
            T.RECORD =            T.get_id('RECORD');
            T.RIGHTBRACKET =      T.get_id('RIGHTBRACKET');
            T.RIGHTPARENTHESIS =  T.get_id('RIGHTPARENTHESIS');
            T.SEMICOLON =         T.get_id('SEMICOLON'); 
            T.THEN =              T.get_id('THEN'); 
            T.TYPE =              T.get_id('TYPE');
            T.TOKEN_ERROR =       T.get_id('TOKEN_ERROR');
            T.VAR =               T.get_id('VAR');
            T.WHILE =             T.get_id('WHILE');                
                       
        

    # Dada una cadena con el nombre de un token, devuelve su id
    @staticmethod
    def get_id(string):
        T.load()
        upper = string.upper()
        if upper in T.name_to_id:
            return T.name_to_id[upper]
        else:
            return -1
        

    # Dada una id de token, devuelve una cadena con su nombre
    @staticmethod
    def get_name(t_id):
        T.load()
        if t_id in T.id_to_name:
            return T.id_to_name[t_id]
        else:
            return "NOT A TOKEN"
