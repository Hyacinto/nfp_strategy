from utils import dukascopy as download_data
from indicators import calculate_indicators
from utils import filter as filter_data
import subprocess
import os

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "../strategies/strategy.py"])

def main():
    print("Current working directory:", os.getcwd())
    print("🔄 Historical data downloading...")
    download_data.run()

    print("🔄 Indicators calculating...")
    calculate_indicators.run()

    print("🔄 Data filtering...")
    filter_data.run()

if __name__ == "__main__":
    main()
    print("Every steps completed, visualization prepare...")
    run_streamlit()
