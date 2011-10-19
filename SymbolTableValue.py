# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        SymbolTableValue.py
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

# Clase nodo de la tabla de simbolos.

class SymbolTableValue:
    
    lexeme = ''
    index = int     # used if this symbol is an identifier
    token_id = int  # used if this symbol is a reserved word   
    line = int
    column = int
    
    def __init__(self, lexeme, index, token_id, line, column):        
        self.lexeme = lexeme  
        self.index = index
        self.token_id = token_id
        self.line = line
        self.column = column        

    def __str__(self):
        string = self.lexeme +  ' ' 
        string += str(self.index) + ' ' + str(self.token_id) + ' '
        string += str(self.line) + ' ' + str(self.column)
        return string
