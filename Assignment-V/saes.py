#!/usr/bin/python3
substitutionDictionary = {
            "0000" : "1001",
            "0001" : "0100",
            "0010" : "1010",
            "0011" : "1011",
            "0100" : "1101",
            "0101" : "0001",
            "0110" : "1000",
            "0111" : "0101",
            "1000" : "0110",
            "1001" : "0010",
            "1010" : "0000",
            "1011" : "0011",
            "1100" : "1100",
            "1101" : "1110",
            "1110" : "1111",
            "1111" : "0111"
            }
def substituteNibbles(plaintextMat):
    substitutedMat = list()
    for l in plaintextMat:
        temp = list()
        for nibble in l:
            temp.append(substitutionDictionary[nibble])
        substitutedMat.append(temp)
    return substitutedMat

def shiftRows(plaintextMat):
    plaintextMat[1].reverse()
    return plaintextMat

def mixColumns(plaintextMat):
    lookupTable = {
            "0000" : 0,
            "0001" : 4,
            "0010" : 8,
            "0011" : 12,
            "0100" : 3,
            "0101" : 7,
            "0110" : 11,
            "0111" : 15,
            "1000" : 6,
            "1001" : 2,
            "1010" : 14,
            "1011" : 10,
            "1100" : 5,
            "1101" : 1,
            "1110" : 13,
            "1111" : 9,
        }
    #irreduciblePolynomial = int("00010011", 2)
    mixedColumns = [
            [
                format(int(plaintextMat[0][0], 2)  ^ lookupTable[plaintextMat[1][0]], "08b")[4:8],
                format(int(plaintextMat[0][1], 2) ^ lookupTable[plaintextMat[1][1]], "08b")[4:8]
            ],
            [
                format(lookupTable[plaintextMat[0][0]] ^ int(plaintextMat[1][0], 2), "08b")[4:8],
                format(lookupTable[plaintextMat[0][1]] ^ int(plaintextMat[1][1], 2), "08b")[4:8]
            ]
        ]
    return mixedColumns

def addRoundKey(plaintext, key):
    return [
            [str(format((int(str(plaintext[0][0]), 2) ^ int(str(key[0][0]), 2)), "08b")[4:8]), str(format((int(str(plaintext[0][1]), 2) ^ int(str(key[0][1]), 2)), "08b")[4:8])],
            [str(format((int(str(plaintext[1][0]), 2) ^ int(str(key[1][0]), 2)), "08b")[4:8]), str(format((int(str(plaintext[1][1]), 2) ^ int(str(key[1][1]), 2)), "08b")[4:8])]
        ]

def expandKey(key, roundNumber):
    key0 = int(key[0][0] + key[1][0], 2)
    key1 = int(key[0][1] + key[1][1], 2)
    #Nibble substitution of the reverse of the second key
    keyTemp = substitutionDictionary[key[1][1]] + substitutionDictionary[key[0][1]]
    
    if roundNumber == 1:
        rcon = int("10000000", 2)
    elif roundNumber == 2:
        rcon = int("00110000", 2)
    else:
        print("Incorrect round number.")
        raise SystemExit
    
    keyTemp = int(keyTemp, 2) ^ rcon
    
    key2 = key0 ^ keyTemp
    key3 = key1 ^ key2

    return [
            [str(format(key2, '08b')[0:4]), str(format(key3, '08b')[0:4])],
            [str(format(key2, '08b')[4:8]), str(format(key3, '08b')[4:8])]
        ]

def getTextFromMatrix(matrix):
    return chr(int(matrix[0][0] + matrix[1][0], 2)) + chr(int(matrix[0][1] + matrix[1][1], 2))

def createMatrix(text):
    return [
            [str(format(ord(text[0]), '08b')[0:4]), str(format(ord(text[1]), '08b')[0:4])],
            [str(format(ord(text[0]), '08b')[4:8]), str(format(ord(text[1]), '08b')[4:8])]
        ]

def encrypt(plaintext, key):
    ciphertext = ""
    plaintextLength = len(plaintext)
    keyMat = createMatrix(key)
    i = 0
    while i < plaintextLength:
        if i != plaintextLength - 1:
            plaintextMat = createMatrix(plaintext[i] + plaintext[i + 1])
        else:
            plaintextMat = createMatrix(plaintext[i] + " ")
        i += 2

        plaintextMat = addRoundKey(plaintextMat, keyMat)
        #print(plaintextMat)
        plaintextMat = substituteNibbles(plaintextMat)
        plaintextMat = shiftRows(plaintextMat)
        plaintextMat = mixColumns(plaintextMat)
        keyMat = expandKey(keyMat, 1)
        #print(keyMat)
        #print(plaintextMat)
        plaintextMat = addRoundKey(plaintextMat, keyMat)

        plaintextMat = substituteNibbles(plaintextMat)
        plaintextMat = shiftRows(plaintextMat)
        keyMat = expandKey(keyMat, 2)
        plaintextMat = addRoundKey(plaintextMat, keyMat)
        
        ciphertext += getTextFromMatrix(plaintextMat)
        #return plaintextMat
    return ciphertext
