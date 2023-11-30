from Relation import Relation
from Toople import Toople
from Header import Header
from Database import Database
from typing import Dict

# imports from project 2
from project_2.datalog import Datalog
from project_2.predicate import Predicate
from project_2.rule import Rule
from project_2.token import Token
from project_2.lexer_fsm import LexerFSM
from project_2.parse import Parser

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database = Database()
    
    def run(self, datalog_program: Datalog) -> str:
        self.datalog_program: Datalog = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        # self.interpret_rules()
        self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None: 
        # Start with an empty Database. 
        # For each scheme in the Datalog program, 
        #   add an empty Relation to the Database. 
        #   Use the scheme name as the name of the relation 
        #   and the attribute list from the scheme as the header of the relation.

        for scheme in self.datalog_program.schemes:
            relation_name: str = scheme.name
            relation_attr = Header(scheme.parameters)
            relation = Relation(relation_name, relation_attr) 
            self.database.add_relation(relation)
    
    def interpret_facts(self) -> None:
        # For each fact in the Datalog program, 
        #   add a Tuple to a Relation. 
        #   Use the predicate name from the fact to 
        #   determine the Relation to which the Tuple should be added. 
        #   Use the values listed in the fact to provide the values for the Tuple.
        for fact in self.datalog_program.facts: 
            fact_name = fact.name
            fact_attr: list[str] = [param.value for param in fact.parameters]
            toople: Toople = Toople(fact_attr)
            self.database.get_relation(fact_name).add_toople(toople)    

    def interpret_queries(self) -> None:
        # for each query in the datalog_program call evaluate predicate.
        # append the predicate returned by this function to the output string
        
        for query in self.datalog_program.queries:
            result_relation = self.evaluate_predicate(query)
            self.output_str += query.to_string() + "? "
            if len(result_relation.toople) == 0:
                self.output_str += 'No\n'
            else:
                self.output_str += f'Yes({len(result_relation.toople)})\n'
                temp_str: str = str(result_relation)
                #temp_str += ...
                self.output_str += temp_str
        
        # output notes:
        # For each query, output the query and a space. 
        # If the relation resulting from evaluating the query is empty, output 'No'. 
        # If the resulting relation is not empty, output 'Yes(n)' where n is the number of tuples in the resulting relation.
        
        # If there are variables in the query, output the tuples from the resulting relation.

        # Output each tuple on a separate line as a comma-space-separated list of pairs.
        # Each pair has the form N='V', 
        # where N is the attribute name from the header and V is the value from the tuple. 
        # Output the name-value pairs in the same order as the variable names appear in the query. 
        # Indent the output of each tuple by two spaces.
        
        # some of this output code was given to you in the Relation.__str__() function. 
        # It may need to be modified slightly

        # Output the tuples in sorted order. 
        # Sort the tuples alphabetically based on the values in the tuples. 
        # Sort first by the value in the first position and if needed up to the value in the nth position.
    
###########################################################
    # def evaluate_queries(self, predicate: Predicate) -> Relation:
    #     relation = self.database.get_relation(predicate.name)
        
    #     const_indices = []
    #     const_values = []
    #     variable_values = []
    #     variable_indices = []
    #     duplicate_indices = []
        
    #     for i, param in enumerate(predicate.parameters): 
    #         if param.value.startswith("'") and param.value.endswith("'"):
    #             const_indices.append(i)
    #             const_values.append(param.value)
    #         else:
    #             variable_indices.append(i)
    #             if (param.value not in variable_values): 
    #                 variable_values.append(param.value)
    #             else:
    #                 duplicate_indices.append(i)
        
    #     relation = relation.select1(const_values, const_indices)
    #     relation = relation.project(variable_indices)
    #     relation = relation.rename(Header(variable_values))
        
    #     return relation
################################################################  
    def evaluate_predicate(self, query: Predicate) -> Relation:
        relation: Relation = self.database.get_relation(query.name)
        
        if relation is None:
            raise ValueError(f"Relation '{query.name}' does not exist in the database.")

        variable_first_occurrence = {}
        keep_i: list[int] = []
        keep_val: list[str] = []

        for i, parameter in enumerate(query.parameters):
            if not parameter.is_id:
                relation = relation.select1(parameter.value, i)
                if relation is None:
                    raise ValueError("The result of select1 is None.")
            else: 
                if parameter.value in variable_first_occurrence:
                    #variable_first_occurrence[parameter.value] = i
                    index1: int = variable_first_occurrence[parameter.value]
                    relation = relation.select2(index1, i)
                    if relation is None:
                        raise ValueError("The result of select2 is None.")
                else:
                    variable_first_occurrence[parameter.value] = i
                    keep_i.append(i)
                    keep_val.append(parameter.value)

        new_header: Header = Header(keep_val)

        relation = relation.project(keep_i)
        if relation is None:
            raise ValueError("The result of project is None.")
        relation = relation.rename(new_header)
        
        return relation


    # def evaluate_queries(self) -> None:
    #     for query in self.datalog_program.queries: 
    #         self.evaluate_predicate(query) 
    #     return


