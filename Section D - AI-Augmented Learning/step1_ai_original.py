orders_db = {
    "QB-101": {"status": "Out for delivery", "prep_min": 15, "rider_min": 10, "cancellable": False},
    "QB-102": {"status": "Preparing in kitchen", "prep_min": 20, "rider_min": 15, "cancellable": True},
    "QB-103": {"status": "Order Placed", "prep_min": 5, "rider_min": 25, "cancellable": True}
}

def track_order(order_id, user_query=""):
    order = orders_db[order_id]
    eta = order["prep_min"] + order["rider_min"]
    
    if "where is my order" in user_query.lower():
        return "Order " + order_id + " is currently " + order["status"] + ". Estimated arrival in " + str(eta) + " minutes."
    elif "cancel" in user_query.lower():
        if order["cancellable"]:
            order["status"] = "Cancelled"
            return "Order " + order_id + " has been cancelled successfully."
        else:
            return "Order " + order_id + " cannot be cancelled as it is already out for delivery."
    else:
        return "Status: " + order["status"] + ", ETA: " + str(eta) + " minutes."

if __name__ == "__main__":
    print(track_order("QB-101", "Where is my order?"))
    print(track_order("QB-102", "Can I cancel?"))
    try:
        print(track_order("QB-999", "Where is my order?"))
    except KeyError as e:
        print("Demonstrating AI flaw: Unhandled KeyError on invalid ID ->", repr(e))

