def biggest(aDict):
    '''
    aDict: A dictionary, where all the values are lists.

    returns: The key with the largest number of values associated with it
    '''
    # Your Code Here

    result =0
    tempkey =""

    '''for value in aDict.values():
        # tempKey=""
        if value == 0:
            print (value,key)
            tempKey=key
            print("     ",tempKey)
            return tempkey
            
        #break
'''
    for key in aDict.keys():
        if len(aDict[key])>result: # check =0 or bigger than
            result=len(aDict[key]) # bigger than
            tempKey=key
        #else: key

    return print(result, tempKey)

# animals = { 'a': ['']}

animals = { 'c': ['aardvark', 'fref'], 'b': ['baboon'], 'a': ['coati']}

animals['d'] = ['donkey']
animals['c'].append('dog')
animals['d'].append('dingo')


biggest(animals)