import datetime as dt

import tqdm

import repo
import services as srvs
import db


def save_trading_data_since(date: dt.date) -> None:
    cur = date
    today = dt.date.today()
    pbar = tqdm.tqdm(total=(today - cur).days + 1, ncols=100)
    while cur <= today:
        data = srvs.get_trading_data(cur)
        if data:
            models = srvs.convert_dict_to_db_models(data)
            repo.add_trading_results(models)
        cur += dt.timedelta(days=1)
        pbar.update(1)


if __name__ == '__main__':
    db.create_tables()
    save_trading_data_since(dt.date(2023, 1, 1))
