from backtest.strategies.Strategy import Strategy
from backtest.pricing.Portfolio import Portfolio
from backtest.pricing.Position import Position
from backtest.pricing.Stock import Stock


class ExampleStrategy(Strategy):
    def __init__(self, name: str, portfolio: Portfolio, hyperparams: dict) -> None:
        super().__init__(name, portfolio)  # call the constructor of the parent class
        self.hyperparams: dict = hyperparams  # strategy specific hyperparameters
        
    def update(self: "ExampleStrategy", quote: dict) -> None:
        
        if quote['id'] == 'Clock':

            if quote['timestamp'] == self.hyperparams['buy_date']:
                new_position = Position(Stock(self.hyperparams['ric']), 100)
                self.portfolio.enter(new_position)

            if quote['timestamp'] == self.hyperparams['sell_date']:
                self.portfolio.exit("JPM.N")
        