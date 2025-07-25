import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
import math
from zxcvbn import zxcvbn

@dataclass
class Analysis:
    score: int
    entropy: float
    warning: str
    suggestions: list[str]

def analyse_password(pw: str) -> Analysis:
    zx = zxcvbn(pw)
    raw_score = zx['score']
    guesses_log10 = zx['guesses_log10']
    entropy_bits = guesses_log10 * math.log2(10)

    clamped = max(0.0, min(entropy_bits, 80.0))
    score_1_10 = int(clamped / 80 * 9 + 1)

    feedback = zx['feedback']
    warning = feedback.get('warning', "")
    suggestions = feedback.get('suggestions', [])

    return Analysis(
        score=score_1_10,
        entropy=entropy_bits,
        warning=warning,
        suggestions=suggestions
    )

# ─── Tooltip Helper ─────────────────────────────────────────────
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, _event):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Segoe UI", 9), wraplength=300)
        label.pack(ipadx=1)

    def hide(self, _event):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# ─── Suggestions ───────────────────────────────────────────────
def suggest_extra_tips(pw: str) -> list[str]:
    suggestions = []

    if len(pw) < 12:
        suggestions.append("Use at least 12 characters.")
    if pw.lower() == pw or pw.upper() == pw:
        suggestions.append("Mix uppercase and lowercase letters.")
    if not any(c.isdigit() for c in pw):
        suggestions.append("Add some numbers (e.g., 3, 7, 9).")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:',.<>/?`~" for c in pw):
        suggestions.append("Include special symbols (!@#$, etc.).")
    if any(pw.count(c) > len(pw) / 2 for c in set(pw)):
        suggestions.append("Avoid repeating the same character too often.")
    if pw.lower() in ["password", "123456", "qwerty", "admin"]:
        suggestions.append("Avoid common passwords like 'password' or '123456'.")

    return suggestions

# ─── GUI Logic ───────────────────────────────────────────────
def on_check():
    pw = password_entry.get()
    if not pw:
        messagebox.showwarning("Input required", "Please enter a password.")
        return

    result = analyse_password(pw)
    all_suggestions = result.suggestions + suggest_extra_tips(pw)

    # Retry advice if score < 8
    if result.score < 8:
        msg = (
            f"🧠 Entropy: {result.entropy:.1f} bits\n"
            f"🔒 Strength Score: {result.score}/10 (too weak)\n"
        )
        if result.warning:
            msg += f"⚠️ Warning: {result.warning}\n"
        if all_suggestions:
            msg += "🔧 Suggestions to improve:\n" + "\n".join(f" • {s}" for s in all_suggestions)
        msg += "\n\nTry editing your password and check again."
        display_output(msg)
    else:
        msg = (
            f"🧠 Entropy: {result.entropy:.1f} bits\n"
            f"🔒 Strength Score: {result.score}/10 ✅\n"
        )
        if result.warning:
            msg += f"⚠️ Warning: {result.warning}\n"
        if result.suggestions:
            msg += "✅ Suggestions you’ve already followed:\n" + "\n".join(f" • {s}" for s in result.suggestions)
        display_output(msg)

# ─── Tkinter UI Setup ─────────────────────────────────────────
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("450x350")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# Title
ttk.Label(main_frame, text="Enter a Password", font=("Segoe UI", 13, "bold")).pack(pady=(0, 10))

# Password Entry
password_entry = ttk.Entry(main_frame, width=30, font=("Segoe UI", 12))
password_entry.pack()

# Tooltip buttons
info_frame = ttk.Frame(main_frame)
info_frame.pack(pady=5)

entropy_label = ttk.Label(info_frame, text="ℹ️ What is entropy?")
entropy_label.pack(side="left", padx=5)
ToolTip(entropy_label, "Entropy estimates how hard it is for a computer to guess your password. Higher bits = stronger password.")

score_label = ttk.Label(info_frame, text="ℹ️ What is strength?")
score_label.pack(side="left", padx=5)
ToolTip(score_label, "Strength is rated from 1 to 10 based on password complexity and estimated cracking time. (Higher the better)")

# Check Button
ttk.Button(main_frame, text="Check Strength", command=on_check).pack(pady=10)

# Output Area
output_frame = ttk.Frame(main_frame)
output_frame.pack(fill='both', expand=True)

output_box = tk.Text(output_frame, wrap="word", font=("Segoe UI", 10), height=10)
output_box.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=output_box.yview)
scrollbar.pack(side="right", fill="y")

output_box.configure(yscrollcommand=scrollbar.set)

def display_output(msg: str):
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, msg)

root.mainloop()
