# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        SyntaxAnalyser.py
FECHA:          02.10.2011
AUTORES:        Marcelino Aitor Concepcion Barandela
                Andres Gonzalez Placeres
                Joram Real Gómez
E-MAILS:        alu0100220919@alumnado.ull.es
                alu0100247671@alumnado.ull.es
                alu0100226300@alumnado.ull.es
ASIGNATURA:     Compiladores
DESCRIPCION:    Practica 4
                Diseño e implementacion de un analizador sintactico recursivo predictivo para PASCAL-
COMENTARIOS:    
*************************************************************************** """
import sys

from LexicalAnalyser import LexicalAnalyser
from Tokens import Tokens

class SyntaxAnalyser:
    
    def __init__ (self, lexical_analyser):
        Tokens.load()
        self.lexical_analyser = lexical_analyser
        self.lookahead = self.lexical_analyser.yylex()

    def peek(self):
        return self.lookahead[0]
    
    def syntax_error(self, expected):
        print (expected + " was expected, but " + Tokens.get_name(self.lookahead[0]) + " was found in line " + str(self.lookahead[3]))
        sys.exit("The program is not valid.")

    def match(self, token):
        if self.peek() == token:
            self.lookahead = self.lexical_analyser.yylex()
            #print "Matched " + Tokens.get_name(token)
        else:
            self.syntax_error(Tokens.get_name(token))
            
    # <Program> ::= program program_name ; <Block body> .
    def program(self):
        self.match(Tokens.PROGRAM)
        self.match(Tokens.ID)
        self.match(Tokens.SEMICOLON)
        self.block_body()
        self.match(Tokens.PERIOD)
        

    # <Block body> ::= [<Constant deﬁnition part>] [<Type deﬁnition part>][<Variable deﬁnition part>] {<Procedure deﬁnition>}<Compound statement>    
    def block_body(self):
        if self.peek() == Tokens.CONST:
            self.constant_definition_part()
        if self.peek() == Tokens.TYPE:
            self.type_definition_part()
        if self.peek() == Tokens.VAR:
            self.variable_definition_part()
        while self.peek() == Tokens.PROCEDURE:
            self.procedure_definition()
        self.compound_statement()
        

    # <Constant deﬁnition part> ::= const <Constant deﬁnition> {<Constant deﬁnition>}
    def constant_definition_part(self):
        self.match(Tokens.CONST)
        self.constant_definition()
        while self.peek() == Tokens.ID:
            self.constant_definition()

            
    # <Constant deﬁnition> ::= constant_name = <Constant> ;
    def constant_definition(self):
        self.match(Tokens.ID)
        self.match(Tokens.EQUAL)
        self.constant()
        self.match(Tokens.SEMICOLON)

        
    # <Type deﬁnition part> ::= type <Type deﬁnition> {<Type deﬁnition>}
    def type_definition_part(self):
        self.match(Tokens.TYPE)
        self.type_definition()
        while self.peek() == Tokens.ID:
            self.type_definition()

            
    # <Type deﬁnition> ::= type_name = <New type> ;    
    def type_definition(self):
        self.match(Tokens.ID)
        self.match(Tokens.EQUAL)
        self.new_type()
        self.match(Tokens.SEMICOLON)

        
    # <New type> ::= <New array type> | <New record type>   
    def new_type(self):
        if self.peek() == Tokens.ARRAY:
            self.new_array_type()
        elif self.peek() == Tokens.RECORD:
            self.new_record_type()
        else:
            self.syntax_error("ARRAY or RECORD")

            
    # <New array type> ::= array ”[”<Index range> ”]”of type_name    
    def new_array_type(self):
        self.match(Tokens.ARRAY)
        self.match(Tokens.LEFTBRACKET)
        self.index_range()
        self.match(Tokens.RIGHTBRACKET)
        self.match(Tokens.OF)
        self.match(Tokens.ID)


    # <Index range> ::= <Constant> .. <Constant>       
    def index_range(self):
        self.constant()
        self.match(Tokens.DOUBLEDOT)
        self.constant()


    # <New record type> ::= record <Field list> end     
    def new_record_type(self):
        self.match(Tokens.RECORD)
        self.field_list()
        self.match(Tokens.END)

        
    # <Field list> ::= <Record section> {; <Record section>}
    def field_list(self):
        self.record_section()
        while self.peek() == Tokens.SEMICOLON:
            self.match(Tokens.SEMICOLON)
            self.record_section()

            
    # <Record section> ::= ﬁeld name {, ﬁeld name} : type name        
    def record_section(self):
        self.match(Tokens.ID)
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA)
            self.match(Tokens.ID)
        self.match(Tokens.COLON)
        self.match(Tokens.ID)

        
    # <Variable deﬁnition part> ::= var <Variable deﬁnition> {<Variable deﬁnition>}
    def variable_definition_part(self):
        self.match(Tokens.VAR)
        self.variable_definition()
        while self.peek() == Tokens.ID:
            self.variable_definition()

            
    # <Variable deﬁnition> ::= <Variable group> ;        
    def variable_definition(self):
        self.variable_group()
        self.match(Tokens.SEMICOLON)

        
    # <Variable group> ::= variable_name {, variable_name} : type_name         
    def variable_group(self):
        self.match(Tokens.ID)
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA)
            self.match(Tokens.ID)
        self.match(Tokens.COLON)
        self.match(Tokens.ID)

        
    # <Procedure deﬁnition> ::= procedure procedure_name <Procedure block> ;
    def procedure_definition(self):
        self.match(Tokens.PROCEDURE)
        self.match(Tokens.ID)
        self.procedure_block()
        self.match(Tokens.SEMICOLON)

        
    # <Procedure block> ::= [( <Formal parameter list> )] ; <Block body>         
    def procedure_block(self):
        if self.peek() == Tokens.LEFTPARENTHESIS:
            self.match(Tokens.LEFTPARENTHESIS)
            self.formal_parameter_list()
            self.match(Tokens.RIGHTPARENTHESIS)
        self.match(Tokens.SEMICOLON)
        self.block_body()
                       

    # <Formal parameter list> ::= <Parameter deﬁnition> {; <Parameter deﬁnition>}        
    def formal_parameter_list(self):
        self.parameter_definition()
        while self.peek() == Tokens.SEMICOLON:
            self.match(Tokens.SEMICOLON)
            self.parameter_definition()
                       

    # <Parameter deﬁnition> ::= [var] <Variable group>        
    def parameter_definition(self):
         if self.peek() == Tokens.VAR:
             self.match(Tokens.VAR)
         self.variable_group()
                       

    # <Statement> ::= <Assignment statement> | <Procedure statement> | <If statement> | <While statement> | <Compound statement> j
    # MODIFICADA : <Statement> ::= ID<Statement_2> | <If statement> | <While statement> | <Compound statement> | €
    def statement(self): 
        if self.peek() == Tokens.ID:
            self.match(Tokens.ID)
            self.statement_2()
        elif self.peek() == Tokens.IF:
            self.if_statement()
        elif self.peek() == Tokens.WHILE:
            self.while_statement()
        elif self.peek() == Tokens.BEGIN:
            self.compound_statement()
                       

    # NUEVA :     <Statement_2> ::= [( <Actual parameter list> )] | <Assignment statement 2>                       
    def statement_2(self):
        if self.peek() == Tokens.LEFTPARENTHESIS:
            self.match(Tokens.LEFTPARENTHESIS)
            self.actual_parameter_list()
            self.match(Tokens.RIGHTPARENTHESIS)
        elif self.peek() == Tokens.LEFTBRACKET or \
                self.peek() == Tokens.PERIOD or \
                self.peek() == Tokens.BECOMES:
            self.assignment_statement_2()
                       

    # <Assignment statement> ::= <Variable access> := <Expression>                       
    def assignment_statement(self):
        self.variable_access()
        self.match(Tokens.BECOMES)
        self.expression()
                       

    # NUEVA :     <Assignment statement 2> ::= {<Selector>} := <Expression>  
    def assignment_statement_2(self):        
        while self.peek() == Tokens.LEFTBRACKET or \
                self.peek() == Tokens.PERIOD:
            self.selector()
        self.match(Tokens.BECOMES)
        self.expression()
                       

    # BORRADA debido a la modificacion de statement
    # <Procedure statement> ::= procedure name [( <Actual parameter list> )]                        
    # def procedure_statement(self):


    # <Actual parameter list> ::= <Actual parameter> { , <Actual parameter>}
    def actual_parameter_list(self):
        self.actual_parameter()
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA)
            self.actual_parameter()
                       

    # <Actual parameter> ::= <Expression> | <Variable access>
    # MODIFICADA: <Actual parameter> ::= <Expression> 
    def actual_parameter(self):
        self.expression()
                       


    # <If statement> ::= if <Expression> then <Statement> [else <Statement>]        
    def if_statement(self):
        self.match(Tokens.IF)
        self.expression()
        self.match(Tokens.THEN)
        self.statement()
        if self.peek() == Tokens.ELSE:
            self.match(Tokens.ELSE)
            self.statement()
        

    # <While statement> ::= while <Expression> do <Statement>
    def while_statement(self):
        self.match(Tokens.WHILE)
        self.expression()
        self.match(Tokens.DO)
        self.statement()
        

    # <Compound statement> ::= begin <Statement> {; <Statement>} end
    def compound_statement(self):
        self.match(Tokens.BEGIN)
        self.statement()
        while self.peek() == Tokens.SEMICOLON:
            self.match(Tokens.SEMICOLON)
            self.statement()
        self.match(Tokens.END)
        

    # <Expression> ::= <Simple expression> [<Relational operator> <Simple expression>]
    def expression(self):
        self.simple_expression()
        if self.peek() == Tokens.LESS or \
                self.peek() == Tokens.EQUAL or \
                self.peek() == Tokens.GREATER or \
                self.peek() == Tokens.NOTGREATER or \
                self.peek() == Tokens.NOTEQUAL or \
                self.peek() == Tokens.NOTLESS:
            self.relational_operator()
            self.simple_expression()

        
    # <Relational operator> ::= < | = | > | <= | <> | >=
    def relational_operator(self):
        if self.peek() == Tokens.LESS:
            self.match(Tokens.LESS)
        elif self.peek() == Tokens.EQUAL:
            self.match(Tokens.EQUAL)
        elif self.peek() == Tokens.GREATER:
            self.match(Tokens.GREATER)
        elif self.peek() == Tokens.NOTGREATER:
            self.match(Tokens.NOTGREATER)
        elif self.peek() == Tokens.NOTEQUAL:
            self.match(Tokens.NOTEQUAL)
        elif self.peek() == Tokens.NOTLESS:
            self.match(Tokens.NOTLESS)        
        else:
            self.syntax_error("Relational Operator")
        

    # <Simple expression> ::= [<Sign operator>] <Term> {<Additive operator> <Term>}
    def simple_expression(self):
        if self.peek() == Tokens.MINUS or self.peek() == Tokens.PLUS:
            self.sign_operator()
        self.term()
        while self.peek() == Tokens.PLUS or \
                  self.peek() == Tokens.MINUS or \
                  self.peek() == Tokens.OR:
            self.additive_operator()
            self.term()
        

    # <Sign operator> ::= + | -
    def sign_operator(self):
        if self.peek() == Tokens.PLUS:
            self.match(Tokens.PLUS)
        elif self.peek() == Tokens.MINUS:
            self.match(Tokens.MINUS)
        else:
            self.syntax_error("Sign Operator")
        

    # <Additive operator> ::= + | - | or
    def additive_operator(self):
        if self.peek() == Tokens.PLUS:
            self.match(Tokens.PLUS)
        elif self.peek() == Tokens.MINUS:
            self.match(Tokens.MINUS)
        elif self.peek() == Tokens.OR:
            self.match(Tokens.OR)               
        else:
            self.syntax_error("Additive Operator") 
        

    # <Term> ::= <Factor> {<Multiplying operator> <Factor>}
    def term(self):
        self.factor()
        while self.peek() == Tokens.ASTERISK or \
                   self.peek() == Tokens.DIV or \
                   self.peek() == Tokens.MOD or \
                   self.peek() == Tokens.AND:
            self.multiplying_operator()
            self.factor()
        

    # <Multiplying operator> ::= * | div | mod | and
    def multiplying_operator(self):
        if self.peek() == Tokens.ASTERISK:
               self.match(Tokens.ASTERISK)
        elif self.peek() == Tokens.DIV:
               self.match(Tokens.DIV)            
        elif self.peek() == Tokens.MOD:
               self.match(Tokens.MOD)     
        elif self.peek() == Tokens.AND:
               self.match(Tokens.AND)
        else:
            self.syntax_error("Multiplying Operator")

               
    # <Factor> ::= <Constant> | <Variable access> | ( <Expression> ) | not <Factor>
    # MODIFICADA ::= NUMERAL | <Variable access> | ( <Expression> ) | not <Factor>
    def factor(self):
        if self.peek() == Tokens.NUMERAL :
            self.match(Tokens.NUMERAL)
        elif self.peek() == Tokens.ID:
            self.variable_access()               
        elif self.peek() == Tokens.LEFTPARENTHESIS:
            self.match(Tokens.LEFTPARENTHESIS)
            self.expression()
            self.match(Tokens.RIGHTPARENTHESIS)
        elif self.peek() == Tokens.NOT:
            self.match(Tokens.NOT)
            self.factor()
        else:
            self.syntax_error("Factor")

            
    # <Variable access> ::= variable name {<Selector>}
    def variable_access(self):
        self.match(Tokens.ID)
        while self.peek() == Tokens.LEFTBRACKET or \
                  self.peek() == Tokens.PERIOD:
            self.selector();

            
    #  <Selector> ::= <Index selector> | <Field selector>      
    def selector(self):
        if self.peek() == Tokens.LEFTBRACKET:
            self.index_selector()
        elif self.peek() == Tokens.PERIOD:
            self.field_selector()
        else:
            self.syntax_error("Selector")

            
    # <Index selector> ::= ”[”<Expression> ”]”  
    def index_selector(self):
        self.match(Tokens.LEFTBRACKET)
        self.expression()
        self.match(Tokens.RIGHTBRACKET)

            
    # <Field Selector> ::= . ﬁeld name   
    def field_selector(self):
        self.match(Tokens.PERIOD)
        self.match(Tokens.ID)

            
    # <Constant> ::= Numeral | constant name   
    def constant(self):
        if self.peek() == Tokens.NUMERAL:
            self.match(Tokens.NUMERAL)
        elif self.peek() == Tokens.ID:
            self.match(Tokens.ID)        
        


