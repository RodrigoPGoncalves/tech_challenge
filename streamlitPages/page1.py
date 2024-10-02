import streamlit as st
from API.apiKaggle import download_kaggle_dataset
from models.trainModel import train_model,predict_any_value
import pandas as pd

def validate_age(age):
    try:
        age = float(age)
        if age < 0:
            raise ValueError("A idade deve ser um número positivo.")
        return age
    except ValueError:
        st.error("Por favor, insira uma idade válida (número positivo).")
        return None

def get_personality_description(personality_type):
    descriptions = {
        "ISTJ": "O Inspetor: Responsável, confiável, e focado em detalhes.",
        "ISFJ": "O Protetor: Calmo, cuidadoso, e protetor das pessoas próximas.",
        "INFJ": "O Conselheiro: Idealista, visionário, e intuitivo.",
        "INTJ": "O Arquiteto: Estrategista, independente, e criador de sistemas.",
        "ISTP": "O Artesão: Prático, observador, e curioso em explorar como as coisas funcionam.",
        "ISFP": "O Compositor: Artístico, sensível, e com forte apreço pela beleza.",
        "INFP": "O Curador: Idealista, sensível, e motivado por valores pessoais.",
        "INTP": "O Lógico: Analítico, lógico, e focado na compreensão de conceitos abstratos.",
        "ESTP": "O Empreendedor: Energético, ousado, e orientado à ação.",
        "ESFP": "O Animador: Espontâneo, divertido, e sempre o centro das atenções.",
        "ENFP": "O Inspirador: Criativo, entusiasta, e cheio de ideias.",
        "ENTP": "O Visionário: Inovador, curioso, e adora debater ideias.",
        "ESTJ": "O Supervisor: Prático, eficiente, e organizado.",
        "ESFJ": "O Provedor: Sociável, caloroso, e focado em cuidar dos outros.",
        "ENFJ": "O Professor: Inspirador, comunicativo, e motivado a ajudar os outros a crescer.",
        "ENTJ": "O Comandante: Líder nato, assertivo, e focado em resultados."
    }
    return descriptions.get(personality_type, "Descrição não disponível para este tipo.")


def app():
    col3, col4 = st.columns([3, 1]) 

    with col3:
        st.write("Clique no botão para atualizar o dataset.") 

    with col4:
        if st.button("Atualizar Dataset"):
            status, message = download_kaggle_dataset()
            if status == 200:
                st.success(f"DataSet atualizado com sucesso: {message}")
            else:
                st.error(f"Falha ao realizar o download. Erro: {message}")
    
    col5, col6 = st.columns([3, 1]) 

    with col5:
        st.write("Clique para treinar o modelo.") 

    with col6:
        if st.button("Treinar Modelo"):
            status, message = train_model()
            if status == 200:
                st.session_state.training_message = ("success", "Modelo Treinado com Sucesso", message)
            else:
                st.session_state.training_message = ("error", f"Falha ao treinar o modelo. Erro: {message}", None)

    # Exibe a mensagem fora das colunas, centralizada
    if "training_message" in st.session_state:
        msg_type, msg_text, msg_data = st.session_state.training_message

        # Centralizando a mensagem
        st.markdown("<h4 style='text-align: center;'>"+ msg_text +"</h4>", unsafe_allow_html=True)

        # Se o status for de sucesso, mostra o DataFrame abaixo da mensagem
        if msg_type == "success" and msg_data is not None:
            st.dataframe(msg_data)

    st.title("Formulário de Coleta de Dados")

    # Criar um formulário
    with st.form(key='data_collection_form'):
        # Idade
        age = st.number_input("Idade:", min_value=0, max_value=120, step=1)

        # Gênero
        gender = st.selectbox("Gênero:", ("Male", "Female"))

        # Educação
        education = st.selectbox("Nível de Educação:", ("0 - Não graduado", "1 - Graduado ou superior"))

        # Interesse
        interest = st.selectbox("Área de Interesse:", ("Technology", "Sports", "Unknown", "Arts", "Others"))

        # Notas de 0 a 10 para os diferentes scores
        introversion_score = st.selectbox("Introversion Score (0 a 10):", list(range(0, 11)))
        sensing_score = st.selectbox("Sensing Score (0 a 10):", list(range(0, 11)))
        thinking_score = st.selectbox("Thinking Score (0 a 10):", list(range(0, 11)))
        judging_score = st.selectbox("Judging Score (0 a 10):", list(range(0, 11)))
        
        # Botão para enviar o formulário
        submit_button = st.form_submit_button(label='Analisar')

        if submit_button:
            # Validar e coletar os dados
            validated_age = validate_age(age)
            
            if validated_age is not None:
                # Criar um DataFrame com os dados coletados
                data = {
                    "age": validated_age,
                    "gender": gender,
                    "education": 1 if education == "1 - Graduado ou superior" else 0,
                    "interest": interest,
                    "introversion_score": introversion_score,
                    "sensing_score": sensing_score,
                    "thinking_score": thinking_score,
                    "judging_score": judging_score,
                }
                df = pd.DataFrame([data])
                status, prediction = predict_any_value(df)
                if status == 200:
                    st.success("Dados coletados com sucesso!")
                    personality_type = prediction[0]  # Altere conforme necessário, dependendo do formato da previsão
                    st.markdown(f"Sua personalidade é: {get_personality_description(personality_type)}")
                else:
                    st.error(f"Falha ao informar Personalidade {prediction}")

