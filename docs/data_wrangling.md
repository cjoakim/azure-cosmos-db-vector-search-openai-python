# Data Wrangling

You, the user of this repo, **don't** have to execute this data wrangling
process as the repo already contains file **data/wrangled/documents.json**
for your use.

This documentation page exists simply for your reference, so you can
understand where the raw data came from and how it was processed.


## The Dataset Used : Sean Lahman Baseball Database

The [Sean Lahman Baseball Database](http://seanlahman.com/download-baseball-database/)
is used by this repository, under the [Creative Commons License](https://creativecommons.org/licenses/by-sa/3.0/) 

Several CSV files from this database have been copied to the **data/seanhahman-baseballdatabank-2023.1/**
directory of this repository, and are used as raw-data for the subject in this repo.

#### These are the Sean Lahman CSV files in this repo; the raw data

```
data/seanhahman-baseballdatabank-2023.1/core/Appearances.csv
data/seanhahman-baseballdatabank-2023.1/core/Batting.csv
data/seanhahman-baseballdatabank-2023.1/core/People.csv
data/seanhahman-baseballdatabank-2023.1/core/Pitching.csv
```

#### Appearances.csv

```
yearID,teamID,lgID,playerID,G_all,GS,G_batting,G_defense,G_p,G_c,G_1b,G_2b,G_3b,G_ss,G_lf,G_cf,G_rf,G_of,G_dh,G_ph,G_pr
...
1954,ML1,NL,aaronha01,122,113,122,116,0,0,0,0,0,0,105,0,11,116,0,7,1
```

#### People.csv

```
playerID,birthYear,birthMonth,birthDay,birthCountry,birthState,birthCity,deathYear,deathMonth,deathDay,deathCountry,deathState,deathCity,nameFirst,nameLast,nameGiven,weight,height,bats,throws,debut,finalGame,retroID,bbrefID
...
aaronha01,1934,2,5,USA,AL,Mobile,2021,1,22,USA,GA,Atlanta,Hank,Aaron,Henry Louis,180,72,R,R,1954-04-13,1976-10-03,aaroh101,aaronha01
...
guidrro01,1950,8,28,USA,LA,Lafayette,,,,,,,Ron,Guidry,Ronald Ames,161,71,L,L,1975-07-27,1988-09-27,guidr001,guidrro01
...
```

#### Batting.csv

```
playerID,yearID,stint,teamID,lgID,G,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,IBB,HBP,SH,SF,GIDP
aaronha01,1955,1,ML1,NL,153,602,105,189,37,9,27,106,3,1,49,61,5,3,7,4,20
...
```

#### Pitching.csv

```
playerID,yearID,stint,teamID,lgID,W,L,G,GS,CG,SHO,SV,IPouts,H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,SF,GIDP
guidrro01,1975,1,NYA,AL,0,1,10,1,0,0,0,47,15,6,0,9,15,0.259,3.45,0,1,1,0,69,6,6,0,1,0
...
```

---

### Wrangled JSON Documents, with calculated fields and embeddings_str

See file **data/wrangled/documents.json**

This is the document for **Hank Aaron**.  Notice that the document contains
raw and aggregated data from the three CSV files, and calculated fields based
on this aggregated data.  The Python **pandas** library was used to do much
of the aggregation; it could also be done with **Spark** as this Python
code is portable to Notebooks.

There is also a computed attribute called **embeddings_str** which contains
**"binned"** text words for the most pertinent player statistics.
For example, the embeddings_str value contains **batting_avg_305**, calculated from
"batting_avg" value 0.30499838240051763.

#### Digression: Machine Learning "Features" vs Text-Based Vectorization

Traditional Machine Learning typically uses normalized floating-point columns
for each feature.  The values are normalized to be in the range from zero to 1.

The approach taken in this project is to instead create text "words" containing
"binned" values **since embeddings are calculated from text values**.

**This value will be passed to OpenAI for vectorization (i.e. - embedding)**

```
  "aaronha01": {
    "playerID": "aaronha01",
    "birthYear": 1934,
    "birthCountry": "USA",
    "deathYear": "2021.0",
    "nameFirst": "Hank",
    "nameLast": "Aaron",
    "weight": 180,
    "height": 72,
    "bats": "R",
    "throws": "R",
    "debut": "1954-04-13",
    "finalGame": "1976-10-03",
    "teams": {
      "total_games": 3298,
      "teams": {
        "ML1": 1806,
        "ATL": 1270,
        "ML4": 222
      },
      "primary_team": "ML1"
    },
    "primary_position": "RF",
    "batting": {
      "G": "3298",
      "AB": "12364",
      "R": "2174",
      "H": "3771",
      "2B": "624",
      "3B": "98",
      "HR": "755",
      "RBI": "2297.0",
      "SB": "240.0",
      "CS": "73.0",
      "BB": "1402",
      "SO": "1383.0",
      "IBB": "293.0",
      "HBP": "32.0",
      "SF": "121.0",
      "calculated": {
        "runs_per_ab": 0.17583306373341961,
        "batting_avg": 0.30499838240051763,
        "2b_avg": 0.050469103849886766,
        "3b_avg": 0.007926237463604012,
        "hr_avg": 0.06106438045939825,
        "rbi_avg": 0.18578130054998382,
        "bb_avg": 0.11339372371400841,
        "so_avg": 0.11185700420575866,
        "ibb_avg": 0.023697832416693626,
        "hbp_avg": 0.002588159171789065
      }
    },
    "category": "fielder",
    "debut_year": 1954,
    "final_year": 1976,
    "embeddings_str": "fielder primary_position_rf total_games_3298 bats_r throws_r hits_3771 hr_755 batting_avg_305 runs_per_ab_176 2b_avg_50 3b_avg_8 hr_avg_61 rbi_avg_186 bb_avg_113 so_avg_112 ibb_avg_24 hbp_avg_3"
  }
```

Note that the **calculated** values are **normalized** to floating-point numbers
between 0 and 1.  This is how one typically creates **features** for **machine learning**.

The **embeddings_str** contains **text words** designed to be used to measure
the relatedness of the baseball players.

In the [Data Vectorization](data_vectorization.md) section of this project you will
vectorize these **embeddings_str** values for each document.

---

## Execute the Data Wrangling Process

Follow these steps:

```
> cd data_wrangling

> .\venv.ps1                  

> .\venv\Scripts\activate

> mkdir tmp

> .\bb_wrangle.ps1
```

The last script creates file **/data/wrangled/documents.json** in this repo,
which is used as the input to the vectorization process.

---

## Next

[Data Vectorization](data_vectorization.md)
