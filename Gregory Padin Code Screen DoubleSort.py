"""
Gregory Padin Code Screen
02/08/2015

Double Sort

Please write a method which accepts an array of strings. 
Each element can either be a number ("165") or a word ("dog"). 
Your method should sort and print the array such that 
    (1) All of the words are sorted alphabetically and the numbers are sorted numerically, and 
    (2) the order of words and numbers is the same. 
You can use standard library sort functions, and should assume that all inputs will be valid. 
If you make any other assumptions, please document those as well.

Examples (input => output):
sort([dog, cat])
=> [cat, dog]
sort(5, 3)
=> [3, 5]
sort(5, 4, dog, 1, cat)
=> [1, 4, cat, 5, dog]



Assuming that a number could be negative, represented by the first character being '-'
Assuming that a number could be an int or a float, but will not cause an overflow error when converted to a number
Assuming that a valid number will only contain alpha-numeric values, and the '.' and '-' symbols. i.e. formulas won't be calculated 
Assuming that the numbers should be displayed in their original string format, so '003' will sort as 3 but appear as '003'
Assuming the capitalization shouldn't matter when sorting the words. 
If given a 0 length list it will return a 0 length list.
I'm referring to a set of strings as a word. 
"""
from collections import deque

def DoubleSort(inputList):
    words = []
    numbers = []
    orderedList = [] #Used to hold the number/word order of the original list. 0 = number 1 = word. Eventually these values are replaced with the sorted list. 
  
    for string in inputList:
        if isValidNumber(string):
            orderedList.append(0)
            numbers.append(string)
        else:
            orderedList.append(1)
            words.append(string)
    #Convert sorted lists to deques so I can remove the first item of the list faster. 
    words = deque(sorted(words, key= lambda x: x.lower()))
    numbers = deque(sorted(numbers, key = float))
 
    for i in range(0, len(orderedList)):
        if orderedList[i] == 0:
            orderedList[i] = numbers[0]
            numbers.popleft()
        else:
            orderedList[i] = words[0]
            words.popleft()
            
    print orderedList
def isValidNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False