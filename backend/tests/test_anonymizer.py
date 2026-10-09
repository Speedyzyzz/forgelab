from app.cloner.anonymizer import DataAnonymizer

def test_deterministic_anonymization_and_fk_integrity():
    anon = DataAnonymizer("test_secret_key_123")

    user_id_raw = 42
    author_id_raw = 42  # Matching foreign key!

    anon_user_id = anon.anonymize_id(user_id_raw)
    anon_author_id = anon.anonymize_id(author_id_raw)

    # Referential integrity invariant: equal IDs must map to identical pseudonym
    assert anon_user_id == anon_author_id
    assert anon_user_id.startswith("anon_id_")

    # Format checks
    email = anon.anonymize_email("Alice@Company.com")
    assert email.endswith("@synthetic-forgelab.internal")
    assert "alice" not in email

    name = anon.anonymize_name("Alice Smith")
    assert name.startswith("Synthetic User ")
