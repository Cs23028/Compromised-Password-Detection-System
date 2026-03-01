import hashlib
import re
import tkinter as tk
from tkinter import messagebox

def load_compromised_hashes(file_path):
    hashes = set()
    try:
        with open(file_path, "r", encoding="latin-1") as f:
            for line in f:
                pwd = line.strip()
                if pwd:
                    h = hashlib.sha1(pwd.encode()).hexdigest()
                    hashes.add(h)
    except FileNotFoundError:
        messagebox.showerror("Error", "compromised_passwords.txt not found")
    return hashes


def check_strength(password):
    score = 0
    issues = []

    if len(password) >= 8:
        score += 1
    else:
        issues.append("Too short")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        issues.append("No uppercase")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        issues.append("No lowercase")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        issues.append("No number")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        issues.append("No special char")

    return score, issues


def weak_pattern(password):
    common = ["123", "abc", "password", "admin"]
    return any(p in password.lower() for p in common)


def analyze():
    pwd = entry.get()

    if not pwd:
        messagebox.showwarning("Input Error", "Enter a password")
        return

    sha1 = hashlib.sha1(pwd.encode()).hexdigest()
    compromised = sha1 in compromised_hashes

    score, issues = check_strength(pwd)
    pattern_flag = weak_pattern(pwd)

    result = ""

    result += "Compromised: YES\n" if compromised else "Compromised: NO\n"
    result += f"Strength Score: {score}/5\n"

    if pattern_flag:
        result += "Weak pattern detected\n"

    if issues:
        result += "Issues:\n"
        for i in issues:
            result += f"- {i}\n"

    output_label.config(text=result)


compromised_hashes = load_compromised_hashes("compromised_passwords.txt")

root = tk.Tk()
root.title("Password Checker GUI")
root.geometry("400x300")

tk.Label(root, text="Enter Password").pack(pady=10)

entry = tk.Entry(root, show="*", width=30)
entry.pack()

tk.Button(root, text="Check", command=analyze).pack(pady=10)

output_label = tk.Label(root, text="", justify="left")
output_label.pack(pady=10)

root.mainloop()
