
import pytest
from time import time

# Assuming miageru.database module and Term class are structured as planned
from miageru.database import open_db, list_terms_from_cursor_result, Term, save_terms

def now():
    return int(time())

def test_dataclass():
    new_entry = Term(
        term="ねこ",
        translation="cat",
        dictionary="A small carnivorous mammal (Felis catus) domesticated as a pet.",
        service="myougiden",
        date="2025-07-06 14:00:00.123"
    )
    print(f"New entry: {new_entry}")
    print(f"Term: {new_entry.term}, Service: {new_entry.service}")

    # Creating a Term record retrieved from the database (id is provided)
    retrieved_entry = Term(
        id=123,
        term="犬",
        translation="dog",
        service="google",
        date="2025-07-06 14:05:30.456",
        # Example with voice data (in a real scenario, 'voice' would be actual bytes)
        voice=b'\x00\x01\x02\x03',
        voice_format="mp3"
    )
    print(f"Retrieved entry: {retrieved_entry}")
    print(f"Translation: {retrieved_entry.translation}, Voice Format: {retrieved_entry.voice_format}")

    # A record from a service that doesn't provide all fields (e.g., dictd)
    dictd_entry = Term(
        id=45,
        term="example",
        dictionary="an example for illustration purposes.",
        service="dictd",
        date="2025-07-06 14:10:15.789"
        # translation, voice, voice_format remain None
    )
    print(f"Dictd entry: {dictd_entry}")
    print(f"Voice data present: {dictd_entry.voice is not None}")    



def test_list_terms_from_query_results():
    """
    Tests the list_terms_from_cursor_result function with in-memory database.
    """
    # 1. Get an in-memory SQLite connection
    conn = open_db(":memory:")
    cursor = conn.cursor()

    # 2. Populate two test rows
    # Note: Use current time for 'date' to ensure uniqueness for test runs
    time1 = now()
    cursor.execute(
        """INSERT INTO terms (term, translation, dictionary, service, date)
           VALUES (?, ?, ?, ?, ?)""",
        (
            "ねこ",
            "cat",
            "A small, carnivorous mammal (Felis catus) domesticated as a pet, known for purring and independent nature. Often depicted with nine lives.",
            "test_service",
            time1
        )
    )

    time2 = now()
    cursor.execute(
        """INSERT INTO terms (term, translation, dictionary, service, date)
           VALUES (?, ?, ?, ?, ?)""",
        (
            "いぬ",
            "dog",
            "A domesticated carnivorous mammal (Canis familiaris) typically having a long snout, an acute sense of smell, and a barking, howling, or whining voice. Often called 'man's best friend'.",
            "test_service",
            time2
        )
    )
    conn.commit()

    # 3. Test Query 1: Query for one specific term ("ねこ")
    cursor.execute("SELECT * FROM terms WHERE term = ?", ("ねこ",))
    neko_results = list_terms_from_cursor_result(cursor)

    assert len(neko_results) == 1, "Should find exactly one result for 'ねこ'"
    assert isinstance(neko_results[0], Term), "Result should be an instance of Term"
    assert neko_results[0].term == "ねこ"
    assert neko_results[0].translation == "cat"
    assert "purring" in neko_results[0].dictionary
    assert neko_results[0].service == "test_service"
    assert isinstance(neko_results[0].id, int) and neko_results[0].id > 0, "ID should be an integer"
    assert neko_results[0].voice is None
    assert neko_results[0].voice_format is None

    # 4. Test Query 2: Query for the service "test_service" to get two results
    cursor.execute("SELECT * FROM terms WHERE service = ?", ("test_service",))
    service_results = list_terms_from_cursor_result(cursor)

    assert len(service_results) == 2, "Should find exactly two results for 'test_service'"
    assert {term.term for term in service_results} == {"ねこ", "いぬ"}, \
           "Should contain both 'ねこ' and 'いぬ' terms"
    assert all(term.service == "test_service" for term in service_results), \
           "All results should be from 'test_service'"

    # Clean up: Close the connection
    conn.close()



def test_save_terms_upsert():
    """
    Tests the save_terms function for correct upsert behavior.
    """
    conn = open_db(":memory:")
    cursor = conn.cursor()

    # Initial data for "ねこ"
    initial_neko_time = now()
    cursor.execute(
        """INSERT INTO terms (term, translation, dictionary, service, date)
           VALUES (?, ?, ?, ?, ?)""",
        (
            "ねこ",
            "old cat translation",
            "This is the initial description for cat.",
            "test_service", # Use "test_service" as planned
            initial_neko_time
        )
    )
    conn.commit()

    # Verify initial state
    cursor.execute("SELECT * FROM terms WHERE term = 'ねこ' AND service = 'test_service'")
    initial_neko = list_terms_from_cursor_result(cursor)[0]
    assert initial_neko.dictionary == "This is the initial description for cat."
    assert initial_neko.date == initial_neko_time
    assert initial_neko.term == "ねこ"
    assert initial_neko.service == "test_service"

    initial_neko_id = initial_neko.id
    time_offset = 1             # make fake time

    # Create a list of Terms to update/insert
    terms_to_save = [
        # 1. Update entry for "ねこ" with different dictionary and new date
        Term(
            term="ねこ",
            translation="new cat translation",
            dictionary="A small domesticated carnivorous mammal with soft fur, often kept as a pet. Known for its graceful movements and independence.",
            service="test_service",
            date=now()+time_offset
        ),
        # 2. New entry for "うま"
        Term(
            term="うま",
            translation="horse",
            dictionary="A large, domesticated, herbivorous mammal, often used for riding, racing, or to carry loads. Known for its strength and speed.",
            service="test_service",
            date=now()+time_offset
        )
    ]

    # Call the new save_terms function
    save_terms(conn, terms_to_save)

    # Assertions after update/insert

    # Query for "ねこ" to verify update
    cursor.execute("SELECT * FROM terms WHERE term = 'ねこ' AND service = 'test_service'")
    updated_neko = list_terms_from_cursor_result(cursor)
    assert len(updated_neko) == 1, "After update, 'ねこ' should still have one entry"
    updated_neko = updated_neko[0]
    assert updated_neko.translation == "new cat translation", "Translation should be updated"
    assert "independence" in updated_neko.dictionary, "Dictionary should be updated"
    assert updated_neko.date != initial_neko_time, "Date should be updated (new timestamp)"
    assert updated_neko.id == initial_neko_id, "ID should remain the same for updated entry"

    # Query for "うま" to verify new insertion
    cursor.execute("SELECT * FROM terms WHERE term = 'うま' AND service = 'test_service'")
    uma_results = list_terms_from_cursor_result(cursor)
    assert len(uma_results) == 1, "New 'うま' entry should be present"
    uma_entry = uma_results[0]
    assert uma_entry.term == "うま"
    assert uma_entry.translation == "horse"
    assert "speed" in uma_entry.dictionary
    assert uma_entry.service == "test_service"
    assert isinstance(uma_entry.id, int) and uma_entry.id > 0, "New 'うま' entry should have an ID"

    # Verify total count in the table
    cursor.execute("SELECT COUNT(*) FROM terms WHERE service = 'test_service'")
    total_count = cursor.fetchone()[0]
    assert total_count == 2, "Total entries for 'test_service' should be 2 (1 updated, 1 new)"

    conn.close()
