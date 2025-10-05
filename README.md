# Interactive Data Analysis Dashboard

## 💡 What Is This?

Hey there! Got some data you wanna check out *without* writing a ton of code?  
Perfect. This little app is your **data playground** — upload your file, clean it up, make some sick charts, and explore insights fast.

It’s all about getting **quick answers from your data** without firing up a heavy Jupyter notebook.  
Super easy, super fast. Let’s dive in! 🚀

---

## 🧠 What This App Can Do

### 1. 📂 Upload Your Files
- Supports **CSV** and **Excel** files.
- Automatically detects delimiters (commas, semicolons, etc.).
- Choose between multiple Excel sheets if needed.

### 2. 🧹 Clean Up Your Data
- **Nuke Missing Stuff:**  
  Delete rows with missing data or auto-fill them using smart techniques (mean for numbers, most frequent for text).
- **Ditch Useless Columns:**  
  Remove irrelevant columns (like random ID fields) to keep your analysis tidy and focused.

### 3. 📈 Get the Lowdown on Your Data
- **Before & After:** Compare original vs cleaned data side-by-side.  
- **Quick Stats:** Instantly see:
  - Number of rows & columns  
  - Data types (numeric, text, etc.)  
  - Basic stats: mean, max, min, std. deviation, etc.  
- **Spot the Gaps:** Identify columns with missing values and their counts.

### 4. 🎨 Make Awesome Charts!
Bring your data to life with interactive visuals:
- **Histograms:** Understand data distribution.
- **Box Plots:** Spot outliers and ranges.
- **Scatter Plots:** Explore relationships between variables (with optional color-coding!).
- **Bar Charts:** Compare metrics across categories.
- **Heatmaps:** Reveal correlations and relationships at a glance.

### 5. 📝 Grab a Report
Download a `.txt` summary of your cleaned dataset — includes:
- Statistical summaries  
- Data types  
- Missing value counts  
Perfect for note-taking or sharing with your team.

---

## ⚙️ How to Get It Running

### ✅ Requirements
- **Python 3.8+** installed on your system.
- (Optional but recommended) Use a **virtual environment** to keep dependencies isolated.

### 🪄 Installation & Startup

1. **Get the Code**  
   Download or clone this repository and locate the `app.py` file.

2. **Install Dependencies**
   
   Open your terminal or command prompt and run:
   ```bash
   pip install streamlit pandas matplotlib seaborn openpyxl

3. **Run the App**
   
   Navigate to the project folder and execute:
   ```
   streamlit run app.py
