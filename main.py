from fastapi import FastAPI
import pandas as pd
import numpy as np
from json import loads
from functools import lru_cache

app = FastAPI()

# popular-df loading function
@lru_cache(maxsize=128, typed=False)
def load_df():
    try:
        df = pd.read_pickle('popular.pkl')
        # Convert DataFrame to JSON orient='records' 
        json_data = df.to_json(orient="records")
        parsed = loads(json_data)
        return parsed 
    
    except FileNotFoundError:
        print('pickle file not found.')
        
    except Exception as e:
        print('Error loading pickle file.')

# model files and caching function
@lru_cache(maxsize=128)
def load_model_files():
    try:
        pt_df = pd.read_pickle('pt.pkl')
        similarity_df = pd.read_pickle('similarity_scores.pkl')
        books_df = pd.read_pickle('books.pkl')

        return pt_df, similarity_df,books_df
        
    except FileNotFoundError:
        print('models-pickle files not found.')
        
    except Exception as e:
        print('Error loading models-pickle files.')
    
# recommend function for the api
@lru_cache(maxsize=128)
def recommend_book(book_name: str):
    # Use the cached data_files 
    pt_df, similarity_df, books_df = load_model_files()
    # index fetch
    index = np.where(pt_df.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_df[index])),key=lambda x:x[1],reverse=True)[1:10]

    data = []
    for i in similar_items:
        item = []
        temp_df = books_df[books_df['Book-Title'] == pt_df.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    recommended = [{"Book-Title": title, "Book-Author": author, "Image-URL-M": image} for title, author, image in data]
    return recommended

# popular-df-api
@app.get('/popular')
async def popular_books():
    return load_df()

# recomment-books-api
@app.post('/recommend/')
async def recommend_books(book_name: str):
    result = recommend_book(book_name)   
    return result
