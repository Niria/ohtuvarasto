from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# In-memory storage for warehouses
warehouses = {}
warehouse_counter = [0]


def get_next_id():
    warehouse_counter[0] += 1
    return warehouse_counter[0]


@app.route('/')
def index():
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/new', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', 'Unnamed Warehouse')
        capacity = float(request.form.get('capacity', 100))
        initial_balance = float(request.form.get('initial_balance', 0))

        warehouse_id = get_next_id()
        warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(capacity, initial_balance)
        }
        return redirect(url_for('index'))

    return render_template('create_warehouse.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))
    return render_template('view_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', warehouse['name'])
        warehouse['name'] = name
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    return render_template('edit_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if warehouse:
        amount = float(request.form.get('amount', 0))
        warehouse['varasto'].lisaa_varastoon(amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if warehouse:
        amount = float(request.form.get('amount', 0))
        warehouse['varasto'].ota_varastosta(amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
