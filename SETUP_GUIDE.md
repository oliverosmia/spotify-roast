# 🎵 Spotify Roast - NLP Pipeline Setup Guide

## Quick Start (Wed Night → Thu Demo)

### Prerequisites
✅ LMStudio running on Windows (http://127.0.0.1:1234)
✅ WSL with Python 3.8+
✅ NLP environment (or create one)

---

## Step 1: Setup Environment in WSL

```bash
# Navigate to your project folder
cd ~/spotify_roast  # (or wherever you want it)

# Create/activate your NLP environment
conda activate nlp_env  # or python -m venv venv && source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download spaCy model (needed for NER)
python -m spacy download en_core_web_sm
```

---

## Step 2: Verify LMStudio Connection

Open WSL terminal and test:

```bash
curl http://127.0.0.1:1234/v1/models
```

**You should see JSON response with your model info.**

If this works → LMStudio is reachable from WSL ✅

If it fails → Make sure LMStudio Local Server is running on Windows

---

## Step 3: Run the Pipeline

**Option A: In Jupyter Lab (Recommended)**
```bash
# Start Jupyter Lab in WSL
jupyter lab

# In the browser:
# 1. Create new notebook
# 2. Copy-paste the code from spotify_roast_pipeline.py into cells
# 3. Run cell by cell to see outputs

# OR load the script directly:
# new terminal → python spotify_roast_pipeline.py
```

**Option B: Direct Python Script**
```bash
python spotify_roast_pipeline.py
```

---

## Step 4: What the Pipeline Does

### Part 1: NER (Named Entity Recognition)
- Extracts artist names from your data
- Identifies genres and their frequencies
- Shows "top 15 artists" extracted

### Part 2: TF-IDF Analysis
- Compares your taste against "mainstream baseline"
- Finds your guilty pleasures (high TF-IDF = unusual taste)
- Calculates "mainstream dependency %" 

### Part 3: LMStudio Roasting
- Sends your taste profile to LMStudio
- Model generates snarky, witty roast
- **This is the fun part!** 🎤

### Part 4: Visualization
- Generates beautiful dashboard (PNG image)
- Shows genre breakdown, artist popularity
- Scorecard with metrics

---

## Step 5: Expected Output

When you run the script, you'll see:

```
================================================================================
SPOTIFY ROAST NLP PIPELINE
================================================================================

👤 User: music_lover_2024
📊 Top Artists: 20
🎵 Top Tracks: 30
🎸 Genres: 20

================================================================================
PART 1: NAMED ENTITY RECOGNITION (NER)
================================================================================

✨ Top 15 Artists:
  1. Taylor Swift (popularity: 95)
  2. The Weeknd (popularity: 94)
  ...

🎭 Top Genres Extracted:
  • pop: 85 occurrences
  • indie rock: 45 occurrences
  ...

================================================================================
PART 2: TF-IDF ANALYSIS (Guilty Pleasures Detection)
================================================================================

🚨 Guilty Pleasures (High TF-IDF = Unusual taste):
  • psychedelic rock: 0.782 (niche factor)
  • indie pop: 0.654 (niche factor)
  ...

📊 Taste Profile:
  Mainstream genres: 12
  Niche/Alternative: 8
  Mainstream dependency: 62.5%

================================================================================
PART 3: GENERATING SNARKY ROAST via LMStudio
================================================================================

🎤 Sending roast prompt to LMStudio...
   Target: http://127.0.0.1:1234/v1/chat/completions

✅ ROAST GENERATED!

================================================================================
🎵 YOUR SPOTIFY ROAST 🎵
================================================================================

"So you've got Taylor Swift on repeat AND Radiohead? That's giving 
'I want to be relatable but also profound.' Your 62% mainstream dependency 
suggests you're basically the musical version of a Pumpkin Spice Latte — 
everyone gets it, but you're desperately throwing some indie folk in there 
to prove you have taste. Kudos on the psychedelic rock phase though, that's 
definitely your personality showing up!" 🎸

================================================================================
PART 4: VISUALIZATION & SCORECARD
================================================================================

📊 SPOTIFY ROAST SCORECARD:

Metric                      Score         Status
--------------------------------------------------
Pop Dependency              62.5%    🟡 Medium
Alternative Niche           37.5%    🟢 Low
Genre Diversity            100.0%    🟢 Low
Indie/Alt Taste             32.1%    🟢 Low
Hip Hop Affinity            18.5%    🔴 High

✅ Dashboard saved as 'spotify_roast_dashboard.png'

================================================================================
✨ PIPELINE COMPLETE ✨
================================================================================

✅ Files generated:
   • spotify_roast_dashboard.png (visualization)

🎤 Ready to demo on Thursday!
```

---

## Step 6: For Your Thursday Demo

**Files you'll have:**
1. ✅ Console output (show the terminal)
2. ✅ `spotify_roast_dashboard.png` (beautiful visualization)
3. ✅ The generated roast text (screenshot or print)

**What to show in demo:**
1. Run the script (show it processing)
2. Show the console output (artist extraction, TF-IDF analysis)
3. Display the dashboard image
4. Read the roast aloud (it's funny!)
5. Explain each NLP component:
   - NER: Artist/genre extraction
   - TF-IDF: Finding guilty pleasures
   - LMStudio: Snarky roast generation
   - Visualization: Dashboard breakdown

---

## Troubleshooting

### "Cannot connect to LMStudio"
- **Fix:** Make sure LMStudio Local Server is running on Windows
- Check: Open http://127.0.0.1:1234 in browser (should show LMStudio page)

### "Module not found: spacy / pandas / etc"
- **Fix:** `pip install -r requirements.txt` in your activated environment
- Check you're in the right environment: `conda activate nlp_env`

### "File not found: sample_spotify_data.json"
- **Fix:** Make sure the JSON file is in the same directory as the script
- Or update the file path in the script

### Script runs but roast says "LMStudio offline"
- **Fix:** LMStudio server probably isn't started
- In LMStudio → click "Local Server" tab → click "Start Server" button

### Spacy model error
- **Fix:** Download it: `python -m spacy download en_core_web_sm`

---

## Using Your Real Spotify Data

Once you download your Spotify JSON from the Streamlit app:

1. Save it: `my_spotify_data.json`
2. Update line in script:
   ```python
   with open('my_spotify_data.json', 'r') as f:  # Change filename here
   ```
3. Run again with your real data!

---

## Timeline

**Tonight (Wed):**
- [ ] Install requirements
- [ ] Test LMStudio connection
- [ ] Run pipeline with sample data
- [ ] Generate dashboard
- [ ] Practice demo

**Tomorrow (Thu):**
- [ ] Final polish
- [ ] Demo time! 🎉

---

Good luck! 🚀 Let me know if anything breaks!
