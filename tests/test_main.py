from main import do_calculation, HTTPException, log_write, json
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.mark.asyncio
@patch("main.log_write", new_callable=AsyncMock)
async def test_do_calculation_good(mock_log_write):

    expected_result = {
        "31.01.2027": 10050,
        "28.02.2027": 10100.25,
        "31.03.2027": 10150.75
    }

    result = await do_calculation("31.01.2027", 3, 10000, float(6))

    assert result == expected_result
    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch("main.log_write", new_callable=AsyncMock)
async def test_do_calculation_bad_date(mock_log_write):

    with pytest.raises(HTTPException) as excinfo:
        await do_calculation("32.01.2027", 3, 10000, float(6))

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Дата должна быть в формате dd.mm.YYYY"


@pytest.mark.asyncio
@patch("main.log_write", new_callable=AsyncMock)
async def test_do_calculation_bad_periods(mock_log_write):

    with pytest.raises(HTTPException) as excinfo:
        await do_calculation("31.01.2027", 100, 10000, float(6))

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Период должен быть целым числом от 1 до 60 месяцев"


@pytest.mark.asyncio
@patch("main.log_write", new_callable=AsyncMock)
async def test_do_calculation_bad_amount(mock_log_write):

    with pytest.raises(HTTPException) as excinfo:
        await do_calculation("31.01.2027", 3, 100, float(6))

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Сумма вклада должна быть целым числом от 10000 до 3000000"



@pytest.mark.asyncio
@patch("main.log_write", new_callable=AsyncMock)
async def test_do_calculation_bad_rate(mock_log_write):

    with pytest.raises(HTTPException) as excinfo:
        await do_calculation("31.01.2027", 3, 10000, float(0))

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Процентная ставка должна быть числом от 1 до 8"


@pytest.mark.asyncio
@patch("main.UseDataBase")  # Замени на правильный путь
async def test_log_write(mock_db):
    # Мокаем объект курсора
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor

    date = "31.01.2021"
    periods = 3
    amount = 10000
    rate = 6.0
    dbconfig = {'host': '127.0.0.1', 'user': 'testuser', 'password': 'testpassword', 'database': 'testdb'}
    results = {"31.01.2021": 10050.0, "28.02.2021": 10100.25, "31.03.2021": 10150.75}

    await log_write(date, periods, amount, rate, dbconfig, results)

    _SQL = """insert into log (request_date, periods, amount, rate, results) values (%s, %s, %s, %s, %s)"""

    # Фактический SQL запрос, вызванный в mock_cursor.execute
    actual_sql = mock_cursor.execute.call_args[0][0]

    # Убираем переносы строк для корректного сравнения
    expected_sql_clean = ' '.join(_SQL.split())
    actual_sql_clean = ' '.join(actual_sql.split())

    # Сравниваем строки SQL без учёта переносов строк и пробелов
    assert actual_sql_clean == expected_sql_clean

    # Проверяем аргументы вызова метода execute
    results_json = json.dumps(results)
    mock_cursor.execute.assert_called_once_with(
        actual_sql,  # Используем реальный SQL с переносом строк
        (date, periods, amount, rate, results_json)
    )
