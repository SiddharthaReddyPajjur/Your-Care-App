from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os
from typing import List, Dict

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables to store loaded models
model = None
encoder = None

def load_models():
    """Load the neural network model and encoder on startup"""
    global model, encoder
    
    try:
        # Load the neural network model
        model_path = os.path.join('src', 'neural_network_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Neural network model loaded successfully")
        
        # Load the label encoder
        encoder_path = os.path.join('src', 'encoder.pkl')
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)
        print("✅ Label encoder loaded successfully")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error: Model file not found - {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "encoder_loaded": encoder is not None
    })

@app.route('/predict', methods=['POST'])
def predict_disease():
    """
    Predict disease based on symptoms
    
    Expected input:
    {
        "symptoms": ["symptom_1", "symptom_5", "symptom_12", ...]
    }
    
    Returns:
    {
        "prediction": "Disease Name",
        "confidence": 0.95,
        "status": "success"
    }
    """
    try:
        # Check if models are loaded
        if model is None or encoder is None:
            return jsonify({
                "error": "Models not loaded. Please check server configuration.",
                "status": "error"
            }), 500
        
        # Get symptoms from request
        data = request.get_json()
        if not data or 'symptoms' not in data:
            return jsonify({
                "error": "Missing 'symptoms' in request body",
                "status": "error"
            }), 400
        
        selected_symptoms = data['symptoms']
        
        # Validate symptoms is a list
        if not isinstance(selected_symptoms, list):
            return jsonify({
                "error": "Symptoms must be provided as a list",
                "status": "error"
            }), 400
        
        # Create symptoms array (377 columns initialized to 0)
        symptoms_array = np.zeros((1, 377), dtype=int)
        
        # Update symptoms array based on selected symptoms
        for symptom_id in selected_symptoms:
            try:
                # Extract symptom index from symptom_id (e.g., "symptom_5" -> 5)
                if symptom_id.startswith('symptom_'):
                    symptom_index = int(symptom_id.split('_')[1])
                    # Convert to 0-based index (symptom_1 -> index 0)
                    array_index = symptom_index - 1
                    
                    if 0 <= array_index < 377:
                        symptoms_array[0, array_index] = 1
                    else:
                        print(f"Warning: Symptom index {array_index} out of range")
                        
            except (ValueError, IndexError) as e:
                print(f"Warning: Invalid symptom ID format: {symptom_id} - {e}")
                continue
        
        # Make prediction using the neural network
        predictions = model.predict(symptoms_array)
        
        # Get the predicted class (argmax)
        predicted_class = np.argmax(predictions, axis=1)[0]
        
        # Get the confidence score
        confidence = float(np.max(predictions))
        
        # Decode the prediction to get disease name
        try:
            disease_name = encoder.inverse_transform([predicted_class])[0]
        except Exception as e:
            return jsonify({
                "error": f"Error decoding prediction: {str(e)}",
                "status": "error"
            }), 500
        
        # Return prediction result
        return jsonify({
            "prediction": disease_name,
            "confidence": confidence,
            "selected_symptoms_count": len(selected_symptoms),
            "symptoms_processed": np.sum(symptoms_array),
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

@app.route('/symptoms-info', methods=['GET'])
def get_symptoms_info():
    """Get information about the symptoms expected by the model"""
    return jsonify({
        "total_symptoms": 377,
        "symptom_format": "symptom_1 to symptom_377",
        "input_format": "Array of 377 integers (0 or 1)",
        "description": "Each position corresponds to a specific symptom in order"
    })

if __name__ == '__main__':
    print("🚀 Starting Disease Prediction Backend...")
    
    # Load models on startup
    if load_models():
        print("✅ All models loaded successfully")
        print("🔗 Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to load models. Please check model files.")
        print("📋 Expected files:")
        print("   - src/neural_network_model.pkl")
        print("   - src/encoder.pkl")
