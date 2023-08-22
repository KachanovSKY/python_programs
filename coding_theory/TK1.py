import random

GenMatrix = [
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 1, 2, 2, 0],
    [0, 0, 1, 0, 0, 0, 1, 2, 1, 0, 2],
    [0, 0, 0, 1, 0, 0, 2, 1, 0, 1, 2],
    [0, 0, 0, 0, 1, 0, 2, 0, 1, 2, 1],
    [0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 1]]

hMatrix = [[2, 2, 2, 2, 2],
           [2, 2, 1, 1, 0],
           [2, 1, 2, 0, 1],
           [1, 2, 0, 2, 1],
           [1, 0, 2, 1, 2],
           [0, 1, 1, 2, 2],
           [1, 0, 0, 0, 0],
           [0, 1, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 1, 0],
           [0, 0, 0, 0, 1]]

def MatrixMultiply(vect, Matrix):
    out = [0]*len(Matrix[0])
    for i in range(len(Matrix[0])):
        tmp = 0
        for j in range(len(vect)):
            tmp += Matrix[j][i] * vect[j]
        out[i] = tmp % 3 
    return out

def Dec2Tri(n):
    out = [0]*6
    i = 0
    while n > 0:
        out[i] = (n%3)
        n //= 3
        i += 1
    out.reverse()
    return out 

def ErrGen(n):
    count = 0
    for i in range(len(n)):
        if random.random() > 0.5:
            n[i] = (n[i] + 2) % 3
            count += 1
        if count == 2:
            break
    return n

def HammSpace(e, n):
    count = 0
    for i in range(len(e)):
        if e[i] == n[i]:
            count += 1
    return count

def Restore(n, G):
    minSpace = 0
    rest = []
    ind = 0
    count = 0
    for i in G:
        count += 1
        tmp = HammSpace(n, i)
        if tmp > minSpace:
            rest = []
            rest.append(i)
            ind = count
            minSpace = tmp
        elif tmp == minSpace:
            rest.append(i)
        
    return rest[0] 

    
def main():
    G = [[0]]
    #Генерация всех возможных кодовых слов
    for i in range (1, 729):
        left = Dec2Tri(i)
        tmp = MatrixMultiply(left, GenMatrix)
        if MatrixMultiply(tmp, hMatrix) == [0]*5:
            G.append(tmp)

    #Выделение сумм для двойных ошибок
    sums = []
    for i in range (len(GenMatrix)):
        for j in range(i + 1, len(GenMatrix)):
            tmp = [[],[i + 1, j + 1]]
            for k in range(6, 11):
                tmp[0].append((GenMatrix[i][k] + GenMatrix[j][k])%3)
            sums.append(tmp)

    for i in range(5):
        seed = int(random.random() * 1000) % len(G)
        print("Message:", Dec2Tri(seed))
        print("Coded word:", G[seed])
        err = ErrGen(G[seed].copy())
        print("Errored word:", err)
        sind = MatrixMultiply(err, hMatrix)
        print("Sindrom:", sind)
        errBits = 0
        for i in range(len(GenMatrix)):
            if GenMatrix[i][6:] == sind:
                print("Error in", i, " bit")
                errBits = 1
        if errBits == 0:
            for i in sums:
                if i[0] == sind:
                    print("Error in", i[1], " bits")
        print("Restored word:", Restore(err, G[1:]))
        print("Encoded message:", Dec2Tri(seed), "\n")

    #Ручные тесты
    # print("Введите вектор с ошибками")
    # err = [input() for i in range(11)]
    # print("Errored word:", err)
    # sind = MatrixMultiply(err, hMatrix)
    # print("Sindrom:", sind)
    # errBits = 0
    # for i in range(len(GenMatrix)):
    #     if GenMatrix[i][6:] == sind:
    #         print("Error in", i, " bit")
    #         errBits = 1
    # if errBits == 0:
    #     for i in sums:
    #         if i[0] == sind:
    #             print("Error in", i[1], " bits")
    # print("Restored word:", Restore(err, G[1:]), "\n")
    #print(sums)
    #print(len(G))
    #print(G)
    #print(weightDict)


if __name__ == "__main__":
    main()