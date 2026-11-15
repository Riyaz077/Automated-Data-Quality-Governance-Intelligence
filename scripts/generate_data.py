from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data import generate_business_data, generate_reference_data
base=Path(__file__).resolve().parents[1]/"data"
generate_business_data().to_csv(base/"business_data.csv",index=False)
generate_reference_data().to_csv(base/"reference_data.csv",index=False)
print("Generated synthetic current and reference datasets.")
