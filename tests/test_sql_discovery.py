import subprocess


command = (
    'sqlcmd -S localhost -C '
    '-Q "SELECT name FROM sys.databases"'
)

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    shell=True,
)

print()
print("RETURN CODE")
print(result.returncode)

print()
print("STDOUT")
print(result.stdout)

print()
print("STDERR")
print(result.stderr)