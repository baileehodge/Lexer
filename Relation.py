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
            raise ValueError(f"Tuple was not the same length as Header of length {length}")
        self.toople.add(toople)
        
######################################################

    def can_join_tooples(self, toople1: Toople, toople2: Toople, overlap: list[tuple[int,int]]) -> bool:
        for x,y in overlap:
            if toople1.values[x] != toople2.values[y]:
                return False
        return True
        
    def join_tooples(self, toople1: Toople, toople2: Toople, unique_cols_1: list[int]) -> Toople:
        toople_values: list[str] = []
        for x in unique_cols_1:
            toople_values.append(toople1.values[x])
        toople_values.extend(toople2.values)
        return Toople(toople_values)
        
        # append puts an item at the end of a list
        # extend ads a list to the end of another list
        
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        header_values: list[str] = []
        for x in unique_cols_1:
            header_values.append(header1.values[x])
        header_values.extend(header2.values)
        return Toople(header_values)
        
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        
        for x in range(len(r1.header.values)):
            is_unique: bool = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
                if is_unique:
                    unique_cols_1.append(x)
                    
        
        #Change function call to join_headers(?). Change it so that it uses overlap instead of unique_cols_1. Use overlap to make a more accurate unique_cols ? We want to tell join_headers which columns of which relations
        #update: determined that this modification would likely be unnecessary
        
        # calculate the correct values for overlap, and unique_cols_1
                    
        # make the header h for the result relation
        #     (combine r1's header with r2's header)
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)
        # make a new empty relation r using header h
        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.toople:
            for t2 in r2.toople:
                if self.can_join_tooples(t1, t2, overlap):
                    result_toople = self.join_tooples(t1, t2, unique_cols_1)
                    result.add_toople(result_toople)

        # 	if t1 and t2 can join
        # 	    join t1 and t2 to make tuple t
        # 	    add tuple t to relation r
        # 	end if

        #     end for
        # end for
        
        return result
    
    def union(self, other: 'Relation') -> list[Toople]: 
        #returns a list of unique tuples
        #like natural_join, but this time we actually change the database        
        new_tooples_list: list[Toople] = []
        #print(f"Type of self.header.values: {type(self.header.values)}")
        
        for toople in other.toople: 
            if toople not in self.toople: 
                self.toople.add(toople)
                new_tooples_list.append(toople)
        return new_tooples_list
        
######################################################
    
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
        new_name = self.name
        new_tooples = self.toople
        
        return Relation(new_name, new_header, new_tooples)
        
    def project(self, col_indices: list[int]) -> 'Relation':
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
    