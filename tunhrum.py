
import json
from datetime import date, datetime
from pathlib import Path

def vivod(product):
    ostalos = product.get('ostalos')
                     
    if ostalos is None:
        ostalos_text = 'нет данных'
    elif ostalos > 0:
        ostalos_text = f'осталось: {ostalos} дн.'
    elif ostalos == 0:
        ostalos_text = 'истекает сегодня'
    else:
        ostalos_text = 'срок истёк'

    print(
        f"{product.get('nazvanie', 'Без названия')} | "
        f"{product.get('kolichestvo', 0)} "
        f"{product.get('meraizmerenia', '')} | "
        f"категория: {product.get('kategoria', 'Без категории')} | "
        f"место: {product.get('storage', 'Не указано')} | "
        f"срок: {product.get('srok_godn') or '—'} | "
        f"{ostalos_text}")

DATA_DIR = Path('TUNHRUM')
DATA_FILE = DATA_DIR / 'products.json'


while True:
    print('\nПерсональный холодильник ТунХрум')
    print('Хотите проверить продукты? (да/нет)')
    answer = input().strip().lower()

    if answer != 'да':
        print('До свидания!')
        break

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        products = []
    mestohr = input('1 — показать всё; 2 — холодильник; 3 — шкаф; 4 — морозилка')
    if mestohr == '1':
        print('Холодильник: ')
        for product in products:
            if product.get('storage') == 'Холодильник':
                vivod(product)
                    
        print('Шкаф: ')
        for product in products:
            if product.get('storage') == 'Шкаф':
                vivod(product)
        print('Морозилка: ')
        for product in products:
            if product.get('storage') == 'Морозилка':
                vivod(product)
    if mestohr == '2':
        print('Холодильник: ')
        print([product for product in products if product.get('storage') == 'Холодильник'])
    if mestohr == '3':
        print('Шкаф: ')
        print([product for product in products if product.get('storage') == 'Шкаф'])
    if mestohr == '4':
        print('Морозилка: ')
        print([product for product in products if product.get('storage') == 'Морозилка'])

    if not products:
        print('Нет продуктов')
    else:
        print('Сортировка: по дате добавления (по умолчанию)')
        print('Можно отсортировать по остатку дней, алфавиту или количеству.')

        sorti = input(
            'Введите "сортировка", чтобы выбрать порядок, '
            'или нажмите Enter: '
        ).strip().lower()

        if sorti == 'сортировка':
            print('1. Остаток дней')
            print('2. Алфавит')
            print('3. Количество')

            choice = input('Выберите сортировку: ').strip()

            if choice == '1':
                products.sort(
                    key=lambda p: (
                        p.get('ostalos') is None,
                        p.get('ostalos')
                        if p.get('ostalos') is not None else 0
                    )
                )
            elif choice == '2':
                products.sort(
                    key=lambda p: p.get('nazvanie', '').lower()
                )
            elif choice == '3':
                products.sort(
                    key=lambda p: p.get('kolichestvo', 0)
                )

        for product in products:
            ostalos = product.get('ostalos')

            if ostalos is None:
                ostalos_text = 'нет данных'
            elif ostalos > 0:
                ostalos_text = f'осталось: {ostalos} дн.'
            elif ostalos == 0:
                ostalos_text = 'истекает сегодня'
            else:
                ostalos_text = 'срок истёк'

            print(
                f"{product.get('nazvanie', 'Без названия')} | "
                f"{product.get('kolichestvo', 0)} "
                f"{product.get('meraizmerenia', '')} | "
                f"категория: {product.get('kategoria', 'Без категории')} | "
                f"место: {product.get('storage', 'Не указано')} | "
                f"срок: {product.get('srok_godn') or '—'} | "
                f"{ostalos_text}"
            )

    # Выбор действия
    dobavlenie = input(
        '\nВыберите действие:\n'
        '1. Добавить продукт\n'
        '2. Удалить продукт\n'
        '3. Изменить продукт\n'
        '4. Выйти\n'
        'Ваш выбор: '
    ).strip().lower()

    changed = False

    # Добавление продукта
    if dobavlenie in ('1', 'добавить'):
        while True:
            nazvanie = input('Введите название продукта: ').strip()
            kategoria = input('Введите категорию продукта: ').strip()
            print('Место хранения:')
            print('1. Холодильник')
            print('2. Шкаф')
            print('3. Морозилка')

            storage_choice = input('Выберите место хранения: ').strip()

            storage_options = {
                '1': 'Холодильник',
                '2': 'Шкаф',
                '3': 'Морозилка'
            }

            while storage_choice not in storage_options:
                print('Выберите 1, 2 или 3.')
                storage_choice = input(
                    'Выберите место хранения: '
                ).strip()

            storage = storage_options[storage_choice]
            
            meraizmerenia = input('Введите меру измерения: ').strip()

            
            while True:
                try:
                    kolichestvo = float(
                        input('Введите количество: ')
                    )

                    if kolichestvo <= 0:
                        print('Количество должно быть больше нуля.')
                        continue

                    break
                except ValueError:
                    print('Это не число, попробуй снова.')

            data_izgot = input(
                'Введите дату изготовления (ГГГГ-ММ-ДД, '
                'можно пропустить): '
            ).strip()

            srok_godn = input(
                'Введите срок годности (ГГГГ-ММ-ДД, '
                'можно пропустить): '
            ).strip()

            ostalos = None

            if srok_godn:
                try:
                    srok_godn_date = datetime.strptime(
                        srok_godn, '%Y-%m-%d'
                    ).date()

                    ostalos = (srok_godn_date - date.today()).days

                except ValueError:
                    print(
                        'Неверный формат даты. '
                        'Оставляю срок годности без расчёта.'
                    )
                    srok_godn = ''

            if data_izgot:
                try:
                    datetime.strptime(data_izgot, '%Y-%m-%d')
                except ValueError:
                    print(
                        'Неверный формат даты изготовления. '
                        'Оставляю дату пустой.'
                    )
                    data_izgot = ''

            products.append({
                'nazvanie': nazvanie,
                'kategoria': kategoria,
                'meraizmerenia': meraizmerenia,
                'kolichestvo': kolichestvo,
                'data_izgot': data_izgot,
                'srok_godn': srok_godn,
                'ostalos': ostalos,
                'storage': storage
            })

            changed = True

            answer = input(
                'Добавить ещё продукт? (да/нет): '
            ).strip().lower()

            if answer != 'да':
                break

    # Удаление продуктов
    elif dobavlenie == '2':
        while True:
            print('\nВыберите действие:')
            print('1. Удалить все продукты')
            print('2. Удалить по категории')
            print('3. Удалить по названию')
            print('4. Удалить продукты с истёкшим сроком годности')
            print('5. Вернуться в главное меню')

            option = input('Введите номер опции: ').strip()

            if option == '1':
                confirm = input(
                    'Точно удалить ВСЕ продукты? (да/нет): '
                ).strip().lower()

                if confirm == 'да':
                    if products:
                        products = []
                        changed = True
                        print('Все продукты удалены.')
                    else:
                        print('Список уже пуст.')

            elif option == '2':
                kategoria = input(
                    'Введите категорию для удаления: '
                ).strip()

                old_length = len(products)

                products = [
                    p for p in products
                    if p.get('kategoria', '').lower() != kategoria.lower()
                ]

                if len(products) < old_length:
                    changed = True
                    print('Продукты выбранной категории удалены.')
                else:
                    print('Такая категория не найдена.')

            elif option == '3':
                nazvanie = input(
                    'Введите название продукта для удаления: '
                ).strip()

                old_length = len(products)

                products = [
                    p for p in products
                    if p.get('nazvanie', '').lower() != nazvanie.lower()
                ]

                if len(products) < old_length:
                    changed = True
                    print('Продукт удалён.')
                else:
                    print('Такой продукт не найден.')

            elif option == '4':
                old_length = len(products)

                products = [
                    p for p in products
                    if not (
                        isinstance(p.get('ostalos'), int)
                        and not isinstance(p.get('ostalos'), bool)
                        and p['ostalos'] < 0
                    )
                ]

                if len(products) < old_length:
                    changed = True
                    print('Просроченные продукты удалены.')
                else:
                    print('Просроченных продуктов не найдено.')

            elif option == '5':
                break

            else:
                print('Неверный выбор.')
                continue

            answer = input(
                'Продолжить удаление? (да/нет): '
            ).strip().lower()

            if answer != 'да':
                break
    elif dobavlenie == '3':
        print('Выберите продукт для изменения:')
        
    elif dobavlenie in ('4', 'выйти', 'выход'):
        print('До свидания!')
        break

    else:
        print('Неизвестное действие.')
        continue

    # Сохранение данных
    if changed:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(
                products,
                f,
                ensure_ascii=False,
                indent=4
            )

        print('Изменения сохранены.')
