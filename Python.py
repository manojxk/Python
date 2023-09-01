import os
import re
import pandas as pd

def append_to_excel(microservice, tag, rlm_ids):
    # Check if the Excel file exists
    file_exists = os.path.isfile("output_data.xlsx")

    # Extract the PROD1 and JPPROD2 IDs using regular expressions
    pattern = r"(\w+)\s*-\s*https://releaseorchestrationdeployment\.citigroup\.net/brpm/requests/(\d+)"
    matches = re.findall(pattern, rlm_ids, re.IGNORECASE)

    # Create a DataFrame with the extracted data
    df = pd.DataFrame(matches, columns=["Name", "ID"])
    
    # Add the microservice and tag values
    df["Microservice"] = microservice
    df["Tag"] = tag

    if not file_exists:
        # If the file doesn't exist, create it with column names
        df.to_excel("output_data.xlsx", index=False)
        print("Excel file 'output_data.xlsx' created with column names.")
    else:
        # If the file exists, load existing data
        existing_df = pd.read_excel("output_data.xlsx")
        
        # Check if the existing DataFrame is empty
        if existing_df.empty:
            # If empty, simply save the current DataFrame
            df.to_excel("output_data.xlsx", index=False)
            print("Data appended to 'output_data.xlsx' in a new row.")
        else:
            # If not empty, concatenate the current DataFrame horizontally
            updated_df = pd.concat([existing_df, df], axis=1)
            updated_df.to_excel("output_data.xlsx", index=False)
            print("Data appended to 'output_data.xlsx' in a new row.")

# Example usage:
microservice = "169068-auth-d-partyauth-apct-dgl-ea"
tag = "jenkins-169068.api.v2.auth.d.partyauth.apct.dgl.ea.gc.iut.int-29"
rlm_ids = "PROD1 - https://releaseorchestrationdeployment.citigroup.net/brpm/requests/7430862, JPPROD2 - https://releaseorchestrationdeployment.citigroup.net/brpm/requests/7430865"
append_to_excel(microservice, tag, rlm_ids)

# You can call append_to_excel function with different values for microservice, tag, and rlm_ids to append data to the Excel file in a single row.
