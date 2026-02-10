#!/usr/bin/env python3
"""
Automated Publication Fetcher for GitHub Actions
Fetches publications from multiple sources and merges them into a unified JSON file.
Handles API failures gracefully with fallback sources.
"""

import json
import os
import sys
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/fetch_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Configuration
AUTHOR_NAME = "Roshan G. Ragel"
ORCID_ID = "0000-0002-4511-2335"
GOOGLE_SCHOLAR_ID = "UTYj8usAAAAJ"
DBLP_URL = "https://dblp.org/pid/25/6238.html"

# Data directories
DATA_DIR = "data"
OUTPUT_JSON = os.path.join(DATA_DIR, "publications.json")
BACKUP_JSON = os.path.join(DATA_DIR, "publications_backup.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def backup_existing_data():
    """Backup existing publications data before updating."""
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON, 'r') as f:
                data = json.load(f)
            with open(BACKUP_JSON, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Backed up existing data to {BACKUP_JSON}")
        except Exception as e:
            logger.warning(f"⚠️ Could not backup existing data: {e}")


def fetch_from_dblp():
    """Fetch publications from DBLP (most reliable source)."""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        logger.info("🔍 Fetching from DBLP...")
        
        response = requests.get(DBLP_URL, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        publications = []
        
        # Find all publication entries
        entries = soup.find_all('li', class_='entry')
        
        for entry in entries[:50]:  # Get most recent 50
            try:
                # Extract title
                title_tag = entry.find('span', class_='title')
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True).rstrip('.')
                
                # Extract authors
                authors = []
                author_tags = entry.find_all('span', itemprop='author')
                for author_tag in author_tags:
                    author_name = author_tag.get_text(strip=True)
                    author_url = author_tag.find('a')
                    authors.append({
                        'name': author_name,
                        'url': author_url.get('href', '') if author_url else ''
                    })
                
                # Extract venue
                venue_tag = entry.find('span', class_='publ')
                venue = venue_tag.get_text(strip=True) if venue_tag else "Unknown"
                
                # Extract year
                year_tag = entry.find('span', itemprop='datePublished')
                year = year_tag.get_text(strip=True) if year_tag else "Unknown"
                
                # Extract DOI/links
                doi = ""
                links = []
                ee_tags = entry.find_all('a', class_='ee')
                for ee_tag in ee_tags:
                    url = ee_tag.get('href', '')
                    if 'doi.org' in url:
                        doi = url.split('doi.org/')[-1]
                    links.append({
                        'type': 'PDF' if 'pdf' in url.lower() else 'Link',
                        'url': url,
                        'icon': 'fa-file-pdf' if 'pdf' in url.lower() else 'fa-link'
                    })
                
                pub = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'year': year,
                    'doi': doi,
                    'topics': [],  # Will be categorized later
                    'links': links
                }
                
                publications.append(pub)
                
            except Exception as e:
                logger.warning(f"⚠️ Error parsing entry: {e}")
                continue
        
        logger.info(f"✅ Fetched {len(publications)} publications from DBLP")
        return publications
        
    except Exception as e:
        logger.error(f"❌ DBLP fetch failed: {e}")
        return []


def fetch_from_google_scholar():
    """Fetch publications from Google Scholar (may be blocked by anti-bot)."""
    try:
        from scholarly import scholarly
        
        logger.info("🔍 Fetching from Google Scholar...")
        
        # Search for author
        search_query = scholarly.search_author(AUTHOR_NAME)
        author = next(search_query)
        author = scholarly.fill(author, sections=['publications'])
        
        publications = []
        
        for pub in author['publications'][:30]:  # Get most recent 30
            try:
                pub_filled = scholarly.fill(pub)
                
                title = pub_filled['bib'].get('title', '')
                authors_str = pub_filled['bib'].get('author', '')
                venue = pub_filled['bib'].get('venue', '')
                year = pub_filled['bib'].get('pub_year', '')
                
                # Parse authors
                authors = []
                if authors_str:
                    for author_name in authors_str.split(' and '):
                        authors.append({
                            'name': author_name.strip(),
                            'url': ''
                        })
                
                pub_data = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'year': str(year),
                    'doi': '',
                    'topics': [],
                    'links': []
                }
                
                # Add Google Scholar link
                if 'pub_url' in pub_filled:
                    pub_data['links'].append({
                        'type': 'Scholar',
                        'url': pub_filled['pub_url'],
                        'icon': 'fa-graduation-cap'
                    })
                
                publications.append(pub_data)
                
            except Exception as e:
                logger.warning(f"⚠️ Error parsing publication: {e}")
                continue
        
        logger.info(f"✅ Fetched {len(publications)} publications from Google Scholar")
        return publications
        
    except Exception as e:
        logger.error(f"❌ Google Scholar fetch failed (likely blocked): {e}")
        return []


