import dash
import plotly.express as px
import dash_html_components as html
import dash_table

app=dash.Dash()
app.layout = html.Div([
    html.Div(html.H1(children="Hello world"))
])
if __name__=='__main__':
    app.run_server(debug=True)
    print("api start!")

# Explication if __name__ ='__main__
# Chaque fois que l'interpréteur Python lit un fichier source, il fait deux choses :
# il définit quelques variables spéciales comme __name__, puis
# il exécute tout le code trouvé dans le fichier.
# Voyons comment cela fonctionne et comment cela se rapporte à votre question sur les __name__vérifications que nous voyons toujours dans les scripts Python.
# Exemple de code
# Utilisons un exemple de code légèrement différent pour explorer le fonctionnement des importations et des scripts. Supposons que ce qui suit se trouve dans un fichier nommé foo.py.
