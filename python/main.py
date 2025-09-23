# Main.py module
import json
import sys

from modules.compute import Compute
from modules.validation_action import validate_action

def read_json(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        return data

def main():
    inputPath = sys.argv[1] if len(sys.argv) > 1 else 'input.json'
    input = read_json(inputPath)
    print("Input data:", input)
    validate_action(input)
    print("Validation input", input)
    comput = Compute(input).calculate()
    print(json.dumps(comput, ensure_ascii=False, indent=2))
    
if __name__ == "__main__":
    main()