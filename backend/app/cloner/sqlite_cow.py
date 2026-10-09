import os
import shutil
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.config import settings
from app.cloner.anonymizer import DataAnonymizer

class CopyOnWriteCloner:
    def __init__(self, storage_root: Optional[str] = None):
        self.root = Path(storage_root or settings.DEFAULT_STORAGE_ROOT)
        self.templates_dir = self.root / "templates"
        self.clones_dir = self.root / "clones"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.clones_dir.mkdir(parents=True, exist_ok=True)
        self.anonymizer = DataAnonymizer()

    def create_template(self, template_name: str, schema_sql: str, seed_rows: List[Dict[str, Any]], schema_hints: Dict[str, str]) -> str:
        tpl_path = self.templates_dir / f"{template_name}.db"
        if tpl_path.exists():
            tpl_path.unlink()

        conn = sqlite3.connect(tpl_path)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)

        # Anonymize seed data before writing to production replica template
        anon_rows = self.anonymizer.anonymize_dataset(seed_rows, schema_hints)

        for row in anon_rows:
            cols = ", ".join(row.keys())
            placeholders = ", ".join(["?"] * len(row))
            sql = f"INSERT INTO users ({cols}) VALUES ({placeholders})"
            cursor.execute(sql, list(row.values()))

        conn.commit()
        conn.close()
        return str(tpl_path)

    def provision_clone(self, template_name: str, clone_id: str) -> Dict[str, Any]:
        """
        Creates an isolated, production-faithful database replica in sub-second latency.
        """
        tpl_path = self.templates_dir / f"{template_name}.db"
        if not tpl_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' does not exist.")

        clone_path = self.clones_dir / f"{clone_id}.db"
        start_time = time.time()
        shutil.copyfile(tpl_path, clone_path)
        latency_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "clone_id": clone_id,
            "template_name": template_name,
            "connection_string": f"sqlite:///{clone_path}",
            "provision_latency_ms": latency_ms,
            "created_at": time.time()
        }

    def destroy_clone(self, clone_id: str) -> bool:
        clone_path = self.clones_dir / f"{clone_id}.db"
        if clone_path.exists():
            clone_path.unlink()
            return True
        return False
