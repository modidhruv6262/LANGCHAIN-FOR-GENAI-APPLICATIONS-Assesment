# QuickBite AI - Mini-Capstone System Documentation

## 1. System Architecture Overview

QuickBite AI is an end-to-end Generative AI and Machine Learning food ordering assistant. It integrates predictive ML, prompt engineering with few-shot demonstration, LangChain conversational flow, and a rich Streamlit chat interface.

```mermaid
flowchart TD
    User([Customer / User]) <--> UI[Streamlit Web Application]
    
    subgraph UI_Components [Streamlit Frontend Interface]
        UI --> ChatWindow[Interactive Chat Bubbles]
        UI --> Sidebar[Sidebar: Profile, Active Cart, Direct Estimator]
    end
    
    subgraph Agent_Core [LangChain Orchestration Engine]
        ChatWindow --> PromptEngine[Few-Shot Prompt Template & History]
        PromptEngine --> LLM[Groq ChatGroq LLM Engine]
        PromptEngine <--> MenuKB[(menu.json Knowledge Base)]
        PromptEngine <--> ToolEngine[@tool get_delivery_estimate]
    end
    
    subgraph ML_Layer [Scikit-Learn Regression Engine]
        ToolEngine --> Model[(delivery_model.joblib)]
        Sidebar --> Model
    end
```

---

## 2. Component Descriptions

| Component | Technology | Purpose & Implementation Details |
| :--- | :--- | :--- |
| **Machine Learning Model** | Scikit-Learn `LinearRegression`, Joblib | Trained on delivery parameters (Distance in km, Number of Items, Weather/Rain Flag) achieving an RMSE of **1.78 minutes**. Persisted as `delivery_model.joblib`. |
| **Delivery Estimation Tool** | LangChain Core `@tool` | Decorated function `get_delivery_estimate(distance_km, num_items, is_peak)` invoked dynamically to supply reliable delivery estimates. |
| **Menu Knowledge Base** | `menu.json` + Retrieval Engine | 12 diverse culinary items spanning Indian, Italian, Continental, Japanese, and Mexican cuisines with pricing, descriptions, and dietary classifications. |
| **Conversational Agent** | LangChain + Groq (`openai/gpt-oss-120b`) | Multi-turn stateful conversational agent governed by a system prompt and two few-shot exemplars ensuring polite tone, dietary adherence, and factual responses. |
| **User Interface** | Streamlit | Chat interface with `st.chat_message`, customer profile sidebar, reactive cart, live distance slider, and session state reset controls. |

---

## 3. Sample Conversation Logs

### Conversation Log 1: Dietary Filtering & Order Selection
```text
User: Hello! I follow a strictly vegetarian diet. What do you recommend from Indian and Italian cuisines?
QuickBite AI: Hello! Welcome to QuickBite. Based on your vegetarian preference, here are top recommendations:
1. Paneer Butter Masala (Indian, Rs. 320) - Succulent cubes of cottage cheese simmered in a velvety tomato-cashew gravy enriched with butter.
2. Dal Makhani (Indian, Rs. 280) - Slow-cooked black lentils and kidney beans simmered overnight with butter and cream.
3. Margherita Gourmet Pizza (Italian, Rs. 390) - Wood-fired hand-tossed crust topped with San Marzano tomato sauce, fresh mozzarella fior di latte, and basil.
4. Truffle Mushroom Risotto (Italian, Rs. 450) - Creamy Arborio rice with wild porcini mushrooms, parmesan shavings, and white truffle oil.
Would you like me to add any of these to your order?

User: Please add 1 Paneer Butter Masala and 1 Margherita Gourmet Pizza to my cart.
QuickBite AI: Excellent! I have added:
- 1x Paneer Butter Masala (Rs. 320)
- 1x Margherita Gourmet Pizza (Rs. 390)
Total Cart Value: Rs. 710.
Your delivery address on record is: Flat 402, Royal Palms, SG Highway, Ahmedabad.
```

### Conversation Log 2: ML Delivery Estimation
```text
User: How long will it take for my order to arrive? The restaurant is roughly 6 km away.
QuickBite AI: Calling QuickBite ML Prediction Engine...
- Distance: 6.0 km
- Total Items: 2 items
- Weather: Normal conditions
The predicted delivery time is approximately 28.6 minutes. Your order is being prepared fresh and will be delivered shortly!
```

---

## 4. Instructions for Running the Application

1. Ensure the virtual environment is activated:
   ```powershell
   .\env\Scripts\activate
   ```
2. Launch the Streamlit application:
   ```powershell
   streamlit run "Section C - Mini Capstone Project/app.py"
   ```
3. Open your browser at `http://localhost:8501` to interact with QuickBite AI.
