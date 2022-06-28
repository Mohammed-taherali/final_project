ab = int(input())

bc = int(input())




# a = ('A', 'B', 'C')

# print(a[0])




# import time
# from collections import Counter

# def no_idea():
#     #No idea!
#     # n -> no. of elements in arr
#     # m -> no of elements in setA and setB

#     n, m = map(int, input().split())
#     arr = list(map(int, input().split()))

#     setA = list(map(int, input().split()))
#     setB = list(map(int, input().split()))

#     happiness = 0
#     for i in range(n):
#         if arr[i] in setA:
#             happiness += 1
#         elif arr[i] in setB:
#             happiness -= 1

#     print(happiness)


# if __name__ == '__main__':
#     no_idea()

# class Solution:
#     def romanToInt(self, s: str) -> int:

#         roman_to_int = {
#             'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000, 'V-I': 4,
#             'X-I': 9, 'L-X': 40, 'C-X': 90, 'D-C': 400, 'M-C': 900
#         }

#         int_val = 0

#         for num in s:
#             print(num)

#         return 5

# class Solution:
#     def romanToInt(self, s: str) -> int:
#         mapp = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}

#         out = mapp[s[-1]]   # store last char value 

#         for i in reversed(range(len(s)-1)):         # iterate from s[-2]
#             if mapp[s[i]] < mapp[s[i+1]]:           # check cur idx and prev idx value and add or sub in out
#                 out -= mapp[s[i]]
#             else:
#                 out += mapp[s[i]]
#         return out

# sol = Solution()
# ans = sol.romanToInt("MCMVI")

# print(ans)


# class Solution:
#     def romanToInt(self, s: str) -> int:

#         roman_to_int = {
#             'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000, 'V-I': 4,
#             'X-I': 9, 'L-X': 40, 'C-X': 90, 'D-C': 400, 'M-C': 900
#         }

#         int_val = 0

#         num = list(s)
#         len_of_num = len(num)

#         for i in range(len_of_num):

#             if i != len_of_num:

#                 if num[i] == 'I':
#                     try:
#                         if num[i + 1] == 'V':
#                             int_val += roman_to_int['V-I']
#                             i += 2

#                         elif num[i + 1] == 'X':
#                             int_val += roman_to_int['X-I']
#                             i += 1

#                         else:
#                             int_val += roman_to_int['I']
#                     except IndexError:
#                         int_val += roman_to_int['I']
#                         return int_val

#                 elif num[i] == 'V':
#                     int_val += roman_to_int['V']
                    

#                 elif num[i] == 'X':
#                     try:
#                         if num[i + 1] == 'L':
#                             int_val += roman_to_int['L-X']
#                             i += 1

#                         elif num[i + 1] == 'C':
#                             int_val += roman_to_int['C-X']
#                             i += 1
                    
#                         else:
#                             int_val += roman_to_int['X']
                    
#                     except IndexError:
#                         int_val += roman_to_int['X']
#                         return int_val

#                 elif num[i] == 'L':
#                     int_val += roman_to_int['L']

#                 elif num[i] == 'C':
#                     try:
#                         if num[i + 1] == 'D':
#                             int_val += roman_to_int['D-C']
#                             i += 1

#                         elif num[i + 1] == 'M':
#                             int_val += roman_to_int['M-C']
#                             i += 1
                    
#                         else:
#                             int_val += roman_to_int['C']

#                     except IndexError:
#                         int_val += roman_to_int['C']
#                         return int_val

#                 elif num[i] == 'D':
#                     int_val += roman_to_int['D']

#                 elif num[i] == 'M':
#                     int_val += roman_to_int['M']


#         return int_val



# ans1 = Solution()
# t = ans1.romanToInt(s="IV")
# print(t)

# a = "ABCD"

# b = list(a)

# print(b)


# class Solution:
#     def isValid(self, s: str) -> bool:
#         print(s)
#         for char in s:
#             if char in ['(', ')', '[', ']', '{', '}']:
#                 pass

        

# ans1 = Solution()
# t = ans1.isValid("(){{}}")

# print(t)

# b = "-121"

# c = b[:0:-1]

# print(c)


# a = 0b1010
# print(a)
# print()

# a = int('ff', base=16)
# b = float('3.14')
# print(a,b)

# c = (17,)
# d = 'don\'t worry'
# print(type(c))
# print(d)

