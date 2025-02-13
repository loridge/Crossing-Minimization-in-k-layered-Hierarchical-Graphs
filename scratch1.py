### A file used for scratch

a = [1, 2, 4, 343, 8, 9, 35, 355, 77, 3]

bb = a.index(4)

c = a[:bb] + a [bb + 1: ] + [a[bb]]

print(c)