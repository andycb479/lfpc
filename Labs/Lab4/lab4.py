# Variant 7

# 1. For the given grammar G=(VN, VT, P, S,), VN ={S, A, B, C}, VT ={a,b,c},
# P={
# 1. S → aA
# 2. A → C
# 3. A → C b A
# 4. C → d B
# 5. B → b
# 6. B → a B },

# implement algorithm of simple precedence parsing and analyze the adbbdb string
# Bonus point: provide as an additional output the derivation tree.
import sys
from pprint import pprint

import regex as re
from anytree import Node, RenderTree

grammar = {
    "S": ["aA"],
    "A": ["C", "CbA"],
    "B": ["b", "aB"],
    "C": ["dB"],
}

nTerminals = ["S", "A", "B", "C"]
terminals = ["a", "b", "d"]
start = "S"


class NonTerminalNode:

    def __init__(self, name):
        self.name = name
        self.nodeList = []

    def __str__(self):
        return f"{self.name}"


class TerminalNode:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name} "

def init(nTerminals):
    first = dict()
    last = dict()

    for nTerminal in nTerminals:
        first[nTerminal] = list()
        last[nTerminal] = list()

    return first, last


def find_first_or_last_set(target, last=False, memo={}):
    if target in memo: return memo[target]

    if target.islower(): return list(target)

    searchSet = list()
    memo[target] = list()

    productions = grammar[target]

    for production in productions:
        char = production[-1] if last else production[0]

        searchSet.append(char)
        if char.isupper():
            searchSet.extend(find_first_or_last_set(char, last, memo))

    searchSet = list(set(searchSet))
    memo[target] = searchSet

    return searchSet


def find_first_sets(first):
    for nTerminal in first:
        first[nTerminal].extend(find_first_or_last_set(nTerminal))


def find_last_sets(last):
    for nTerminal in last:
        last[nTerminal].extend(find_first_or_last_set(nTerminal, last=True, memo={}))


def print_last_first(first, last):
    print("1. First & Last Table")
    print("\t{:<8} {:<20} {:<20}".format('NT', 'First', 'Last'))
    for key in first:
        print("\t{:<8} {:<20} {:<20}".format(key, str(first[key]), str(last[key])))


def find_equal_rule_relations(precedence_table):
    for key in grammar:
        for prod in grammar[key]:
            if len(prod) > 1:
                for index, char in enumerate(prod):
                    if index + 1 < len(prod): precedence_table[char + "," + prod[index + 1]] = "="


def add_less_rule_to_table(precedence_table, matches, first):
    for match in matches:
        for right in first[match[1]]:
            precedence_table[match[0] + "," + right] = "<"


def find_less_rule_relations(precedence_table, first):
    for key in grammar:
        for prod in grammar[key]:
            if len(prod) > 1:
                matches = re.findall('([a-zA-Z][A-Z])', prod, overlapped=True)
                add_less_rule_to_table(precedence_table, matches, first)


def add_less_rule_one_to_table(precedence_table, matches, last):
    for match in matches:
        for left in last[match[0]]:
            precedence_table[left + "," + match[1]] = ">"


def add_less_rule_two_to_table(precedence_table, matches, first, last):
    for match in matches:
        for left in last[match[0]]:
            for right in first[match[1]]:
                if (right.islower()):
                    precedence_table[left + "," + right] = ">"


def find_greater_rule_relations(precedence_table, first, last):
    for key in grammar:
        for prod in grammar[key]:
            if len(prod) > 1:
                matche_rule_one = re.findall('([A-Z][a-z])', prod, overlapped=True)
                matche_rule_two = re.findall('([A-Z][A-Z])', prod, overlapped=True)
                if (matche_rule_one):
                    add_less_rule_one_to_table(precedence_table, matche_rule_one, last)
                if (matche_rule_two):
                    add_less_rule_two_to_table(precedence_table, matche_rule_two, first, last)


def compute_precedence_table(first, last):
    precedence_table = dict()
    find_equal_rule_relations(precedence_table)
    find_less_rule_relations(precedence_table, first)
    find_greater_rule_relations(precedence_table, first, last)
    return precedence_table


