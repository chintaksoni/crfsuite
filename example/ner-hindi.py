#!/usr/bin/env python

"""
A feature extractor for named eneity recognition (NER).
Copyright 2010,2011 Naoaki Okazaki.
"""

days = {}
def prepareDict_days():
    f = open('days.txt','r')
    all_lines = f.readlines()
    for line in all_lines:
        name = (line.split())[0]
        days[name]=1

months = {}
def prepareDict_months():
    f = open('months.txt','r')
    all_lines = f.readlines()
    for line in all_lines:
        name = (line.split())[0]
        months[name]=1

money = {}
def prepareDict_money():
    f = open('money.txt','r')
    all_lines = f.readlines()
    for line in all_lines:
        name = (line.split())[0]
        money[name]=1


# Separator of field values.
separator = ' '

# Field names of the input data.
fields = 'y w pos chk'


import crfutils

#print "OK"
def get_shape(token):
#    print "1 call"
    r = ''
    for c in token:
        if c.isupper():
            r += 'U'
        elif c.islower():
            r += 'L'
        elif c.isdigit():
            r += 'D'
        elif c in ('.', ','):
            r += '.'
        elif c in (';', ':', '?', '!'):
            r += ';'
        elif c in ('+', '-', '*', '/', '=', '|', '_'):
            r += '-'
        elif c in ('(', '{', '[', '<'):
            r += '('
        elif c in (')', '}', ']', '>'):
            r += ')'
        else:
            r += c
    return r

def degenerate(src):
    dst = ''
    for c in src:
        if not dst or dst[-1] != c:
            dst += c
    return dst
'''
def get_type(token):
    T = (
        'AllUpper', 'AllDigit', 'AllSymbol',
        'AllUpperDigit', 'AllUpperSymbol', 'AllDigitSymbol',
        'AllUpperDigitSymbol',
        'InitUpper',
        'AllLetter',
        'AllAlnum',
        )
    R = set(T)
    if not token:
        return 'EMPTY'

    for i in range(len(token)):
        c = token[i]
        if c.isupper():
            R.discard('AllDigit')
            R.discard('AllSymbol')
            R.discard('AllDigitSymbol')
        elif c.isdigit() or c in (',', '.'):
            R.discard('AllUpper')
            R.discard('AllSymbol')
            R.discard('AllUpperSymbol')
            R.discard('AllLetter')
        elif c.islower():
            R.discard('AllUpper')
            R.discard('AllDigit')
            R.discard('AllSymbol')
            R.discard('AllUpperDigit')
            R.discard('AllUpperSymbol')
            R.discard('AllDigitSymbol')
            R.discard('AllUpperDigitSymbol')
        else:
            R.discard('AllUpper')
            R.discard('AllDigit')
            R.discard('AllUpperDigit')
            R.discard('AllLetter')
            R.discard('AllAlnum')

        if i == 0 and not c.isupper():
            R.discard('InitUpper')

    for tag in T:
        if tag in R:
            return tag
    return 'NO'
'''

def get_2d(token):
    return len(token) == 2 and token.isdigit()

def get_4d(token):
    return len(token) == 4 and token.isdigit()
'''
def get_da(token):
    bd = False
    ba = False
    for c in token:
        if c.isdigit():
            bd = True
        elif c.isalpha():
            ba = True
        else:
            return False
    return bd and ba
'''

def get_dand(token, p):
    bd = False
    bdd = False
    for c in token:
        if c.isdigit():
            bd = True
        elif c == p:
            bdd = True
        else:
            return False
    return bd and bdd

def get_all_other(token):
    for c in token:
        if c.isalnum():
            return False
    return True
'''
def get_capperiod(token):
    return len(token) == 2 and token[0].isupper() and token[1] == '.'
'''
# my feature function
def get_appos(token):
    if len(token) == 2 and token[0] == '\'' and token[1] == 's':
        return True
    else:
        return False
'''
def contains_upper(token):
    b = False
    for c in token:
        b |= c.isupper()
    return b

def contains_lower(token):
    b = False
    for c in token:
        b |= c.islower()
    return b

def contains_alpha(token):
    b = False
    for c in token:
        b |= c.isalpha()
    return b
'''
def contains_digit(token):
    b = False
    for c in token:
        b |= c.isdigit()
    return b

def contains_symbol(token):
    b = False
    for c in token:
        b |= ~c.isalnum()
    return b

# new feature $
def contains_dollar(token):
    if'$' in token:
        return True
    else:
        return False

# new feature :
def contains_collen(token):
    if':' in token:
        return True
    else:
        return False

# new feature &
def contains_and(token):
    if'&' in token:
        return True
    else:
        return False

# new feature Rs
def contains_rupees(token):
    if'rs' in token:
        return True
    else:
        return False

# new feature ji
def contains_ji(token):
    if'जी' in token:
        return True
    else:
        return False


# new feature baje
def contains_baje(token):
    if'बजे' in token:
        return True
    else:
        return False


# pos tag = 'NNP'
def get_NNP(token):
    if 'NNP' in token:
        return True
    else:
        return False

# pos tag = 'NNPC'
def get_NNPC(token):
    if 'NNPC' in token:
        return True
    else:
        return False

# pos tag = 'NNC'
def get_NNC(token):
    if 'NNC' in token:
        return True
    else:
        return False

# pos tag = 'QC'
def get_QC(token):
    if 'QC' in token:
        return True
    else:
        return False
	

def b(v):
    return 'yes' if v else 'no'

def observation(v, defval=''):
    # Lowercased token.
    v['wl'] = v['w'].lower()
    # Token shape.
    v['shape'] = get_shape(v['w'])
    # Token shape degenerated.
    v['shaped'] = degenerate(v['shape'])
    # Token type.
