#!/usr/bin/env python
import sys

fileName = "input.txt"
with open(sys.argv[1], 'r') as my_file:
    inputContent = my_file.read()
fileIndex = 0
EOF = "EOF"
INVALID = "INVALID"
tokens = []
lexemes = []
tokens_lines = []
lexemes_lines = []

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
STRING = 12
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
IF_TOKEN = 41
THEN_TOKEN = 42
FLOAT_TOKEN = 46
COMMA = 48
SEMI_COLON = 49
COLON = 50
EQUALS_TO = 51
GREATER = 52
LESS = 53
PRINT = 54
SINGLE_QUOTE = 55
GOTO_TOKEN = 56
MOD_OP = 57


lexeme = ""
lexLen = 0


def lookupSymbol(character):
    if (character == "("):
        nextToken = LEFT_PAREN
    elif (character == ")"):
        nextToken = RIGHT_PAREN
    elif (character == ">"):
        nextToken = GREATER
    elif (character == "<"):
        nextToken = LESS
    elif (character == "-"):
        nextToken = SUB_OP
    elif (character == "*"):
        nextToken = MULT_OP
    elif (character == "/"):
        nextToken = DIV_OP
    elif (character == ","):
        nextToken = COMMA
    elif (character == ";"):
        nextToken = SEMI_COLON
    elif (character == ":"):
        nextToken = COLON
    elif (character == "'"):
        nextToken = SINGLE_QUOTE
    else:
        nextToken = INVALID

    return nextToken


def getChar():
    global inputContent
    global fileIndex
    if (fileIndex < len(inputContent)):
        nextChar = inputContent[fileIndex]
        fileIndex += 1
        return nextChar
    else:
        return EOF


def getNonBlank():
    char = getChar()
    while (char.isspace()):
        char = getChar()
    return char


def getCharClass(char):
    if char.isalpha():
        charClass = LETTER
    elif char.isdigit():
        charClass = DIGIT
    else:
        charClass = UNKNOWN
    return charClass


def lex(char):
    lexeme = ""
    charClass = getCharClass(char)
    global fileIndex

    if (charClass == LETTER):
        lexeme += char
        nextChar = getChar()
        while(nextChar != EOF and nextChar != " " and (getCharClass(nextChar) == LETTER or getCharClass(nextChar) == DIGIT)):
            lexeme += nextChar
            nextChar = getChar()

        # Check for keywords

        if (lexeme == "IF"):
            nextToken = IF_TOKEN
        elif (lexeme == "THEN"):
            nextToken = THEN_TOKEN
        elif (lexeme == "SET"):
            nextToken = ASSIGN_OP
        elif (lexeme == "integer"):
            nextToken = INT_LIT
        elif (lexeme == "float"):
            nextToken = FLOAT_TOKEN
        elif (lexeme == "string"):
            nextToken = STRING
        elif (lexeme == "GOTO"):
            nextToken = GOTO_TOKEN
        elif (lexeme == "ADD"):
            nextToken = ADD_OP
        elif (lexeme == "SUB"):
            nextToken = SUB_OP
        elif (lexeme == "MULT"):
            nextToken = MULT_OP
        elif (lexeme == "DIV"):
            nextToken = DIV_OP
        elif (lexeme == "MOD"):
            nextToken = MOD_OP
        elif (lexeme == "EQ"):
            nextToken = EQUALS_TO
        elif (lexeme == "GRE"):
            nextToken = GREATER
        elif (lexeme == "LESS"):
            nextToken = LESS
        elif (lexeme == "PRINT"):
            nextToken = PRINT
        else:
            nextToken = IDENT

        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == DIGIT):
        lexeme += char
        nextChar = getChar()
        while((nextChar != EOF) and (nextChar != " ") and (getCharClass(nextChar) == DIGIT)):
            lexeme += nextChar
            nextChar = getChar()
        nextToken = INT_LIT
        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == UNKNOWN):
        token = lookupSymbol(char)
        lexeme += char
        nextToken = token

    tokens.append(nextToken)
    lexemes.append(lexeme)
    return nextToken