def assemble_precedence_table():
    first, last = init(nTerminals)
    find_first_sets(first)
    find_last_sets(last)
    print_last_first(first, last)
    precedence_table = compute_precedence_table(first, last)
    for char in nTerminals + terminals:
        precedence_table["$," + char] = "<"
        precedence_table[char + ",$"] = ">"
    print("2. Precedence Table\n", precedence_table)
    return precedence_table


def find_char_relations(input, precedence_table):
    new_input = input

    scale = 1

    for index, char in enumerate(input):
        if index + 1 < len(input):
            if (char.isalpha() and input[index + 1].isalpha()) or (char == "$" and input[index + 1].isalpha()) or (
                    char.isalpha() and input[index + 1] == "$"):
                try:
                    new_input = new_input[:index + scale] + precedence_table[char + "," + input[index + 1]] + new_input[
                                                                                                              index + scale:]
                    scale += 1
                except:
                    print("Invalid Input")
                    sys.exit(1)
    return new_input


def invertGrammar():
    new_grammar = dict()

    for key in grammar:
        for prod in grammar[key]:
            new_grammar[prod] = key

    return new_grammar

def stringTree(node, level):
    res = ""
    if not isinstance(node, NonTerminalNode):
        return "  " * level + str(node) + "\n"

    for child in node.nodeList:
        res = "  " * level + str(node) + "\n"
        for child in node.nodeList:
            res += stringTree(child, level + 1)
        return res

# Parse Tree with Python Objects
# def find_tree_rec(target,input_list,index,precedence_table):
#
#     root = NonTerminalNode(target)
#
#     matches = re.findall('[<][a-zA-Z=]+[>]', input_list[index], overlapped=True)
#     if not matches:
#         while not matches:
#             index += 1
#             matches = re.findall('[<][a-zA-Z=]+[>]', input_list[index], overlapped=True)
#     start_index = input_list[index].index(matches[0])
#
#
#     current = input_list[index][start_index+1:start_index+len(matches[0])-1]
#     current = current[::-1]
#     input_list[index] = input_list[index].replace(matches[0], "")
#
#     for char in current:
#         if not char.isalpha():
#             continue
#         if char.isupper():
#             root.nodeList.append(find_tree_rec(char,input_list,index+1,precedence_table))
#         elif char.islower():
#             root.nodeList.append(TerminalNode(char))
#
#     return root

def find_tree_rec(target,input_list,index,root):

    matches = re.findall('[<][a-zA-Z=]+[>]', input_list[index], overlapped=True)
    if not matches:
        while not matches:
            index += 1
            matches = re.findall('[<][a-zA-Z=]+[>]', input_list[index], overlapped=True)
    start_index = input_list[index].index(matches[0])


    current = input_list[index][start_index+1:start_index+len(matches[0])-1]
    current = current[::-1]
    input_list[index] = input_list[index].replace(matches[0], "")

    for char in current:
        if not char.isalpha():
            continue
        if char.isupper():
            node = Node(char,parent=root)
            find_tree_rec(char,input_list,index+1,node)
        elif char.islower():
            node = Node(char, parent=root)

    return root


def main():
    input = "adbbdb"
    precedence_table = assemble_precedence_table()

    input = "$ $".replace(" ", input)
    print("3. Parsing of input\n"+"Input = ", input)

    invertedGrammar = invertGrammar()

    input = find_char_relations(input, precedence_table)

    input_list = list()
    input_list.append(input)

    while input != "$<S>$":
        matches = re.findall('[<][a-zA-Z=]+[>]', input, overlapped=True)
        current = matches[0].replace("<", "").replace(">", "").replace("=", "")
        try:
            input = input.replace(matches[0], invertedGrammar[current],1)
        except:
            print("Invalid Input")
            sys.exit(1)

        input = find_char_relations(input, precedence_table)
        input_list.append(input)

    input_list.reverse()

    pprint(input_list)

    parseTree = find_tree_rec("S",input_list,1, Node("S"))
    print("4. Derivation Tree")
    for pre, fill, node in RenderTree(parseTree):
        print("%s%s" % (pre, node.name))

main()
