#-------------------------- IMPORTS-----------------------
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
import connect
#-----------------------END IMPORTS-----------------------

conn = connect.connect()
cur = conn.cursor()

class DBData:
    #-------------------------- VIEWS -------------------------
    def getViews():
        views_query = """
        SELECT
            bits_views_user_links.user_id,
            bits_views_bits_content_links.bits_content_id,
            bits_contents.title,
            bits_contents.caption
        FROM
            bits_views_user_links
            JOIN bits_views_bits_content_links ON bits_views_user_links.bits_view_id = bits_views_bits_content_links.bits_view_id
            JOIN bits_contents ON bits_views_bits_content_links.bits_content_id = bits_contents.id"""

        cur.execute(views_query)


        views = pd.DataFrame.from_dict(cur.fetchall())

        colnames = ['user_id', 'bits_id', 'title', 'caption']
        views.columns = colnames
        views.reset_index(drop=True, inplace=True)
        views['views'] = 1
        return views

    #-----------------------END VIEWS-----------------------

    #-------------------------- LIKES -------------------------
    def getLikes():
        likes_query = """
        SELECT
            bits_likes_user_links.user_id,
            bits_likes_bits_content_links.bits_content_id,
            bits_contents.title
        FROM
            bits_likes_user_links
            JOIN bits_likes_bits_content_links ON bits_likes_user_links.bits_like_id = bits_likes_bits_content_links.bits_like_id
            JOIN bits_contents ON bits_likes_bits_content_links.bits_content_id = bits_contents.id"""
            
        cur.execute(likes_query)

        likes = pd.DataFrame.from_dict(cur.fetchall())

        colnames = ['user_id', 'bits_id', 'title']
        likes.columns = colnames
        likes.reset_index(drop=True, inplace=True)
        likes

        likes = likes[['user_id', 'bits_id', 'title']].value_counts().to_frame()
        likes.reset_index(inplace=True)
        likes.rename( columns={0: 'likes'}, inplace=True )
        return likes

    #-----------------------END LIKES-----------------------

    #-------------------------- COMMENTS -------------------------
    def getComments():
        comments_query = """
        SELECT
            bits_comments_user_links.user_id,
            bits_comments_bits_content_links.bits_content_id,
            bits_contents.title
        FROM
            bits_comments_user_links
            JOIN bits_comments_bits_content_links ON bits_comments_user_links.bits_comment_id = bits_comments_bits_content_links.bits_comment_id
            JOIN bits_contents ON bits_comments_bits_content_links.bits_content_id = bits_contents.id"""

        cur.execute(comments_query)


        comments = pd.DataFrame.from_dict(cur.fetchall())

        colnames = ['user_id', 'bits_id', 'title']
        comments.columns = colnames
        comments.reset_index(drop=True, inplace=True)

        comments = comments[['bits_id', 'user_id', 'title']].value_counts().to_frame()
        comments.reset_index(inplace=True)
        comments.rename( columns={0: 'comments'}, inplace=True )
        return comments
    #-----------------------END LIKES-----------------------
    
    #-------------------------- COMMENTS -------------------------
    def getData(views = getViews(), likes = getLikes(), comments = getComments()):
        # if conn is not None:
        #     conn.close()
        #     print('Database connection closed.')
        temp = pd.merge(views, likes, on=['bits_id', 'user_id', 'title'], how='outer')
        df = pd.merge(temp, comments, on=['bits_id', 'user_id', 'title'], how='outer')
        df.fillna({'likes': 0, 'comments': 0}, inplace=True)


        # Rating Calculation
        base = df.likes.max() + df.views.max() + df.comments.max()
        df['rating'] = round((((df['likes'] + df['views'] + df['comments'])/base) * 5 + (base/10)), 2)
        

        df2 = df.copy()

        df2 = df2[['bits_id', 'user_id', 'rating']]


        return df, df2