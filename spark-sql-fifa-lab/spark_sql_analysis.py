from pyspark.sql import SparkSession

# =========================
# 1. Spark Session
# =========================
spark = SparkSession.builder \
    .appName("FIFA World Cup Spark SQL Lab") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# =========================
# 2. Load Dataset
# =========================
df = spark.read.option("header", True) \
               .option("inferSchema", True) \
               .csv("data/results.csv")

df.createOrReplaceTempView("matches")

print("\nSchema:")
df.printSchema()

print("\nSample data:")
df.show(5)

# =========================
# PART 1 — Découverte & requêtes simples
# =========================

print("\n1. Total number of matches")
spark.sql("""
SELECT COUNT(*) AS total_matches
FROM matches
""").show()

print("\n2. First and last year")
spark.sql("""
SELECT MIN(YEAR(date)) AS first_year,
       MAX(YEAR(date)) AS last_year
FROM matches
""").show()

print("\n3. Top 10 most frequent tournaments")
spark.sql("""
SELECT tournament, COUNT(*) AS nb_matches
FROM matches
GROUP BY tournament
ORDER BY nb_matches DESC
LIMIT 10
""").show()

print("\n4. Matches played on neutral ground")
spark.sql("""
SELECT COUNT(*) AS neutral_matches
FROM matches
WHERE neutral = true
""").show()

print("\n5. Top 10 host countries")
spark.sql("""
SELECT country, COUNT(*) AS nb_matches
FROM matches
GROUP BY country
ORDER BY nb_matches DESC
LIMIT 10
""").show()

print("\n6. Matches ending in a draw")
spark.sql("""
SELECT COUNT(*) AS draws
FROM matches
WHERE home_score = away_score
""").show()

print("\n7. Matches with total score > 6")
spark.sql("""
SELECT date, home_team, away_team, home_score, away_score,
       (home_score + away_score) AS total_goals
FROM matches
WHERE (home_score + away_score) > 6
ORDER BY total_goals DESC
""").show()

# =========================
# PART 2 — Agrégations & statistiques
# =========================

print("\n8. Total matches played by each team")
spark.sql("""
SELECT team, COUNT(*) AS total_matches
FROM (
    SELECT home_team AS team FROM matches
    UNION ALL
    SELECT away_team AS team FROM matches
)
GROUP BY team
ORDER BY total_matches DESC
""").show()

print("\n9. Top 10 teams by goals scored")
spark.sql("""
SELECT team, SUM(goals) AS total_goals
FROM (
    SELECT home_team AS team, home_score AS goals FROM matches
    UNION ALL
    SELECT away_team AS team, away_score AS goals FROM matches
)
GROUP BY team
ORDER BY total_goals DESC
LIMIT 10
""").show()

print("\n10. Average goals per match by decade")
spark.sql("""
SELECT (YEAR(date) DIV 10) * 10 AS decade,
       AVG(home_score + away_score) AS avg_goals
FROM matches
GROUP BY (YEAR(date) DIV 10) * 10
ORDER BY decade
""").show()

print("\n11. Matches per tournament per year")
spark.sql("""
SELECT tournament,
       YEAR(date) AS year,
       COUNT(*) AS nb_matches
FROM matches
GROUP BY tournament, YEAR(date)
ORDER BY tournament, year
""").show()

print("\n12. Home wins ranking")
spark.sql("""
SELECT home_team, COUNT(*) AS home_wins
FROM matches
WHERE home_score > away_score
GROUP BY home_team
ORDER BY home_wins DESC
""").show()

print("\n13. Wins, draws and losses per team")
spark.sql("""
SELECT team,
       SUM(win) AS wins,
       SUM(draw) AS draws,
       SUM(loss) AS losses
FROM (
    SELECT home_team AS team,
           CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS win,
           CASE WHEN home_score = away_score THEN 1 ELSE 0 END AS draw,
           CASE WHEN home_score < away_score THEN 1 ELSE 0 END AS loss
    FROM matches
    UNION ALL
    SELECT away_team AS team,
           CASE WHEN away_score > home_score THEN 1 ELSE 0 END,
           CASE WHEN away_score = home_score THEN 1 ELSE 0 END,
           CASE WHEN away_score < home_score THEN 1 ELSE 0 END
    FROM matches
)
GROUP BY team
ORDER BY wins DESC
""").show()

