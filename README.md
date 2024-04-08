## premier-league-match-result-prediction

## Introduction

In this project, we compare the performance of many Machine Learning and Deep Learning strategies and models to predict the outcomes of English Premier League soccer matches based on the average player performance of both teams from the previous season (mormalized by minutes played). We have two targets for prediction: the result (Home Win, Away Win, or Draw), as well as the Goal Difference for the home team (home goals - away goals). This allows us to perform both classification and regression, to have a greater chance at discovering the best predictor model possible.

The goal is to have the best model (that is within our means to achieve) to **predict the result of an EPL match based only on the team sheets (player list) for the Home and Away teams.** This could be useful for betting, fantasy sports, or other applications where predicting the outcome of a match based on limited, but fast and readily available information is important.

Both traditional machine learning and basic deep learning techniques will be used. To ensure a rigorous assessment, we will employ pipelines for hyperparameter tuning, and k-fold cross-validation for validating model performance. We will also create different neural network models, such as a basic fully connected NN, an Tabular CNN, or other neural network strategies, and compare their accuracy metrics. This methodology will give us an exhaustive exploration of a wide array of models for the selection of a model that best captures the match outcomes.

## Data
The data used is [final_dataset.csv](final_dataset.csv).

## Method
Please see [MatchResultPrediction.ipynb](MatchResultPrediction.ipynb).

## Report
Please see [ENEL645 - Final Project.pdf](ENEL645%20-%20Final%20Project.pdf).