def match_set_code(program, i):
    match program[i]:
        case ((20, _), (25, _), (11, x), (48, _), (10, y), (26, _)):
            globals()[x] = int(y)
        case ((20, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[y]
        case ((20, _), (11, x), (25, _), (21, _), (10, y), (48, _), (10, z), (26, _)):
            globals()[x] = int(y) + int(z)
        case ((20, _), (11, x), (25, _), (22, _), (10, y), (48, _), (10, z), (26, _)):
            globals()[x] = int(y) - int(z)
        case ((20, _), (11, x), (25, _), (23, _), (10, y), (48, _), (10, z), (26, _)):
            globals()[x] = int(y) * int(z)
        case ((20, _), (11, x), (25, _), (24, _), (10, y), (48, _), (10, z), (26, _)):
            globals()[x] = int(y) / int(z)
        case ((20, _), (11, x), (25, _), (21, _), (11, y), (48, _), (11, z), (26, _)):
            globals()[x] = globals()[y] + globals()[z]
        case ((20, _), (11, x), (25, _), (21, _), (11, y), (48, _), (10, z), (26, _)):
            globals()[x] = globals()[y] + int(z)
        case ((20, _), (11, x), (25, _), (22, _), (11, y), (48, _), (11, z), (26, _)):
            globals()[x] = globals()[y] - globals()[z]
        case ((20, _), (11, x), (25, _), (22, _), (11, y), (48, _), (10, z), (26, _)):
            globals()[x] = globals()[y] - int(z)
        case ((20, _), (11, x), (25, _), (23, _), (11, y), (48, _), (11, z), (26, _)):
            globals()[x] = globals()[y] * globals()[z]
        case ((20, _), (11, x), (25, _), (23, _), (11, y), (48, _), (10, z), (26, _)):
            globals()[x] = globals()[y] * int(z)
        case ((20, _), (11, x), (25, _), (24, _), (11, y), (48, _), (11, z), (26, _)):
            globals()[x] = globals()[y] / globals()[z]
        case ((20, _), (11, x), (25, _), (24, _), (11, y), (48, _), (10, z), (26, _)):
            globals()[x] = globals()[y] / int(z)


def match_int_code(program, i):
    match program[i]:
        case ((10, _), (11, x)):
            globals()[x] = 0
        case ((10, _), (11, x), (48, _), (10, y)):
            globals()[x] = int(y)
        case ((10, _), (25, _), (11, x), (48, _), (10, y), (26, _)):
            globals()[x] = int(y)


def match_string_code(program, i):
    match program[i]:
        case ((12, _), (11, x)):
            globals()[x] = ''
        case ((12, _), (11, x), (48, _), (55, _), (11, y), (55, _)):
            globals()[x] = str(y)
        case ((12, _), (25, _), (11, x), (48, _), (55, _), (10, y), (55, _), (26, _)):
            globals()[x] = str(y)


def match_add_code(program, i):
    match program[i]:
        case ((21, _), (25, _), (10, x), (48, _), (10, y), (26, _)):
            int(x) + int(y)
        case ((21, _), (25, _), (11, x), (48, _), (10, y), (26, _)):
            globals()[x] = globals()[x] + int(y)
        case ((21, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[x] + globals()[y]
        case ((21, _), (11, x), (48, _), (10, y)):
            globals()[x] = globals()[x] + int(y)
        case ((22, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[x] - globals()[y]
        case ((22, _), (11, x), (48, _), (10, y)):
            globals()[x] = globals()[x] - int(y)
        case ((23, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[x] * globals()[y]
        case ((23, _), (11, x), (48, _), (10, y)):
            globals()[x] = globals()[x] * int(y)
        case ((24, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[x] / globals()[y]
        case ((24, _), (11, x), (48, _), (10, y)):
            globals()[x] = globals()[x] / int(y)


def match_if_code(program, i):
    if(program[i][-2][0] == 56):
        match program[i]:
            case ((41, _), (11, x), (_, _), (11, y), (42, _), (56, _), (11, z)):
                match program[i][2][0]:
                    case 51:
                        if(globals()[x] == globals()[y]):
                            match_goto_code(program, i)
                    case 52:
                        if(globals()[x] > globals()[y]):
                            match_goto_code(program, i)
                    case 53:
                        if(globals()[x] < globals()[y]):
                            match_goto_code(program, i)
    elif (program[i][2][0] == 57):
        match_mod_code(program, i)

    else:
        match program[i][:5]:
            case ((41, _), (11, x), (_, _), (11, y), (42, _)):
                def fun():
                    num = 5 - len(program[i])
                    a_list = []
                    a_list.append(program[i][num:])
                    match_operator(a_list, 0)

                match program[i][2][0]:
                    case 51:
                        if(globals()[x] == globals()[y]):
                            fun()
                    case 52:
                        if(globals()[x] > globals()[y]):
                            fun()
                    case 53:
                        if(globals()[x] < globals()[y]):
                            fun()


def match_print_code(program, i):
    match program[i]:
        case ((54, _), (11, x)):
            print(globals()[x])
        case ((54, _), (55, _), (11, x), (55, _)):
            print(str(x))
        case ((54, _), (25, _), (21, _), (25, _), (11, x), (48, _), (11, y), (26, _), (26, _)):
            print(globals()[x] + globals()[y])
        case ((54, _), (25, _), (22, _), (25, _), (11, x), (48, _), (11, y), (26, _), (26, _)):
            print(globals()[x] - globals()[y])
        case ((54, _), (25, _), (23, _), (25, _), (11, x), (48, _), (11, y), (26, _), (26, _)):
            print(globals()[x] * globals()[y])
        case ((54, _), (25, _), (24, _), (25, _), (11, x), (48, _), (11, y), (26, _), (26, _)):
            print(globals()[x] / globals()[y])


def match_goto_pos(program, i):
    globals()[program[i][0][1]] = i


def match_goto_code(program, i):
    match program[i]:
        case ((56, _), (11, _)):
            for index in range(globals()[program[i][1][1]], i):
                print(index+1)
                match_operator(program, index)
        case (_, _, _, _, _, (56, _), (11, x)):
            for index in range(globals()[x], i+1):
                match_operator(program, index)


def match_mod_code(program, i):
    match program[i]:
        case((41, _), (11, x), (57, _), (11, y), (51, _), (11, z), (42, _), (54, _), (11, k)):
            if((globals()[x] % globals()[y]) == globals()[z]):
                print(globals()[k])


def match_operator(program, i):
    match program[i][0][0]:
        case 10:
            match_int_code(program, i)
        case 11:
            match_goto_pos(program, i)
        case 20:
            match_set_code(program, i)
        case 21:
            match_add_code(program, i)
        case 54:
            match_print_code(program, i)
        case 12:
            match_string_code(program, i)
        case 41:
            match_if_code(program, i)
        case 56:
            match_goto_code(program, i)
        case _:
            raise TypeError("not a operator we support")


def merge(list1, list2):

    merged_list = tuple(zip(list1, list2))
    return merged_list


def first_list_partition(list, x):
    return list[:list.index(x)]


def second_list_partition(list, x):
    return list[list.index(x)+1:]


def getLines_addAnother(list, x, list_to_add):
    if(x not in list):
        return

    list_to_add.append(first_list_partition(list, x))
    getLines_addAnother(second_list_partition(list, x), x, list_to_add)


def merge_lists_toTuple(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(merge(list1[i], list2[i]))
    return merged_list


def main():
    nextChar = getNonBlank()
    if (nextChar == EOF):
        print("File is empty")
        return

    while nextChar != EOF:
        nextToken = lex(nextChar)
        if (nextToken == INVALID):
            break
        nextChar = getNonBlank()

    getLines_addAnother(lexemes, ';', lexemes_lines)
    getLines_addAnother(tokens, SEMI_COLON, tokens_lines)
    main_list = merge_lists_toTuple(tokens_lines, lexemes_lines)
    for i in range(len(main_list)):
        match_operator(main_list, i)


main()
