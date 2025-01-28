# Authorize.Net ARB CSV Exporter

This project is a tool for exporting subscription details from Authorize.Net's ARB (Automated Recurring Billing) system to a CSV file. It uses the Authorize.Net SDK and is configured to work with `pipenv` for managing dependencies.

## Prerequisites

Before using this tool, ensure you have the following installed:

1. **Python** (>= 3.11.6)
2. **pipenv**

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
$ git clone <repository_url>
$ cd authorize-net-arb-csv-exporter
```

### 2. Install Dependencies
Install the required Python dependencies using `pipenv`:
```bash
$ pipenv install
```

### 3. Configure Authentication

Set your Authorize.Net API credentials in the script:

1. Open `main.py`.
2. Update the `AUTH_NET_LOGIN_ID` and `AUTH_NET_TRANSACTION_KEY` variables with your API credentials:
   ```python
   AUTH_NET_LOGIN_ID = "your_login_id"
   AUTH_NET_TRANSACTION_KEY = "your_transaction_key"
   ```

**Note:** Ensure you use the correct credentials for the environment (sandbox or production).

### 4. Create the Exports Directory
Ensure the `exports` directory exists for saving CSV files:
```bash
$ mkdir exports
```

## Usage

Run the script using `pipenv` to activate the virtual environment:
```bash
$ pipenv run python main.py
```

The script will:
- Retrieve a list of active subscriptions from Authorize.Net.
- Export the subscription details to a CSV file in the `exports` directory.

### Example Output

Upon running the script, you will see output like this:
```plaintext
Successfully retrieved subscription list.
Message Code: I00001
Message Text: Successful.
Total Number In Results: 2

Found: SubscriptionExportDetails(subscription_id='67541691', subscription_name='Rock Subscription', first_name='John', last_name='Doe', pay_flow_pro_id='', subscription_status='active', customer_profile_id='715469660', customer_payment_profile_id='721651257')

Found: SubscriptionExportDetails(subscription_id='67519058', subscription_name='Rock Subscription', first_name='Jane', last_name='Doe', pay_flow_pro_id='', subscription_status='active', customer_profile_id='715469661', customer_payment_profile_id='721651258')

Exporting 2 subscriptions to exports/subscriptions-2025-01-28-09-55-12.csv
Exported subscriptions to exports/subscriptions-2025-01-28-09-55-12.csv
```

The resulting CSV file will look like this:

| SubscriptionId | SubscriptionName | FirstName | LastName | PayFlowProId | SubscriptionStatus | CustomerProfileId | CustomerPaymentProfileId | GatewayPersonIdentifier             |
|----------------|------------------|-----------|----------|--------------|--------------------|-------------------|--------------------------|--------------------------------------|
| 67541691       | Rock Subscription| John      | Doe      |              | active             | 715469660         | 721651257                | 715469660|721651257                          |
| 67519058       | Rock Subscription| Jane      | Doe      |              | active             | 715469661         | 721651258                | 715469661|721651258                          |

## Dependencies

This script uses the following dependencies:

- `authorizenet` - Authorize.Net Python SDK
- `pipenv` - Python dependency manager

Install these dependencies with `pipenv install`.

## Notes

- The `PayFlowProId` field may be empty if it is not available for the subscription.
- Ensure you have proper API permissions and the necessary credentials for Authorize.Net.
- This script retrieves only **active subscriptions**. Update the `request.searchType` field in `get_list_of_subscriptions` to retrieve other subscription types.
