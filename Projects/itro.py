#  # this practise file for git 
# # name = "ali"
# # height = 139
# # weight = 70
# # address = 'lahore'
# # bmi = height * weight
# # print(bmi)
# # if bmi > 10000:
# #     print("greater than")
# # elif bmi >= 9730:
# #     print("equal good luck")
# # else:
# #     print('less than')

# # usefull tutorials for coding
# # https://github.com/iamshaunjp/flutter-beginners-tutorial
# # closures and decorators
# # *args and **kwargs
# # map, filter, and lambda functions.
# # encapsulation 
# # robust 

# inp  = 'ali: '
# print(inp)
# inp = '4: '
# print(type(inp))
# inp = 'ahg: '
# print('input is this:' , type(inp)(inp))
# print(4//2)
# a=3
# b=4
# print(a+b), (a/b),(a*b),(a-b), (a==b),(a>>b),(a<b) ,(a!=b),(a>=b),(a >= b),(a+b)
# print(a is not b)
# print(a is  b)
# min = a if a < b else b
# print(min)


# Str="GeeksForGeeks"
# lower=0
# upper=0
# for i in Str:
# 	if(i.islower()):
# 			lower+=1
# 	else:
# 			upper+=1
# print("The number of lowercase characters is:",lower)
# print("The number of uppercase characters is:",upper)


# a="abAcdefDghiCjkl"
# lower=0
# upper=0
# for i in a:
# 	if(i.islower()):
# 		lower+=1
# 	else:
# 		upper+=1
# print("The number of lowercase characters is:",lower)
# print("The number of uppercase characters is:",upper)

# # Python3 program to count upper and
# # lower case characters without using
# # inbuilt functions
# def upperlower(string):

# 	upper = 0
# 	lower = 0

# 	for i in range(len(string)):
		
# 		# For lower letters
# 		if (ord(string[i]) >= 97 and
# 			ord(string[i]) <= 122):
# 			lower += 1

# 		# For upper letters
# 		elif (ord(string[i]) >= 65 and
# 			ord(string[i]) <= 90):
# 			upper += 1

# 	print('Lower case characters = %s' %lower,
# 		'Upper case characters = %s' %upper)

# # Driver Code
# string = 'GeeksforGeeks is a portal for Geeks'
# upperlower(string)


# s = "The Geek King"
# l,u = 0,0
# for i in s:
# 	if (i>='a'and i<='z'):
		
# 		# counting lower case
# 		l=l+1			
# 	if (i>='A'and i<='Z'):
		
# 		#counting upper case
# 		u=u+1
		
# print('Lower case characters: ',l)
# print('Upper case characters: ',u)

# # Python3 program to count upper and
# # lower case characters without using
# # inbuilt functions
# string = 'GeeksforGeeks is a portal for Geeks'
# upper = 0
# lower = 0
# up="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# lo="abcdefghijklmnopqrstuvwxyz"
# for i in string:
# 	if i in up:
# 		upper+=1
# 	elif i in lo:
# 		lower+=1
# print('Lower case characters = %s' %lower)
# print('Upper case characters = %s' %upper)

# import operator as op
# Str = "GeeksForGeeks"
# lower = "abcdefghijklmnopqrstuvwxyz"
# l = 0
# u = 0
# for i in Str:
# 	if op.countOf(lower, i) > 0:
# 		l += 1
# 	else:
# 		u += 1
# print("The number of lowercase characters is:", l)
# print("The number of uppercase characters is:", u)




# import re
 
# my_string = "Good Morning and Morning is Great."
# substring = "Morning"
# substring_count = len(re.findall(substring, my_string))
# print(substring_count)

# print("a".encode('utf-8'))

# from encodings.aliases import aliases

# # Printing list available
# print("The available encodings are : ")
# print(aliases.keys())

