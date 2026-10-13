# Section A — Concept Application

---

## Scenario 1: Model Serialisation — Pickle vs. Joblib in Production Flask APIs

**Comparison & Selection:**  
For deploying a scikit-learn regression model in a production Flask API handling hundreds of requests per hour, **Joblib** is the superior serialisation choice over Python's standard `pickle`. While `pickle` serialises arbitrary Python object hierarchies as generic byte streams, `joblib` is explicitly optimised for scientific computing objects containing large internal NumPy arrays, using memory mapping and efficient chunking that dramatically accelerates disk I/O and deserialisation speeds during service initialization. 

**Environment Mismatch Risks:**  
Both formats store object class references and memory representations rather than portable executable code. If the deployment container uses a different Python, scikit-learn, or NumPy version than the training environment, deserialisation frequently throws `ModuleNotFoundError`, `AttributeError`, or silent numerical incompatibilities due to internal C-extension and class layout changes. Additionally, unpickling untrusted files presents severe arbitrary code execution vulnerabilities (`__reduce__` exploit), requiring strict container immutability and checksum verification.

---

## Scenario 2: Image Generation — Variational Autoencoders (VAEs) vs. Stable Diffusion

**Architectural Differences & Output Quality:**  
Variational Autoencoders (VAEs) are deterministic encoder-decoder networks trained via an explicit reconstruction loss combined with KL-divergence, compressing inputs into a smooth continuous latent space. Consequently, VAE reconstructions and generations inherently suffer from blurry edges, loss of fine textural details, and oversmoothed realism because pixel-wise mean squared error penalises sharp high-frequency variations. In contrast, **Stable Diffusion** models operate by iteratively denoising Gaussian noise in a latent feature space conditioned on text and image cross-attention embeddings, generating photorealistic, high-frequency textural details such as food garnishes, sauces, and lighting reflections.

**Production Recommendation:**  
Stable Diffusion (specifically ControlNet or image-to-image conditioning) is the only viable choice for a commercial marketing pipeline. While VAEs offer faster single-step inference, their blurred outputs look unappetising and fail commercial standards, whereas Stable Diffusion preserves plated dish geometry while synthesising studio-grade promotional aesthetics.

---

## Scenario 3: Architectural Specialisation — Decoder-Only (GPT) vs. Encoder-Only (BERT)

**Task 1: Open-Ended Recommendation Generation (Decoder-Only GPT):**  
Answering conversational, open-ended inquiries such as *"What cuisines are trending near me this weekend?"* requires an autoregressive **decoder-only model (GPT style)**. Decoder architectures use causal (masked) self-attention, ensuring each token is predicted strictly from preceding context, which is the mathematically necessary inductive bias for coherent, fluid, and creative multi-token natural language generation.

**Task 2: Sentiment Classification (Encoder-Only BERT):**  
Classifying incoming customer feedback into Positive, Neutral, or Negative is optimal for a **bidirectional encoder-only model (BERT style)**. Encoder architectures employ unmasked, bidirectional attention, allowing every token to attend simultaneously to both left and right context representations across the entire sentence, capturing nuanced grammatical qualifiers (e.g., *"not bad at all"* vs *"really bad"*). This produces fixed-size dense pooled embeddings ideal for training a compact, low-latency, and cost-effective softmax classification head.

---

## Scenario 4: Few-Shot Prompt Engineering for Cold-Start Customer Support

**Concept Comparison:**  
**Zero-shot prompting** provides the LLM only with task instructions and category labels without concrete demonstrations, forcing reliance on generalised prior training. **Few-shot prompting** conditions the LLM's in-context learning by including a small set of exemplar input-output demonstrations directly inside the prompt context window, establishing the expected tone, boundary resolution, and structured output formatting.

**Strategy & Prompt Structure:**  
Given 3 annotated pairs per category across unseen classes ('wrong item delivered', 'packaging damaged', 'missing cutlery'), **few-shot prompting** is strictly required. The prompt should be structured with: (1) a system role assigning food delivery support responsibilities, (2) clear operational definitions of each category, (3) exactly 2 to 3 balanced input-output demonstration pairs per category demonstrating edge cases, and (4) strict formatting instructions (e.g., *"Output strictly JSON with keys: category and proposed_resolution"*). This eliminates ambiguity and enforces consistent taxonomy without model fine-tuning.

---

## Scenario 5: LangChain Agents vs. Chains — Trade-Offs in Dynamic Food Ordering

**Distinction & Justification:**  
A standard LangChain `Chain` (like `LLMChain` or LCEL pipelines) follows a rigid, hardcoded sequential execution graph where every step occurs regardless of user input. A **LangChain Agent** leverages the LLM as a dynamic reasoning engine within a ReAct (Reason + Act) loop, autonomously deciding which tools to call, with what parameters, and in what order based on runtime state. Because this ordering assistant must dynamically inspect live restaurant availability, invoke a regression API for transit estimates, and validate coupon codes, an **Agent** is necessary to dynamically choose the appropriate external API based on user intent.

**Introduced Risks:**  
1. **Non-Deterministic Execution & Infinite Loops:** The agent may enter repetitive tool-calling cycles or select inappropriate tools if an API returns ambiguous error messages, resulting in high token costs and latency timeouts.  
2. **Security & Parameter Injection Risks:** The LLM translates unvalidated natural language into tool parameters; malicious or unexpected user prompts can trick the agent into passing malformed payloads to backend REST APIs.

---

## Scenario 6: Knowledge Grounding — Fine-Tuning vs. Retrieval-Augmented Generation (RAG)

**Comparison Across Operational Dimensions:**  
- **Update Frequency & Agility:** Fine-tuning requires curating datasets and retraining model weights, which is completely unfeasible for a menu catalogue updated daily. RAG updates instantaneously by simply indexing new vectors into a vector database without model retraining.  
- **Inference Cost & Hardware:** Fine-tuning incurs massive GPU training compute costs; RAG requires only lightweight embedding generation and vector lookups.  
- **Hallucination Risk & Citations:** Fine-tuned models encode facts probabilistically in internal weights, leading to confident hallucinations; RAG retrieves verbatim handbook clauses and grounds the answer strictly in retrieved context with source attribution.  
- **Data Privacy:** RAG supports fine-grained document access control (filtering documents by user role before vector retrieval), whereas fine-tuned models permanently absorb sensitive data across all users.

**Recommendation & Residual Limitations:**  
**RAG is overwhelmingly the correct architecture** for this scenario. However, RAG still carries limitations: retrieval quality depends heavily on chunking heuristics (bad chunks sever policy tables), dense semantic search can fail on exact keyword or numerical item code lookups without hybrid BM25 search, and large retrieved context blocks consume context window capacity, increasing per-turn inference latency.
