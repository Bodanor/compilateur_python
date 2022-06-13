def Prog():
    SymboleSuivant(0)
    if SymboleCourant(5) == "start":
        SymboleSuivant(5)
        affectation()
        codeCible.append("void main()")
        codeCible.append("{")
        codeCible.append("\t_asm")
        codeCible.append("\t{")
        SuiteInstr()
        if SymboleCourant(4) == "stop":
            SymboleSuivant(4)
            codeCible.append("\t}")
            codeCible.append("}")
            return True
        else:
            return False
    else:
        return False

# ----------------------------------------


def affectation():
    if "input" in programme and "print" not in programme:
        codeCible.append("#include <stdio.h>")
        codeCible.append('const char msgSaisie[] = "%d";')
        codeCible.append('const char msgEntrez[] = "Entrez une valeur : ";')
        codeCible.append("int varSaisie;")
    if "print" in programme and "input" not in programme:
        codeCible.append("#include <stdio.h>")
        codeCible.append('const char msgAffichage[] = "Valeur = %d\\n";')
    if "print" in programme and "input" in programme:
        codeCible.append("#include <stdio.h>")
        codeCible.append('const char msgSaisie[] = "%d";')
        codeCible.append('const char msgEntrez[] = "Entrez une valeur : ";')
        codeCible.append("int varSaisie;")
        codeCible.append('const char msgAffichage[] = "Valeur = %d\\n";')
    oui = 0
    mot = ""
    for i in programme:
        if oui == 1 or i in "isb":
            if i in " +-/*01234567890;":
                if mot not in VAR:
                    if mot != "b":
                        VAR.append(mot)
                mot = ""
                oui = 0
            else:
                mot = mot + i
                oui = 1
    i = 0
    while i < len(VAR):
        mot = VAR[i]
        if mot not in ["input", "start", "stop", "int", "print", "input ", "start ", "stop ", "int ", "print ", "input ", " start ", " stop ", " int ", " print "]:
            if mot[0] in "i":
                codeCible.append("int "+mot+";")
            if mot[0] in "b":
                codeCible.append("char "+mot+";")
            if mot[0] in "s":
                codeCible.append("short "+mot+";")

        i = i + 1

# ----------------------------------------


def SuiteInstr():
    Instr()
    while SymboleCourant(1) == ';':
        SymboleSuivant(1)
        Instr()

# ----------------------------------------


def Instr():
    if Reg():
        regCible = SymboleCourant(1)
        SymboleSuivant(1)
        while Reg():
            regCible = regCible + SymboleCourant(1)
            SymboleSuivant(1)
            if regCible == "print" or regCible == "input" or regCible in VAR:
                break
        if regCible not in VAR:
            VAR.append(regCible)

        if SymboleCourant(1) == '=':
            SymboleSuivant(1)
            ExprOr()
            if regCible[0:1] == "i":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov " + regCible + ", eax")
            elif regCible[0:1] == "s":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov " + regCible + ", ax")
            elif regCible[0:1] == "b":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov " + regCible + ", al")
        elif regCible == "print":
            ExprOr()
            codeCible.append("\t\tpush offset msgAffichage")
            codeCible.append("\t\tcall dword ptr printf")
            codeCible.append("\t\tadd esp, 8")
        elif regCible == "input":
            codeCible.append("\t\tpush offset msgEntrez")
            codeCible.append("\t\tcall dword ptr printf")
            codeCible.append("\t\tadd esp, 4")
            codeCible.append("\t\tpush offset varSaisie")
            codeCible.append("\t\tpush offset msgSaisie")
            codeCible.append("\t\tcall dword ptr scanf")
            codeCible.append("\t\tadd esp, 8")
            codeCible.append("\t\tpush varSaisie")
            codeCible.append("\t\tpop eax")
            if Reg():
                regCible = SymboleCourant(1)
                SymboleSuivant(1)
                while Reg():
                    regCible = regCible + SymboleCourant(1)
                    SymboleSuivant(1)
                    if regCible == "print" or regCible == "input" or regCible in VAR:
                        break
                if regCible not in VAR:
                    VAR.append(regCible)
            if regCible[0:1] == "s":
                codeCible.append("\t\tmov "+regCible+",ax")
            elif regCible[0:1] == "b":
                codeCible.append("\t\tmov "+regCible+",al")
            if regCible[0:1] == "i":
                codeCible.append("\t\tmov "+regCible+",eax")


