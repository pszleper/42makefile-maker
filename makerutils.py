import os
from pathlib import Path

def is_positive_response(res):
    positive_responses = ["y", "ye", "yes", "yea", "yeah"]
    if (res in positive_responses):
        return True
    else:
        return False

def add_line(makefile_contents, line, beginning="\n\n"):
    makefile_contents += beginning + line
    return makefile_contents

def generate_src_variable(makefile_contents, src_path="."):
    src_files = []
    width = len("SRC = ")
    header_width = 80
    i = 0

    for file in Path(src_path).rglob("*.c"):
        src_files.append(str(file))

    makefile_contents += "\n\nSRC ="
    for filename in src_files:
        if len(filename + " ") < header_width:
            makefile_contents += " "
            makefile_contents += filename
            width += len(filename + " ")
        else:
            makefile_contents += " \\\n"
            makefile_contents += "\t"
            makefile_contents += filename
            width = len("\t" + filename + " ")
        if i == len(src_files):
            makefile_contents += " "
            makefile_contents += src_files[i]
            makefile_contents += "\n\n"
            break
        i += 1

    return makefile_contents

def generate_libft_makefile(makefile_contents):
    makefile_contents = add_line(makefile_contents, "CC = gcc")
    makefile_contents = add_line(makefile_contents, "AR = ar -rcs")
    makefile_contents = add_line(makefile_contents, "FLAGS = -Wall -Wextra -Werror -c")
    makefile_contents = add_line(makefile_contents, "NAME = libft.a")
    makefile_contents = add_line(makefile_contents, "HEADER = libft.h")
    makefile_contents = generate_src_variable(makefile_contents, ".")
    makefile_contents = add_line(makefile_contents, "OBJECTS = $(SRC:.c=.o)")
    makefile_contents = add_line(makefile_contents, "all: $(NAME)\n\n$(NAME): $(OBJECTS)\n\t$(AR) $(NAME) $(OBJECTS) $(HEADER)")
    makefile_contents = add_line(makefile_contents, "%.o: %.c\n\t $(CC) $(FLAGS) $< -o $@")
    makefile_contents = add_line(makefile_contents, "clean:\n\trm -f *.o")
    makefile_contents = add_line(makefile_contents, "fclean: clean\n\trm -f libft.a")
    makefile_contents = add_line(makefile_contents, "re: fclean all")

    return makefile_contents

def save_makefile_prompt_make(makefile_contents):
    print("Generating Makefile...")
    with open("./Makefile", "w") as makefile:
        makefile.write(makefile_contents)
    print("Makefile done! Thank you for using 42makefile-maker.\n")
    print("If you found any bugs, please post an issue on Github at https://github.com/pszleper/42makefile-maker.")
    response = input("Do you want to run make now? (yes/no)\n")
    if is_positive_response(response)or response == "make":
        os.system("make")