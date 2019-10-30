import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read dataset
# products = pd.read_csv('../dataset/products.csv', sep=';', error_bad_lines=False, encoding="latin-1")
# products.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
# users = pd.read_csv('../dataset/users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
# users.columns = ['userID', 'Location', 'Age']
# ratings = pd.read_csv('../dataset/ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
# ratings.columns = ['userID', 'ISBN', 'bookRating']

# combine_rating = pd.merge(ratings, products, on='ISBN')
# columns = ['yearOfPublication', 'publisher', 'bookAuthor', 'imageUrlS', 'imageUrlM', 'imageUrlL']
# combine_rating = combine_rating.drop(columns, axis=1)
# combine_rating.head()

# combine_rating = combine_rating.dropna(axis = 0, subset = ['bookTitle'])

# rating_count = (combine_rating.
#      groupby(by = ['bookTitle'])['bookRating'].
#      count().
#      reset_index().
#      rename(columns = {'bookRating': 'totalRatingCount'})
#      [['bookTitle', 'totalRatingCount']]
#     )
# rating_count.head()

# rating_with_totalRatingCount = combine_rating.merge(rating_count, left_on = 'bookTitle', right_on = 'bookTitle', how = 'left')
# rating_with_totalRatingCount

# pd.set_option('display.float_format', lambda x: '%.3f' % x)

# print(rating_count['totalRatingCount'].quantile(np.arange(.9, 1, .01)))

# # popularity_threshold = 50
# # rating_popular = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
# # rating_popular.head()



# from scipy.sparse import csr_matrix

# user_rating = rating_popular.drop_duplicates(['userID', 'bookTitle'])
# user_rating_pivot = user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
# user_rating_matrix = csr_matrix(user_rating_pivot.values)

# from sklearn.neighbors import NearestNeighbors

# model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
# model_knn.fit(user_rating_matrix)



class knn:
    def __init__(self):
        self.dataset()
        self.model()
        self.get_kneighbors('stardust')

    def dataset(self):
        print('##############dataset###################3')
        products = pd.read_csv('../dataset/products.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        products.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
        users = pd.read_csv('../dataset/users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        users.columns = ['userID', 'Location', 'Age']
        ratings = pd.read_csv('../dataset/ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
        ratings.columns = ['userID', 'ISBN', 'bookRating']

        combine_rating = pd.merge(ratings, products, on='ISBN')
        columns = ['yearOfPublication', 'publisher', 'bookAuthor', 'imageUrlS', 'imageUrlM', 'imageUrlL']
        combine_rating = combine_rating.drop(columns, axis=1)
        combine_rating.head()

        combine_rating = combine_rating.dropna(axis = 0, subset = ['bookTitle'])

        rating_count = (combine_rating.
            groupby(by = ['bookTitle'])['bookRating'].
            count().
            reset_index().
            rename(columns = {'bookRating': 'totalRatingCount'})
            [['bookTitle', 'totalRatingCount']]
            )
        rating_count.head()

        rating_with_totalRatingCount = combine_rating.merge(rating_count, left_on = 'bookTitle', right_on = 'bookTitle', how = 'left')
        rating_with_totalRatingCount

        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        ###################
        popularity_threshold = 50
        self.rating_popular = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
        self.rating_popular.head()
    
    def model(self):
        print('##############model###################3')
        from scipy.sparse import csr_matrix

        user_rating = self.rating_popular.drop_duplicates(['userID', 'bookTitle'])
        self.user_rating_pivot = user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
        user_rating_matrix = csr_matrix(self.user_rating_pivot.values)

        from sklearn.neighbors import NearestNeighbors

        self.model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
        self.model_knn.fit(user_rating_matrix)
    
    def get_kneighbors(self, product):
        print('##############GET###################3')
        distances, indices = self.model_knn.kneighbors(self.user_rating_pivot.loc[product, :].values.reshape(1, -1), n_neighbors = 11)

        for i in range(0, len(distances.flatten())):
            if i == 0:
                print(f'Recommendations for {product}:')
            else:
                print(f'{i}: {self.user_rating_pivot.index[indices.flatten()[i]]}, with distance of {distances.flatten()[i]}:')



a = knn()
# query_index = np.random.choice(user_rating_pivot.shape[0])

# distances, indices = model_knn.kneighbors(user_rating_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 11)

# for i in range(0, len(distances.flatten())):
#     if i == 0:
#         print(f'Recommendations for {user_rating_pivot.index[query_index]}:')
#     else:
#         print(f'{i}: {user_rating_pivot.index[indices.flatten()[i]]}, with distance of {distances.flatten()[i]}:')