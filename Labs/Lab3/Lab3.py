# Variant 26
# 1.Eliminate ε productions.
# 2.Eliminate any renaming.
#  3.Eliminate inaccessible symbols.
#  4. Eliminate the non productive symbols.
#  5. Obtain the Chomsky Normal Form.
# G=(VN, VT, P, S) VN={S, A, B, D} VT={a, b, d}
# P={
# S->aBA | AB
# A->d | dS | AbBA | ε
# B->a | aS | A |
# D->Aba}
import itertools
import string
from pprint import pprint


initGrammar = {
    "S": ["aBA", "AB"],
    "A": ["d", "dS", "AbBA", "@"],
    "B": ["a", "aS", "A"],
    "D": ["Aba"],
}


def removeMultipleEmpty(production, ntSet):
    ret = []

    nonTerminalsCount = 0

    for nt in ntSet:
        nonTerminalsCount += production.count(nt)

    lst = list(map(list, itertools.product([0, 1], repeat=nonTerminalsCount)))
    lst.pop()
    for i, combination, in enumerate(lst):
        temp = ""
        elementCount = 0
        for char in production:
            if char in ntSet and combination[elementCount]:
                temp += char
                elementCount += 1
            elif char in ntSet:
                elementCount += 1
            elif char not in ntSet:
                temp += char
        # check if string is not empty
        if temp: ret.append(temp)
    return ret


def removeEmpty(grammar, empty):
    emptyNonTerminals = ""
    emptyNonTerminals = emptyNonTerminals.join(empty)
    for key in grammar:
        temp = list()
        for production in grammar[key]:
            emptyInProduction = [nt for nt in emptyNonTerminals if (nt in production)]
            if emptyInProduction and not len(emptyInProduction) > 1 and len(production) > 1:
                afterReplace = production.replace(emptyInProduction[0], "")
                if not grammar[key].__contains__(afterReplace):  # check for dublicates in the list before adding
                    grammar[key].append(afterReplace)
            elif emptyInProduction and len(production) > 1:
                temp += removeMultipleEmpty(production, emptyInProduction)
        grammar[key].extend(set(temp) - set(grammar[key]))


def checkEmpty(grammar):
    empty = set()
    for key in grammar:
        for production in grammar[key]:
            if production == "@":
                empty.add(key)
                grammar[key].remove(production)
    flag = True
    while flag:
        flag = False
        for key in grammar:
            for production in grammar[key]:
                emptyInProduction = [nt for nt in empty if (nt in production)]
                if emptyInProduction and key not in empty and len(production) == len(emptyInProduction):
                    empty.add(key)
                    flag = True
    return empty


def checkForMultipleUnitProductions(unitProductions, key):
    if not unitProductions[key][0] in unitProductions:
        return unitProductions[key][0]
    return checkForMultipleUnitProductions(unitProductions, unitProductions[key][0])


def getUnitProductions(grammar):
    unitProductions = {}
    for key in grammar:
        temp = []
        for production in grammar[key]:
            if len(production) == 1 and production.isupper():
                temp.append(production)
        if temp:
            unitProductions[key] = temp

    for key in unitProductions:
        temp = checkForMultipleUnitProductions(unitProductions, key)
        if temp and temp != key and temp not in unitProductions[key]:
            unitProductions[key].extend(temp)

    # remove unit productions
    for key in unitProductions:
        for production in unitProductions[key]:
            if grammar[key].__contains__(production):
                grammar[key].remove(production)


    return unitProductions


def removeRenaiming(grammar):
    unitProductions = getUnitProductions(grammar)
    print("Unit Productions = ", unitProductions)
    for key in unitProductions:
        for production in unitProductions[key]:
            grammar[key].extend(set(grammar[production]) - set(grammar[key]))


def getNonProductiveSymbols(grammar):
    nonTerminals = set(grammar.keys())
    productiveSymbols = set()
    for key in grammar:
        if any(production.islower() for production in grammar[key]):
            productiveSymbols.add(key)

    # if a NonTerminal has as productions 2 NonTerminals that can be productive or not productive
    temp = nonTerminals.difference(productiveSymbols)
    temp2 = {""}
    for key in grammar:
        for production in grammar[key]:
            for productive in productiveSymbols:
                if production.__contains__(productive):
                    for nonProductive in temp:
                        if not production.__contains__(nonProductive):
                            temp2.add(key)

    productiveSymbols |= (temp2)

    return list(nonTerminals.difference(productiveSymbols))


