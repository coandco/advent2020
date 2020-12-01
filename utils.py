from pathlib import Path
import inspect


# Grab my input data from the automatically-named file generated by get_data.py
def read_data():
    caller_filename = inspect.stack()[1].filename
    filename = Path(f'inputs/{Path(caller_filename).stem}_input.txt')
    return filename.read_text()