print("\n14. Average score: neutral vs non-neutral")
spark.sql("""
SELECT neutral,
       AVG(home_score + away_score) AS avg_score
FROM matches
GROUP BY neutral
""").show()

print("\n15. Top 5 matches with highest goal difference")
spark.sql("""
SELECT date, home_team, away_team,
       home_score, away_score,
       ABS(home_score - away_score) AS goal_diff
FROM matches
ORDER BY goal_diff DESC
LIMIT 5
""").show()

# =========================
# PART 3 — Requêtes analytiques (fenêtres)
# =========================

print("\n16. Goal average per team")
spark.sql("""
SELECT team,
       SUM(scored) - SUM(conceded) AS goal_average
FROM (
    SELECT home_team AS team,
           home_score AS scored,
           away_score AS conceded
    FROM matches
    UNION ALL
    SELECT away_team,
           away_score,
           home_score
    FROM matches
)
GROUP BY team
ORDER BY goal_average DESC
""").show()

print("\n17. Ranking teams by wins per year")
spark.sql("""
SELECT year, team, wins,
       ROW_NUMBER() OVER (PARTITION BY year ORDER BY wins DESC) AS rank
FROM (
    SELECT YEAR(date) AS year, home_team AS team, COUNT(*) AS wins
    FROM matches
    WHERE home_score > away_score
    GROUP BY YEAR(date), home_team
)
ORDER BY year, rank
""").show()

print("\n18. Matches evolution by decade")
spark.sql("""
SELECT (YEAR(date) DIV 10) * 10 AS decade,
       COUNT(*) AS nb_matches
FROM matches
GROUP BY (YEAR(date) DIV 10) * 10
ORDER BY decade
""").show()

print("\n19. Unbeaten teams per year")
spark.sql("""
SELECT team, year
FROM (
    SELECT team, year, SUM(loss) AS losses
    FROM (
        SELECT home_team AS team, YEAR(date) AS year,
               CASE WHEN home_score < away_score THEN 1 ELSE 0 END AS loss
        FROM matches
        UNION ALL
        SELECT away_team, YEAR(date),
               CASE WHEN away_score < home_score THEN 1 ELSE 0 END
        FROM matches
    )
    GROUP BY team, year
)
WHERE losses = 0
ORDER BY year
""").show()

print("\n20. Longest winning streak per team")
spark.sql("""
WITH results AS (
    SELECT date, team,
           CASE WHEN win = 1 THEN 1 ELSE 0 END AS win
    FROM (
        SELECT date, home_team AS team,
               CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS win
        FROM matches
        UNION ALL
        SELECT date, away_team AS team,
               CASE WHEN away_score > home_score THEN 1 ELSE 0 END
        FROM matches
    )
),
groups AS (
    SELECT *,
           SUM(CASE WHEN win = 0 THEN 1 ELSE 0 END)
           OVER (PARTITION BY team ORDER BY date) AS grp
    FROM results
)
SELECT team, MAX(streak) AS longest_win_streak
FROM (
    SELECT team, grp, COUNT(*) AS streak
    FROM groups
    WHERE win = 1
    GROUP BY team, grp
)
GROUP BY team
ORDER BY longest_win_streak DESC
""").show()

print("\n21. Most successful team per tournament")
spark.sql("""
SELECT tournament, team, wins
FROM (
    SELECT tournament, team, COUNT(*) AS wins,
           ROW_NUMBER() OVER (PARTITION BY tournament ORDER BY COUNT(*) DESC) AS rank
    FROM (
        SELECT tournament, home_team AS team
        FROM matches
        WHERE home_score > away_score
    )
    GROUP BY tournament, team
)
WHERE rank = 1
""").show()

print("\n22. Home vs away performance per team")
spark.sql("""
SELECT team,
       SUM(home_wins) AS home_wins,
       SUM(away_wins) AS away_wins
FROM (
    SELECT home_team AS team,
           CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS home_wins,
           0 AS away_wins
    FROM matches
    UNION ALL
    SELECT away_team,
           0,
           CASE WHEN away_score > home_score THEN 1 ELSE 0 END
    FROM matches
)
GROUP BY team
ORDER BY home_wins DESC
""").show()

# =========================
# End
# =========================
spark.stop()
