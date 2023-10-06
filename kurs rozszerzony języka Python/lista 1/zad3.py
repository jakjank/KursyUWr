def tabliczka(x1,x2,y1,y2,d):
    xs = [1]
    ys = [1]
    while x1 < x2:
        xs.append(x1)
        x1+=d
    xs.append(x2)

    while y1 < y2:
        ys.append(y1)
        y1+=d
    ys.append(y2)
    
    tabliczka = [[x*y for x in xs] for y in ys]
    width = max(len(str(word)) for row in tabliczka for word in row)

    
    print(tabliczka, width)


    

tabliczka(1,3,3,6,1.3)
