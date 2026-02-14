# 🚀 Quick Start Guide

Get up and running with the Intelligent Data Visualization App in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd projet_finale_dataviz
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Application

```bash
streamlit run src/app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 Using the App

### Step 1: Upload Data
- Click "Browse files" or drag and drop a CSV file
- The app will display a preview of your data

### Step 2: Ask a Question
Type a business question in the text box, for example:
- "What factors influence housing prices?"
- "Show the distribution of sales by region"
- "How do age and income correlate?"

### Step 3: Generate Visualizations
- Click "🚀 Generate Visualizations"
- Wait for the AI to analyze your data (usually 10-30 seconds)

### Step 4: Review Proposals
- The app will show 3 different visualization options
- Each comes with a justification explaining why it's appropriate
- Click through the tabs to see each visualization

### Step 5: Download
- Select your favorite visualization
- Click "⬇️ Download PNG" to save it

## 📊 Try It with Sample Data

Don't have a dataset? Try these:

1. **Sales Data** (included):
   ```
   examples/sample_datasets/sales_data.csv
   ```
   Try asking: "How do sales vary by region?"

2. **Online Datasets**:
   - [Iris Dataset](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv)
   - [Tips Dataset](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv)

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not set"
- Ensure your `.env` file exists in the project root
- Check that the API key is correct
- Restart the Streamlit app

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Download button not working
```bash
pip install kaleido
```

### Port already in use
```bash
streamlit run src/app.py --server.port 8502
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the code in the `src/` directory

## 💡 Tips for Best Results

1. **Clear Questions**: Ask specific, actionable questions
2. **Clean Data**: Ensure your CSV is well-formatted
3. **Appropriate Size**: Works best with 100-10,000 rows
4. **Column Names**: Use descriptive column names

## 🆘 Getting Help

- Check the [Issues](../../issues) page
- Review the documentation
- Contact the development team

---

Happy visualizing! 🎨📊
