from datetime import datetime, date
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / 'products.json'


def load_products():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_products(products):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)
def days_left(srok_godn):
    if not srok_godn:
        return None
    try:
        expiry_date = datetime.strptime(srok_godn, '%Y-%m-%d').date()
        return (expiry_date - date.today()).days
    except ValueError:
        return None

print(days_left('2026-11-15'))

@app.route('/', methods=['GET', 'POST'])
def home():
    products = load_products()
    print(products)
    holodil = []
    shkaf = []
    morozilka = []
    for index, product in enumerate(products):

        if product['storage'] == 'Холодильник':
            holodil.append((index,product))


            
        elif product['storage'] == 'Шкаф':
            shkaf.append((index,product))
        elif product['storage'] == 'Морозилка':
            morozilka.append((index,product))

    if request.method == 'POST':
        
            nazvanie = request.form['food']
            kategoria = request.form['kategoria']
            kolichestvo = float(request.form['kolvo'])
            meraizmerenia = request.form['meraizmerenia']
            data_izgot = request.form['data0']
            srok_godn = request.form['data']
            storage = request.form['storage']
    
            print(nazvanie)
            print(kategoria)
            print(kolichestvo)
            print(meraizmerenia)
            print(data_izgot)
            print(srok_godn)
            print(storage)
            product = {
            'nazvanie': nazvanie,
            'kategoria': kategoria,
            'kolichestvo': kolichestvo,
            'meraizmerenia': meraizmerenia,
            'data_izgot': data_izgot,
            'srok_godn': srok_godn,
            'ostalos': None,
            'storage': storage
            }
            products.append(product)
            save_products(products)
            return redirect('/')
            

    return render_template('tunhrum.html', products=products, holodil = holodil, shkaf = shkaf, morozilka = morozilka)
@app.route('/delete/<int:product_id>', methods=['GET', 'POST'])
def delete(product_id):
    products = load_products()
    products.pop(product_id)
    save_products(products)
    
    return redirect('/')
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    products = load_products()
    
    if product_id >= len(products):
        return redirect('/')
    if request.method == 'POST':
        products[product_id]['nazvanie'] = request.form['food']
        products[product_id]['kolichestvo'] = float(request.form['kolvo'])
        products[product_id]['meraizmerenia'] = request.form['meraizmerenia']
        save_products(products)
        return redirect('/')
    product = products[product_id]
    return render_template('edit.html', product=product, product_id=product_id)

if __name__ == '__main__':
    app.run(debug=True)


        