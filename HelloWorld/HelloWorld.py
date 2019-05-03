# ipAddress = input("Please enter an IP address: ")
# if ipAddress[-1] != '.':
#     ipAddress += '.'
#
# segment = 1
# segment_length = 0
#
# for character in ipAddress:
#     if character == '.':
#         print("segment {} contains {} characters".format(segment, segment_length))
#         segment += 1
#         segment_length = 0
#     else:
#         segment_length += 1

# import random
# highest = 10
# answer = random.randint(1, highest)

# print("Please guess a number between 1 and {}: ".format(highest))
# guess = int(input())
# if guess != answer:
#     if guess < answer:
#         print("Please guess higher")
#     else:
#         print("JPlease guess lower")
#     guess = int(input())
#     if guess == answer:
#         print("Well done, you guess it")
#     else:
#         print("Sorry, you have not guessed correctly")
# else:
#     print("You got it first time")

# print("Please guess a number between 1 and {}: ".format(highest))
# guess = int(input())
# if guess == answer:
#     print("You got it first time")
# while guess != answer:
#     if guess < answer:
#         print("Please guess higher")
#     else:
#         print("Please guess lower")
#     guess = int(input())
# if guess == answer:
#     print("Well done, you guessed it")

# menu = []
# menu.append(["egg", "spam", "bacon"])
# menu.append(["egg", "sausage", "bacon"])
# menu.append(["egg", "spam"])
# menu.append(["egg", "bacon", "spam"])
# menu.append(["egg", "bacon", "sausage", "spam"])
# menu.append(["spam", "bacon", "sausage", "spam"])
# menu.append(["spam", "egg", "spam", "spam", "bacon", "spam"])
# menu.append(["spam", "egg", "sausage", "spam"])
#
# for meal in menu:
#     if not "spam" in meal:
#         print(meal)
#         for ingredient in meal:
#             print(ingredient)



