from flask import Flask, render_template, request, jsonify, session
from pqc_utils import PQCUtils
from database import Database
import json
import time

app = Flask(__name__)
app.secret_key = 'pqc_demo_secret_key_2024'

# Initialize PQC utilities and database
pqc_utils = PQCUtils()
db = Database()

@app.route('/')
def index():
    """Main page with PQC demonstration interface"""
    system_info = pqc_utils.get_system_info()
    performance_metrics = pqc_utils.get_performance_metrics()
    
    # Get recent operations from database
    recent_kyber = db.get_recent_kyber_operations(5)
    recent_dilithium = db.get_recent_dilithium_operations(5)
    performance_stats = db.get_performance_stats()
    
    return render_template('index.html', 
                         system_info=system_info,
                         performance_metrics=performance_metrics,
                         recent_kyber=recent_kyber,
                         recent_dilithium=recent_dilithium,
                         performance_stats=performance_stats)

@app.route('/api/kyber/keygen', methods=['POST'])
def kyber_keygen():
    """Generate Kyber keypair"""
    try:
        start_time = time.time()
        result = pqc_utils.generate_kyber_keypair()
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Store in database
        db.store_kyber_keygen(result['public_key'], result['private_key'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('kyber_keygen', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        # Store in session for demo purposes
        session['kyber_public_key'] = result['public_key']
        session['kyber_private_key'] = result['private_key']
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/kyber/encaps', methods=['POST'])
def kyber_encaps():
    """Encapsulate shared secret using Kyber"""
    try:
        data = request.get_json()
        public_key = data.get('public_key')
        
        if not public_key:
            return jsonify({'success': False, 'error': 'Public key is required'}), 400
        
        start_time = time.time()
        result = pqc_utils.kyber_encapsulate(public_key)
        execution_time = (time.time() - start_time) * 1000
        
        # Store in database
        db.store_kyber_encaps(public_key, result['ciphertext'], result['shared_secret'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('kyber_encaps', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/kyber/decap', methods=['POST'])
def kyber_decap():
    """Decapsulate shared secret using Kyber"""
    try:
        data = request.get_json()
        private_key = data.get('private_key')
        ciphertext = data.get('ciphertext')
        
        if not private_key or not ciphertext:
            return jsonify({'success': False, 'error': 'Private key and ciphertext are required'}), 400
        
        start_time = time.time()
        result = pqc_utils.kyber_decap(private_key, ciphertext)
        execution_time = (time.time() - start_time) * 1000
        
        # Store in database
        db.store_kyber_decap(private_key, ciphertext, result['shared_secret'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('kyber_decap', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/dilithium/keygen', methods=['POST'])
def dilithium_keygen():
    """Generate Dilithium keypair"""
    try:
        start_time = time.time()
        result = pqc_utils.generate_dilithium_keypair()
        execution_time = (time.time() - start_time) * 1000
        
        # Store in database
        db.store_dilithium_keygen(result['public_key'], result['private_key'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('dilithium_keygen', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        # Store in session for demo purposes
        session['dilithium_public_key'] = result['public_key']
        session['dilithium_private_key'] = result['private_key']
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/dilithium/sign', methods=['POST'])
def dilithium_sign():
    """Sign a message using Dilithium"""
    try:
        data = request.get_json()
        private_key = data.get('private_key')
        message = data.get('message')
        
        if not private_key or not message:
            return jsonify({'success': False, 'error': 'Private key and message are required'}), 400
        
        start_time = time.time()
        result = pqc_utils.dilithium_sign(private_key, message)
        execution_time = (time.time() - start_time) * 1000
        
        # Store in database
        db.store_dilithium_sign(private_key, message, result['signature'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('dilithium_sign', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/dilithium/verify', methods=['POST'])
def dilithium_verify():
    """Verify a signature using Dilithium"""
    try:
        data = request.get_json()
        public_key = data.get('public_key')
        message = data.get('message')
        signature = data.get('signature')
        
        if not public_key or not message or not signature:
            return jsonify({'success': False, 'error': 'Public key, message, and signature are required'}), 400
        
        start_time = time.time()
        result = pqc_utils.dilithium_verify(public_key, message, signature)
        execution_time = (time.time() - start_time) * 1000
        
        # Store in database
        db.store_dilithium_verify(public_key, message, signature, result['is_valid'])
        
        # Store performance metric
        metrics = pqc_utils.get_performance_metrics()
        db.store_performance_metric('dilithium_verify', execution_time, 
                                  metrics.get('memory_mb', 0), 
                                  metrics.get('cpu_percent', 0))
        
        return jsonify({
            'success': True,
            'result': result,
            'execution_time_ms': round(execution_time, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/metrics')
def get_metrics():
    """Get current performance metrics"""
    try:
        metrics = pqc_utils.get_performance_metrics()
        system_info = pqc_utils.get_system_info()
        performance_stats = db.get_performance_stats()
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'system_info': system_info,
            'performance_stats': performance_stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/history')
def get_history():
    """Get recent operations history"""
    try:
        recent_kyber = db.get_recent_kyber_operations(10)
        recent_dilithium = db.get_recent_dilithium_operations(10)
        
        return jsonify({
            'success': True,
            'kyber_operations': recent_kyber,
            'dilithium_operations': recent_dilithium
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/clear', methods=['POST'])
def clear_database():
    """Clear all stored data"""
    try:
        db.clear_database()
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Database cleared successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 