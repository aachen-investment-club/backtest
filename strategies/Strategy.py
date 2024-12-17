from abc import ABC, abstractmethod
from backtest.pricing.Portfolio import Portfolio


class Strategy(ABC):
    def __init__(self: "Strategy", name: str, portfolio: Portfolio) -> None:
        self.name: str = name  # name of the strategy
        self.portfolio: Portfolio = portfolio

    @abstractmethod
    def update() -> None:
        raise NotImplementedError("Derived class should implement update()")
