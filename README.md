# 🎬 Subtitle Translator (English → Dutch)

This is a simple Python script designed to translate `.srt` subtitle files from **English to Dutch** using an offline machine translation model (MarianMT via Hugging Face).

If you'd like to translate between different languages, simply update the `MODEL_NAME` variable within the script with a compatible MarianMT model (e.g., `Helsinki-NLP/opus-mt-nl-en` for Dutch → English).

---

### 📂 Project Setup

Before you begin, please ensure you have the following folder structure set up in the root directory of your project:

* `srt_en/`: Place your original English `.srt` files in this directory.
* `srt_nl/`: The translated Dutch `.srt` files will be automatically saved here.

---

### ▶️ Getting Started

Here's how to use the script:

1.  **Install Dependencies:** Open your terminal or command prompt and run the following commands to create a virtual environment and install the necessary packages:

```bash
python -m venv venv
```

**Activate the virtual environment:**

* **macOS/Linux:**
```bash
source venv/bin/activate
```
* **Windows:**
```bash
.\venv\Scripts\activate
```

After activating the virtual environment, install the required libraries:

```bash
pip install -r requirements.txt
```

2.  **Run the Script:** Once the dependencies are installed, execute the translation script:

```python
python srt_translator.py
```

---

### 💡 Important Notes

1.  **Offline Operation:** This script performs the translation entirely offline, meaning you don't need an internet connection after installing the necessary libraries.

2.  **Subtitle-Optimized Translation:** The MarianMT model is pretrained on subtitle data (OpenSubtitles), making it highly effective at translating conversational text commonly found in subtitles.

3.  **Customization:** If you wish to modify the translation's tone, language style, or implement features like profanity filtering, you can directly edit the script.

---

Enjoy your translated subtitles! 🎉