#!/usr/bin/env python3
"""
Demo script for Post-Quantum Cryptography
Shows practical examples of Kyber and Dilithium operations
"""

import time
from pqc_utils import PQCUtils
from database import Database

def demo_kyber_operations():
    """Demonstrate Kyber key encapsulation mechanism"""
    print("🔑 CRYSTALS-Kyber Demo")
    print("=" * 50)
    
    pqc = PQCUtils()
    db = Database()
    
    # Step 1: Generate keypair
    print("1. Generating Kyber keypair...")
    start_time = time.time()
    keys = pqc.generate_kyber_keypair()
    keygen_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Public key: {len(keys['public_key'])} characters")
    print(f"   ✅ Private key: {len(keys['private_key'])} characters")
    print(f"   ⏱️  Generation time: {keygen_time:.2f} ms")
    
    # Store in database
    db.store_kyber_keygen(keys['public_key'], keys['private_key'])
    
    # Step 2: Encapsulate shared secret
    print("\n2. Encapsulating shared secret...")
    start_time = time.time()
    encaps_result = pqc.kyber_encapsulate(keys['public_key'])
    encaps_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Ciphertext: {len(encaps_result['ciphertext'])} characters")
    print(f"   ✅ Shared secret: {len(encaps_result['shared_secret'])} characters")
    print(f"   ⏱️  Encapsulation time: {encaps_time:.2f} ms")
    
    # Store in database
    db.store_kyber_encaps(keys['public_key'], encaps_result['ciphertext'], encaps_result['shared_secret'])
    
    # Step 3: Decapsulate shared secret
    print("\n3. Decapsulating shared secret...")
    start_time = time.time()
    decap_result = pqc.kyber_decap(keys['private_key'], encaps_result['ciphertext'])
    decap_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Recovered shared secret: {len(decap_result['shared_secret'])} characters")
    print(f"   ⏱️  Decapsulation time: {decap_time:.2f} ms")
    
    # Store in database
    db.store_kyber_decap(keys['private_key'], encaps_result['ciphertext'], decap_result['shared_secret'])
    
    # Verify shared secrets match
    if encaps_result['shared_secret'] == decap_result['shared_secret']:
        print("   ✅ Shared secrets match! Key exchange successful.")
    else:
        print("   ❌ Shared secrets do not match!")
    
    return {
        'keygen_time': keygen_time,
        'encaps_time': encaps_time,
        'decap_time': decap_time
    }

def demo_dilithium_operations():
    """Demonstrate Dilithium digital signatures"""
    print("\n✍️ CRYSTALS-Dilithium Demo")
    print("=" * 50)
    
    pqc = PQCUtils()
    db = Database()
    
    # Step 1: Generate keypair
    print("1. Generating Dilithium keypair...")
    start_time = time.time()
    keys = pqc.generate_dilithium_keypair()
    keygen_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Public key: {len(keys['public_key'])} characters")
    print(f"   ✅ Private key: {len(keys['private_key'])} characters")
    print(f"   ⏱️  Generation time: {keygen_time:.2f} ms")
    
    # Store in database
    db.store_dilithium_keygen(keys['public_key'], keys['private_key'])
    
    # Step 2: Sign a message
    message = "Hello, Post-Quantum World! This message is signed with Dilithium."
    print(f"\n2. Signing message: '{message}'")
    start_time = time.time()
    sign_result = pqc.dilithium_sign(keys['private_key'], message)
    sign_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Signature: {len(sign_result['signature'])} characters")
    print(f"   ⏱️  Signing time: {sign_time:.2f} ms")
    
    # Store in database
    db.store_dilithium_sign(keys['private_key'], message, sign_result['signature'])
    
    # Step 3: Verify the signature
    print("\n3. Verifying signature...")
    start_time = time.time()
    verify_result = pqc.dilithium_verify(keys['public_key'], message, sign_result['signature'])
    verify_time = (time.time() - start_time) * 1000
    
    print(f"   ✅ Verification result: {verify_result['is_valid']}")
    print(f"   ⏱️  Verification time: {verify_time:.2f} ms")
    
    # Store in database
    db.store_dilithium_verify(keys['public_key'], message, sign_result['signature'], verify_result['is_valid'])
    
    # Test with modified message (should fail)
    print("\n4. Testing signature with modified message...")
    modified_message = "Hello, Post-Quantum World! This message is modified."
    verify_modified = pqc.dilithium_verify(keys['public_key'], modified_message, sign_result['signature'])
    print(f"   ✅ Verification with modified message: {verify_modified['is_valid']}")
    
    return {
        'keygen_time': keygen_time,
        'sign_time': sign_time,
        'verify_time': verify_time
    }

