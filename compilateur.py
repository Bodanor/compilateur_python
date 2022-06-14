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
        codeCible.append("void main()")
        codeCible.append("{")
        codeCible.append("\t_asm")
        codeCible.append("\t{")
        SuiteInstruction()
        if SymboleCourant(5) == "<stop":
            SymboleSuivant(5)
            codeCible.append("\t}")
            codeCible.append("}")
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
    global declare_header
    global declare_print
    global declare_input
    instru = ""

    if programme[posCourante : posCourante + 5] == "input":
        SymboleSuivant(5)
        if not declare_header:
            codeCible.insert(0, "#include <stdio.h>")
            declare_header = 1
        if not declare_input:
            codeCible.insert(1,'const char msgSaisie[] = "%d";')
            codeCible.insert(2, 'const char msgEntrez[] = "Entrez une valeur : ";')
            codeCible.insert(3, "int varSaisie;")
            declare_input = 1

        codeCible.append("\t\tpush offset msgEntrez")
        codeCible.append("\t\tcall dword ptr printf")
        codeCible.append("\t\tadd esp, 4")
        codeCible.append("\t\tpush offset varSaisie")
        codeCible.append("\t\tpush offset msgSaisie")
        codeCible.append("\t\tcall dword ptr scanf")
        codeCible.append("\t\tadd esp, 8")
        codeCible.append("\t\tpush varSaisie")
        codeCible.append("\t\tpop eax")
        if Var() == True:
            if word not in variables:
                variables.append(word)
                if word[0] == "i":
                    codeCible.insert(4, "int {};".format(word))
                elif word[0] == "s":
                    codeCible.insert(4, "short {};".format(word))
                elif word[0] == "b":
                    codeCible.insert(4, "char {};".format(word))

            if word[0] == "i":
                codeCible.append("\t\tmov {}, eax".format(word))
            if word[0] == "s":
                codeCible.append("\t\tmov {}, ax".format(word))
            if word[0] == "b":
                codeCible.append("\t\tmov {}, al".format(word))



    if Var() == True:
        if SymboleCourant(1) == "=":
            destination_word = word
            if len(variables) == 0:
                if word[0] == "i":
                    codeCible.insert(0, "int {};".format(word))
                elif word[0] == "s":
                    codeCible.insert(0, "short {};".format(word))
                elif word[0] == "b":
                    codeCible.insert(0, "char {};".format(word))
                variables.append(word)

            if word not in variables:
                variables.append(word)
                if word[0] == "i":
                    codeCible.insert(0, "int {};".format(word))
                elif word[0] == "s":
                    codeCible.insert(0, "short {};".format(word))
                elif word[0] == "b":
                    codeCible.insert(0, "char {};".format(word))

            SymboleSuivant(1)
            while SymboleCourant(1) == " ":
                SymboleSuivant(1)
            ExprOR()
            if destination_word[0] == "i":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov {}, eax".format(destination_word))
            if destination_word[0] == "s":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov {}, ax".format(destination_word))
            if destination_word[0] == "b":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov {}, al".format(destination_word))

    if programme[posCourante : posCourante + 5] == "print":
        SymboleSuivant(5)
        if not declare_header:
            codeCible.insert(0, "#include <stdio.h>")
            declare_header = 1

        if not declare_print:
            codeCible.insert(1,'const char msgAffichage[] = "Valeur = %d\\n";')
            declare_print = 1
        ExprOR()
        codeCible.append("\t\tpush offset msgAffichage")
        codeCible.append("\t\tcall dword ptr printf")
        codeCible.append("\t\tadd esp, 8")


    else:
        ExprOR()
        if SymboleCourant(1) == " ":
            codeCible.append("\t\tpop eax")
# ----------------------------------------
def ExprOR():
    ExprAND()
    if SymboleCourant(1) == '|':
        SymboleSuivant(1)
        ExprAND()
        codeCible.append("\t\tpop ebx")
        codeCible.append("\t\tpop eax")
        codeCible.append("\t\tor eax, ebx")
        codeCible.append("\t\tpush eax")
def ExprAND():
    ExprPM()
    if SymboleCourant(1) == '&':
        SymboleSuivant(1)
        ExprPM()
        codeCible.append("\t\tpop ebx")
        codeCible.append("\t\tpop eax")
        codeCible.append("\t\tand eax, ebx")
        codeCible.append("\t\tpush eax")


def ExprPM():
    ExprFD()
    while SymboleCourant(1) in "+-":
        if SymboleCourant(1) == '+':
            SymboleSuivant(1)
            ExprFD()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tadd eax, ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            ExprFD()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tsub eax, ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------

def ExprFD():
    ExprNV()
    while SymboleCourant(1) in "*/%":
        if SymboleCourant(1) == '*':
            SymboleSuivant(1)
            ExprNV()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\timul eax, ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '/':
            SymboleSuivant(1)
            ExprNV()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '%':
            SymboleSuivant(1)
            Factor()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush edx")

def ExprNV():
    Factor()
    while SymboleCourant(1) in "~-":
        if SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Factor()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tnot eax")
            codeCible.append("\t\tpush eax")

        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Factor()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tneg eax")
            codeCible.append("\t\tpush eax")

def Factor():
    global destination_word
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprOR()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    elif Var():
        while Var():
            SymboleSuivant(1)
        if word not in variables:
            print("Erreur position {} : {} n'a pas été déclaré précedemment".format(str(posCourante + 1), word))
            exit(-1)
        if word[0:1] in "sb":
            codeCible.append("\t\tmovsx eax, {}".format(word))
        else:
            codeCible.append("\t\tmov eax, {}".format(word))
        codeCible.append("\t\tpush eax")
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
            codeCible.append("\t\tpush dword ptr " + str(nb))

        elif SymboleCourant(1) == "x" or SymboleCourant(1) == "x":
            nb += SymboleCourant(1)
            SymboleSuivant(1)
            while Hexa() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 16)
            codeCible.append("\t\tpush dword ptr " + str(nb))
        else:
            while Digit() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            codeCible.append("\t\tpush dword ptr " + str(nb))
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

programme = ("start> input sNombre;input bNb;print sNombre * -bNb <stop")
codeCible = []
posCourante = 0
word = ""
destination_word = ""
declare_header = 0
declare_print = 0
declare_input = 0
variables = []
if Prog() == True:
    for c in codeCible:
        print(c)
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1),
          "à la " + str(posCourante + 1) + "e position est invalide!")