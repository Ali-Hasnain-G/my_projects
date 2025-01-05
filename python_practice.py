# Hi, Welcome to my Python file practice book 
# Python first programe

print("hello world!")

A = 'hello World'
print(A)

x = y = z = 5
print(z,x,y)
print(x+y+z)

#first function 

def sum_of_num():
    x = y = z = 5
    return x + y + z + x

# Call the function and print the result
print(sum_of_num())

# another funtion
a = 0

def type_of_number():

    if a > 0: # type: ignore
     return 'this is big number'
    elif a < 0: # type: ignore
     return 'this small number'
    else:
     return "nothing"
    
print(type_of_number())

# Fibonacci series:
# the sum of two elements defines the next
a, b = 0, 1
while a < 10:
    print(a)
    a, b = b, a+b

a,b = 0,1
while a < 10:
   print(a)
   a, b = b, a+b

# calcualte the value
i = 674*345
print('The value of i is:', i)


a, b = 0,1
while a < 1000:
   print(a, end=",")
   a, b = b, a+b

# calcualter

num1 = 2 + 2
print(num1)

num2 =50 - 5*6
print(num2)

num3 = (50 - 5*6) / 4
print(num3)

num5 = 8 / 5  # division always returns a floating-point number   
print(num5)