# -*- coding: utf-8 -*-
""" **************************************************************************
FICHERO:        p4sintactico.py
FECHA:          02.10.2011
AUTORES:        Marcelino Aitor Concepcion Barandela
                Andres Gonzalez Placeres
                Joram Real Gómez
E-MAILS:        alu0100220919@alumnado.ull.es
                alu0100247671@alumnado.ull.es
                alu0100226300@alumnado.ull.es
ASIGNATURA:     Compiladores
DESCRIPCION:    Practica 3
                Diseño e implementacion de un analizador sintactico para PASCAL-
COMENTARIOS:    
*************************************************************************** """

import argparse

from SyntaxAnalyser import SyntaxAnalyser
from LexicalAnalyser import LexicalAnalyser
from SymbolTable import SymbolTable


parser = argparse.ArgumentParser(description='Pascal- Syntax analyzer')
parser.add_argument('in_file', metavar='File_Name', type=argparse.FileType('rb'),
                    help='File to be analyzed')
"""
parser.add_argument('-d', dest='show_dict', action='store_true',
                    help='Show the symbol table at the end of the analysis')
parser.add_argument('-t', dest='show_tokens', action='store_true',
                    help='Show tokens while analyzing the code')
"""

args = parser.parse_args()


T = SymbolTable()
L = LexicalAnalyser(args.in_file, T)
S = SyntaxAnalyser(L)
S.program()

print("The program is valid.")


      

