def contagem(i):
    print(i)
    if i <= 1:
        return
    else:
        contagem(i - 1)

contagem(9)