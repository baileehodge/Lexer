from Header import Header
from Toople import Toople

class Relation:
    def __init__(self, name: str, header: Header, tooples: set = None) -> None:
        self.name: str = name
        self.header: Header = header
        if tooples is None:
            tooples = set()
        self.toople: set[Toople] = tooples
        
        
    def __str__(self) -> str:
        output_str: str = ""
        for toople in sorted(self.toople):
            if len(toople.values) == 0:
                continue
            sep: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += self.header.values[i]
                output_str += "="
                output_str += toople.values[i]
                sep = ", "
            output_str += "\n"
        return output_str
        
    def add_toople(self, toople: Toople) -> None:
        if len(toople.values) != len(self.header.values):
            length = len(self.header.values)
            raise ValueError("Tuple was not the same length as Header of length {length}")
        self.toople.add(toople)
    
    def select1(self, value: str, index: int) -> 'Relation':
        # Select type 1 will take an index and a constant value
        # make an empty relation
        # fill the relation
        # return the relation
        
        #checks that the index is in range
        if index >= len(self.header.values):
            raise ValueError
        if index < 0:
            raise ValueError
        
        

        new_name = self.name
        new_header = self.header
        new_tooples = set()
        
        for toople in self.toople:
            if toople.values[index] == value:
                new_tooples.add(toople)
        
        return Relation(new_name, new_header, new_tooples)
    
    def select2(self, index1: int, index2: int) -> 'Relation': 
    # Select type 2 will take two indexes
    # make an empty relation
    # fill the relation
    # return the relation
    
        if index1 >= len(self.header.values):
            raise ValueError
        if index1 < 0:
            raise ValueError
        if index2 >= len(self.header.values):
            raise ValueError
        if index2 < 0:
            raise ValueError
    
        new_name = self.name
        new_header = self.header
        new_tooples = set()
        
        for toople in self.toople:
            if toople.values[index1] == toople.values[index2]:
                new_tooples.add(toople)
        
        if len(new_tooples) <= 0:
            return None
        
        return Relation(new_name, new_header, new_tooples)

    def rename(self, new_header: Header) -> 'Relation':
    # make an empty relation
    # fill the relation
    # return the relation
        new_name = self.name
        new_tooples = self.toople
        
        return Relation(new_name, new_header, new_tooples)
        
    def project(self, col_indices: list[int]) -> 'Relation':
    # make an empty relation
    # fill the relation
    # return the relation
    
        #checks that the index is in range
        for index in col_indices: 
            if index >= len(self.header.values) | index < 0:
                raise ValueError
    
        new_name = self.name
        #temp_list: list[str] = [self.header.values[i] for i in col_indices]
        temp_list: list[str] = [self.header.values[i] for i in col_indices if 0 <= i < len(self.header.values)] 
        #will this cause issues later? (T_T)

        new_header = Header(temp_list)
        new_tooples = set()
        
        
        for toople in self.toople:
            new_values = [toople.values[i] for i in col_indices if 0 <= i < len(toople.values)]
            new_tooples.add(Toople(new_values))
            
        return Relation(new_name, new_header, new_tooples)