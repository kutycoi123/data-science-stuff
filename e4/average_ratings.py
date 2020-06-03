import sys
import pandas as pd
from difflib import get_close_matches

def extractMovies(path):
    return pd.read_csv(path, sep='\n', names=['title'])

def extractRatings(path):
    return pd.read_csv(path)

def normalize(column):
    return column.str.replace(' ', '').str.lower()


def process(movies, ratings):
    movies['normalized_title'] = normalize(movies['title'])
    movie_titles = movies['normalized_title'].tolist() 
    rating_titles = normalize(ratings['title'])
    
    def validateTitle(unclean_title):
        """Return null if title is not valid"""
        matches = get_close_matches(unclean_title, movie_titles, cutoff=0.7)
        if matches:
            return matches[0]
        return None
            
    ratings['normalized_title'] = rating_titles.apply(lambda x : validateTitle(x))
    ratings = ratings[ratings.normalized_title.notna()].drop(['title'], axis=1)
    ratings = ratings.groupby('normalized_title').mean().round(2).reset_index()
    #movies = pd.concat([movies, ratings], axis=1)
    movies = movies.join(ratings.set_index('normalized_title'), on='normalized_title')
    movies = movies[movies.rating.notna()].drop(['normalized_title'], axis=1).sort_values(by=['title'])
    return movies, ratings

def save(data, path):
    data.to_csv(path, index=False)
    
def main():
    outFile = sys.argv[3]
    movies = extractMovies(sys.argv[1])
    ratings = extractRatings(sys.argv[2])
    movies_with_ratings, ratings = process(movies, ratings)
    save(movies_with_ratings, outFile)
if __name__ == "__main__":
    main()
