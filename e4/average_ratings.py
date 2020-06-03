import sys
import pandas as pd

def extractMovies(path):
    return pd.read_csv(path, sep='\n')

def extractRatings(path):
    return pd.read_csv(path)

def main():
    movies = extractMovies(sys.argv[1])
    ratings = extractRatings(sys.argv[2])
    outFile = sys.argv[3]
if __name__ == "__main__":
    main()
