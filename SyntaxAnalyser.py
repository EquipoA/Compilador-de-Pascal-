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


def printset(S):
    a = ""
    for i in S:
        a += Tokens.get_name(i) + " "
    print(a)

class SyntaxAnalyser:
    
    def __init__ (self, lexical_analyser):
        Tokens.load()
        self.lexical_analyser = lexical_analyser
        self.lookahead = self.lexical_analyser.yylex()
        self.ErrorLinea = 0;
        self.ErrorCount = 0;

    def peek(self):
        return self.lookahead[0]

    def syntax_error(self, Stop):
        #print("Conjunto de parada")
        #printset(Stop)
        if self.ErrorLinea != self.lexical_analyser.get_current_line():
            self.ErrorCount += 1
            self.ErrorLinea = self.lexical_analyser.get_current_line()
            print ("Error en la linea " + str(self.lexical_analyser.get_current_line()) + ". No se esperaba el token " + Tokens.get_name(self.peek()))
        while (self.peek() not in Stop):
            #print("Descartando: " + Tokens.get_name(self.peek()))
            self.lookahead = self.lexical_analyser.yylex()
        #print("Recuperado con: " + Tokens.get_name(self.peek()))
                

    def match(self, token, Stop):
        if self.peek() == token:
            self.lookahead = self.lexical_analyser.yylex()
            self.syntax_check(Stop)
            #print "Matched " + Tokens.get_name(token)
        else:
            self.syntax_error(Stop)

    def syntax_check(self, Stop):
        if ((self.peek() not in Stop) and  (len(Stop) <> 1)):
            self.syntax_error(Stop)
            
    # <Program> ::= program program_name ; <Block body> .
    def program(self, Stop):
        self.match(Tokens.PROGRAM, Stop | set([Tokens.ID, Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN, Tokens.PERIOD]))
        self.match(Tokens.ID, Stop|set([Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN, Tokens.PERIOD]))
        self.match(Tokens.SEMICOLON, Stop|set([Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN, Tokens.PERIOD]))
        self.block_body(Stop|set([Tokens.PERIOD]))
        self.match(Tokens.PERIOD, Stop)
        

    # <Block body> ::= [<Constant deﬁnition part>] [<Type deﬁnition part>][<Variable deﬁnition part>] {<Procedure deﬁnition>}<Compound statement>    
    def block_body(self, Stop):
        self.syntax_check(Stop|set([Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        if self.peek() == Tokens.CONST:
            self.constant_definition_part(Stop|set([Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
            
        self.syntax_check(Stop|set([Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        if self.peek() == Tokens.TYPE:
            self.type_definition_part(Stop|set([Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
            
        self.syntax_check(Stop|set([Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        if self.peek() == Tokens.VAR:
            self.variable_definition_part(Stop|set([Tokens.PROCEDURE, Tokens.BEGIN]))
            
        self.syntax_check(Stop|set([Tokens.PROCEDURE, Tokens.BEGIN]))
        while self.peek() == Tokens.PROCEDURE:
            self.procedure_definition(Stop|set([Tokens.PROCEDURE, Tokens.BEGIN]))
            
        self.compound_statement(Stop)
        

    # <Constant deﬁnition part> ::= const <Constant deﬁnition> {<Constant deﬁnition>}
    def constant_definition_part(self,Stop):
        self.match(Tokens.CONST, Stop|set([Tokens.ID]))
        self.constant_definition(Stop|set([Tokens.ID]))
        
        self.syntax_check(Stop | set([Tokens.ID]))
        while self.peek() == Tokens.ID:
            self.constant_definition(Stop|set([Tokens.ID]))

            
    # <Constant deﬁnition> ::= constant_name = <Constant> ;
    def constant_definition(self, Stop):
        self.match(Tokens.ID, Stop|set([Tokens.EQUAL, Tokens.ID, Tokens.NUMERAL, Tokens.SEMICOLON]))
        self.match(Tokens.EQUAL, Stop|set([Tokens.ID, Tokens.NUMERAL, Tokens.SEMICOLON]))
        self.constant(Stop|set([Tokens.SEMICOLON]))
        self.match(Tokens.SEMICOLON, Stop)

        
    # <Type deﬁnition part> ::= type <Type deﬁnition> {<Type deﬁnition>}
    def type_definition_part(self, Stop):
        self.match(Tokens.TYPE, Stop|set([Tokens.ID]))
        self.type_definition(Stop|set([Tokens.ID]))
        
        self.syntax_check(Stop | set([Tokens.ID]))
        while self.peek() == Tokens.ID:
            self.type_definition(Stop|set([Tokens.ID]))

            
    # <Type deﬁnition> ::= type_name = <New type> ;    
    def type_definition(self, Stop):
        self.match(Tokens.ID, Stop|set([Tokens.EQUAL, Tokens.ARRAY, Tokens.RECORD, Tokens.SEMICOLON]))
        self.match(Tokens.EQUAL, Stop|set([Tokens.ARRAY, Tokens.RECORD, Tokens.SEMICOLON]))
        self.new_type(Stop|set([Tokens.SEMICOLON]))
        self.match(Tokens.SEMICOLON, Stop)

        
    # <New type> ::= <New array type> | <New record type>   
    def new_type(self, Stop):
        if self.peek() == Tokens.ARRAY:
            self.new_array_type(Stop)
        elif self.peek() == Tokens.RECORD:
            self.new_record_type(Stop)
        else:
            self.syntax_error(Stop)

            
    # <New array type> ::= array ”[”<Index range> ”]”of type_name    
    def new_array_type(self, Stop):
        self.match(Tokens.ARRAY, Stop|set([Tokens.LEFTBRACKET, Tokens.NUMERAL, Tokens.ID, Tokens.RIGHTBRACKET, Tokens.OF]))
        self.match(Tokens.LEFTBRACKET, Stop|set([Tokens.NUMERAL, Tokens.ID, Tokens.RIGHTBRACKET, Tokens.OF]))
        self.index_range(Stop|set([Tokens.RIGHTBRACKET, Tokens.OF, Tokens.ID]))
        self.match(Tokens.RIGHTBRACKET, Stop|set([Tokens.OF, Tokens.ID]))
        self.match(Tokens.OF, Stop|set([Tokens.ID]))
        self.match(Tokens.ID, Stop)


    # <Index range> ::= <Constant> .. <Constant>       
    def index_range(self, Stop):
        self.constant(Stop|set([Tokens.DOUBLEDOT, Tokens.NUMERAL, Tokens.ID]))
        self.match(Tokens.DOUBLEDOT, Stop|set([Tokens.NUMERAL, Tokens.ID]))
        self.constant(Stop)


    # <New record type> ::= record <Field list> end     
    def new_record_type(self, Stop):
        self.match(Tokens.RECORD, Stop|set([Tokens.ID, Tokens.END]))
        self.field_list(Stop|set([Tokens.END]))
        self.match(Tokens.END, Stop)

        
    # <Field list> ::= <Record section> {; <Record section>}
    def field_list(self, Stop):
        self.record_section(Stop|set([Tokens.SEMICOLON]))
        
        #self.syntax_check(Stop | set([Tokens.SEMICOLON]))
        while self.peek() == Tokens.SEMICOLON:
            self.match(Tokens.SEMICOLON, Stop|set([Tokens.ID, Tokens.SEMICOLON]))
            self.record_section(Stop|set([Tokens.SEMICOLON]))

            
    # <Record section> ::= ﬁeld name {, ﬁeld name} : type name        
    def record_section(self, Stop):
        self.match(Tokens.ID, Stop|set([Tokens.COMMA, Tokens.ID, Tokens.COLON]))
        
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA, Stop|set([Tokens.ID, Tokens.COMMA, Tokens.COLON]))
            self.match(Tokens.ID, Stop|set([Tokens.COMMA, Tokens.ID, Tokens.COLON]))
            
        self.match(Tokens.COLON, Stop|set([Tokens.ID]))
        self.match(Tokens.ID, Stop)

        
    # <Variable deﬁnition part> ::= var <Variable deﬁnition> {<Variable deﬁnition>}
    def variable_definition_part(self, Stop):
        self.match(Tokens.VAR, Stop | set([Tokens.ID]))
        self.variable_definition(Stop | set([Tokens.ID]))
        
        self.syntax_check(Stop | set([Tokens.ID]))
        
        while self.peek() == Tokens.ID:
            self.variable_definition(Stop|set([Tokens.ID]))

            
    # <Variable deﬁnition> ::= <Variable group> ;        
    def variable_definition(self, Stop):
        self.variable_group(Stop|set([Tokens.SEMICOLON]))
        self.match(Tokens.SEMICOLON, Stop)

        
    # <Variable group> ::= variable_name {, variable_name} : type_name         
    def variable_group(self, Stop):
        self.match(Tokens.ID, Stop|set([Tokens.COMMA, Tokens.ID, Tokens.COLON]))
        
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA, Stop|set([Tokens.ID, Tokens.COMMA, Tokens.COLON]))
            self.match(Tokens.ID, Stop|set([Tokens.COMMA, Tokens.ID, Tokens.COLON]))
            
        self.match(Tokens.COLON, Stop|set([Tokens.ID]))
        self.match(Tokens.ID, Stop)

        
    # <Procedure deﬁnition> ::= procedure procedure_name <Procedure block> ;
    def procedure_definition(self, Stop):
        self.match(Tokens.PROCEDURE, Stop|set([Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        self.match(Tokens.ID, Stop|set([Tokens.LEFTPARENTHESIS, Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        self.procedure_block(Stop|set([Tokens.SEMICOLON]))
        self.match(Tokens.SEMICOLON, Stop)

        
    # <Procedure block> ::= [( <Formal parameter list> )] ; <Block body>         
    def procedure_block(self, Stop):
        self.syntax_check(Stop | set([Tokens.LEFTPARENTHESIS]))
        if self.peek() == Tokens.LEFTPARENTHESIS:
            self.match(Tokens.LEFTPARENTHESIS, Stop|set([Tokens.VAR, Tokens.ID, Tokens.RIGHTPARENTHESIS, Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.PROCEDURE, Tokens.BEGIN]))
            self.formal_parameter_list(Stop|set([Tokens.RIGHTPARENTHESIS, Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
            self.match(Tokens.RIGHTPARENTHESIS, Stop|set([Tokens.SEMICOLON, Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        self.match(Tokens.SEMICOLON, Stop|set([Tokens.CONST, Tokens.TYPE, Tokens.VAR, Tokens.PROCEDURE, Tokens.BEGIN]))
        self.block_body(Stop)
                       

    # <Formal parameter list> ::= <Parameter deﬁnition> {; <Parameter deﬁnition>}        
    def formal_parameter_list(self, Stop):
        self.parameter_definition(Stop|set([Tokens.SEMICOLON]))
        
        while self.peek() == Tokens.SEMICOLON:
            self.match(Tokens.SEMICOLON, Stop|set([Tokens.VAR, Tokens.ID, Tokens.SEMICOLON]))
            self.parameter_definition(Stop|set([Tokens.SEMICOLON, Tokens.VAR, Tokens.ID]))
                       

    # <Parameter deﬁnition> ::= [var] <Variable group>        
    def parameter_definition(self, Stop):
         if self.peek() == Tokens.VAR:
             self.match(Tokens.VAR, Stop|set([Tokens.ID]))
         self.variable_group(Stop)
                       

    # <Statement> ::= <Assignment statement> | <Procedure statement> | <If statement> | <While statement> | <Compound statement> j
    # MODIFICADA : <Statement> ::= ID<Statement_2> | <If statement> | <While statement> | <Compound statement> | €
    def statement(self, Stop): 
        #print("Entrando en Statement");
        if self.peek() == Tokens.ID:
            self.match(Tokens.ID, Stop|set([Tokens.LEFTBRACKET, Tokens.LEFTPARENTHESIS, Tokens.PERIOD, Tokens.BECOMES]))
            self.statement_2(Stop)
        elif self.peek() == Tokens.IF:
            self.if_statement(Stop)
        elif self.peek() == Tokens.WHILE:
            self.while_statement(Stop)
        elif self.peek() == Tokens.BEGIN:
            self.compound_statement(Stop)
        #else:
        self.syntax_check(Stop)
        #print("Saliendo de Statement")
                       

    # NUEVA :     <Statement_2> ::= [( <Actual parameter list> )] | <Assignment statement>                       
    def statement_2(self, Stop):
        #print("Entrando en Statement 2");
        if self.peek() == Tokens.LEFTPARENTHESIS:
            #print("OMG, un LEFTPARENTHESIS")
            self.match(Tokens.LEFTPARENTHESIS, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.RIGHTPARENTHESIS]))
            self.actual_parameter_list(Stop|set([Tokens.RIGHTPARENTHESIS]))
            self.match(Tokens.RIGHTPARENTHESIS, Stop)
        elif self.peek() == Tokens.LEFTBRACKET or \
                self.peek() == Tokens.PERIOD or \
                self.peek() == Tokens.BECOMES:
            #print("LEFTBRACKET o PERIOD o BECOMES")
            self.assignment_statement(Stop)
        else:
            self.syntax_check(Stop)
        #print("Saliendo de Statement 2")
                       

    # NUEVA :     <Assignment statement> ::= {<Selector>} := <Expression> 
    def assignment_statement(self, Stop):        
        while self.peek() == Tokens.LEFTBRACKET or self.peek() == Tokens.PERIOD:
            self.selector(Stop|set([Tokens.LEFTBRACKET, Tokens.PERIOD, Tokens.BECOMES, Tokens.PLUS, Tokens.MINUS, Tokens.ID, Tokens.NUMERAL, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        self.match(Tokens.BECOMES, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        self.expression(Stop)
                       

    # BORRADA debido a la modificacion de statement
    # <Procedure statement> ::= procedure name [( <Actual parameter list> )]                        
    # def procedure_statement(self):


    # <Actual parameter list> ::= <Actual parameter> { , <Actual parameter>}
    def actual_parameter_list(self, Stop):
        self.actual_parameter(Stop|set([Tokens.COMMA, Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        
        while self.peek() == Tokens.COMMA:
            self.match(Tokens.COMMA, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.COMMA]))
            self.actual_parameter(Stop|set([Tokens.COMMA, Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
                       

    # <Actual parameter> ::= <Expression> | <Variable access>
    # MODIFICADA: <Actual parameter> ::= <Expression> 
    def actual_parameter(self, Stop):
        self.expression(Stop)
                       


    # <If statement> ::= if <Expression> then <Statement> [else <Statement>]        
    def if_statement(self, Stop):
        self.match(Tokens.IF, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.THEN, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.ELSE]))
        self.expression(Stop|set([Tokens.THEN, Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.ELSE]))
        self.match(Tokens.THEN, Stop|set([Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.ELSE]))
        self.statement(Stop|set([Tokens.ELSE, Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN]))
        if self.peek() == Tokens.ELSE:
            self.match(Tokens.ELSE, Stop|set([Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN]))
            self.statement(Stop)
        

    # <While statement> ::= while <Expression> do <Statement>
    def while_statement(self, Stop):
        self.match(Tokens.WHILE, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.DO, Tokens.IF, Tokens.WHILE, Tokens.BEGIN]))
        self.expression(Stop|set([Tokens.DO, Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN]))
        self.match(Tokens.DO, Stop|set([Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN]))
        self.statement(Stop)
        

    # <Compound statement> ::= begin <Statement> {; <Statement>} end
    def compound_statement(self, Stop):
        self.match(Tokens.BEGIN, Stop|set([Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.SEMICOLON, Tokens.END]))
        
        #self.statement(Stop|set([Tokens.SEMICOLON, Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.END]))
        self.statement(Stop|set([Tokens.SEMICOLON, Tokens.END]))
        
        while self.peek() == Tokens.SEMICOLON:
        #while self.peek() in Stop:
            self.match(Tokens.SEMICOLON, Stop|set([Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.SEMICOLON, Tokens.END]))
            
            #self.statement(Stop|set([Tokens.SEMICOLON, Tokens.ID, Tokens.IF, Tokens.WHILE, Tokens.BEGIN, Tokens.END]))
            self.statement(Stop|set([Tokens.SEMICOLON, Tokens.END]))
            
            #print("Al final del while lookahead es " + Tokens.get_name(self.peek()))
            #printset(Stop)

        self.match(Tokens.END, Stop)
        #print("Se acaba el compound_statement tio")
        

    # <Expression> ::= <Simple expression> [<Relational operator> <Simple expression>]
    def expression(self, Stop):
        self.simple_expression(Stop|set([Tokens.LESS, Tokens.EQUAL, Tokens.GREATER, Tokens.NOTGREATER, Tokens.NOTEQUAL, Tokens.NOTLESS, Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        if self.peek() == Tokens.LESS or \
                self.peek() == Tokens.EQUAL or \
                self.peek() == Tokens.GREATER or \
                self.peek() == Tokens.NOTGREATER or \
                self.peek() == Tokens.NOTEQUAL or \
                self.peek() == Tokens.NOTLESS:
            self.relational_operator(Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
            self.simple_expression(Stop)

        
    # <Relational operator> ::= < | = | > | <= | <> | >=
    def relational_operator(self, Stop):
        if self.peek() == Tokens.LESS:
            self.match(Tokens.LESS, Stop)
        elif self.peek() == Tokens.EQUAL:
            self.match(Tokens.EQUAL, Stop)
        elif self.peek() == Tokens.GREATER:
            self.match(Tokens.GREATER, Stop)
        elif self.peek() == Tokens.NOTGREATER:
            self.match(Tokens.NOTGREATER, Stop)
        elif self.peek() == Tokens.NOTEQUAL:
            self.match(Tokens.NOTEQUAL, Stop)
        elif self.peek() == Tokens.NOTLESS:
            self.match(Tokens.NOTLESS, Stop)        
        else:
            self.syntax_error(Stop)
        

    # <Simple expression> ::= [<Sign operator>] <Term> {<Additive operator> <Term>}
    def simple_expression(self, Stop):
        if self.peek() == Tokens.MINUS or self.peek() == Tokens.PLUS:
            self.sign_operator(Stop|set([Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.PLUS, Tokens.MINUS, Tokens.OR]))
        self.term(Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.OR, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        while self.peek() == Tokens.PLUS or \
                  self.peek() == Tokens.MINUS or \
                  self.peek() == Tokens.OR:
            self.additive_operator(Stop|set([Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.PLUS, Tokens.MINUS, Tokens.OR]))
            self.term(Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.OR, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        

    # <Sign operator> ::= + | -
    def sign_operator(self, Stop):
        if self.peek() == Tokens.PLUS:
            self.match(Tokens.PLUS, Stop)
        elif self.peek() == Tokens.MINUS:
            self.match(Tokens.MINUS, Stop)
        else:
            self.syntax_error(Stop)
        

    # <Additive operator> ::= + | - | or
    def additive_operator(self, Stop):
        if self.peek() == Tokens.PLUS:
            self.match(Tokens.PLUS, Stop)
        elif self.peek() == Tokens.MINUS:
            self.match(Tokens.MINUS, Stop)
        elif self.peek() == Tokens.OR:
            self.match(Tokens.OR, Stop)               
        else:
            self.syntax_error(Stop)

    # <Term> ::= <Factor> {<Multiplying operator> <Factor>}
    def term(self, Stop):
        self.factor(Stop|set([Tokens.ASTERISK, Tokens.DIV, Tokens.MOD, Tokens.AND, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        while self.peek() == Tokens.ASTERISK or \
                   self.peek() == Tokens.DIV or \
                   self.peek() == Tokens.MOD or \
                   self.peek() == Tokens.AND:
            self.multiplying_operator(Stop|set([Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT, Tokens.ASTERISK, Tokens.MOD, Tokens.DIV, Tokens.MOD, Tokens.AND]))
            self.factor(Stop|set([Tokens.ASTERISK, Tokens.DIV, Tokens.MOD, Tokens.AND, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        

    # <Multiplying operator> ::= * | div | mod | and
    def multiplying_operator(self, Stop):
        if self.peek() == Tokens.ASTERISK:
               self.match(Tokens.ASTERISK, Stop)
        elif self.peek() == Tokens.DIV:
               self.match(Tokens.DIV, Stop)            
        elif self.peek() == Tokens.MOD:
               self.match(Tokens.MOD, Stop)     
        elif self.peek() == Tokens.AND:
               self.match(Tokens.AND, Stop)
        else:
            self.syntax_error(Stop)
               
    # <Factor> ::= <Constant> | <Variable access> | ( <Expression> ) | not <Factor>
    # MODIFICADA ::= NUMERAL | <Variable access> | ( <Expression> ) | not <Factor>
    def factor(self, Stop):
        if self.peek() == Tokens.NUMERAL :
            self.match(Tokens.NUMERAL, Stop)
        elif self.peek() == Tokens.ID:
            self.variable_access(Stop)               
        elif self.peek() == Tokens.LEFTPARENTHESIS:
            self.match(Tokens.LEFTPARENTHESIS, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
            self.expression(Stop|set([Tokens.RIGHTPARENTHESIS]))
            self.match(Tokens.RIGHTPARENTHESIS, Stop)
        elif self.peek() == Tokens.NOT:
            self.match(Tokens.NOT, Stop|set([Tokens.NUMERAL, Tokens.ID]))
            self.factor(Stop)
        else:
            self.syntax_error(Stop)
            
    # <Variable access> ::= variable name {<Selector>}              NI IDEA
    def variable_access(self, Stop):
        self.match(Tokens.ID, Stop|set([Tokens.LEFTBRACKET, Tokens.PERIOD]))
        while self.peek() == Tokens.LEFTBRACKET or \
                  self.peek() == Tokens.PERIOD:
            self.selector(Stop|set([Tokens.LEFTBRACKET, Tokens.PERIOD]));

            
    #  <Selector> ::= <Index selector> | <Field selector>      
    def selector(self, Stop):
        if self.peek() == Tokens.LEFTBRACKET:
            self.index_selector(Stop)
        elif self.peek() == Tokens.PERIOD:
            self.field_selector(Stop)
        else:
            self.syntax_error(Stop)
            
    # <Index selector> ::= ”[”<Expression> ”]”  
    def index_selector(self, Stop):
        self.match(Tokens.LEFTBRACKET, Stop|set([Tokens.PLUS, Tokens.MINUS, Tokens.NUMERAL, Tokens.ID, Tokens.LEFTPARENTHESIS, Tokens.NOT]))
        self.expression(Stop|set([Tokens.RIGHTBRACKET]))
        self.match(Tokens.RIGHTBRACKET, Stop)

            
    # <Field Selector> ::= . ﬁeld name   
    def field_selector(self, Stop):
        self.match(Tokens.PERIOD, Stop|set([Tokens.ID]))
        self.match(Tokens.ID, Stop)

            
    # <Constant> ::= Numeral | constant name   
    def constant(self, Stop):
        if self.peek() == Tokens.NUMERAL:
            self.match(Tokens.NUMERAL, Stop)
        elif self.peek() == Tokens.ID:
            self.match(Tokens.ID, Stop)
        else:
            self.syntax_error(Stop)
