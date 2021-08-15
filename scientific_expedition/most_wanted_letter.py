import string

def checkio(text):
    letterCount = dict()
    for a in text.lower():
        if a in 'abcdefghijklmnopqrstuvwxyz':
            if not a in letterCount:
                #
                letterCount[a] = 1
            else:
                letterCount[a] += 1
    k = sorted(letterCount.items(), key=lambda x: (-x[1], x[0]))
    #
    return k[0][0]

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("Hello World!") == "l", "Hello test"
    assert checkio("How do you do?") == "o", "O is most wanted"
    assert checkio("One") == "e", "All letter only once."
    assert checkio("Oops!") == "o", "Don't forget about lower case."
    assert checkio("AAaooo!!!!") == "a", "Only letters."
    assert checkio("abe") == "a", "The First."
    print("Start the long test")
    assert checkio("a" * 9000 + "b" * 1000) == "a", "Long."
    print("The local tests are done.")
