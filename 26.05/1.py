# 1
# a = int(input())
# b = a // 2
# Al_summa = b * (b + 1)
# print(Al_summa)


# 2
# import math
#
# n = int(input())
# print(math.factorial(n))

# 3
# a = int(input())
# count = 0
# for i in range(1, a + 1):
#     if a % i == 0:
#         count += 1
# print(count)


# 4
# N = int(input())
# counter = 0
# a = 1
# while a <= N:
#     if N % a == 0:
#         counter +=1
#     a += 1
# if counter == 2:
#     print("простое число")
# else:
#     print("не явл простым числом")

# 5
# import math
# N = input()
# M = input()
# a = [N,M]
# F = max(a)
# print(F)

# 6
# list = []
# a = int(input())
# while a != 0:
#     list.append(a)
#     a = int(input())
# la = [i for i in list if i > 0]
# count = la.count(min(la))
# if count == 1:
#     print("Yes")
# else:
#     print("No")

# 7
# list = []
# a = int(input())
# while a != 0:
#     list.append(a)
#     a = int(input())
# S = sum(list) / len(list)
# print(S)