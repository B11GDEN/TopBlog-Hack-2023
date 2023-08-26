from datetime import datetime

TYPE2COLOR = {
    'text': 'red',
    'number': 'green',
    'date': 'yellow',
}


def text_cls(value: str):
    # проверка на число с процентом
    if value.endswith('%'):
        try:
            num = float(value[:-1])
            return 'number'
        except Exception:
            pass

    # если это предложение
    if len(value.split(' ')) > 1:
        return 'text'

    # проверка на обычное число
    try:
        num = float(value)
        return 'number'
    except Exception:
        pass

    # проверка на дату и время
    try:
        num = datetime.strptime(value, '%d.%m.%Y')
        return 'date'
    except:
        pass

    return 'text'
