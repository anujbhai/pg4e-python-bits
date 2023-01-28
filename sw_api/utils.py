def query_value(cur, sql, fields=None, error=None):
    row = query_row(cur, sql, fields, error);
    if row is None : return None
    return row[0]

def query_row(cur, sql, fields=None, error=None):
    row = do_query(cur, sql, fields)
    try:
        row = cur.fetchone()
        return row
    except Exception as e:
        if error:
            print(error, e)
        else:
            print(e)
        return  None

def do_query(cur, sql, fields=None):
    row = cur.execute(sql, fields)
    return row
