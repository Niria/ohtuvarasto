import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, warehouses, warehouse_counter


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Clear warehouses before each test
        warehouses.clear()
        warehouse_counter[0] = 0

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Manager', response.data)

    def test_index_shows_empty_state(self):
        response = self.client.get('/')
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_warehouse_page_loads(self):
        response = self.client.get('/warehouse/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse(self):
        response = self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '50'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertEqual(len(warehouses), 1)

    def test_view_warehouse(self):
        # Create a warehouse first
        self.client.post('/warehouse/new', data={
            'name': 'View Test',
            'capacity': '100',
            'initial_balance': '25'
        })

        response = self.client.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'View Test', response.data)
        self.assertIn(b'25.0', response.data)

    def test_view_nonexistent_warehouse_redirects(self):
        response = self.client.get('/warehouse/999', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_edit_warehouse(self):
        # Create a warehouse first
        self.client.post('/warehouse/new', data={
            'name': 'Original Name',
            'capacity': '100',
            'initial_balance': '0'
        })

        # Edit the warehouse
        response = self.client.post('/warehouse/1/edit', data={
            'name': 'New Name'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Name', response.data)
        self.assertEqual(warehouses[1]['name'], 'New Name')

    def test_add_to_warehouse(self):
        # Create a warehouse first
        self.client.post('/warehouse/new', data={
            'name': 'Add Test',
            'capacity': '100',
            'initial_balance': '0'
        })

        # Add items
        response = self.client.post('/warehouse/1/add', data={
            'amount': '50'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(warehouses[1]['varasto'].saldo, 50.0)

    def test_remove_from_warehouse(self):
        # Create a warehouse first
        self.client.post('/warehouse/new', data={
            'name': 'Remove Test',
            'capacity': '100',
            'initial_balance': '50'
        })

        # Remove items
        response = self.client.post('/warehouse/1/remove', data={
            'amount': '25'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(warehouses[1]['varasto'].saldo, 25.0)

    def test_delete_warehouse(self):
        # Create a warehouse first
        self.client.post('/warehouse/new', data={
            'name': 'Delete Test',
            'capacity': '100',
            'initial_balance': '0'
        })

        self.assertEqual(len(warehouses), 1)

        # Delete the warehouse
        response = self.client.post('/warehouse/1/delete',
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouses), 0)

    def test_multiple_warehouses(self):
        # Create multiple warehouses
        self.client.post('/warehouse/new', data={
            'name': 'Warehouse 1',
            'capacity': '100',
            'initial_balance': '10'
        })
        self.client.post('/warehouse/new', data={
            'name': 'Warehouse 2',
            'capacity': '200',
            'initial_balance': '20'
        })

        response = self.client.get('/')
        self.assertIn(b'Warehouse 1', response.data)
        self.assertIn(b'Warehouse 2', response.data)
        self.assertEqual(len(warehouses), 2)

    def test_warehouse_uses_varasto_class(self):
        # Create a warehouse
        self.client.post('/warehouse/new', data={
            'name': 'Varasto Test',
            'capacity': '100',
            'initial_balance': '0'
        })

        varasto = warehouses[1]['varasto']
        # Test that it uses the Varasto class methods
        self.assertEqual(varasto.paljonko_mahtuu(), 100.0)

        varasto.lisaa_varastoon(30)
        self.assertEqual(varasto.saldo, 30.0)
        self.assertEqual(varasto.paljonko_mahtuu(), 70.0)

        taken = varasto.ota_varastosta(10)
        self.assertEqual(taken, 10.0)
        self.assertEqual(varasto.saldo, 20.0)
