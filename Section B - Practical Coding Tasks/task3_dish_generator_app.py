import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

st.set_page_config(page_title="AI Dish Description Generator", page_icon="🍽️", layout="centered")

st.markdown("""
<style>
    .dish-card {
        background-color: #f8f9fa;
        border-left: 5px solid #ff4b4b;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 10px;
        color: #212529;
    }
    .dish-title {
        color: #ff4b4b;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ AI Dish Description Generator")
st.markdown("Craft enticing, sensory-rich menu descriptions for restaurant partners with beverage pairings.")

col1, col2 = st.columns(2)
with col1:
    dish_name = st.text_input("Dish Name", value="Paneer Butter Masala", placeholder="e.g. Truffle Risotto")
with col2:
    cuisine_type = st.selectbox(
        "Cuisine Type",
        ["Indian", "Italian", "Mexican", "Japanese", "Continental"]
    )

length_option = st.selectbox(
    "Description Length",
    [
        "Short - 1 sentence",
        "Medium - 2-3 sentences",
        "Detailed - 4-5 sentences with pairing recommendation"
    ]
)

if "generated_desc" not in st.session_state:
    st.session_state.generated_desc = ""

col_gen, col_regen = st.columns([1, 1])
with col_gen:
    generate_clicked = st.button("✨ Generate Description", use_container_width=True)
with col_regen:
    regenerate_clicked = st.button("🔄 Regenerate", use_container_width=True)

def generate_description(dish, cuisine, length):
    prompt_template = ChatPromptTemplate.from_template(
        """You are an elite culinary copywriter and food critic for a high-end food delivery service called QuickBite.
Write an alluring, mouth-watering menu description for the following dish:

- Dish Name: {dish}
- Cuisine: {cuisine}
- Desired Length Specification: {length}

Guidelines:
1. Use evocative sensory vocabulary (textures, aromas, cooking methods, premium ingredients).
2. Highlight suitable dietary tags (e.g., [Vegetarian], [Vegan], [Gluten-Free], or [Contains Dairy]).
3. Recommend an exquisite beverage pairing (wine, craft beer, mocktail, or traditional brew).
4. Strictly adhere to the requested length specification. Do not include meta-chatter or preamble.
"""
    )
    llm = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.7)
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"dish": dish, "cuisine": cuisine, "length": length})

if generate_clicked or regenerate_clicked:
    if not dish_name.strip():
        st.warning("Please provide a valid dish name before generating.")
    else:
        with st.spinner("Crafting gourmet dish description with sensory notes..."):
            try:
                desc = generate_description(dish_name, cuisine_type, length_option)
                st.session_state.generated_desc = desc
            except Exception as e:
                st.error(f"Failed to generate description: {str(e)}")

if st.session_state.generated_desc:
    with st.container():
        st.markdown(
            f"""
            <div class="dish-card">
                <div class="dish-title">📖 Menu Presentation: {dish_name} ({cuisine_type})</div>
                <p>{st.session_state.generated_desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        char_count = len(st.session_state.generated_desc)
        word_count = len(st.session_state.generated_desc.split())
        st.caption(f"📊 Character Count: **{char_count}** characters | Word Count: **{word_count}** words")
