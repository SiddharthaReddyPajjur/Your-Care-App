#!/usr/bin/env python3
"""
Convert pickle model files to TensorFlow.js format for browser usage

This script converts:
1. neural_network_model.pkl -> TensorFlow.js model
2. encoder.pkl -> JSON labels file

Requirements:
pip install tensorflow tensorflowjs pickle sklearn numpy
"""

import pickle
import json
import numpy as np
import tensorflow as tf
import tensorflowjs as tfjs
import os

def convert_neural_network_model():
    """Convert the pickle neural network model to TensorFlow.js format"""
    
    print("🔄 Loading neural network model...")
    
    try:
        # Load the pickle model
        with open('src/neural_network_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        print(f"✅ Model loaded successfully")
        print(f"   Model type: {type(model)}")
        
        # Check if it's already a TensorFlow/Keras model
        if hasattr(model, 'save'):
            print("🔄 Converting TensorFlow/Keras model to TensorFlow.js...")
            
            # Create output directory
            os.makedirs('public/models', exist_ok=True)
            
            # Save as TensorFlow.js format
            tfjs.converters.save_keras_model(model, 'public/models')
            print("✅ Model converted successfully to public/models/")
            
        else:
            print("❌ Model is not a TensorFlow/Keras model")
            print("   You may need to recreate the model in TensorFlow/Keras format")
            return False
            
    except Exception as e:
        print(f"❌ Error converting model: {e}")
        return False
    
    return True

def convert_encoder():
    """Convert the label encoder to JSON format"""
    
    print("🔄 Loading label encoder...")
    
    try:
        # Load the pickle encoder
        with open('src/encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
        
        print(f"✅ Encoder loaded successfully")
        print(f"   Encoder type: {type(encoder)}")
        
        # Extract class labels
        if hasattr(encoder, 'classes_'):
            disease_labels = encoder.classes_.tolist()
        elif hasattr(encoder, 'inverse_transform'):
            # Try to get all possible labels
            try:
                # Assuming encoder can handle range of integers
                max_label = 100  # Adjust based on your data
                disease_labels = [encoder.inverse_transform([i])[0] for i in range(max_label)]
            except:
                print("❌ Could not extract labels from encoder")
                return False
        else:
            print("❌ Encoder format not recognized")
            return False
        
        # Create output directory
        os.makedirs('public/models', exist_ok=True)
        
        # Save as JSON
        with open('public/models/disease_labels.json', 'w') as f:
            json.dump(disease_labels, f, indent=2)
        
        print(f"✅ Encoder converted successfully")
        print(f"   Number of diseases: {len(disease_labels)}")
        print(f"   Sample diseases: {disease_labels[:5]}")
        
    except Exception as e:
        print(f"❌ Error converting encoder: {e}")
        return False
    
    return True

def create_test_model():
    """Create a test TensorFlow model if conversion fails"""
    
    print("🔄 Creating test model for demonstration...")
    
    # Create a simple neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(377,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')  # Assuming 10 diseases
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Create output directory
    os.makedirs('public/models', exist_ok=True)
    
    # Convert to TensorFlow.js
    tfjs.converters.save_keras_model(model, 'public/models')
    
    # Create sample disease labels
    sample_diseases = [
        'Common Cold', 'Flu', 'Headache', 'Fever', 'Cough',
        'Allergies', 'Fatigue', 'Nausea', 'Dizziness', 'Anxiety'
    ]
    
    with open('public/models/disease_labels.json', 'w') as f:
        json.dump(sample_diseases, f, indent=2)
    
    print("✅ Test model created successfully")
    print("   Note: This is a dummy model for testing purposes")

def main():
    print("🚀 Starting model conversion...")
    print("=" * 50)
    
    # Check if source files exist
    if not os.path.exists('src/neural_network_model.pkl'):
        print("❌ neural_network_model.pkl not found in src/ directory")
        create_test_model()
        return
    
    if not os.path.exists('src/encoder.pkl'):
        print("❌ encoder.pkl not found in src/ directory")
        create_test_model()
        return
    
    # Convert model
    model_success = convert_neural_network_model()
    
    # Convert encoder
    encoder_success = convert_encoder()
    
    if model_success and encoder_success:
        print("\n" + "=" * 50)
        print("✅ Conversion completed successfully!")
        print("\n📋 Next steps:")
        print("1. The converted files are in public/models/")
        print("2. model.json - TensorFlow.js model")
        print("3. disease_labels.json - Disease names")
        print("4. Install TensorFlow.js: npm install @tensorflow/tfjs")
        print("5. Use the DirectPredictionService in your React app")
    else:
        print("\n" + "=" * 50)
        print("❌ Conversion failed!")
        print("Creating test model for demonstration...")
        create_test_model()

if __name__ == "__main__":
    main()
