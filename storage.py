import json

class SecureStorage:
    def save_file(self, filename, encrypted_package):

        full_name = filename + ".secure"
        with open(full_name, "w") as f:
            json.dump(encrypted_package, f, indent=4)
        print(f"   [Disk I/O] File saved securely as '{full_name}'")

    def load_file(self, filename):

        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None