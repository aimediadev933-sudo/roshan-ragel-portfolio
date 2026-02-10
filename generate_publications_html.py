#!/usr/bin/env python3
"""
Publication HTML Generator
Reads publications from JSON and generates a beautiful, searchable HTML page.
"""

import json
import os
from datetime import datetime
from collections import defaultdict

# Configuration
DATA_DIR = "data"
INPUT_JSON = os.path.join(DATA_DIR, "publications.json")
OUTPUT_HTML = "publications.html"
TEMPLATE_HTML = "templates/publications_template.html"

# Statistics (will be calculated from data)
stats = {
    'total_citations': 1885,
    'h_index': 36,
    'i10_index': 20,
    'total_publications': 0
}


def load_publications():
    """Load publications from JSON file."""
    try:
        with open(INPUT_JSON, 'r') as f:
            pubs = json.load(f)
        print(f"✅ Loaded {len(pubs)} publications from {INPUT_JSON}")
        stats['total_publications'] = len(pubs)
        return pubs
    except Exception as e:
        print(f"❌ Error loading publications: {e}")
        return []


def group_by_year(publications):
    """Group publications by year."""
    by_year = defaultdict(list)
    for pub in publications:
        year = pub.get('year', 'Unknown')
        by_year[year].append(pub)
    
    # Sort years in descending order
    sorted_years = sorted(by_year.keys(), reverse=True, key=lambda x: int(x) if x.isdigit() else 0)
    return {year: by_year[year] for year in sorted_years}


def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def generate_publication_html(pub):
    """Generate HTML for a single publication."""
    topics_attr = ','.join(pub.get('topics', []))
    
    html = f'<div class="publication-item" data-topics="{topics_attr}">\n'
    html += f'    <p class="pub-title">{escape_html(pub["title"])}</p>\n'
    
    # Authors
    authors_html = []
    for author in pub.get('authors', []):
        name = escape_html(author['name'])
        url = author.get('url', '')
        if url:
            authors_html.append(f'<a href="{url}" target="_blank">{name}</a>')
        else:
            authors_html.append(name)
    
    html += f'    <p class="pub-authors">{", ".join(authors_html)}</p>\n'
    
    # Venue
    if pub.get('venue'):
        html += f'    <p class="pub-venue">{escape_html(pub["venue"])}</p>\n'
    
    # DOI
    if pub.get('doi'):
        doi_url = f"https://doi.org/{pub['doi']}" if not pub['doi'].startswith('http') else pub['doi']
        html += f'    <p class="pub-doi">DOI: <a href="{doi_url}" target="_blank">{escape_html(pub["doi"])}</a></p>\n'
    
    # Links
    if pub.get('links'):
        html += '    <div class="pub-links">\n'
        for link in pub['links']:
            icon = link.get('icon', 'fa-link')
            html += f'        <a href="{link["url"]}" target="_blank" class="pub-link">\n'
            html += f'            <i class="fas {icon}"></i> {link["type"]}\n'
            html += '        </a>\n'
        html += '    </div>\n'
    
    html += '</div>\n'
    return html


def generate_year_section(year, publications):
    """Generate HTML for a year section."""
    is_open = 'open' if year == '2025' else ''
    
    html = f'<details class="year-section" {is_open}>\n'
    html += f'    <summary class="year-header">{year}</summary>\n'
    html += '    <div class="year-content">\n'
    
    for pub in publications:
        html += generate_publication_html(pub)
    
    html += '    </div>\n'
    html += '</details>\n\n'
    return html


def generate_complete_html(publications_by_year):
    """Generate the complete HTML page."""
    
    # Read template or create default
    try:
        with open(TEMPLATE_HTML, 'r') as f:
            template = f.read()
        print(f"✅ Using template from {TEMPLATE_HTML}")
    except:
        print("ℹ️ No template found, using embedded template")
        template = None
    
    # Generate publications HTML
    publications_html = ""
    for year, pubs in publications_by_year.items():
        publications_html += generate_year_section(year, pubs)
    
    # If template exists, inject the publications
    if template:
        # Replace placeholder in template
        html = template.replace('{{PUBLICATIONS_CONTENT}}', publications_html)
        html = html.replace('{{TOTAL_PUBLICATIONS}}', str(stats['total_publications']))
        html = html.replace('{{UPDATE_DATE}}', datetime.now().strftime('%B %d, %Y'))
    else:
        # Generate complete HTML from scratch
        html = generate_standalone_html(publications_html)
    
    return html


def generate_standalone_html(publications_html):
    """Generate complete standalone HTML (if no template)."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications | Roshan G. Ragel</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <nav>
        <div class="nav-content">
            <a href="index.html" class="logo">Roshan G. Ragel</a>
            <ul class="nav-links">
                <li><a href="about.html">ABOUT</a></li>
                <li><a href="publications.html" class="active">PUBLICATIONS</a></li>
                <li><a href="projects.html">Projects</a></li>
                <li><a href="students.html">Students</a></li>
            </ul>
        </div>
    </nav>

    <header class="page-header">
        <h1>Publications</h1>
        <p>Research Output and Scholarly Contributions</p>
    </header>

    <main>
        <div class="content-section">
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-number">{stats['total_citations']}</div>
                    <div class="stat-label">Total Citations</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats['h_index']}</div>
                    <div class="stat-label">H-Index</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats['i10_index']}</div>
                    <div class="stat-label">i10-Index</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats['total_publications']}+</div>
                    <div class="stat-label">Total Publications</div>
                </div>
            </div>

            <h2>Publications by Year</h2>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Last updated: {datetime.now().strftime('%B %d, %Y')}
            </p>

            <div class="publications-years">
                {publications_html}
            </div>
        </div>
    </main>

    <footer>
        <p>&copy; 2025 Roshan G. Ragel. All rights reserved.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
'''


def main():
    """Main execution function."""
    print("=" * 60)
    print("🚀 Generating Publications HTML")
    print(f"📅 Date: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Load publications
    publications = load_publications()
    if not publications:
        print("❌ No publications to process!")
        return
    
    # Group by year
    publications_by_year = group_by_year(publications)
    print(f"📊 Grouped into {len(publications_by_year)} years")
    
    # Generate HTML
    html = generate_complete_html(publications_by_year)
    
    # Save to file
    try:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Generated {OUTPUT_HTML} successfully!")
        print(f"📄 File size: {len(html)} bytes")
    except Exception as e:
        print(f"❌ Error saving HTML: {e}")
        return
    
    print("=" * 60)
    print("✅ HTML generation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
