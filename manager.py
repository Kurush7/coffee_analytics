import random

from prolog_wrapper import *
from repository import InfoRepo, LogicRepo


class InfoParser:
    def _add_indent(self, s, indent=0):
        return ' ' * indent + s

    def _parse_list(self, data, indent=0):
        if len(data) == 1:
            return self._parse_result(data[0], indent)
        s = ''
        for d in data:
            s += self._add_indent(f'---\n', indent)
            #s += self._add_indent(f'{self._parse_result(d, indent+2)}\n', indent)
            s += f'{self._parse_result(d, indent)}\n'
        return s

    def _parse_dict(self, data, indent=0):
        s = ''
        for k, v in data.items():
            if type(v) in [list, dict]:
                s += self._add_indent(f'{k}:\n', indent)
                #s += self._add_indent(f'{self._parse_result(v, indent+2)}\n', indent)
                s += f'{self._parse_result(v, indent+2)}\n'
            else:
                s += self._add_indent(f'{k}: {self._parse_result(v, indent+2)}\n', indent)
        return s

    def _parse_result(self, data, indent=0):
        if type(data) == list:
            s = self._parse_list(data, indent=indent)
        elif type(data) == dict:
            s = self._parse_dict(data, indent=indent)
        elif type(data) == bool:
            if data == False:
                s = self._add_indent('Данные не найдены', indent)
            else:
                s = self._add_indent('ОК', indent)
        else:
            s = self._add_indent(data, indent)
        s = s.replace(':  ', ': ')
        s = s.replace('\n\n', '\n')
        return s


class InfoManager(InfoParser):
    def __init__(self, repo: InfoRepo):
        self.repo = repo

    def info(self, *args, **kwargs):
        res = self.repo.info(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def coffee_sort(self, *args, **kwargs):
        res = self.repo.coffee_sort(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def process_types(self, *args, **kwargs):
        res = self.repo.process_types(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def cooking_type(self, *args, **kwargs):
        res = self.repo.cooking_type(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def roasting(self, *args, **kwargs):
        res = self.repo.roasting(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def grinding(self, *args, **kwargs):
        res = self.repo.grinding(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def ingredients(self, *args, **kwargs):
        res = self.repo.ingredients(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def instruments(self, *args, **kwargs):
        res = self.repo.instruments(*args, **kwargs)
        s = self._parse_result(res)
        print(s)

    def descriptors(self, *args, **kwargs):
        res = self.repo.descriptors(*args, **kwargs)
        s = self._parse_result(res)
        print(s)


class LogicManager(InfoManager):
    def __init__(self, repo: LogicRepo):
        super().__init__(repo)

    def _apply_array_logic(self, data, limit=None, offset=None, shuffle=False):
        if type(data) == list:
            if shuffle:
                random.shuffle(data)
            if offset is not None:
                data = data[offset:]
            if limit is not None:
                data = data[:limit]
        return data

    def from_what_to_cook(self, method, limit=None, offset=None, shuffle=False):
        res = self.repo.from_what_to_cook(method)
        res = self._apply_array_logic(res, limit, offset, shuffle)

        s = self._parse_result(res)
        print(s)

    def howto_cook(self, sort=None, process=None,roast=None, grind=None, limit=None, offset=None, shuffle=False):
        res = self.repo.howto_cook(sort, process, roast, grind)
        res = self._apply_array_logic(res, limit, offset, shuffle)

        s = self._parse_result(res)
        print(s)

    def predict_result(self, method=None,  sort=None, process=None, roast=None, grind=None, limit=None, offset=None, shuffle=False):
        if sum(x is not None for x in [method, sort, process, roast, grind]) == 0:
            raise Exception('гадание по воздуху ненаучно')

        res = self.repo.predict_result(method, sort, process, roast, grind)
        res = self._apply_array_logic(res, limit, offset, shuffle)

        s = self._parse_result(res)
        print(s)

    def howto_get_result(self, acidity=None, sweetness=None, bitterness=None, modifiers=None, limit=None, offset=None, shuffle=False):
        if sum(x is not None for x in [acidity, sweetness, bitterness, modifiers]) == 0:
            raise Exception('гадание по воздуху ненаучно')

        if modifiers is not None:
            modifiers = modifiers.split(',')

        res = self.repo.howto_get_result(acidity, sweetness, bitterness, modifiers)
        res = self._apply_array_logic(res, limit, offset, shuffle)

        s = self._parse_result(res)
        s = s.strip()
        if len(s) == 0:
            s = 'Данные не найдены'
        print(s)