
from classifier import classify_email
from extractors import extract_tonnage, extract_vc, extract_tc
from utils import save_output
import pandas as pd
import os

emails = []

email_folder = "emails"
all_results = []
for filename in os.listdir(email_folder):

    if filename.endswith(".txt"):

        with open(
            os.path.join(email_folder, filename),
            "r",
            encoding="utf-8"
        ) as f:

            emails.append(f.read())

for idx, email in enumerate(emails, start=1):

    category = classify_email(email)

    if category == "TONNAGE":
        data = extract_tonnage(email)

    elif category == "CARGO_VC":
        data = extract_vc(email)

    else:
        data = extract_tc(email)

    result = {
        "category": category,
        "extracted_data": data
    }
    flat_result = {"category": category}

    flat_result.update(data)

    all_results.append(flat_result)
    print(result)

    save_output(result, f"output/result_{idx}.json")
df = pd.DataFrame(all_results)

df.to_csv("shipping_data.csv", index=False)

print("CSV saved successfully")