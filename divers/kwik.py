#! /usr/bin/env python3

import decimal
import re
import math
import readline


RED = "\033[0;31m"
LIGHT_GREEN = "\033[1;32m"
LIGHT_CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
END = "\033[0m"
DARK_GRAY = "\033[1;30m"


while True:
    try:
        a = input(LIGHT_GREEN + "expr ? " + END)

        if a.strip() == "":
            continue

        b = a.replace(",", ".")
        b = b.replace("−", "-")
        b = b.replace("×", "*")
        b = b.replace("^", "**")
        b = b.replace("÷", "/")
        b = b.replace(":", "/")

        v = re.sub(r"(\d+\.?\d*)", r'D("\1")', b)
        w = eval(v, {"D": decimal.Decimal, "sqrt": math.sqrt, "pi": decimal.Decimal(math.pi), "sin": math.sin, "cos": math.cos, "tan": math.tan,},)
        print("  ⟹  {}{}{} = {}{}{}     {}{}{}".format(YELLOW, a, END, LIGHT_CYAN, w, END, DARK_GRAY, v, END))
    except SyntaxError as e:
        print("  ⟹  {}{}{} : {}".format(RED, a, END, e))
    except NameError as e:
        print("  ⟹  {}{}{} : {}".format(RED, a, END, e))
    except TypeError as e:
        w = eval(b, {"sqrt": math.sqrt, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan,},)
        print("  ⟹  {}{}{} = {}{}{}     {}{}{}".format(YELLOW, a, END, LIGHT_CYAN, w, END, DARK_GRAY, b, END))
    except EOFError:
        print()
        print("Bye.")
        break
    except Exception as e:
        print("  ⟹  {}{}{} : {}".format(RED, a, END, e))
