# **Intelligent Content Recommendation System** **<a href="https://www.researchgate.net/publication/372518685_Intelligent_Content_Recommendation_System" target="_blank">📄</a> <a href="https://padhaai.gurucool.xyz/bits" target="_blank">🔗</a>**
  
  
This project is an in-house project for .
The Padhaai App has a feature for bits, a short 30 seconds video platform which is similar to Instagram Reels and YouTube shorts.

This documentation provides an overview of the recommendation system project and its components. It explains the purpose of the project, the structure of the codebase, and how to use the different modules to generate recommendations.

### Introduction
The recommendation system project aims to provide personalized recommendations to users based on their viewing history, likes, and comments. It utilizes various recommendation algorithms, including popularity-based, user-based collaborative filtering, and item-based collaborative filtering. The project is implemented in Python using the FastAPI framework for building API endpoints.

### Project Structure
The project consists of the following files and directories:

config.py: Contains a function to read database configuration from a database.ini file.
connect.py: Establishes a connection to the PostgreSQL database using the configuration obtained from config.py.
DBData.py: Defines a DBData class that retrieves data from the database, including views, likes, and comments, and performs data processing and calculations.
recommend.py: Implements the recommendation methods, including popularity-based, user-based collaborative filtering, and item-based collaborative filtering.
main.py: Defines the FastAPI application and sets up API endpoints for accessing the recommendations.
README.md: Documentation file providing an overview of the project and usage instructions.

### Configuration
The project utilizes a configuration file named database.ini to store PostgreSQL connection parameters. The configuration file should be present in the same directory as the project files and should have the following structure:
Usage
makefile:
```python
database.ini
[postgresql]
host=<database_host>
database=<database_name>
user=<database_user>
password=<database_password>
```

Clone the Git repository to your local machine.
Install the required dependencies listed in the requirements.txt file.
Set up the PostgreSQL database and provide the necessary configuration details in the database.ini file.
Run the FastAPI application using the command uvicorn main:app --reload.
Access the API endpoints to retrieve recommendations based on different methods.

### Recommendation Methods
The project provides the following recommendation methods:

Popularity-Based Recommendations: This method recommends the most popular bits based on the number of views, likes, and comments. It is implemented in the popular_recommend method in the Recommend class.

User-Based Collaborative Filtering: This method recommends bits to a user based on the preferences of similar users. It utilizes Singular Value Decomposition (SVD) and user ratings to generate predictions. It is implemented in the user_based_recommend method in the Recommend class.

Item-Based Collaborative Filtering: This method recommends similar bits based on the preferences of a given bit. It uses the cosine similarity metric and nearest neighbors algorithm to find similar bits. It is implemented in the item_based_recommend method in the Recommend class.

### API Endpoints
The project exposes the following API endpoints for retrieving recommendations:

/bits/popular/ (GET): Retrieves popularity-based recommendations. It calls the popular_recommend method in the Recommend class.

/bits/user/{user_id} (GET): Retrieves user-based recommendations for a specific user. It calls the user_based_recommend method in the Recommend class.

/bits/item/{bits_id} (GET): Retrieves item-based recommendations for a specific bit. It calls the item_based_recommend method in the Recommend class.

### Dependencies
The project has the following dependencies:
```
psycopg2: PostgreSQL database adapter for Python.
pandas: Data manipulation and analysis library.
numpy: Numerical computing library.
scipy: Scientific
```
