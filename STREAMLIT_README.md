# Streamlit Application - English Version

## Overview
This Streamlit application provides an interactive web interface for exploring the social network analysis results of Xue Baochai (薛寶釵) from Dream of the Red Chamber.

## Features
- **Overview**: Key statistics and findings
- **Network Visualization**: Interactive and static network graphs
- **Centrality Analysis**: Detailed centrality metrics comparison
- **Interaction Details**: Filterable interaction records with context
- **Data Download**: Download analysis results in CSV/JSON format

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application, run:

```bash
streamlit run 4_streamlit_app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## Usage

1. **Overview Page**: View summary statistics and key findings
2. **Network Visualization**: Explore interactive network graphs (requires pyvis)
3. **Centrality Analysis**: Compare centrality metrics across characters
4. **Interaction Details**: Filter and explore specific interactions
5. **Data Download**: Download analysis results for further study

## Requirements

- Python 3.7+
- Streamlit 1.28.0+
- NetworkX 3.0+
- Pandas 1.5.0+
- Matplotlib 3.5.0+
- Pyvis 0.3.2+ (optional, for interactive graphs)

## Data Files Required

The application expects the following data files in the `data/` directory:
- `interactions.csv`: Interaction relationship data
- `results/centrality_metrics.csv`: Centrality metrics for all characters
- `results/薛寶釵_metrics.json`: Detailed metrics for Xue Baochai

## Notes

- The application is now fully in English
- Character names remain in Chinese characters as they are part of the data
- Interactive network graphs require the `pyvis` library

