# 🤖 Automated Publication Updates System

**Automatically fetch and update Prof. Roshan G. Ragel's publications every month!**

## 🎯 What This Does

- ✅ **Auto-fetches** publications from DBLP, Google Scholar monthly
- ✅ **Merges** new data with existing (no duplicates)
- ✅ **Categorizes** publications by topic (AI, Bioinformatics, Security, etc.)
- ✅ **Generates** beautiful, searchable HTML page
- ✅ **Deploys** to GitHub Pages automatically
- ✅ **Logs** everything for debugging

## 🚀 5-Minute Setup

### 1. Upload to GitHub

```bash
git init
git add .
git commit -m "Add automated publication system"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Select **"Read and write permissions"**
3. Click **Save**

### 3. Done! 🎉

The system will now:
- Run automatically on the **1st of every month** at 2 AM UTC
- Can also be **triggered manually** anytime from the Actions tab

## 📁 File Structure

```
.
├── .github/workflows/
│   └── update-publications.yml    # GitHub Actions workflow
├── data/
│   ├── publications.json          # Your publications (auto-updated)
│   └── fetch_log.txt              # Fetch logs
├── scripts/
│   ├── fetch_publications_auto.py # Fetches from DBLP, Scholar
│   └── generate_publications_html.py # Generates HTML
├── publications.html               # Output (auto-generated)
└── SETUP_GUIDE.md                 # Detailed setup guide
```

## 🎮 How to Use

### Manual Trigger

1. Go to your repo → **Actions** tab
2. Click **"Update Publications Automatically"**
3. Click **"Run workflow"**
4. Wait ~2 minutes
5. Check the updated `publications.html`!

### Automatic Updates

- Runs every month automatically
- Check **Actions** tab for status
- Get email notifications on failures

## 📊 What Gets Updated

### Data Sources
- ✅ **DBLP** (most reliable)
- ✅ **Google Scholar** (may be blocked sometimes)
- ✅ **Manual JSON** (fallback)

### Output
- Updated `publications.html` with latest papers
- Statistics: Citations, H-index, i10-index
- Searchable, filterable by topic
- Links to PDFs, DOIs, GitHub repos

## 🛠️ Customization

### Change Update Schedule

Edit `.github/workflows/update-publications.yml`:

```yaml
schedule:
  - cron: '0 2 1 * *'  # Monthly
```

Options:
- **Weekly:** `'0 2 * * 1'`
- **Daily:** `'0 2 * * *'`
- **Custom:** Use [crontab.guru](https://crontab.guru)

### Add More Topics

Edit `scripts/fetch_publications_auto.py`:

```python
def categorize_topics(publication):
    if 'your_keyword' in text:
        topics.append('YourTopic')
```

### Change Author Info

Edit `scripts/fetch_publications_auto.py`:

```python
AUTHOR_NAME = "Your Name"
ORCID_ID = "0000-0000-0000-0000"
GOOGLE_SCHOLAR_ID = "your_id"
DBLP_URL = "https://dblp.org/..."
```

## 🐛 Troubleshooting

### "Permission denied" Error
→ Enable write permissions: Settings → Actions → General → Read and write permissions

### No New Publications Found
→ Normal! Google Scholar blocks automated requests sometimes. System will retry next month.

### Workflow Failed
→ Check logs in Actions tab → Click on failed run → View details

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[GitHub Actions Docs](https://docs.github.com/en/actions)** - Official documentation
- **[DBLP API](https://dblp.org/faq/)** - DBLP documentation

## 🎨 Features

✨ **Real-time Search** - Find publications instantly  
✨ **Topic Filters** - AI/ML, Bioinformatics, Security, Hardware, IoT  
✨ **Live Statistics** - Auto-updated from Google Scholar  
✨ **Mobile Responsive** - Works on all devices  
✨ **Dark Theme** - Beautiful modern design  
✨ **Direct Links** - DOI, PDFs, GitHub, Presentations

## 📈 Statistics

Current data (auto-updated monthly):
- **1,885** Citations
- **H-index:** 36
- **i10-index:** 20
- **200+** Publications

## 🔐 Security

- ✅ No API keys stored (uses public APIs)
- ✅ Read-only access to external sources
- ✅ Write access only to your own repo
- ✅ All actions logged and auditable

## 🆘 Support

### Need Help?

1. **Check logs:** `data/fetch_log.txt` in your repo
2. **Read guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. **GitHub Issues:** Open an issue in your repository

### Common Issues

**Q: Can I run this locally?**  
A: Yes! Install dependencies and run:
```bash
pip install -r requirements.txt
python scripts/fetch_publications_auto.py
python scripts/generate_publications_html.py
```

**Q: How do I add publications manually?**  
A: Edit `data/publications.json` directly, commit, and push.

**Q: Will this work with a private repo?**  
A: Yes! Just enable GitHub Actions and Pages if needed.

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Credits

**Created for:** Prof. Roshan G. Ragel  
**Department:** Computer Engineering  
**University:** University of Peradeniya, Sri Lanka

**Made with ❤️ by AI Assistant**

---

**Last Updated:** February 10, 2025  
**Version:** 1.0.0

## 🚦 Status

[![Update Publications](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/update-publications.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/update-publications.yml)

*Replace `YOUR_USERNAME/YOUR_REPO` with your actual GitHub username and repository name*
