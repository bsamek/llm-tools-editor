# LLM File Tools Plugin

This is a plugin for the [`llm`](https://llm.datasette.io/) CLI that provides useful file manipulation tools:

- **Read File**: Read the contents of a file.
- **List Files**: List files and directories at a given path.
- **Apply Diff**: Edit files by applying diffs in a simple, structured format.

Shell commands are intentionally **not** implemented as tools.

## Installation

First, clone or download this repository, then run:

```bash
llm install .
```

## Tools Provided

- **read_file(path)**: Reads and returns the contents of the file at the given path.
- **list_files(path=".")**: Lists files and directories at the given path (adds `/` for directories).
- **apply_diff(diff)**: Applies one or more edits using a diff block format:
    ```
    path/to/file.py
    <<<<<<< SEARCH
    old text
    =======
    new text
    >>>>>>> REPLACE
    ```
    Each diff block edits one file and replaces `old text` with `new text`.

## Usage

Once installed, these tools will be available for use with LLM models via the `llm` CLI or associated interfaces.

## Notes

- Only the diff edit format is supported for file editing.
