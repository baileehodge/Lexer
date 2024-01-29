from typing import Dict
from Relation import Relation

class Database:
    def __init__(self) -> None:
        self.relations: Dict[str, Relation] = {}

    def add_relation(self, relation: Relation) -> None:
        self.relations[relation.name] = relation

    def get_relation(self, name: str) -> Relation:
        return self.relations[name]
    
    def remove_relation(self, name: str) -> None:
        if name in self.relations:
            del self.relations[name]
            
    def get_database(self) -> Dict[str, Relation]:
        return self.relations