def demo_resource_monitoring():
    """Demonstrate resource monitoring"""
    print("\n💻 Resource Monitoring Demo")
    print("=" * 50)
    
    pqc = PQCUtils()
    
    # Get current resource usage
    metrics = pqc.get_performance_metrics()
    
    print(f"Memory Usage: {metrics['memory_mb']:.2f} MB / {metrics['max_memory_mb']} MB")
    print(f"CPU Usage: {metrics['cpu_percent']:.2f}% / {metrics['max_cpu_percent']}%")
    
    # Simulate resource-intensive operations
    print("\nSimulating resource-intensive operations...")
    for i in range(5):
        # Generate keys to increase memory usage
        pqc.generate_kyber_keypair()
        pqc.generate_dilithium_keypair()
        
        metrics = pqc.get_performance_metrics()
        print(f"After operation {i+1}: Memory={metrics['memory_mb']:.2f}MB, CPU={metrics['cpu_percent']:.2f}%")
    
    return metrics

def demo_database_operations():
    """Demonstrate database operations"""
    print("\n🗄️ Database Operations Demo")
    print("=" * 50)
    
    db = Database()
    
    # Get recent operations
    recent_kyber = db.get_recent_kyber_operations(10)
    recent_dilithium = db.get_recent_dilithium_operations(10)
    performance_stats = db.get_performance_stats()
    
    print(f"Recent Kyber operations: {len(recent_kyber)}")
    print(f"Recent Dilithium operations: {len(recent_dilithium)}")
    print(f"Performance statistics: {performance_stats}")
    
    # Show some example operations
    if recent_kyber:
        print(f"\nLatest Kyber operation: {recent_kyber[0]['operation_type']}")
    if recent_dilithium:
        print(f"Latest Dilithium operation: {recent_dilithium[0]['operation_type']}")

def main():
    """Run the complete demo"""
    print("🚀 Post-Quantum Cryptography Demo")
    print("=" * 60)
    print("This demo showcases CRYSTALS-Kyber and CRYSTALS-Dilithium")
    print("algorithms with resource monitoring and database storage.\n")
    
    try:
        # Run Kyber demo
        kyber_times = demo_kyber_operations()
        
        # Run Dilithium demo
        dilithium_times = demo_dilithium_operations()
        
        # Run resource monitoring demo
        resource_metrics = demo_resource_monitoring()
        
        # Run database demo
        demo_database_operations()
        
        # Summary
        print("\n📊 Performance Summary")
        print("=" * 50)
        print(f"Kyber Key Generation: {kyber_times['keygen_time']:.2f} ms")
        print(f"Kyber Encapsulation: {kyber_times['encaps_time']:.2f} ms")
        print(f"Kyber Decapsulation: {kyber_times['decap_time']:.2f} ms")
        print(f"Dilithium Key Generation: {dilithium_times['keygen_time']:.2f} ms")
        print(f"Dilithium Signing: {dilithium_times['sign_time']:.2f} ms")
        print(f"Dilithium Verification: {dilithium_times['verify_time']:.2f} ms")
        print(f"Final Memory Usage: {resource_metrics['memory_mb']:.2f} MB")
        print(f"Final CPU Usage: {resource_metrics['cpu_percent']:.2f}%")
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the web interface:")
        print("python app.py")
        print("Then open http://localhost:8080 in your browser")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 