import sqlite3

conn = sqlite3.connect("photos.db")
cursor = conn.cursor()

cursor.execute("""create table if not exists phyla_characteristics(
                phyla_characteristics_id integer primary key,
                phyla_characteristics_t text not null unique
                );""")

cursor.execute("""create table if not exists name_classes(
                class_id integer primary key,
                class_name text not null unique
                );""")

cursor.execute("""create table if not exists phyla(
                phylum_id integer primary key,
                phylum_name text not null unique
                );""")

cursor.execute("""create table if not exists phyla_and_characteristics(
                phyla_characteristics_id integer,
                phylum_id integer,
                photo blob,
                foreign key (phyla_characteristics_id) references phyla_characteristics(phyla_characteristics_id),
                foreign key (phylum_id) references phyla(phylum_id)
                );""")

cursor.execute("""create table if not exists classes(
                phylum_id integer,
                class_id integer,
                photo blob,
                foreign key (phylum_id) references phyla(phylum_id),
                foreign key (class_id) references classes(class_id)
                );""")

conn.close()


def convert(filename):
    with open(filename, "rb") as file:
        blob_data = file.read()
    return blob_data


def exists(table, column, value):
    c = sqlite3.connect("photos.db")
    cur = c.cursor()
    prompt = f"select exists(select 1 from {table} where {column} = (:value));"
    cur.execute(prompt, {"value": value})
    existence = cur.fetchone()[0]
    c.close()
    return existence


def insert(table, column, value):
    c = sqlite3.connect("photos.db")
    cur = c.cursor()
    prompt = f"insert into {table} ({column}) values (:value);"
    cur.execute(prompt, {"value": value})
    c.commit()
    c.close()


def select_one(table, column_selected, column_condition, value):
    c = sqlite3.connect("photos.db")
    cur = c.cursor()
    prompt = f"select {column_selected} from {table} where {column_condition} = (:value);"
    cur.execute(prompt, {"value": value})
    fetched_value = cur.fetchone()[0]
    c.close()
    return fetched_value


def select_many(table, column_selected, column_condition, value):
    c = sqlite3.connect("photos.db")
    cur = c.cursor()
    prompt = f"select {column_selected} from {table} where {column_condition} = (:value);"
    cur.execute(prompt, {"value": value})
    fetched_value = cur.fetchall()
    c.close()
    return fetched_value


def select_unusual(prompt, to_replace, dict_value):
    c = sqlite3.connect("photos.db")
    cur = c.cursor()
    cur.execute(prompt, {to_replace: dict_value})
    fetched_value = cur.fetchall()
    c.close()
    return fetched_value


def display_phyla(range_temp):
    range_id = [phylum_id[0] for chunk, phylum_id in enumerate(range_temp) if phylum_id not in range_temp[:chunk]]
    range_id = tuple(range_id)
    prompt = f"""select phylum_name from phyla where phylum_id in {range_id};"""
    option = select_unusual(prompt, None, None)
    return option
