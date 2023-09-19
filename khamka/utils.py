
def validate_code_meli(codemeli):
    b = False
    invali = ["0000000000", "1111111111", "2222222222", "3333333333", "4444444444",
              "5555555555", "6666666666", "7777777777", "8888888888", "9999999999"]
    len_code_is_valid = True if len(codemeli) == 10 else False
    if len_code_is_valid:
        Sum = 0
        for j in range(9):
            Sum += int(codemeli[j])*(10 - j)  # sum number code meli 1-9
        sc = Sum
        c = int(sc / 11)
        ba = abs(sc - (c*11))
        A = int(codemeli[9])  # Ragam 10 codemeli
        B = 11-ba
        if (c == 0 and A == ba) or (c == 1 and A == ba) or (c > 1 and A == B):
            b = True
    return b


