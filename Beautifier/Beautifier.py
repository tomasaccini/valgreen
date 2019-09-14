#!/usr/bin/env python3

from colorama import Fore, Style
import re

class Colorer:
    def _add_color(self, input_string, opener, closer):
        return opener + input_string + closer

    def add_red_color(self, input_string):
        return self._add_color(input_string, Fore.RED, Fore.RESET)

    def add_blue_color(self, input_string):
        return self._add_color(input_string, Fore.BLUE, Fore.RESET)

    def add_magenta_color(self, input_string):
        return self._add_color(input_string, Fore.MAGENTA, Fore.RESET)

    def add_orange_color(self, input_string):
        return self._add_color(input_string, Fore.YELLOW, Fore.RESET)

    def add_green_color(self, input_string):
        return self._add_color(input_string, Fore.GREEN, Fore.RESET)
    
    def add_grey_color(self, input_string):
        return self._add_color(input_string, Fore.LIGHTBLACK_EX, Fore.RESET)

class Styler:
    def _add_style(self, input_string, opener, closer):
        return opener + input_string + closer
    
    def add_bold(self, input_string):
        return self._add_style(input_string, Style.BRIGHT, Style.RESET_ALL)

class TextEditor:
    def remove_PID(self, input_string):
        return re.sub(r'==\d{1,5}== *', '', input_string)
    
    def remove_address(self, input_string):
        return re.sub(r'0x.*: ', '', input_string)

    def add_number(self, input_string, i):
        return str(i) + ") " + input_string
        
    def add_spaces(self, input_string, n):
        return ' ' * n + input_string
    
