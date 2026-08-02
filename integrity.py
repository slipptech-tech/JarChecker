import hashlib
from pathlib import Path

class IntegrityChecker:
    @staticmethod
    def calculate_sha256(file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return "File not found."

    @classmethod
    def verify_file(cls, file_path: str, expected_hash: str) -> bool:
        path = Path(file_path)
        print(f"[*] Calculating hash for: {path.name}...")
        actual_hash = cls.calculate_sha256(path)
        
        print(f"    Expected: {expected_hash}")
        print(f"    Actual:   {actual_hash}")

        return actual_hash.lower() == expected_hash.lower()

if __name__ == "__main__":
    target = "OpenSource.zip"
    if Path(target).exists():
        sample_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        result = IntegrityChecker.verify_file(target, sample_hash)
        if result:
            print("[OK] Checksum matches! File is secure.")
        else:
            print("[!] Checksum mismatch!")
    else:
        print(f"[-] Target file {target} not found for verification.")