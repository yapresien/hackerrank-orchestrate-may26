import pandas as pd
from agent import process_ticket
from config import TICKETS_PATH, OUTPUT_PATH

def main():
    print(process_ticket("My Visa payment failed but I was charged"))
    return
    
    df = pd.read_csv(TICKETS_PATH)

    outputs = []

    for _, row in df.iterrows():
        result = process_ticket(row["ticket"])

        outputs.append({
            "status": result["status"],
            "product_area": result["product_area"],
            "response": result["response"],
            "justification": result["justification"],
            "request_type": result["request_type"]
        })

    out_df = pd.DataFrame(outputs)
    out_df.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    main()