# this is sometimes called tuple, I am renaming it to separate it from the built-in tuple class
class Toople:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values
    
    def __eq__(self, other: 'Toople') -> bool:
        return self.values == other.values
        
        
    def __hash__(self) -> int:
        return hash(tuple(self.values))
        #casting it to a tuple so that we can hash the value directly rather than the memory address
    
    def __lt__(self, other: 'Toople') -> bool:
        return self.values < other.values  
        
    def by_list(ele: 'Toople'): 
        return ele.values
    
    def __str__(self) -> str:
        return f"{', '.join(self.values)}"