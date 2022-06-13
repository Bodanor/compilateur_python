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
            if word[0] == "i":
                codeCible.append("\t\tpop {}".format(destination_word))
            elif word[0] == "s":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov {}, ax".format(destination_word))
            elif word[0] == "b":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov {}, al".format(destination_word))
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
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprOR()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    else:
        if Digit() == True:
            Nb()
        else:
            Var()
            if word not in variables:
                print("Variable innexistante !")
                SymboleSuivant(1)

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
    while Alhp() == True :
        word += SymboleCourant(1)
        SymboleSuivant(1)

#-----------------------------------------
def Alhp() :
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

programme = ("start> sVar = (2 + 33) * 5; bVal = 8 / 2 * 0xf0; sVar = 0b110 + bVal <stop")
codeCible = []
posCourante = 0
word = ""
destination_word = ""

variables = []
if Prog() == True:
    for c in codeCible:
        print(c)
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1),
          "à la " + str(posCourante + 1) + "e position est invalide!")