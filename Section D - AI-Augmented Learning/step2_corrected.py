from typing import Dict, Any, Optional
import unittest

DEFAULT_ORDERS_DATABASE: Dict[str, Dict[str, Any]] = {
    "QB-101": {
        "status": "Out for delivery",
        "prep_min": 15,
        "rider_min": 10,
        "cancellable": False
    },
    "QB-102": {
        "status": "Preparing in kitchen",
        "prep_min": 20,
        "rider_min": 15,
        "cancellable": True
    },
    "QB-103": {
        "status": "Order Placed",
        "prep_min": 5,
        "rider_min": 25,
        "cancellable": True
    },
    "QB-104": {
        "status": "Delivered",
        "prep_min": 0,
        "rider_min": 0,
        "cancellable": False
    }
}

class OrderTracker:
    """Production-grade order tracking service providing validated status lookups and order actions."""

    def __init__(self, database: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        self._db = database if database is not None else {k: v.copy() for k, v in DEFAULT_ORDERS_DATABASE.items()}

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Safely fetch order record by sanitized ID."""
        if not isinstance(order_id, str):
            return None
        sanitized_id = order_id.strip().upper()
        return self._db.get(sanitized_id)

    def track_order(self, order_id: Any, user_query: Optional[str] = "") -> Dict[str, Any]:
        """Tracks the status of an order and answers common support questions with comprehensive error handling."""
        if not order_id or not isinstance(order_id, str):
            return {
                "success": False,
                "error": "INVALID_ORDER_ID",
                "message": "Order ID must be a non-empty string."
            }

        sanitized_id = order_id.strip().upper()
        order = self.get_order(sanitized_id)
        if order is None:
            return {
                "success": False,
                "error": "ORDER_NOT_FOUND",
                "message": f"Order '{sanitized_id}' was not found in our records. Please verify the ID."
            }

        query_str = (user_query or "").strip().lower()
        eta_minutes = order["prep_min"] + order["rider_min"]
        current_status = order["status"]

        if "cancel" in query_str:
            if current_status == "Cancelled":
                return {
                    "success": True,
                    "order_id": sanitized_id,
                    "status": "Cancelled",
                    "action": "already_cancelled",
                    "message": f"Order {sanitized_id} is already cancelled."
                }
            if order["cancellable"]:
                order["status"] = "Cancelled"
                return {
                    "success": True,
                    "order_id": sanitized_id,
                    "status": "Cancelled",
                    "action": "cancellation_success",
                    "message": f"Order {sanitized_id} has been successfully cancelled."
                }
            return {
                "success": False,
                "order_id": sanitized_id,
                "status": current_status,
                "action": "cancellation_rejected",
                "message": f"Order {sanitized_id} cannot be cancelled because it is '{current_status}'."
            }

        if "where" in query_str or "status" in query_str or "eta" in query_str:
            return {
                "success": True,
                "order_id": sanitized_id,
                "status": current_status,
                "eta_minutes": eta_minutes,
                "message": f"Order {sanitized_id} is '{current_status}'. Estimated arrival in {eta_minutes} minutes."
            }

        return {
            "success": True,
            "order_id": sanitized_id,
            "status": current_status,
            "eta_minutes": eta_minutes,
            "message": f"Order {sanitized_id} status: {current_status}. Estimated delivery time: {eta_minutes} minutes."
        }

class TestOrderTracker(unittest.TestCase):
    """Unit tests validating the correctness and robustness of OrderTracker."""

    def setUp(self) -> None:
        self.tracker = OrderTracker()

    def test_valid_order_id(self) -> None:
        """Test Case A: Valid order ID returns correct status and ETA."""
        result = self.tracker.track_order("QB-101", "Where is my order?")
        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "QB-101")
        self.assertEqual(result["status"], "Out for delivery")
        self.assertEqual(result["eta_minutes"], 25)

    def test_invalid_and_missing_order_id(self) -> None:
        """Test Case B: Missing, non-existent, or malformed order IDs handled gracefully without raising exceptions."""
        result_missing = self.tracker.track_order("QB-999", "Where is my order?")
        self.assertFalse(result_missing["success"])
        self.assertEqual(result_missing["error"], "ORDER_NOT_FOUND")

        result_empty = self.tracker.track_order("", "Where is my order?")
        self.assertFalse(result_empty["success"])
        self.assertEqual(result_empty["error"], "INVALID_ORDER_ID")

        result_none = self.tracker.track_order(None, "Where is my order?")
        self.assertFalse(result_none["success"])
        self.assertEqual(result_none["error"], "INVALID_ORDER_ID")

    def test_cancellation_edge_cases(self) -> None:
        """Test Case C: Edge cases including non-cancellable order rejection and repeated cancellation."""
        non_cancellable_result = self.tracker.track_order("qb-101", "Can I cancel this order?")
        self.assertFalse(non_cancellable_result["success"])
        self.assertEqual(non_cancellable_result["action"], "cancellation_rejected")

        cancellable_result = self.tracker.track_order("qb-102", "Please cancel my order")
        self.assertTrue(cancellable_result["success"])
        self.assertEqual(cancellable_result["status"], "Cancelled")

        repeat_result = self.tracker.track_order("QB-102", "Can I cancel?")
        self.assertTrue(repeat_result["success"])
        self.assertEqual(repeat_result["action"], "already_cancelled")

if __name__ == "__main__":
    unittest.main()
