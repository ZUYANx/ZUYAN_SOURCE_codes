import marshal
import base64
import hashlib
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import DOUBLE

console = Console()

# XOR function for encryption/decryption
def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encode_file(file_path, key):
    if not os.path.isfile(file_path):
        return None, None, f"[red]Error:[/] File '{file_path}' not found."
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        
        compiled = compile(code, file_path, "exec")
        marshaled = marshal.dumps(compiled)

        # Encrypt marshaled code
        encrypted = xor_bytes(marshaled, key)

        # Base64 encode encrypted code
        encoded = base64.b64encode(encrypted).decode()

        # Compute hash of original marshaled code for integrity check
        hash_digest = hashlib.sha256(marshaled).hexdigest()

        return encoded, hash_digest, None
    except Exception as e:
        return None, None, f"[red]Error:[/] {e}"

def write_encoded_file(encoded_code, hash_digest, key, output_path):
    # XOR decrypt function inside the loader stub
    loader_code = f'''
# Encoded by ZUYAN
# GitHub: https://github.com/ZUYANx

import marshal, base64, hashlib

def xor_bytes(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

key = {list(key)}  # Key as list of ints

encoded_data = "{encoded_code}"
expected_hash = "{hash_digest}"

encrypted = base64.b64decode(encoded_data)
decrypted = xor_bytes(encrypted, bytes(key))

actual_hash = hashlib.sha256(decrypted).hexdigest()
if actual_hash != expected_hash:
    raise RuntimeError("Code integrity check failed!")

code = marshal.loads(decrypted)
exec(code)
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(loader_code)

def main():
    console.print(Panel.fit("MARSHAL + BASE64 + XOR FILE ENCODER (Harder)", style="bold green", box=DOUBLE))
    
    file_path = Prompt.ask("[cyan]Enter the path to your .py file[/cyan]").strip()

    # Choose your XOR key here — keep it secret and reasonably long
    key = b"ZUYAN_SECRET_KEY_12345"

    encoded, hash_digest, error = encode_file(file_path, key)
    
    if error:
        console.print(error)
        return

    output_path = os.path.splitext(file_path)[0] + "_enx.py"
    write_encoded_file(encoded, hash_digest, key, output_path)

    console.print(Panel.fit("✅ [bold green]Encoding complete![/bold green]", box=DOUBLE))
    console.print(f"[bold yellow]Output saved to:[/] [green]{output_path}[/green]")
    console.print("[bold cyan]Encoded by ZUYAN | GitHub: https://github.com/ZUYANx[/bold cyan]")

if __name__ == "__main__":
    main()