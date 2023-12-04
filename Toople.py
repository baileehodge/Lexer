# this is sometimes called tuple, I am renaming it to help be specific
class Toople:
    def __init__(self, values: list[str]) -> None:
        self.values: list[str] = values
    
    def __eq__(self, other: 'Toople') -> bool:
        return self.values == other.values
        
    # def __eq__(self, other):
    #     if isinstance(other, Toople):
    #         return self.values == other.values
    #     return False
        
    def __hash__(self) -> int:
        return hash(tuple(self.values))
        #casting it to a tuple so that we can hash the value directly rather than the memory address
    
    def __lt__(self, other: 'Toople') -> bool:
        return self.values < other.values  # <=  like the demo code?
        
    def by_list(ele: 'Toople'): 
        return ele.values
    
    def __str__(self) -> str:
        return f"{', '.join(self.values)}"