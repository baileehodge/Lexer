from RelationDemo import Relation
from RowDemo import Row
from HeaderDemo import Header
from typing import Dict

# imports from project 2
from project_2.datalog import Datalog
from project_2.predicate import Predicate
from project_2.token import Token
from project_2.lexer_fsm import LexerFSM
from project_2.parse import Parser
from project_2.rule import Rule

class Interpreter:
    
    
    def interpret_rules(self) -> None:
        # fixed point algorithm to evaluate rules goes here:
        pass
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Predicate) -> int:
        # Step 1:
        
        # Evaluate the predicates on the right-hand side of the rule (the body predicates):

        # For each predicate on the right-hand side of a rule, 
        #   evaluate the predicate in the same way you evaluated the queries in the last project (using select, project, and rename operations). 
        #   Each predicate should produce a single relation as an intermediate result. 
        #   If there are n predicates on the right-hand side of a rule, 
        #   there should be n intermediate results.
        
        # HINT: 
        #   if you used the EvaluatePredicate function as suggested in lab 3
        #   you should only need to call that function once per 
        #   body predicate and store the result
        
        # Example:
        # for body_predicate in rule.body:
        # result = self.evaluate_predicate(body_predicate))

        # Step 2:
        # Join the relations that result:

        # If there are two or more predicates on the right-hand side of a rule, 
        #   join the intermediate results to form the single result for Step 2. 
        #   Thus, if p1, p2, and p3 are the intermediate results from Step 1, join them 
        #   (p1 |x| p2 |x| p3) into a single relation.
        
        

        # If there is a single predicate on the right hand side of the rule, 
        # use the single intermediate result from Step 1 as the result for Step 2.

        # Step 3:
        # Project the columns that appear in the head predicate:

        # The predicates in the body of a rule may have variables 
        #   that are not used in the head of the rule. 
        #   The variables in the head may also appear in a different order 
        #   than those in the body. Use a project operation on the result from 
        #   Step 2 to remove the columns that don't appear in the head of the 
        #   rule and to reorder the columns to match the order in the head.

        # Step 4:
        # Rename the relation to make it union-compatible:
        
        # Rename the relation that results from Step 3 to 
        #   make it union compatible with the relation that 
        #   matches the head of the rule. Rename each attribute 
        #   in the result from Step 3 to the attribute name found 
        #   in the corresponding position in the relation 
        #   that matches the head of the rule.

        # Step 5:
        # Union with the relation in the database:

        # Save the size of the database relation before calling union
        size_before: int = 0
        
        # Union the result from Step 4 with the relation 
        # in the database whose name matches the name of the head of the rule.
        
        
        # Save the size of the database relation after calling union
        size_after: int = 10
        # int = len(rel.rows) or something like that
        
        return size_after - size_before

        