import sqlite3
from dataclasses import dataclass
from typing import Optional, List



# class Context:
#     def __init__(self, dbfile):
#         self.dbfile = dbfile
#     def connect(self):
#         return open_db(self.dbfile)
#     def find_term(self, term, service=None):
#         pass


@dataclass
class Term:
    """
    Represents a single row from the 'translations' SQLite table.
    """
    term: str             # TEXT NOT NULL
    service: str          # TEXT NOT NULL
    date: int           # INTEGER NOT NULL
    id: Optional[int] = None  # INTEGER PRIMARY KEY AUTOINCREMENT
    translation: Optional[str] = None  # TEXT
    dictionary: Optional[str] = None   # TEXT
    voice: Optional[bytes] = None      # BLOB (Python's type for binary data)
    voice_format: Optional[str] = None # TEXT (e.g., 'mp3', 'ogg', 'wav')

def _row_to_term(row: sqlite3.Row) -> Term:
    """
    Helper function to convert a single sqlite3.Row object to a Term instance.
    """
    return Term(
        id=row['id'],
        term=row['term'],
        translation=row['translation'],
        dictionary=row['dictionary'],
        voice=row['voice'],
        voice_format=row['voice_format'],
        service=row['service'],
        date=row['date']
    )

def list_terms_from_cursor_result(cursor_result: sqlite3.Cursor) -> List[Term]:
    """
    Converts an sqlite3 cursor result (e.g., from a SELECT query)
    into a list of Term instances.

    Args:
        cursor_result: An sqlite3.Cursor object after executing a query.
                       Assumes the connection's row_factory is set to sqlite3.Row.

    Returns:
        A list of Term instances.
    """
    return [_row_to_term(row) for row in cursor_result]

def save_terms(conn: sqlite3.Connection, terms: List[Term]) -> None:
    """
    Inserts or updates a list of Term objects into the database.
    It replaces existing entries if the (term, service) pair is the same.

    Args:
        conn: The SQLite database connection.
        terms: A list of Term objects to save.
    """
    terms_data = []
    for term_obj in terms:
        terms_data.append({
            "term": term_obj.term,
            "translation": term_obj.translation,
            "dictionary": term_obj.dictionary,
            "voice": term_obj.voice,
            "voice_format": term_obj.voice_format,
            "service": term_obj.service,
            "date": term_obj.date,
            "id": term_obj.id # Include id, but it will be ignored by UPSERT's DO UPDATE unless specified
        })

    sql = """
    INSERT INTO terms (term, translation, dictionary, voice, voice_format, service, date)
    VALUES (:term, :translation, :dictionary, :voice, :voice_format, :service, :date)
    ON CONFLICT (term, service) DO UPDATE SET
        translation = EXCLUDED.translation,
        dictionary = EXCLUDED.dictionary,
        voice = EXCLUDED.voice,
        voice_format = EXCLUDED.voice_format,
        date = EXCLUDED.date;
    """

    cursor = conn.cursor()
    # `executemany` with a list of dictionaries works well with named parameters
    cursor.executemany(sql, terms_data)
    conn.commit()


def open_db(filename):

    def adapt_datetime(ts):
        return time.mktime(ts.timetuple())

    conn = sqlite3.connect(filename,
                           detect_types=sqlite3.PARSE_DECLTYPES |
                           sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL,
    service TEXT NOT NULL,
    translation TEXT,
    dictionary TEXT,
    voice BLOB,
    voice_format TEXT,
    date INTEGER DEFAULT (unixepoch()),
    UNIQUE(term, service)
    );''')
    cur.execute('''CREATE INDEX IF NOT EXISTS
    term_index ON terms(term);''')
    cur.execute('''CREATE INDEX IF NOT EXISTS
    translation_index ON terms(translation);''')
    cur.execute('''CREATE INDEX IF NOT EXISTS
    dictionary_index ON terms(dictionary);''')
    conn.commit()
    return conn


