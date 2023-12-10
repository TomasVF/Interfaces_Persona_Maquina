#!/usr/bin/env python3

from sys import argv
import string
from typing import Optional
import cheathelper
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import ast
import textwrap	
import locale
import gettext
from pathlib import Path

_ = gettext.gettext
N_ = gettext.ngettext

class State:
    #entrada de busqueda
    entrada: str= ""
    #resultado de la busqueda
    command: str= ""
    
    #actualiza el resultado de la busqueda segun la entrada dada
    def change_command(self, entrada) -> None:
         recipes = cheathelper.get_cheatsheet(entrada)
         resultado=""   
         for i, r in enumerate(recipes, start= 1):
            idx = f"{i}."
            resultado = resultado + (
                textwrap.indent(
                    f"{idx} {r}",
                    prefix= "    ",
                    predicate= lambda line: not line.startswith(idx)
                )
            )
            resultado = resultado + "\n"
         if resultado.startswith("1. () error de red"):
            resultado = _("\nThere are connection problems")
         elif resultado.startswith("1. ()"):
            resultado = "\n" + entrada + _(" is an unknown command")
         self.command = resultado
         self.entrada = entrada

    def get_command(self) -> str:
        return self.command
    def get_entrada(self) -> str:
        return self.entrada
   

