from pathlib import Path

class NameInName(Exception):
    pass

def collect(path, student_name = None):
    if not isinstance(path, Path):
        path = Path(path)
    name_path = path / '.name.cfg'
    if name_path.exists():
        print(name_path)
    
