import streamlit as st
import pandas as pd

def app():
    st.markdown("<h1 style='text-align: center;'>Análise do DataSet</h1>", unsafe_allow_html=True)


    st.markdown("Abaixo será apresentada a análise e investigação dos dados de People Personality retirados do link abaixo:")
    st.markdown("[Link para o dataset no Kaggle](https://www.kaggle.com/datasets/stealthtechnologies/predict-people-personality-types/data)")


    st.markdown("""
    O intuito aqui é, a partir de dados inseridos pelo usuário, prever qual a sua personalidade classificada pelo
    sistema chamado MBTI (Myers-Briggs Type Indicator), um instrumento psicológico baseado nas teorias de Carl Jung.
    Este sistema divide as personalidades humanas em 16 tipos diferentes com base em quatro dicotomias principais.
    """)

    st.markdown("""
    Essas quatro dicotomias são:
    - **Extroversão (E) vs. Introversão (I)**: Como você lida com o mundo externo e obtém energia.
    - **Sensação (S) vs. Intuição (N)**: Como você percebe o mundo e processa informações.
    - **Pensamento (T) vs. Sentimento (F)**: Como você toma decisões.
    - **Julgamento (J) vs. Percepção (P)**: Como você organiza sua vida externa.
    """)

    st.markdown("A descrição dos dados (alvos a serem previstos) disponíveis neste dataset pode ser vista abaixo.")
    st.markdown("""
                - **ISTJ**: O Inspetor: Responsável, confiável, e focado em detalhes.
                - **ISFJ**: O Protetor: Calmo, cuidadoso, e protetor das pessoas próximas.
                - **INFJ**: O Conselheiro: Idealista, visionário, e intuitivo.
                - **INTJ**: O Arquiteto: Estrategista, independente, e criador de sistemas.
                - **ISTP**: O Artesão: Prático, observador, e curioso em explorar como as coisas funcionam.
                - **ISFP**: O Compositor: Artístico, sensível, e com forte apreço pela beleza.
                - **INFP**: O Curador: Idealista, sensível, e motivado por valores pessoais.
                - **INTP**: O Lógico: Analítico, lógico, e focado na compreensão de conceitos abstratos.
                - **ESTP**: O Empreendedor: Energético, ousado, e orientado à ação.
                - **ESFP**: O Animador: Espontâneo, divertido, e sempre o centro das atenções.
                - **ENFP**: O Inspirador: Criativo, entusiasta, e cheio de ideias.
                - **ENTP**: O Visionário: Inovador, curioso, e adora debater ideias.
                - **ESTJ**: O Supervisor: Prático, eficiente, e organizado.
                - **ESFJ**: O Provedor: Sociável, caloroso, e focado em cuidar dos outros.
                - **ENFJ**: O Professor: Inspirador, comunicativo, e motivado a ajudar os outros a crescer.
                - **ENTJ**: O Comandante: Líder nato, assertivo, e focado em resultados.
                """)
    st.header("Análise DataSet")
    st.markdown("Carregando dados:")
    codeLoadData = """
                    df = pd.read_csv('dataPersonality.csv')
                    """
    st.code(codeLoadData, language='python')
    st.markdown("O Dataframe possui o seguinte shape: (128061, 9)")
    
    st.markdown("Inicialmente foi verificado com o código abaixo a necessidade de algum tratamento das variáveis devido à falta ou duplicidade de dados:")

    code1 = '''
    print("Head dos dados")
    print(df.head())
    print("Descrição dos dados")
    print(df.describe())
    print("Valores Nulos")
    print(df.isnull().sum())
    print("Valores NA")
    print(df.isna().sum())
    df_duplicatedColumns = df.loc[df.duplicated() == True]
    print("Valores duplicados")
    print(df_duplicatedColumns.head())
    '''
    st.code(code1, language='python')
    
    st.markdown("Abaixo é possível ver como é um pedaço dos dados desse dataframe:")
    data = {
    'Age': [19, 27, 21, 28, 36],
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Female'],
    'Education': [0, 0, 0, 0, 1],
    'Introversion Score': [9.47080, 5.85392, 7.08615, 2.01892, 9.91703],
    'Sensing Score': [7.141434, 6.160195, 3.388433, 4.823624, 4.755080],
    'Thinking Score': [6.03696, 0.80552, 2.66188, 7.30625, 5.31469],
    'Judging Score': [4.360278, 4.221421, 5.127320, 5.986550, 4.677213],
    'Interest': ['Unknown', 'Sports', 'Unknown', 'Others', 'Technology'],
    'Personality': ['ENFP', 'ESFP', 'ENFP', 'INTP', 'ENFP']
    }
    st.dataframe(pd.DataFrame(data).head())
    
    st.markdown("""Logo, o proximo passo é entender como estão distribuidos os alvos do nosso modelo,
                no caso a coluna Personality do dataframe, mostrado na imagem abaixo em formato de porcentagem no dataset""")
    st.image("./images/pizzaPersonality.png", caption="Quantidade da variavel target Personality", use_column_width=True)
    
    st.markdown("Por curiosidade tbm trouxe a variável categorica Interest, pois percebi que talvez ela poderia ser um gargalo na distribuição de dados ")
    st.image("./images/pizzaInterest.png", caption="Quantidade da variavel Interest", use_column_width=True)
    
    st.markdown("""Ao olhar para os dados de Interest percebo que o mesmo não dará problemas para o modelo, já a variável
                    Personality tem um grande desbalancemento em suas classes o que pode ser prejudicial para o modelo.
                    Assim, começo a preparar os dados de forma a não só testar com o conjunto completo, mas também avaliar
                    se dividir a variável Personality em dois modelos, e depois uni-los através de probabilidade ou um terceiro modelo
                    não é melhor do que realizar algum tipo de balanceamento, já que aumentando os dados eu teria muitos dados replicados
                    ou não verdadeiros e diminuindo teria dados que talvez não generalizassem a informação.""")
    st.markdown("""
                Agora, sabendo como estão os dados e suas caracteristicas basta realizar os ajustes de forma a normalizar dados contínuos e
                categorizar os dados que estão no formato string, para isso utilizei o código descrito abaixo, onde inicialmente é coletado os
                index de forma a já possuir uma divisão em um conjunto de dados de alta frquencia, concentrando os targets de valores
                ["ENFP", "ENTP", "INFP", "INTP"] e outro com dados de menor frequencia ["ESFP", "ENFJ", "ISFP", "ESTP", "INFJ", "ENTJ", "ISTP", "INTJ", "ESFJ", "ESTJ", "ISFJ", "ISTJ"]
                """)
    
    code2 = '''
    perdonality_Big = ["ENFP", "ENTP", "INFP", "INTP"]
    perdonality_Small = ["ESFP", "ENFJ", "ISFP", "ESTP", "INFJ", "ENTJ", "ISTP", "INTJ", "ESFJ", "ESTJ", "ISFJ", "ISTJ"]
    index_big = df.index[df['Personality'].isin(perdonality_Big)].tolist()
    index_small = df.index[df['Personality'].isin(perdonality_Small)].tolist()


    # Definindo as colunas
    continuous_cols = ["Age", "Introversion Score", "Sensing Score", "Thinking Score", "Judging Score"]
    categorical_cols = ["Gender","Interest"]
    others_cols = ["Education"]
    y_target = ["Personality"]

    le_gender = LabelEncoder()
    le_interest = LabelEncoder()
    le_y = LabelEncoder()
    scaler = MinMaxScaler()


    def preprocess_dataY(df):
        y_processed = pd.DataFrame()
        y_processed['Personality'] = le_y.fit_transform(df['Personality'])
        return y_processed

    def preprocess_dataX(df):
        X_processed = pd.DataFrame()

        X_processed[categorical_cols[0]] = le_gender.fit_transform(df[categorical_cols[0]].values)
        X_processed[categorical_cols[1]] = le_interest.fit_transform(df[categorical_cols[1]].values)
        
        normalized_array = scaler.fit_transform(df[continuous_cols])
        X_processed[continuous_cols] = pd.DataFrame(normalized_array, columns=continuous_cols)
        
        X_processed[others_cols] = df[others_cols]
        
        return X_processed

    y_processed = preprocess_dataY(df[y_target])
    X_processed = preprocess_dataX(df)
    '''
    st.code(code2, language='python')
    
    st.markdown("""
                Logo em seguida é necessário avaliar as informações de X e y_processed de forma a garantir que os seus tipos estão corretos
                """)
    code3 = '''
    print(X_processed.info())
    print(y_processed.info())
    '''
    st.code(code3, language='python')
    
    info1 = """
    RangeIndex: 128061 entries, 0 to 128060
    Data columns (total 8 columns):
    #   Column              Non-Null Count   Dtype  
    ---  ------              --------------   -----  
    0   Gender              128061 non-null  int32  
    1   Interest            128061 non-null  int32  
    2   Age                 128061 non-null  float64
    3   Introversion Score  128061 non-null  float64
    4   Sensing Score       128061 non-null  float64
    5   Thinking Score      128061 non-null  float64
    6   Judging Score       128061 non-null  float64
    7   Education           128061 non-null  int64  
    dtypes: float64(5), int32(2), int64(1)
    memory usage: 6.8 MB
    """

    info2 = """
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 128061 entries, 0 to 128060
    Data columns (total 1 columns):
    #   Column       Non-Null Count   Dtype
    ---  ------       --------------   -----
    0   Personality  128061 non-null  int32
    dtypes: int32(1)
    memory usage: 500.4 KB
    """

    # Exibindo as informações do DataFrame no Streamlit
    st.text("Informações sobre o DataFrame:")
    st.text(info1)

    st.text("Informações sobre o DataFrame (Personalidade):")
    st.text(info2)

    st.markdown("""
                Antes de seguirmos par ao modelo é necessário analisar como essas variavéis agora transformadas estão se comportando, logo,
                de forma visual analisar o histograma delas e entender como está suas distribuições.
                """)
    st.image("./images/histogramAllDataset.png", caption="Histograma das Variaveis de X_processed", use_column_width=True)
    st.markdown("""
                Apesar do desbalanceamento já sábido da variavel target Personality, percebe-se que temos uma curva gaussiana bem definida
                nas variaveis Age, Sensing Score e Judging Score e uma boa divisão na quantidade de classes em Education, Gender e até em
                Interest (onde talvez possa haver necessidade de alguma diminuição de dados de Unknown para balanceamento). 
                A tendência a uma curva gaussiana no histograma ajuda no treinamento dos dadoss, mas nem sempre isso é possível, então, 
                apesar das variáveis Introversion Score e Thinking Score não possuirem tal característica seguiremos desta forma para a modelagem
                do machine learning e lá entender o quanto essa variável irá interferir ou não no treinamento.
                """)
    
    st.markdown("""
                Outra visão interessante para se ter antes de serguir par a modelagem é o heatmap, onde o intuito é ver de uma forma clara
                se alguma variavel está ou não relacionada com outra, indicando que será necessário realizar analises mais profunda como o 
                uso do pvalue e outras de forma a entender se tal correlação será ou não prejudiciosa para o modelo. 
                """)
    st.image("./images/heatmapAll.png", caption="Histograma das Variaveis de X_processed", use_column_width=True)
    st.markdown("""
                Como podemos observar na imagem acima, as variaveis possuem baixa correlação, então neste momento não irei buscar outras analises
                de varivaies para seguir para a modelagem.
                """)