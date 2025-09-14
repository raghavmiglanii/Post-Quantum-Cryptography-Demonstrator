# Post-Quantum Cryptography Demo

A minimal Python-based web interface for demonstrating post-quantum cryptography (PQC) algorithms on IoT-like devices. This application showcases CRYSTALS-Kyber for key encapsulation and CRYSTALS-Dilithium for digital signatures with a clean, professional interface.

## Features

- **CRYSTALS-Kyber**: Key encapsulation mechanism (KEM) for secure key exchange
- **CRYSTALS-Dilithium**: Digital signature algorithm for authentication
- **Resource Monitoring**: Simulates IoT constraints with memory and CPU limits
- **Performance Metrics**: Real-time measurement of cryptographic operations
- **SQLite Storage**: Persistent storage of operations and metrics
- **Clean Web Interface**: Professional, responsive design optimized for usability
- **Fallback Mode**: Simulation mode when liboqs is not available
- **Real-time Updates**: Auto-refreshing metrics and system status

## System Requirements

- Python 3.7+
- Flask 2.3.3+
- psutil (for resource monitoring)
- liboqs-python (optional, for real PQC algorithms)

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Install liboqs for real PQC algorithms**:
   ```bash
   # On macOS with Homebrew:
   brew install liboqs
   pip install liboqs-python
   
   # On Ubuntu/Debian:
   sudo apt-get install liboqs-dev
   pip install liboqs-python
   
   # On Windows:
   # Download pre-built binaries from liboqs GitHub releases
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8080
   ```

3. **Use the web interface**:
   - Generate Kyber keypairs for secure key exchange
   - Encapsulate/decapsulate shared secrets
   - Generate Dilithium keypairs for digital signatures
   - Sign and verify messages
   - Monitor performance metrics and resource usage

## Web Interface Design

The application features a clean, professional web interface designed for:
- **Clarity**: Simple, intuitive layout without unnecessary visual clutter
- **Responsiveness**: Works seamlessly on desktop and mobile devices
- **Accessibility**: High contrast, readable fonts, and clear visual hierarchy
- **Performance**: Minimal JavaScript with efficient DOM updates

### Interface Components
- **System Status Panel**: Real-time monitoring of PQC library availability, memory, and CPU usage
- **Cryptographic Operations**: Separate cards for Kyber and Dilithium operations
- **Performance Metrics**: Live updates of operation execution times
- **Result Display**: Clean formatting of cryptographic outputs and execution statistics

## Architecture

### Core Components

- **`app.py`**: Main Flask application with REST API endpoints
- **`pqc_utils.py`**: PQC cryptographic operations and resource monitoring
- **`database.py`**: SQLite database for storing operations and metrics
- **`templates/index.html`**: Clean, responsive web interface

### API Endpoints

#### Kyber Operations
- `POST /api/kyber/keygen` - Generate Kyber keypair
- `POST /api/kyber/encaps` - Encapsulate shared secret
- `POST /api/kyber/decap` - Decapsulate shared secret

#### Dilithium Operations
- `POST /api/dilithium/keygen` - Generate Dilithium keypair
- `POST /api/dilithium/sign` - Sign a message
- `POST /api/dilithium/verify` - Verify a signature

#### System Information
- `GET /api/metrics` - Get performance metrics and system info
- `GET /api/history` - Get recent operations history
- `POST /api/clear` - Clear all stored data

### API Response Format

All API endpoints return JSON responses with the following structure:

```json
{
    "success": true|false,
    "result": {...},  // Operation result data
    "execution_time_ms": 123.45,  // Execution time in milliseconds
    "error": "Error message"  // Only present when success is false
}
```

### Error Handling

The application includes comprehensive error handling:
- **Input Validation**: Checks for required parameters and valid data formats
- **Cryptographic Errors**: Graceful handling of PQC operation failures
- **Resource Limits**: Monitoring and enforcement of memory/CPU constraints
- **Network Errors**: User-friendly error messages for connection issues

