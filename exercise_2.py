import os
import logging
import datetime
import time
from functools import wraps


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            now = datetime.datetime.now()
            logging.basicConfig(level=logging.INFO, filename=path, filemode="w", force=True,
                                format="%(asctime)s %(levelname)s %(message)s")
            ret = old_function(*args, **kwargs)
            logging.info(f' ============== {now} ==================')
            logging.info(f'Запущена функция {old_function.__name__}')
            logging.info(f'Аргументы запущенной функциии. ARGS -  {args}, KWARGS -  {kwargs}')
            logging.info(f'Результат работы функции - {ret}')
            logging.info(f' ========================= КОНЕЦ ============================')
            return ret

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
