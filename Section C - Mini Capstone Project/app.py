from pathlib import Path
import json
import streamlit as st
import numpy as np
import joblib
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

st.set_page_config(
    page_title="QuickBite AI - Food Ordering & Delivery Assistant",
    page_icon="🍔",
    layout="wide"
)

base_dir = Path(__file__).resolve().parent
model_file = base_dir / "delivery_model.joblib"
if not model_file.exists():
    model_file = Path("delivery_model.joblib")

loaded_model = joblib.load(model_file) if model_file.exists() else None

menu_file = base_dir / "menu.json"
if not menu_file.exists():
    menu_file = Path("menu.json")

with open(menu_file, "r", encoding="utf-8") as f:
    MENU_DATA = json.load(f)

@tool
def get_delivery_estimate(distance_km: float, num_items: int = 1, is_peak: bool = False) -> str:
    """Predicts estimated delivery time in minutes based on distance in kilometers, number of items, and peak/rain conditions."""
    if loaded_model is None:
        estimated = 15.0 + 2.5 * float(distance_km) + 1.5 * int(num_items)
        return f"Estimated delivery time: {estimated:.1f} minutes (heuristic mode)."
    rain_val = 1 if is_peak else 0
    feats = np.array([[float(distance_km), int(num_items), rain_val]])
    pred = float(loaded_model.predict(feats)[0])
    return f"Estimated delivery time: {pred:.1f} minutes based on QuickBite ML engine."

def search_menu(query: str, veg_preference: str = "All", limit: int = 4):
    q = query.lower().strip()
    results = []
    for item in MENU_DATA:
        if veg_preference == "Veg" and not item["is_veg"]:
            continue
        if veg_preference == "Non-Veg" and item["is_veg"]:
            continue
        score = 0
        if any(term in item["name"].lower() for term in q.split()):
            score += 3
        if any(term in item["cuisine"].lower() for term in q.split()):
            score += 2
        if any(term in item["category"].lower() for term in q.split()):
            score += 2
        if any(term in item["description"].lower() for term in q.split()):
            score += 1
        if score > 0 or not q:
            results.append((score, item))
    results.sort(key=lambda x: x[0], reverse=True)
    if not results and (not q or q in ["hi", "hello", "menu", "recommend"]):
        results = [(1, it) for it in MENU_DATA if (veg_preference == "All" or (veg_preference == "Veg" and it["is_veg"]) or (veg_preference == "Non-Veg" and not it["is_veg"]))]
    return [it for _, it in results[:limit]]

FEW_SHOT_PROMPT = """You are QuickBite AI, a friendly, courteous, and professional food ordering and delivery assistant for QuickBite.
You assist customers in browsing the menu, personalizing recommendations based on dietary preferences, capturing orders, calculating totals, and estimating delivery times using machine learning.

Here are examples of how you converse:

Example 1: Dietary Restrictions
User: Hi, I'm strictly vegetarian. What are your best dishes?
Assistant: Hello! Welcome to QuickBite. We have wonderful vegetarian options for you:
1. Paneer Butter Masala (Rs. 320) - Succulent cottage cheese cubes simmered in velvety tomato-cashew gravy.
2. Dal Makhani (Rs. 280) - Slow-cooked black lentils simmered overnight with butter and cream.
3. Margherita Gourmet Pizza (Rs. 390) - Hand-tossed crust with fresh mozzarella and basil.
4. Truffle Mushroom Risotto (Rs. 450) - Creamy arborio rice with porcini mushrooms and truffle oil.
Would you like to add any of these to your order?

Example 2: Delivery Time Estimation
User: I'm ordering from 4.5 km away. How long will 2 items take to arrive?
Assistant: Based on QuickBite's delivery prediction engine:
- Distance: 4.5 km
- Quantity: 2 items
The predicted delivery time is approximately 25.0 minutes. We'll have your hot meal dispatched as soon as the kitchen wraps preparation!

Now respond to the customer while adhering to their user profile and context."""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to QuickBite! I am your AI dining and delivery assistant. How can I delight your tastebuds today?"}
    ]

if "cart" not in st.session_state:
    st.session_state.cart = []

