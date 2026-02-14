# 🚀 Hugging Face Spaces Deployment Guide

## Files Created ✅

The following files have been created for HF Spaces deployment:

1. **app.py** - Entry point for HF Spaces
2. **.streamlit/config.toml** - Streamlit configuration
3. **README.md** - Updated with HF YAML header

## Deployment Steps

### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configure:
   - **Owner**: Your username
   - **Space name**: intelligent-data-viz (or your choice)
   - **License**: MIT
   - **Select the Space SDK**: Streamlit
   - **Visibility**: Public

### Step 2: Upload Files

Upload these files to your Space (via web interface or git):

**Required files:**
- app.py
- requirements.txt
- README.md
- src/ folder (all .py files)
- .streamlit/config.toml
- .gitignore

**Do NOT upload:**
- .env file (secrets go in HF settings)
- venv/ folder
- __pycache__/ folders
- tests/ folder
- examples/ folder

### Step 3: Set API Key Secret

CRITICAL - Without this, the app won't work!

1. Go to your Space → **Settings**
2. Scroll to **Variables and secrets**
3. Click **New secret**
4. Enter:
   - **Name**: GEMINI_API_KEY
   - **Value**: Your actual Gemini API key
5. Click **Save**

Get your API key: https://makersuite.google.com/app/apikey

### Step 4: Deploy via Git (Option A)

```bash
# Add HF remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Add files
git add app.py .streamlit/ README.md requirements.txt src/

# Commit
git commit -m "Deploy to Hugging Face Spaces"

# Push
git push hf main
```

### Step 5: Deploy via Web Interface (Option B)

1. Go to your Space → Files
2. Click **Add file** → **Upload files**
3. Drag & drop all required files
4. Click **Commit changes to main**

## Post-Deployment

### Verify Deployment

1. Wait for build to complete (~2-3 minutes)
2. Check build logs for errors
3. Test app by uploading a dataset

### Common Issues

**"GEMINI_API_KEY not set"**
- Solution: Add the secret in Space settings (Step 3 above)

**"Module not found"**
- Solution: Check requirements.txt is uploaded

**App crashes on startup**
- Solution: Check build logs in your Space

## Your Space URL

After deployment, your app will be available at:
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

## Files Structure for Upload

```
your-space/
├── app.py                    # HF Spaces entry point
├── requirements.txt          # Python dependencies
├── README.md                 # With HF YAML header
├── .streamlit/
│   └── config.toml          # Streamlit config
├── src/
│   ├── __init__.py
│   ├── app.py               # Main Streamlit app
│   ├── llm_handler.py
│   ├── data_processor.py
│   ├── visualization.py
│   └── utils.py
└── .gitignore
```

## Next Steps

1. Create your Space on Hugging Face
2. Upload the files
3. Set the GEMINI_API_KEY secret
4. Wait for deployment
5. Share your Space URL!

---

Need help? Check:
- HF Spaces docs: https://huggingface.co/docs/hub/spaces
- Streamlit on HF: https://huggingface.co/docs/hub/spaces-sdks-streamlit
