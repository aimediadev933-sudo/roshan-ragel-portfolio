# 🤖 Automated Publication Updates - Setup Guide

## 📋 Overview
This system automatically updates Prof. Roshan G. Ragel's publication page every month by:
1. Fetching latest publications from DBLP, Google Scholar, and other sources
2. Merging with existing data (no duplicates)
3. Regenerating the HTML page
4. Committing changes to GitHub
5. Auto-deploying to GitHub Pages

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Upload to GitHub Repository

Create a new GitHub repository or use existing one:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Automated publications system"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/roshan-ragel-website.git

# Push
git push -u origin main
```

### Step 2: Required Repository Structure

Ensure your repository has this structure:

```
roshan-ragel-website/
├── .github/
│   └── workflows/
│       └── update-publications.yml    # ← GitHub Actions workflow
├── data/
│   ├── publications.json              # ← Publication data (will be created)
│   ├── publications_backup.json       # ← Automatic backups
│   └── fetch_log.txt                  # ← Fetch logs
├── scripts/
│   ├── fetch_publications_auto.py     # ← Auto-fetcher
│   └── generate_publications_html.py  # ← HTML generator
├── publications.html                   # ← Output HTML
├── styles.css                          # ← Your CSS
├── script.js                           # ← Your JavaScript
└── README.md
```

### Step 3: Create Initial Data File

Create `data/publications.json` with initial data:

```bash
mkdir -p data
```

Copy your existing publications into `data/publications.json` in this format:

```json
[
  {
    "title": "Paper Title Here",
    "authors": [
      {"name": "Author Name", "url": "profile_url"}
    ],
    "venue": "Conference/Journal Name",
    "year": "2025",
    "doi": "10.xxxx/yyyy",
    "topics": ["AI", "Bioinformatics"],
    "links": [
      {"type": "PDF", "url": "https://...", "icon": "fa-file-pdf"}
    ]
  }
]
```

### Step 4: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions":
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
4. Click **Save**

### Step 5: Enable GitHub Pages (Optional)

1. Go to **Settings** → **Pages**
2. Under "Source":
   - Select **"Deploy from a branch"**
   - Branch: **`gh-pages`**
   - Folder: **`/ (root)`**
3. Click **Save**

---

## ⚙️ Configuration

### Update Schedule

Edit `.github/workflows/update-publications.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 1 * *'  # Monthly on the 1st at 2 AM UTC
```

**Change to:**
- Weekly: `'0 2 * * 1'` (Every Monday at 2 AM)
- Daily: `'0 2 * * *'` (Every day at 2 AM)
- Custom: Use [crontab.guru](https://crontab.guru) to generate

### Author Information

Edit `scripts/fetch_publications_auto.py`:

```python
AUTHOR_NAME = "Roshan G. Ragel"
ORCID_ID = "0000-0002-4511-2335"
GOOGLE_SCHOLAR_ID = "UTYj8usAAAAJ"
DBLP_URL = "https://dblp.org/pid/25/6238.html"
```

---

## 🎯 How to Use

### 1. Manual Trigger (Anytime)

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **"Update Publications Automatically"** workflow
4. Click **"Run workflow"** button
5. Select branch (usually `main`)
6. Click **"Run workflow"**

### 2. Automatic Updates

- The workflow runs automatically on the 1st of every month
- No action required!
- Check the **Actions** tab to see status

### 3. Check Results

After workflow runs:
1. Go to **Actions** tab
2. Click on the latest workflow run
3. View the **Summary** to see:
   - How many publications were fetched
   - How many were new
   - Any errors or warnings

---

## 📊 Monitoring

### View Logs

Check `data/fetch_log.txt` in your repository after each run:

```bash
# View logs
cat data/fetch_log.txt

# Or on GitHub: browse to data/fetch_log.txt
```

### Email Notifications

GitHub automatically sends email notifications for:
- ✅ Successful runs (optional, can disable)
- ❌ Failed runs (always enabled)

**To customize:**
1. Go to **Settings** → **Notifications**
2. Under "Actions", choose your preferences

---

## 🛠️ Troubleshooting

### Issue 1: Workflow Permission Denied

**Error:** `permission denied` or `unable to push`

**Fix:**
1. Settings → Actions → General
2. Workflow permissions → "Read and write permissions"
3. Save

### Issue 2: No New Publications Found

**Possible causes:**
- Google Scholar blocked the request (common)
- DBLP hasn't updated yet
- Network issues

**Fix:**
- Check logs in `data/fetch_log.txt`
- System will keep existing data
- Will retry next month automatically

### Issue 3: Python Dependency Errors

**Error:** `ModuleNotFoundError: No module named 'scholarly'`

**Fix:**
The workflow installs dependencies automatically. If it fails:
1. Check `.github/workflows/update-publications.yml`
2. Ensure this line exists:
   ```yaml
   pip install requests beautifulsoup4 scholarly habanero lxml
   ```

### Issue 4: Merge Conflicts

**Error:** Git push fails due to conflicts

**Fix:**
The workflow pulls latest changes before committing. If it still fails:
1. Manually pull latest changes
2. Resolve conflicts
3. Push
4. Re-run workflow

---

## 🎨 Customization

### Add More Data Sources

Edit `scripts/fetch_publications_auto.py` and add functions like:

```python
def fetch_from_custom_source():
    """Fetch from your custom source."""
    # Your code here
    return publications

