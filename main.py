import os, sys, csv
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
from datetime import *
from typing import List
from random import randint
from dataclasses import dataclass

AUTH_NET_LOGIN_ID = ""
AUTH_NET_TRANSACTION_KEY = ""


@dataclass
class SubscriptionExportDetails:
    subscription_id: str
    subscription_name: str
    first_name: str
    last_name: str
    pay_flow_pro_id: str
    subscription_status: str
    customer_profile_id: str
    customer_payment_profile_id: str


def get_merchant_auth():
    """get merchant authentication"""
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = AUTH_NET_LOGIN_ID
    merchantAuth.transactionKey = AUTH_NET_TRANSACTION_KEY
    return merchantAuth


def get_list_of_subscriptions() -> List[SubscriptionExportDetails]:
    """get list of subscriptions"""
    results: List[SubscriptionExportDetails] = []

    merchantAuth = get_merchant_auth()

    # set sorting parameters
    sorting = apicontractsv1.ARBGetSubscriptionListSorting()
    sorting.orderBy = apicontractsv1.ARBGetSubscriptionListOrderFieldEnum.id
    sorting.orderDescending = True

    # set paging and offset parameters
    paging = apicontractsv1.Paging()
    # Paging limit can be up to 1000 for this request
    paging.limit = 20
    paging.offset = 1

    request = apicontractsv1.ARBGetSubscriptionListRequest()
    request.merchantAuthentication = merchantAuth
    request.refId = f"dts-{randint(1000, 9999)}"
    request.searchType = (
        apicontractsv1.ARBGetSubscriptionListSearchTypeEnum.subscriptionActive
    )
    request.sorting = sorting
    request.paging = paging

    controller = ARBGetSubscriptionListController(request)
    controller.setenvironment("https://api.authorize.net/xml/v1/request.api")
    controller.execute()

    # Work on the response
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            if hasattr(response, "subscriptionDetails"):
                print("Successfully retrieved subscription list.")
                if response.messages is not None:
                    print(
                        "Message Code: %s" % response.messages.message[0]["code"].text
                    )
                    print(
                        "Message Text: %s" % response.messages.message[0]["text"].text
                    )
                    print("Total Number In Results: %s" % response.totalNumInResultSet)
                    print()
                for subscription in response.subscriptionDetails.subscriptionDetail:
                    # if subscription.invoice is None:
                    #     print(
                    #         f"Skipping subscription {subscription.id} as it has no invoice number"
                    #     )
                    #     continue
                    subscription_export = SubscriptionExportDetails(
                        subscription_id=str(subscription.id),
                        subscription_name=str(subscription.name),
                        first_name=str(subscription.firstName),
                        last_name=str(subscription.lastName),
                        pay_flow_pro_id=str(subscription.invoice),
                        subscription_status=str(subscription.status),
                        customer_profile_id=str(subscription.customerProfileId),
                        customer_payment_profile_id=str(
                            subscription.customerPaymentProfileId
                        ),
                    )
                    results.append(subscription_export)
                    print(f"Found: {subscription_export}" % subscription.id)
                    print()
            else:
                if response.messages is not None:
                    print("Failed to get subscription list.")
                    print("Code: %s" % (response.messages.message[0]["code"].text))
                    print("Text: %s" % (response.messages.message[0]["text"].text))
        else:
            if response.messages is not None:
                print("Failed to get transaction list.")
                print("Code: %s" % (response.messages.message[0]["code"].text))
                print("Text: %s" % (response.messages.message[0]["text"].text))
    else:
        print("Error. No response received.")

    return results


if __name__ == "__main__":
    export_file_name = (
        f"exports/subscriptions-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    )
    # export CSV of subscription exports
    csv_headers = [
        "SubscriptionId",
        "SubscriptionName",
        "FirstName",
        "LastName",
        "PayFlowProId",
        "SubscriptionStatus",
        "CustomerProfileId",
        "CustomerPaymentProfileId",
        "GatewayPersonIdentifier"
    ]

    subscriptions = get_list_of_subscriptions()
    print(f"Exporting {len(subscriptions)} subscriptions to {export_file_name}")

    with open(export_file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        for subscription in subscriptions:
            writer.writerow(
                [
                    subscription.subscription_id,
                    subscription.subscription_name,
                    subscription.first_name,
                    subscription.last_name,
                    subscription.pay_flow_pro_id,
                    subscription.subscription_status,
                    subscription.customer_profile_id,
                    subscription.customer_payment_profile_id,
                    f"{subscription.customer_profile_id}|{subscription.customer_payment_profile_id}"
                ]
            )

    print(f"Exported subscriptions to {export_file_name}")
