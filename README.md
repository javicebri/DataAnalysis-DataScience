# Data Analyst/Data Science projects and tools

Projects are organized by thematic folder.
My_tools folder contains my generic functions so I can use them when I need.

### Topics covered:

___
#### Optimization:
[Linear programming](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/My_tools/Optimization): 
Linear programing: Continuous and MILP with Scipy and Pulp libraries.
[Leontief optimization](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/My_tools/Optimization): 
- Introducion to input output economy models
- Simulation of economy, plannig resources and excess of production.
- Simulation of the economy with planning optmization of the input resources to achieve the excess of specific resources.

#### Data transformation: 
[DataAnalysis-DataScience/Padron_Madrid](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Padron_Madrid): In this notebook the data from the 2020 Madrid population census are crossed with the 2016 average income and the 2020 social services data. The purpose of the notebook is to show the work with the Pandas and Plotly libraries: 
- Make groups (groupby)
- Dataframe intersections (merge)
- Data transformation (apply) and other operations
- Plots (pie, stacked bar...)
- Correlation
___
#### Classification, machine learning:
[Classification_tools](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/My_tools/Classification):
Cheatsheet, this notebook has the basic code reference to: 
- Train 
- Tune hyperparameters: (GridSearchCV, RandomSearchCV...)
- Dummy classifier
- Evaluation: (accuracy, precision, recall, f1, report, ROC AUC and Precision-Recall Curves with best threshold)
- Visualize regions and data
- Pipelines and cross validation

___
#### Maximum likelihood estimation:
[Experiment_With_Exponential_and_Gamma_Distributions](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Experiment_With_Exponential_and_Gamma_Distributions): 
Own data experiment in which cars are counted on a highway to show that the time intervals follow an exponential / gamma distribution. For this, the parameters are obtained by maximum likelihood and a non-parametric test is performed (Kolmogorov-Smirnov)

[My_tools/maximum_likelihood_estimation.ipynb](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/My_tools/Maximum_likelihood_estimation): Reference notebook to have the maximum likelihood calculation quickly.
___      
#### Nonparametric test:
[Experiment_With_Exponential_and_Gamma_Distributions](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Experiment_With_Exponential_and_Gamma_Distributions): 
Own data experiment in which cars are counted on a highway to show that the time intervals follow an exponential / gamma distribution. For this, the parameters are obtained by maximum likelihood and a non-parametric test is performed (Kolmogorov-Smirnov)

[Astronomy/Kepler/Star_mass_distribution](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Astronomy/Kepler/Star_mass_distribution): 
Exploration of data from the Kepler mission to search for exoplanets. He performs a study of the stellar mass distribution in stars with exoplanets and applies a nonparametric test (Kolmogorov-Smirnov) to rule out a normal distribution.
___
#### API and JSON: 
[SWAPI/Planet_population_distribution](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/SWAPI/Planet_population_distribution): It asks for the data on the Star Wars planets in an open API and shows the population percentage of the 5 most inhabited planets and groups the rest as 'other' in a pie chart. 
___      
#### Correlation:
[Astronomy/Kepler/Correlation_orbital_period](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Astronomy/Kepler/Star_mass_distribution): 
Exploration of data from the Kepler mission to search for exoplanets. Correlates the orbital period of exoplanets and searches with theoretical approximations.
___
#### Distributions:
[001-Distribution](https://github.com/javicebri/DataAnalysis-DataScience/tree/main/Theory%20%26%20Practice/001-Distributions): 
- Bernoulli
- Binomial with monte carlo
