from decimal import Decimal, InvalidOperation
import datetime

goods = {
    'Фабрика №2: яйца': [
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2024, 9, 20)},
        {'amount': Decimal('3'), 'expiration_date': datetime.date(2024, 9, 22)}
    ],
    'Яйца Фабрики №1': [
        {'amount': Decimal('1'), 'expiration_date': datetime.date(2024, 9, 24)}
    ],
    'макароны': [
        {'amount': Decimal('100'), 'expiration_date': None}
    ]
}


def add(items, title, amount, expiration_date=None):
    if isinstance(expiration_date, str):
        expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()

    if title not in items:
        items[title] = []
    items[title].append({'amount': amount, 'expiration_date': expiration_date})


def add_by_note(items, note):
    parts = note.split()

    amount = None
    title = ''
    expiration_date = None
    for i, part in enumerate(parts):
        try:
            amount = Decimal(part)
            title = ' '.join(parts[:i])
            if len(parts) > i + 1 and parts[-1].count('-') == 2:
                expiration_date = datetime.datetime.strptime(parts[-1], '%Y-%m-%d').date()
            else:
                expiration_date = None
            break
        except (InvalidOperation, IndexError):
            continue
    if amount is None:
        raise ValueError(f'Количество не найдено в строке: {note}')

    add(items, title, amount, expiration_date)


def find(items, needle):
    result = []
    for item in items.keys():
        if needle.lower() in item.lower():
            result.append(item)
    return result


def amount(items, needle):
    total_amount = Decimal('0')
    found_items = find(items, needle)

    for item in found_items:
        for entry in items[item]:
            total_amount += entry['amount']
    return total_amount


def expire(items, in_advance_days=0):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=in_advance_days) if in_advance_days is not None else today
    expired_items = []

    for product, batches in goods.items():
        total_amount = Decimal('0')
        for batch in batches:
            expiration_date = batch['expiration_date']
            amount = batch['amount']
            if expiration_date is not None and expiration_date <= future_date:
                total_amount += amount
        if total_amount > 0:
            expired_items.append((product, total_amount))

    return expired_items