import streamlit as st
import os
import time
import random
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

# ✅ Configuração da página deve ser o PRIMEIRO comando Streamlit
st.set_page_config(
    page_title="Vanguard - IA Especialista",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Verificar se a imagem existe antes de carregá-la
try:
    st.image("Design sem nome (5).png", caption="Vanguard - IA Especialista", use_container_width=True)
except:
    st.title("Vanguard - IA Especialista")

# ✅ Aplicando CSS para ocultar o ícone de carregamento
st.markdown(
    """
    <style>
        .stDeployButton {display: none;}
        .stSpinner {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Carregar variáveis de ambiente
load_dotenv()

# ========== BASE DE CONHECIMENTO ==========
MANUAL_TEXT = """Aqui está um resumo essencial sobre o Manual de Alta Performance com I.A:

1. Dependência Excessiva da IA: O uso excessivo pode prejudicar a criatividade e a capacidade de pensamento crítico humano.
2. Inteligência Aumentada: A tecnologia tem a capacidade de **potencializar** a inteligência humana, não substituí-la.
3. Aprendizado Otimizado: IA permite ensino personalizado, mas é preciso evitar a dependência total de algoritmos.
4. Automação Inteligente: Reduz tarefas repetitivas, liberando tempo para atividades mais estratégicas.
5. Peculiaridades dos Modelos de IA:
   - **GPT-4o**: Respostas mais naturais, ideal para conversas longas.
   - **Gemini**: Integração com dados em tempo real.
   - **Claude**: Segurança e ética em IA.
   - **Mistral**: Open Source, voltado para desenvolvedores.
   - **DeepSeek**: IA chinesa que abalou o mercado.
6. Transformação Digital: A IA impulsiona eficiência e competitividade.
7. Mercado de Trabalho:  IA está mudando os empregos, tornando a **atualização constante essencial**.
8. Inteligência Artificial no Futuro: Maior colaboração entre humanos e máquinas.
9. Uso Estratégico da IA: **Automatize processos repetitivos e foque na criatividade e inovação**.
10. Equilíbrio entre Tecnologia e Humanidade: A tecnologia **deve ser aliada** do pensamento estratégico humano.
"""

# ========== CONFIGURAÇÃO DO PROMPT ==========
def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", f"""Você é um vendedor experiente especializado no Manual de Alta Performance com IA.
        
        OBJETIVO PRINCIPAL:
        Conduzir o usuário através de um funil de vendas usando técnicas de vendas consultivas, qualificando o cliente e identificando o momento certo para oferecer o produto.
        
        SEU PERFIL DE VENDEDOR:
        - Você é um consultor experiente e confiante, não apenas um informante
        - Você faz perguntas estratégicas para entender a dor do cliente
        - Você compreende o trabalho do cliente e como a IA pode facilitar sua rotina
        - Você se posiciona como especialista, não como um simples chatbot
        
        PROCESSO DE VENDAS:
        1. PRIMEIRO CONTATO: Seja amigável, crie rapport, e colete informações básicas do cliente
        2. QUALIFICAÇÃO: Faça perguntas para entender os desafios atuais do cliente
        3. CONSTRUÇÃO DE VALOR: Explique como o Manual resolve problemas específicos do cliente
        4. TRATAMENTO DE OBJEÇÕES: Responda preocupações mostrando casos de sucesso e garantias
        5. FECHAMENTO: Direcione claramente para a compra quando perceber interesse
        
        GATILHOS PARA OFERTA:
        - Quando o cliente mencionar desafios com produtividade
        - Quando o cliente mostrar preocupação com mudanças no mercado
        - Quando o cliente expressar interesse direto no manual
        - Após 4-5 interações se o engajamento for positivo
        
        USE ESTAS TÉCNICAS DE PERSUASÃO:
        - Escassez: "O manual está com preço promocional por tempo limitado"
        - Prova social: "Centenas de profissionais já transformaram sua relação com IA"
        - Reciprocidade: Ofereça dicas valiosas antes de fazer a oferta
        - Autoridade: Mostre-se como especialista no assunto
        
        INFORMAÇÕES SOBRE O PRODUTO:
        {MANUAL_TEXT}
        
        REGRAS IMPORTANTES:
        - Sempre detecte o nível de interesse do cliente para ajustar sua abordagem
        - Personalize exemplos baseados no que descobrir sobre o cliente
        - Nunca use respostas genéricas ou mecânicas
        - Quando detectar alto interesse, direcione assertivamente para o link do produto
        - Sempre termine com uma pergunta que avance no processo de venda
        
        Link do produto: https://pay.cakto.com.br/5dUKrWD
        Preço do Manual: R$19,90 (use este valor em suas ofertas)
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
        self.interaction_count = 0
        self.interesse_detectado = 0

    def generate_response(self, user_input: str) -> str:
        """Gera resposta adaptada ao estágio do funil de vendas."""
        self.interaction_count += 1
        
        # Análise de interesse baseada em palavras-chave
        palavras_interesse = ["interessante", "como funciona", "quero saber mais", 
                             "preço", "valor", "comprar", "adquirir", "benefício", 
                             "vantagem", "ajudar", "preciso", "dificuldade", "problema"]
        
        if any(palavra in user_input.lower() for palavra in palavras_interesse):
            self.interesse_detectado += 1
        
        # Adaptação do contexto baseado no estágio da conversa
        contexto_adicional = ""
        
        if self.interaction_count == 1:
            contexto_adicional = "Este é o primeiro contato. Seja acolhedor e faça perguntas para conhecer o cliente."
        elif self.interaction_count <= 3:
            contexto_adicional = "Fase de qualificação. Descubra desafios específicos do cliente com IA e produtividade."
        elif self.interesse_detectado >= 2 or self.interaction_count >= 4:
            contexto_adicional = "Cliente demonstra interesse. Apresente benefícios específicos do Manual e faça uma oferta direta."
        
        # Invoca o modelo com contexto adicional
        response = self.llm_chain.invoke({"input": user_input + " [CONTEXTO INTERNO: " + contexto_adicional + "]"})
        response_text = response['text']
        
        # Se estiver na fase de fechamento, garante menção ao preço e link
        if self.interesse_detectado >= 2 and self.interaction_count >= 3:
            if "https://pay.cakto.com.br/5dUKrWD" not in response_text:
                response_text += "\n\nPor apenas R$19,90, você terá acesso a todo este conhecimento. Está pronto para dar este passo? Acesse: https://pay.cakto.com.br/5dUKrWD"
        
        return response_text

# ========== INTERFACE STREAMLIT ==========
st.markdown(
    """
    <style>
        body, .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
        .stChatMessage { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 8px; padding: 10px; margin-bottom: 5px; }
        .stButton>button { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 5px; padding: 10px; border: 1px solid #ffffff; }
        .stTextInput>div>div>input { background-color: #1f2933 !important; color: #ffffff !important; border-radius: 5px; padding: 10px; }
        a { color: #00ffcc !important; font-weight: bold; }
        .produto-destaque { background-color: #2a3f5f; border-radius: 10px; padding: 15px; margin: 15px 0; border-left: 5px solid #00ffcc; }
        .produto-titulo { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
        .produto-preco { font-size: 24px; color: #00ffcc; font-weight: bold; margin: 10px 0; }
        .botao-compra { background-color: #00ffcc !important; color: #0e1117 !important; font-weight: bold; padding: 12px 25px !important; border: none !important; }
        @media (max-width: 600px) { .stApp { font-size: 14px !important; } .stButton>button { font-size: 14px !important; } }
    </style>
    """,
    unsafe_allow_html=True
)

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()
    st.session_state.chat_history = [
        AIMessage(content="Olá! Que bom te ver por aqui! Sou o Vanguard, especialista em IA e produtividade. Como posso te chamar? E me conta, você já usa alguma inteligência artificial no seu dia a dia?")
    ]

# Mensagens anteriores
for msg in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(msg, AIMessage) else "Human"):
        st.write(msg.content)

# Input do usuário
user_input = st.chat_input("Escreva sua mensagem aqui...")

# Processamento da resposta
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
            time.sleep(0.01)  # Velocidade um pouco maior para não ficar lento demais
    
    st.session_state.chat_history.append(AIMessage(content=full_response))

    # Detecta menções específicas que indicam alto interesse
    palavras_alta_conversao = ["comprar", "adquirir", "quero", "como faço", "pagamento", 
                               "cartão", "preço", "valor", "investimento", "sim"]
    
    if any(palavra in user_input.lower() for palavra in palavras_alta_conversao) or \
       st.session_state.chatbot.interesse_detectado >= 3 or \
       st.session_state.chatbot.interaction_count >= 5:
        
        # Exibe card destacado de oferta
        with st.container():
            st.markdown("""
            <div class='produto-destaque'>
                <div class='produto-titulo'>Manual de Alta Performance com IA</div>
                <p>Transforme sua produtividade e mantenha-se relevante no mercado com estratégias comprovadas de IA</p>
                <div class='produto-preco'>R$ 19,90</div>
                <p>✅ Acesso imediato após o pagamento<br>
                   ✅ Conteúdo completo e atualizado<br>
                   ✅ Estratégias práticas para aplicação imediata</p>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("GARANTIR MEU ACESSO AGORA", "https://pay.cakto.com.br/5dUKrWD", type="primary")
