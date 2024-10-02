import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center;'>Modelagem ML</h1>", unsafe_allow_html=True)

    st.markdown("Abaixo será apresentado a método de Machine Learning escolhido e os dados obtidos")
    
    st.markdown("""Após algumas pesquisas foi verificado que dentre os melhores métodos de ML para a aplicação de classificação em questão
                seria o NaiveBayes e o RandomForest, aplicados juntos ao cross validantion e uma técnica de busca aleatória de 
                parametros chamada RandomizedSearchCV.""")
    st.markdown("""
                Após alguns testes e validações do métodos citados acima e análise das métricas que serão 
                demonstradas abaixo cheguei a conclusão que o melhor modelo para a classificação da personalidade do usuário é o 
                RandomForestClassifier.
                """)
    
    st.markdown("""
                Desta forma, após obter o X e y_processed foi necessário dividir os dados nas categorias de treinamento e test e para isso foi
                utilizado o código abaixo onde o critério de separação foi de 20% dos dados para test.
                """)
    codeTrainTest = """
                    X_train, X_test, y_train, y_test = train_test_split(X_processed, y_processed, test_size=0.2, random_state=42)
                    """
    st.code(codeTrainTest, language='python')
    
    st.markdown("""
                Através da métrica RandomizedSearchCV, foi definido um conjunto de parâmetros do RandomForest para serem variados de forma
                aleátoria e validados com o intuito de retornar o melhor resultado possível, esse grid de parâmetro pode ser visto abaixo.
                """)
    codeParamGrid = """
                    param_grid = {
                        'n_estimators': [50, 100, 150,200],
                        'max_depth': [None, 10, 20, 30],
                        'min_samples_split': [2, 5, 10, 15],
                        'min_samples_leaf': [1, 2, 4, 6],
                    }
                    """
    st.code(codeParamGrid, language='python')
    
    st.markdown("""
                Agora, basta aplicar o RandomForest através do RandomizedSearchCV, onde foi definido que deveria haver 30 iterações aleatórias
                sendo cada uma um modelo diferente baseado nos parâmetros que podiam ser variados já citado acima. Além disso foi definido uma 
                janela de CrossValidation de 5 posições:
                """)
    
    codeModel = """
                    rf_all = RandomForestClassifier(random_state=42)
                    random = RandomizedSearchCV(rf_all, param_distributions=param_grid, cv=5,n_iter=30, scoring='accuracy',n_jobs=-1)
                    random.fit(X_train, y_train)
                """
    st.code(codeModel, language='python')
    
    st.markdown("""
                Ao final da compilação é possível identificar quais foram os melhores parâmetros utilizados nos conjuntos de treinamento.
                """)
    
    bestParamsRf = {
    'n_estimators': 200, 
    'min_samples_split': 10, 
    'min_samples_leaf': 4, 
    'max_depth': 20
    }
    st.write(bestParamsRf)
    
    st.markdown("""
                Utilizando o codigo construído abaixo é possível avaliar as principais métricas para ver o comportamento do modelo treinado acima:
                """)
    codeVarAnalise = """
                    def print_classification_report(y_test, targets, predicao):
                        report_rf_Small = classification_report(y_test, predicao, target_names=targets)
                        print("Classification Report Random Forest Small:")
                        print(report_rf_Small)

                    def print_confusion_matrix( y_test, targets,predicao):
                        matriz_rf_Small = confusion_matrix(y_test, predicao)
                        labels_Small = targets

                        # Plotar a matriz de confusão usando seaborn
                        plt.figure(figsize=(10, 7))
                        sns.heatmap(matriz_rf_Small, annot=True, fmt='g', cmap='Blues', xticklabels=labels_Small, yticklabels=labels_Small)
                        plt.xlabel('Predicted')
                        plt.ylabel('True')
                        plt.title('Confusion Matrix')
                        plt.show()
                        
                    def print_feature_importance(modelo, nameColums):
                        feature_importance_rf_Small = modelo.feature_importances_

                        # Plotar importância das features
                        plt.figure(figsize=(10, 6))
                        sorted_idx = np.argsort(feature_importance_rf_Small)[::-1]
                        features = nameColums
                        plt.barh(features[sorted_idx], feature_importance_rf_Small[sorted_idx])
                        plt.xlabel('Feature Importance')
                        plt.ylabel('Feature')
                        plt.title('Feature Importance')
                        plt.show()
                    def analise_dados_modelo(modelo, x_train, y_train, x_test, y_test, targets, nameColums):
                        modelo.fit(x_train, y_train)
                        predicao = modelo.predict(x_test)
                        
                        print_classification_report(y_test, targets, predicao)
                        print_confusion_matrix( y_test, targets,predicao)
                        print_feature_importance(modelo, nameColums)
                """
    st.code(codeVarAnalise, language='python')
    
    
    
    st.markdown("""
                Agora sim é podemos analisar como se comportou o modelo treinado com os melhores parâmetros, abaixo é possível
                observar o Classification Report, onde a variável que deve ser mais notada é o F1 Score, pois ela informa uma relação
                entre a acurácia (proporção de previsões corretas feitas pelo modelo em relação ao total de previsões) e o recal
                (proporção de positivos reais que foram corretamente identificados pelo modelo), temos a matriz de confusão onde pode 
                se observar o valor absoluto de acertos e erros de cada uma classe e ao final a analise de importancia de cada feature 
                (variável) utilizada para o treinamento do modelo.
                """)
    classification_report = """
    Classification Report Random Forest Small:
                precision    recall  f1-score   support

            ENTP       0.94      0.91      0.93       799
            INTJ       0.93      0.94      0.93      6963
            ENFP       0.93      0.89      0.91       531
            INTP       0.92      0.93      0.93      4989
            INFP       0.82      0.75      0.78       101
            ESFP       0.85      0.84      0.84       981
            INFJ       0.89      0.73      0.80        78
            ISFP       0.84      0.81      0.82       633
            ESTP       0.91      0.91      0.91       611
            ENFJ       0.90      0.91      0.91      4895
            ENTJ       0.92      0.85      0.88       362
            ISTP       0.89      0.91      0.90      3415
            ESTJ       0.87      0.55      0.67        75
            ISTJ       0.82      0.78      0.80       670
            ESFJ       0.83      0.79      0.81        48
            ISFJ       0.84      0.79      0.81       462

        accuracy                           0.91     25613
    macro avg       0.88      0.83      0.85     25613
    weighted avg       0.91      0.91      0.91     25613
    """

    st.code(classification_report)
    st.markdown("""
                Analisando o classification report, mais especificadamente o F1 score percebe-se que a porcentagem de acerto, apesar 
                do desbalanceamento de algumas classes, foi muito boa, melhor do que esperado, logo, entendo que o modelo ficou bem treinado
                já que até para pouca quantidade de dados ele foi capaz de obter valores bem altos de acerto, mesmo para as classes com 
                menor quantidade de amostras como ESFJ, ESTJ, ISFJ, ISTJ.
                """)
    
    st.image("./images/matrixConfusion.png", caption="Matiz de Confusão", use_column_width=True)
    
    st.markdown("""
                A matriz de confusão acima só salienta mais o que foi dito na analise do classification report.
                """)
    
    st.image("./images/featureImportance.png", caption="Feature Importance", use_column_width=True)

    st.markdown("""
                Agora na feature importance tem-se uma visão das variáveis utilizadas no modelo onde visualmente é possível analisar
                a importância delas para o treinamento e neste caso tem algo bem interessante, apesar dos dados de Introversion Score e 
                Thinking Score não possuirem uma distribuição nem um pouco gaussiana, como observado na analise do dataframe
                foram eles que mais influenciaram na previsão do
                modelo, isso pode estar ocorrendo pois essas duas variáveis estão muito ligadas ao comportamento de todos os tipos
                de personalidades analisadas, mesmo isso não podendo ser visível.
                Exatamente por isso foi escolhido o RandomForest, pois ele é um modelo bem eficaz na captura de padrões complexos.
                """)
    
    st.markdown("""
                Portanto, consigo afirmar que o modelo está bem treinado e acredito até que não tanto envieisado quanto esperava, pois no 
                inicio busquei trabalhar e atacar o problema através de dois modelos definindo dois datasets diferentes, um big e um small,
                que representavam as classes com grande quantidade de amostras e a outra com as menores, porem no fim observei, que o F1 score
                erá bem melhor para todas as classes quando o modelo era treinado de forma geral e não dividida. 
                Também me surpreendi com a analise de feature importance, não esperava que as duas variaveis com comportamentos menos gaussianos
                possíveis no dataset seriam as que mais importavam para a predição do modelo.
                """)
    