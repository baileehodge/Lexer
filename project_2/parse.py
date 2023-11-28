from .datalog import Datalog
from .rule import Rule
from .parameter import Parameter
from .predicate import Predicate
from .token import Token

class Parser():
    def __init__(self):
        self.index = 0
        self.tokens = []
        
        self.schemes: list[Predicate] = []
        self.facts: list[Predicate] = []
        self.rules: list[Rule] = []
        self.queries: list[Predicate] = []
        
        self.program: Datalog = []
        
    def get_program(self):
        return self.program
        
    def add_to(self, type: str, predicate: Predicate):
        if type == "scheme":
            self.schemes.append(predicate)
        if type == "fact":
            self.facts.append(predicate)
        if type == "query":
            self.queries.append(predicate)

    def add_to_rules(self, rule: Rule):
        self.rules.append(rule)

    def throw_error(self):
        raise ValueError (self.get_curr_token().to_string())
    
    def advance(self):
        self.index += 1

    def get_curr_token(self) -> Token:
        if self.index >= len(self.tokens):
            self.index = len(self.tokens) - 1
            self.throw_error()
        while self.tokens[self.index].token_type == "COMMENT":
            self.advance()
        return self.tokens[self.index]
        
    def get_prev_token_value(self) -> str:
        return self.tokens[self.index - 1].value

    def match(self, expected_type: str):
        #print(f"Current token: {self.get_curr_token().to_string()}, Expected token type: {expected_type}")
        
        if self.get_curr_token().token_type == expected_type:
            #print(f"Matching current token {self.get_curr_token().to_string()} with expected type {expected_type}")  # Debugging statement

            self.advance()
        else:
            self.throw_error()

    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0 
        self.tokens: list[Token] = tokens

        try:
            datalog_items: Datalog = self.parse_datalogProgram()
            return "Success!\n" + datalog_items.to_string()
            # scheme: Predicate = self.parse_scheme()
            # return "Success!\n" + scheme.to_string()      
        except ValueError as ve:
            return f"Failure!\n  {ve}"
        
    #datalogProgram	->	SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF
    def parse_datalogProgram(self) -> Datalog:        
        self.match("SCHEMES")
        self.match("COLON")
        self.parse_scheme()
        self.parse_schemeList()
        self.match("FACTS")
        self.match("COLON")
        self.parse_factList()
        self.match("RULES")
        self.match("COLON")
        self.parse_ruleList()
        self.match("QUERIES")
        self.match("COLON")
        self.parse_query()
        self.parse_queryList()
        self.match("EOF")
        
        self.program = Datalog(self.schemes, self.facts, self.rules, self.queries )
        return self.program
        
    # schemeList -> scheme, schemeList | lambda
    def parse_schemeList(self) -> list[Predicate]:
        predicates: list[Predicate] = []
        
        if self.get_curr_token().token_type == "ID":
            predicates.append(self.parse_scheme())
            predicates.append(self.parse_schemeList())
            return predicates
        else:
            return []

    # factList -> fact, factList | lambda
    def parse_factList(self) -> list[Predicate]:
        predicates: list[Predicate] = []
        
        if self.get_curr_token().token_type == "ID":
            predicates.append(self.parse_fact())
            predicates.append(self.parse_factList())
            return predicates
        else:
            return []
        
    # ruleList -> fact, ruleList | lambda
    def parse_ruleList(self):
        #rules: list[Rule] = []
        
        if self.get_curr_token().token_type == "ID":
            #rules.append(self.parse_rule())
            #rules.extend(self.parse_ruleList())
            self.parse_rule()
            self.parse_ruleList()
            return
        else:
            return []
        
    # queryList -> query, queryList | lambda
    def parse_queryList(self):

        if self.get_curr_token().token_type == "ID":
            self.parse_query()
            self.parse_queryList()
            return
        else:
            return 



    # scheme 	-> 	ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_scheme(self) -> Predicate:
        name: str = ""
        parameters: list[Parameter] = []
        
        self.match("ID")
        name = self.get_prev_token_value()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(Parameter(self.get_prev_token_value(), True))
        parameters.extend(self.parse_idList())
        self.match("RIGHT_PAREN")
        self.add_to("scheme", Predicate(name, parameters))
        
        return Predicate(name, parameters)
    
    # fact -> ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
    def parse_fact(self) -> Predicate: 
        name: str = ""
        parameters: list[Parameter] = []
        
        self.match("ID")
        name = self.get_prev_token_value()
        self.match("LEFT_PAREN")
        self.match("STRING")
        temp: str= self.get_prev_token_value()
        parameters.append(Parameter(temp, False))
        parameters.extend(self.parse_stringList())
        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        self.add_to("fact", Predicate(name, parameters))
        
        return Predicate(name, parameters)


    # rule -> headPredicate COLON_DASH predicate predicateList PERIOD
    #TODO: Fix
    def parse_rule(self):
        temp: Rule()
        
        temp_pred: Predicate = self.parse_headPredicate()
        self.match("COLON_DASH")
        temp_pred_list: list[Predicate] = [self.parse_predicate()]
        #temp_pred_list.extend(self.parse_predicateList())
        new_preds: list[Predicate] = self.parse_predicateList()
        for predicate in new_preds:
                temp_pred_list.append(predicate)
        
        self.match("PERIOD")
        self.add_to_rules(Rule(temp_pred, temp_pred_list))


    #query -> predicate Q_MARK
    def parse_query(self) -> Predicate:
        pred: Predicate = self.parse_predicate()
        
        self.match("Q_MARK")
        
        self.add_to("query", pred)
        return pred
    
