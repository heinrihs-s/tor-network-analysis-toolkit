#!/usr/bin/env python3
"""
TorNetworkAnalyzer - A tool for network analysis through Tor
"""

import os
import re
import json
import logging
from typing import Dict, List, Optional, Tuple
import requests
import py7zr
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class TorConnectionManager:
    """Manages Tor network connections and requests"""
    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 9050):
        self.proxy_url = f"socks5h://{proxy_host}:{proxy_port}"
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Creates and configures a requests session for Tor"""
        session = requests.Session()
        session.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        return session
    
    def fetch_content(self, url: str) -> Optional[bytes]:
        """Fetches content from a URL through Tor"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logging.error(f"Failed to fetch content from {url}: {str(e)}")
            return None

@dataclass
class FileEntry:
    """Represents a file entry with path and size information"""
    path: str
    size: int
    extension: str = ""

class FileAnalyzer:
    """Analyzes file listings and generates statistics"""
    
    SIZE_MULTIPLIERS = {
        'K': 1024,
        'M': 1024**2,
        'G': 1024**3,
        'T': 1024**4
    }
    
    @staticmethod
    def parse_file_size(size_str: str) -> int:
        """Converts size string (e.g., '4.2M') to bytes"""
        match = re.match(r'^([\d.]+)([KMGT])?B?$', size_str.strip())
        if not match:
            return 0
            
        value, unit = match.groups()
        bytes_value = float(value)
        
        if unit:
            bytes_value *= FileAnalyzer.SIZE_MULTIPLIERS.get(unit, 1)
            
        return int(bytes_value)

    @staticmethod
    def process_file_listing(content: str) -> List[FileEntry]:
        """Processes a file listing and returns structured data"""
        entries = []
        current_path = []
        
        for line in content.splitlines():
            if not line.strip():
                continue
                
            indent_level = (len(line) - len(line.lstrip())) // 2
            while len(current_path) > indent_level:
                current_path.pop()
                
            # Extract file information using regex
            match = re.match(r'.*\[(.+?)\]\s+(.+)$', line.strip())
            if not match:
                continue
                
            size_str, name = match.groups()
            size = FileAnalyzer.parse_file_size(size_str)
            
            current_path = current_path[:indent_level]
            current_path.append(name)
            
            full_path = '/'.join(current_path)
            extension = Path(name).suffix.lower()
            
            entries.append(FileEntry(full_path, size, extension))
            
        return entries

class DataVisualizer:
    """Handles visualization of file analysis results"""
    
    @staticmethod
    def generate_extension_wordcloud(entries: List[FileEntry], output_path: str):
        """Generates a wordcloud visualization of file extensions"""
        extension_counts = {}
        for entry in entries:
            if entry.extension:
                extension_counts[entry.extension] = extension_counts.get(entry.extension, 0) + 1
                
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='black',
            colormap='viridis'
        )
        wordcloud.generate_from_frequencies(extension_counts)
        
        plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
        plt.close()

    @staticmethod
    def analyze_patterns(entries: List[FileEntry]) -> Dict:
        """Analyzes patterns in file listings"""
        analysis = {
            'total_files': len(entries),
            'total_size': sum(entry.size for entry in entries),
            'extension_stats': {},
            'size_distribution': {
                'small': 0,    # < 1MB
                'medium': 0,   # 1MB - 100MB
                'large': 0     # > 100MB
            }
        }
        
        for entry in entries:
            # Extension statistics
            if entry.extension:
                if entry.extension not in analysis['extension_stats']:
                    analysis['extension_stats'][entry.extension] = 0
                analysis['extension_stats'][entry.extension] += 1
            
            # Size distribution
            if entry.size < 1024**2:
                analysis['size_distribution']['small'] += 1
            elif entry.size < 100 * 1024**2:
                analysis['size_distribution']['medium'] += 1
            else:
                analysis['size_distribution']['large'] += 1
                
        return analysis

def main():
    """Main execution function"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Tor connection
    tor_manager = TorConnectionManager()
    
    # Example URL (replace with actual URL)
    target_url = "http://example.onion/files.lst.7z"
    
    # Download and process file
    content = tor_manager.fetch_content(target_url)
    if not content:
        logging.error("Failed to fetch content")
        return
        
    # Save downloaded content
    with open("downloaded.7z", "wb") as f:
        f.write(content)
        
    # Extract archive
    with py7zr.SevenZipFile("downloaded.7z", mode='r') as archive:
        archive.extractall(path="extracted")
        
    # Process first file in extracted directory
    extracted_files = os.listdir("extracted")
    if not extracted_files:
        logging.error("No files extracted")
        return
        
    # Read and analyze file listing
    with open(os.path.join("extracted", extracted_files[0]), 'r') as f:
        file_content = f.read()
        
    analyzer = FileAnalyzer()
    entries = analyzer.process_file_listing(file_content)
    
    # Generate visualizations and analysis
    visualizer = DataVisualizer()
    visualizer.generate_extension_wordcloud(entries, "extension_wordcloud.png")
    
    analysis_results = visualizer.analyze_patterns(entries)
    
    # Save analysis results
    with open("analysis_results.json", 'w') as f:
        json.dump(analysis_results, f, indent=2)
        
    logging.info("Analysis complete. Results saved to analysis_results.json")

if __name__ == "__main__":
    main()
