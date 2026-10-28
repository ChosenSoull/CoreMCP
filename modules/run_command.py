import subprocess

def run_command(query: str):
    """Execute a CLI command inside a secure Docker container.
    Parameters
        ----------
        query: str
            Target command.
        
        Returns
        -------
        string output.
    """
    try:
        safe_command = query.replace("'", "'\\''")
        docker_cmd = f"docker exec ai-sandbox bash -c '{safe_command}'"
        result = subprocess.run(
                docker_cmd, 
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
        return result.stdout if result.stdout else "Command executed successfully (no output)."
    except subprocess.CalledProcessError as e:
        return f"Command failed with error:\n{e.stderr}"
    except Exception as e:
        return f"System error: {e}"