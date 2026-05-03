# Annual Trading Statistics Web Application
## Overview
This project is an interactive web application developed using Streamlit to analyze and visualize annual trading statistics of Commercial Bank of Ceylon PLC.
It explores trading behavior, price volatility, and market relationships using statistical analysis and visual dashboards.

## Dataset
The dataset used in this project contains annual trading statistics of Commercial Bank of Ceylon PLC, including variables such as turnover, trade volume, share volume, and price range indicators.
#### The dataset was manually constructed by extracting and compiling information from publicly available sources. Due to this manual data collection process, the dataset may contain minor inconsistencies and may not fully represent official or perfectly verified market data.

## Features
- Interactive filtering by share class and year range
- Visualization of turnover trends and volatility
- Year-over-year growth analysis
- Statistical relationship analysis using regression models
- Turnover persistence analysis using lag models
- Market phase segmentation (Growth, Decline, Expansion)

## Screenshots
- [Introduction](screenshots/1.jpg)
  - [Dashboard Guide](screenshots/2.jpg)
- [Data & Visualization](screenshots/3.jpg)
- [Market Analysis](screenshots/5.jpg)

## Tools & Technologies
- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels
- OpenPyXL

## How to Run the Project
1. Install dependencies:
   - pip install -r requirements.txt
2. Run the Streamlit app:
   - streamlit run ComBank.py

## Limitations
- Dataset is manually compiled and may contain minor inaccuracies
- Only linear relationships are modeled
- External market factors are not included
- Limited historical scope of analysis

## Author
- Fazra Farook
- BSc (Hons) in Applied Statistics – University of Colombo

## Demo
- [Watch the application demo](https://drive.google.com/file/d/1EUPEjwqJXFIuZbMDo344cB7NM3kvhat8/view?usp=sharing)
