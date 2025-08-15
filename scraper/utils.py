class Map:
    def __init__(self, mapping: dict):
        self.mapping = mapping

    def get(self, key: str) -> str:
        key = key.upper()
        if key not in self.mapping:
            raise ValueError(f"Unknown key: {key}")
        return self.mapping[key]
