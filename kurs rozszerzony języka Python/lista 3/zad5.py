def max_sublist_sum(l):
    maxi = cur = 0
    for el in l:
        cur = max(cur + el, 0)
        maxi = max(cur, maxi)
    return maxi

print(max_sublist_sum([1,2,3,4]))
print(max_sublist_sum([1,-4,-5,4]))
print(max_sublist_sum([100,-1,200]))