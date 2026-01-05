# LABORATOIRES D'INGÉNIERIE BIG DATA

[![Hadoop](https://img.shields.io/badge/Hadoop-3.2.0-yellow?logo=apache-hadoop)](https://hadoop.apache.org/)
[![Spark](https://img.shields.io/badge/Apache%20Spark-3.5.1-orange?logo=apache-spark)](https://spark.apache.org/)
[![Java](https://img.shields.io/badge/Java-8-red?logo=java)](https://www.java.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)

---

## Présentation Générale

Ce dépôt contient une collection de laboratoires Big Data réalisés dans le cadre de mon cursus en ingénierie Data Science & Business Intelligence.

Les travaux couvrent les fondamentaux de l'écosystème Big Data, notamment :

* Hadoop & HDFS
* MapReduce (Java & Python Streaming)
* Apache Spark & Spark SQL
* Analyse de données à grande échelle

Chaque laboratoire est accompagné de scripts exécutables, de commandes documentées et d'une approche pédagogique progressive.

---

## Structure du Projet

```
BIGDATA_ENGINEERING_LABS/
├── hadoop_lab0_2/                 # Opérations Hadoop de base (HDFS)
│   ├── HadoopFileStatus.java
│   ├── ReadHDFS.java
│   ├── HDFSWrite.java
│   ├── pom.xml
│   └── commands.sh
│
├── lab3_mapreduce/                # MapReduce Java & Python Streaming
│   ├── WordCount.java
│   ├── pom.xml
│   ├── mapper.py
│   ├── reducer.py
│   └── run_lab3.sh
│
├── lab4_spark_sql/                # Analyse avec Apache Spark SQL
│   ├── data/
│   │   └── results.csv
│   ├── spark_sql_analysis.py
│   └── README.md
│
└── README.md
```

---

## Lab 0–2 : Opérations Hadoop de Base (HDFS)

Ces laboratoires démontrent l'interaction avec HDFS à l'aide de programmes Java.

### Exemples d'Exécution

#### Affichage du statut des fichiers HDFS

```bash
hadoop jar HadoopFileStatus.jar /user/root/input purchases.txt achats.txt
```

Affiche les métadonnées (taille, permissions, réplication, date).

#### Lecture d'un fichier HDFS

```bash
hadoop jar ReadHDFS.jar /user/root/input/achats.txt
```

#### Écriture dans HDFS

```bash
hadoop jar HDFSWrite.jar /input/bonjour.txt "Bonjour depuis HDFSWrite"
```

---

## Lab 3 : WordCount avec MapReduce

Comparaison de deux implémentations du classique WordCount :

* MapReduce Java (compilé)
* Hadoop Streaming avec Python

### Java MapReduce

```bash
hadoop jar WordCount.jar input output
```

### Python Streaming

```bash
hadoop jar hadoop-streaming.jar \
  -files mapper.py,reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input input \
  -output output_py
```

---

## Lab 4 : Analyse de Données avec Apache Spark SQL

### Objectif

Se familiariser avec l'API Spark SQL pour l'analyse analytique et statistique de données sportives à grande échelle.

### Dataset

* 44 341 matchs internationaux
* Période : 1872 – 2022
* Compétitions : Coupe du Monde FIFA, amicaux, tournois officiels
* Matchs internationaux masculins uniquement

### Analyses Réalisées

* Requêtes SQL simples (COUNT, GROUP BY, ORDER BY)
* Agrégations avancées
* Fonctions analytiques (ROW_NUMBER, fenêtres)
* Comparaisons domicile / extérieur
* Séries de victoires et goal average

### Exécution

```bash
python spark_sql_analysis.py
```

### Technologies

* Apache Spark 3.5.1
* PySpark
* Spark SQL
* Mode local (sans Hadoop)

---

## Comparaison des Approches Big Data

| Technologie | Usage principal    | Points forts               |
| ----------- | ------------------ | -------------------------- |
| Hadoop HDFS | Stockage distribué | Fiabilité                  |
| MapReduce   | Traitement batch   | Scalabilité                |
| Spark SQL   | Analyse analytique | Performance & expressivité |

---

## Technologies Utilisées

* Apache Hadoop 3.2.0
* Apache Spark 3.5.1
* Java 8
* Python 3
* Maven
* Docker (cluster Hadoop)

---

## Auteur

**Omar LARAJE**

Étudiant Ingénieur en Data Science & Business Intelligence

Intéressé par le Big Data, l'Analytics et l'Intelligence Artificielle

GitHub : [https://github.com/omarlr-pro](https://github.com/omarlr-pro)

LinkedIn : [https://www.linkedin.com/in/omar-laraje-998827233/](https://www.linkedin.com/in/omar-laraje-998827233/)