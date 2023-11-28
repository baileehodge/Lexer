# help slides:
# https://docs.google.com/presentation/d/1I1rmBa7SKR8g6UliwpAZmsorvSprK4ZXzhUgE-nlVB4/edit
from Relation import Relation
from Header import Header
from Toople import Toople
from Interpreter import Interpreter

# remove this and delete the file 
# after you add in your code from project 2
# from class_stubs import * 

from project_2.datalog import Datalog
from project_2.predicate import Predicate
from project_2.token import Token
from project_2.lexer_fsm import LexerFSM
from project_2.parse import Parser

base_Toople_1: Toople = Toople(['\'12345\'','\'Charlie\'','\'12 Apple St.\'','\'555-1234\''])
base_Toople_2: Toople = Toople(['\'67890\'','\'Lucy\'','\'34 Pear Ave.\'','\'555-5678\''])
base_Toople_3: Toople = Toople(['\'33333\'','\'Snoopy\'','\'12 Apple St.\'','\'555-1234\''])
base_Toople_4: Toople = Toople(['\'33333\'','\'Charlie\'','\'12 Apple St.\'','\'Charlie\''])
base_Toople_5: Toople = Toople(['\'33333\'','\'Snoopy\'','\'12 Apple St.\'','\'Snoopy\''])
base_header: Header = Header(["S", "N", "A", "P"])
base_relation: Relation = Relation("SNAP", base_header, set([base_Toople_1, base_Toople_2, base_Toople_3, base_Toople_4, base_Toople_5]))

def test_select1():
    print('select1("\'Charlie\'", 1):')
    print(base_relation.select1("\'Charlie\'", 1).__str__())
    print('select("\'12 Apple St.\'", 2):')
    print(base_relation.select1("\'12 Apple St.\'", 2).__str__())
    try:
        print('select1("\'Charlie\'",-1):')
        print(base_relation.select1("\'Charlie\'", -1).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
        
    try:
        print('select1("\'Charlie\'",4):')
        print(base_relation.select1("\'Charlie\'", 4).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_select2():
    print('select2(1,3):')
    print(base_relation.select2(1, 3).__str__())
    print('select2(0,1):')
    print(base_relation.select2(0,1).__str__())
    try:
        print('select2(-1,1):')
        print(base_relation.select2(-1,0).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
    try:
        print('select2(0,4):')
        print(base_relation.select2(0,4).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_rename():
    print('rename(["studentID", "studentName", "studentAddress", "studentPhoneNum"]):')
    print(base_relation.rename(Header(["studentID", "studentName", "studentAddress", "studentPhoneNum"])).__str__())
    try:
        print('rename(["studentID", "studentName"]):')
        print(base_relation.rename(Header(["studentID", "studentName"])).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")

def test_project():
    print('project([1]):')
    print(base_relation.project([1]).__str__())
    
    print('project([2]):')
    print(base_relation.project([2]).__str__())
    
    print('project([3, 1]):')
    print(base_relation.project([3, 1]).__str__())
    
    print('project([3, 2, 1, 0]):')
    print(base_relation.project([3, 2, 1, 0]).__str__())
    try:
        print('project([4, 1])):')
        print(base_relation.project([4, 1]).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
        
        
    try:
        print('project([-1, 1])):')
        print(base_relation.project([-1, 1]).__str__())
    except ValueError as ve:
        print(f"  Value Error raised: {ve}\n")
    
    print('project([3, 2, 1, 0]):')
    print(base_relation.project([3, 2, 1, 0]).__str__())
    
    # this should have 1 Toople, with a length of 0, why is this the case?
    print('project([]):')
    print(base_relation.project([]).__str__())


# __name__ 
if __name__=="__main__": 
    print("Base Relation")
    print(base_relation.__str__())
    # test_select1()
    # test_select2()
    # test_rename()
    test_project()
    
    

# example code for the actual project

# def project3(input_string):
#     lexer: LexerFSM = LexerFSM()
#     lexer.run(input_string)
#     tokens: list[Token] = lexer.getTokens()

#     parser: Parser = Parser()
#     parser.run(tokens)
#     datalog_program: Datalog = parser.get_program()

#     interpreter: Interpreter = Interpreter()
#     print(interpreter.run(datalog_program))