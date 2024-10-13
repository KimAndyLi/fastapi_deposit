from fastapi import FastAPI, Request, Form, Body, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from datetime import datetime
from db import UseDataBase, ConnectionError, CredentialsError, SQLError
import json
from dateutil.relativedelta import relativedelta


app = FastAPI()

templates = Jinja2Templates(directory="templates")

dbconfig = {'host': 'db',
            'user': 'moneyman',
            'password': 'moneypasswd',
            'database': 'moneyDB', }


@app.get("/", response_class=HTMLResponse)
@app.get("/entry", response_class=HTMLResponse)
async def entry_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="entry.html")


@app.post('/do_count')
async def do_calculation(date: Annotated[str, Form()],
                         periods: Annotated[int, Form()],
                         amount: Annotated[int, Form()],
                         rate: Annotated[float, Form()]):

    try:
        datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Дата должна быть в формате dd.mm.YYYY")

    if not isinstance(periods, int) or not (1 <= periods <= 60):
        raise HTTPException(status_code=400, detail="Период должен быть целым числом от 1 до 60 месяцев")

    if not isinstance(amount, int) or not (10000 <= amount <= 3000000):
        raise HTTPException(status_code=400, detail="Сумма вклада должна быть целым числом от 10000 до 3000000")

    if not isinstance(rate, float) or not (1 <= rate <= 8):
        raise HTTPException(status_code=400, detail="Процентная ставка должна быть числом от 1 до 8")

    results = await calculate_deposit_per_month(amount, rate, periods, date)

    try:
        await log_write(date, periods, amount, rate, dbconfig, results)
    except Exception as err:
        print(f'***** Logging failed with next error: {err}')

    return results


async def calculate_deposit_per_month(amount, rate, periods, start_date, compounding_frequency=12):
    rate_decimal = rate / 100
    monthly_rate = rate_decimal / compounding_frequency
    results = {}

    current_amount = amount
    current_date = datetime.strptime(start_date, "%d.%m.%Y")
    original_day = current_date.day

    for i in range(periods):
        current_amount *= (1 + monthly_rate)
        results[current_date.strftime("%d.%m.%Y")] = round(current_amount, 2)
        next_date = current_date + relativedelta(months=1)
        try:
            current_date = next_date.replace(day=original_day)
        except ValueError:
            current_date = next_date + relativedelta(day=31)

    return results


async def log_write(date, periods, amount, rate, dbconfig, results) -> None:
    try:
        results_json = json.dumps(results)
        with UseDataBase(dbconfig) as cursor:
            _SQL = """insert into log (request_date, periods, amount, rate, results)
            values (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (date,
                                  periods,
                                  amount,
                                  rate,
                                  results_json,))
    except ConnectionError as err:
        print(f'Something went wrong: {err}')
    except Exception as err:
        print(f'Something went wrong: {err}')
    return 'Error'
