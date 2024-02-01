#Importing all the requirements
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import ta

#Reading the data
df = pd.read_csv('D:\script\schei2\daFontiOnline\Binance-ETHUSDT-22-04-2020.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'],format='%Y-%m-%d %H:%M:%S')
df.set_index('timestamp',inplace=True)
#df = df.astype(float)

#using TA
df1 = ta.add_all_ta_features(df, open="open", high="high", low="low", close="close", volume="volume")

#Method for outcomes and scenarios 0s and 1s
def scenarios(df1=df1,n=30,lower=-0.5,upper=0.5):
    df1 = df1[['open','high','low','close','volume']]
    Cumulated_name = []
    Cumulated_boundary = []

    for i in range(1,n+1):
        first_name = 'DiffClose'+str(i)
        second_name = 'DiffMin'+str(i)
        df1[first_name] = df1['close'].diff(i).shift(-i).fillna(0)/df['close']*100
        df1[second_name] = np.where((df1[first_name]<lower) | (df1[first_name]>upper),i,n)
        Cumulated_name.append(first_name)
        Cumulated_boundary.append(second_name)

    df1['Period'] = df1[Cumulated_boundary].min(axis=1)
    df1['Outcome'] = df1.apply(lambda x:x['DiffClose'+str(x['Period']).split('.')[0]],axis=1)
    df1 = df1[['open','high','low','close','volume','Period','Outcome']]
    return df1

#Selecting indicator and changing names
final=scenarios(df1,n=100)
#print(final)
'''
                       open    high     low   close      volume  Period   Outcome
timestamp
2018-12-09 03:40:00   90.49   90.61   90.42   90.49  1083.72391      17  0.508343
2018-12-09 03:45:00   90.46   90.88   90.41   90.87  1724.56186      32 -1.320568
2018-12-09 03:50:00   90.82   90.95   90.68   90.73  2595.24130      31 -1.168302
2018-12-09 03:55:00   90.74   90.74   90.36   90.48   566.44107      14  0.519452
2018-12-09 04:00:00   90.48   90.76   90.37   90.53   976.74525      14  0.563349
...                     ...     ...     ...     ...         ...     ...       ...
2020-04-22 03:20:00  171.66  171.68  171.32  171.52  1098.67428     100  0.000000
2020-04-22 03:25:00  171.52  171.53  171.22  171.26   714.05771     100  0.000000
2020-04-22 03:30:00  171.27  171.61  171.26  171.48   571.75550     100  0.000000
2020-04-22 03:35:00  171.50  171.50  171.15  171.34  1059.38062     100  0.000000
2020-04-22 03:40:00  171.35  171.41  171.20  171.21   771.07284     100  0.000000
'''

