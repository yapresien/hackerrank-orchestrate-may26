import pandas as pd
from agent import process_ticket
from config import TICKETS_PATH, OUTPUT_PATH

def main():
    
    df = pd.read_csv(TICKETS_PATH)

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

    out_df = pd.DataFrame(outputs)
    out_df.to_csv(OUTPUT_PATH, index=False)

    out_df.to_csv("support_tickets/test_output.csv", index=False)

    print("✅ Saved to support_tickets/test_output.csv")

if __name__ == "__main__":
    main()