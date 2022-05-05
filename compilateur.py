def Prog():
    SymboleSuivant(0)
    if SymboleCourant(6) == "start>":
        SymboleSuivant(6)
        codeCible.append("void main()")
        codeCible.append("{")
        codeCible.append("\t_asm")
        codeCible.append("\t{")
        ExprO()
        if SymboleCourant(5) == "<stop":
            SymboleSuivant(5)
            codeCible.append("\t\tpop eax")
            codeCible.append("\t}")
            codeCible.append("}")
            return True
        else:
            return False
    else:
        return False

# ----------------------------------------
def ExprO():
    ExprA()
    if SymboleCourant(1) == '|':
        SymboleSuivant(1)
        ExprA()
        codeCible.append("\t\tpop ebx")
        codeCible.append("\t\tpop eax")
        codeCible.append("\t\tor eax, ebx")
        codeCible.append("\t\tpush eax")
def ExprA():
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
            Facteur()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush edx")

def ExprNV():
    Facteur()
    while SymboleCourant(1) in "~-":
        if SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tnot eax")
            codeCible.append("\t\tpush eax")

        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tneg eax")
            codeCible.append("\t\tpush eax")

def Facteur():
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprO()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    else:
        Nombre()

# ----------------------------------------
def Nombre():
    nb = ""
    if Chiffre() == True:
        nb += SymboleCourant(1)
        SymboleSuivant(1)
        if SymboleCourant(1) == "b" or SymboleCourant(1) == "B":
            nb += SymboleCourant(1)
            SymboleSuivant(1)
            while Binaire() == True:
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
            while Chiffre() == True:
                nb += SymboleCourant(1)
                SymboleSuivant(1)
            codeCible.append("\t\tpush dword ptr " + str(nb))
# ----------------------------------------

def Binaire():
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

def Chiffre():
    if SymboleCourant(1) in "0123456789":
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

programme = ("start> -(-(144 + 0b11) + ~0xff) <stop")
codeCible = []
posCourante = 0

if Prog() == True:
    for c in codeCible:
        print(c)
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1),
          "à la " + str(posCourante + 1) + "e position est invalide!")