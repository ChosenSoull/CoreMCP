import os
import shlex
import subprocess
from pathlib import Path

def run_command(query: str):
    """Execute a CLI command inside my PC. My PC Windows 10 22H2.
    Parameters
    ----------
    query: str
        Target command.
    Returns
    -------
    string output.
    """
    try:
        is_windows = os.name == "nt"
        args = shlex.split(query, posix=not is_windows)
        
        result = subprocess.run(
                args, 
                shell=is_windows,
                capture_output=True,
                text=True,
                check=True
            )
        return result.stdout if result.stdout else "Command executed successfully (no output)."
    except subprocess.CalledProcessError as e:
        return f"Command failed with error:\n{e.stderr}"
    except Exception as e:
        return f"System error: {e}"

def list_directory(dir_path: str = "E:/", recursive: bool = False) -> str:
    """List files and directories in the specified path.
    Parameters
    ----------
    dir_path : str
        The target directory path to inspect.
    recursive : bool
        Whether to recursively inspect subdirectories.
    Returns
    -------
    str
        A formatted list of files and directories found in the specified path.
    """
    try:
        path = Path(dir_path).resolve()

        if not path.exists():
            return f"Error: Directory '{dir_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{dir_path}' is not a directory."

        items = []
        if recursive:
            for item in path.glob("**/*"):
                prefix = "[DIR] " if item.is_dir() else "[FILE]"
                items.append(f"{prefix} {item.relative_to(path)}")
                if len(items) >= 500:
                    items.append(
                        "... (output truncated, found more than 500 items)"
                    )
                    break
        else:
            for item in path.iterdir():
                prefix = "[DIR] " if item.is_dir() else "[FILE]"
                items.append(f"{prefix} {item.name}")

        return "\n".join(items) if items else "(Directory is empty)"

    except Exception as e:
        return f"Error viewing directory: {e}"


def read_file(file_path: str, max_bytes: int = 100000) -> str:
    """Read the content of a text file.
    Parameters
    ----------
    file_path : str
        The target path of the file to read.
    max_bytes : int
        Maximum size limit in bytes to prevent reading overly large files.
    Returns
    -------
    str
        The text content of the file or an error message.
    """
    try:
        path = Path(file_path).resolve()

        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not path.is_file():
            return f"Error: Specified path '{file_path}' is a directory."

        if path.stat().st_size > max_bytes:
            return f"Warning: File is too large ({path.stat().st_size} bytes). Limit is: {max_bytes} bytes."

        content = path.read_text(encoding="utf-8", errors="replace")
        return content if content else "(File is empty)"

    except Exception as e:
        return f"Error reading file: {e}"


def write_file(file_path: str, content: str, append: bool = False) -> str:
    """Write or append text content to a file.
    Parameters
    ----------
    file_path : str
        The target path of the file to write to.
    content : str
        The text content to write into the file.
    append : bool
        If True, appends content to the existing file instead of overwriting it.
    Returns
    -------
    str
        A status message confirming the operation result.
    """
    try:
        path = Path(file_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if append else "w"
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)

        action = "appended" if append else "created/overwritten"
        return f"File successfully {action}: {path}"

    except Exception as e:
        return f"Error writing to file: {e}"


def search_files(
    pattern: str, search_path: str = "E:/", max_results: int = 100
) -> str:
    """Search for files and directories matching a pattern across the specified path.
    Parameters
    ----------
    pattern : str
        Search pattern or wildcard (e.g., '*.json', '*minecraft*', 'launch.exe').
    search_path : str
        Root path to start the search from (e.g., 'C:/', 'E:/', 'E:/Programs').
    max_results : int
        Maximum number of matching results to return.
    Returns
    -------
    str
        A list of paths matching the search criteria or a status message.
    """
    try:
        root_path = Path(search_path).resolve()

        if not root_path.exists():
            return f"Error: Search root path '{search_path}' does not exist."

        found_items = []
        for item in root_path.rglob(pattern):
            prefix = "[DIR] " if item.is_dir() else "[FILE]"
            found_items.append(f"{prefix} {item}")

            if len(found_items) >= max_results:
                break

        if not found_items:
            return f"No items found matching '{pattern}' in '{search_path}'."

        result = "\n".join(found_items)
        if len(found_items) >= max_results:
            result += (
                f"\n... (found more than {max_results} matches, output limited)"
            )

        return result

    except Exception as e:
        return f"Error searching files: {e}"


def run_program(
    target_path: str, args: str = "", background: bool = True
) -> str:
    """Execute an executable program or file.
    Parameters
    ----------
    target_path : str
        Path to the executable or file (e.g., 'E:/Minecraft/LL.exe').
    args : str
        Optional command line arguments to pass to the executable.
    background : bool
        If True, launches the process in non-blocking background mode.
    Returns
    -------
    str
        Execution status or output produced by the program.
    """
    try:
        path = Path(target_path).resolve()

        if not path.exists():
            return f"Error: Executable file not found: {target_path}"

        full_command = f'"{path}" {args}'.strip()

        if background:
            subprocess.Popen(
                full_command,
                shell=True,
                creationflags=subprocess.DETACHED_PROCESS,
            )
            return f"Program successfully launched in background mode: {path.name}"
        else:
            res = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            out = res.stdout if res.stdout else "Program finished with no output."
            if res.returncode != 0:
                out += f"\nStderr: {res.stderr}"
            return out

    except Exception as e:
        return f"Error launching program: {e}"