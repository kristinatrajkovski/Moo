import sqlite3


def query(query_text, *param):
    conn = sqlite3.connect ('mooooo.db')
    cur = conn.cursor()
    cur.execute(query_text, param)

    column_names = []
    for column in cur.description:
        column_names.append(column[0])

    rows = cur.fetchall()
    dicts= []
    if rows == []:
        dicts = [{'Symptoms':'healthy', 'Illnesses':'most likely alright!'}]
    print(rows)
    for row in rows:
        d = dict(zip(column_names, row))
        dicts.append(d)
    conn.close()
    return dicts


def get_all():
    return query("""SELECT * FROM MOooo GROUP BY Symptom""")

def get_filtered(symptom):
    return query("""SELECT * FROM MOooo WHERE Symptom = ? """, symptom)