class Beautifier:
    def __init__(self):
        self.colorer = Colorer()
        self.styler = Styler()
        self.textEditor = TextEditor()
        self.skip = ["Memcheck, a memory error detector", "For counts of detected and suppressed errors, rerun with: -v"]
        self.skipRegex = [r"Copyright \(C\) 2002-.*, and GNU GPL'd, by Julian Seward et al.", r"Using Valgrind-.* and LibVEX; rerun with -h for copyright info"]
        self.problemTitles = ["Conditional jump or move depends on uninitialised value(s)", "Invalid free() / delete / delete[] / realloc()"]
        self.problemTitlesRegex = [r'Invalid write of size .*', r'Invalid read of size .*', r'Use of uninitialised value of size .*', r'.* bytes in .* blocks are .* in loss record .* of .*']
        self.rootCauseTitles = ["Uninitialised value was created by a heap allocation", "Uninitialised value was created by a stack allocation", "Block was alloc'd at"]
        self.rootCauseTitlesRegex = [r'Address 0x.* is .* bytes .* a block of size .* free\'d']
        self.leakSummaryRegex = [r"definitely lost: .* bytes in .* blocks", r"possibly lost: .* bytes in .* blocks", r"still reachable: .* bytes in .* blocks", r"suppressed: .* bytes in .* blocks", r"indirectly lost: .* bytes in .* blocks"]

    def _skip(self, line):
        if (line == ''):
            return True
        if (line in self.skip):
            return True
        for reg in self.skipRegex:
            if (re.sub(reg, '', line) == ''):
                return True
        return False

    def _isLeakSummary(self, line):
        if (line == ''):
            return False
        for reg in self.leakSummaryRegex:
            if (re.sub(reg, '', line) == ''):
                return True
        return False


    def _isProblemTitle(self, line):
        if (line == ''):
            return False
        if (line in self.problemTitles):
            return True
        for reg in self.problemTitlesRegex:
            if (re.sub(reg, '', line) == ''):
                return True
        return False

    def _isRootCause(self, line):
        if (line == ''):
            return False
        if (line in self.rootCauseTitles):
            return True
        for reg in self.rootCauseTitlesRegex:
            if (re.sub(reg, '', line) == ''):
                return True
        return False

    def process(self, input_string):
        lines = input_string.split('\n')
        result = ""
        problem_numbering = 1
        first_line_of_problem = False
        first_important_line_of_problem = False
        first_line_of_root_cause = False
        first_importat_line_of_root_cause = False
        orange_colored = False
        sendToBack = []

        for line in lines:
            temp = self.textEditor.remove_address(self.textEditor.remove_PID(line))
            if (self._skip(temp)):
                continue

            if (re.sub(r'Command: \./.*', '', temp) == ''):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.colorer.add_green_color(temp)), 1)
                result += temp + '\n'
                continue

            # Is HEAP SUMMARY header?
            if (temp == "HEAP SUMMARY:"):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.colorer.add_green_color(temp)), 1)
                sendToBack.append('\n\n'+temp)
                continue
            if (re.sub(r'in use at exit: .* bytes in .* blocks', '', temp) == '' or re.sub(r'total heap usage: .* allocs, .* frees, .* bytes allocated', '', temp) == ''):
                temp = self.textEditor.add_spaces(self.styler.add_bold(temp), 4)
                sendToBack.append(temp)
                continue

            # LEAK SUMMARY
            if (temp == "LEAK SUMMARY:"):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.colorer.add_red_color(temp)), 1)
                sendToBack.append('\n\n'+temp)
                continue
            
            if (self._isLeakSummary(temp)):
                temp = self.textEditor.add_spaces(self.styler.add_bold(temp), 4)
                sendToBack.append(temp)
                continue

            # VALGRIND CONCLUSION
            if ("All heap blocks were freed -- no leaks are possible" in temp or "ERROR SUMMARY: 0 errors from 0 contexts" in temp):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.colorer.add_green_color(temp)), 1)
                sendToBack.append('\n'+temp)
                continue

            if ("ERROR SUMMARY: " in temp):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.colorer.add_red_color(temp)), 1)
                sendToBack.append('\n\n'+temp)
                continue

            # Is title?
            if (self._isProblemTitle(temp)):
                temp = self.textEditor.add_spaces(self.styler.add_bold(self.textEditor.add_number(temp, problem_numbering)), 2 - len(str(problem_numbering)))
                problem_numbering += 1
                first_line_of_problem = True
                first_important_line_of_problem = True
                result += '\n'+temp + '\n'
                continue

            # Is root cause?
            if (self._isRootCause(temp)):
                if ("free'd" in temp):
                    orange_colored = True
                temp = self.textEditor.add_spaces(self.styler.add_bold(temp), 3)
                first_line_of_root_cause = True
                first_importat_line_of_root_cause = True
                result += temp + '\n'
                continue

            # Is a .so line?
            if (re.sub(r'\(.*\.so\)', '', temp) != temp):
                first_part = re.sub(r'\(.*\.so\)', '', temp)
                second_part = self.colorer.add_grey_color(temp[len(first_part):])
                temp = first_part + second_part

            # Is the first important line of the problem?
            if (first_important_line_of_problem):
                # If it is not a .so line
                if (re.sub(r'\(.*\.so\)', '', temp) == temp):
                    temp = self.colorer.add_red_color(self.styler.add_bold(temp))
                    first_important_line_of_problem = False

            # Is the first important line of the root cause?
            if (first_importat_line_of_root_cause):
                # If it is not a .so line
                if (re.sub(r'\(.*\.so\)', '', temp) == temp):
                    if (orange_colored):
                        temp = self.colorer.add_orange_color(temp)
                        orange_colored = False
                    else:
                        temp = self.colorer.add_magenta_color(temp)
                    temp = self.styler.add_bold(temp)
                    first_importat_line_of_root_cause = False

            # Is the first line of the problem?
            if (first_line_of_problem):
                temp = self.textEditor.add_spaces(temp, 3)
                first_line_of_problem = False

            # Is the first line of the root cause?
            elif (first_line_of_root_cause):
                temp = self.textEditor.add_spaces(temp, 3)
                first_line_of_root_cause = False

            # Else it is a secondary line, will be shown in grey
            else:
                temp = self.textEditor.add_spaces(self.colorer.add_grey_color(temp), 4)

            result += temp + '\n'

        for line in sendToBack:
            result += line + '\n'
            
        return result