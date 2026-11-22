# Guide oral — 27 diapositives

Les notes suivent l'ordre du modèle fourni. Les valeurs expérimentales sont reprises du fichier `04_Experiments/results/metrics.json` et doivent être présentées comme un test interne BoolQ.

1. Présenter le sujet, les quatre membres et l'établissement.
2. Annoncer le fil : problème, méthodes, données, évaluation, résultats puis démonstration.
3. Expliquer pourquoi une recherche contextuelle peut limiter les réponses non sourcées, sans prétendre éliminer l'hallucination.
4. Lire la question de recherche et distinguer hypothèses de résultats.
5. Décrire indexation hors-ligne, requête, récupération, reranking et décision binaire.
6. Décomposer BM25 : rareté du terme, fréquence et longueur du passage.
7. Opposer représentation TF-IDF aux vecteurs latents LSA ; préciser que LSA est ici exécuté.
8. Comparer fusion de scores et fusion de rangs RRF.
9. Expliquer l'apprentissage du reranker à partir des candidats, positifs et négatifs.
10. Définir Hit@k, MRR, nDCG et les métriques de classification.
11. Présenter la provenance BoolQ, sa licence et ses splits.
12. Signaler l'équilibre des réponses et la variété des titres.
13. Décrire normalisation, déduplication et séparation par titre.
14. Résumer les six stratégies de récupération comparées.
15. Montrer les cinq couches : données, retrieval, reranking, lecteur, système.
16. Rapporter les résultats des baselines avec les valeurs mesurées.
17. Comparer lexical, LSA et approche combinée.
18. Présenter RRF sans extrapoler au-delà de la mesure obtenue.
19. Montrer l'effet du reranker sur Hit@k et MRR.
20. Expliquer le compromis profondeur/latence à partir des mesures disponibles.
21. Décrire les caractéristiques du reranker, sans inventer d'analyse causale.
22. Examiner les erreurs par question, prédiction et passage remonté.
23. Présenter le déploiement local Streamlit et les artefacts reproductibles.
24. Démontrer une question, changer de méthode et ouvrir les preuves.
25. Répondre aux hypothèses au moyen des résultats et limites.
26. Conclure : récupération mesurée, lecteur binaire, extensions neurales non évaluées.
27. Remercier et inviter aux questions.