# e = '\u20B9100'
# t = [('a', 'hi'), ('b', 'bye')]
# ans = dict(t)
# print(ans)
# print(e)
# print( "Welcome to the GPA calculator. ") 
# print(" Please enter all your letter grades, one per line." ) 
# print( "Enter a blank line to designate the end." ) # map from letter grade to point value 
# points = { 'A+' :4.0, 'A' :4.0, 'A-' :3.67, 'B+' :3.33, 'B' :3.0, 'B-' :2.67, 'C+' :2.33, 'C' :2.0, 'C' :1.67, 'D+' :1.33, 'D' :1.0, 'F' :0.0}
# num_courses = 0 
# total_points = 0 
# done = False 
# while not done: 
#     grade = input( ) 
#     if grade == '':
#         done = True 
#     elif grade not in points: # unrecognized grade entered 
#         print("Unknown grade {0} being ignored".format(grade)) 
#     else:
#         num_courses += 1 
#         total_points += points[grade]

# if num_courses > 0: # avoid division by zero
#     print("Your GPA is {0:.3} ".format(total_points / num_courses))


# class Solution:
#     def isPalindrome(self, x: int) -> bool:
#         org = str(x)
#         new = org[::-1]
#         try:
#             new = int(org[::-1])
#         except ValueError:
#             new = int(org[::-2])
#             new -= 2*new


#         if x == new:
#             print("true")
#             return True
#         else:
#             print("false")
#             return False

# ans1 = Solution()
# t = ans1.isPalindrome(-121)

# print(t)

# a = "10"
# b = 10

# if a == b:
#     print("equal")

# else:
#     print("not equal")

"""cur_time = list(map(int, input().split()))
time_req = list(map(int, input().split()))

total_time = cur_time

if cur_time[1] + time_req[1] > 60:
    total_time[1] = int((cur_time[1] + time_req[1])% 60)
    total_time[0] += 1
    # print(total_time[0])
    if total_time[0] > 23:
        total_time[0] = total_time[0] % 24
        total_time[0] += time_req[0]
        print(cur_time[0] + time_req[0])
    if cur_time[0] + time_req[0] > 23:
        total_time[0] = (cur_time[0] + time_req[0]) % 24
    total_time[0] = cur_time[0] + time_req[0]


    

else:
    total_time[1] = cur_time[1] + time_req[1]
    total_time[0] = cur_time[0] + time_req[0]


print(f"{total_time[0]:02d} {total_time[1]:02d}")"""

# cur_time = list(map(int, input().split()))
# time_req = list(map(int, input().split()))

# total_time = [0, 0]

# if cur_time[1] + time_req[1] > 60:
#     total_time[1] = int((cur_time[1] + time_req[1])% 60)
#     total_time[0] = cur_time[0] + time_req[0]
#     total_time[0] += 1
    

# else:
#     pass
#     total_time[1] = cur_time[1] + time_req[1]
#     total_time[0] = cur_time[0] + time_req[0]


# print(total_time[0], total_time[1])

# a = 45 
# b = 20

# c = (a + b)%60

# print(c)


# print(cur_time, time_req)









# a = 0.0

# if a:
#     print("hi")
# else:
#     print("bye")
# try:
#     b = int(a)
#     print(b)
# except ValueError:
#     print("not possible")


# a = ""

# try:
#     b = int(a)
# except ValueError:
#     b = int("0")

# print(b)

# lst = ["a","b","c"]

# print(lst)
# t = ""
# print(t.strip().upper())
# lst = []

# print(lst)

# t = "fas"

# print(float(t))

# abcd = "None"

# if abcd:
#     print("hi")

# else:
#     print("BYE!")

# from werkzeug.security import generate_password_hash,check_password_hash

# hash_pass = generate_password_hash("Mohammed")
# print(hash_pass)
# # print(check_password_hash(hash_pass, "mohammed"))

# print(check_password_hash("pbkdf2:sha256:260000$wSkbU8M4q5mwpBTr$ace9fa7841a7bb058f1df4126157e6f1a5c0782b9080cc0fb5bb3a49571e0763", "jhalrapatan420"))

# t = "abcd ab ab ab ba ba"
# print(t)

# from datetime import date

# # print(date.today().strftime("%d/%m/%Y"))

# a = "10/06/2023"
# b = "11/06/2022"

# bill_date = "2023/06/10"

# curr_date = "2023/06/11"

# if curr_date < 