## IoT Simulation Features

### Resource Constraints
- **Memory Limit**: 50MB maximum usage
- **CPU Limit**: 80% maximum CPU usage
- **Real-time Monitoring**: Continuous resource tracking

### Performance Metrics
- Key generation time
- Encryption/decryption time
- Signature/verification time
- Memory and CPU usage
- Operation counts and averages

## Cryptographic Algorithms

### CRYSTALS-Kyber
- **Purpose**: Key encapsulation mechanism
- **Security Level**: 128-bit post-quantum security
- **Key Sizes**: Public key ~800 bytes, Private key ~1632 bytes
- **Ciphertext**: ~768 bytes
- **Shared Secret**: 32 bytes
- **Use Cases**: Secure key exchange, hybrid encryption systems

### CRYSTALS-Dilithium
- **Purpose**: Digital signature algorithm
- **Security Level**: 128-bit post-quantum security
- **Key Sizes**: Public key ~1952 bytes, Private key ~4000 bytes
- **Signature**: ~2701 bytes
- **Use Cases**: Digital signatures, authentication, document signing

## Database Schema

### Tables
- `kyber_operations`: Store Kyber key generation and encapsulation operations
- `dilithium_operations`: Store Dilithium key generation, signing, and verification
- `performance_metrics`: Store execution times and resource usage

### Data Persistence
- **Operation History**: Complete audit trail of all cryptographic operations
- **Performance Tracking**: Historical data for performance analysis
- **Resource Monitoring**: Long-term resource usage patterns

## Development

### Adding New PQC Algorithms
1. Extend `PQCUtils` class in `pqc_utils.py`
2. Add corresponding API endpoints in `app.py`
3. Update the web interface in `templates/index.html`
4. Add database tables in `database.py`

### Customizing Resource Limits
Modify the `ResourceMonitor` class in `pqc_utils.py`:
```python
self.resource_monitor = ResourceMonitor(
    max_memory_mb=50,      # Adjust memory limit
    max_cpu_percent=80.0   # Adjust CPU limit
)
```

### Web Interface Customization
The interface uses a clean, minimal design that can be easily customized:
- **Colors**: Modify CSS variables for consistent theming
- **Layout**: Adjust grid systems and spacing for different screen sizes
- **Typography**: Change fonts and sizing for improved readability

## Troubleshooting

### Common Issues

1. **liboqs Import Error**:
   - The application will automatically fall back to simulation mode
   - Install liboqs for real cryptographic operations

2. **Memory/CPU Limits Exceeded**:
   - Increase limits in `ResourceMonitor` class
   - Or optimize the cryptographic operations

3. **Database Errors**:
   - Delete `pqc_demo.db` file to reset the database
   - Check file permissions in the project directory

4. **Web Interface Issues**:
   - Clear browser cache and cookies
   - Check browser console for JavaScript errors
   - Verify Flask server is running on correct port

### Performance Tips

- Use simulation mode for development and testing
- Install liboqs for production use with real PQC algorithms
- Monitor resource usage in the web interface
- Clear database periodically to maintain performance
- Use modern browsers for optimal web interface performance

## Security Notes

- This is a demonstration application
- Keys and signatures are stored in plain text for educational purposes
- Do not use this application for production cryptographic operations
- Always use established cryptographic libraries for real applications
- The web interface is designed for local development and testing

## Browser Compatibility

The web interface is tested and optimized for:
- **Chrome/Chromium**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## License

This project is for educational and demonstration purposes only.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the demonstration application.

## References

- [CRYSTALS-Kyber](https://pq-crystals.org/kyber/)
- [CRYSTALS-Dilithium](https://pq-crystals.org/dilithium/)
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [NIST Post-Quantum Cryptography](https://www.nist.gov/programs-projects/post-quantum-cryptography)
- [Flask Web Framework](https://flask.palletsprojects.com/) 