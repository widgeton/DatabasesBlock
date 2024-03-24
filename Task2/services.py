from io import BytesIO
import datetime as dt
import requests
import pandas as pn

import models


def get_trading_data(date: dt.date) -> dict[str:dict] | None:
    link = "https://spimex.com/upload/reports/oil_xls/oil_xls_{}162000.xls"
    offset = 7
    col_idxs_in_xls = [1, 2, 3, 4, 5, 14]
    columns = [
        "exchange_product_id",
        "exchange_product_name",
        "delivery_basis_name",
        "volume",
        "total",
        "count",
    ]
    convert_to_int = lambda x: 0 if x == '-' else int(x)
    converters = {
        "exchange_product_id": str,
        "exchange_product_name": str,
        "delivery_basis_name": str,
        "volume": convert_to_int,
        "total": convert_to_int,
        "count": convert_to_int,
    }

    res = requests.get(link.format(date.strftime("%Y%m%d")))
    if res.status_code == 200:
        while True:
            try:
                df = pn.read_excel(io=BytesIO(res.content),
                                   header=offset,
                                   usecols=col_idxs_in_xls,
                                   names=columns,
                                   converters=converters)
                offset = 7
                break
            except ValueError as err:
                if "invalid literal for int()" in str(err):
                    offset += 1
                else:
                    raise err
        df.dropna(subset=["exchange_product_name"], inplace=True)
        df["date"] = [date for _ in range(len(df))]
        return df.query("count > 0").to_dict()


def convert_dict_to_db_models(dct: dict[str:dict]) -> list[models.TradingResults]:
    lst = []
    for idx in dct["count"].keys():
        res = models.TradingResults(exchange_product_id=dct["exchange_product_id"][idx],
                                    exchange_product_name=dct["exchange_product_name"][idx],
                                    oil_id=dct["exchange_product_id"][idx][:4],
                                    delivery_basis_id=dct["exchange_product_id"][idx][4:7],
                                    delivery_basis_name=dct["delivery_basis_name"][idx],
                                    delivery_type_id=dct["exchange_product_id"][idx][-1],
                                    volume=dct["volume"][idx],
                                    total=dct["total"][idx],
                                    count=dct["count"][idx],
                                    date=dct["date"][idx])
        lst.append(res)
    return lst
