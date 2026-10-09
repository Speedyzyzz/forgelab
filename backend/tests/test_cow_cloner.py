import tempfile
import sqlite3
from app.cloner.sqlite_cow import CopyOnWriteCloner

def test_cow_cloning_subsecond():
    with tempfile.TemporaryDirectory() as tmp_dir:
        cloner = CopyOnWriteCloner(tmp_dir)
        schema = "CREATE TABLE users (id TEXT PRIMARY KEY, email TEXT, name TEXT);"
        seed_data = [
            {"id": "usr_1", "email": "bob@org.com", "name": "Bob Jones"},
            {"id": "usr_2", "email": "carol@org.com", "name": "Carol Danvers"}
        ]
        hints = {"id": "id", "email": "email", "name": "name"}

        tpl_path = cloner.create_template("prod_users", schema, seed_data, hints)
        assert tpl_path is not None

        # Provision Clone
        clone_info = cloner.provision_clone("prod_users", "agent_sandbox_clone_1")
        assert clone_info["provision_latency_ms"] < 500.0  # Sub-second guarantee!

        # Verify cloned database contains anonymized seed data
        conn = sqlite3.connect(clone_info["connection_string"].replace("sqlite:///", ""))
        rows = conn.cursor().execute("SELECT id, email, name FROM users").fetchall()
        assert len(rows) == 2
        # Ensure email was pseudonymized
        assert rows[0][1].endswith("@synthetic-forgelab.internal")
        conn.close()

        # Teardown clone
        assert cloner.destroy_clone("agent_sandbox_clone_1") is True
