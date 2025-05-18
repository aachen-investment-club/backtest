import pandas as pd
from tqdm import tqdm
import os

# own modules
from backtest.pricing.Portfolio import Portfolio
from backtest.pricing.Market import Market
from backtest.datastream.Datastream import Datastream
from backtest.datastream.EODSource import EODSource
from backtest.strategies.Strategy import Strategy


class Engine():
    def __init__(self, universe: list[str], data: dict, strategy: Strategy) -> None:

        # create datasources
        sources = []
        for ric in universe:
            sources.append(EODSource(ric, data[ric]))

        # create datasource manager
        self.datastream: Datastream = Datastream(
            data_sources=sources,
            clock_cycle=pd.Timedelta(days=1)
        )

        # set strategy, portfolio and market
        # TODO: I am not sure if it is smart to implement it like this
        self.strategy: Strategy = strategy
        self.portfolio: Portfolio = self.strategy.portfolio
        self.market: Market = self.strategy.portfolio.market

        # backtest results
        self.portfolio_nav: dict[pd.Timestamp, float] = {}


    def run(self) -> None:
        
        # loop through data
        with tqdm(total=self.datastream.total_data_obj) as pbar:  # init progress bar
            while True:

                # get next data object
                quote = self.datastream.pop_next()

                # break if done
                if quote is None:
                    break

                # update market
                self.market.update(quote)

                # update strategy
                self.strategy.update(quote)

                # track backtest results
                if quote['id'] == 'Clock':
                    self.portfolio_nav[quote['timestamp']] = self.portfolio.nav()

                # update progress bar
                pbar.update(1)

        # returns = pd.Series(self.portfolio_nav).pct_change().dropna()




    def save(self, dir: str) -> None:

        # create new directory with time as folder name
        save_dir = dir + "/" + self.strategy.name + "/" + pd.Timestamp.now().strftime("%Y%m%d-%H%M%S") + "/"
        os.makedirs(save_dir, exist_ok=True)

        # save nav df
        nav_df = pd.DataFrame(self.portfolio_nav.items(), columns=['timestamp', 'nav'])
        nav_df.set_index('timestamp', inplace=True)
        nav_df['nav_norm'] = (nav_df['nav'] / nav_df['nav'].iloc[0]) * 100
        nav_df['returns'] = nav_df['nav'].pct_change()
        nav_df.to_parquet(save_dir + 'nav.parquet')

       # TODO: Compute stats


