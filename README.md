# RAGNova

Prototype de recherche documentaire et de question-réponse binaire sur BoolQ. Le système classe des passages avec six méthodes et un lecteur TF-IDF/logistique répond « oui » ou « non ». Il ne génère pas de réponses en prose.

## Dossiers

- `01_Rapport/` : rapport Word et PDF.
- `02_Presentation/` : présentation PowerPoint et PDF.
- `03_Dataset/` : données sources et script de préparation.
- `04_Experiments/` : scripts, données préparées, résultats et modèles.
- `05_Application/` : application Streamlit, pipeline et vérifications.
- `06_Documentation/` : méthodologie, reproductibilité et notes de soutenance.
- `07_Captures/` : captures de l’application.

## Installer et lancer sous Windows

Utiliser Python 3.12 en 64 bits. Depuis PowerShell, à la racine du projet :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run 05_Application\app.py
```

On peut aussi lancer `lancer_windows.bat`. L’application s’ouvre sur `http://localhost:8501`.

## Vérifications

Lancer les quatre tests unitaires :

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s 05_Application -v
```

Comparer ensuite les résultats aux traces archivées :

```powershell
.\.venv\Scripts\python.exe 05_Application\verify_pipeline.py 2083
```

Les quatre tests unitaires et l’exécution Streamlit ont été vérifiés sous Windows. La comparaison stricte aux traces archivées peut toutefois diverger selon la plateforme lorsque plusieurs passages ont le même score : le tri top-k utilise NumPy et les égalités ne sont pas départagées explicitement. RRF et le reranker peuvent aussi hériter de ces écarts dans leurs listes de candidats. Les métriques archivées dans `04_Experiments/results/metrics.json` ne sont pas recalculées par l’application.

## Méthodes présentes

Le pipeline compare BM25, TF-IDF, LSA (SVD à 48 dimensions), fusion pondérée BM25/TF-IDF, RRF et reranking logistique. Le reranker combine quatre signaux. L’application comprend aussi un lecteur binaire TF-IDF/logistique. Les encodeurs neuronaux, cross-encodeurs et modèles génératifs cités dans le rapport sont des pistes théoriques, pas des composants exécutés.

Pour reproduire les expériences depuis les données brutes :

```powershell
.\.venv\Scripts\python.exe 03_Dataset\prepare_data.py
.\.venv\Scripts\python.exe 04_Experiments\run_experiments.py
.\.venv\Scripts\python.exe 04_Experiments\statistical_analysis.py
```

Ces commandes régénèrent les données et résultats sous `04_Experiments/`. Les résultats archivés sont remplacés. Les dépendances sont épinglées dans `requirements.txt`.
