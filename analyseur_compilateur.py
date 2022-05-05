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

# ----------------------------------------
def ExprO():
    ExprA()
    if SymboleCourant(1) == '|':
        SymboleSuivant(1)
        ExprA()
        nb2 = popResultat()
        nb1 = popResultat()
        resultat.append(nb1 | nb2)
def ExprA():
    ExprPM()
    if SymboleCourant(1) == '&':
        SymboleSuivant(1)
        ExprPM()
        nb2 = popResultat()
        nb1 = popResultat()
        resultat.append(nb1 & nb2)



def ExprPM():
    ExprFD()
    while SymboleCourant(1) in "+-":
        if SymboleCourant(1) == '+':
            SymboleSuivant(1)
            ExprFD()
            nb2 = popResultat()
            nb1 = popResultat()
            resultat.append(nb1 + nb2)
        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            ExprFD()
            nb2 = popResultat()
            nb1 = popResultat()
            resultat.append(nb1 - nb2)

# ----------------------------------------
def ExprFD():
    ExprNV()
    while SymboleCourant(1) in "*/%":
        if SymboleCourant(1) == '*':
            SymboleSuivant(1)
            ExprNV()
            nb2 = popResultat()
            nb1 = popResultat()
            resultat.append(nb1 * nb2)
        elif SymboleCourant(1) == '/':
            SymboleSuivant(1)
            ExprNV()
            nb2 = popResultat()
            nb1 = popResultat()
            resultat.append(int(nb1 / nb2))
        elif SymboleCourant(1) =='%':
            SymboleSuivant(1)
            ExprNV()
            nb2 = popResultat()
            nb1 = popResultat()
            resultat.append(int(nb1 % nb2))
# ----------------------------------------
def ExprNV():
    Facteur()
    while SymboleCourant(1) in "~-":
        if SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Facteur()
            nb1 = popResultat()
            resultat.append(~int(nb1))

        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Facteur()
            nb1 = popResultat()
            resultat.append(not int(nb1))
# ----------------------------------------
def Facteur():
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprO()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    else:
        Nombre()
# -----------------------------------------
def Nombre():
    nb = ""
    if Chiffre() == True:
        nb = ""
        nb = ord(SymboleCourant(1)) - 0x30
        SymboleSuivant(1)
        while Chiffre() == True:
            nb = nb * 10 + ord(SymboleCourant(1)) - 0x30
            SymboleSuivant(1)
    if SymboleCourant(1) == "b" or SymboleCourant(1) == "B":
        nb = ""
        SymboleSuivant(1)
        while Binaire() == True:
            nb += SymboleCourant(1)
            SymboleSuivant(1)
        nb = int(nb, 2)

    if SymboleCourant(1) == "x" or SymboleCourant(1) == "x":
        nb = ""
        SymboleSuivant(1)
        while Hexa() == True:
            nb += SymboleCourant(1)
            SymboleSuivant(1)
        nb = int(nb, 16)
    resultat.append(nb)

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
# ----------------------------------------
def Chiffre():
    if SymboleCourant(1) in "0123456789":
        return True
    else :
        return False

# ----------------------------------------
def popResultat():
    if len(resultat) > 0:
        return resultat.pop()
    else:
        print("Valeur manquante dans l'expression !")
        exit()

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
programme = ("start" "-(-(144 + 0b11) + ~0xff)" "stop")
resultat = []
posCourante = 0
if Prog() == True:
    print("Le résultat de l'expression est :", popResultat())
else:
    print("Erreur dans le code source à partir de la " + str(posCourante + 1) + "e position !")