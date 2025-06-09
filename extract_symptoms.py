#!/usr/bin/env python3
"""
Script to extract symptoms from symptom_columns.pkl file and generate TypeScript code
Place this script in the same directory as your "model attachments" folder
"""

import pickle
import os
import sys

def extract_symptoms():
    """Extract symptoms from pickle file and generate TypeScript code"""
    
    # Try to find the pickle file
    pickle_paths = [
        "model attachments/symptom_columns.pkl",
        "./symptom_columns.pkl",
        "../symptom_columns.pkl"
    ]
    
    symptoms_data = None
    for path in pickle_paths:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    symptoms_data = pickle.load(f)
                print(f"✅ Successfully loaded symptoms from: {path}")
                break
            except Exception as e:
                print(f"❌ Error loading {path}: {e}")
                continue
    
    if symptoms_data is None:
        print("❌ Could not find or load symptom_columns.pkl file")
        print("📁 Please ensure the file exists in one of these locations:")
        for path in pickle_paths:
            print(f"   - {path}")
        return None
    
    # Process symptoms data
    if isinstance(symptoms_data, list):
        symptoms = symptoms_data
    elif hasattr(symptoms_data, 'tolist'):  # numpy array
        symptoms = symptoms_data.tolist()
    elif hasattr(symptoms_data, 'columns'):  # pandas DataFrame
        symptoms = symptoms_data.columns.tolist()
    else:
        symptoms = list(symptoms_data)
    
    print(f"📊 Found {len(symptoms)} symptoms")
    
    # Generate TypeScript code
    ts_code = generate_typescript_code(symptoms)
    
    # Write to file
    output_file = "src/data/symptoms.ts"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ts_code)
        print(f"✅ Generated TypeScript file: {output_file}")
        print(f"🎯 Total symptoms: {len(symptoms)}")
        
        # Show sample symptoms
        print("\n📋 Sample symptoms:")
        for i, symptom in enumerate(symptoms[:10]):
            print(f"   {i+1}. {symptom}")
        if len(symptoms) > 10:
            print(f"   ... and {len(symptoms) - 10} more")
            
    except Exception as e:
        print(f"❌ Error writing TypeScript file: {e}")
        return None
    
    return symptoms

def clean_symptom_name(symptom):
    """Clean and format symptom name"""
    if not isinstance(symptom, str):
        symptom = str(symptom)
    
    # Remove underscores and convert to title case
    cleaned = symptom.replace('_', ' ').replace('-', ' ')
    
    # Handle special cases
    cleaned = cleaned.replace('  ', ' ').strip()
    
    # Convert to title case but preserve specific medical terms
    words = cleaned.split()
    title_words = []
    for word in words:
        if word.upper() in ['BMI', 'HIV', 'AIDS', 'COPD', 'UTI', 'BP']:
            title_words.append(word.upper())
        else:
            title_words.append(word.capitalize())
    
    return ' '.join(title_words)

def symptom_to_id(symptom):
    """Convert symptom name to a valid ID"""
    if not isinstance(symptom, str):
        symptom = str(symptom)
    
    # Convert to lowercase and replace spaces/special chars with underscores
    symptom_id = symptom.lower()
    symptom_id = ''.join(c if c.isalnum() else '_' for c in symptom_id)
    symptom_id = '_'.join(filter(None, symptom_id.split('_')))  # Remove empty parts
    
    return symptom_id

def generate_typescript_code(symptoms):
    """Generate TypeScript code for symptoms"""
    
    # Clean and process symptoms
    processed_symptoms = []
    seen_ids = set()
    
    for i, symptom in enumerate(symptoms):
        clean_name = clean_symptom_name(symptom)
        symptom_id = symptom_to_id(symptom)
        
        # Handle duplicate IDs
        original_id = symptom_id
        counter = 1
        while symptom_id in seen_ids:
            symptom_id = f"{original_id}_{counter}"
            counter += 1
        
        seen_ids.add(symptom_id)
        processed_symptoms.append({
            'id': symptom_id,
            'name': clean_name,
            'original': symptom
        })
    
    # Generate TypeScript code
    ts_code = '''// Symptom data extracted from symptom_columns.pkl
// Total symptoms: {total_count}
// Generated automatically - do not edit manually

export interface Symptom {{
  id: string;
  name: string;
}}

export const symptoms: Symptom[] = [
{symptom_entries}
];

// Utility functions
export const getSymptomById = (id: string): Symptom | undefined => {{
  return symptoms.find(symptom => symptom.id === id);
}};

export const searchSymptoms = (searchTerm: string): Symptom[] => {{
  if (!searchTerm.trim()) return symptoms;
  
  const term = searchTerm.toLowerCase();
  return symptoms.filter(symptom => 
    symptom.name.toLowerCase().includes(term) ||
    symptom.id.toLowerCase().includes(term)
  );
}};

export const getSymptomsPage = (page: number, pageSize: number = 50): Symptom[] => {{
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  return symptoms.slice(startIndex, endIndex);
}};

export const getTotalPages = (pageSize: number = 50): number => {{
  return Math.ceil(symptoms.length / pageSize);
}};

// Export total count for convenience
export const TOTAL_SYMPTOMS = {total_count};
'''.format(
        total_count=len(processed_symptoms),
        symptom_entries=',\n'.join([
            f'  {{ id: "{s["id"]}", name: "{s["name"]}" }}'
            for s in processed_symptoms
        ])
    )
    
    return ts_code

if __name__ == "__main__":
    print("🔄 Extracting symptoms from pickle file...")
    symptoms = extract_symptoms()
    
    if symptoms:
        print("✅ Extraction completed successfully!")
        print("\n📝 Next steps:")
        print("1. The symptoms.ts file has been updated")
        print("2. The symptom checker UI will now use these symptoms")
        print("3. You can test the updated symptom checker")
    else:
        print("❌ Extraction failed!")
        sys.exit(1)
