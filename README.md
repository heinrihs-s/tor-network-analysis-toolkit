# Tor Network Analysis Toolkit

An educational Python toolkit demonstrating programmatic interaction with the Tor network for cybersecurity research and network analysis purposes.

## Overview

This project provides a series of Python scripts and exercises designed to teach network analysis and data processing techniques using the Tor network. The toolkit demonstrates various aspects of network interaction, data normalization, and analysis techniques commonly used in cybersecurity research.

## Educational Objectives

- Learn programmatic interaction with the Tor network using Python
- Understand SOCKS5 proxy configuration and usage
- Practice data processing and normalization techniques
- Develop skills in file system analysis and pattern recognition
- Gain experience with data visualization and statistical analysis

## Features

- Tor network connectivity via SOCKS5 proxy
- File listing analysis and normalization
- Data extraction and processing utilities
- Pattern recognition for file system analysis
- Data visualization capabilities including word clouds
- Size analysis and statistical reporting

## Prerequisites

- Python 3.x
- Tor service with SOCKS5 proxy configured
- Required Python packages:
  - requests
  - py7zr
  - pandas
  - pathlib
  - wordcloud
  - matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tor-network-analysis-toolkit.git
cd tor-network-analysis-toolkit
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Ensure Tor service is running with SOCKS5 proxy configured (default port 9050)

## Usage

The toolkit is organized into several educational modules:

1. **Basic Tor Network Connection**
   - Demonstrates connection to Tor network via SOCKS5 proxy
   - Shows basic HTTP requests through Tor

2. **File System Analysis**
   - Processes and normalizes file listings
   - Extracts metadata and statistics

3. **Data Visualization**
   - Generates word clouds of file extensions
   - Creates statistical visualizations of file patterns

4. **Pattern Recognition**
   - Identifies common file patterns
   - Analyzes file size distributions

## Example Usage

```python
# Setup Tor proxy connection
proxy = 'socks5h://127.0.0.1:9050'
proxies = {
    'http': proxy,
    'https': proxy,
}

# Make request through Tor
response = requests.get(URL, proxies=proxies)
```

## Responsible Usage Notice

This toolkit is designed for educational purposes in cybersecurity research and network analysis. Users should:

- Comply with all applicable laws and regulations
- Respect network usage policies and guidelines
- Use the tools responsibly and ethically
- Obtain necessary permissions before analyzing any network or system

## Contributing

Contributions to improve the educational value of this toolkit are welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description of changes

## License

[MIT License](LICENSE)

## Acknowledgments

This project is designed for educational purposes to demonstrate:
- Network analysis techniques
- Data processing methodologies
- Python programming practices
- Cybersecurity research methods

## Disclaimer

This software is provided for educational purposes only. Users are responsible for ensuring their usage complies with all applicable laws and regulations.
