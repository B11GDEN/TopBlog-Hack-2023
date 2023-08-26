from datetime import datetime


class Instance:
    def __init__(self, prediction: list):
        bbox, text, prob = prediction
        (x1, y1), (x2, y2) = bbox[0], bbox[2]
        self.prob = prob
        self.bbox = [x1, y1, x2, y2]
        self.value, self.label = self.get_cls(text)
        if self.label == 'text':
            self.value = self.filter_text_value(self.value)
        self.match_instance = None
        self.is_user = False

    @staticmethod
    def filter_text_value(value: str):
        return value.lower().strip().replace('o', 'о').replace('0', 'о')

    @staticmethod
    def get_cls(value: str):
        # проверка на число с процентом
        if value.endswith('%'):
            try:
                num = float(value[:-1].replace(',', '.'))
                return num, 'number'
            except Exception:
                pass

        # проверка на число с часами
        if value.endswith('ч.'):
            try:
                num = float(value[:-2].replace(',', '.'))
                return num, 'number'
            except Exception:
                pass

        # проверка на число с тыс.
        if value.endswith('тыс.'):
            try:
                num = float(value[:-4].replace(',', '.'))
                return num*1000, 'number'
            except Exception:
                pass

        # проверка на число с тыс.
        if value.endswith('тыс:'):
            try:
                num = float(value[:-4].replace(',', '.'))
                return num * 1000, 'number'
            except Exception:
                pass

        # проверка на число с тыс.
        if value.endswith('тыс'):
            try:
                num = float(value[:-3].replace(',', '.'))
                return num * 1000, 'number'
            except Exception:
                pass

        # проверка на число с пробелами
        try:
            num = float(''.join(value.split(' ')).replace(',', '.'))
            return num, 'number'
        except Exception:
            pass

        # если это предложение
        if len(value.split(' ')) > 1:
            return value, 'text'

        # проверка на обычное число
        try:
            num = float(value.replace(',', '.'))
            return num, 'number'
        except Exception:
            pass

        # проверка на дату и время
        try:
            date = datetime.strptime(value, '%d.%m.%Y')
            return date, 'date'
        except:
            pass

        return value, 'text'
