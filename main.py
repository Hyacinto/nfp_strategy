from utils.dukascopy import download_and_write
from indicators.calculate_indicators import calculate_and_save_indicators
from utils.filter import filtering
import subprocess

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "strategies/nfp_strategy.py"])

def main():
    print("🔄 Historical data downloading...")
    download_and_write()

    print("🔄 Indicators calculating...")
    calculate_and_save_indicators()

    print("🔄 Data filtering...")
    filtering()

if __name__ == "__main__":
    main()
    print("Every steps completed, visualization prepare...")
    run_streamlit()
