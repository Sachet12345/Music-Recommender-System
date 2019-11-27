# Music-Recommender-System
## 1 Description
Our study is based on Million Song Dataset Challenge in Kaggle. We would
like to do a large, personalized music recommendation system with the goal of
predicting the songs that a user is going to listen. We learn from users listening
history and full information of all songs (metadata, audio content analysis and
standardized identifiers). Our goal is make our system largescale and more
personal to users
## 2 Project approach
We propose following algorithms for our task1. Popularity based
The most trivial recommendation algorithm is to simply present each song
in descending order of its popularity skipping those songs already consumed by the user, regardless of the user’s taste profile./n
### 1. Popularity based
The most trivial recommendation algorithm is to simply present each song
in descending order of its popularity skipping those songs already consumed by the user, regardless of the user’s taste profile.
### 2. Same artist greatest hits
This simply produces the most popular songs by artists that the user
has already listened to. This gives some level of personalization in the
recommendation system.
### 3. Collaborative Filtering
It can be either user-based or item-based. In user-based recommendation,
users who listen to the same songs in the past tend to have similar interests
and will probably listen to the same songs in future. In the item-based
recommendation strategy, songs that are often listened by the same user
tend to be similar and are more likely to be listened together in future by
some other user.
### 4. Latent factor model
The ratings are deeply influenced by a set of factors that are very specific
to the domain (e.g. genre, artist). These factors are in general not obvious
and we need to infer those so called latent factors from the rating data.
Users and songs are characterized by latent factors and a latent factor
model such as Singular Value Decomposition (SVD) can decompose rating
matrix into the product of a user feature and an item(song) feature matrix.
## 3 Dataset
We would be using the database provided by Kaggle competition, refer
https://www.kaggle.com/c/msdchallenge/data
It includes metadata (e.g., artist identifiers, tags,etc) , audio content analysis
and standardized identifiers.
## Libraries
Please install the following libraries:
*sklearn*
*pandas*
*numpy*
