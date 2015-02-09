# ugly stuff to import modules one directory up
import os
import sys
import StringIO
cur_dir = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.dirname(cur_dir)
parser_dir = os.path.join(top_dir, "lib", "parser")
sys.path.insert(0, parser_dir)
import ast
from eval_ast import evaluate
from kobjects import builtins

reducible_nodes = ["StatementList", "ExpressionList", "KeyValueList"]

compile = ast.get_compiler(
    os.path.join(cur_dir, "tokens.txt"), 
    os.path.join(cur_dir, "language.txt"), 
    reducible_nodes
)

def execute(program_text, strict=False):
    if not strict:
        program_text += ";"
    tree = compile(program_text)
    scopes = [builtins]
    evaluate(tree, scopes)


def check_output(*args, **kargs):
    """
    #behaves identically to `execute`, 
    except it suppresses all print statements, 
    and returns a string containing what would have been printed.
    """
    s = StringIO.StringIO()
    old_stdout = sys.stdout
    sys.stdout = s
    try:
        execute(*args, **kargs)
    finally:
        sys.stdout = old_stdout
    return s.getvalue().rstrip()
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("please supply a file name.")
        sys.exit(0)


    with open(sys.argv[1]) as file:
        program_text = file.read()

    execute(program_text, "--strict" in sys.argv[2:])