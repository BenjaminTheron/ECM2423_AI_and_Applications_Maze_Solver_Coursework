dict = {}
(row1, column1) = (2,5)
(row2, column2) = (0,8)
(row3, column3) = (4,7)
dict[(row1, column1)] = "cost"
dict[(row2, column2)] = "cost2"
dict[(row3, column3)] = "cost3"

if (3,4) in dict:
    print("ok")
else:
    print("fukcoff")

for item in dict:
    print(item)

var = next(reversed(dict))
print(var)

print()
print(len(dict))