## 

    # headPredicate -> ID LEFT_PAREN ID idList RIGHT_PAREN
    def parse_headPredicate(self) -> Predicate:
        name: str = ""
        parameters: list[str] = []
        
        name = self.get_curr_token().value
        self.match("ID")
        name = self.get_prev_token_value()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(Parameter(self.get_prev_token_value(), True))
        parameters.extend(self.parse_idList())
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters)
        
    # predicate -> ID LEFT_PAREN parameter parameterList RIGHT_PAREN
    def parse_predicate(self) -> Predicate:
        name = self.get_curr_token().value 
        self.match("ID")
        self.match("LEFT_PAREN")
        parameters = [self.parse_parameter()] 
        parameters += self.parse_parameterList() 
        self.match("RIGHT_PAREN")
        return Predicate(name, parameters) 

## 
    
    # predicateList -> COMMA predicate predicateList | lambda
    def parse_predicateList(self) -> list[Predicate]:
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            first_pred: list[Predicate] = [self.parse_predicate()]
            pred_list: list[Predicate] = self.parse_predicateList()
            #return first_pred + pred_list
            #return_val = first_pred.extend(pred_list)
            for predicate in pred_list:
                first_pred.append(predicate)
            return first_pred
        else:
            return []

    # parameterList -> COMMA parameter parameterList | lambda
    def parse_parameterList(self) -> list[Parameter]:
        parameters: list[Parameter] = []
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            parameters.append(self.parse_parameter())
            parameters.extend(self.parse_parameterList())
            return parameters
        else:
            return []

    # stringList - > COMMA STRING stringList | lambda
    def parse_stringList(self) -> list[Parameter]:
        parameters: list[Parameter] = []
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            temp: str = self.get_prev_token_value()
            parameters.append(Parameter(temp, False))
            parameters.extend(self.parse_stringList())
            return parameters
        
        else:
            return []

    # parameter -> STRING | ID
    def parse_parameter(self) -> Parameter:
        if self.get_curr_token().token_type == "STRING":
            self.match("STRING")
            return Parameter(self.get_prev_token_value(), False)
        elif self.get_curr_token().token_type == "ID":
            self.match("ID")
            return Parameter(self.get_prev_token_value(), True)
        else:
            self.throw_error()
            

    # idList  	-> 	COMMA ID idList | lambda
    def parse_idList(self) -> list[Parameter]:
        # the first set is {COMMA} << TODO: add a similar statement in all functions
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("ID")
            p = Parameter(self.get_prev_token_value(), True)
            p_list: list[Parameter] = []
            p_list.append(p)
            #what else?
            #curr_id: list[str] = [self.get_prev_token_value()]
            # [Name]
            #rest_ids: list[str] = self.parse_idList()
            temp_list: list[Parameter] = self.parse_idList()
            if (len(temp_list) != 0 ):
                p_list.extend(temp_list)
            return p_list
            
            # [Address, PhoneNumber]
            #return curr_id + rest_ids
            # -> [Name, Address, PhoneNumber]
        
        #lambda
        else:
            return []
        
        
        
        #remeber to add () or to_string and other functions
        
        # detailed plan