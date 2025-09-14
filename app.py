from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from ecdsa import SigningKey, SECP256k1
import hashlib
from base58 import b58encode_check, b58decode_check
import requests
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Network configuration
NETWORKS = {
    'mainnet': {
        'name': 'Mainnet',
        'url': 'https://api.trongrid.io',
        'faucet': None,
        'explorer': 'https://tronscan.org'
    },
    'shasta': {
        'name': 'Shasta Testnet',
        'url': 'https://api.shasta.trongrid.io',
        'faucet': 'https://www.trongrid.io/shasta',
        'explorer': 'https://shasta.tronscan.org'
    }
}

def init_db():
    conn = sqlite3.connect('tron_wallet.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS wallets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  address TEXT UNIQUE,
                  private_key TEXT,
                  network TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  wallet_id INTEGER,
                  tx_id TEXT,
                  network TEXT,
                  to_address TEXT,
                  amount REAL,
                  status TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(wallet_id) REFERENCES wallets(id))''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('tron_wallet.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_wallet():
    priv_key = SigningKey.generate(curve=SECP256k1)
    priv_hex = priv_key.to_string().hex()
    pub_key = priv_key.get_verifying_key().to_string()
    address = b58encode_check(b'\x41' + hashlib.sha3_256(pub_key).digest()[-20:]).decode()
    return priv_hex, address

def get_balance(address, network):
    try:
        response = requests.get(f"{NETWORKS[network]['url']}/v1/accounts/{address}")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [{}])[0].get('balance', 0) / 1000000
        return 0
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0

@app.route('/set_network', methods=['POST'])
def set_network():
    try:
        network = request.form.get('network')
        if network in NETWORKS:
            session['network'] = network
            return jsonify({
                'status': 'success',
                'network': network,
                'message': 'Network switched successfully'
            })
        return jsonify({
            'status': 'error',
            'message': 'Invalid network specified'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error="Username and password are required")
        
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Username already exists")
        except Exception as e:
            return render_template('register.html', error=str(e))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['network'] = 'shasta'
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    network = session.get('network', 'shasta')
    db = get_db()
    
    # Get user wallets
    wallets = db.execute(
        "SELECT * FROM wallets WHERE user_id = ? AND network = ? ORDER BY created_at DESC",
        (session['user_id'], network)
    ).fetchall()
    
    # Get transactions
    transactions = db.execute(
        """SELECT t.*, w.address as from_address 
           FROM transactions t
           JOIN wallets w ON t.wallet_id = w.id
           WHERE w.user_id = ? AND t.network = ?
           ORDER BY t.timestamp DESC LIMIT 10""",
        (session['user_id'], network)
    ).fetchall()
    
    wallet_data = []
    for wallet in wallets:
        balance = get_balance(wallet['address'], network)
        wallet_data.append({
            'id': wallet['id'],
            'address': wallet['address'],
            'balance': balance,
            'created_at': wallet['created_at']
        })
    
    return render_template('dashboard.html',
        wallets=wallet_data,
        transactions=transactions,
        current_network=network,
        networks=NETWORKS,
        username=session.get('username'),
        explorer_url=NETWORKS[network]['explorer']
    )

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    try:
        priv_key, address = generate_wallet()
        network = session.get('network', 'shasta')
        
        db = get_db()
        db.execute(
            "INSERT INTO wallets (user_id, address, private_key, network) VALUES (?, ?, ?, ?)",
            (session['user_id'], address, priv_key, network)
        )
        db.commit()
        
        return jsonify({
            'status': 'success',
            'address': address,
            'private_key': priv_key,
            'message': 'Wallet created successfully'
        })
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Wallet already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_trx', methods=['POST'])
def send_transaction():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    data = request.json
    required_fields = ['private_key', 'to_address', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        network = session.get('network', 'shasta')
        priv_key = SigningKey.from_string(bytes.fromhex(data['private_key']), curve=SECP256k1)
        pub_key = priv_key.get_verifying_key().to_string()
        from_address = b58encode_check(b'\x41' + hashlib.sha3_256(pub_key).digest()[-20:]).decode()
        
        # Verify wallet belongs to user
        db = get_db()
        wallet = db.execute(
            "SELECT id FROM wallets WHERE address = ? AND user_id = ?",
            (from_address, session['user_id'])
        ).fetchone()
        
        if not wallet:
            return jsonify({'error': 'Wallet not found or not owned by user'}), 404
        
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
            
        amount_sun = int(amount * 1000000)
        
        # Create transaction
        tx = {
            "to_address": b58decode_check(data['to_address']).hex(),
            "owner_address": b58decode_check(from_address).hex(),
            "amount": amount_sun
        }
        
        response = requests.post(
            f"{NETWORKS[network]['url']}/wallet/createtransaction",
            json=tx
        )
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Failed to create transaction',
                'details': response.json()
            }), 400
            
        tx_data = response.json()
        
        # Sign transaction
        signature = priv_key.sign(bytes.fromhex(tx_data['txID'])).hex()
        
        # Broadcast transaction
        broadcast = {
            "txID": tx_data['txID'],
            "raw_data": tx_data['raw_data'],
            "signature": [signature]
        }
        
        response = requests.post(
            f"{NETWORKS[network]['url']}/wallet/broadcasttransaction",
            json=broadcast
        )
        
        result = response.json()
        if not result.get('result'):
            return jsonify({
                'error': 'Transaction failed',
                'details': result
            }), 400
        
        # Save transaction
        db.execute(
            '''INSERT INTO transactions 
               (wallet_id, tx_id, network, to_address, amount, status) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (wallet['id'], tx_data['txID'], network, 
             data['to_address'], amount, 'completed')
        )
        db.commit()
        
        return jsonify({
            'status': 'success',
            'tx_id': tx_data['txID'],
            'explorer_url': f"{NETWORKS[network]['explorer']}/#/transaction/{tx_data['txID']}"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)