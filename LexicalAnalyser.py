# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        LexicalAnalyser.py
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

import string
from Tokens import Tokens
from SymbolTable import SymbolTable

class LexicalAnalyser:

    separators = [' ', '\t', '\n', '\r', '{']	# Conjunto de separadores   
    
    lexeme_begin = 0				# Puntero que indica el comienzo de la sub-cadena que esta siendo analizada
    forward = 0                                 # Puntero de avance
    current_line = 1				# Linea siendo analizada
    current_column = 1				# Columna siendo analizada


    string_buffer = ""
    string_buffer_len = 0

    
    def __init__(self, ifile, symbol_table):
        self.string_buffer = ifile.read()
        self.string_buffer_len = len(self.string_buffer)
        self.symbol_table = symbol_table


    def yylex(self):
        return self.get_token()

    def get_token(self):        
     
        def next_line():
            self.forward += 1
            self.current_line += 1
            self.current_column = 1
            

        def next_column():
            self.forward += 1
            self.current_column += 1
            

        def move_begin():
            self.lexeme_begin = self.forward
            
            
        def ignore_others():            
            pairs = 0
            while self.forward < self.string_buffer_len \
                    and (self.string_buffer[self.forward] in self.separators \
                    or pairs > 0):
                if self.string_buffer[self.forward] == '\n':
                    next_line()
                else:
                    if self.string_buffer[self.forward] == '{':
                        pairs += 1
                    elif self.string_buffer[self.forward] == '}':
                        pairs -= 1
                    next_column()
            move_begin()
            if pairs == 0:
                return True
            else:
                return False
            

        def is_id():
            if self.forward < self.string_buffer_len \
                    and self.string_buffer[self.forward].isalpha():
                while self.forward < self.string_buffer_len \
                        and (self.string_buffer[self.forward].isalnum() \
                        or self.string_buffer[self.forward] == '_'):
                    next_column()
                return True
            
            return False
        

        def is_special_symbol():
            if self.forward < self.string_buffer_len:
                char = self.string_buffer[self.forward]
                
                if char == ':':
                    next_column()
                    if self.forward < self.string_buffer_len \
                            and self.string_buffer[self.forward] == '=':
                        next_column()
                        return Tokens.BECOMES
                    else:
                        return Tokens.COLON
                    
                elif char == '*':
                    next_column()
                    return Tokens.ASTERISK
                
                elif char == '+':
                    next_column()
                    return Tokens.PLUS
                
                elif char == '-':
                    next_column()
                    return Tokens.MINUS
                
                elif char == '=':
                    next_column()
                    return Tokens.EQUAL
                
                elif char == ';':
                    next_column()
                    return Tokens.SEMICOLON
                
                elif char == '(':
                    next_column()
                    return Tokens.LEFTPARENTHESIS
                
                elif char == ')':
                    next_column()
                    return Tokens.RIGHTPARENTHESIS
                    
                elif char == '<':
                    next_column()
                    if self.forward < self.string_buffer_len \
                            and self.string_buffer[self.forward] == '=':
                        next_column()
                        return Tokens.NOTGREATER
                    elif self.forward < self.string_buffer_len \
                            and self.string_buffer[self.forward] == '>':
                        next_column()
                        return Tokens.NOTEQUAL
                    else:                   
                        return Tokens.LESS
                
                elif char == '>':
                    next_column()
                    if self.forward < self.string_buffer_len \
                            and self.string_buffer[self.forward] == '=':
                        next_column()
                        return Tokens.NOTLESS
                    else:                    
                        return Tokens.GREATER
                
                elif char == '[':
                    next_column()
                    return Tokens.LEFTBRACKET
                
                elif char == ']':
                    next_column()
                    return Tokens.RIGHTBRACKET
                elif char == ',':
                    next_column()
                    return Tokens.COMMA
                
                elif char == '.':
                    next_column()
                    if self.forward < self.string_buffer_len \
                            and self.string_buffer[self.forward] == '.':
                        next_column()
                        return Tokens.DOUBLEDOT
                    else:
                        return Tokens.PERIOD
                

        def is_numeral():
            numeral = False
            while self.forward < self.string_buffer_len \
                    and self.string_buffer[self.forward].isdigit():
                numeral = True
                next_column()
            return numeral
        

        def build_id_pair():        
            lexeme = self.string_buffer[self.lexeme_begin:self.forward]
            ref = self.symbol_table.install_id(lexeme, self.current_line, self.current_column)

            t_id  = self.symbol_table.is_keyword(ref)
            if t_id == -1:
                t_id = Tokens.ID
                
            #debug version
            return (t_id, ref, lexeme, self.current_line, self.current_column)
            #return (t_id, ref)
        
        

        def build_numeral_pair():        
            lexeme = self.string_buffer[self.lexeme_begin:self.forward]
            ref = self.symbol_table.install_id(lexeme, self.current_line, self.current_column)

            #debug version
            return (Tokens.NUMERAL, ref, lexeme, self.current_line, self.current_column)            
            #return (Tokens.NUMERAL, ref) 

        move_begin()            

        if  not ignore_others():
            #debug version
            return (Tokens.TOKEN_ERROR, -1, "TOKEN_ERROR" , self.current_line, self.current_column)
            #return (Tokens.TOKEN_ERROR, -1) # comentario sin cerrar        
       
        if is_id():
            return build_id_pair()
            
        t_id = is_special_symbol()
        if t_id >= 0:
            #debug version
            return (t_id, -1, "SPECIAL", self.current_line, self.current_column)
            #return (t_id, -1)
                
        if is_numeral():
            return build_numeral_pair()
            
        if self.forward < self.string_buffer_len:
            next_column()
            #debug version
            return (Tokens.TOKEN_ERROR, -1, "TOKEN_ERROR" , self.current_line, self.current_column)
            #return (Tokens.TOKEN_ERROR, -1)
        
        #debug version        
        return (Tokens.ENDTEXT, -1, "ENDTEXT", self.current_line, self.current_column)
        #return (Tokens.ENDTEXT, -1)
