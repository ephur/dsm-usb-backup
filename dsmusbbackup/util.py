import os
import subprocess
import shlex


def pipe_exec(args, stdin=None, cwd=None, env=None):
    """
    A function to accept a list of commands and pipe them together.

    Takes optional stdin to give to the first item in the pipe chain. It returns a tuple of, exit code, stdout, stderr, with empty outputs being None.
    """
    count = 0
    commands = []
    if env is None:
        env = os.environ.copy()

    if not isinstance(args, list):
        args = [args]

    for i in args:
        if count == 0:
            if stdin is None:
                commands.append(subprocess.Popen(shlex.split(i), stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE, cwd=cwd, env=env))
            else:
                commands.append(subprocess.Popen(shlex.split(i), stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=cwd, env=env))
        else:
            commands.append(subprocess.Popen(shlex.split(i), stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, stdin=commands[count -
                                                                                    1].stdout, cwd=cwd,
                                             env=env))
        count = count + 1

    if stdin is not None:
        stdin_bytes = stdin.encode()
        if len(commands) > 1:
            commands[0].communicate(input=stdin_bytes)
            stdout, stderr = commands[-1].communicate()
            commands[-1].wait()
            returncode = commands[-1].returncode
        else:
            stdout, stderr = commands[0].communicate(input=stdin_bytes)
            commands[0].wait()
            returncode = commands[0].returncode
    else:
        stdout, stderr = commands[-1].communicate()
        commands[-1].wait()
        returncode = commands[-1].returncode

    return (returncode, stdout, stderr)
