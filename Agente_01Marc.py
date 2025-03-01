
import streamlit as st
import os
import time
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

# ✅ Configuração da página deve ser o PRIMEIRO comando Streamlit
st.set_page_config(
    st.image("sua_imagem.png", caption="Vanguard - IA Especialista", use_column_width=True),
    page_title="Vanguard - IA Especialista",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Aplicando CSS para ocultar o ícone de carregamento
st.markdown(
    """
    <style>
        .stDeployButton {display: none;}
        .stSpinner {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar variáveis de ambiente
load_dotenv()

# ========== BASE DE CONHECIMENTO DIRETA ==========
MANUAL_TEXT = """Aqui está um resumo essencial sobre Inteligência Artificial e conceitos sobre a Inteligência Aumentada:

1. Dependência Excessiva da IA: O uso excessivo pode prejudicar a criatividade e a capacidade de pensamento crítico humano.
2. Inteligência Aumentada: A tecnologia tem a capacidade **potencializar** a inteligência humana, não substituí-la.
3. Aprendizado Otimizado: IA permite ensino personalizado, mas é preciso evitar a dependência total de algoritmos.
4. Automação Inteligente: Reduz tarefas repetitivas, liberando tempo para atividades mais estratégicas.
5. Peculiaridades dos Modelos de IA:
   - **GPT-4o**: Respostas mais naturais, ideal para conversas longas.
   - **Gemini**: Integração com dados em tempo real.
   - **Claude**: Segurança e ética em IA.
   - **Mistral**: Open Source, voltado para desenvolvedores.
   - **DeepSeek**: IA chinesa que abalou o mercado.
6. Transformação Digital: A IA impulsiona eficiência e competitividade.
7. Mercado de Trabalho: A IA está mudando os empregos, tornando a **atualização constante essencial**.
8. Inteligência Aumentada no Futuro: Maior colaboração entre humanos e máquinas.
9. Uso Estratégico da IA: **Automatize processos repetitivos e foque na criatividade e inovação**.
10. Equilíbrio entre Tecnologia e Humanidade: A tecnologia **deve ser aliada** do pensamento estratégico humano.
"""

# ========== CONFIGURAÇÃO DO PROMPT ==========
def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", f"""Você é um especialista em Inteligência Artificial e Inteligência Aumentada.
        Seu objetivo é **explicar conceitos sobre IA** e **persuadir o usuário** a entender sua importância no mercado e converter a interação em venda.
        Use respostas claras e objetivas, sem parágrafos longos. **Sempre finalize com uma pergunta estratégica para engajar a conversa.**
        
        Aqui estão informações importantes que você deve usar nas respostas:
        {MANUAL_TEXT}
        
        Se perceber que o usuário está interessado, direcione-o para o link do produto (https://pay.cakto.com.br/5dUKrWD).
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

# ========== LÓGICA PRINCIPAL ==========
class Chatbot:
    def __init__(self):
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            input_key="input",
            k=5,
            return_messages=True
        )
        self.llm_chain = LLMChain(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
            prompt=get_prompt(),
            memory=self.memory
        )

    def generate_response(self, user_input: str) -> str:
        """Gera resposta baseada diretamente no manual e no prompt."""
        response = self.llm_chain.invoke({"input": user_input})
        response_text = response['text']

        # Adiciona uma pergunta estratégica para engajamento
        perguntas_estrategicas = [
            "Como você acredita que a IA pode melhorar sua rotina?",
            "Você já tentou alguma ferramenta de IA antes?",
            "Se pudesse automatizar uma tarefa chata do seu dia, qual seria?",
            "Qual seu maior desafio hoje que a IA poderia resolver?",
            "Você gostaria de conhecer um método comprovado para usar IA na produtividade?"
        ]
        import random
        pergunta = random.choice(perguntas_estrategicas)

        return f"{response_text} {pergunta}"

# ========== INTERFACE STREAMLIT ==========
st.markdown(
    """
    <style>
        body, .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
        .stChatMessage { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 8px; padding: 10px; margin-bottom: 5px; }
        .stButton>button { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 5px; padding: 10px; border: 1px solid #ffffff; }
        .stTextInput>div>div>input { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 5px; padding: 10px; }
        a { color: #00ffcc !important; font-weight: bold; }
        @media (max-width: 600px) { .stApp { font-size: 14px !important; } .stButton>button { font-size: 14px !important; } }
    </style>
    """,
    unsafe_allow_html=True
)

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()
    st.session_state.chat_history = [
        AIMessage(content="Olá! Eu sou o Vanguard, especialista no Manual de Alta Performance com IA. Qual o seu nome?")
    ]

for msg in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(msg, AIMessage) else "Human"):
        st.write(msg.content)

user_input = st.chat_input("Escreva sua pergunta sobre IA aqui...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("Human"):
        st.write(user_input)

    with st.chat_message("AI"):
        response = st.session_state.chatbot.generate_response(user_input)
        response_placeholder = st.empty()
        full_response = ""
        for char in response:
            full_response += char
            response_placeholder.markdown(full_response)
            time.sleep(0.03)
    
    st.session_state.chat_history.append(AIMessage(content=full_response))

    # Se o usuário demonstrar interesse em comprar, exibe o link do produto
    if "sim" in full_response.lower() or "quero comprar" in full_response.lower():
        st.markdown("### 🚀 Garanta Seu Acesso Imediato! Por apenas 19.90")
        st.link_button("Adquirir Manual Completo", "https://pay.cakto.com.br/5dUKrWD")
