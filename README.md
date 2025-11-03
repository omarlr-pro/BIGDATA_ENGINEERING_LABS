# LABORATOIRES D'INGÉNIERIE BIG DATA

Ce dépôt contient une collection de laboratoires Hadoop et d'exercices MapReduce développés dans le cadre de mon cursus en ingénierie .  
Chaque laboratoire explore les concepts fondamentaux de l'écosystème Hadoop — des opérations de fichiers de base à l'implémentation de MapReduce en Java et Python.

---

## Structure du Projet

```
BIGDATA_ENGINEERING_LABS/
├── hadoop_lab0_2/                 # Opérations Hadoop de base
│   ├── HadoopFileStatus.java
│   ├── ReadHDFS.java
│   ├── HDFSWrite.java
│   ├── pom.xml
│   └── commands.sh
│
├── lab3_mapreduce/         # Implémentation MapReduce (Java + Python)
│   ├── WordCount.java
│   ├── pom.xml
│   ├── mapper.py
│   ├── reducer.py
│   └── run_lab3.sh
│
└── README.md
```

---

## Lab 0–2 : Opérations Hadoop de Base

Ces laboratoires démontrent l'interaction avec HDFS (Hadoop Distributed File System) à l'aide de programmes Java.

### Exécutions JAR Java

#### Commande 1 : Afficher le Statut des Fichiers dans HDFS
```bash
hadoop jar /shared_volume/hadoop_lab-1.0-SNAPSHOT-HadoopFileStatus.jar /user/root/input purchases.txt achats.txt
```
**Objectif :** Cette commande exécute l'application Java HadoopFileStatus pour récupérer et afficher les métadonnées des fichiers spécifiés stockés dans HDFS, incluant la taille, les permissions, le facteur de réplication et la date de dernière modification.

#### Commande 2 : Lire un Fichier depuis HDFS
```bash
hadoop jar /shared_volume/hadoop_lab-1.0-SNAPSHOT-ReadHDFS.jar /user/root/input/achats.txt
```
**Objectif :** Cette commande exécute l'application Java ReadHDFS pour lire et afficher le contenu du fichier `achats.txt` stocké dans le répertoire HDFS `/user/root/input`.

#### Commande 3 : Écrire du Texte dans HDFS
```bash
hadoop jar /shared_volume/hadoop_lab-1.0-SNAPSHOT-HDFSWrite.jar /input/bonjour.txt "Bonjour depuis HDFSWrite"
```
**Objectif :** Cette commande exécute l'application Java HDFSWrite pour créer un nouveau fichier nommé `bonjour.txt` dans le répertoire HDFS `/input` et y écrire le texte "Bonjour depuis HDFSWrite".

---

## Lab 3 : WordCount avec MapReduce

Ce laboratoire compare deux implémentations de l'algorithme WordCount :
- Java MapReduce (JAR compilé)
- Python Hadoop Streaming (scripts mapper/reducer)

### Exécution Java MapReduce

```bash
#!/bin/bash

# Nettoyer les sorties précédentes
hdfs dfs -rm -r /user/root/output /user/root/output_py 2>/dev/null

# Exécuter WordCount en Java
hadoop jar /shared_volume/WordCount.jar /user/root/input/achats.txt /user/root/output

# Afficher les 20 premiers résultats
hdfs dfs -cat /user/root/output/part-r-00000 | head -20
```

**Explication des Commandes :**

1. **`hdfs dfs -rm -r /user/root/output /user/root/output_py 2>/dev/null`**  
   Supprime les répertoires de sortie existants pour éviter les conflits. Le `2>/dev/null` supprime les messages d'erreur si les répertoires n'existent pas.

2. **`hadoop jar /shared_volume/WordCount.jar /user/root/input/achats.txt /user/root/output`**  
   Exécute l'application Java MapReduce WordCount compilée. Elle lit le fichier d'entrée `achats.txt`, compte les occurrences de mots et écrit les résultats dans le répertoire `/user/root/output`.

3. **`hdfs dfs -cat /user/root/output/part-r-00000 | head -20`**  
   Affiche les 20 premières lignes du fichier de sortie MapReduce, montrant les comptes de mots au format `mot nombre`.

### Exécution Python Streaming

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.0.jar \
  -files /shared_volume/mapper.py,/shared_volume/reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /user/root/input/achats.txt \
  -output /user/root/output_py

# Afficher les dernières lignes de sortie
hdfs dfs -cat /user/root/output_py/part-00000 | tail -20
```

**Explication des Commandes :**

1. **`hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.0.jar`**  
   Invoque l'utilitaire Hadoop Streaming, qui permet l'exécution de jobs MapReduce en utilisant n'importe quel script exécutable (Python, Perl, etc.).

2. **`-files /shared_volume/mapper.py,/shared_volume/reducer.py`**  
   Distribue les scripts Python mapper et reducer à tous les nœuds du cluster pour exécution.

3. **`-mapper "python3 mapper.py"`**  
   Spécifie la commande pour exécuter le script mapper, qui traite les données d'entrée et émet des paires clé-valeur.

4. **`-reducer "python3 reducer.py"`**  
   Spécifie la commande pour exécuter le script reducer, qui agrège les sorties du mapper et produit les résultats finaux.

5. **`-input /user/root/input/achats.txt`**  
   Définit le chemin du fichier d'entrée dans HDFS.

6. **`-output /user/root/output_py`**  
   Définit le répertoire de sortie où les résultats seront stockés.

7. **`hdfs dfs -cat /user/root/output_py/part-00000 | tail -20`**  
   Affiche les 20 dernières lignes du fichier de sortie, montrant les résultats finaux du comptage de mots.

---

## Comparaison : Java vs Python Streaming

| **Critère**              | **Java MapReduce**              | **Python Streaming**              |
|--------------------------|---------------------------------|-----------------------------------|
| **Type de Code**         | Compilé                         | Interprété                        |
| **Performance**          | Rapide et optimisé              | Plus lent sur grands ensembles    |
| **Facilité d'Usage**     | Plus complexe à implémenter     | Simple et léger                   |
| **Outil d'Exécution**    | `hadoop jar`                    | `hadoop-streaming.jar`            |
| **Langage**              | Java                            | Python                            |

---

## Technologies Utilisées

- Hadoop 3.2.0
- Java 8
- Python 3
- Maven
- Cluster Hadoop Docker

---

## Auteur

**Omar LARAJE**  
Étudiant Ingénieur en Data Science & Business Intelligence
