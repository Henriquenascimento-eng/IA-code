# para interagir com a pagina
import os

# para criar a interface web interativa
import streamlit as st

# para conectar com a API Groq
from groq import Groq


# Configuração da página
st.set_page_config(
    page_title="IA Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Prompt do sistema
CUSTOM_PROMPT = """
Você é o IA Coder, um assistente de IA especialista em programação,
com foco principal em Python e Java.

Sua missão é ajudar desenvolvedores iniciantes com dificuldade.

REGRAS DE OPERAÇÃO:

1 - Foco em programação:
Responda perguntas relacionadas a programação, algoritmos,
estrutura de dados, bibliotecas e frameworks.

2 - Explicação clara:
- Seja didático.
- Mostre exemplos de código quando necessário.
- Explique cada parte do código passo a passo.
- Mostre boas práticas.

3 - Clareza e precisão:
Use linguagem simples e respostas organizadas.

4 - Documentação:
Sempre que possível indique a documentação oficial
da tecnologia citada.
"""


# Barra lateral
with st.sidebar:

    st.title("🤖 IA Coder")

    st.markdown(
        "Um assistente de IA focado em ajudar estudantes de programação iniciantes."
    )


    groq_api_key = st.text_input(
        "Insira sua chave da API Groq",
        type="password",
        help="Pegue sua chave em: https://console.groq.com/keys"
    )


    st.markdown("---")

    st.markdown(
        "Desenvolvido para auxiliar dúvidas de programação 🚀"
    )



# Título principal

st.title("IA Coder")
st.subheader("Assistente de Programação")
st.caption("Faça sua pergunta abaixo 👇")



# Criar histórico da conversa

if "messages" not in st.session_state:
    st.session_state.messages = []



# Mostrar mensagens antigas

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])




# Inicializa cliente

client = None


if groq_api_key:

    try:

        client = Groq(
            api_key=groq_api_key
        )


    except Exception as e:

        st.sidebar.error(
            f"Erro ao conectar com Groq: {e}"
        )

        st.stop()



elif st.session_state.messages:

    st.warning(
        "Insira sua chave da API Groq para continuar."
    )



# Entrada do usuário

if prompt := st.chat_input("Qual sua dúvida?"):


    # verifica API

    if client is None:

        st.warning(
            "Por favor, insira sua chave da API Groq."
        )

        st.stop()



    # salva mensagem usuário

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # mostra mensagem

    with st.chat_message("user"):

        st.markdown(prompt)




    # prepara mensagens para API

    messages_for_api = [
        {
            "role": "system",
            "content": CUSTOM_PROMPT
        }
    ]


    for msg in st.session_state.messages:

        messages_for_api.append(msg)




    # resposta IA

    with st.chat_message("assistant"):


        with st.spinner("Analisando pergunta..."):


            try:


                response = client.chat.completions.create(

                    model="openai/gpt-oss-20b",

                    messages=messages_for_api,

                    temperature=0.7,

                    max_tokens=2048
                )



                ai_response = response.choices[0].message.content



                st.markdown(ai_response)



                # salva resposta

                st.session_state.messages.append(

                    {
                        "role": "assistant",
                        "content": ai_response
                    }

                )



            except Exception as e:


                st.error(
                    f"Erro ao chamar a API: {e}"
                )




# Rodapé

st.markdown(
    """
    <div style="text-align:center; color:gray;">
        <hr>
        <p>IA CODER 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)