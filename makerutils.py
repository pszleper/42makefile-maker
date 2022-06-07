import os
from pathlib import Path
from colorama import Fore
import bonus_lists

def is_positive_response(res):
    positive_responses = ["y", "ye", "yes", "yea", "yeah"]
    if (res.strip() in positive_responses):
        return True
    else:
        return False

def add_line(makefile_contents, line, beginning="\n\n"):
    makefile_contents += beginning + line
    return makefile_contents

def add_phony_rule(makefile_contents, phony_targets):
    makefile_contents += "\n\n" + ".PHONY: " + (" ".join(phony_targets))
    return makefile_contents

def generate_variable(makefile_contents, path=".", name_var="SRC", file_extension="c", blacklist=[], whitelist=[]):
    src_files = []
    width = len(f"{name_var} =")
    header_width = 80
    
    for file in Path(path).rglob(f"*.{file_extension}"):
        if not str(file) in blacklist and len(whitelist) == 0:
            src_files.append(str(file))
        elif len(whitelist) > 0 and str(file) in whitelist:
            src_files.append(str(file))

    makefile_contents += f"\n\n{name_var} ="
    for filename in src_files:
        if width + len(filename + " \\\n") < header_width:
            makefile_contents += " "
            makefile_contents += filename
            width += len(filename + " ")
        else:
            makefile_contents += " \\\n"
            makefile_contents += "\t"
            makefile_contents += filename
            width = len("\t" + filename + " ")

    return makefile_contents

def generate_libft_makefile(makefile_contents):
    bonuses_present = False
    makefile_contents = add_line(makefile_contents, "CC = gcc")
    makefile_contents = add_line(makefile_contents, "AR = ar -rcs")
    makefile_contents = add_line(makefile_contents, "FLAGS = -Wall -Wextra -Werror -c")
    makefile_contents = add_line(makefile_contents, "NAME = libft.a")
    makefile_contents = add_line(makefile_contents, "HEADER = libft.h")

    makefile_contents = generate_variable(makefile_contents, ".", name_var="SRC", blacklist=bonus_lists.libft_bonus)
    makefile_contents = add_line(makefile_contents, "OBJECTS = $(SRC:.c=.o)")
    prompt_bonuses = input("Did you do the bonus? (yes/no)\n").strip()
    if is_positive_response(prompt_bonuses):
        bonuses_present = True
        makefile_contents = generate_variable(makefile_contents, ".", name_var="BONUS", whitelist=bonus_lists.libft_bonus)
        makefile_contents = add_line(makefile_contents, "BONUS_OBJECTS = $(BONUS:.c=.o)")
    makefile_contents = add_line(makefile_contents, "all: $(NAME)\n\n$(NAME): $(OBJECTS)\n\t$(AR) $(NAME) $(OBJECTS) $(HEADER)")

    if bonuses_present:
        makefile_contents = add_line(makefile_contents, "bonus: $(NAME) $(BONUS_OBJECTS)\n\tar -rs $(NAME) $(BONUS_OBJECTS) $(HEADER)")

    makefile_contents = add_line(makefile_contents, "%.o: %.c\n\t $(CC) $(FLAGS) $< -o $@")
    makefile_contents = add_line(makefile_contents, "clean:\n\trm -f *.o")
    makefile_contents = add_line(makefile_contents, "fclean: clean\n\trm -f $(NAME)")
    makefile_contents = add_line(makefile_contents, "re: fclean all")

    phony_targets = []
    if bonuses_present:
        phony_targets = ["all", "clean", "fclean", "re", "bonus"]
    else:
        phony_targets = ["all", "clean", "fclean", "re"]
    makefile_contents = add_phony_rule(makefile_contents, phony_targets)

    return makefile_contents

def save_makefile_prompt_make(makefile_contents):
    print("Generating Makefile...")
    with open("./Makefile", "w") as makefile:
        makefile.write(makefile_contents)
    print(Fore.GREEN + "Makefile done!" + Fore.RESET, end=" ")
    print("Thank you for using 42makefile-maker.")
    print("If you found any bugs, please post an issue on Github at ", end="")
    print(Fore.BLUE + "https://github.com/pszleper/42makefile-maker." + Fore.RESET)
    response = input("Do you want to run make now? (yes/no)\n").strip()
    if is_positive_response(response) or response == "make":
        os.system("make")


if __name__ == "__main__":
    print("You must execute the 42makefile-maker.py file, like so:\npython3 42makefile-maker.py")