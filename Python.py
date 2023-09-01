import os
import re
import pandas as pd

# Create an empty DataFrame with the desired column names
output_df = pd.DataFrame(columns=["Microservice", "Tag", "PROD1", "JPPROD2"])

def append_to_excel(microservice, tag, rlm_ids):
    global output_df  # Access the global DataFrame

    # Extract the PROD1 and JPPROD2 IDs using regular expressions
    pattern = r"(\w+)\s*-\s*https://releaseorchestrationdeployment\.citigroup\.net/brpm/requests/(\d+)"
    matches = re.findall(pattern, rlm_ids, re.IGNORECASE)

    # Create a dictionary with the data to append
    new_row = {
        "Microservice": microservice,
        "Tag": tag,
        "PROD1": None,  # Initialize with None
        "JPPROD2": None  # Initialize with None
    }

    # Fill in the PROD1 and JPPROD2 values if they exist in the matches
    for name, id in matches:
        if name == "PROD1":
            new_row["PROD1"] = id
        elif name == "JPPROD2":
            new_row["JPPROD2"] = id

    # Append the new row to the DataFrame
    output_df = pd.concat([output_df, pd.DataFrame([new_row])], ignore_index=True)

    # Print the updated DataFrame
    print(output_df)

# Example usage:
microservice = "169068-auth-d-partyauth-apct-dgl-ea"
tag = "jenkins-169068.api.v2.auth.d.partyauth.apct.dgl.ea.gc.iut.int-29"
rlm_ids = "PROD1 - https://releaseorchestrationdeployment.citigroup.net/brpm/requests/7430862, JPPROD2 - https://releaseorchestrationdeployment.citigroup.net/brpm/requests/7430865"
append_to_excel(microservice, tag, rlm_ids)

# Save the DataFrame to an Excel file
output_df.to_excel("output_data.xlsx", index=False)
print("Data saved to 'output_data.xlsx'.")
