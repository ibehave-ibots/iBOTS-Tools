from pathlib import Path


class Filesystem:
    
    @staticmethod
    def _(data: bytes, path: Path):
        path.write_bytes(data=data)
        
    @staticmethod
    def write_text(data: str, path: Path):
        path.write_text(data)