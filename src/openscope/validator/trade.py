import json
from typing import Dict, List, Union

import requests

from src.openscope.validator.config import Config

DEFAULT_TOKENS = [
    "0x514910771af9ca656af840dff83e8264ecf986ca",
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "0x6982508145454ce325ddbe47a25d4ec3d2311933",
    "0xaea46a60368a7bd060eec7df8cba43b7ef41ad85",
    "0x808507121b80c02388fad14726482e061b8da827",
    "0x9d65ff81a3c488d585bbfb0bfe3c7707c7917f54",
    "0x6e2a43be0b1d33b726f0ca3b8de60b3482b8b050",
    "0xc18360217d8f7ab5e7c516566761ea12ce7f9d72",
    "0xa9b1eb5908cfc3cdf91f9b8b3a74108598009096",
    "0x57e114b691db790c35207b2e685d4a43181e6061",
]


class Account:
    def __init__(self, portfolio, avg_price, win_rate, balance, time_stamp):
        self.portfolio = portfolio
        self.initial_balance = balance or 0
        self.avg_price = {} if avg_price is None else avg_price.copy()
        self.first_trade = time_stamp or 0
        self.win_rate = {} if win_rate is None else win_rate.copy()


def init_account(account_id: str):
    portfolio = {account_id: {}}
    for item in DEFAULT_TOKENS:
        asset = {"asset": 0.0, "usd": 10.0}
        portfolio[item] = asset
    account = Account(
        portfolio=portfolio, avg_price=None, win_rate=None, balance=0, time_stamp=0
    )
    return account


class Order:
    def __init__(
        self,
        miner_id,
        token,
        is_close,
        direction,
        nonce,
        price,
        price_4h,
        time_stamp,
    ):
        self.miner_id = miner_id
        self.token = token
        self.is_close = is_close
        self.direction = direction
        self.nonce = nonce
        self.price = price
        self.price_4h = price_4h
        self.time_stamp = time_stamp


def process_order(
    accounts: Dict[str, Account], order: Order, latest_price: Dict[str, float]
):
    if not accounts:
        raise ValueError("accounts is empty")
    address = order.miner_id
    token = order.token
    # validate miner
    if address not in accounts.keys():
        return
    account = accounts[address]
    if account.first_trade == 0 or account.first_trade > order.time_stamp:
        account.first_trade = order.time_stamp
    # calculate winrate, only calculate open order
    if not order.is_close:
        if order.price_4h == 0:
            order.price_4h = latest_price.get(token, 0)
        if order.price < order.price_4h and order.direction == 1:
            account.win_rate[order.nonce] = 1
        elif order.price > order.price_4h and order.direction == -1:
            account.win_rate[order.nonce] = 1
        else:
            account.win_rate[order.nonce] = 0

    # calculate portfolio
    asset = accounts[address].portfolio.get(token, {})
    if order.is_close:
        new_asset = {
            "asset": 0.0,
        }
        balance = asset.get("asset", 0)
        if balance > 0:
            usd = balance * order.price
        else:
            avg_price = account.avg_price.get(token, 0)
            if avg_price == 0:
                return
            usd = (-balance) * avg_price * (1 - (order.price - avg_price) / avg_price)
        new_asset["usd"] = usd
        account.portfolio[token] = new_asset
        account.avg_price[token] = 0
    else:
        if order.direction == 1:
            usd_balance = asset.get("usd", 0)
            if usd_balance > 0:
                new_asset = {"usd": 0.0, "asset": usd_balance / order.price}
                account.portfolio[token] = new_asset
                account.avg_price[token] = order.price
            else:
                token_balance = asset.get("asset", 0)
                if token_balance < 0:
                    avg_price = account.avg_price.get(token, 0)
                    if avg_price == 0:
                        return
                    usd = (
                        (-token_balance)
                        * avg_price
                        * (1 - (order.price - avg_price) / avg_price)
                    )
                    amount = usd / order.price
                    new_asset = {
                        "asset": amount,
                        "usd": 0.0,
                    }
                    account.portfolio[token] = new_asset
                    account.avg_price[token] = order.price
        else:
            usd_balance = asset.get("usd", 0)
            if usd_balance > 0:
                new_asset = {"usd": 0.0, "asset": usd_balance / order.price * (-1)}
                account.portfolio[token] = new_asset
                account.avg_price[token] = order.price
            else:
                token_balance = asset.get("asset", 0)
                if token_balance > 0:
                    new_asset = {
                        "asset": token_balance * (-1),
                        "usd": 0.0,
                    }
                    account.portfolio[token] = new_asset
                    account.avg_price[token] = order.price

    accounts[address] = account
    print("Finished processing order, token_address: {}".format(order.token))
    return


def evaluate_account(account: Account, prices: Dict[str, float]):
    unrealized: float = 0
    usd_balance: float = 0
    # prices = get_latest_price()
    for token, asset in account.portfolio.items():
        latest_price = prices.get(token, 0)
        token_balance = asset.get("asset", 0)
        if token_balance > 0:
            unrealized += latest_price * token_balance
        elif token_balance < 0:
            avg_price = account.avg_price.get(token, 0)
            usd = (
                (-token_balance)
                * avg_price
                * (1 - (latest_price - avg_price) / avg_price)
            )
            unrealized += usd
        usd_balance += asset["usd"]

    pnl = usd_balance + unrealized - account.initial_balance
    roi = pnl / account.initial_balance * 100

    win = 0
    total_trades = len(account.win_rate.keys())
    for value in account.win_rate.values():
        if value > 0:
            win += 1
    win_rate = float(win / total_trades) if total_trades > 0 else 0.0
    return roi, win_rate


def get_latest_price(
    addr: str, pub_key: str, time_stamp: int, signature: str
) -> Union[dict, None]:
    config_file = "env/config.ini"
    config = Config(config_file)
    url = str(config.api.get("url")) + "getlatestprice"
    params = {
        "userId": addr,
        "pubKey": pub_key,
        "time_stamp": time_stamp,
        "sig": signature,
    }
    resp = requests.get(url, params=params, timeout=25)
    if resp.status_code != 200:
        return {}
    json_resp = json.loads(resp.text)
    if json_resp.get("code") == 200 and json_resp.get("data"):
        result = {}
        for price_data in json_resp["data"]:
            price = price_data["price"]
            token = price_data["tokenAddress"]
            result[token] = price
        return result
    else:
        return {}


def get_recent_orders(
    addr: str, pub_key: str, time_stamp: int, signature: str
) -> Union[List, None]:
    config_file = "env/config.ini"
    config = Config(config_file)
    url = str(config.api.get("url")) + "getalltrades"
    params = {
        "userId": addr,
        "pubKey": pub_key,
        "time_stamp": time_stamp,
        "sig": signature,
    }
    resp = requests.get(url, params=params, timeout=25)
    if resp.status_code != 200:
        return []
    json_resp = json.loads(resp.text)
    order_list = []
    if json_resp.get("code") == 200 and json_resp.get("data"):
        for order_data in json_resp["data"]:
            order = Order(
                miner_id=order_data.get("miner_id", ""),
                token=order_data.get("tokenAddress", ""),
                is_close=(order_data.get("PositionManager", "") == "close"),
                direction=order_data.get("direction", 0),
                nonce=order_data.get("nonce", 0),
                price=order_data.get("Tradeprice", 0),
                price_4h=order_data.get("Tradeprice_4h", 0),
                time_stamp=order_data.get("time_stamp", 0),
            )
            order_list.append(order)
        order_list.sort(key=lambda x: x.time_stamp)
        return order_list
    else:
        return []
