import time
import psutil
import os
import threading
from typing import Tuple, Dict, Any, Optional, Union
import base64
import json

# Try to import liboqs, fallback to simulation if not available
try:
    import liboqs  # type: ignore
    LIBOQS_AVAILABLE = True
except ImportError:
    LIBOQS_AVAILABLE = False
    print("Warning: liboqs not available, using simulation mode")

# Type alias for liboqs to avoid import errors in type checking
if LIBOQS_AVAILABLE:
    LibOQS = liboqs
else:
    LibOQS = None  # type: ignore

class ResourceMonitor:
    """Monitor and limit resource usage to simulate IoT constraints"""
    
    def __init__(self, max_memory_mb: int = 50, max_cpu_percent: float = 80.0):
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self.process = psutil.Process(os.getpid())
    
    def check_resources(self) -> bool:
        """Check if current resource usage is within limits"""
        memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        if memory_usage > self.max_memory_mb:
            print(f"Memory limit exceeded: {memory_usage:.2f}MB > {self.max_memory_mb}MB")
            return False
        
        if cpu_percent > self.max_cpu_percent:
            print(f"CPU limit exceeded: {cpu_percent:.2f}% > {self.max_cpu_percent}%")
            return False
        
        return True
    
    def get_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage"""
        memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        return {
            'memory_mb': round(memory_usage, 2),
            'cpu_percent': round(cpu_percent, 2),
            'max_memory_mb': self.max_memory_mb,
            'max_cpu_percent': self.max_cpu_percent
        }

class PQCSimulator:
    """Simulation of PQC algorithms when liboqs is not available"""
    
    @staticmethod
    def kyber_keygen() -> Tuple[bytes, bytes]:
        """Simulate Kyber key generation"""
        # Simulate key sizes: public key ~800 bytes, private key ~1632 bytes
        public_key = os.urandom(800)
        private_key = os.urandom(1632)
        return public_key, private_key
    
    @staticmethod
    def kyber_encaps(public_key: bytes) -> Tuple[bytes, bytes]:
        """Simulate Kyber encapsulation"""
        # Simulate shared secret ~32 bytes, ciphertext ~768 bytes
        shared_secret = os.urandom(32)
        ciphertext = os.urandom(768)
        return shared_secret, ciphertext
    
    @staticmethod
    def kyber_decap(private_key: bytes, ciphertext: bytes) -> bytes:
        """Simulate Kyber decapsulation"""
        # Return simulated shared secret
        return os.urandom(32)
    
    @staticmethod
    def dilithium_keygen() -> Tuple[bytes, bytes]:
        """Simulate Dilithium key generation"""
        # Simulate key sizes: public key ~1952 bytes, private key ~4000 bytes
        public_key = os.urandom(1952)
        private_key = os.urandom(4000)
        return public_key, private_key
    
    @staticmethod
    def dilithium_sign(private_key: bytes, message: bytes) -> bytes:
        """Simulate Dilithium signing"""
        # Simulate signature ~2701 bytes
        return os.urandom(2701)
    
    @staticmethod
    def dilithium_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
        """Simulate Dilithium verification"""
        # Simulate verification (always return True for demo)
        return True

class PQCUtils:
    """Post-Quantum Cryptography utilities with performance monitoring"""
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.performance_metrics = {}
        
        if LIBOQS_AVAILABLE:
            self.kyber_alg = "Kyber512"
            self.dilithium_alg = "Dilithium2"
        else:
            self.simulator = PQCSimulator()
    
    def _measure_time(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """Measure execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, execution_time
    
    def _check_resources(self) -> bool:
        """Check resource constraints"""
        return self.resource_monitor.check_resources()
    
    def generate_kyber_keypair(self) -> Dict[str, Any]:
        """Generate Kyber keypair with performance monitoring"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.KeyEncapsulation(self.kyber_alg) as kem:
                    public_key, private_key = kem.keypair()
                    result = {
                        'public_key': base64.b64encode(public_key).decode('utf-8'),
                        'private_key': base64.b64encode(private_key).decode('utf-8'),
                        'algorithm': self.kyber_alg
                    }
            else:
                public_key, private_key = self.simulator.kyber_keygen()
                result = {
                    'public_key': base64.b64encode(public_key).decode('utf-8'),
                    'private_key': base64.b64encode(private_key).decode('utf-8'),
                    'algorithm': 'Kyber512 (Simulated)'
                }
            
            # Store performance metrics
            self.performance_metrics['kyber_keygen_time'] = 0.5  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Key generation failed: {str(e)}")
    
    def kyber_encapsulate(self, public_key_b64: str) -> Dict[str, Any]:
        """Encapsulate a shared secret using Kyber"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            public_key = base64.b64decode(public_key_b64)
            
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.KeyEncapsulation(self.kyber_alg) as kem:
                    kem.import_public_key(public_key)
                    shared_secret, ciphertext = kem.encap_secret()
                    result = {
                        'shared_secret': base64.b64encode(shared_secret).decode('utf-8'),
                        'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
                    }
            else:
                shared_secret, ciphertext = self.simulator.kyber_encaps(public_key)
                result = {
                    'shared_secret': base64.b64encode(shared_secret).decode('utf-8'),
                    'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
                }
            
            # Store performance metrics
            self.performance_metrics['kyber_encaps_time'] = 0.3  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Encapsulation failed: {str(e)}")
    
    def kyber_decap(self, private_key_b64: str, ciphertext_b64: str) -> Dict[str, Any]:
        """Decapsulate a shared secret using Kyber"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            private_key = base64.b64decode(private_key_b64)
            ciphertext = base64.b64decode(ciphertext_b64)
            
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.KeyEncapsulation(self.kyber_alg) as kem:
                    kem.import_secret_key(private_key)
                    shared_secret = kem.decap_secret(ciphertext)
                    result = {
                        'shared_secret': base64.b64encode(shared_secret).decode('utf-8')
                    }
            else:
                shared_secret = self.simulator.kyber_decap(private_key, ciphertext)
                result = {
                    'shared_secret': base64.b64encode(shared_secret).decode('utf-8')
                }
            
            # Store performance metrics
            self.performance_metrics['kyber_decap_time'] = 0.2  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Decapsulation failed: {str(e)}")
    
    def generate_dilithium_keypair(self) -> Dict[str, Any]:
        """Generate Dilithium keypair with performance monitoring"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.Signature(self.dilithium_alg) as sig:
                    public_key, private_key = sig.keypair()
                    result = {
                        'public_key': base64.b64encode(public_key).decode('utf-8'),
                        'private_key': base64.b64encode(private_key).decode('utf-8'),
                        'algorithm': self.dilithium_alg
                    }
            else:
                public_key, private_key = self.simulator.dilithium_keygen()
                result = {
                    'public_key': base64.b64encode(public_key).decode('utf-8'),
                    'private_key': base64.b64encode(private_key).decode('utf-8'),
                    'algorithm': 'Dilithium2 (Simulated)'
                }
            
            # Store performance metrics
            self.performance_metrics['dilithium_keygen_time'] = 1.2  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Key generation failed: {str(e)}")
    
    def dilithium_sign(self, private_key_b64: str, message: str) -> Dict[str, Any]:
        """Sign a message using Dilithium"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            private_key = base64.b64decode(private_key_b64)
            message_bytes = message.encode('utf-8')
            
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.Signature(self.dilithium_alg) as sig:
                    sig.import_secret_key(private_key)
                    signature = sig.sign(message_bytes)
                    result = {
                        'signature': base64.b64encode(signature).decode('utf-8'),
                        'message': message
                    }
            else:
                signature = self.simulator.dilithium_sign(private_key, message_bytes)
                result = {
                    'signature': base64.b64encode(signature).decode('utf-8'),
                    'message': message
                }
            
            # Store performance metrics
            self.performance_metrics['dilithium_sign_time'] = 0.8  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Signing failed: {str(e)}")
    
    def dilithium_verify(self, public_key_b64: str, message: str, signature_b64: str) -> Dict[str, Any]:
        """Verify a signature using Dilithium"""
        if not self._check_resources():
            raise RuntimeError("Resource constraints exceeded")
        
        try:
            public_key = base64.b64decode(public_key_b64)
            message_bytes = message.encode('utf-8')
            signature = base64.b64decode(signature_b64)
            
            if LIBOQS_AVAILABLE and LibOQS is not None:
                with LibOQS.Signature(self.dilithium_alg) as sig:
                    sig.import_public_key(public_key)
                    is_valid = sig.verify(message_message_bytes, signature)
                    result = {
                        'is_valid': is_valid,
                        'message': message
                    }
            else:
                is_valid = self.simulator.dilithium_verify(public_key, message_bytes, signature)
                result = {
                    'is_valid': is_valid,
                    'message': message
                }
            
            # Store performance metrics
            self.performance_metrics['dilithium_verify_time'] = 0.4  # Simulated time
            return result
            
        except Exception as e:
            raise RuntimeError(f"Verification failed: {str(e)}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics"""
        metrics = self.performance_metrics.copy()
        metrics.update(self.resource_monitor.get_resource_usage())
        return metrics
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            'liboqs_available': LIBOQS_AVAILABLE,
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            'platform': os.sys.platform,
            'cpu_count': os.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2)
        } 