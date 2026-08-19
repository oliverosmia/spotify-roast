# 🎵 Spotify Roast - Streamlit App Setup Guide

## Quick Start (Wed Night → Thu Demo)

### Prerequisites
✅ LMStudio running on Windows with **Local Network enabled**  
✅ WSL with Python 3.8+  
✅ NLP environment (or create one)  

---

## Step 1: Setup Environment in WSL

```bash
# Navigate to your project folder
cd ~/spotify_roast

# Create/activate your NLP environment
conda activate nlp_env  # or python -m venv venv && source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download spaCy model (needed for NER)
python -m spacy download en_core_web_sm
```

---

## Step 2: Verify LMStudio Connection

**On Windows LMStudio:**
1. Click **"Local Server"** tab
2. Make sure **"Serve on local network"** is ENABLED ✅
3. Note your IP address (e.g., `192.168.86.3:1234`)
4. Click **"Start Server"**

**Test from WSL:**
```bash
# Replace with YOUR IP
curl http://192.168.86.3:1234/v1/models
```

Should return JSON response. ✅

---

## Step 3: Run the Streamlit App

**In WSL terminal:**
```bash
streamlit run streamlit_app.py
```

The app will open in your browser (usually `http://localhost:8501`).

---

## Step 4: Using the App

### Sidebar Controls:
1. **Data Source** → Select "Sample Data" or "Upload JSON"
2. **Sample Profile** → Choose from 5 profiles:
   - `music_lover_2024` (Balanced taste)
   - `pop_addict` (Pop heavy - 95% pop!)
   - `indie_hipster` (Indie & alternative)
   - `metal_head` (Rock & metal)
   - `kpop_stan` (K-pop focused)
3. **LMStudio Settings** → Enter your IP:port
4. **Test Connection** → Verify it works

### Main App Workflow:
1. Select a sample profile
2. See NER analysis (artists & genres)
3. View TF-IDF analysis (guilty pleasures)
4. Click **"🚀 Generate Roast!"**
5. Watch LMStudio generate your snarky roast 🎤
6. View beautiful dashboard
7. Download dashboard as PNG

---

## Sample Profiles Included

### 1. **music_lover_2024** (Balanced)
- Mix of pop, indie, hip hop, rock
- Mainstream: 62.5%
- **Roast Theme:** "You're trying to seem cool with indie, but you're basically a pop listener"

### 2. **pop_addict** (Pop Heavy)
- 95% pop + synth-pop
- Mostly Taylor Swift, Ariana Grande, Dua Lipa
- **Roast Theme:** "Your entire personality is influenced by pop radio"

### 3. **indie_hipster** (Indie Obsessed)
- Arctic Monkeys, Tame Impala, Phoebe Bridgers
- Lo-fi, bedroom pop, indie rock
- **Roast Theme:** "You listen exclusively to artists who use Bandcamp"

### 4. **metal_head** (Rock/Metal)
- Led Zeppelin, Black Sabbath, Metallica
- Heavy metal + progressive rock
- **Roast Theme:** "Your music has more guitar solos than lyrics"

### 5. **kpop_stan** (K-Pop Fan)
- BTS, BLACKPINK, TWICE, NewJeans
- Exclusively K-pop artists
- **Roast Theme:** "Your bias group is your entire personality"

---

## File Structure

```
spotify_roast/
├── streamlit_app.py                 # Main Streamlit app
├── spotify_roast_pipeline.py        # Original pipeline (backup)
├── requirements.txt                 # Python dependencies
├── sample_spotify_data.json          # Balanced profile
├── sample_pop_addict.json            # Pop heavy profile
├── sample_indie_hipster.json         # Indie focused profile
├── sample_metal_head.json            # Metal/rock profile
├── sample_kpop_stan.json             # K-pop profile
└── SETUP_GUIDE.md                    # This file
```

---

## Troubleshooting

### Streamlit won't start
```bash
# Install/upgrade Streamlit
pip install --upgrade streamlit
```

### "Cannot connect to LMStudio"
- Make sure LMStudio **Local Server is running** on Windows
- Make sure **"Serve on local network"** is enabled
- Check your IP address in LMStudio matches what you entered
- Test: `curl http://YOUR_IP:1234/v1/models`

### "Module not found: streamlit / spacy"
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### "No such file: sample_pop_addict.json"
- Make sure ALL 5 sample JSON files are in the same directory as `streamlit_app.py`
- Check filenames match exactly (case-sensitive)

### App runs but roast says "LMStudio offline"
- Verify Local Server is actually **running** (not just loaded)
- Check "Serve on local network" is enabled
- Look for error message in console

---

## For Your Thursday Demo

**What to Show:**
1. Open the Streamlit app
2. Select different sample profiles from dropdown
3. Show how roast changes based on taste profile
4. Click **"🚀 Generate Roast!"** and watch it generate
5. Display the dashboard visualization
6. Optionally download PNG

**Talking Points:**
- **NER:** "We extract artist names and genres automatically"
- **TF-IDF:** "We find what's unusual about your taste by comparing to mainstream"
- **LMStudio:** "We send this analysis to a local LLM to generate witty roasts"
- **Visualization:** "Beautiful dashboard showing your taste profile"

**Demo Time:** ~3-5 minutes per profile
**Profiles to Demo:** At least 2-3 different ones (e.g., pop_addict + indie_hipster for contrast)

---

## Tips for a Great Demo

1. **Test beforehand** — Run through entire flow once before presenting
2. **Have backup** — If LMStudio crashes, have a screenshot of output ready
3. **Practice roasts** — Different profiles generate different roasts, so play with a few
4. **Show contrast** — Demo pop_addict vs indie_hipster to show how different roasts are
5. **Explain the pipeline** — Mention NER → TF-IDF → LMStudio → visualization

---

## Advanced: Using Real Spotify Data

Once you download your Spotify JSON:

1. In app sidebar → **"Upload JSON"**
2. Select your JSON file
3. App processes it automatically
4. See YOUR roast! 🎤

---

## Timeline

**Tonight (Wed):**
- [ ] Install requirements
- [ ] Test LMStudio connection
- [ ] Run Streamlit app with sample data
- [ ] Test all 5 profiles
- [ ] Generate roasts from 2-3 profiles
- [ ] Download dashboards

**Tomorrow (Thu):**
- [ ] Do final test run
- [ ] Practice demo (~5 mins)
- [ ] Presentation time! 🎉

---

Good luck! You've got this! 🚀

Questions? Let me know!