# Then call in main():
custom_pubs = fetch_from_custom_source()
if custom_pubs:
    all_new_pubs.extend(custom_pubs)
```

### Customize HTML Template

Edit `scripts/generate_publications_html.py` to change:
- Layout
- Styling
- Sections
- Statistics

### Change Topics/Categories

Edit `categorize_topics()` function in `scripts/fetch_publications_auto.py`:

```python
def categorize_topics(publication):
    """Auto-categorize publication topics."""
    text = publication['title'].lower()
    topics = []
    
    if 'your_keyword' in text:
        topics.append('YourTopic')
    
    return topics
```

---

## 📦 Deployment Options

### Option 1: GitHub Pages (Recommended)
✅ Free hosting
✅ Automatic HTTPS
✅ Fast CDN
✅ Easy setup

**URL:** `https://yourusername.github.io/repository-name/`

### Option 2: Custom Domain
1. Buy domain (e.g., roshanragel.com)
2. Add CNAME file:
   ```
   roshanragel.com
   ```
3. Configure DNS:
   - Type: CNAME
   - Name: www
   - Value: yourusername.github.io

### Option 3: Other Hosting
- Netlify
- Vercel
- AWS S3 + CloudFront
- Your own server

Just push the generated `publications.html` to your hosting!

---

## 🔐 Security Best Practices

### 1. Use Repository Secrets
For API keys (if needed):
1. Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add: `API_KEY_NAME` and value
4. Use in workflow: `${{ secrets.API_KEY_NAME }}`

### 2. Limit Workflow Permissions
- Use minimum required permissions
- Don't give write access unless needed

### 3. Review Commits
- Check automated commits before deploying
- Use branch protection rules

---

## 📈 Advanced Features

### Feature 1: Send Notifications

Add to workflow:

```yaml
- name: Send Notification
  if: steps.check_changes.outputs.changes == 'true'
  run: |
    curl -X POST https://your-webhook-url.com \
      -H 'Content-Type: application/json' \
      -d '{"text": "Publications updated!"}'
```

### Feature 2: Generate Analytics

Add script to calculate:
- Citations per year
- Most cited papers
- Collaboration networks
- Topic trends

### Feature 3: Multi-Language Support

Generate publications page in multiple languages:
- English
- Sinhala
- Tamil

---

## 📝 Maintenance

### Monthly Tasks
- ✅ Check workflow status
- ✅ Review new publications
- ✅ Verify data accuracy

### Quarterly Tasks
- ✅ Update statistics (citations, H-index)
- ✅ Review categorization accuracy
- ✅ Update styling/layout if needed

### Yearly Tasks
- ✅ Backup complete data
- ✅ Update author information
- ✅ Review and optimize scripts

---

## 🆘 Support

### Get Help
1. **Check logs:** `data/fetch_log.txt`
2. **GitHub Issues:** Report problems in your repository
3. **Documentation:** Refer to this guide

### Common Questions

**Q: Can I run this locally?**
A: Yes! Just run:
```bash
python scripts/fetch_publications_auto.py
python scripts/generate_publications_html.py
```

**Q: How do I add publications manually?**
A: Edit `data/publications.json` directly, commit, and push.

**Q: Can I disable automatic updates?**
A: Yes, delete `.github/workflows/update-publications.yml` or disable in Actions settings.

**Q: Will this work with a private repository?**
A: Yes! GitHub Actions work with private repos. Just enable GitHub Pages if needed.

---

## ✅ Testing

### Test Locally

```bash
# 1. Install dependencies
pip install requests beautifulsoup4 scholarly habanero lxml

# 2. Run fetcher
python scripts/fetch_publications_auto.py

# 3. Check data
cat data/publications.json

# 4. Generate HTML
python scripts/generate_publications_html.py

# 5. Open in browser
open publications.html
```

### Test on GitHub

1. Create a test branch
2. Push changes
3. Run workflow manually
4. Verify results
5. Merge to main if successful

---

## 🎉 Success Checklist

- [ ] Repository created and pushed to GitHub
- [ ] GitHub Actions workflow file added
- [ ] Initial `data/publications.json` created
- [ ] Workflow permissions configured (read + write)
- [ ] Manual workflow test successful
- [ ] GitHub Pages enabled (optional)
- [ ] Email notifications configured
- [ ] Custom domain configured (optional)
- [ ] First automatic run completed
- [ ] HTML page displays correctly

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Cron Schedule Helper](https://crontab.guru)
- [DBLP API Documentation](https://dblp.org/faq/How+to+use+the+dblp+API.html)
- [Google Scholar API](https://scholarly.readthedocs.io/)

---

## 📧 Contact

For questions or support, contact the Department of Computer Engineering, University of Peradeniya.

**Made with ❤️ by AI Assistant for Prof. Roshan G. Ragel**

---

**Last Updated:** February 10, 2025  
**Version:** 1.0.0
