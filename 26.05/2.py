# num = int(input())
# posit = 0
# negat = 0
# while numbers !=0:
#     if numbers > 0:
#         posit += 1
#     else:
#         negat += 1
# num = int(input())
# print(posit)
# print(negat)


# print(min(x for x in map(int, input().split()) if x % 2 == 0))


# a = [1,2,3,4,2,5,6]
# rez = all(x < y for x, y in zip(a, a[1:]))
# print(rez)


# a = int(input())
# f = False
# while True:
#     c = int(input())
#     if c == 0:
#         break
#     if c >= a:
#             f = False
#             a = c
#             if f:
#                  print("Да")
#             else:
#                  print("Нет")


# count = 0
# total_sum = 0
# while True:
#     number = int(input())
#     if number == 0:
#         break
#     if number % 2 == 0:
#         total_sum += number
#         count += 1
# if count > 0:
#     average = total_sum / count
#     print(average)
# else:
#     print("нет")



# n = int(input())
# arr = list(map(float, input().split()))
# 
# nega_num = [x for x in arr if x < 0]
# 
# if nega_num:
#     average = sum(nega_num) / len(nega_num)
#     print(average)
# else:
#     print("Отр")