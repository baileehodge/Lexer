from Relation import Relation
from Header import Header
from Toople import Toople

def test_can_join_tooples():
    # Create two tooples with overlapping values
    toople1 = Toople(['\'12345\'', '\'John\'', '\'123 Main St.\'', '\'555-1234\''])
    toople2 = Toople(['\'54321\'', '\'Doe\'', '\'123 Main St.\'', '\'555-4321\''])
    toople3 = Toople(['\'12345\'', '\'Doe\'', '\'123 Main St.\'', '\'555-4321\''])
    
    # Define the overlap as a list of tuples representing column indices
    overlap = [(0, 0), (2, 2)]  # Assuming the first and third columns overlap
    rel = Relation("test", Header([]), set())
    print(f"Can Join toople1 and toople2: {rel.can_join_tooples(toople1, toople2, overlap)}")
    print(f"Can Join toople2 and toople3: {rel.can_join_tooples(toople2, toople3, overlap)}")
    print(f"Can Join toople1 and toople3: {rel.can_join_tooples(toople1, toople3, overlap)}")
    print()


def test_join_headers():
    # Create two headers
    header1 = Header(["ID", "Name", "Address"])
    header2 = Header(["Course", "ID", "Grade"])
    
    # Define the columns from header1 that should be unique in the result
    unique_cols_1 = [1, 2]  # Assuming the first and third columns are unique
    
    # Test the join operation for headers
    result = Relation("test", Header([]), set()).join_headers(header1, header2, unique_cols_1)
    print("Join Headers")
    print(result)
    print()


def test_join_tooples():
    # Create two tooples
    toople1 = Toople(['\'12345\'', '\'John\'', '\'123 Main St.\''])
    toople2 = Toople(['\'CS101\'', '\'12345\'', '\'A\''])
    
    # Define the columns from toople1 that should be unique in the result
    unique_cols_1 = [1, 2]  # Assuming the first and third columns are unique
    
    # Test the join operation for tooples
    result = Relation("test", Header([]), set()).join_tooples(toople1, toople2, unique_cols_1)
    print("Join tooples")
    print(result)
    print()
    


def test_natural_join():
    snap_t1 = Toople(['\'33333\'', '\'Snoopy\'', '\'12 Apple St.\'', '\'555-1234\''])
    snap_t2 = Toople(['\'12345\'', '\'C. Brown\'', '\'12 Apple St.\'', '\'555-1234\''])
    snap_t3 = Toople(['\'22222\'', '\'P. Patty\'', '\'56 Grape Blvd\'', '\'555-9999\''])

    csg_t1 = Toople(['\'cs101\'', '\'12345\'', '\'A\''])
    csg_t2 = Toople(['\'cs101\'', '\'22222\'', '\'B\''])
    csg_t3 = Toople(['\'cs101\'', '\'33333\'', '\'C\''])
    csg_t4 = Toople(['\'EE200\'', '\'12345\'', '\'B+\''])
    csg_t5 = Toople(['\'EE200\'', '\'22222\'', '\'B\''])

    h1 = Header(["StudentID", "Name", "Address", "Phone"])
    h2 = Header(["Course", "StudentID", "Grade"])

    r1 = Relation("snap", h1, set([snap_t1, snap_t2, snap_t3]))
    r2 = Relation("csg", h2, set([csg_t1, csg_t2, csg_t3, csg_t4, csg_t5]))

    # Performing natural join and printing the result
    result = r1.natural_join(r2)
    print("Natural Join r1 and r2")
    print(result)
    print()



if __name__ == "__main__":
    test_can_join_tooples()
    test_join_headers()
    test_join_tooples()
    test_natural_join()