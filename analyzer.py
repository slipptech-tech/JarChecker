import os
import zipfile
from pathlib import Path

class JarAnalyzer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.suspicious_extensions = {".exe", ".bat", ".cmd", ".vbs", ".js", ".scr"}

    def scan_directory(self) -> None:
        if not self.target_dir.exists():
            print(f"[-] Directory not found: {self.target_dir}")
            return

        jar_files = list(self.target_dir.glob("**/*.jar"))
        print(f"[*] Found {len(jar_files)} JAR file(s) to analyze.")

        for jar_path in jar_files:
            self._analyze_single_jar(jar_path)

    def _analyze_single_jar(self, jar_path: Path) -> None:
        print(f"\n[+] Analyzing: {jar_path.name}")
        try:
            with zipfile.ZipFile(jar_path, 'r') as archive:
                file_list = archive.namelist()
                suspicious_found = []

                for file_name in file_list:
                    ext = Path(file_name).suffix.lower()
                    if ext in self.suspicious_extensions:
                        suspicious_found.append(file_name)

                print(f"    - Total files inside: {len(file_list)}")
                if suspicious_found:
                    print(f"    [!] WARNING: Suspicious files detected:")
                    for sf in suspicious_found:
                        print(f"        -> {sf}")
                else:
                    print(f"    [OK] No obvious threats found in structure.")

        except zipfile.BadZipFile:
            print(f"    [ERROR] File is corrupted or not a valid ZIP/JAR archive.")
        except Exception as e:
            print(f"    [ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyzer = JarAnalyzer(".")
    analyzer.scan_directory()