with st.sidebar:
    st.header("👤 Customer Profile")
    user_address = st.text_input("Delivery Address", value="Flat 402, Royal Palms, SG Highway, Ahmedabad")
    user_diet = st.selectbox("Dietary Preference", ["All", "Veg", "Non-Veg"], index=0)

    st.markdown("---")
    st.header("🛒 Active Order Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty. Ask the assistant to add dishes!")
    else:
        total_price = 0
        for idx, item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{item['name']}** x{item.get('qty', 1)}")
                st.caption(f"Rs. {item['price'] * item.get('qty', 1)}")
            with col_b:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            total_price += item["price"] * item.get("qty", 1)
        st.success(f"**Total Cart Value: Rs. {total_price}**")

    st.markdown("---")
    st.header("⚡ Quick ML Delivery Estimator")
    est_distance = st.slider("Distance from restaurant (km)", min_value=1.0, max_value=25.0, value=4.5, step=0.5)
    est_items = st.number_input("Number of Items", min_value=1, max_value=20, value=max(1, sum(item.get("qty", 1) for item in st.session_state.cart)))
    est_rain = st.checkbox("Heavy Rain / Peak Traffic")
    if st.button("Calculate Delivery Time", use_container_width=True):
        if loaded_model:
            sample_feats = np.array([[est_distance, est_items, 1 if est_rain else 0]])
            pred_time = loaded_model.predict(sample_feats)[0]
            st.metric(label="Predicted Delivery Time", value=f"{pred_time:.1f} min")
        else:
            st.warning("Model file not loaded.")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared. How may I assist you with your QuickBite order?"}
        ]
        st.rerun()

st.title("🍔 QuickBite AI Assistant")
st.markdown("Order your favorite meals, explore customized recommendations, and get real-time delivery estimates powered by Machine Learning.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask for food recommendations, place an order, or check delivery time...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    matched_items = search_menu(user_input, veg_preference=user_diet, limit=3)
    menu_context_str = ""
    if matched_items:
        menu_context_str = "Relevant QuickBite Menu Items:\n" + "\n".join(
            f"- {item['name']} ({item['cuisine']} - {'Veg' if item['is_veg'] else 'Non-Veg'}): Rs. {item['price']} | {item['description']}"
            for item in matched_items
        )

    cart_summary = f"Current Cart: {len(st.session_state.cart)} items"
    if st.session_state.cart:
        cart_summary += " (" + ", ".join(f"{it['name']} x{it.get('qty', 1)}" for it in st.session_state.cart) + ")"

    est_line = ""
    if any(k in user_input.lower() for k in ["time", "minute", "how long", "reach", "deliver", "estimate", "distance"]):
        dist = est_distance
        num_it = max(1, sum(it.get("qty", 1) for it in st.session_state.cart))
        est_result = get_delivery_estimate.invoke({"distance_km": dist, "num_items": num_it, "is_peak": est_rain})
        est_line = f"\nML Prediction Tool Result for {dist} km, {num_it} items: {est_result}\n"

    system_content = f"{FEW_SHOT_PROMPT}\n\nCustomer Profile:\n- Delivery Address: {user_address}\n- Dietary Preference: {user_diet}\n- {cart_summary}\n\n{menu_context_str}\n{est_line}\nPlease provide a helpful, polite, and well-structured response without emojis."

    llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.3)
    history_messages = [SystemMessage(content=system_content)]
    for m in st.session_state.messages[-8:]:
        if m["role"] == "user":
            history_messages.append(HumanMessage(content=m["content"]))
        else:
            history_messages.append(AIMessage(content=m["content"]))

    with st.chat_message("assistant"):
        with st.spinner("QuickBite AI is preparing your answer..."):
            try:
                ai_response = llm.invoke(history_messages).content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                err_text = f"Apologies, an error occurred: {str(e)}"
                st.error(err_text)
                st.session_state.messages.append({"role": "assistant", "content": err_text})

    lower_input = user_input.lower()
    for item in MENU_DATA:
        if item["name"].lower() in lower_input and any(w in lower_input for w in ["add", "order", "want", "take", "give"]):
            if not any(c["name"] == item["name"] for c in st.session_state.cart):
                st.session_state.cart.append({"name": item["name"], "price": item["price"], "qty": 1})
                st.rerun()
