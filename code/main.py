import pandas as pd
from agent import process_ticket
from config import TICKETS_PATH, OUTPUT_PATH
from validator import print_validation_report

def main():
    
    df = pd.read_csv(TICKETS_PATH)#.head(1)  # Limit to first 100 tickets for testing

    outputs = []

    for _, row in df.iterrows():
        result = process_ticket(row["Issue"])

        outputs.append({
            "status": result["status"],
            "product_area": result["product_area"],
            "response": result["response"],
            "justification": result["justification"],
            "request_type": result["request_type"]
        })

    # =======================================
    # Validate before writing to CSV
    # =======================================
    is_valid = print_validation_report(outputs, title="🔍 Output Validation Report")

    out_df = pd.DataFrame(outputs)
    out_df.to_csv(OUTPUT_PATH, index=False)

    if is_valid:
        print("✅ All validations passed. Saved to", OUTPUT_PATH)
    else:
        print("⚠️  Some validations failed. Review errors above. Saved to", OUTPUT_PATH)

if __name__ == "__main__":
    main()