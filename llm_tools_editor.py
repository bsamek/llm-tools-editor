import os
import glob
import re
from typing import List, Union
import llm

def read_file(path: str) -> str:
    """
    Read the contents of a given file path.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading '{path}': {e}"

def list_files(path: str = ".") -> Union[List[str], str]:
    """
    List files and directories at a given path.
    Appends a '/' to directory names.
    """
    try:
        entries = glob.glob(os.path.join(path, "*"))
        out: List[str] = []
        for e in entries:
            if os.path.isdir(e):
                out.append(e.rstrip(os.sep) + "/")
            else:
                out.append(e)
        return out
    except Exception as e:
        return f"Error listing '{path}': {e}"

def apply_diff(diff: str) -> str:
    """
    Apply a diff in the 'diff' edit format, e.g.:

    path/to/file.py
    <<<<<<< SEARCH
    old text
    =======
    new text
    >>>>>>> REPLACE

    You can include multiple file-blocks in one diff string.
    """
    pattern = re.compile(
        r"^(.+?)\r?\n<<<<<<< SEARCH\r?\n(.*?)\r?\n=======\r?\n(.*?)\r?\n>>>>>>> REPLACE",
        re.MULTILINE | re.DOTALL,
    )

    applied_files = []
    for match in pattern.finditer(diff):
        path, old, new = match.group(1).strip(), match.group(2), match.group(3)
        if not os.path.exists(path):
            return f"Error: file '{path}' does not exist."
        try:
            content = open(path, "r", encoding="utf-8").read()
        except Exception as e:
            return f"Error reading '{path}': {e}"
        if content.count(old) != 1:
            return (
                f"Error: expected exactly one occurrence of SEARCH block in '{path}', "
                f"found {content.count(old)}."
            )
        updated = content.replace(old, new, 1)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)
        except Exception as e:
            return f"Error writing '{path}': {e}"
        applied_files.append(path)

    if not applied_files:
        return "No diff blocks found or did not match expected format."
    return f"Applied diff to: {', '.join(applied_files)}"

@llm.hookimpl
def register_tools(register):
    register(read_file)
    register(list_files)
    register(apply_diff)