# ----------------------------------------

def ExprOr():
    ExprAnd()
    while SymboleCourant(1) in "|":
        if SymboleCourant(1) == '|':
            SymboleSuivant(1)
            ExprAnd()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tor eax, ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------


def ExprAnd():
    ExprPM()
    while SymboleCourant(1) in "&":
        if SymboleCourant(1) == '&':
            SymboleSuivant(1)
            ExprPM()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tand eax, ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------


def ExprPM():
    ExprFD()
    while SymboleCourant(1) in "+-":
        if SymboleCourant(1) == '+':
            SymboleSuivant(1)
            if Reg():
                ExprFD()
                codeCible.append("\t\tpop ebx")
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tadd eax," + VAR[1])
                codeCible.append("\t\tpush eax")
            else:
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
    ExprNotNeg()
    while SymboleCourant(1) in "*/%":
        if SymboleCourant(1) == '*':
            SymboleSuivant(1)
            ExprNotNeg()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\timul eax, ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '/':
            SymboleSuivant(1)
            ExprNotNeg()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '%':
            SymboleSuivant(1)
            ExprNotNeg()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush edx")

# ----------------------------------------


def ExprNotNeg():
    Facteur()
    while SymboleCourant(1) in "-~":
        if SymboleCourant(1) == '-':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tneg eax")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tnot ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------


def Facteur():
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        ExprOr()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    elif Reg():
        regCible = SymboleCourant(1)
        SymboleSuivant(1)
        while Reg():
            regCible = regCible + SymboleCourant(1)
            SymboleSuivant(1)
            if regCible == "print" or regCible == "input" or regCible in VAR:
                break
        if regCible not in VAR:
            VAR.append(regCible)
        if regCible[0:1] in "sb":
            codeCible.append("\t\tmovsx eax, " + regCible)
        else:
            codeCible.append("\t\tmov eax, " + regCible)
        codeCible.append("\t\tpush eax")
    else:
        Nombre()

# ----------------------------------------


def Nombre():
    chiffreHexaBinaire()
    if Chiffre():
        nb = ord(SymboleCourant(1)) - 0x30
        SymboleSuivant(1)
        while Chiffre():
            nb = nb * 10 + ord(SymboleCourant(1)) - 0x30
            SymboleSuivant(1)
        codeCible.append("\t\tpush dword ptr " + str(nb))

# ----------------------------------------


def chiffreHexaBinaire():
    if SymboleCourant(2) in ["0b", "0x"]:
        if SymboleCourant(2) == "0b":
            SymboleSuivant(2)
            if chiffreBinaire():
                nb = SymboleCourant(1)
                SymboleSuivant(1)
                while chiffreBinaire():
                    nb = nb + SymboleCourant(1)
                    SymboleSuivant(1)
                nb = int(nb, 2)
                codeCible.append("\t\tpush dword ptr " + str(nb))
        elif SymboleCourant(2) == "0x":
            SymboleSuivant(2)
            if chiffreHexadecimal():
                nb = SymboleCourant(1)
                SymboleSuivant(1)
                while chiffreHexadecimal():
                    nb = nb + SymboleCourant(1)
                    SymboleSuivant(1)
                nb = int(str(nb), 16)
                codeCible.append("\t\tpush dword ptr " + str(nb))

# ----------------------------------------


def Reg():
    if SymboleCourant(1) in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return True
    else:
        return False
# ----------------------------------------


def Chiffre():
    if SymboleCourant(1) in "0123456789":
        return True
    else:
        return False
# ----------------------------------------


def chiffreHexadecimal():
    if SymboleCourant(1) in "0123456789abcdef":
        return True
    else:
        return False
# ----------------------------------------


def chiffreBinaire():
    if SymboleCourant(1) in "01":
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


programme = ("start "
                "ival = 2;"
                "sVal = (0b110010 | 9008 / (2 * 0xf)) + ival"
             "stop")
codeCible = []
posCourante = 0
VAR = []

if Prog():
    for c in codeCible:
        print(c)
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1), "à la " + str(posCourante + 1) + "e position est invalide!")