poly = list(map(int, input().split()))
summ = 0
for num in poly:
    summ += 1 / num * 3
print(summ)
