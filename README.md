# 🎨 Intelligent Data Visualization App

An intelligent web application that uses Large Language Models (LLMs) to automatically recommend and generate data visualizations from user-provided datasets and business questions.

## 📋 Overview

This project leverages Google's Gemini API with a **multi-step scaffolding approach** to intelligently analyze datasets and generate appropriate visualizations that follow best practices in data visualization (Tufte, Cleveland, Few).

### Key Features

- **AI-Powered Analysis**: Automatically identifies relevant columns and relationships in your data
- **Smart Recommendations**: Proposes 3 different visualization types with detailed justifications
- **Best Practices**: Follows visualization principles:
  - Right chart type for the data
  - Maximum data-ink ratio
  - No chartjunk (unnecessary decorations)
  - Perceptual effectiveness
- **Interactive Interface**: User-friendly Streamlit interface
- **Export Capability**: Download visualizations as PNG images

## 🔄 User Flow

1. **Upload** a CSV dataset
2. **Ask** a business question (e.g., "What factors influence housing prices?")
3. **Review** 3 AI-generated visualization proposals with justifications
4. **Select** your preferred visualization
5. **Download** the chart as a PNG file

## 🏗️ Architecture

### Multi-Step LLM Scaffolding (Chain-of-Thought Approach)

The application uses a sophisticated 3-step pipeline instead of a single monolithic prompt:

#### Step 1: Column Analysis
- Analyzes CSV schema and user question
- Identifies relevant columns for visualization
- Provides reasoning for column selection

#### Step 2: Chart Type Selection
- Selects 3 appropriate chart types
- Provides justifications based on visualization best practices
- Considers data types, relationships, and perceptual effectiveness

#### Step 3: Code Generation
- Generates executable Python/Plotly code
- Creates production-ready visualizations
- Handles edge cases and errors gracefully

This chain-of-thought approach ensures more accurate and contextually appropriate visualizations compared to single-step LLM queries.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd projet_finale_dataviz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
projet_finale_dataviz/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── llm_handler.py         # Multi-step LLM scaffolding logic
│   ├── data_processor.py      # Data loading and analysis
│   ├── visualization.py       # Chart generation functions
│   └── utils.py               # Utility functions
├── tests/
│   ├── test_data_processor.py
│   └── test_llm_handler.py
├── examples/
│   └── sample_datasets/
│       └── placeholder.csv
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project metadata
├── LICENSE
└── README.md
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📊 Example Questions

Try these sample questions with your datasets:

- "What factors influence housing prices?"
- "Show the distribution of sales by region"
- "How do age and income correlate?"
- "What are the trends over time?"
- "Compare performance across categories"

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly Express
- **LLM**: Google Gemini API
- **Data Processing**: Pandas
- **Testing**: Pytest

## 📚 Visualization Best Practices

This application follows principles from leading visualization experts:

- **Edward Tufte**: Maximizing data-ink ratio, eliminating chartjunk
- **William Cleveland**: Perceptual effectiveness and accurate representation
- **Stephen Few**: Dashboard design and information display

## 🤝 Contributing

This project is developed collaboratively using:

- Feature branches for development
- Pull requests for code review
- Clear commit messages
- Comprehensive testing

### Development Workflow

1. Create a feature branch
2. Implement changes
3. Write/update tests
4. Submit pull request
5. Code review and merge

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- Streamlit for the web framework
- The data visualization community for best practices

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using multi-step LLM scaffolding and visualization best practices**
