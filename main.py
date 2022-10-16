

from manager import InfoManager, LogicManager
from prolog_wrapper import PrologWrapper
from qr_console import QRConsole, QRCommand

from repository import InfoRepo, LogicRepo


def create_console(manager):
    def add_array_params(command):
        return command\
            .add_argument('--макс', type=int, default=None, help='вернуть не более указанного числа результатов')\
            .add_argument('--отступ', type=int, default=None, help='пропустить указанное число результатов')\
            .add_argument('--рандом', action='store_true', help='перемешать результаты')

    console = QRConsole(hello='Добро пожаловать в информационную систему по способам приготовления кофе.')
    console.add_command(QRCommand('инфо', manager.info, 'получение общий сведений (глоссарий)')
                        .add_argument('--про', type=str, default=None, help='объект, о котором необходимы сведения')
                        )
    console.add_command(QRCommand('сорта кофе', manager.coffee_sort, 'получение сведений о сортах кофе'))
    console.add_command(QRCommand('типы обработки', manager.process_types, 'получение сведений о типах обработки кофе'))
    console.add_command(QRCommand('способы приготовления', manager.cooking_type, 'получение сведений о способах приготовления'))
    console.add_command(QRCommand('виды обжарки', manager.roasting, 'получение сведений о видах обжарки'))
    console.add_command(QRCommand('виды помола', manager.grinding, 'получение сведений о видах помола'))
    console.add_command(QRCommand('ингредиенты', manager.ingredients, 'получение сведений об ингредиентах, которые могут быть использованы при приготовлении'))
    console.add_command(QRCommand('инструменты', manager.instruments, 'получение сведений об инструменты, которые могут быть использованы при приготовлении'))
    console.add_command(QRCommand('дескрипторы', manager.descriptors, 'получение сведений дескрипторах вкуса'))

    console.add_command(
        add_array_params(
            QRCommand('из чего приготовить', manager.from_what_to_cook, 'получение возможных ингредиентов и инструментов')
                        .add_argument('кофе', type=str, default='эспрессо', help='способ приготовления')
                        )
    )

    console.add_command(
        add_array_params(
            QRCommand('что приготовить из', manager.howto_cook, 'получение возможных способов приготовления указанного кофе')
                        .add_argument('--сорт', type=str, default=None, help='сорт кофе')
                        .add_argument('--обработка', type=str, default=None, help='способ обработки кофе')
                        .add_argument('--обжарка', type=str, default=None, help='степень обжарки кофе')
                        .add_argument('--помол', type=str, default=None, help='степень помола кофе')
                        )
    )

    console.add_command(
        add_array_params(
            QRCommand('что получится', manager.predict_result, 'получение возможных способов приготовления указанного кофе')
                        .add_argument('--способ', type=str, default=None, help='название способа приготовления')
                        .add_argument('--сорт', type=str, default=None, help='сорт кофе')
                        .add_argument('--обработка', type=str, default=None, help='способ обработки кофе')
                        .add_argument('--обжарка', type=str, default=None, help='степень обжарки кофе')
                        .add_argument('--помол', type=str, default=None, help='степень помола кофе')
                        )
    )

    console.add_command(
        add_array_params(
            QRCommand('как бы так приготовить', manager.howto_get_result, 'получение возможных ингредиентов и инструментов')
                        .add_argument('--кислотность', type=str, default=None, help='уровень кислотности')
                        .add_argument('--сладость', type=str, default=None, help='уровень сладости')
                        .add_argument('--горечь', type=str, default=None, help='уровень горечи')
                        .add_argument('--дескрипторы', type=str, default=None, help='дескрипторы (через запятую, без пробелов)')
                        )
    )

    return console


def main():
    pw = PrologWrapper('prolog')
    manager = LogicManager(LogicRepo(pw))

    print('\n')
    console = create_console(manager)
    console.run()

    # список запросов из readme
    # инфо --про "сорт кофе"
    # "способы приготовления"
    # "из чего приготовить" аффогато --макс=2 --рандом
    # "что приготовить из" --помол=крупный --макс=2 --рандом
    # "что получится" --способ=эспрессо --сорт=кения --макс=2 --рандом
    # "как бы так приготовить" --кислотность=средний --сладость=средний --дескрипторы=фруктовый --макс=2 --рандом
    # "как бы так приготовить" --модификаторы=яблоко


if __name__ == '__main__':
    main()
