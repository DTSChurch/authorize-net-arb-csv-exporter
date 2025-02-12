import requests
import csv

PAYFLOW_API_URL = "https://payflowpro.paypal.com"

# API credentials
PAYFLOW_CREDENTIALS = {
    "PARTNER": "PremierPayment",
    "VENDOR": "LegacyChristian",
    "USER": "DTSAPI",
    "PWD": "4ViCWRbNrMWb",
}


def cancel_recurring_billing(profile_id):
    """Cancels a Payflow Pro recurring billing profile."""
    payload = {
        "TRXTYPE": "R",  # Recurring Transaction
        "ACTION": "C",  # Reactivate, Cancel, Suspend, Modify
        "STATUS": "C",  # C = Cancel
        "ORIGPROFILEID": profile_id,  # Subscription ID
        "PARTNER": PAYFLOW_CREDENTIALS["PARTNER"],
        "VENDOR": PAYFLOW_CREDENTIALS["VENDOR"],
        "USER": PAYFLOW_CREDENTIALS["USER"],
        "PWD": PAYFLOW_CREDENTIALS["PWD"],
        "VERBOSITY": "HIGH",  # Get detailed response
    }

    response = requests.post(PAYFLOW_API_URL, data=payload)
    response_text = response.text

    # Parse response
    response_dict = dict(
        item.split("=") for item in response_text.split("&") if "=" in item
    )

    if response_dict.get("RESULT") == "0":
        print(f"Subscription {profile_id} successfully canceled.")
    else:
        print(
            f"Failed to cancel subscription {profile_id}: {response_dict.get('RESPMSG')}"
        )


with open("cancel.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        profile_id = row[0]
        cancel_recurring_billing(profile_id)
