# CF Book Recommendation API

This is a simple book recommendation API built with FastAPI. It provides two endpoints:

- `/popular`: Returns a list of popular books loaded from a pickled Pandas DataFrame (`popular.pkl`). The DataFrame is cached with an LRU cache for performance.
- `/recommend`: Provides personalized book recommendations based on the input book title. It uses pre-calculated book similarity scores stored in pickled DataFrames (`pt.pkl`, `similarity_scores.pkl`, `books.pkl`) and caches them in memory.

## Recommendation Process

The recommendation works by:
1. Finding the index of the input book title in the `pt_df`.
2. Getting the most similar books based on the similarity scores.
3. Looking up book info from the `books_df`.
4. Returning a list of recommended books with title, author, and image URL.

The data files and recommendation function are cached with an LRU cache for performance.

## Built With

- FastAPI
- Pandas
- Numpy

## Requirements

- Python 3.6+
- FastAPI
- Pandas
- Numpy
- Mangum

## Usage

Run with Uvicorn:

```bash
uvicorn main:app --reload
```

Try the endpoints:
```bash
GET /popular
POST /recommend
Body: {"book_name": "The Great Gatsby"}
```

## Deployment
To deploy the API to AWS Lambda:

1) organise dependencies:
```bash
pip3 install -t dep -r requirements.txt
```
2) Package the dependencies:
```bash
(cd dep; zip ../lambda_artifact.zip -r .)
```

3) Update the main script in the artifact:
```bash
zip lambda_artifact.zip -u main.py
```

The Mangum handler makes it easy to deploy the API to AWS Lambda.
* make sure to change aws runtime hander to `main.handler`