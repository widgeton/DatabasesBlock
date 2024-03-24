import models
import db


def add_trading_results(results: list[models.TradingResults]) -> None:
    with db.Session() as session:
        session.add_all(results)
        session.commit()
