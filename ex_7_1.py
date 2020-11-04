import math

def cal(a):  # square root using numerical method type iteration
    x = a/4  # estimated value to start iteration
    while True:
        # print(x)  #Muted to only show final value
        y=(x+(a/x))/2
        if y == x:
            return y 
        x=y    


def test(a):  
    e= cal(a)
    f=(math.sqrt(a))
    diff =(f-e)
    return print('Number:',a,'MySqrt:',e,'PySqrt:',f,'Difference:',diff)  
        
        
n=1.0
while n<10.0:
    a=n
    test(a)
    n=n+1.0
    
