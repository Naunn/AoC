from aocd import get_data
import yaml
import numpy as np


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_ten = get_data(session=S, day=10, year=2021)

syntax_ = day_ten.split('\n')

# {([(<{}[<>[]}>{[]{[(<()> drop {}, <>, [], [], ()
# {([(<[}>{{[(<> drop <>
# {([(<[}>{{[( found [}

# [[<[([]))<([[{}[[()]]] drop [], {}, ()
# [[<[())<([[[[]]] drop (), []
# [[<[)<([[[]] drop []
# [[<[)<([[] drop []
# [[<[)<([ found [)

# [{[{(]}([{[{{}([] drop {}, {}, {}
# [{[{(]}([{[{{}([] drop {}, []
# [{[{(]}([{[{( found (]

# [<(<(<(<{}))><([]([]() drop {}, [], [], ()
# [<(<(<(<))><(( found <)
                  
# <{([([[(<>()){}]>(<<{{ drop <>, (), {}
# <{([([[()]>(<<{{ drop ()
# <{([([[]>(<<{{ drop []
# <{([([>(<<{{ found [>

# Utowrzyc 3 tablice:
# pairs = ['()','[]','{}','<>']
# left_wing = ['(','[','{','<']
# right_wing =  [')',']','}','>']

# notatki:
# Przechodzac po kolejnych parach elementow sprawdzac czy znajduje sie w pairs i wyrzucic
# Powtarzac az do braku zmiany ilosci znakow w liscie
# Sprawdzic czy jak znajdziemy znak w left_wing, to czy jego sasiad z prawej jest w right_wing
# potrzeba bedzie jakos je ponumerowac
# zapewnienie, ze to nie bedzie para zapewnia nam wyrzucenie par w pierwszym kroku

tst = [
       '[({(<(())[]>[[{[]{<()<>>',
       '[(()[<>])]({[<{<<[]>>(',
       '{([(<{}[<>[]}>{[]{[(<()>',
       '(((({<>}<{<{<>}{[]{[]{}',
       '[[<[([]))<([[{}[[()]]]',
       '[{[{({}]{}}([{[{{{}}([]',
       '{<[[]]>}<{[{[{[]{()[[[]',
       '[<(<(<(<{}))><([]([]()',
       '<{([([[(<>()){}]>(<<{{',
       '<{([{{}}[<[[[<>{}]]]>[]]',
       ]

def corrupted(syntax: list):
    pairs = ['()','[]','{}','<>']
    right_wing =  [')',']','}','>']
    dict_ = {')': 3,
             ']': 57,
             '}': 1197,
             '>': 25137}
    crptd = []
    score = 0
    
    # Pick string from list of strings and convert it to list of chars using list()
    for k in range(len(syntax)):
        temp = list(syntax[k]) # temporary list (will be overwirited every iteration)
        j = [] # list of founded pairs
        
        # Iter through list of characters
        for iter in np.arange(len(temp)/2)+1: # length is enough to iterate multiple times
            
            # If list of pairs is none empty then pop pairs from list
            if len(j) > 0:
                for _ in sorted(j, reverse = True):
                    temp.pop(_)
                j = []
            else:
                # check if next two characters match any pair
                for i in range(len(temp)-1):
                    if temp[i]+temp[i+1] in pairs:
                        j.append(i)
                        j.append(i+1)
        
        # After removing all pairs, check if any right_wing sign occurs,
        # which indicate that there is an inappropriate match.
        for t in temp:
            if t in right_wing:
                crptd.append(t)
                break
    
    # count the score of founded mismatches by using dictionary values         
    for n in crptd:
        score += dict_[n]
    return score

corrupted(tst) # 26397 - good

print("The total syntax error score for those errors is:", corrupted(syntax_))

# Incomplete lines don't have any incorrect characters!
# [({(<(())[]>[[{[]{<()<>> drop (), [], [], (), <>
# [({(<()>[[{{<> drop (), <>
# [({(<>[[{{ drop <>
# [({([[{{ found }}]])})]

# [(()[<>])]({[<{<<[]>>( drop (), <>, []
# [([])]({[<{<<>>( drop [], <>
# [()]({[<{<>( drop (), <>
# []({[<{( drop []
# ({[<{( found )}>]})

# (((({<>}<{<{<>}{[]{[]{} drop <>, <>, [], [], {}
# (((({}<{<{}{{ drop {}, {}
# ((((<{<{{ found }}>}>))))

# {<[[]]>}<{[{[{[]{()[[[] drop [], [], (), []
# {<[]>}<{[{[{{[[ drop []
# {<>}<{[{[{{[[ drop <>
# {}<{[{[{{[[ drop {}
# <{[{[{{[[ found ]]}}]}]}>

# <{([{{}}[<[[[<>{}]]]>[]] drop {}, <>, {}, []
# <{([{}[<[[[]]]>] drop {}, []
# <{([[<[[]]>] drop []
# <{([[<[]>] drop []
# <{([[<>] drop <>
# <{([[] drop []
# <{([ found ])}>

# notatki:
# Dodac warunek do corrupted(), ktory nie sprawdza list "corrupted-owych"
# Usuwac pary analogicznie jak w corrupted()
# w incomplete nie sprawdzamy list gdzie wystepuja domkniecia nie do pary
# Utowrzyc dwa sloniki z pasujacymi wartosciami
# dopasowac lewe domkniecia do prawych po slownikach
# wykorzystac trzeci slownik zeby zliczyc wynik
    
def incomplete(syntax: list):
    pairs = ['()','[]','{}','<>']
    right_wing =  [')',']','}','>']
    right_wing_dict = {'(': ')',
                       '[': ']',
                       '{': '}',
                       '<': '>'}
    score_dict = {')': 1,
                  ']': 2,
                  '}': 3,
                  '>': 4}
    incmplt = []
    
    # Pick string from list of strings and convert it to list of chars using list()
    for k in range(len(syntax)):
        temp = list(syntax[k]) # temporary list (will be overwirited every iteration)
        j = [] # list of founded pairs
        
        # Iter through list of characters
        for iter in np.arange(len(temp)/2)+1: # length is enough to iterate multiple times
            
            # If list of pairs is none empty then pop pairs from list
            if len(j) > 0:
                for _ in sorted(j, reverse = True):
                    temp.pop(_)
                j = []
            else:
                # check if next two characters match any pair
                for i in range(len(temp)-1):
                    if temp[i]+temp[i+1] in pairs:
                        j.append(i)
                        j.append(i+1)
        
        # After removing all pairs, iterate through temp and count scores
        score = 0
        for t in temp[::-1]: # Remember to reverse order
            if t not in right_wing:
                score = score*5 + score_dict[right_wing_dict[t]]
            # In case of occuring corrupted pair, set score to 0 and break loop
            else:
                score = 0
                break
        
        incmplt.append(score)
        
    # Make sure to remove 0 values and return middle value
    final = sorted([_ for _ in incmplt if _ > 0])
    return final[int(len(final)/2)]

incomplete(tst)

print('The middle score is:', incomplete(syntax_))
