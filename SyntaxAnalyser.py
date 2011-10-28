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
from Tokens import T

class SyntaxAnalyser:
    
    def __init__ (self, lexical_analyser):
        T.load()
        self.lexical_analyser = lexical_analyser
        self.lookahead = self.lexical_analyser.yylex()

    def peek(self):
        return self.lookahead[0]
    
    def syntax_error(self, expected):
        print (expected + " was expected, but " + T.get_name(self.lookahead[0]) + " was found in line " + str(self.lookahead[3]))
        sys.exit("The program is not valid.")

    def match(self, token):
        if self.peek() == token:
            self.lookahead = self.lexical_analyser.yylex()
            #print "Matched " + T.get_name(token)
        else:
            self.syntax_error(T.get_name(token))
            
    # <Program> ::= program program_name ; <Block body> .
    def program(self):
        self.match(T.PROGRAM)
        self.match(T.ID)
        self.match(T.SEMICOLON)
        self.block_body()
        self.match(T.PERIOD)
        

    # <Block body> ::= [<Constant deﬁnition part>] [<Type deﬁnition part>][<Variable deﬁnition part>] {<Procedure deﬁnition>}<Compound statement>    
    def block_body(self):
        if self.peek() == T.CONST:
            self.constant_definition_part()
        if self.peek() == T.TYPE:
            self.type_definition_part()
        if self.peek() == T.VAR:
            self.variable_definition_part()
        while self.peek() == T.PROCEDURE:
            self.procedure_definition()
        self.compound_statement()
        

    # <Constant deﬁnition part> ::= const <Constant deﬁnition> {<Constant deﬁnition>}
    def constant_definition_part(self):
        self.match(T.CONST)
        self.constant_definition()
        while self.peek() == T.ID:
            self.constant_definition()

            
    # <Constant deﬁnition> ::= constant_name = <Constant> ;
    def constant_definition(self):
        self.match(T.ID)
        self.match(T.EQUAL)
        self.constant()
        self.match(T.SEMICOLON)

        
    # <Type deﬁnition part> ::= type <Type deﬁnition> {<Type deﬁnition>}
    def type_definition_part(self):
        self.match(T.TYPE)
        self.type_definition()
        while self.peek() == T.ID:
            self.type_definition()

            
    # <Type deﬁnition> ::= type_name = <New type> ;    
    def type_definition(self):
        self.match(T.ID)
        self.match(T.EQUAL)
        self.new_type()
        self.match(T.SEMICOLON)

        
    # <New type> ::= <New array type> | <New record type>   
    def new_type(self):
        if self.peek() == T.ARRAY:
            self.new_array_type()
        elif self.peek() == T.RECORD:
            self.new_record_type()
        else:
            self.syntax_error("ARRAY or RECORD")

            
    # <New array type> ::= array ”[”<Index range> ”]”of type_name    
    def new_array_type(self):
        self.match(T.ARRAY)
        self.match(T.LEFTBRACKET)
        self.index_range()
        self.match(T.RIGHTBRACKET)
        self.match(T.OF)
        self.match(T.ID)


    # <Index range> ::= <Constant> .. <Constant>       
    def index_range(self):
        self.constant()
        self.match(T.DOUBLEDOT)
        self.constant()


    # <New record type> ::= record <Field list> end     
    def new_record_type(self):
        self.match(T.RECORD)
        self.field_list()
        self.match(T.END)

        
    # <Field list> ::= <Record section> {; <Record section>}
    def field_list(self):
        self.record_section()
        while self.peek() == T.SEMICOLON:
            self.match(T.SEMICOLON)
            self.record_section()

            
    # <Record section> ::= ﬁeld name {, ﬁeld name} : type name        
    def record_section(self):
        self.match(T.ID)
        while self.peek() == T.COMMA:
            self.match(T.COMMA)
            self.match(T.ID)
        self.match(T.COLON)
        self.match(T.ID)

        
    # <Variable deﬁnition part> ::= var <Variable deﬁnition> {<Variable deﬁnition>}
    def variable_definition_part(self):
        self.match(T.VAR)
        self.variable_definition()
        while self.peek() == T.ID:
            self.variable_definition()

            
    # <Variable deﬁnition> ::= <Variable group> ;        
    def variable_definition(self):
        self.variable_group()
        self.match(T.SEMICOLON)

        
    # <Variable group> ::= variable_name {, variable_name} : type_name         
    def variable_group(self):
        self.match(T.ID)
        while self.peek() == T.COMMA:
            self.match(T.COMMA)
            self.match(T.ID)
        self.match(T.COLON)
        self.match(T.ID)

        
    # <Procedure deﬁnition> ::= procedure procedure_name <Procedure block> ;
    def procedure_definition(self):
        self.match(T.PROCEDURE)
        self.match(T.ID)
        self.procedure_block()
        self.match(T.SEMICOLON)

        
    # <Procedure block> ::= [( <Formal parameter list> )] ; <Block body>         
    def procedure_block(self):
        if self.peek() == T.LEFTPARENTHESIS:
            self.match(T.LEFTPARENTHESIS)
            self.formal_parameter_list()
            self.match(T.RIGHTPARENTHESIS)
        self.match(T.SEMICOLON)
        self.block_body()
                       

    # <Formal parameter list> ::= <Parameter deﬁnition> {; <Parameter deﬁnition>}        
    def formal_parameter_list(self):
        self.parameter_definition()
        while self.peek() == T.SEMICOLON:
            self.match(T.SEMICOLON)
            self.parameter_definition()
                       

    # <Parameter deﬁnition> ::= [var] <Variable group>        
    def parameter_definition(self):
         if self.peek() == T.VAR:
             self.match(T.VAR)
         self.variable_group()
                       

    # <Statement> ::= <Assignment statement> | <Procedure statement> | <If statement> | <While statement> | <Compound statement> j
    # MODIFICADA : <Statement> ::= ID<Statement_2> | <If statement> | <While statement> | <Compound statement> | €
    def statement(self): 
        if self.peek() == T.ID:
            self.match(T.ID)
            self.statement_2()
        elif self.peek() == T.IF:
            self.if_statement()
        elif self.peek() == T.WHILE:
            self.while_statement()
        elif self.peek() == T.BEGIN:
            self.compound_statement()
                       

    # NUEVA :     <Statement_2> ::= [( <Actual parameter list> )] | <Assignment statement 2>                       
    def statement_2(self):
        if self.peek() == T.LEFTPARENTHESIS:
            self.match(T.LEFTPARENTHESIS)
            self.actual_parameter_list()
            self.match(T.RIGHTPARENTHESIS)
        elif self.peek() == T.LEFTBRACKET or \
                self.peek() == T.PERIOD or \
                self.peek() == T.BECOMES:
            self.assignment_statement_2()
                       

    # <Assignment statement> ::= <Variable access> := <Expression>                       
    def assignment_statement(self):
        self.variable_access()
        self.match(T.BECOMES)
        self.expression()
                       

    # NUEVA :     <Assignment statement 2> ::= {<Selector>} := <Expression>  
    def assignment_statement_2(self):        
        while self.peek() == T.LEFTBRACKET or \
                self.peek() == T.PERIOD:
            self.selector()
        self.match(T.BECOMES)
        self.expression()
                       

    # BORRADA debido a la modificacion de statement
    # <Procedure statement> ::= procedure name [( <Actual parameter list> )]                        
    # def procedure_statement(self):


    # <Actual parameter list> ::= <Actual parameter> { , <Actual parameter>}
    def actual_parameter_list(self):
        self.actual_parameter()
        while self.peek() == T.COMMA:
            self.match(T.COMMA)
            self.actual_parameter()
                       

    # <Actual parameter> ::= <Expression> | <Variable access>
    # MODIFICADA: <Actual parameter> ::= <Expression> 
    def actual_parameter(self):
        self.expression()
                       


    # <If statement> ::= if <Expression> then <Statement> [else <Statement>]        
    def if_statement(self):
        self.match(T.IF)
        self.expression()
        self.match(T.THEN)
        self.statement()
        if self.peek() == T.ELSE:
            self.match(T.ELSE)
            self.statement()
        

    # <While statement> ::= while <Expression> do <Statement>
    def while_statement(self):
        self.match(T.WHILE)
        self.expression()
        self.match(T.DO)
        self.statement()
        

    # <Compound statement> ::= begin <Statement> {; <Statement>} end
    def compound_statement(self):
        self.match(T.BEGIN)
        self.statement()
        while self.peek() == T.SEMICOLON:
            self.match(T.SEMICOLON)
            self.statement()
        self.match(T.END)
        

    # <Expression> ::= <Simple expression> [<Relational operator> <Simple expression>]
    def expression(self):
        self.simple_expression()
        if self.peek() == T.LESS or \
                self.peek() == T.EQUAL or \
                self.peek() == T.GREATER or \
                self.peek() == T.NOTGREATER or \
                self.peek() == T.NOTEQUAL or \
                self.peek() == T.NOTLESS:
            self.relational_operator()
            self.simple_expression()

        
    # <Relational operator> ::= < | = | > | <= | <> | >=
    def relational_operator(self):
        if self.peek() == T.LESS:
            self.match(T.LESS)
        elif self.peek() == T.EQUAL:
            self.match(T.EQUAL)
        elif self.peek() == T.GREATER:
            self.match(T.GREATER)
        elif self.peek() == T.NOTGREATER:
            self.match(T.NOTGREATER)
        elif self.peek() == T.NOTEQUAL:
            self.match(T.NOTEQUAL)
        elif self.peek() == T.NOTLESS:
            self.match(T.NOTLESS)        
        else:
            self.syntax_error("Relational Operator")
        

    # <Simple expression> ::= [<Sign operator>] <Term> {<Additive operator> <Term>}
    def simple_expression(self):
        if self.peek() == T.MINUS or self.peek() == T.PLUS:
            self.sign_operator()
        self.term()
        while self.peek() == T.PLUS or \
                  self.peek() == T.MINUS or \
                  self.peek() == T.OR:
            self.additive_operator()
            self.term()
        

    # <Sign operator> ::= + | -
    def sign_operator(self):
        if self.peek() == T.PLUS:
            self.match(T.PLUS)
        elif self.peek() == T.MINUS:
            self.match(T.MINUS)
        else:
            self.syntax_error("Sign Operator")
        

    # <Additive operator> ::= + | - | or
    def additive_operator(self):
        if self.peek() == T.PLUS:
            self.match(T.PLUS)
        elif self.peek() == T.MINUS:
            self.match(T.MINUS)
        elif self.peek() == T.OR:
            self.match(T.OR)               
        else:
            self.syntax_error("Additive Operator") 
        

    # <Term> ::= <Factor> {<Multiplying operator> <Factor>}
    def term(self):
        self.factor()
        while self.peek() == T.ASTERISK or \
                   self.peek() == T.DIV or \
                   self.peek() == T.MOD or \
                   self.peek() == T.AND:
            self.multiplying_operator()
            self.factor()
        

    # <Multiplying operator> ::= * | div | mod | and
    def multiplying_operator(self):
        if self.peek() == T.ASTERISK:
               self.match(T.ASTERISK)
        elif self.peek() == T.DIV:
               self.match(T.DIV)            
        elif self.peek() == T.MOD:
               self.match(T.MOD)     
        elif self.peek() == T.AND:
               self.match(T.AND)
        else:
            self.syntax_error("Multiplying Operator")

               
    # <Factor> ::= <Constant> | <Variable access> | ( <Expression> ) | not <Factor>
    # MODIFICADA ::= NUMERAL | <Variable access> | ( <Expression> ) | not <Factor>
    def factor(self):
        if self.peek() == T.NUMERAL :
            self.match(T.NUMERAL)
        elif self.peek() == T.ID:
            self.variable_access()               
        elif self.peek() == T.LEFTPARENTHESIS:
            self.match(T.LEFTPARENTHESIS)
            self.expression()
            self.match(T.RIGHTPARENTHESIS)
        elif self.peek() == T.NOT:
            self.match(T.NOT)
            self.factor()
        else:
            self.syntax_error("Factor")

            
    # <Variable access> ::= variable name {<Selector>}
    def variable_access(self):
        self.match(T.ID)
        while self.peek() == T.LEFTBRACKET or \
                  self.peek() == T.PERIOD:
            self.selector();

            
    #  <Selector> ::= <Index selector> | <Field selector>      
    def selector(self):
        if self.peek() == T.LEFTBRACKET:
            self.index_selector()
        elif self.peek() == T.PERIOD:
            self.field_selector()
        else:
            self.syntax_error("Selector")

            
    # <Index selector> ::= ”[”<Expression> ”]”  
    def index_selector(self):
        self.match(T.LEFTBRACKET)
        self.expression()
        self.match(T.RIGHTBRACKET)

            
    # <Field Selector> ::= . ﬁeld name   
    def field_selector(self):
        self.match(T.PERIOD)
        self.match(T.ID)

            
    # <Constant> ::= Numeral | constant name   
    def constant(self):
        if self.peek() == T.NUMERAL:
            self.match(T.NUMERAL)
        elif self.peek() == T.ID:
            self.match(T.ID) 
	else:
	    self.syntax_error("Numeral or ID")       
        


