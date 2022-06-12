def Prog():
    SymboleSuivant(0)
    if SymboleCourant(5) == "start":
        SymboleSuivant(5)
        ExprO()
        if SymboleCourant(4) == "stop":
            SymboleSuivant(4)
            return True
        else:
            return False
    else:
        return False
def Instruction():
    if Var() == True:
        if SymboleCourant(1) == "=":
            SymboleSuivant(1)
            while SymboleCourant(1) == " ":
                SymboleSuivant(1)
            ExprOR()
    else:
        ExprOR()

# ----------------------------------------
def ExprO():
    ExprA()
    if SymboleCourant(1) == '|':
        SymboleSuivant(1)
        ExprA()

def ExprA():
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
            ExprNV()

# ----------------------------------------
def ExprNV():
    Facteur()
    while SymboleCourant(1) in "~-":
        if SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Facteur()

        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Facteur()
# ----------------------------------------
def Factor():

    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprOR()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    else:
        Nb()
        Var()
# -----------------------------------------
def Nb():
    nb = ""
    if Digit() == True:
        nb += SymboleCourant(1)
        SymboleSuivant(1)
        if SymboleCourant(1) == "b" or SymboleCourant(1) == "B":
            SymboleSuivant(1)
            while Binary() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 2)

        elif SymboleCourant(1) == "x" or SymboleCourant(1) == "x":
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

#-----------------------------------------
def Var():
    if SymboleCourant(1) == "i":
        SymboleSuivant(1)
        Word()
        return True
    elif SymboleCourant(1) == "s":
        SymboleSuivant(1)
        Word()
        return True
    elif SymboleCourant(1) == "b":
        SymboleSuivant(1)
        Word()
        return True
    else:
        return False


#-----------------------------------------
def Word():
    word = ""
    while Alhp() == True :
        word += SymboleCourant(1)
        SymboleSuivant(1)

# ----------------------------------------
def SymboleCourant(n):
    return programme[posCourante:posCourante + n]
# ---------------------------------------
def SymboleSuivant(n):
    global posCourante
    posCourante = posCourante + n
    while posCourante < len(programme) and programme[posCourante] == ' ':
        posCourante = posCourante + 1
# ----------------------------------------
programme = ("start iVar = -(-(144 + 0b11) + ~0xff) stop")

posCourante = 0
if Prog() == True:
    print("Analyse reussie !")

else:
    print("Erreur dans le code source à partir de la " + str(posCourante + 1) + "e position !")