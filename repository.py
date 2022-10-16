import copy

from prolog_wrapper import *


class InfoRepo:
    def __init__(self, prolog: PrologWrapper):
        self.prolog = prolog
        self.prolog.start()

    def __del__(self):
        self.prolog.stop()

    def info(self, req=None):
        if req is None:
            req = 'Объект'
        else:
            req = '"' + req + '"'
        request = f'info({req}, Сведения)'
        return self.prolog.query(request)

    def coffee_sort(self):
        request = f'сорт_кофе(Сорт)'
        return self.prolog.query(request)

    def process_types(self):
        request = f'тип_обработки(Тип)'
        return self.prolog.query(request)

    def cooking_type(self):
        request = f'способ_приготовления(Способ, _, _)'
        return self.prolog.query(request)

    def roasting(self):
        request = f'обжарка(Обжарка)'
        return self.prolog.query(request)

    def grinding(self):
        request = f'помол(Помол)'
        return self.prolog.query(request)

    def ingredients(self):
        request1 = f'ингредиент(Ингредиент, _, _, _, _)'   # для кофе
        res1 = self.prolog.query(request1)

        request2 = f'ингредиент(Ингредиент)'
        res2 = self.prolog.query(request2)

        if res1 == False:
            res1 = []
        if res2 == False:
            res2 = []
        return res1 + res2

    def instruments(self):
        request = f'инструмент(Инструмент)'
        return self.prolog.query(request)

    def descriptors(self):
        request = f'колесо_вкусов(Дескриптор)'
        basic = self.prolog.query(request)

        request = f'колесо_вкусов(From, To)'
        res = self.prolog.query(request)
        mapping = {x['To']: x['From'] for x in res}

        def fill(x):
            x['Расширения'] = []
            for child, parent in mapping.items():
                if parent == x['Дескриптор']:
                    elem = {'Дескриптор': child}
                    fill(elem)
                    x['Расширения'].append(elem)
            if len(x['Расширения']) == 0:
                x.pop("Расширения")
        for b in basic:
            fill(b)
        return basic


class LogicRepo(InfoRepo):
    def _parse_functors(self, data):
        if type(data) == list:
            if len(data) == 0:
                return 'нет'
            return [self._parse_functors(d) for d in data]
        elif type(data) == dict:
            if list(data.keys()) == ['args', 'functor']:
                return self._parse_functors(self._decide_functor(data))
            else:
                for k in data.keys():
                    data[k] = self._parse_functors(data[k])
        return data

    def to_list(self, arr):
        return ', '.join(str(x) for x in arr)

    def _decide_functor(self, data):
        args, f = data['args'], data['functor']
        if f == 'инструмент':
            res = args[0]
        elif f == 'ингредиент':
            if args[0] == 'кофе':
                res = {'кофе': {'сорт': args[1], 'обработка': args[2], 'обжарка': args[3], 'помол': args[4]}}
            else:
                res = args[0]
        elif f == 'результат':
            res = {'уровень кислотности': args[0], 'уровень сладости': args[1], 'уровень горечи': args[2], 'возможные дескрипторы': self.to_list(args[3])}
        else:
            raise Exception('unknown functor')

        def post_process(x):
            if type(x) == dict:
                x = {k:post_process(v) for k, v in x.items() if v not in ['_', 'null']}
                if len(x) == 0:
                    x['ограничения'] = 'отсутствуют'
            return x
        return post_process(res)

    def from_what_to_cook(self, method):
        request = f'способ_приготовления("{method}", Ингредиенты, Инструменты)'
        res = self.prolog.query(request)

        res = self._parse_functors(res)
        return res

    def howto_cook(self, sort, process, roast, grind):
        params = [sort, process, roast, grind]
        for i in range(len(params)):
            if params[i] is None:
                params[i] = '_'
        request = f'способ_приготовления(Способ, [ингредиент(кофе, {",".join(params)})| ДопИнгредиенты], Инструменты)'
        res = self.prolog.query(request)

        res = self._parse_functors(res)
        return res

    def predict_result(self, method, sort, process, roast, grind):
        params = [method, sort, process, roast, grind]
        replace = ['Способ','Сорт','Обработка','Обжарка','Помол']
        for i in range(len(params)):
            if params[i] is None:
                params[i] = replace[i]

        req_part = f'способ_приготовления("{params[0]}", [ингредиент(кофе, {",".join(params[1:])})| ДопИнгредиенты], Инструменты)'
        request = f'{req_part}, результат({req_part}, Результат)'
        res = self.prolog.query(request)

        res = self._parse_functors(res)
        res = [{'Результат': x['Результат'], 'ДопПараметры': {k:v for k,v in x.items() if k != 'Результат'}} for x in res]
        return res

    def howto_get_result(self, acidity, sweetness, bitterness, modifiers):
        params = [acidity, sweetness, bitterness]
        for i in range(len(params)):
            if params[i] is None:
                params[i] = '_'

        # получить и обработать способы приготовления
        req_part = f'способ_приготовления(Способ, Ингредиенты, Инструменты)'
        result = f'''результат({','.join(['"'+x+'"' if x != '_' else '_' for x in params])}, Дескрипторы)'''
        request = f'{req_part}, результат({req_part}, {result})'
        res = self.prolog.query(request)
        res = self._parse_functors(res)

        if modifiers in [None, list()]:
            [r.pop('Дескрипторы') for r in res]
        else:
            # получить поддеревья модификаторов
            mods = copy.copy(modifiers)
            for m in modifiers:
                r = self.prolog.query(f'поддерево_колеса({m}, X)')
                if r != False:
                    mods.extend(x['X'] for x in r)
            mods = set(mods)
            res = [r for r in res if len(mods.intersection(r['Дескрипторы']))>0]
        return res