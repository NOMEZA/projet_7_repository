import pandas as pd
from flask import Flask
import json
import pandas as pd
import pickle as pk
import numpy as np

with open('../python_preprocessing/finalized_model.pickle', 'rb') as handle:
    model= pk.load(handle)
data_raw=pd.read_csv("../python_preprocessing/data_test_project.csv")
# feature_importances = pd read csv features.csv
data_raw = data_raw.set_index("SK_ID_CURR")
app = Flask(__name__)
df=pd.read_csv("../python_preprocessing/data_useful.csv")
#print(df)
df=df.set_index('SK_ID_CURR') # methode de fixer, transformer une colonne en une clé, on peut accéder la valeur de la ligne par la clé qui est id_client
# comme dictionnaire avec une clé, comme une masque  à une seule valeur mais normalement, le masque est à plusieurs valeurs



@app.route("/get_id_client", methods=['GET'])
def get_id_client():
    return json.dumps({"data":list(data_raw.index)})

@app.route("get_feature_importance", methods=['GET'])
def get_feature_importance():
    name_features = feature_importances["feature"]
    importance_feature = feature_importances["importance"]
    return json.dumps({"feature": list(name_features), "importance": list(importance_feature}))

@app.route("/get_score/<id_client>", methods=['GET']) # c'est mon routeur et on a rendu la route dynamique pour éviter de taper une route de milliers id_client
def get_score(id_client):
    '''
    fonction qui charge le modèle pickle
    il fait une prediction de données de l' id_client
    Args:
        id_client:
    Returns: score du client qui calcule sa solvabilité
    '''
    data_client = data_raw.loc[int(id_client)]
    prediction=model.predict_proba(np.array(data_client).reshape(1, -1))
    prediction_user = list(prediction[0])
    return json.dumps({"id_client": id_client, "prediction": prediction_user}) # erreur sur json.dump, en réalité , je dois remplacer par json.dumps pour qu'il fonctionne

@app.route("/get_info_client/<id_client>", methods=['GET']) # qui visualise les informations du client et les graphiques associés, et qui appelle l’API via une url pour récupérer le score du client
def get_info_client(id_client):
    info_client=df.loc[int(id_client)]   # mon paramètre id_client ne change pas, c'est ma fonction qui change

    return json.dumps({"info_client": info_client.to_dict()}) # on a transformé une serie en dictionnaire erreur sur json.dump, en réalité , je dois r


@app.route("/get_correlation/", methods=['GET']) # analyse bivariée ntre les deux features sélectionnées, avec un dégradé de couleur selon le score des clients, et le positionnement du client
def get_correlation():
    col = ['TARGET', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'DAYS_BIRTH', 'AMT_INCOME_TOTAL', 'AMT_ANNUITY', 'DAYS_EMPLOYED']
    df_column = df[col]
    corr= df_column.corr()
    return json.dumps({"correlation": corr.to_dict()}) # il renvoie une erreur lorsqu'on traduit pas en dict

@app.route("/relevant_features", methods=['GET']) # rappel route est toujours suivi par une df
def relevant_feature():
    cols_relevant = ['DAYS_BIRTH', 'DAYS_EMPLOYED', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'AMT_INCOME_TOTAL', 'AMT_ANNUITY']
    relevant=df[cols_relevant]
    return json.dumps({"relevant": relevant.to_dict()})



if __name__=='__main__': # la logique principale, le coeur principal du fichier qui appelle les autres fichiers à disposition, celui qqui est lancé
    app.run(debug=True)
    print("api start!")


 ###







# @app.route("/get_relation_day_birth_&_target/<id_client>", methods=['GET']) # variable qui influence le score
###


# @app.route("/get_relation_day_birth_&_target/<id_client>", methods=['GET']) # 2 graphiques de features dans une liste déroulante




#@app.route("/get_relation_day_birth_&_target/<id_client>", methods=['GET']) # importance feature globale
    ###