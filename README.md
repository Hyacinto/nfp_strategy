# NFP News Trading Robot

This project is a trading robot that performs backtesting on historical data around Non-Farm Payroll (NFP) announcements. It downloads historical data, calculates technical indicators, filters the data, and visualizes the results using Streamlit.


## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the main script:**
    ```sh
    python main.py
    ```

## Main Components

### main.py

This is the entry point of the project. It performs the following steps:
1. Downloads historical data using the *download_and_write* function.
2. Calculates technical indicators using the *calculate_and_save_indicators* function.
3. Filters the data using the *filtering* function.
4. Runs the Streamlit application to visualize the results.

### dukascopy.py

Contains functions to download historical data from Dukascopy:
- `download_dukascopy`
- `download_and_write`

### calculate_indicators.py

Contains functions to calculate technical indicators:
- `calculate_indicators_for_each_nfp`
- `calculate_and_save_indicators`

### nfp_strategy.py

Contains the strategy logic and visualization code for backtesting:
- Loads NFP dates and historical data with indicators.
- Visualizes the data using Plotly and Streamlit.
- Implements the trading strategy based on technical indicators.

## Data

The project uses historical data stored in the **data** directory:
- `nfp_dates.csv`: Contains NFP announcement dates and times.
- `nfp_eurusd.csv`: Contains raw historical data for EUR/USD.
- `nfp_eurusd_with_indicators.csv`: Contains historical data with calculated technical indicators.

## Running the Streamlit App

After running *main.py*, the Streamlit app will automatically start. You can access it in your web browser to visualize the backtesting results.

```sh
streamlit run strategies/nfp_strategy.py