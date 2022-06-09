import os
from pathlib import Path
from colorama import Fore

def is_positive_response(res):
    positive_responses = ["y", "ye", "yes", "yea", "yeah"]
    if (res.strip().lower() in positive_responses):
        return True
    else:
        return False

def add_line(makefile_contents, line, beginning="\n\n"):
    makefile_contents += beginning + line
    return makefile_contents

def add_phony_rule(makefile_contents, phony_targets=["all", "clean", "fclean", "re"]):
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
        elif len(filename + " \\\n") >= header_width:
            makefile_contents += filename + " \\\n"
            if filename != src_files[-1]:
                makefile_contents += "\t"
            width = len("\t")
        else:
            makefile_contents += " \\\n"
            makefile_contents += "\t"
            makefile_contents += filename
            width = len("\t" + filename + " ")

    return makefile_contents

def generate_libft_makefile(makefile_contents):
    print("Generating Makefile...")
    bonuses_present = False
    libft_bonus = ["ft_lstnew.c", "ft_lstadd_front.c", "ft_lstsize.c", "ft_lstlast.c", "ft_lstadd_back.c", "ft_lstdelone.c", "ft_lstclear.c", "ft_lstiter.c", "ft_lstmap.c"]
    makefile_contents = add_line(makefile_contents, "CC = gcc")
    makefile_contents = add_line(makefile_contents, "AR = ar -rcs")
    makefile_contents = add_line(makefile_contents, "FLAGS = -Wall -Wextra -Werror -c")
    makefile_contents = add_line(makefile_contents, "NAME = libft.a")
    makefile_contents = add_line(makefile_contents, "HEADER = libft.h")

    makefile_contents = generate_variable(makefile_contents, ".", name_var="SRC", blacklist=libft_bonus)
    makefile_contents = add_line(makefile_contents, "OBJECTS = $(SRC:.c=.o)")
    prompt_bonuses = input("Did you do the bonus? (yes/no)\n").strip()
    if is_positive_response(prompt_bonuses):
        bonuses_present = True
        makefile_contents = generate_variable(makefile_contents, ".", name_var="BONUS", whitelist=libft_bonus)
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

def remove_extension(executable):
    return executable.split(".")[0]

def generate_name_var(makefile_contents, executable_names=[]):
    for i in range (len(executable_names)):
        makefile_contents += f"\n\nNAME{i} = {executable_names[i]}"
    return makefile_contents

def extension_in_executables(extension, executable_names):
    for executable in executable_names:
        if executable.endswith(extension):
            return True
    return False

def generate_all_rule(makefile_contents, executable_names, libft_present):
    makefile_contents += "\n\nall:"
    if libft_present:
        makefile_contents += " libft.a"
    for i in range(len(executable_names)):
        makefile_contents += f" $(NAME{i})"
    return makefile_contents

def generate_libft_rule(makefile_contents, libft_path):
    makefile_contents = add_line(makefile_contents, "libft.a:\n")
    makefile_contents += f"\tmake -C {libft_path}\n"
    makefile_contents += f"\tcp {libft_path}/libft.a .\n"
    makefile_contents += f"\tcp {libft_path}/libft.h ."
    return makefile_contents

def generate_makefile(makefile_contents, executable_names, libft_present, libft_path):
    print("Generating Makefile...")
    makefile_contents = add_line(makefile_contents, "CC = gcc")
    if extension_in_executables(".a", executable_names):
        makefile_contents = add_line(makefile_contents, "AR = ar -rcs")
    makefile_contents = add_line(makefile_contents, "FLAGS = -Wall -Wextra -Werror -c")


    makefile_contents = generate_name_var(makefile_contents, executable_names)
    makefile_contents = generate_variable(makefile_contents, name_var="HEADER", file_extension="h")

    makefile_contents = add_line(makefile_contents, "#You must clean up the SRC variables (and maybe the HEADER too), delete this comment, and you're done!")
    for executable in executable_names:
        makefile_contents = generate_variable(makefile_contents, ".", name_var=f"SRC_{remove_extension(executable.upper())}")

    for executable in executable_names:
        makefile_contents = add_line(makefile_contents, f"OBJECTS_{remove_extension(executable.upper())} = $(SRC_{remove_extension(executable.upper())}:.c=.o)")

    if libft_present:
        makefile_contents = generate_all_rule(makefile_contents, executable_names, libft_present)
        makefile_contents = generate_libft_rule(makefile_contents, libft_path)
    else:
        makefile_contents = generate_all_rule(makefile_contents, executable_names,libft_present)


    for i in range(len(executable_names)):
        makefile_contents += f"\n\n$(NAME{i}): "
        if libft_present:
            makefile_contents += "libft.a "
        if executable_names[i].endswith(".a"):
            makefile_contents = add_line(makefile_contents, f"$(OBJECTS_{remove_extension(executable_names[i].upper())})\n\t$(AR) $(NAME{i}) $(OBJECTS_{remove_extension(executable_names[i].upper())}) $(HEADER)", beginning="")
        else:
            makefile_contents = add_line(makefile_contents, f"$(OBJECTS_{remove_extension(executable_names[i].upper())})\n\t$(CC) $(OBJECTS_{remove_extension(executable_names[i].upper())}) $(HEADER) -o $(NAME{i})", beginning="")

    makefile_contents = add_line(makefile_contents, "%.o: %.c\n\t $(CC) $(FLAGS) $< -o $@")
    makefile_contents = add_line(makefile_contents, "clean:\n\trm -f *.o")
    makefile_contents = add_line(makefile_contents, "fclean: clean")
    for i in range(len(executable_names)):
        makefile_contents += f"\n\trm -f $(NAME{i})"
    if libft_present:
        makefile_contents += f"\n\trm -f libft.a && rm -f libft.h"
    makefile_contents = add_line(makefile_contents, "re: fclean all")

    makefile_contents = add_phony_rule(makefile_contents)

    return makefile_contents

def save_makefile_prompt_make(makefile_contents):
    with open("./Makefile", "w") as makefile:
        makefile.write(makefile_contents)
    print(Fore.GREEN + "Makefile done!" + Fore.RESET, end=" ")
    print("Thank you for using 42makefile-maker.")
    print("If you found any bugs, please post an issue on Github at ", end="")
    print(Fore.BLUE + "https://github.com/pszleper/42makefile-maker." + Fore.RESET)
    response = input("Do you want to run make now? (yes/no)\n").strip()
    if is_positive_response(response) or response == "make":
        if os.getcwd().endswith("42makefile-maker"):
            os.system("cd .. && make")
        else:
            os.system("make")


if __name__ == "__main__":
    print("You must execute the 42makefile-maker.py file, like so:\npython3 42makefile-maker.py")