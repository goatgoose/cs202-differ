import sys
import os
import subprocess
import requests
from bs4 import BeautifulSoup
from pathlib import Path

test_case = sys.argv[1]

test_string = open(test_case, "r").read()


def run_main_hs():
    comp = subprocess.run(["stack", "runghc", "Main.hs", f"{test_case}"],
                            stdout=subprocess.PIPE, encoding="UTF-8")

    comp_hs = comp.stdout
    return comp_hs


def get_solution_comp():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    assignment = current_dir.split("/")[-1]

    ret = requests.post(f"https://jnear.w3.uvm.edu/cs202/compiler-{assignment}.php", data={
        "program": test_string
    })
    soup = BeautifulSoup(ret.text, 'html.parser')
    text = soup.pre.text
    return text


if __name__ == '__main__':
    comp_text = run_main_hs()
    solution_text = get_solution_comp()
    if len(solution_text) > len(comp_text):
        end_text = len(comp_text) + 50
        if end_text >= len(solution_text):
            end_text = len(solution_text)
        solution_text = solution_text[:end_text]

    open("solution_out.txt", "w").write(solution_text)
    open("comp_out.txt", "w").write(comp_text)
    diff = subprocess.run(["diff", "-y", "comp_out.txt", "solution_out.txt"],
                          stdout=subprocess.PIPE, encoding="UTF-8")
    print(diff.stdout)
