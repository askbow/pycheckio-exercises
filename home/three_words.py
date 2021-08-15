def isword(text):
    for l in text:
        if not l.isalpha(): return False
    return True

def checkio(words):
    wordsSplit = words.split()
    a = 0
    for ww in wordsSplit:
        if isword(ww): a += 1
        else: a = 0
        if a>2: return True
    if a>2: return True
    else: return False

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("Hello World hello") == True, "Hello"
    assert checkio("He is 123 man") == False, "123 man"
    assert checkio("1 2 3 4") == False, "Digits"
    assert checkio("bla bla bla bla") == True, "Bla Bla"
    assert checkio("Hi") == False, "Hi"
