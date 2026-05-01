from dotenv import load_dotenv
load_dotenv()

import os
import random

SEED = 42
random.seed(SEED)

MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

DATA_PATH = "code/../data"
TICKETS_PATH = "code/../support_tickets/support_tickets.csv"
OUTPUT_PATH = "code/../support_tickets/output.csv"

TOP_K = 5
CONFIDENCE_THRESHOLD = 0.6