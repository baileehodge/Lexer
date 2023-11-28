from HeaderDemo import Header
from RowDemo import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set[Row]) -> None:
        self.name: str = name
        self.header: Header = header
        self.rows: set[Row] = rows
    
    def __str__(self) -> str:
        result_str = f"Relation: {self.name}\n"
        result_str += str(self.header) + "\n"

        for row in self.rows:
            result_str += str(row) + "\n"

        return result_str
        
    def add_row(self, row: Row):
        if len(row.values) != len(self.header.values):
            raise ValueError("Row and header must be the same length")
        self.rows.add(row)

    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x,y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
        return True
        
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        row_values: list[str] = []
        for x in unique_cols_1:
            row_values.append(row1.values[x])
        row_values.extend(row2.values)
        return Row(row_values)
        
        # append puts an item at the end of a list
        # extend ads a list to the end of another list
        
        
    
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        header_values: list[str] = []
        for x in unique_cols_1:
            header_values.append(header1.values[x])
        header_values.extend(header2.values)
        return Row(header_values)
    
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        #do some weird in range thing here
        
        for x in len(r1.header.values):
            is_unique: bool = True
            for y in len(r2.header.values):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
                if is_unique:
                    unique_cols_1.append(x)
        
        # calculate the correct values for overlap, and unique_cols_1
                    
        # make the header h for the result relation
        #     (combine r1's header with r2's header)
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)
        # make a new empty relation r using header h
        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1, t2, overlap):
                    result_row = self.join_rows(t1, t2, unique_cols_1)
                    result.add_row(result_row)

        # 	if t1 and t2 can join
        # 	    join t1 and t2 to make tuple t
        # 	    add tuple t to relation r
        # 	end if

        #     end for
        # end for
        
        return result