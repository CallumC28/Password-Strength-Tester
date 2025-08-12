# 🔐 Password Strength Checker

A simple GUI tool that analyses password strength and provides real-time feedback. It uses entropy, complexity metrics, and custom rules to evaluate the security of a password.

---

## Features

- ✅ **Strength Score (1–10):** Based on entropy and guessability
- 🧠 **Entropy Bits Calculation:** Reflects how hard a password is to brute-force
- ⚠️ **Live Warnings & Suggestions:** From both `zxcvbn` and custom heuristics
- 🔍 **Tooltips:** Explain entropy and strength scoring clearly
- 🧪 **Extra Checks:** Flags short, repetitive, or overly simple passwords
- 📜 **Scrollable Output Box:** Ensures all feedback is visible
- 🖼️ **Responsive GUI:** Dynamically adjusts to fit content length

---

## Screenshot

> ![App Screenshot](Screenshot(24).png)

---

## Example Output

**For a weak password:**
🧠 Entropy: 24.6 bits
🔒 Strength Score: 3/10 (too weak)
⚠️ Warning: This is a top-10 common password
🔧 Suggestions to improve:
• Use at least 12 characters.
• Mix uppercase and lowercase letters.
• Add some numbers (e.g., 3, 7, 9).
• Include special symbols (!@#$, etc.).

**For a strong password:**
🧠 Entropy: 63.7 bits
🔒 Strength Score: 9/10 ✅
✅ Suggestions you’ve already followed:
• Use a long, uncommon phrase or sentence.

---

## How It Works

The tool uses [Dropbox’s `zxcvbn`](https://github.com/dropbox/zxcvbn) password estimator, combined with custom heuristics for:

- Minimum length enforcement
- Symbol and digit usage
- Repeated character detection
- Avoidance of common passwords

It then calculates entropy and displays feedback in a scrollable output box.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/CallumC28/Password-Strength-Tester.git
```
### 2. Install Dependencies
```bash
pip install zxcvbn
```
tkinter (included in standard Python distribution)

### 3. Run the Application
```bash
python password.py
```
