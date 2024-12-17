# backtest
Backtesting module for researching investment strategies at AIC

## Setup
This module should be integrated as submodule in other repositories:

```sh
git submodule add https://github.com/aachen-investment-club/backtest.git
git submodule update --init --recursive
```

## Example Run

```py
import pandas as pd
from backtest.Engine import Engine
from backtest.strategies.ExampleStrategy import ExampleStrategy
from backtest.pricing.Portfolio import Portfolio
from backtest.pricing.Market import Market
from dataloader.src.refintinvloader import load_preprocessed_data

def run() -> None:
    
    universe = ['JPM.N']
    data = load_preprocessed_data(universe)
    
    portfolio = Portfolio(100000, Market(universe))
    hyperparams = {
        'ric': 'JPM.N',
        'buy_date': pd.Timestamp('2010-01-01'),
        'sell_date': pd.Timestamp('2020-01-01')
    }
    strategy = ExampleStrategy('example_strategy', portfolio, hyperparams)
    engine = Engine(universe, data, strategy)
    engine.run()
    engine.save('outputs')
```