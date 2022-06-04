import os
import datetime
import re


if os.path.exists("./Makefile"):
    print("A makefile already exists in the current directory, please move/remove it before running 42makefile-maker again")
    quit()

while True:
    login = input("Enter your 42 login: ").strip()

    if (len(login) > 0):
        break
    else:
        print("You did not enter a valid 42 login")
email = f"{login}@student.42.fr"
createdDate = str(datetime.datetime.now())
createdDate = re.sub(r"\.\d+", "", createdDate)
createdDate = re.sub(r"-", "/", createdDate)

print("Generating Makefile...")

emailSpaces = " " * (80 - len(f"/*   By: {login} <{email}>") - len(f"+#+  +:+       +#+        */"))
createdSpaces1 = " " * (80 - len(f"/*   Created: {createdDate} by {login}") - len(f"#+#    #+#             */"))
createdSpaces2 = " " * (80 - len(f"/*   Updated: {createdDate} by {login}") - len(f"###   ########.fr       */"))

#this is the template for the header
makefileContents = f'''# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: {login} <{email}>{emailSpaces}+#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: {createdDate} by {login}{createdSpaces1}#+#    #+#              #
#    Updated: {createdDate} by {login}{createdSpaces2}###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''


with open("./Makefile", "w") as makefile:
    makefile.write(makefileContents)
response = input("Makefile done!\nDo you want to run make now? (yes/no)\n")
if (response == "y" or response == "ye" or response == "yes"):
    os.system("make")
else:
    pass