def removeNonProductive(grammar):
    nonProductiveSymbols = getNonProductiveSymbols(grammar)
    print("Non Productive Set = ", nonProductiveSymbols)
    if not nonProductiveSymbols:
        return
    for key in grammar:
        for production in grammar[key]:
            for nonProductive in nonProductiveSymbols:
                if production.__contains__(nonProductive):
                    grammar[key].remove(production)


def checkAccesible(grammar, start, accessible):
    if start != "S":
        if start in accessible:
            return
        elif start not in accessible:
            accessible.extend(start)

    for production in grammar[start]:
        for char in production:
            if char.isupper() and char != start and char not in accessible:
                checkAccesible(grammar, char, accessible)

    return accessible


def removeNonAccesible(grammar):
    nonTerminals = set(grammar.keys())
    accesible = ["S"]
    checkAccesible(grammar, "S", accesible)
    nonAccesible = set(nonTerminals) - set(accesible)
    print("Non Accesible = ", nonAccesible)
    for key in nonAccesible:
        grammar.pop(key)


def replaceTerminals(grammar, dictionaryOfReplaces, alphabet):
    for key in grammar:
        newList = list()
        for production in grammar[key]:
            if len(production) > 1 and not production.isupper():
                changed = production
                for char in production:
                    if char.islower() and char not in dictionaryOfReplaces:
                        dictionaryOfReplaces[char] = alphabet[-1]
                        changed = changed.replace(char, alphabet[-1])
                        alphabet.pop()
                    elif char.islower():
                        changed = changed.replace(char, dictionaryOfReplaces[char])
                newList.append(changed)
            else:
                newList.append(production)
        grammar[key] = newList


def divideProduction(grammar, production, dictionaryOfReplaces, alphabet):
    changed = production
    chunks = [production[i:i + 2] for i in range(0, len(production), 2)]
    if len(chunks) <= 4:
        for prod in chunks:
            if prod not in dictionaryOfReplaces:
                if len(prod) % 2 == 0:
                    temp = alphabet[-1]
                    dictionaryOfReplaces[prod] = temp
                    changed = changed.replace(prod, temp)
                    alphabet.pop()
            elif prod in dictionaryOfReplaces:
                changed = changed.replace(prod, dictionaryOfReplaces[prod])
    return changed


def divideNonTerminals(grammar, dictionaryOfReplaces, alphabet):
    for key in grammar:
        newList = list()
        for production in grammar[key]:
            if len(production) in [1, 2]:
                newList.append(production)
            else:
                newList.append(divideProduction(grammar, production, dictionaryOfReplaces, alphabet))
        grammar[key] = newList


def normalizeToChomsky(grammar):
    dictionaryOfReplaces = dict()
    alphabet = list(set(string.ascii_uppercase) - set(grammar.keys()))
    alphabet.sort(reverse=True)
    replaceTerminals(grammar, dictionaryOfReplaces, alphabet)
    print("Chomsky Normalization Step 1: Replace terminals with NonTerminals ->\n", grammar)
    divideNonTerminals(grammar, dictionaryOfReplaces, alphabet)
    print("Chomsky Normalization Step 2: Replace chunks with NonTerminals ->\n", grammar)
    newDict = dict()
    for key in dictionaryOfReplaces:
        newDict[dictionaryOfReplaces[key]] = [key]
    grammar.update(newDict)


def checkForDirectLeftRecursion(grammar):
    keys = list()
    for key in grammar:
        for production in grammar[key]:
            if production[0] == key:
                keys.append(key)
    return keys


def checkProductionHead(grammar, key, head, prevkey):

    if head.islower():
        return
    if key == head:
        return prevkey
    for production in grammar[head]:
        if production[0].isupper():
            if production[0] == head:
                return
            if production[0] == prevkey == key:
                return head
            elif production[0] == prevkey:
                return
            temp = checkProductionHead(grammar, key, production[0], head)
            if temp:
                return temp





