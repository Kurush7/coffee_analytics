import os
from types import MappingProxyType

from swiplserver import PrologMQI, PrologThread


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
        res = self.prolog.query(q)
        if type(res) == list:
            return unique_dict_list(res)
        else:
            return res