list1 = [((1,2),8),((2,3),23),((3,4),4),((5,6),1)]

(cr,cc) = (1,2)
newCost = 2

for x in range(len(list1)):
    ((r,c),cost) = list1[x]
    
    if cr == r and cc == c:
        if newCost < cost:
            print("This works!")
            list1[x] = ((r,c),newCost)


print(list1[list1.index(((1,2),newCost))])