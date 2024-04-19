'''
If divisible by 3, print Fizz.  
If divisible by 5, print Buzz.  
If divisible by both, print FizzBuzz.  
Else, print the number.
'''

import time
from typing import List

def regular_long(n:int=15):
    """
    N (int) :  up to what number?
    d (dict) :  divisor, word to print in place of dividend if divisible
        i.e. { 3: "Fizz", 5: "Buzz" }
    """
    d = {
        3:'Fizz',
        5:'Buzz'
    }
    output = []
    for i in range(1,n+1):
        print_num = True # print number
        num_string = ''

        for divisor,word in d.items():
            if (i % divisor) == 0:
                num_string += word
                print_num = False  # don't print number if printing word

        if print_num:
            output.append(str(i))
        else:
            output.append(num_string)
    
    return output


def golfed_limited(n:int=15):
    """
    N (int) :  number to go to
    a (List) :  list of value/word lists
        i.e. [ [3, "fizz"] , [5, "buzz"] ]
    """
    a = [[3,"Fizz"],[5,"Buzz"]]
    output = []
    for x in range(1,n+1):
        output.append(str(''.join(j*(x%i<1)for i,j in a)or x))
    return output


golfed_infinite=lambda a,n=1:print(''.join(j*(n%i<1)for i,j in a)or n)+golfed_infinite(a,n+1)


if __name__ == "__main__":
    start_time = time.time()

    print(regular_long())
    print()
    print(golfed_limited())
    # golfed_infinite([[4, "Foo"], [7, "Bar"], [9, "Baz"]])

    print(f'\nElapsed Time: {time.time()-start_time:0.8f} seconds')
