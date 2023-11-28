from .predicate import Predicate
from .rule import Rule

class Datalog():
    def __init__(self, schemes: list[Predicate], facts: list[Predicate], rules: list[Rule], queries: list[Predicate]):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries

    def to_string(self) ->str:
        master_string: str = ""
        domains: list[str] = []
        master_string += (f'Schemes({len(self.schemes)}):\n')
        for scheme in self.schemes:
            master_string += (f'  {scheme.to_string()}\n')
        master_string += (f'Facts({len(self.facts)}):\n')
        for fact in self.facts:
            master_string += (f'  {fact.to_string()}.\n')
            for parameters in fact.parameters:
                domains.append(parameters.value)
            #fact_string: str = fact.basic_to_string()
            
            #domains.append(fact_string)
        master_string += (f'Rules({len(self.rules)}):\n')
        for rule in self.rules:
            master_string += (f'  {rule.rule_to_string()}.\n')
            
            
        master_string += (f'Queries({len(self.queries)}):\n')
        for query in self.queries:
            master_string += (f'  {query.to_string()}?\n')
            
        # create a set to keep track of the domain. DONE
        # add domains to the set as the function progresses
        # sort the set and put it in a list. DONE
        # format it like a domain list
        # add the list to the master string. DONE
        
        # unique_domains = set(domains)
        # sorted_domains = sorted(unique_domains)
        # final_domains_string = ",\n".join(sorted_domains)
        # master_string += final_domains_string
        
        # Sort the domains alphabetically
        sorted_domains = sorted(set(domains))
        #print(sorted_domains)
        master_string += f'Domain({len(sorted_domains)}):\n'
        for domain in sorted_domains:
            master_string += f'  {domain}\n'
        
        return master_string
    