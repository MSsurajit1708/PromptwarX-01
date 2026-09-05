import json
import re

class AIParser:
    @staticmethod
    def parse_json(raw_text):
        if not raw_text:
            return None
        cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
        cleaned = re.sub(r'\s*```$', '', cleaned)
        try:
            return json.loads(cleaned)
        except Exception:
            match = re.search(r'(\[.*\]|\{.*\})', cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
        return None
