from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.3)

system_instruction = (
    "You are QuickBite AI, a friendly, professional food ordering assistant for QuickBite. "
    "You assist customers in discovering dishes, taking orders, capturing special instructions, "
    "and confirming deliveries. Always remember and track details provided across previous turns "
    "(such as delivery address, dietary preferences, and selected items) accurately. "
    "Please respond strictly in standard plain text without emojis or non-ASCII symbols."
)

conversation_history = [
    SystemMessage(content=system_instruction)
]

def chat_turn(user_message: str) -> str:
    conversation_history.append(HumanMessage(content=user_message))
    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))
    return response.content

def run_simulation():
    turns = [
        "Hello! I would like to order dinner tonight. My delivery address is 402 Palm Heights, Ring Road, Ahmedabad.",
        "Could you recommend some delicious vegetarian dishes for me?",
        "I'll go with the Paneer Butter Masala and 2 Garlic Naans. Please make the curry extra spicy!",
        "Can you please confirm my complete order and the delivery address you have on record?",
        "Great! What is the estimated delivery time for my order?"
    ]

    print("=" * 70)
    print("QUICKBITE AI - 5-TURN MULTI-TURN CONVERSATION SIMULATION")
    print("=" * 70)

    for i, user_msg in enumerate(turns, start=1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {user_msg}")
        assistant_reply = chat_turn(user_msg)
        print(f"QuickBite AI: {assistant_reply}\n")

    print("=" * 70)
    print("FINAL MEMORY BUFFER DUMP (CONVERSATION HISTORY)")
    print("=" * 70)
    for msg in conversation_history:
        if isinstance(msg, SystemMessage):
            role_label = "SYSTEM"
        elif isinstance(msg, HumanMessage):
            role_label = "USER"
        else:
            role_label = "ASSISTANT"
        print(f"\n[{role_label}]:\n{msg.content}")

def interactive_loop():
    print("=" * 70)
    print("QUICKBITE AI - INTERACTIVE CHAT MODE (Type 'exit' or 'quit' to end)")
    print("=" * 70)
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            break
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("Ending session. Thank you for using QuickBite AI!")
            break
        reply = chat_turn(user_input)
        print(f"\nQuickBite AI: {reply}")

    print("\n" + "=" * 70)
    print("FINAL MEMORY BUFFER DUMP (CONVERSATION HISTORY)")
    print("=" * 70)
    for msg in conversation_history:
        if isinstance(msg, SystemMessage):
            role_label = "SYSTEM"
        elif isinstance(msg, HumanMessage):
            role_label = "USER"
        else:
            role_label = "ASSISTANT"
        print(f"\n[{role_label}]:\n{msg.content}")

if __name__ == "__main__":
    run_simulation()
