# Protocole expérimental

## Question étudiée

Dans quelle mesure une récupération lexicale, latente ou combinée retrouve-t-elle le passage de référence d'une question BoolQ, et un reranker léger améliore-t-il son ordre ? Un second volet mesure si un classifieur oui/non prédit la réponse à partir du passage placé en tête.

## Corpus, split et ajustement

Les textes des passages constituent le corpus de documents. L'index ne contient ni les réponses ni les étiquettes. La séparation train/validation/test est faite au niveau du titre par une affectation déterministe SHA-256 (70/15/15). BM25, TF-IDF et LSA n'utilisent pas les étiquettes ; la fusion est réglée sur Hit@5 de validation. Le reranker logistique est appris sur un échantillon fixe de 1 600 questions d'entraînement : candidats lexicaux/LSA et passage de référence, avec caractéristiques de scores normalisés et recouvrement du titre. Le lecteur est appris avec la question et son passage de référence, uniquement dans le train.

## Méthodes

- **BM25** : fréquence de termes avec saturation (k_1=1.5), normalisation de longueur (b=0.75).
- **TF-IDF** : unigrammes et bigrammes, fréquence documentaire minimale 2, TF sous-linéaire.
- **LSA** : SVD à 48 dimensions sur la matrice TF-IDF ; cosine sur vecteurs normalisés.
- **Hybride** : combinaison convexe des scores BM25 et TF-IDF après normalisation par maximum ; le coefficient est choisi sur validation.
- **RRF** : fusion des rangs BM25, TF-IDF et LSA, constante (k=60).
- **Reranker** : régression logistique équilibrée sur les candidats issus des trois récupérateurs.
- **Lecteur** : classifieur logistique binaire sur les vecteurs TF-IDF de la concaténation question/passage.

## Mesures et interprétation

Hit@k et Recall@k vérifient la présence du passage associé à la question dans les k premiers résultats ; MRR et nDCG@10 récompensent les rangs plus élevés. Le lecteur est évalué par exactitude, précision, rappel et F1 de la classe « oui ». Le temps de bout en bout est mesuré sur CPU, avec matrices préchargées en mémoire ; il n'inclut ni démarrage, ni construction d'index.

Les mesures sont accompagnées d'intervalles à 95 % par bootstrap de titres et d'un test de permutation signé apparié au niveau titre pour les différences de Hit@5 de RRF et du reranker face à BM25. La procédure est exploratoire et les contrastes sont limités aux deux comparaisons prévues. Les scripts gardent les traces par question, les paramètres et les sorties afin de permettre un réexamen. Il n'est pas permis d'interpréter les résultats comme une comparaison à un LLM génératif ou aux méthodes neurales pré-entraînées.