final['Outcome']=np.where(final['Outcome']>0,'+0.5%','-0,5%')
final['Outcome']=np.where(final['Period']==100,'No Outcome',final['Outcome'])
indicator=pd.concat([df1[['trend_macd','trend_macd_signal','trend_macd_diff']],final],axis=1)
indicator=indicator[indicator['Outcome']!='No Outcome'].dropna()
indicator.columns=['trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'Open', 'High', 'Low', 'Close', 'Volume', 'Period', 'Outcome']
#print(final)
'''
                       open    high     low   close      volume  Period     Outcome
timestamp
2018-12-09 03:40:00   90.49   90.61   90.42   90.49  1083.72391      17       +0.5%
2018-12-09 03:45:00   90.46   90.88   90.41   90.87  1724.56186      32       -0,5%
2018-12-09 03:50:00   90.82   90.95   90.68   90.73  2595.24130      31       -0,5%
2018-12-09 03:55:00   90.74   90.74   90.36   90.48   566.44107      14       +0.5%
2018-12-09 04:00:00   90.48   90.76   90.37   90.53   976.74525      14       +0.5%
...                     ...     ...     ...     ...         ...     ...         ...
2020-04-22 03:20:00  171.66  171.68  171.32  171.52  1098.67428     100  No Outcome
2020-04-22 03:25:00  171.52  171.53  171.22  171.26   714.05771     100  No Outcome
2020-04-22 03:30:00  171.27  171.61  171.26  171.48   571.75550     100  No Outcome
2020-04-22 03:35:00  171.50  171.50  171.15  171.34  1059.38062     100  No Outcome
2020-04-22 03:40:00  171.35  171.41  171.20  171.21   771.07284     100  No Outcome
'''

#---------------------------------------------------------

data = (final['Outcome'].value_counts()/len(final)*100).reset_index()
data.columns = ['Final Outcome','% Cases']
#print(data)
'''
  Final Outcome    % Cases
0         -0,5%  49.851611
1         +0.5%  48.880467
2    No Outcome   1.267922
'''
plt.figure(figsize=(11,7))
plt.title('Outcomes + 8 Hours',fontsize=20)
#sns.barplot(data=data,x='Final Outcome',y='% Cases',palette='Pastel1')
plt.bar(x = data["Final Outcome"], height = data["% Cases"])
plt.legend()
plt.xlabel('Final Outcome',fontsize=16)
plt.ylabel('% Cases',fontsize=16)
#plt.show()

#---------------------------------------------------------

#Adding variables 
#indicator["200MA"] = ta.trend.ema(indicator["Close"], periods=200)
indicator["200MA"] = ta.trend.EMAIndicator(indicator["Close"], window = 200).ema_indicator()
indicator["uptrend"] = np.where(indicator["200MA"] < indicator["Close"], 1, 0)
indicator["trend_macd_diff1"] = indicator["trend_macd_diff"].shift(1)
#setting up the constraints
indicator["trend_signal_positive"] = np.where(
    (indicator["trend_macd_diff1"] * indicator["trend_macd_diff"] < 0)
    & (indicator["trend_macd_diff"] > 0)
    & (indicator["trend_macd_signal"] < 0)
    & (indicator["uptrend"] == 1),
    1,
    0,
)

#---------------------------------------------------------

#---------------------------------------------------------


#code for barplot2
indicator['macd_cut'] = pd.cut(indicator['trend_macd'],bins=[-5,-3,-2,-1,-0.5,-0.2,0,0.2,0.5,1,2,3,5])
histogram1=indicator.groupby(['macd_cut','Outcome']).size().reset_index()
histogram1.columns = ['macd_cut','Outcome','Cases']
histogram1['Grouped_cases'] = histogram1.groupby(['macd_cut'])['Cases'].transform(sum)
histogram1['percent'] = histogram1['Cases']/histogram1['Grouped_cases']*100
plt.figure(figsize=(14,7))
#sns.barplot(x="macd_cut", y="percent", hue="Outcome", data=histogram1,palette='Pastel1')

#---------------------------------------------------------

#---------------------------------------------------------

#---------------------------------------------------------


# Training the first model
from sklearn.ensemble import RandomForestClassifier

Initial = indicator[0:120244][ ["trend_macd", "trend_macd_signal", "trend_macd_diff", "Outcome"] ]
Initial = pd.concat(
    [
        Initial[Initial["Outcome"] == "+0.5%"].sample(57000),
        Initial[Initial["Outcome"] != "+0.5%"].sample(57000),
    ]
)

Initial = Initial.sample(frac=1)
X_train = Initial[["trend_macd", "trend_macd_signal", "trend_macd_diff"]]
y_train = np.where(Initial["Outcome"] == "+0.5%", 1, 0)
X_test = indicator[120245:][["trend_macd", "trend_macd_signal", "trend_macd_diff"]]
y_test = np.where(indicator[120245:]["Outcome"] == "+0.5%", 1, 0)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

Classifier1 = RandomForestClassifier(
    max_depth=3,
    min_samples_leaf=400,
    max_features=3,
    min_samples_split=4,
    n_estimators=500,
    random_state=41,
)
Classifier1 = Classifier1.fit(X_train, y_train)
y_pred1 = Classifier1.predict(X_test)

#print(confusion_matrix(y_test, y_pred1))
'''
[[6358 4125]
 [6240 4721]]
'''

#---------------------------------------------------------

#---------------------------------------------------------

#conditional probability
predictions_proba = Classifier1.predict_proba(X_test)
predictions_probability = pd.concat(
    [pd.DataFrame(predictions_proba), pd.DataFrame(y_test)], axis=1
)
predictions_probability.columns = ["prob_0", "prob_1", "result"]

predictions = Classifier1.predict(X_test)
predictions_1 = pd.concat([pd.DataFrame(predictions), pd.DataFrame(y_test)], axis=1)
predictions_1.columns = ["prediction", "result"]
Results = pd.DataFrame([], columns=["P(p)>", "Success rate", "Quantity"])


for i in range(1, 10):
    P_p = np.round(0.48 + i / 50, 2)
    tmp = predictions_probability[ predictions_probability["prob_1"] >= (0.48 + (i / 50)) ]

    Quantity = len( ( tmp ) )
    if Quantity == 0:
        break
    Success_rate = np.round(
        ( tmp["result"] ).sum()
        / len( ( tmp ) ),
        3,
    )
    Results = Results.append( {"P(p)>": P_p, "Success rate": Success_rate, "Quantity": Quantity}, ignore_index=True, )

'''
print(Results)
   P(p)>  Success rate  Quantity
0   0.50         0.534    8878.0
1   0.52         0.535    8036.0
2   0.54         0.537    6400.0
3   0.56         0.542     684.0
4   0.58         0.556     421.0
5   0.60         0.557     210.0
'''

plt.figure(figsize=(12, 7))
#sns.set(font_scale=1.3)
#g = sns.barplot(data=Results, x="P(p)>", y="Success rate", palette="Pastel1")
plt.bar(x = Results["Success rate"], height = Results["P(p)>"])
#plt.ylim(0.5, 0.65)
plt.show()

'''
for index, row in Results.iterrows():
    g.text(
        row.name,
        row["Success rate"],
        int(row.Quantity),
        fontsize=20,
        color="black",
        ha="center",
    )
'''

#---------------------------------------------------------

#adding the variables

indicator['trend_macd_diff1'] = indicator['trend_macd_diff']-indicator['trend_macd_diff'].shift(1)
indicator['trend_macd_diff3'] = indicator['trend_macd_diff']-indicator['trend_macd_diff'].shift(3)
indicator['trend_macd_diff5'] = indicator['trend_macd_diff']-indicator['trend_macd_diff'].shift(5)
indicator['trend_macd_signal1'] = indicator['trend_macd_signal']-indicator['trend_macd_signal'].shift(1)
indicator['trend_macd_signal3'] = indicator['trend_macd_signal']-indicator['trend_macd_signal'].shift(3)
indicator['trend_macd_signal5'] = indicator['trend_macd_signal']-indicator['trend_macd_signal'].shift(5)
indicator['trend_macd1'] = indicator['trend_macd']-indicator['trend_macd'].shift(1)
indicator['trend_macd3'] = indicator['trend_macd']-indicator['trend_macd'].shift(3)
indicator['trend_macd5'] = indicator['trend_macd']-indicator['trend_macd'].shift(5)
indicator['trend'] = (indicator['200MA'] - indicator['Close']) / indicator['Close']

#---------------------------------------------------------

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

#second model
Initial = indicator[0:120244][['trend_macd','trend_macd_signal','trend_macd_diff','trend_macd_diff1','trend_macd_diff3','trend_macd_diff5','trend_macd_signal1','trend_macd_signal3','trend_macd_signal5','trend_macd1','trend_macd3','trend_macd5','trend','Outcome']].dropna()
Initial = pd.concat([Initial[Initial['Outcome']=='+0.5%'].sample(57000),Initial[Initial['Outcome']!='+0.5%'].sample(57000)])
Initial = Initial.sample(frac=1)
X_train = Initial[['trend_macd','trend_macd_signal','trend_macd_diff','trend_macd_diff1','trend_macd_diff3','trend_macd_diff5','trend_macd_signal1','trend_macd_signal3','trend_macd_signal5','trend_macd1','trend_macd3','trend_macd5','trend']]
y_train = np.where(Initial['Outcome']=='+0.5%',1,0)
X_test = indicator[120245:][['trend_macd','trend_macd_signal','trend_macd_diff','trend_macd_diff1','trend_macd_diff3','trend_macd_diff5','trend_macd_signal1','trend_macd_signal3','trend_macd_signal5','trend_macd1','trend_macd3','trend_macd5','trend']]
y_test = np.where(indicator[120245:]['Outcome']=='+0.5%',1,0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

Classifier = RandomForestClassifier(max_depth=11,min_samples_leaf=400,max_features=11,min_samples_split=4,n_estimators=500, random_state=28)
Classifier.fit(X_train, y_train)
y_pred = Classifier.predict(X_test)

print(confusion_matrix(y_test,y_pred))
'''
[[4999 5484]
 [4540 6421]]
 '''














