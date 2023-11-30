from Relation import Relation
from Toople import Toople
from Header import Header
from Database import Database
from typing import Dict
from Interpreter import Interpreter

from project_2.datalog import Datalog
from project_2.predicate import Predicate
from project_2.token import Token
from project_2.lexer_fsm import LexerFSM
from project_2.parse import Parser

#Return your program output here for grading (can treat this function as your "main")
def project4(input: str) -> str:
    lexer: LexerFSM = LexerFSM()
    lexer.run(input)
    tokens: list[Token] = lexer.get_tokens()
    
    parser: Parser = Parser()
    parser.run(tokens)
    datalog_program: Datalog = parser.get_program()
    
    interpreter: Interpreter = Interpreter()
    print(interpreter.run(datalog_program))

    return interpreter.run(datalog_program)

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read() 

#Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("project4-passoff/80/input0.txt")
    print(project4(input_contents))

