import os
from datetime import datetime
import re
import makerutils as utils

if os.path.exists("../Makefile"):
    print("A makefile already exists in the project directory, please move/remove/rename it before running 42makefile-maker again")
    quit()

while True:
    login = input("Enter your 42 login: ").strip()

    if len(login) > 0:
        break
    else:
        print("You did not enter a valid 42 login")

# generate the header and add it to the makefile_contents string
email = f"{login}@student.42.fr"
created_date = str(datetime.now())
created_date = re.sub(r"\.\d+", "", created_date)
created_date = re.sub(r"-", "/", created_date)

# calculate the number of spaces to insert to keep the header width consistent
email_spaces = " " * (80 - len(f"/*   By: {login} <{email}>") - len(f"+#+  +:+       +#+        */"))
created_spaces_1 = " " * (80 - len(f"/*   Created: {created_date} by {login}") - len(f"#+#    #+#             */"))
created_spaces_2 = " " * (80 - len(f"/*   Updated: {created_date} by {login}") - len(f"###   ########.fr       */"))

# this is the template for the header
makefile_contents = f'''# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: {login} <{email}>{email_spaces}+#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: {created_date} by {login}{created_spaces_1}#+#    #+#              #
#    Updated: {created_date} by {login}{created_spaces_2}###   ########.fr        #
#                                                                              #
# **************************************************************************** #'''

project_is_libft = input("Is this project the libft itself? (yes/no)\n").strip()
if utils.is_positive_response(project_is_libft):
    print("Understood, you're working on the libft. We will generate the appropriate makefile")
    makefile_contents = utils.generate_libft_makefile(makefile_contents)
    utils.save_makefile_prompt_make(makefile_contents)
    quit()


executables_names = None
libft_path = "../libft"
libft_present = False

libft_present = input("Have you included your libft in your project? (yes/no)\n").strip()
if utils.is_positive_response(libft_present):
    libft_present = True
    while True:
        libft_path = input("Input the name of the libft folder (leave empty for \"libft\"). If you haven't included your libft, type nolibft\n").strip()
        if os.path.exists(libft_path):
            print("Found your libft folder!")
            break
        elif libft_path == "nolibft":
            libft_present = False
            libft_path = None
            break
        else:
            print("You've input an invalid path to your libft folder. Try again, or type nolibft to signal you haven't included your libft")
else:
    libft_present = False


executable_names_input = None
print("Input the name(s) of executables/archives/outfiles you must generate. If there's more than one, separate the names by using a semicolon \";\", colon\":\" or comma \",\"")
print("Example 1: libft.a\nExample 2: client;server")
while True:
    executable_names_input = input("").strip()
    if len(executable_names_input) > 0:
        break
    else:
        print("You must input a name or series of names in order to proceed")

executable_names = re.split(r",|;|:", executable_names_input)
print("You've input ", end="")
for i in range(0, len(executable_names) - 1):
    print(executable_names[i], end=", ")
print("and " + executable_names[-1])
print("\n", end="")

makefile_contents = utils.generate_makefile(makefile_contents, executable_names, libft_present, libft_path)
utils.save_makefile_prompt_make(makefile_contents)