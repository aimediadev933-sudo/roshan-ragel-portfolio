# 🏗️ System Architecture - Automated Publication Updates

## 📊 Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTOMATED PUBLICATION SYSTEM                 │
│                    Prof. Roshan G. Ragel's Website               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TRIGGER (3 Ways)                                                │
├─────────────────────────────────────────────────────────────────┤
│  1. ⏰ Automatic - Every 1st of month at 2 AM UTC                │
│  2. 👆 Manual - Click "Run workflow" in GitHub Actions          │
│  3. 📝 On Push - When data/publications.json is updated          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS WORKFLOW                                         │
│  (.github/workflows/update-publications.yml)                     │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Checkout repository                                           │
│  ✓ Setup Python 3.11                                             │
│  ✓ Install dependencies                                          │
│  ✓ Run fetch script                                              │
│  ✓ Generate HTML                                                 │
│  ✓ Commit & push changes                                         │
│  ✓ Deploy to GitHub Pages (optional)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  DATA FETCHING                                                   │
│  (scripts/fetch_publications_auto.py)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   DBLP      │  │   Google    │  │   Manual    │             │
│  │   API       │  │   Scholar   │  │   JSON      │             │
│  │  (Primary)  │  │  (Backup)   │  │ (Fallback)  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┴────────────────┘                     │
│                          ↓                                       │
│  ┌──────────────────────────────────────┐                       │
│  │  Merge & Deduplicate                 │                       │
│  │  - Remove duplicates by title        │                       │
│  │  - Merge author information           │                       │
│  │  - Add missing metadata               │                       │
│  └──────────────────────────────────────┘                       │
│                          ↓                                       │
│  ┌──────────────────────────────────────┐                       │
│  │  Auto-Categorize Topics              │                       │
│  │  - AI/ML                              │                       │
│  │  - Bioinformatics                     │                       │
│  │  - Security                           │                       │
│  │  - Hardware                           │                       │
│  │  - IoT/Robotics                       │                       │
│  │  - Agriculture                        │                       │
│  └──────────────────────────────────────┘                       │
│                          ↓                                       │
│  ┌──────────────────────────────────────┐                       │
│  │  Save to JSON                         │                       │
│  │  data/publications.json               │                       │
│  └──────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  HTML GENERATION                                                 │
│  (scripts/generate_publications_html.py)                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Load publications.json                                       │
│  2. Group by year                                                │
│  3. Generate HTML for each publication                           │
│  4. Add search/filter functionality                              │
│  5. Calculate statistics                                         │
│  6. Save to publications.html                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  OUTPUT FILES                                                    │
├─────────────────────────────────────────────────────────────────┤
│  📄 publications.html          - Updated webpage                 │
│  📄 data/publications.json     - Latest data                     │
│  📄 data/publications_backup.json - Backup                       │
│  📄 data/fetch_log.txt         - Logs                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  DEPLOYMENT                                                      │
├─────────────────────────────────────────────────────────────────┤
│  🌐 GitHub Pages                                                 │
│  🌐 Custom Domain (optional)                                     │
│  🌐 Any static hosting                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌──────────────┐
│  Data Sources│
└──────┬───────┘
       │
       ├─► DBLP (https://dblp.org/pid/25/6238.html)
       │   └─► Fetch latest 50 publications
       │       └─► Parse: Title, Authors, Venue, Year, DOI, Links
       │
       ├─► Google Scholar (UTYj8usAAAAJ)
       │   └─► Fetch latest 30 publications
       │       └─► Parse: Title, Authors, Venue, Year
       │
       └─► Manual JSON (data/publications.json)
           └─► User-provided publications
               └─► Complete metadata
       
       ↓
       
┌──────────────────────┐
│  Processing Pipeline  │
└──────┬───────────────┘
       │
       ├─► Step 1: Backup existing data
       │   └─► data/publications_backup.json
       │
       ├─► Step 2: Fetch from all sources
       │   └─► Combine all results
       │
       ├─► Step 3: Merge & Deduplicate
       │   └─► Compare by normalized title
       │       └─► Keep unique publications
       │
       ├─► Step 4: Auto-categorize
       │   └─► Analyze title + venue
       │       └─► Assign topics (AI, Bio, Security, etc.)
       │
       ├─► Step 5: Sort by year
       │   └─► Descending order (2025 → 2006)
       │
       └─► Step 6: Save to JSON
           └─► data/publications.json

       ↓

┌──────────────────────┐
│  HTML Generation      │
└──────┬───────────────┘
       │
       ├─► Load JSON data
       │
       ├─► Group by year
       │   └─► 2025, 2024, 2023, ...
       │
       ├─► Generate HTML
       │   └─► For each publication:
       │       ├─► Title
       │       ├─► Authors (with links)
       │       ├─► Venue
       │       ├─► DOI
       │       └─► Action links (PDF, GitHub, etc.)
       │
       ├─► Add search functionality
       │   └─► Real-time filter by keyword
       │
       ├─► Add topic filters
       │   └─► Filter by: AI, Bio, Security, Hardware, IoT, Agriculture
       │
       ├─► Add statistics
       │   └─► Citations, H-index, i10-index, Total pubs
       │
       └─► Save publications.html

       ↓

┌──────────────────────┐
│  Deployment           │
└──────┬───────────────┘
       │
       ├─► Commit to Git
       │   └─► Auto-commit by GitHub Actions Bot
       │
       ├─► Push to main branch
       │   └─► Trigger GitHub Pages rebuild
       │
       └─► Deploy to web
           └─► https://yourusername.github.io/repo/
```

---

## 📁 File Relationships

```
Repository Root
│
├── .github/
│   └── workflows/
│       └── update-publications.yml ──┐ (Orchestrates everything)
│                                      │
├── scripts/                           │
│   ├── fetch_publications_auto.py ◄──┤ (Called by workflow)
│   │   │                              │
│   │   ├─► Fetches from DBLP          │
│   │   ├─► Fetches from Google Scholar│
│   │   └─► Saves to data/publications.json
│   │                                  │
│   └── generate_publications_html.py ◄┤ (Called by workflow)
│       │                              │
│       ├─► Reads data/publications.json
│       └─► Generates publications.html
│
├── data/
│   ├── publications.json ◄────────────┤ (Main data file)
│   ├── publications_backup.json       │ (Auto-backup)
│   └── fetch_log.txt                  │ (Fetch logs)
│
├── publications.html ◄─────────────────┘ (Output)
│
├── styles.css ─────────────────────────► (Styles for HTML)
├── script.js ──────────────────────────► (Search/filter logic)
│
├── requirements.txt ───────────────────► (Python dependencies)
├── README_AUTOMATION.md ───────────────► (Quick start guide)
└── SETUP_GUIDE.md ─────────────────────► (Detailed setup)
```

---

## 🔁 Execution Timeline

```
Month 1 (Initial Setup)
└─► Day 1: Push to GitHub
    └─► Configure Actions permissions
        └─► Manual test run ✓
            └─► Success! HTML generated

Month 2 (Automatic Update #1)
└─► Day 1, 2 AM UTC: GitHub Actions triggers
    └─► Fetch from DBLP ✓
        └─► Fetch from Scholar (blocked) ✗
            └─► Use existing + DBLP data ✓
                └─► 3 new publications found!
                    └─► HTML regenerated ✓
                        └─► Committed & pushed ✓
                            └─► Deployed to web ✓

Month 3 (Automatic Update #2)
└─► Day 1, 2 AM UTC: GitHub Actions triggers
    └─► Fetch from DBLP ✓
        └─► Fetch from Scholar ✓ (Success!)
            └─► 5 new publications found!
                └─► HTML regenerated ✓
                    └─► Committed & pushed ✓
                        └─► Deployed to web ✓

... and so on, every month automatically! 🚀
```

---

## 🔧 Component Details

### 1. GitHub Actions Workflow

**File:** `.github/workflows/update-publications.yml`

**Purpose:** Orchestrate the entire automation

**Steps:**
1. Checkout repository
2. Setup Python environment
3. Install dependencies
4. Run fetch script
5. Run HTML generator
6. Check for changes
7. Commit & push if changes found
8. Deploy to GitHub Pages

**Runtime:** ~2-3 minutes

---

### 2. Publication Fetcher

**File:** `scripts/fetch_publications_auto.py`

**Purpose:** Fetch publications from multiple sources

**Features:**
- Multi-source fetching (DBLP, Scholar, Manual)
- Intelligent merging (no duplicates)
- Auto-categorization
- Error handling & fallbacks
- Detailed logging

**Output:** `data/publications.json`

---

### 3. HTML Generator

**File:** `scripts/generate_publications_html.py`

**Purpose:** Generate beautiful, searchable HTML

**Features:**
- Year-based grouping
- Search functionality
- Topic filtering
- Statistics display
- Mobile responsive

**Output:** `publications.html`

---

## 📊 Success Metrics

### What Gets Updated Monthly:

✅ **New Publications**
- Added automatically
- Categorized by topic
- Linked to DOI/PDF

✅ **Statistics**
- Citations count
- H-index
- i10-index
- Total publications

✅ **Metadata**
- Author profiles
- Conference/journal info
- Publication links

✅ **Search Index**
- All text searchable
- Filter by topic
- Sort by year

---

## 🛡️ Reliability Features

### Backup System
```
Before fetch:
├─► Backup current data
│   └─► data/publications_backup.json
│
After successful fetch:
├─► Save new data
│   └─► data/publications.json
│
On failure:
└─► Restore from backup
    └─► Keep existing data
```

### Fallback Sources
```
Try Source 1: DBLP
├─► Success? Use data
└─► Failed? Try Source 2

Try Source 2: Google Scholar
├─► Success? Merge with Source 1
└─► Failed? Use Source 1 only

No sources work?
└─► Keep existing data
    └─► Log error
        └─► Retry next month
```

### Error Handling
```
Every operation wrapped in try-catch
├─► Log all errors
├─► Continue on non-critical failures
└─► Exit gracefully on critical failures
```

---

## 🎯 Key Benefits

1. **Zero Maintenance** - Runs automatically every month
2. **Always Up-to-Date** - Latest publications within 24 hours
3. **No API Keys** - Uses public data sources
4. **Version Control** - All changes tracked in Git
5. **Transparent** - Full logs of every operation
6. **Reliable** - Multiple fallback sources
7. **Fast** - Entire update takes ~2 minutes
8. **Free** - 100% free with GitHub Actions & Pages

---

## 📈 Future Enhancements

### Possible Additions:

1. **Email Notifications**
   - Send summary of new publications
   - Alert on fetch failures

2. **Analytics Dashboard**
   - Citation trends over time
   - Collaboration network graph
   - Topic distribution chart

3. **Multi-language Support**
   - Generate pages in Sinhala, Tamil
   - Auto-translate metadata

4. **Export Formats**
   - BibTeX export
   - CSV export
   - PDF report generation

5. **Social Media Integration**
   - Auto-tweet new publications
   - LinkedIn updates

---

**System Status:** ✅ Fully Operational  
**Last Updated:** February 10, 2025  
**Version:** 1.0.0

**Made with ❤️ for Prof. Roshan G. Ragel**
