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
        self.interpret_rules()
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
        self.output_str += "Query Evaluation\n"
        for query in self.datalog_program.queries:
            result_relation = self.evaluate_predicate(query)
            self.output_str += query.to_string() + "? "
            if len(result_relation.toople) == 0:
                self.output_str += 'No\n'
            else:
                self.output_str += f'Yes({len(result_relation.toople)})\n'
                temp_str: str = str(result_relation)
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



    def interpret_rules(self) -> None:
        # fixed point algorithm to evaluate rules goes here:
        # this will call evaluate_rule over and over again
        self.output_str += "Rule Evaluation\n"
        changed: bool = True
        passes: int = 0
        
        while (changed):
            changed = False
            for rule in self.datalog_program.rules:
                size_change = self.evaluate_rule(rule)
                if size_change > 0:
                    changed = True
            passes += 1
        
        self.output_str += f"\nSchemes populated after {passes} passes through the Rules.\n\n"
        
        pass
    
    # this function should return the number of unique tuples added to the database
    def evaluate_rule(self, rule: Rule) -> int:
        #print head
        head_pred_params: str = ""
        for i, param in enumerate(rule.head_predicate.parameters):
            head_pred_params += f"{param.value}"
            if i < len(rule.head_predicate.parameters) - 1:
                head_pred_params += ","
        self.output_str += f"{rule.head_predicate.name}({head_pred_params}) :- "
        #print body
        for i, pred in enumerate(rule.body_predicates):
            self.output_str += f"{pred.name}("
            for j, param in enumerate(pred.parameters):
                self.output_str += f"{param.value}"
                if j < len(pred.parameters) - 1:
                    self.output_str += ","
            
            self.output_str += ")"
            if i < len(rule.body_predicates) - 1:
                self.output_str += ","
        
        self.output_str += f".\n"
        
        intermediate_results: list[Relation] = []
        the_intermediate_result: Relation = None
        
        for body_predicate in rule.body_predicates:
            result = self.evaluate_predicate(body_predicate) #returns a relation
            intermediate_results.append(result)

        
        if len(intermediate_results) > 1:
            the_intermediate_result = intermediate_results[0] 

            for next_result in intermediate_results[1:]:
                the_intermediate_result = the_intermediate_result.natural_join(next_result)
        elif len(intermediate_results) == 1:
            the_intermediate_result = intermediate_results[0]
        else:
            print("Error 404, no body predicates found\n")
            the_intermediate_result = result
        
        
        variable_first_occurrence = {}
        keep_i: list[int] = []
        
        for i, param in enumerate(rule.head_predicate.parameters):
            for j, para in enumerate(the_intermediate_result.header.values):
                if param.value == para:
                    keep_i.append(j)
                    if param.value not in variable_first_occurrence:
                        variable_first_occurrence[param.value] = i
                    
                

        the_intermediate_result = the_intermediate_result.project(keep_i) 
        data_relation: Relation = self.database.get_relation(rule.head_predicate.name)
        
        result = the_intermediate_result.rename(data_relation.header)

        size_before = len(data_relation.toople)
        new_tooples: list[Toople] = []
        print_relation: Relation = ''
        
        new_tooples = data_relation.union(result)
        print_relation = Relation("", Header([p.value for p in result.header.values]), new_tooples)
        self.output_str += print_relation.__str__()
        #print new tooples
        
        # Save the size of the database relation after calling union
        size_after = len(data_relation.toople)
        
        return size_after - size_before
    