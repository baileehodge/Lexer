from .predicate import Predicate

class Rule():
    def __init__(self, head: Predicate, body: list[Predicate]):
        self.head_predicate = head
        self.body_predicates = body

    def rule_to_string(self) -> str:
        temp_str: str = self.head_predicate.to_string()
        temp_str += " :- "
        temp_str += ','.join([i.to_string() for i in self.body_predicates])
        return temp_str
    

    