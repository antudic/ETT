isIter = lambda arg: isinstance(arg, list) or isinstance(arg, tuple)
# ^ allows program to handle tuples and lists
# ^ the above code is the same as the below code
# 
#def isIter(arg):
#    return (isinstance(arg, list) or isinstance(arg, tuple))

def createTable(name: str, fields: dict):
    # fields format example:
    # {"ID": ["INT", "PRIMARY KEY"], "NAME": ["TEXT", "NOT NULL"]}
    # OR
    # {"ID": "INT PRIMARY KEY", "NAME": "TEXT NOT NULL"}
    
    query = f"CREATE TABLE {name}("

    for fName, fArgs in fields.items(): # fieldName, fieldArgs
        
        if isIter(fArgs): # convert to string if iter
            fArgs = " ".join(fArgs)
        
        query+= f"\n{fName} {fArgs},"

    query = query[:-1] # remove trailing ","
    query+= ");" # add ending

    return query


def addColumn(tableName: str, columnName: str, args: tuple | str):
    
    if isIter(args): args = " ".join(args)
        
    return f"ALTER TABLE {tableName} ADD COLUMN '{columnName}' {args};"


def getColumns(name: str):
    return f"PRAGMA TABLE_INFO({name});"


def insert(tableName: str, values: tuple | dict, columns=None):
    query = f"INSERT INTO {tableName} "
    
    if columns:
        values, columns = columns, values # switch to correct order
        query+= f"{str(columns)} VALUES{str(values)}"
    
    elif isIter(values):
        values = str(values)[1:-1]
        # The "str.join" method does not work with non-string types
        query+= f"VALUES({values})"

    else:
        # Below is an atrocious line of code. Don't do this.
        query+= " VALUES".join(map(str, map(tuple, (values.keys(), values.values()))))
        
    query+= ";"
    
    return query


def select(tableName,
           conditions: list = None,
           orderBy: str = None,
           limit: int = None):

    conditions = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    orderBy = f" ORDER BY {orderBy}" if orderBy else ""
    limit = f" LIMIT {limit}" if limit else ""
    
    return f"SELECT * FROM {tableName}{conditions}{orderBy}{limit};"











