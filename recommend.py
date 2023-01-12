from DBData import DBData
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from scipy.sparse.linalg import svds
df, df2 = DBData.getData()
df = df.drop_duplicates()
df2 = df2.drop_duplicates()

class Recommend:
    # Use popularity based recommender model to make predictions
    def popular_recommend(user_id=5):  
        #Split the training and test data in the ratio 70:30
        train_data, test_data = train_test_split(df2, test_size = 0.3, random_state=0)


        #Count of user_id for each unique product as recommendation score 
        train_data_grouped = train_data.groupby('bits_id').agg({'user_id': 'count'}).reset_index()
        train_data_grouped.rename(columns = {'user_id': 'score'},inplace=True)

        #Sort the products on recommendation score 
        train_data_sort = train_data_grouped.sort_values(['score', 'bits_id'], ascending = [0,1]) 
            
        #Generate a recommendation rank based upon score 
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first') 
                
        #Get the top 5 recommendations 
        user_recommendations = train_data_sort.head(25) 

        #Add user_id column for which the recommendations are being generated 
        user_recommendations['user_id'] = user_id 
        
        #Bring user_id column to the front 
        # ['Bits_ID', 'score', 'Rank', 'User_ID']
        cols = user_recommendations.columns.tolist()
        
        # ['User_ID', 'Bits_ID', 'score', 'Rank']
        cols = cols[-1:] + cols[:-1]
        
        user_recommendations = user_recommendations[cols]
        user_recommendations = user_recommendations['bits_id'].reset_index(drop=True).to_dict()
        
        print(user_recommendations)
        return user_recommendations


    # def checkUser(user_id):
    #     if user_id in df.user_id.values:
    #         print('Present')
    #     else:
    #         print('absent')
        
    def user_based_recommend(user_id, num_recommendations=10, df=df, df2=df2):
        #User-based Collaborative Filtering
        # Matrix with row per 'user' and column per 'bit' 
        pivot_df = df2.pivot(index = 'user_id', columns ='bits_id', values = 'rating').fillna(0)
        pivot_df.head()

        # Singular Value Decomposition
        U, sigma, Vt = svds(pivot_df.to_numpy())
        # Construct diagonal array in SVD
        sigma = np.diag(sigma)

        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 

        # Predicted ratings
        preds_df = pd.DataFrame(all_user_predicted_ratings, columns = pivot_df.columns)
        preds_df.head()
        user_idx = np.where(pivot_df.index == df[df['user_id'] == user_id]['user_id'].values[0])[0][0]
        # index starts at 0
        
        # Get and sort the user's ratings
        sorted_user_ratings = pivot_df.iloc[user_idx].sort_values(ascending=False)
        #sorted_user_ratings
        sorted_user_predictions = preds_df.iloc[user_idx].sort_values(ascending=False)
        #sorted_user_predictions

        temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
        temp.index.name = 'Recommended Bits'
        temp.columns = ['user_ratings', 'user_predictions']
        
        temp = temp.loc[temp.user_ratings == 0]   
        temp = temp.sort_values('user_predictions', ascending=False)
        # print('\nBelow are the recommended items for user(user_id = {}):\n'.format(userID))
        # print(temp.head(num_recommendations))
        len_temp = temp.head(num_recommendations).index.to_list()
        rec_dict = {}
        for i in range(0, len(len_temp)):
            rec_dict[i] = len_temp[i]
        print(rec_dict)
        return rec_dict

    def item_based_recommend(bits_id, num_recs=16, df=df, df2=df2):
        # bits_id = float(bits_id)
        bits_id = bits_id
        x = df2.user_id.value_counts() >= 50

        y = x[x].index

        df2 = df2[df2['user_id'].isin(y)]
        newdf = df2.merge(df, on=['user_id', 'bits_id'])
        newdf.drop(columns='rating_x', inplace=True)
        newdf.rename({'rating_y': 'rating'}, axis=1, inplace=True)
        number_rating = newdf.groupby('title')['rating'].count().reset_index()

        number_rating.rename(columns = {'rating': 'number of rating'}, inplace=True)

        final_rating = newdf.merge(number_rating, on='title')

        bit_pivot = final_rating.pivot_table(columns='user_id', index='title', values='rating', fill_value=0)

        bit_sparse = csr_matrix(bit_pivot)
        bit_model = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
        bit_model.fit(bit_sparse)

        title = df[df['bits_id'] == bits_id]['title'].values[0]
        bit_pivot_idx = np.where(bit_pivot.index == title)[0][0]
        # print(f'bits_id: {bits_id} - pivot_seid = {bit_pivot_idx} - {title}, ', end=f'\n{"-"*50}\n')
        
        distances, suggestions = bit_model.kneighbors(bit_pivot.iloc[bit_pivot_idx, :].values.reshape(1, -1), n_neighbors=num_recs)
        suggestions = suggestions[0][1:]
        bits_dict = {}
        for i in range(len(suggestions)):
            # print(df[df['title'] == bit_pivot.index[suggestions[i]]]['bits_id'].values[0]," : ", bit_pivot.index[suggestions[i]])
            bits_dict[int(i)] = int(df[df['title'] == bit_pivot.index[suggestions[i]]]['bits_id'].values[0])
        print(bits_dict)
        return bits_dict


    # if __name__ == "__main__":
    #     item_based_recommend(66)
    #     print('popular', popular_recommend())
    #     user_based_recommend(5)
