import pandas as pd
from backtest.strategies.Strategy import Strategy
from backtest.pricing.Portfolio import Portfolio
from backtest.pricing.Position import Position
from backtest.pricing.Stock import Stock


class TradeLogEval(Strategy):
    def __init__(self, name: str, portfolio: Portfolio, tradelog: dict, ric_lookup: dict) -> None:
        super().__init__(name, portfolio)  # call the constructor of the parent class
        self.tradelog: dict = tradelog  # trade log in specific format -> TODO: Write Docstring
        self.ric_lookup: dict = ric_lookup
        
    def update(self: "TradeLogEval", quote: dict) -> None:
        
        if quote['id'] == 'Clock':

            for i, entry in enumerate(self.tradelog):

                if quote['timestamp'] == pd.Timestamp(entry['date']):

                    if entry['type'] == 'DEPOSIT':
                        continue  # deposit should have been defined in portfolio before strategy starts

                    elif entry['type'] == 'PURCHASE':
                        new_position = Position(Stock(self.ric_lookup[entry['security']['ticker']]), entry['amount'])
                        self.portfolio.enter(new_position)

                    elif entry['type'] == 'DIVIDEND':
                        NotImplementedError('Needs to be implemented ASAP')

                    elif entry['type'] == 'REMOVAL':
                        NotImplementedError('Needs to be implemented ASAP')

                    elif entry['type'] == 'SALE':
                        NotImplementedError('Needs to be implemented ASAP')