#################################################################

# ──────────██▄▄───────
# ──────────██▀▀───────
# ────────▄███▄────────
# ──────▄█████─────────
# ─▀▄▄▀▀──█▄─█▄────────
        # For this predicate you need to
        #   use a sequence of select, project, and rename operations on the Database 
        #   to evaluate the query. Evaluate the queries in the order given in the input.
        # Get the Relation from the Database with the 
        #   same name as the predicate name in the query.
        # Use one or more select operations to select 
        #   the tuples from the Relation that match the query. Iterate over the parameters of the query: If the parameter is a constant, select the tuples from the Relation that have the same value as the constant in the same position as the constant. If the parameter is a variable and the same variable name appears later in the query, select the tuples from the Relation that have the same value in both positions where the variable name appears.
        # After selecting the matching tuples, use the project operation 
        #   to keep only the columns from the Relation that correspond to the 
        #   positions of the variables in the query. Make sure that each variable name appears only once in the resulting relation. If the same name appears more than once, keep the first column where the name appears and remove any later columns where the same name appears. (This makes a difference when there are other columns in between the ones with the same name.)
        # After projecting, use the rename operation to 
        #   rename the header of the Relation to the
        #   names of the variables found in the query.
        # The operations must be done in the order described above: 
        #   any selects, 
        #   followed by a project, 
        #   followed by a rename.
        # return the new predicate
    
    # this will be implemented during project 4 #####################################
    def interpret_rules(self) -> None:
        # fixed point algorithm to evaluate rules goes here:
        # this will call evaluate_rule over and over again
        pass
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Rule) -> int:
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
        intermediate_results: list[Relation] = []
        the_intermediate_result: Relation = None
        
        for body_predicate in enumerate(rule.body_predicates):
            result = self.evaluate_predicate(body_predicate) #returns a relation
            intermediate_results.append(result)

        # Step 2:
        # Join the relations that result:

        # If there are two or more predicates on the right-hand side of a rule, 
        #   join the intermediate results to form the single result for Step 2. 
        #   Thus, if p1, p2, and p3 are the intermediate results from Step 1, join them 
        #   (p1 |x| p2 |x| p3) into a single relation.
        
        

        # If there is a single predicate on the right hand side of the rule, 
        # use the single intermediate result from Step 1 as the result for Step 2.
        
        if len(intermediate_results) > 1:
            the_intermediate_result = intermediate_results[0] 

            for next_result in intermediate_results[1:]:
                the_intermediate_result = the_intermediate_result.natural_join(next_result)
        elif len(intermediate_results) == 1:
            the_intermediate_result = intermediate_results[0]
        else:
            print("Error 404, no body predicates found\n")
            the_intermediate_result = result
        

        # Step 3:
        # Project the columns that appear in the head predicate:

        # The predicates in the body of a rule may have variables 
        #   that are not used in the head of the rule. 
        #   The variables in the head may also appear in a different order 
        #   than those in the body. Use a project operation on the result from 
        #   Step 2 to remove the columns that don't appear in the head of the 
        #   rule and to reorder the columns to match the order in the head.
        
        variable_first_occurrence = {}
        keep_i: list[int] = []
        
        for i, param in enumerate(rule.head_predicate.parameters):
            if param.is_id and param.value not in variable_first_occurrence:
                variable_first_occurrence[param.value] = i
                keep_i.append(i)
                

        the_intermediate_result = the_intermediate_result.project(keep_i) #call it with a list of integers... how do we get the integers? in the head predicate. It's all the parameters that are a variable


        # Step 4:
        # Rename the relation to make it union-compatible:
        
        # Rename the relation that results from Step 3 to 
        #   make it union compatible with the relation that 
        #   matches the head of the rule. Rename each attribute 
        #   in the result from Step 3 to the attribute name found 
        #   in the corresponding position in the relation 
        #   that matches the head of the rule.
        
        the_intermediate_result = the_intermediate_result.rename(rule.head_predicate)


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