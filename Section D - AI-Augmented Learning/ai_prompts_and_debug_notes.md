# AI-Augmented Learning: Order Tracking System Review & Refactoring

## 1. Exact AI Prompt Used

> **Prompt:**  
> *"Write a Python function `track_order(order_id)` that looks up order status from a dictionary, calculates estimated arrival time, and handles common customer support follow-ups like 'where is my order?' and 'can I cancel?'"*

---

## 2. Flaws Identified in AI-Generated Code (`step1_ai_original.py`)

| # | Flaw Identified | Line(s) | Severity | Real-World Impact |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **Unchecked Dictionary Access (`KeyError`)** | Line 8 (`orders_db[order_id]`) | **Critical** | When an invalid, mistyped, or non-existent order ID is provided (e.g., `"QB-999"`), the script crashes unconditionally with an unhandled `KeyError`. |
| **2** | **Mutable Global State Mutation** | Line 15 (`order["status"] = "Cancelled"`) | **High** | Mutates global dictionary directly without encapsulation or thread locks, leading to race conditions and test pollution. |
| **3** | **Missing Type Validation & Sanitization** | Line 7, 8 | **Medium** | Fails on non-string inputs (e.g., `None`, integer `101`) or whitespace variants (`" qb-101 "`), raising `AttributeError` on `.lower()` or failing lookup due to case sensitivity. |
| **4** | **Unstructured Return Types** | Lines 12, 17, 19, 21 | **Medium** | Returns unstructured concatenated strings instead of typed structured dictionaries or JSON objects required by modern frontend/API consumers. |
| **5** | **Lack of Edge-Case Handling on Cancellation** | Lines 14–19 | **Medium** | Does not check if an order was already marked `"Cancelled"` or `"Delivered"`, producing redundant status changes or misleading responses. |
| **6** | **Zero Unit Testing & Docstrings** | Lines 1–25 | **Low** | Absence of docstrings, type annotations, and automated unit test assertions for production verification. |

---

## 3. Comparison Table: Original vs. Corrected Implementation

| Aspect | Original AI Code (`step1_ai_original.py`) | Corrected Production Code (`step2_corrected.py`) |
| :--- | :--- | :--- |
| **Error Handling** | None; raises unhandled `KeyError` on missing ID | Returns structured response with `"error": "ORDER_NOT_FOUND"` or `"INVALID_ORDER_ID"` |
| **Input Sanitization** | Raw lookup without strip/case handling | Strips whitespace and standardizes casing via `.strip().upper()` |
| **Data Architecture** | Naked global variable `orders_db` | Encapsulated inside `OrderTracker` class with instance copy isolation |
| **Response Format** | Raw concatenated string | Strongly-typed dictionary (`Dict[str, Any]`) with success flags, status, ETA, and messages |
| **Type Hints & Docs** | None | Full PEP 484 type annotations and comprehensive docstrings |
| **Test Verification** | Manual ad-hoc print calls | 3 automated unit test suites in `unittest.TestCase` (Valid ID, Missing/None ID, Edge cases) |

---

## 4. Key Fixes Applied

1. **Safe Dictionary Retrieval:** Utilized `self._db.get(sanitized_id)` inside an encapsulated class to guarantee safe lookups without `KeyError`.
2. **Defensive Input Validation:** Added checks for `None`, non-string types, and empty strings, gracefully returning descriptive errors.
3. **Structured API Contract:** Replaced arbitrary string responses with standardized JSON-like dictionary payloads containing `success`, `order_id`, `status`, `eta_minutes`, and `message`.
4. **Idempotent Cancellation Logic:** Verified current status before cancellation to prevent redundant operations on already cancelled or delivered orders.
5. **Automated Unit Testing:** Integrated a comprehensive `unittest.TestCase` suite testing valid lookups, missing IDs, invalid inputs, and cancellation state transitions.

---

## 5. Reflection on AI Code Quality

While Large Language Models excel at generating quick algorithmic prototypes and readable boilerplate, they frequently overlook defensive programming practices such as boundary condition checks, type sanitization, and state encapsulation. Relying on raw AI output in production services poses severe availability risks—such as unhandled server crashes on malformed customer inputs. Human-in-the-loop engineering, rigorous code reviews, and comprehensive automated test suites remain indispensable to harden AI-generated code for mission-critical enterprise systems.
