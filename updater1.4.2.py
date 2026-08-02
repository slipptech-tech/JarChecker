import urllib.request
import json

class UpdateChecker:
    def __init__(self, current_version: str = "v1.0.0"):
        self.current_version = current_version
        self.api_url = "https://api.github.com/repos/slipptech-tech/JarChecker/releases/latest"

    def check_for_updates(self) -> None:
        print("[*] Checking for updates...")
        try:
            req = urllib.request.Request(
                self.api_url, 
                headers={"User-Agent": "JarChecker-Client"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name")
                
                if latest_version and latest_version != self.current_version:
                    print(f"[!] New version available: {latest_version} (Current: {self.current_version})")
                else:
                    print("[OK] You are using the latest version.")
        except Exception as e:
            print(f"[-] Could not check for updates: {e}")

if __name__ == "__main__":
    checker = UpdateChecker()
    checker.check_for_updates()