# Reproductibilité

## Préparation

L'archive Kaggle de version 2 est incluse dans `03_Dataset/raw`. Vérifier son empreinte SHA-256, puis exécuter :

```bash
python 03_Dataset/prepare_data.py
python 04_Experiments/run_experiments.py
python 04_Experiments/statistical_analysis.py
```

La graine est 20261114. Les données préparées, paramètres, agrégats, réglage de validation, modèle et traces individuelles sont écrits sous `04_Experiments/`.

## Interface

```bash
pip install -r requirements.txt
streamlit run 05_Application/app.py
```

L'interface charge les artefacts sauvegardés par l'expérience. Pour reconstruire les résultats depuis les données brutes, exécuter les trois scripts de préparation, d'expérience et d'analyse dans l'ordre indiqué plus haut. L'application propose une vue d'ensemble, une recherche interactive, l'exploration des méthodes, un laboratoire de reranking, les résultats, l'analyse d'erreurs et les informations d'équipe.

## Contrôles de l'application

Sous Windows avec l'environnement Python 3.12 livré, les quatre tests unitaires passent et l'application Streamlit se charge sans exception. La vérification stricte de 2 083 traces peut toutefois retourner un code d'échec entre plateformes : les égalités de score dans le tri top-k ne sont pas départagées explicitement, et les sélections différentes peuvent se propager au RRF et au reranker. Les fichiers de résultats archivés restent inchangés ; l'application lit les métriques depuis ces fichiers.

## Environnement et limites de reproduction

La construction a utilisé Python 3.12, scikit-learn, NumPy, SciPy, pandas et joblib. Le calcul a été exécuté sur CPU. Le fichier `rag_nova_models.joblib` est un artefact pratique pour la démonstration, tandis que les scripts restent la référence de reproduction. La version précise des bibliothèques et les métriques sont consignées dans les fichiers de résultats.

Les composants MiniLM, CrossEncoder, LambdaMART/LightGBM et FLAN-T5 ne sont pas installés ni évalués ici. Leur mention dans les diapositives ou le rapport est limitée aux fondements théoriques et aux perspectives ; leurs performances ne sont jamais chiffrées.
