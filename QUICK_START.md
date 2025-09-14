# Quick Start Guide

## Get Started in 3 Steps

### 1. Run the Application
```bash
./start.sh
```

### 2. Open Your Browser
Navigate to: http://localhost:8080

### 3. Start Exploring!
- Generate Kyber keypairs for secure key exchange
- Encapsulate and decapsulate shared secrets
- Generate Dilithium keypairs for digital signatures
- Sign and verify messages
- Monitor performance metrics in real-time

## What You'll See

### System Status Dashboard
- PQC library availability (real or simulated)
- Memory and CPU usage with IoT-like constraints
- Platform information

### CRYSTALS-Kyber Section
- **Generate Keypair**: Creates public/private key pair
- **Encapsulate Secret**: Creates shared secret and ciphertext
- **Decapsulate Secret**: Recovers shared secret using private key

### CRYSTALS-Dilithium Section
- **Generate Keypair**: Creates signing key pair
- **Sign Message**: Creates digital signature
- **Verify Signature**: Validates signature authenticity

### Performance Metrics
- Real-time execution times
- Resource usage monitoring
- Historical operation tracking

## Alternative Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv pqc_env
source pqc_env/bin/activate

# Install dependencies
pip install flask psutil

# Run tests
python3 test_app.py

# Start application
python3 app.py
```

## Test the System

Run the comprehensive demo:
```bash
source pqc_env/bin/activate
python3 demo.py
```

## Features Demonstrated

- **Post-Quantum Cryptography**: Kyber and Dilithium algorithms
- **IoT Simulation**: Resource constraints and monitoring
- **Performance Tracking**: Real-time metrics and timing
- **Database Storage**: SQLite for operation history
- **Clean Web Interface**: Professional, responsive design
- **Fallback Mode**: Works without liboqs installation

## Use Cases

- **Education**: Learn about post-quantum cryptography
- **Research**: Test PQC algorithms on resource-constrained systems
- **Development**: Prototype IoT security solutions
- **Demonstration**: Show PQC capabilities to stakeholders

## Troubleshooting

- **Port 5000 in use**: Change port in `app.py`
- **Database errors**: Delete `pqc_demo.db` to reset
- **Memory limits**: Adjust in `pqc_utils.py` ResourceMonitor class
- **liboqs not available**: Application runs in simulation mode

## Next Steps

- Install liboqs for real cryptographic operations
- Customize resource limits for your target platform
- Add more PQC algorithms (Falcon, SPHINCS+, etc.)
- Integrate with actual IoT devices

---

**Ready to explore post-quantum cryptography? Start with `./start.sh`!** 