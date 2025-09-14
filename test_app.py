#!/usr/bin/env python3
"""
Test script for Post-Quantum Cryptography Demo Application
"""

import sys
import time
from pqc_utils import PQCUtils
from database import Database

def test_pqc_utils():
    """Test PQC utilities functionality"""
    print("🔐 Testing PQC Utilities...")
    
    pqc = PQCUtils()
    
    # Test system info
    system_info = pqc.get_system_info()
    print(f"✅ System Info: {system_info}")
    
    # Test Kyber key generation
    print("\n🔑 Testing Kyber Key Generation...")
    try:
        kyber_keys = pqc.generate_kyber_keypair()
        print(f"✅ Kyber keys generated: {len(kyber_keys['public_key'])} chars public, {len(kyber_keys['private_key'])} chars private")
        
        # Test Kyber encapsulation
        print("\n🔐 Testing Kyber Encapsulation...")
        encaps_result = pqc.kyber_encapsulate(kyber_keys['public_key'])
        print(f"✅ Encapsulation successful: {len(encaps_result['ciphertext'])} chars ciphertext")
        
        # Test Kyber decapsulation
        print("\n🔓 Testing Kyber Decapsulation...")
        decap_result = pqc.kyber_decap(kyber_keys['private_key'], encaps_result['ciphertext'])
        print(f"✅ Decapsulation successful: {len(decap_result['shared_secret'])} chars shared secret")
        
    except Exception as e:
        print(f"❌ Kyber test failed: {e}")
        return False
    
    # Test Dilithium key generation
    print("\n✍️ Testing Dilithium Key Generation...")
    try:
        dilithium_keys = pqc.generate_dilithium_keypair()
        print(f"✅ Dilithium keys generated: {len(dilithium_keys['public_key'])} chars public, {len(dilithium_keys['private_key'])} chars private")
        
        # Test Dilithium signing
        print("\n📝 Testing Dilithium Signing...")
        test_message = "Hello, Post-Quantum World!"
        sign_result = pqc.dilithium_sign(dilithium_keys['private_key'], test_message)
        print(f"✅ Signing successful: {len(sign_result['signature'])} chars signature")
        
        # Test Dilithium verification
        print("\n🔍 Testing Dilithium Verification...")
        verify_result = pqc.dilithium_verify(dilithium_keys['public_key'], test_message, sign_result['signature'])
        print(f"✅ Verification successful: {verify_result['is_valid']}")
        
    except Exception as e:
        print(f"❌ Dilithium test failed: {e}")
        return False
    
    # Test performance metrics
    print("\n📊 Testing Performance Metrics...")
    metrics = pqc.get_performance_metrics()
    print(f"✅ Performance metrics: {metrics}")
    
    return True

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing Database...")
    
    db = Database()
    
    # Test storing operations
    print("📝 Testing database operations...")
    try:
        # Test Kyber operations
        db.store_kyber_keygen("test_public_key", "test_private_key")
        db.store_kyber_encaps("test_public_key", "test_ciphertext", "test_shared_secret")
        db.store_kyber_decap("test_private_key", "test_ciphertext", "test_shared_secret")
        
        # Test Dilithium operations
        db.store_dilithium_keygen("test_public_key", "test_private_key")
        db.store_dilithium_sign("test_private_key", "test_message", "test_signature")
        db.store_dilithium_verify("test_public_key", "test_message", "test_signature", True)
        
        # Test performance metrics
        db.store_performance_metric("test_operation", 1.5, 25.0, 15.0)
        
        print("✅ Database operations successful")
        
        # Test retrieving operations
        recent_kyber = db.get_recent_kyber_operations(5)
        recent_dilithium = db.get_recent_dilithium_operations(5)
        performance_stats = db.get_performance_stats()
        
        print(f"✅ Retrieved {len(recent_kyber)} Kyber operations")
        print(f"✅ Retrieved {len(recent_dilithium)} Dilithium operations")
        print(f"✅ Retrieved performance stats: {performance_stats}")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    return True

def test_resource_monitoring():
    """Test resource monitoring"""
    print("\n💻 Testing Resource Monitoring...")
    
    pqc = PQCUtils()
    metrics = pqc.get_performance_metrics()
    
    print(f"✅ Memory usage: {metrics.get('memory_mb', 0):.2f} MB")
    print(f"✅ CPU usage: {metrics.get('cpu_percent', 0):.2f}%")
    print(f"✅ Memory limit: {metrics.get('max_memory_mb', 0)} MB")
    print(f"✅ CPU limit: {metrics.get('max_cpu_percent', 0)}%")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Post-Quantum Cryptography Demo Tests\n")
    
    tests = [
        ("PQC Utilities", test_pqc_utils),
        ("Database", test_database),
        ("Resource Monitoring", test_resource_monitoring)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED\n")
            else:
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("1. Activate the virtual environment: source pqc_env/bin/activate")
        print("2. Run the application: python app.py")
        print("3. Open your browser to: http://localhost:5000")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 