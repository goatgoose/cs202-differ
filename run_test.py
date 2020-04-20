import sys
import os
import subprocess
import requests
from bs4 import BeautifulSoup

test_case = sys.argv[1]
assignment_dir = sys.argv[2]

test_string = open(test_case, "r").read()


def run_main_hs():
    comp = subprocess.run(["stack", "runghc", f"{assignment_dir}/Main.hs", f"{test_case}"],
                            stdout=subprocess.PIPE, encoding="UTF-8")

    comp_hs = comp.stdout
    return comp_hs


def get_solution_comp():
    ret = requests.post("https://jnear.w3.uvm.edu/cs202/compiler-a6.php", data={
        "program": test_string
    })
    soup = BeautifulSoup(ret.text, 'html.parser')
    text = soup.pre.text
    return text


if __name__ == '__main__':
    comp_text = run_main_hs()
    solution_text = get_solution_comp()
    if len(solution_text) > len(comp_text):
        solution_text = solution_text[:len(comp_text) + 50]

    open(f"{assignment_dir}/solution_out.txt", "w").write(solution_text)
    open(f"{assignment_dir}/comp_out.txt", "w").write(comp_text)
    diff = subprocess.run(["diff", "-y", f"{assignment_dir}/comp_out.txt", f"{assignment_dir}/solution_out.txt"])
    print(diff.stdout)