def categorize_topics(publication):
    """Auto-categorize publication topics based on title and venue."""
    title_lower = publication['title'].lower()
    venue_lower = publication['venue'].lower()
    text = title_lower + ' ' + venue_lower
    
    topics = []
    
    # AI/ML keywords
    if any(word in text for word in ['deep learning', 'machine learning', 'neural network', 
                                      'cnn', 'yolo', 'ai', 'classification', 'detection']):
        topics.append('AI')
    
    # Bioinformatics keywords
    if any(word in text for word in ['genomic', 'nanopore', 'sequencing', 'bioinformatics',
                                      'medical', 'cancer', 'health']):
        topics.append('Bioinformatics')
    
    # Security keywords
    if any(word in text for word in ['security', 'encryption', 'attack', 'detection',
                                      'suspicious', 'riot']):
        topics.append('Security')
    
    # Hardware keywords
    if any(word in text for word in ['fpga', 'hardware', 'acceleration', 'embedded',
                                      'hw/sw', 'tcad']):
        topics.append('Hardware')
    
    # IoT/Robotics keywords
    if any(word in text for word in ['iot', 'robot', 'swarm', 'sensor', 'localization',
                                      'slam', 'mixed reality']):
        topics.append('IoT')
    
    # Agriculture keywords
    if any(word in text for word in ['plant', 'leaf', 'disease', 'agriculture', 'crop']):
        topics.append('Agriculture')
    
    publication['topics'] = topics
    return publication


def merge_publications(new_pubs, existing_pubs):
    """Merge new publications with existing ones, removing duplicates."""
    # Create a set of existing titles (normalized)
    existing_titles = {pub['title'].lower().strip() for pub in existing_pubs}
    
    # Add only new publications
    merged = existing_pubs.copy()
    new_count = 0
    
    for pub in new_pubs:
        title_normalized = pub['title'].lower().strip()
        if title_normalized not in existing_titles:
            merged.append(pub)
            existing_titles.add(title_normalized)
            new_count += 1
    
    # Sort by year (descending)
    merged.sort(key=lambda x: x.get('year', '0'), reverse=True)
    
    logger.info(f"📊 Merged: {new_count} new publications added, {len(merged)} total")
    return merged


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("🚀 Starting automated publication fetch")
    logger.info(f"📅 Date: {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    # Backup existing data
    backup_existing_data()
    
    # Load existing publications
    existing_pubs = []
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON, 'r') as f:
                existing_pubs = json.load(f)
            logger.info(f"📂 Loaded {len(existing_pubs)} existing publications")
        except Exception as e:
            logger.error(f"❌ Could not load existing data: {e}")
    
    # Try fetching from multiple sources
    all_new_pubs = []
    
    # Source 1: DBLP (most reliable)
    dblp_pubs = fetch_from_dblp()
    if dblp_pubs:
        all_new_pubs.extend(dblp_pubs)
    
    # Source 2: Google Scholar (may be blocked)
    scholar_pubs = fetch_from_google_scholar()
    if scholar_pubs:
        all_new_pubs.extend(scholar_pubs)
    
    # If no new publications fetched, keep existing data
    if not all_new_pubs:
        logger.warning("⚠️ No new publications fetched from any source")
        logger.info("✅ Keeping existing data unchanged")
        sys.exit(0)  # Exit successfully (no changes)
    
    # Categorize topics
    logger.info("🏷️ Categorizing topics...")
    for pub in all_new_pubs:
        categorize_topics(pub)
    
    # Merge with existing publications
    final_pubs = merge_publications(all_new_pubs, existing_pubs)
    
    # Save updated data
    try:
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(final_pubs, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved {len(final_pubs)} publications to {OUTPUT_JSON}")
    except Exception as e:
        logger.error(f"❌ Could not save data: {e}")
        sys.exit(1)
    
    # Summary
    logger.info("=" * 60)
    logger.info("✅ Publication fetch completed successfully!")
    logger.info(f"📊 Total publications: {len(final_pubs)}")
    logger.info(f"🆕 New publications: {len(final_pubs) - len(existing_pubs)}")
    logger.info("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
