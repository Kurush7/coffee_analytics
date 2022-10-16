import os
from types import MappingProxyType

from swiplserver import PrologMQI, PrologThread


class PrologWrapper:
    def __init__(self, prolog_dir):
        self.prolog_dir = prolog_dir

    def start(self):
        base_root = os.getcwd()
        os.chdir(self.prolog_dir)
        self.prolog = PrologMQI().create_thread()
        self.prolog.start()

        print('initializing prolog:')
        ok = self.prolog.query("set_prolog_flag(encoding,utf8).")
        for file in os.listdir('.'):
            print(f'\tloading {file}')
            ok &= self.prolog.query(f"consult(\"{file}\").")
        os.chdir(base_root)
        if not ok:
            raise Exception('failed to load prolog files')

    def stop(self):
        del self.prolog

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.prolog.stop()

    def query(self, q):
        return self.prolog.query(q)

def unique_dict_list(data):
    res = []
    for x in data:
        ok = True
        for a in res:
            if a == x:
                ok = False
        if ok:
            res.append(x)
    return res

def main():
    pw = PrologWrapper('prolog')
    pw.start()
    #res = pw.query('дескриптор(X).')
    #res = pw.query('результат(сорт_кофе(Coffee), тип_обработки(Process), Result).')
    #res = pw.query('сборка_модификаторов([результат("низкий","низкий", "низкий", [a,b]), результат("низкий","низкий", "низкий", [c])], Res)')
    #res = pw.query('сумма_категорий("низкий", "низкий", Res)')

    # запросить все способы приготовить и что из этого выльется
    #res = pw.query('способ_приготовления(Name, Ingredients, Instruments), результат(способ_приготовления(Name, Ingredients, Instruments), Res)')
    #res = pw.query('способ_приготовления(Name, Ingredients, Instruments)')
    #res = pw.query('ингредиент(кофе, S, P, R, G)')
    #res = pw.query('ингредиент(кофе, S, _, _, _)')

    # запросить способы с конкретным результатом
    #res = pw.query('способ_приготовления(Name, Ingredients, Instruments), результат(способ_приготовления(Name, Ingredients, Instruments), результат("низкий", _, _, _))')
    #res = pw.query('способ_приготовления(Name, _, _)')
    #res = pw.query('info(A, B)')
    res = pw.query(
        #'способ_приготовления("латте", Ingredients, Instruments), результат(способ_приготовления("латте", Ingredients, Instruments), Res)')
        'способ_приготовления("эспрессо", Ingredients, Instruments), результат(способ_приготовления("эспрессо", Ingredients, Instruments), Res)')
    # способ_приготовления("латте", Ingredients, Instruments), результат(способ_приготовления("латте", Ingredients, Instruments), Res).
    # todo запрос на вхождение в результат какого-либо модификатора

    if res == False:
        print(res)
    else:
        res = unique_dict_list(res)
        print(len(res))
        if len(res) > 20:
            res = res[:10] + res[-10:]
        for r in res:
            print(r)

    pw.stop()

if __name__ == '__main__':
    main()