#    v['type'] = get_type(v['w'])

    # Prefixes (length between one to four).
    v['p1'] = v['w'][0] if len(v['w']) >= 1 else defval
    v['p2'] = v['w'][:2] if len(v['w']) >= 2 else defval
    v['p3'] = v['w'][:3] if len(v['w']) >= 3 else defval
    v['p4'] = v['w'][:4] if len(v['w']) >= 4 else defval

    # Suffixes (length between one to four).
    v['s1'] = v['w'][-1] if len(v['w']) >= 1 else defval
    v['s2'] = v['w'][-2:] if len(v['w']) >= 2 else defval
    v['s3'] = v['w'][-3:] if len(v['w']) >= 3 else defval
    v['s4'] = v['w'][-4:] if len(v['w']) >= 4 else defval

    # Two digits
    v['2d'] = b(get_2d(v['w']))
    # Four digits.
    v['4d'] = b(get_4d(v['w']))
    # Alphanumeric token.
#    v['d&a'] = b(get_da(v['w']))
    # Digits and '-'.
    v['d&-'] = b(get_dand(v['w'], '-'))
    # Digits and '/'.
    v['d&/'] = b(get_dand(v['w'], '/'))
    # Digits and ','.
    v['d&,'] = b(get_dand(v['w'], ','))
    # Digits and '.'.
    v['d&.'] = b(get_dand(v['w'], '.'))
    # A uppercase letter followed by '.'
#    v['up'] = b(get_capperiod(v['w']))

    # For 's 
    v['as'] = b(get_appos(v['w']))

    # An initial uppercase letter.
#   v['iu'] = b(v['w'] and v['w'][0].isupper())
    # All uppercase letters.
#    v['au'] = b(v['w'].isupper())
    # All lowercase letters.
#    v['al'] = b(v['w'].islower())
    # All digit letters.
    v['ad'] = b(v['w'].isdigit())
    # All other (non-alphanumeric) letters.
    v['ao'] = b(get_all_other(v['w']))

    # Contains a uppercase letter.
#    v['cu'] = b(contains_upper(v['w']))
    # Contains a lowercase letter.
#    v['cl'] = b(contains_lower(v['w']))
    # Contains a alphabet letter.
#    v['ca'] = b(contains_alpha(v['w']))
    # Contains a digit.
    v['cd'] = b(contains_digit(v['w']))
    # Contains a symbol.
    v['cs'] = b(contains_symbol(v['w']))

    # Contains $ as symbol
    v['do'] = b(contains_dollar(v['w'])) 
    # Contains Rs as symbol
    v['rs'] = b(contains_rupees(v['w']))
    # Contains : as symbol
    v['col'] = b(contains_collen(v['w']))
    # Contains & as symbol
    v['and'] = b(contains_and(v['w']))
    # Contains जी 
    v['ji'] = b(contains_ji(v['w']))
    # Contains बजे
    v['baje'] = b(contains_baje(v['w']))

    # Get Pos = NNP
    v['nnp'] = b(get_NNP(v['pos']))
    # Get Pos = NNC
    v['nnc'] = b(get_NNC(v['pos']))
    # Get Pos = NNPC
    v['nnpc'] = b(get_NNC(v['pos']))
    # Get Pos = NNP
    v['qc'] = b(get_QC(v['pos']))

    # gazzater for days
    v['gaz-d'] = '0'    
    if v['w'] in days:
        v['gaz-d'] = '1'

    # gazzater for months
    v['gaz-m'] = '0'    
    if v['w'] in months:
        v['gaz-m'] = '1'

    # gazzater for money
    v['gaz-m'] = '0'    
    if v['w'] in money:
        v['gaz-m'] = '1'



def disjunctive(X, t, field, begin, end):
    name = '%s[%d..%d]' % (field, begin, end)
    for offset in range(begin, end+1):
        p = t + offset
        if p not in range(0, len(X)):
            continue
        X[t]['F'].append('%s=%s' % (name, X[p][field]))

U = [
    'w', 'wl', 'pos', 'chk', 'shape', 'shaped',
    'p1', 'p2', 'p3', 'p4',
    's1', 's2', 's3', 's4',
    '2d', '4d', 'd&-', 'd&/', 'd&,', 'd&.',
    'ad', 'ao',
    'cd', 'cs',
    'as','do','rs','nnp','nnc','qc','nnpc',
    'col','and','ji','baje',
    'gaz-d','gaz-m','gaz-l','gaz-a','gaz-m','gaz-e','gaz-lt','gaz-p','gaz-lm'
    ]
B = ['w', 'pos', 'chk', 'shaped']

templates = []
for name in U:
    templates += [((name, i),) for i in range(-2, 3)]
for name in B:
    templates += [((name, i), (name, i+1)) for i in range(-2, 2)]

def feature_extractor(X):
#    print "in feature_extractor"
    # Append observations.
    for x in X:
        observation(x)

    # Apply the feature templates.
    crfutils.apply_templates(X, templates)

    # Append disjunctive features.
    for t in range(len(X)):
        disjunctive(X, t, 'w', -4, -1)
        disjunctive(X, t, 'w', 1, 4)

    # Append BOS and EOS features.
    if X:
        X[0]['F'].append('__BOS__')
        X[-1]['F'].append('__EOS__')

if __name__ == '__main__':
    prepareDict_days()
    prepareDict_months()
    prepareDict_locations()
    prepareDict_artifacts()
    prepareDict_money()
    prepareDict_entertainment()
    prepareDict_livingthings()
    prepareDict_plants()
    prepareDict_locomotives()
    crfutils.main(feature_extractor, fields=fields, sep=separator)
