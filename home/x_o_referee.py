
def checkio(game_result):
    #
    #
    for h in game_result:
        if h == "XXX": return "X"
        elif h == "OOO": return "O"
    for l in range(len(game_result[0])):
        if game_result[0][l] == game_result[1][l] and game_result[0][l] == game_result[2][l]: 
            if game_result[0][l] == "X" or game_result[0][l] == "O": return game_result[0][l]
    if game_result[0][0] == game_result[1][1] and game_result[0][0] == game_result[2][2]: 
        if game_result[0][0] == "X" or game_result[0][0] == "O": return game_result[0][0]
    if game_result[0][2] == game_result[1][1] and game_result[0][2] == game_result[2][0]: 
        if game_result[0][2] == "X" or game_result[0][2] == "O": return game_result[0][2]
    return "D"

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([
        "X.O",
        "XX.",
        "XOO"]) == "X", "Xs wins"
    assert checkio([
        "OO.",
        "XOX",
        "XOX"]) == "O", "Os wins"
    assert checkio([
        "OOX",
        "XXO",
        "OXX"]) == "D", "Draw"
    assert checkio([
        "O.X",
        "XX.",
        "XOO"]) == "X", "Xs wins again"
    print("Coding complete? Click 'Check' to review your tests and earn cool rewards!")
