import hmac
import hashlib
from typing import Any, Dict, List

try:
    import blake3
    def keyed_hash(key: str, data: str) -> str:
        return blake3.blake3(data.encode("utf-8"), key=key.encode("utf-8")[:32].ljust(32, b"0")).hexdigest()
except ImportError:
    def keyed_hash(key: str, data: str) -> str:
        return hmac.new(key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()

class DataAnonymizer:
    def __init__(self, secret_key: str = "forgelab_default_anonymization_key_2026"):
        self.secret_key = secret_key
        # Memoization cache to ensure strict 1:1 mapped referential integrity
        self._id_cache: Dict[str, str] = {}

    def anonymize_id(self, original_id: Any) -> str:
        s_id = str(original_id)
        if s_id not in self._id_cache:
            digest = keyed_hash(self.secret_key, f"id:{s_id}")[:12]
            self._id_cache[s_id] = f"anon_id_{digest}"
        return self._id_cache[s_id]

    def anonymize_email(self, original_email: str) -> str:
        digest = keyed_hash(self.secret_key, f"email:{original_email.lower()}")[:10]
        return f"user_{digest}@synthetic-forgelab.internal"

    def anonymize_name(self, original_name: str) -> str:
        digest = keyed_hash(self.secret_key, f"name:{original_name}")[:8]
        return f"Synthetic User {digest}"

    def anonymize_record(self, record: Dict[str, Any], schema_hints: Dict[str, str]) -> Dict[str, Any]:
        """
        Anonymizes a database row based on schema hints (e.g. {"user_id": "id", "email": "email", "name": "name"}).
        """
        anon_row = dict(record)
        for field, f_type in schema_hints.items():
            if field in anon_row and anon_row[field] is not None:
                val = anon_row[field]
                if f_type == "id" or field.endswith("_id") or field == "id":
                    anon_row[field] = self.anonymize_id(val)
                elif f_type == "email":
                    anon_row[field] = self.anonymize_email(str(val))
                elif f_type == "name":
                    anon_row[field] = self.anonymize_name(str(val))
        return anon_row

    def anonymize_dataset(self, rows: List[Dict[str, Any]], schema_hints: Dict[str, str]) -> List[Dict[str, Any]]:
        return [self.anonymize_record(r, schema_hints) for r in rows]