def checkForIndirectLeftRecursion(grammar):

    for key in grammar:
        for production in grammar[key]:
            if production[0].isupper():
                temp = checkProductionHead(grammar, key, production[0],key)
                if temp and temp != key:
                    newlist = list()
                    for prod in grammar[temp]:#replace with all productions
                        newlist.append(prod+production[1:])
                    grammar[key].extend(newlist)
                    if grammar[key].__contains__(production):
                        grammar[key].remove(production)




def removeDirectLeftRecursion(grammar,keys):

    alphabet = list(set(string.ascii_uppercase) - set(grammar.keys()))
    alphabet.sort(reverse=True)

    for key in keys:
        alphas = list()
        betas = list()
        replaceKey = alphabet[0]
        newProductions = (list(),list())
        productions = grammar[key]
        for production in productions:
            if production[0] == key:#alphas
                newProductions[0].extend((production[1:], production[1:] + replaceKey))
            else:#betas
                newProductions[1].extend((production, production+replaceKey))

        grammar[replaceKey] = newProductions[0]
        grammar[key] = newProductions[1]
        alphabet.pop(0)


def replaceNTtoT(grammar):
    flag = True
    while flag:
        flag = False
        for key in grammar:
            newList = list()
            for production in grammar[key]:
                if production[0].isupper():
                    if all(i[0].islower() for i in grammar[production[0]]):
                        for innerProd in grammar[production[0]]:
                            if innerProd.islower():
                                changed = production.replace(production[0],innerProd)
                                newList.append(changed)
                                flag = True
                            elif innerProd[0].islower():
                                newList.append(innerProd+production[1:])
                                flag = True
                    else:
                        newList.append(production)

                else:
                    newList.append(production)
            grammar[key] = newList
        print(grammar)




def normalizeToGreibach(grammar):

    print("Transform indirect left recursion to direct left recursion")
    checkForIndirectLeftRecursion(grammar)
    print(grammar)
    directLeftRecursionKeys = checkForDirectLeftRecursion(grammar)
    print("Direct Left Recursion NonTerminals =", list(set(directLeftRecursionKeys)), "Remove ->")
    removeDirectLeftRecursion(grammar, list(set(directLeftRecursionKeys)))
    print(grammar)
    print("Replace first NonTerminal with productions that have first char a terminal ->")
    replaceNTtoT(grammar)
    print(grammar)






def transformGrammar(grammar):
    print("Initial Grammar ->\n", grammar)
    emptySet = checkEmpty(grammar)
    print("Empty set = ", emptySet)
    print("Removed direct empty transitions ->\n", grammar)
    removeEmpty(grammar, emptySet)
    print("New Transitions for empty replace ->\n", grammar)
    removeRenaiming(grammar)
    print("New Tranistions for direct acces to productions ->\n", grammar)
    removeNonProductive(grammar)
    print("Removed NonProductive NonTerminals ->\n", grammar)
    removeNonAccesible(grammar)
    print("Removed NonAccesible NonTerminals ->\n", grammar)
    normalizeToChomsky(grammar)
    print("Chomsky Normalization Step 3: Add new transitions ->\n", grammar)
    normalizeToGreibach(grammar)
    removeNonAccesible(grammar)
    print("Removed NonAccesible NonTerminals ->\n", grammar)
    # print("Greibach Normalization Step 1: Replace first nonterminals with a terminal ->\n", grammar)

testGrammarGreibach = {

    "S": ["AC"],
    "C": ["a"],
    "B": ["aA", "BC",],
    "A": ["b", "SB"]

}
testChomsky = {
    "S": ["SC","SA","ab"],
    "C":["c"],
    "A": ["b"]
}

testGrammarGreibach3 = {

    "S": ["AC"],
    "C": ["a"],
    "B": ["aA", "BC","Ba"],
    "A": ["b", "B"]

}

testGrammarGreibach2 = {
    "S": ["AB"],
    "B": ["c"],
    "D": ["a"],
    "G": ["AD",],
    "A": ["GB", "a"]
}
transformGrammar(initGrammar)
#transformGrammar(testChomsky)
#transformGrammar(testGrammarGreibach)
#normalizeToGreibach(testGrammarGreibach2)
# normalizeToGreibach(testGrammarGreibach)