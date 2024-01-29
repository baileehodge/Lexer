import os
from project_2.parse import Parser
from project_2.lexer_fsm import LexerFSM
# import your lexer

def project2(input: str) -> str:
    lexer = LexerFSM()
    lexer.run(input)
    tokens = lexer.get_tokens()

    parser = Parser()

    return parser.run(tokens)


def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()


# Use this to run and debug code within VS
if __name__ == "__main__":
    # input_contents = read_file_contents("Path to input file goes here")
    os.chdir('.')
    input_contents = read_file_contents("./project2-passoff/80/input0.txt")
    #input_contents = read_file_contents("test.txt")
    print(project2(input_contents))
    
    