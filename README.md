# AI Review Analytics — Product Sentiment Pipeline

A cloud-native data engineering pipeline that ingests mobile phone reviews,
runs sentiment analysis using Azure AI Language, and surfaces product ratings
through a Power BI dashboard.

> This project is a modern reimagination of a sentiment analysis system 
> originally published at IEEE ICEEOT 2016. The original system used Twitter 
> data, SVM classifiers, and lexicon-based dictionaries to rate mobile phones. 
> This version rebuilds the same core idea using current cloud-native 
> engineering practices on Microsoft Azure and Microsoft Fabric.

## Architecture
Raw Reviews (Kaggle CSV)
→
Bronze Layer — Raw file landing (ADLS / Fabric Lakehouse)
→
Silver Layer — Cleaned & transformed (PySpark notebooks)
→
Gold Layer — Sentiment scored (Azure AI Language) + Aggregated ratings
→
Power BI Dashboard — Overall & per-brand product ratings

## Tech Stack

| Layer | Technology |
|---|---|
| Storage | Azure Data Lake Storage / Microsoft Fabric Lakehouse |
| Transformation | PySpark (Microsoft Fabric Notebooks) |
| Sentiment Analysis | Azure AI Language (managed cognitive service) |
| Orchestration | Microsoft Fabric Data Pipelines |
| Serving | Power BI |
| Version Control | GitHub |

## Dataset

Amazon Unlocked Mobile Phones reviews dataset (Kaggle / PromptCloud).
~413,840 reviews across multiple brands with columns: Product Name, 
Brand Name, Price, Rating (1-5 stars), Review text, Review Votes.

The existing star Rating column serves as ground truth to validate 
sentiment model output — reviews scored as "positive" by Azure AI 
Language should correlate strongly with 4-5 star ratings.

## Pipeline Stages

### Bronze — Raw Ingestion
Raw CSV uploaded into Fabric Lakehouse Files section. No transformation 
at this layer — data lands exactly as received from source.

### Silver — Cleaning & Transformation
PySpark notebook reads raw CSV, removes nulls/duplicates, normalizes 
text (lowercase, trim whitespace), selects relevant columns, writes 
output as a Delta table (`silver_reviews`).

### Gold — Sentiment Scoring & Aggregation
Azure AI Language API scores each review as positive/negative/neutral 
with a confidence score. Results aggregated by brand and product to 
produce overall sentiment ratings. Validated against actual star ratings.

### Serving — Power BI Dashboard
Live-connected Power BI report showing:
- Overall sentiment score by brand
- Sentiment vs actual star rating comparison
- Review volume by price range
- Top/bottom rated products

## Design Decisions

- **Lakehouse over Warehouse** — needed to land raw unstructured text 
  files before transformation; a Warehouse alone only accepts structured 
  SQL inserts
- **Azure AI Language over custom model** — using a managed cognitive 
  service is the correct production engineering decision; avoids 
  maintaining a custom model when a pretrained one exceeds requirements
- **Sampled dataset for scoring** — full 413k rows scored against the 
  Azure AI Language API would incur unnecessary cost at this scale; 
  5,000 row sample used for sentiment scoring while full dataset used 
  for Bronze/Silver transformation steps
- **Delta tables for Silver/Gold** — Delta format gives ACID transactions,
  schema enforcement, and time travel; critical for reliable pipeline runs

## Project Status

| Stage | Status |
|---|---|
| Bronze ingestion | Complete |
| Silver cleaning | In progress |
| Gold sentiment scoring | In progress |
| Power BI dashboard | In progress |
| Pipeline orchestration | In progress |

## Author

Minara P Anto

MEng Student (University of Waterloo) | Aspiring Azure Data Engineer

Co-author: "Product Rating Using Sentiment Analysis", IEEE ICEEOT 2016
