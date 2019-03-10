#!/usr/bin/env python3

from colorama import Fore, Style
from src.Beautifier import Colorer, Styler, TextEditor, Beautifier

def color_test():
    colorer = Colorer()
    input_string = "Hello World"
    assert colorer.add_red_color(input_string) == Fore.RED + input_string + Fore.RESET, "Red color failed"
    assert colorer.add_green_color(input_string) == Fore.GREEN + input_string + Fore.RESET, "Green color failed"
    assert colorer.add_orange_color(input_string) == Fore.LIGHTRED_EX + input_string + Fore.RESET, "Orange color failed"
    assert colorer.add_grey_color(input_string) == Fore.LIGHTBLACK_EX + input_string + Fore.RESET, "Grey color failed"

def style_test():
    styler = Styler()
    input_string = "Hello World"
    assert styler.add_bold(input_string) == Style.BRIGHT + input_string + Style.RESET_ALL, "Bold failed"

def text_editor_test():
    text_editor = TextEditor()
    input_string = "==22== Conditional jump or move depends on uninitialised value(s)"
    address_string = "by 0x11D3DB: join (strutil.c:85)"
    assert text_editor.remove_PID(input_string) == "Conditional jump or move depends on uninitialised value(s)", "Remove PID failed"
    assert text_editor.add_number(input_string, 3) == "3-" + input_string, "Add line number failed"
    assert text_editor.add_spaces(input_string, 3) == '   ' + input_string, "Add space failed"
    assert text_editor.remove_address(address_string) == "by join (strutil.c:85)", "Remove address failed"

def _file_processing(file_name):
    beautifier = Beautifier()
    input_file = open('resources/input/' + file_name, 'r')
    expected_output_file = open('resources/expectedOutput/' + file_name, 'r')
    input_content = input_file.read()
    expected_output_content = expected_output_file.read()
    assert beautifier.process(input_content) == expected_output_content, file_name + " processing failed"

def file_processing():
    files = ["useOfUninitialisedValue.txt", "memoryLeaks.txt", "conditionalJump.txt", "invalidFree.txt", "invalidWriteRead.txt"]
    for f in files:
        _file_processing(f)

if __name__ == "__main__":
    color_test()
    style_test()
    text_editor_test()
    file_processing()
    print("Everything passed")