import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import base64
import os
import time
from PIL import Image, ImageTk

# --- Import your existing modules ---
try:
    from symmetric import AESEngine
    from quantum_engine import QuantumEngine
    from storage import SecureStorage
except ImportError:

    print("⚠️ Modules not found. Ensure symmetric.py, quantum_engine.py, and storage.py exist.")


class SecureOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Secure OS Layer - Group 17")
        self.root.geometry("1050x800")  # Increased size slightly for the visualizer
        self.root.configure(bg="#1e1e1e")

        # --- Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#00ff00", font=("Consolas", 10))
        style.configure("TButton", font=("Consolas", 11, "bold"), background="#333", foreground="white", borderwidth=1)
        style.map("TButton", background=[("active", "#444")])

        self.logo_photo = None
        try:
            img = Image.open("logo.png")
            target_width = 400
            aspect_ratio = img.height / img.width
            target_height = int(target_width * aspect_ratio)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Initialize Crypto Engines
        self.aes = None
        self.quantum = None
        self.storage = None

        # Show Login Screen first
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.login_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo_photo:
            logo_label = tk.Label(self.login_frame, image=self.logo_photo, bg="#1e1e1e")
            logo_label.pack(pady=(0, 20))

        tk.Label(self.login_frame, text="QUANTUM ENCRYPTION LAYER", bg="#1e1e1e", fg="#00ff00",
                 font=("Consolas", 22, "bold")).pack(pady=10)
        tk.Label(self.login_frame, text="Secure OS File Storage", bg="#1e1e1e", fg="white", font=("Consolas", 14)).pack(
            pady=(0, 20))

        tk.Label(self.login_frame, text="Username:", bg="#1e1e1e", fg="#aaa", font=("Consolas", 12)).pack(anchor="w")
        self.entry_user = tk.Entry(self.login_frame, font=("Consolas", 12), bg="#333", fg="white",
                                   insertbackground="white", width=30)
        self.entry_user.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#1e1e1e", fg="#aaa", font=("Consolas", 12)).pack(anchor="w")
        self.entry_pass = tk.Entry(self.login_frame, font=("Consolas", 12), bg="#333", fg="white", show="*",
                                   insertbackground="white", width=30)
        self.entry_pass.pack(pady=5)

        tk.Button(self.login_frame, text="AUTHENTICATE", command=self.perform_login, bg="#005500", fg="white",
                  font=("Consolas", 12, "bold"), padx=20, pady=10).pack(pady=30)

        self.status_label = tk.Label(self.login_frame, text="Status: System Locked", bg="#1e1e1e", fg="gray",
                                     font=("Consolas", 10))
        self.status_label.pack()

    def perform_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if user == "admin" and pwd == "secure123":
            self.status_label.config(text="Access Granted. Loading Kernels...", fg="yellow")
            self.root.update()
            time.sleep(1)

            # Check if modules exist before initializing
            try:
                self.aes = AESEngine()
                self.quantum = QuantumEngine()
                self.storage = SecureStorage()
                self.show_dashboard()
            except NameError:
                messagebox.showerror("Error", "Crypto modules (symmetric.py, etc) not found.\nCannot start engine.")
        else:
            messagebox.showerror("Access Denied", "Invalid Credentials.\nIncident Reported.")

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- Main Layout ---
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- HEADER ---
        header_frame = tk.Frame(main_frame, bg="#1e1e1e")
        header_frame.pack(fill="x", pady=(0, 20))

        if self.logo_photo:
            logo_label = tk.Label(header_frame, image=self.logo_photo, bg="#1e1e1e")
            logo_label.pack(side="left", padx=(0, 20))

        title_frame = tk.Frame(header_frame, bg="#1e1e1e")
        title_frame.pack(side="left", fill="both")
        tk.Label(title_frame, text="SECURE PQC FILE SYSTEM", bg="#1e1e1e", fg="#00ff00",
                 font=("Consolas", 24, "bold")).pack(anchor="w")
        tk.Label(title_frame, text="User: Admin | made by: Manil Laroussi, Mohammed Elsafi,\n Moustafa Nasser", bg="#1e1e1e", fg="cyan", font=("Consolas", 12)).pack(anchor="w")

        tk.Button(header_frame, text="LOGOUT", command=self.show_login_screen, bg="#550000", fg="white").pack(
            side="right", anchor="ne")

        content_frame = tk.Frame(main_frame, bg="#1e1e1e")
        content_frame.pack(fill="both", expand=True)

        # --- Controls (Left) ---
        controls_frame = tk.LabelFrame(content_frame, text=" Command Center ", bg="#1e1e1e", fg="white",
                                       font=("Consolas", 12, "bold"))
        controls_frame.pack(side="left", fill="both", expand=False, padx=(0, 10), ipadx=10)

        tk.Label(controls_frame, text="Target Filename:", bg="#1e1e1e", fg="#aaa").pack(anchor="w", padx=10,
                                                                                        pady=(15, 0))
        self.filename_entry = tk.Entry(controls_frame, bg="#333", fg="white", font=("Consolas", 11), width=30)
        self.filename_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(controls_frame, text="File Content / Data:", bg="#1e1e1e", fg="#aaa").pack(anchor="w", padx=10,
                                                                                            pady=(10, 0))
        self.content_entry = tk.Entry(controls_frame, bg="#333", fg="white", font=("Consolas", 11))
        self.content_entry.pack(fill="x", padx=10, pady=5)

        tk.Button(controls_frame, text="ENCRYPT & SIGN (Write)", command=self.run_secure_write, bg="#004400",
                  fg="white", font=("Consolas", 11)).pack(fill="x", padx=10, pady=(20, 5))
        tk.Button(controls_frame, text="VERIFY & DECRYPT (Read)", command=self.run_secure_read, bg="#000044",
                  fg="white", font=("Consolas", 11)).pack(fill="x", padx=10, pady=5)

        tk.Frame(controls_frame, bg="gray", height=1).pack(fill="x", padx=10, pady=15)

        tk.Button(controls_frame, text="SIMULATE TAMPER ATTACK", command=self.run_tamper_attack, bg="#880000",
                  fg="white", font=("Consolas", 11, "bold")).pack(fill="x", padx=10, pady=5)
        tk.Button(controls_frame, text="Clear Logs", command=self.clear_logs, bg="#444", fg="white").pack(side="bottom",
                                                                                                          fill="x",
                                                                                                          padx=10,
                                                                                                          pady=10)

        # --- Right Side Wrapper (Logs + Visualizer) ---
        right_wrapper = tk.Frame(content_frame, bg="#1e1e1e")
        right_wrapper.pack(side="right", fill="both", expand=True)

        # 1. Logs (Top Right)
        logs_frame = tk.LabelFrame(right_wrapper, text=" Live System Audit ", bg="#1e1e1e", fg="white",
                                   font=("Consolas", 12, "bold"))
        logs_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.log_area = scrolledtext.ScrolledText(logs_frame, bg="black", fg="#00ff00", font=("Consolas", 10),
                                                  state='disabled', height=15)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

        # 2. Visualizer (Bottom Right)
        vis_frame = tk.LabelFrame(right_wrapper, text=" Quantum Lattice State (Kyber) ", bg="#1e1e1e", fg="#03fcf0",
                                  font=("Consolas", 12, "bold"))
        vis_frame.pack(side="bottom", fill="both", expand=True)

        self.vis_area = tk.Text(vis_frame, bg="#111", fg="#03fcf0", font=("Consolas", 10), state='disabled', height=12)
        self.vis_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Initial Text for Visualizer
        self.update_visualizer(None, init_msg=True)

        self.log("Session Started.")
        self.log("Quantum Engine (Kyber-1024/Dilithium-87) Active.")
        self.log("AES-GCM Co-Processor Ready.")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f">> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update()

    # --- VISUALIZER FUNCTION ---
    def update_visualizer(self, data_bytes, title="LATTICE KEY STATE", init_msg=False):

        self.vis_area.config(state='normal')
        self.vis_area.delete(1.0, tk.END)

        if init_msg:
            self.vis_area.insert(1.0, "Waiting for Quantum Key Encapsulation...\nSystem Idle.")
            self.vis_area.config(state='disabled')
            return

        rows = 8
        cols = 8

        # Prepare Matrix String
        display_str = f"--- {title} ---\n"
        display_str += "Polynomial Vector Sample (Mod 3329):\n\n"

        # Ensure we have enough bytes
        needed = rows * cols
        if len(data_bytes) < needed:
            data_bytes += b'\x00' * (needed - len(data_bytes))

        indices = list(data_bytes[:needed])

        for r in range(rows):
            display_str += "[ "
            for c in range(cols):
                # Map byte to a coefficient for visuals
                # Kyber coeffs are up to 3329, bytes are 255
                val = (indices[r * cols + c] * 13) % 3329
                display_str += f"{val:04d}  "
            display_str += "]\n"

        display_str += "\n[...vector continues...]"

        self.vis_area.insert(tk.END, display_str)
        self.vis_area.config(state='disabled')
        self.root.update()

    # --- LOGIC FUNCTIONS ---

    def run_secure_write(self):
        filename = self.filename_entry.get()
        content = self.content_entry.get()

        if not filename or not content:
            messagebox.showwarning("Input Error", "Fields cannot be empty.")
            return

        self.log("-" * 40)
        self.log(f"OP: SECURE WRITE -> {filename}")

        # Clear visualizer initially
        self.update_visualizer(None, init_msg=True)

        self.log("1. [Kyber] Encapsulating AES Key...")
        time.sleep(0.5)
        aes_key, encapsulated_key = self.quantum.encapsulate_key()

        # --- TRIGGER VISUALIZER ---
        self.log("   > Visualizing Lattice Vector...")
        self.update_visualizer(encapsulated_key, "GENERATED KYBER LATTICE")
        time.sleep(0.5)  # Pause to let user see it

        self.log("2. [AES-256] Encrypting Payload...")
        time.sleep(0.2)
        nonce, ciphertext = self.aes.encrypt_data(aes_key, content)

        self.log("3. [Dilithium] Signing Data Integrity...")
        time.sleep(0.5)
        combined_data = ciphertext + encapsulated_key
        signature = self.quantum.sign_data(combined_data)

        file_package = {
            "enc_key": base64.b64encode(encapsulated_key).decode('utf-8'),
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "signature": base64.b64encode(signature).decode('utf-8')
        }
        self.storage.save_file(filename, file_package)
        self.log(f"✅ SUCCESS: Encrypted & Signed.")
        messagebox.showinfo("Success", "File Secured Successfully.")

    def run_secure_read(self):
        filename = self.filename_entry.get()
        if not filename.endswith(".secure"): filename += ".secure"

        self.log("-" * 40)
        self.log(f"OP: SECURE READ -> {filename}")

        # Clear visualizer initially
        self.update_visualizer(None, init_msg=True)

        data = self.storage.load_file(filename)
        if not data:
            self.log("❌ ERROR: File not found.")
            messagebox.showerror("Error", "File not found.")
            return

        try:
            enc_key = base64.b64decode(data["enc_key"])
            nonce = base64.b64decode(data["nonce"])
            ciphertext = base64.b64decode(data["ciphertext"])
            signature = base64.b64decode(data["signature"])
        except:
            self.log("❌ ERROR: Invalid File Format.")
            return

        # --- TRIGGER VISUALIZER (SHOW THE KEY WE FOUND) ---
        self.log("   > Reading Lattice Vector from disk...")
        self.update_visualizer(enc_key, "READ KYBER LATTICE")
        time.sleep(0.5)

        self.log("1. [Dilithium] Verifying Signature...")
        time.sleep(0.5)
        combined_data = ciphertext + enc_key
        is_valid = self.quantum.verify_signature(combined_data, signature)

        if not is_valid:
            self.log("❌ CRITICAL ALERT: SIGNATURE INVALID!")
            self.log("⛔ ACCESS DENIED. Tampering Detected.")
            messagebox.showerror("SECURITY ALERT", "Signature Verification Failed!\nFile Integrity Compromised.")
            return

        self.log("   > Signature Valid.")

        self.log("2. [Kyber] Decapsulating AES Key...")
        time.sleep(0.5)
        try:
            aes_key = self.quantum.decapsulate_key(enc_key)
        except:
            self.log("❌ ERROR: Key Decapsulation Failed.")
            return

        self.log("3. [AES-256] Decrypting...")
        try:
            plaintext = self.aes.decrypt_data(aes_key, nonce, ciphertext)
            self.log(f"📄 DATA: {plaintext}")
            messagebox.showinfo("Decrypted Content", f"The secret is:\n\n{plaintext}")
        except Exception as e:
            self.log(f"❌ Decryption Error: {e}")

    def run_tamper_attack(self):
        filename = self.filename_entry.get()
        if not filename.endswith(".secure"): filename += ".secure"

        if not os.path.exists(filename):
            self.log("❌ ERROR: File not found.")
            return

        self.log("-" * 40)
        self.log(f"⚠️ HACKER MODE: Tampering {filename}...")
        time.sleep(0.5)

        import json
        with open(filename, "r") as f:
            data = json.load(f)

        original_ct = data["ciphertext"]
        tampered_ct = "B" + original_ct[1:]
        data["ciphertext"] = tampered_ct

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        self.log("   > Bits corrupted.")
        self.log("⚠️ ATTACK COMPLETE.")
        messagebox.showwarning("Hacker Mode",
                               "File Corrupted.\n\nTry 'Verify & Decrypt' now to see if the Quantum Layer catches it.")

    def clear_logs(self):
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureOSApp(root)
    root.mainloop()
