array=[23,56,32,45,78,78,98,21,38,57,72,54,34,22,1,456,39,2,5564,3423,7898,454,2315,4675,3245,.5,24578,98765,12343,12323,11233456,2111,7896,345322,.4,.3]

def sorrtArray():
    i = 0
    count = 0
    while count < 1300:
        
        if i == len(array) - 1:
            i = 0
        if array[i+1] < array[i]:
            array.insert(i, array.pop(array.index(array[i+1])))
        if array[i+1] == array[i] or str(array[i]) is True:
            array.remove(array[i])
     
        

        i += 1
        count +=1
    print(array)
sorrtArray()



