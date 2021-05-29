from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
REC_DIR=os.path.join(BASE_DIR,"recommendation")
FILE_DIR=os.path.join(REC_DIR,"movie_dataset.csv")


# Create your views here.
def index(request):
    if request.method=='POST':
        if len(request.POST.get('search'))==0:
            return render(request,'recommendation/index.html')

        def get_title_from_index(index):
            return df[df.index == index]["title"].values[0]

        def get_index_from_title(title):
            return df[df.title == title]["index"].values[0]

        df = pd.read_csv(FILE_DIR)
        #print df.columns

        features = ['keywords','cast','genres','director']

        for feature in features:
        	df[feature] = df[feature].fillna('')

        def combine_features(row):
        	try:
        		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
        	except:
        		print ("Error:", row)

        df["combined_features"] = df.apply(combine_features,axis=1)

        cv = CountVectorizer()

        count_matrix = cv.fit_transform(df["combined_features"])


        cosine_sim = cosine_similarity(count_matrix)
        movie_user_likes = request.POST.get('search')

        # print(cosine_sim)
        movie_index = get_index_from_title(movie_user_likes)

        similar_movies =  list(enumerate(cosine_sim[movie_index]))


        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

        #Print titles of first 50 movies
        i=0
        mylist=[]
        for element in sorted_similar_movies:
        		mylist.append(get_title_from_index(element[0]))
        		i=i+1
        		if i==50:
        			break
        # print(mylist)
        return render(request,'recommendation/index.html',context={'mylist':mylist})
        # print(request.POST.get('search'))
    return render(request,'recommendation/index.html')
