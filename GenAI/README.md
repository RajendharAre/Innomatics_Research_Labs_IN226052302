# NLP Text Preprocessing Pipeline

This project implements a robust **Natural Language Processing (NLP)** preprocessing pipeline designed to clean and standardize raw text data for machine learning models. It handles common "noise" found in social media and web data, such as URLs, emojis, and repeated characters.

## 🚀 Features
* **Case Normalization:** Converts all text to lowercase.
* **Noise Removal:** Strips out URLs, emails, and special characters.
* **Character Leveling:** Fixes elongated words (e.g., "sooooo" -> "so").
* **Advanced Tokenization:** Filters out short, non-essential tokens while preserving critical sentiment words like "no" and "not."
* **Data Analytics:** Built-in frequency analysis and token statistics.

## 📁 Project Structure
* `preprocessing_script.py`: The core Python logic for text cleaning.
* `README.md`: Project documentation.

## 🛠️ How to Use
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/nlp-logic-building.git
    ```
2.  **Run in Google Colab or Local Python:**
    Copy the code from `preprocessing_script.py` into a cell and run it. The pipeline will process a set of sample "stress-test" sentences and output the cleaned results.

## 📊 Sample Output
| Original Text | Cleaned Text |
| :--- | :--- |
| "Get 100% FREE access now!!!" | "get free access now" |
| "I absolutely looooved this product 😍" | "absolutely loved product" |
| "Visit [https://openai.com](https://openai.com) now!" | "visit now" |

## 🧠 Logic & Insights
This project addresses key NLP challenges discussed in the [Internship Task Document](https://docs.google.com/document/d/1g0zjEwjZDF6-Vog5_QN0rlON-OuCNM382U1rrQ1WP6g/edit?tab=t.0):
* **Stopwords:** Why we keep words like "not" for sentiment accuracy.
* **Lemmatization:** The importance of root-word identification over simple stemming.

---

**Author:** Rajendhar Are
**Task:** Feb Internship Logic Building Task – 1 (Innomatics Research Labs)
