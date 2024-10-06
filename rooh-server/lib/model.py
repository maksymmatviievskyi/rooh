import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle

#Read and format the CSV file
df = pd.read_csv('PATH_TO_FILE')
df[df['class']=='up']
X=df.drop('class', axis=1)
y = df['class']

#Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.3,random_state=1234)

#Define nn algorithms
pipelines = {
    'lr':make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000)),
    'rc':make_pipeline(StandardScaler(), RidgeClassifier(max_iter=10000)),
    'rf':make_pipeline(StandardScaler(), RandomForestClassifier()),
    'gb':make_pipeline(StandardScaler(), GradientBoostingClassifier()),
}
fit_models = {}

#Train the model
for algo, pipeline in pipelines.items():
    model = pipeline.fit(X_train.values, y_train.values)
    fit_models[algo] = model

#Save the model
with open('PATH_TO_FILE', 'wb') as f:
    pickle.dump(fit_models['rf'], f)
    
for algo, model in fit_models.items():
    yhat = model.predict(X_test)
    print(algo, accuracy_score(y_test.values, yhat), 
          precision_score(y_test.values, yhat,  pos_label='up'), 
          recall_score(y_test.values, yhat,  pos_label='up'))