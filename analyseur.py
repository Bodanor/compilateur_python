#-----------------
# Grammaire :
# <Prog> → start>  <SuitesInstructions>  <stop
# <SuitesInstructions> → <Instruction> | <SuiteInstructions>; <Instruction>
# <Instruction> → <Var> =  <ExprOR> | print <ExprOR> | input <Var>
# <ExprOR> → <ExprAND> | <ExprOR> | <ExprAND>
# <ExprAND> →  <ExprPM> | <ExprAND> & <ExprPM>
# <ExprPM> → <ExprFDM> | <ExprPM> + <ExprFDM> | <ExprPM> - <ExprFDM>
# <ExprFDM> → <Sign> | <ExprFDM> * <Sign> | <ExprFDM>/ <Sign> | <ExprFDM>% <Sign>
# <Sign> → <Factor> | - <Factor> | ~ <Factor>
# <Factor> → ( <ExprOR> ) | <Nb> | <Var>
# <Nb> →  0b<Binaire> | 0x<Hexa> | <Digit>
# <Digit> → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# <Binaire> → 0| 1
# <Hexa> → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9  | A | B | C | D | E | F | a | b | c | d | e | f
# <Var> → i<Word> | s<Word> | b <Word>
# <Word> → <Alph> | <Word> <Alph>
# <Alph> → a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|
# M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
#------------------------------

def Prog():
    SymboleSuivant(0)
    if SymboleCourant(6) == "start>":
        SymboleSuivant(6)
        SuiteInstruction()
        if SymboleCourant(5) == "<stop":
            SymboleSuivant(5)
            return True
        else:
            return False
    else:
        return False

def SuiteInstruction():
    Instruction()
    if SymboleCourant(1) == ";":
        while SymboleCourant(1) == ";":
            SymboleSuivant(1)
            Instruction()


#-----------------------------------------
def Instruction():
    global word
    global destination_word
    instru = ""

    if programme[posCourante : posCourante + 5] == "input":
        SymboleSuivant(5)
        if Var() == True:
            if word not in variables:
                variables.append(word)
    if Var() == True:
        if SymboleCourant(1) == "=":
            destination_word = word
            if len(variables) == 0:
                variables.append(word)

            if word not in variables:
                variables.append(word)

            SymboleSuivant(1)
            while SymboleCourant(1) == " ":
                SymboleSuivant(1)
            ExprOR()

    if programme[posCourante : posCourante + 5] == "print":
        SymboleSuivant(5)
        ExprOR()
    else:
        ExprOR()
# ----------------------------------------
def ExprOR():
    ExprAND()
    if SymboleCourant(1) == '|':
        SymboleSuivant(1)
        ExprAND()

def ExprAND():
    ExprPM()
    if SymboleCourant(1) == '&':
        SymboleSuivant(1)
        ExprPM()

def ExprPM():
    ExprFD()
    while SymboleCourant(1) in "+-":
        if SymboleCourant(1) == '+':
            SymboleSuivant(1)
            ExprFD()

        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            ExprFD()


# ----------------------------------------

def ExprFD():
    ExprNV()
    while SymboleCourant(1) in "*/%":
        if SymboleCourant(1) == '*':
            SymboleSuivant(1)
            ExprNV()

        elif SymboleCourant(1) == '/':
            SymboleSuivant(1)
            ExprNV()

        elif SymboleCourant(1) == '%':
            SymboleSuivant(1)
            Factor()

def ExprNV():
    Factor()
    while SymboleCourant(1) in "~-":
        if SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Factor()


        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Factor()


def Factor():
    global destination_word
    global word

    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprOR()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    elif Var():
        if word not in variables:
            print("Erreur position {} : {} n'a pas été déclaré précedemment".format(str(posCourante + 1), word))
            exit(-1)
    else:
        Nb()


# ----------------------------------------
def Nb():
    nb = ""
    if Digit() == True:
        nb += SymboleCourant(1)
        SymboleSuivant(1)
        if SymboleCourant(1) == "b" or SymboleCourant(1) == "B":
            nb += SymboleCourant(1)
            SymboleSuivant(1)
            while Binary() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 2)

        elif SymboleCourant(1) == "x" or SymboleCourant(1) == "x":
            nb += SymboleCourant(1)
            SymboleSuivant(1)
            while Hexa() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 16)

        else:
            while Digit() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
# ----------------------------------------

def Binary():
    if SymboleCourant(1) in "01":
        return True
    else:
        return False
# ---------------------------------------
def Hexa():
    if SymboleCourant(1) in "0123456789abcdef" or SymboleCourant(1) in "ABCDEF":
        return True
    else:
        return False

def Digit():
    if SymboleCourant(1) in "0123456789":
        return True
    else:
        return False
#-----------------------------------------
def Var():

    global word

    if SymboleCourant(1) in "isb":
        word = SymboleCourant(1)
        SymboleSuivant(1)
        Word()
        return True
    else:
        return False

#-----------------------------------------
def Word():
    global word
    while Alph() == True :
        word += SymboleCourant(1)
        SymboleSuivant(1)

#-----------------------------------------
def Alph() :
    if SymboleCourant(1) in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return True
    else:
        return False
# ----------------------------------------


def SymboleCourant(n):
    return programme[posCourante:posCourante + n]

# ----------------------------------------

def SymboleSuivant(n):
    global posCourante
    posCourante = posCourante + n
    while posCourante < len(programme) and programme[posCourante] == ' ':
        posCourante = posCourante + 1

# ----------------------------------------

programme = ("start>input sNombre; input bNb; print sNombre * -bNb<stop")
posCourante = 0
word = ""
destination_word = ""
declare_header = 0
declare_print = 0
declare_input = 0
variables = []
if Prog() == True:
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1),
          "à la " + str(posCourante + 1) + "e position est invalide!")