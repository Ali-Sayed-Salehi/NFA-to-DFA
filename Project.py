# import the required modules
import json
import PySimpleAutomata
from PySimpleAutomata import automata_IO
from PySimpleAutomata import NFA
from PySimpleAutomata import DFA
from tabulate import tabulate

# open the file in read-only mode
with open('given_transition_table.txt', 'r') as f:
    # read the entire file as a single string
    text = f.read()

# split the string into a list of words
words = text.split()


states = list()
accepting_states = list()
initial_state = list()
transitions = list()
#transitionsDict = dict()


i = 0
while True:
    if i > len(words) - 1:
        break
    else:
        if '*' in words[i]:
            words[i] = words[i].replace('*', '')
            accepting_states.append(words[i])
        if '->' in words[i]:
            words[i] = words[i].replace('->', '')
            initial_state.append(words[i])
            #initialState = words[i]

        if words[i+1] != "phi":
            words[i + 1] = words[i + 1].replace('}', '')
            words[i + 1] = words[i + 1].replace('{', '')
            destinationStates_zero = words[i + 1].split(",")
            for j in destinationStates_zero:
                transitions.append([words[i], "0", j])
                #transitionsDict[("words[i]", "0")] = {"words[i+1]"}

        if words[i+2] != "phi":
            words[i + 2] = words[i + 2].replace('}', '')
            words[i + 2] = words[i + 2].replace('{', '')
            destinationStates_one = words[i + 2].split(",")
            for j in destinationStates_one:
                transitions.append([words[i], "1", j])
                #transitionsDict[("words[i]", "1")] = {"words[i+2]"}

        states.append(words[i])
        i += 3



givenTable = {
    "alphabet": ["0", "1"],
    "states": states,
    "initial_states": initial_state,
    "accepting_states": accepting_states,
    "transitions": transitions
}


# open the file in write mode
with open('givenTable.json', 'w') as g:
    # write the data to the file as JSON
    json.dump(givenTable, g)

# json to NFA
NFA_fromTable = PySimpleAutomata.automata_IO.nfa_json_importer("givenTable.json")

# NFA to DFA
DFA_fromTable = PySimpleAutomata.NFA.nfa_determinization(NFA_fromTable)

# DFA to json
PySimpleAutomata.automata_IO.dfa_to_json(DFA_fromTable, "result_DFA", "./")

# DFA to DOT file
PySimpleAutomata.automata_IO.dfa_to_dot(DFA_fromTable, "result_DFA", "./")

# DFA to table
with open('result_DFA.json', 'r') as h:
  DFA_Dict = json.load(h)


transitionsList = DFA_Dict["transitions"]
statesList = DFA_Dict["states"]
tableRow = list()
transitionsList = DFA_Dict["transitions"]
appectingStatesList = DFA_Dict["accepting_states"]
initialState = DFA_Dict["initial_state"]


with open('DFA_transition_table_result.txt', 'w') as k:
    # read the entire file as a single string

    k.write(tabulate(transitionsList, headers = ["start state", "transition", "end state"]))

    k.write("\n\naccepting_states\n")
    k.write(str(appectingStatesList))

    k.write("\ninitial_state\n")
    k.write(initialState)



