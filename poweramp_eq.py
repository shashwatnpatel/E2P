import json
import argparse
import glob
from pathlib import Path

def convert_eq_to_poweramp(file_inputs=None):
    # Mapping: 0-Low, 1-High, 2-Band, 3-Peaking, 4-Low Shelf, 5-High Shelf
    type_map = {
        'LP': 0, 'LOW': 0, 'HP': 1, 'HIGH': 1, 
        'BP': 2, 'BAND': 2, 'PK': 3, 'PEAKING': 3, 
        'LS': 4, 'LOWSHELF': 4, 'HS': 5, 'HIGHSHELF': 5
    }

    # Assigning individual colors (Poweramp uses ARGB decimal values)
    color_map = {
        0: -256,        # Yellow (Low Pass)
        1: -65281,      # Purple (High Pass)
        2: -16711681,   # Cyan (Band Pass)
        3: -16711936,   # Green (Peaking)
        4: -65536,      # Red (Low Shelf)
        5: -16776961    # Blue (High Shelf)
    }

    # FIX 2: Resolve files & handle Windows wildcard expansion (e.g., *.txt)
    target_files = []
    if file_inputs:
        for item in file_inputs:
            # If item contains a wildcard, expand it; otherwise treat as normal file
            matched = glob.glob(item) if any(char in item for char in '*?') else [item]
            target_files.extend([Path(f) for f in matched])
    else:
        # Default behavior: grab all .txt files in current directory
        target_files = list(Path('.').glob('*.txt'))
    
    # Filter out directories accidentally caught or typed
    target_files = [f for f in target_files if f.is_file()]

    if not target_files:
        print("No files specified or found for conversion.")
        return

    for file_path in target_files:
        # FIX 1: Modern path handling with pathlib
        output_path = file_path.with_name(f"{file_path.stem}_Poweramp.json")
        
        # Mandatory Tone Control entries (Index 0 and 1)
        bands = [
            {"type": 0, "channels": 0, "frequency": 90, "q": 0.0, "gain": 0.0, "color": 0},
            {"type": 1, "channels": 0, "frequency": 10000, "q": 0.0, "gain": 0.0, "color": 0}
        ]
        preamp = 0.0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or "[" in line: 
                        continue

                    if "Preamp:" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            preamp = float(parts[1].replace("dB", "").strip())
                    
                    # Original strict index-based parsing preserved (No Fix 3)
                    elif "Filter" in line:
                        parts = line.split()
                        f_type_str = parts[3].upper()
                        f_type_id = type_map.get(f_type_str, 3) 
                        
                        try:
                            # ROUND FREQUENCY TO INT: Fixed bug where floats break UI
                            freq = int(round(float(parts[5])))
                            gain = float(parts[8])
                            
                            q_val = 1.0
                            if "Q" in parts:
                                q_idx = parts.index("Q")
                                if q_idx + 1 < len(parts):
                                    q_val = float(parts[q_idx + 1])

                            bands.append({
                                "type": f_type_id,
                                "channels": 0,
                                "frequency": freq, # Integer frequency
                                "q": q_val,
                                "gain": gain,
                                "color": color_map.get(f_type_id, 0) # Individual color assignment
                            })
                        except (ValueError, IndexError):
                            continue

            output_data = [{
                "name": file_path.stem,
                "preamp": preamp,
                "parametric": True,
                "bands": bands
            }]

            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(output_data, out_f, indent=4)
            
            print(f"Created: {output_path.name}")
            
        except Exception as e:
            print(f"Error processing '{file_path.name}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert standard EQ text files to Poweramp JSON format.")
    parser.add_argument(
        'files', 
        nargs='*', 
        help="Optional: Specific .txt file(s) or patterns (e.g., *.txt) to convert. If omitted, all .txt files in the current folder will be processed."
    )
    
    args = parser.parse_args()
    convert_eq_to_poweramp(args.files)