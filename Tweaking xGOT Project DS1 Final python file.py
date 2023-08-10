#!/usr/bin/env python
# coding: utf-8

# In[20]:


#importing the neccessary libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import squarify

get_ipython().run_line_magic('matplotlib', 'inline')


# In[21]:


#quick look at the dataset

xgot_unfiltered_df = pd.read_csv(r'C:\Users\siddh\OneDrive\Desktop\project dataset xgot.csv')
xgot_unfiltered_df.head()


# In[22]:


xgot_unfiltered_df.info()


# In[23]:


#filtering the data
xgot_df = xgot_unfiltered_df[xgot_unfiltered_df['Gls'] >= 15]

# Display the filtered DataFrame
xgot_df


# In[24]:


plt.figure(figsize=(10, 6))

# Sort the DataFrame by the 'Gls' column in descending order
xgot_df_sortedbyxGOT = xgot_df.sort_values('Gls', ascending=False)

# Then use slicing to select the top 20 rows
xgot_df_sortedbyxGOT_top20 = xgot_df_sortedbyxGOT[:20]

# Plotting the data
plt.hlines(y=np.arange(1,21), xmin=0, xmax=xgot_df_sortedbyxGOT_top20['xGOT'][:20], color="skyblue")
plt.plot(xgot_df_sortedbyxGOT_top20['xGOT'][:20], np.arange(1,21), "o")
plt.yticks(np.arange(1,21), xgot_df_sortedbyxGOT_top20["Player"][:20])
plt.gca().invert_yaxis()  # This line inverts the y-axis so the player with the most goals is at the top
plt.xlabel('xGOT accumulated')
plt.show()


# In[25]:


# Fit a linear regression line to the 'xG' and 'xGOT' data
slope, intercept = np.polyfit(xgot_df['xG'], xgot_df['xGOT'], 1)

# Generate the x values for the trendline
x_values = np.linspace(xgot_df['xG'].min(), xgot_df['xG'].max(), 100)

# Calculate the corresponding y values using the slope and intercept
y_values = slope * x_values + intercept

# Now you can create your scatterplot with this new DataFrame
fig, ax = plt.subplots()
fig.set_size_inches(7, 5)

plt.plot(xgot_df['xG'], xgot_df['xGOT'], ".")
plt.axvline(xgot_df['xG'].mean(), linestyle=':', color='r')  # Vertical line at the mean of 'Gls'
plt.axhline(y=xgot_df['xGOT'].mean(), linestyle=':', color='r')  # Horizontal line at the mean of 'MP'

plt.plot(x_values, y_values, "-", color="blue")  # Plot the trendline

ax.set_title("xG (X) & xGOT (Y) Correlation")
ax.set_xlabel("xG Accumulated")
ax.set_ylabel("xGOT Accumulated")

highlighted_players = ["Erling Haaland", "Lionel Messi" , "Jonathan David"]  

for index, row in xgot_df.iterrows():
    if row['Player'] in highlighted_players:
        plt.text(row['xG'], row['xGOT'], row['Player'], fontsize=9, ha='right')

plt.show()


# In[26]:


xgot_unfiltered_df['xGOTop'] = xgot_unfiltered_df['xGOT'] - xgot_unfiltered_df['PK'] * 0.975
xgot_unfiltered_df['xGOT_difference'] = xgot_unfiltered_df['xGOT'] - xgot_unfiltered_df['xGOTop']


# In[27]:


xgot_df = xgot_unfiltered_df[xgot_unfiltered_df['Gls'] >= 15]
xgot_df


# In[28]:


import matplotlib
import matplotlib.pyplot as plt
import squarify

# Filter to include only players with shots between 50 and 75 in the English Premier League
xGOTop_treemap = xgot_df[(xgot_df["SoT"] >= 20) & (xgot_df["SoT"] <= 50) & (xgot_df["xGOTop"] > 0)]

# Sort the data by xGOTop in descending order
xGOTop_treemap = xGOTop_treemap.sort_values(by='xGOTop', ascending=False)

# Utilize matplotlib to scale our numbers between the min and max, then assign this scale to our values.
norm = matplotlib.colors.Normalize(vmin=min(xGOTop_treemap.xGOTop), vmax=max(xGOTop_treemap.xGOTop))
colors = [matplotlib.cm.coolwarm(norm(value)) for value in xGOTop_treemap.xGOTop]  # You can change the color map here

# Create our plot and resize it.
fig = plt.gcf()
ax = fig.add_subplot()
fig.set_size_inches(16, 4.5)

# Use squarify to plot our data, label it, and add colors. We add an alpha layer to ensure black labels show through
squarify.plot(label=xGOTop_treemap.Player, sizes=xGOTop_treemap.xGOTop, color=colors, alpha=.6)
plt.title("xGOT from open play for players with 20 to 50 shots on target")

plt.axis('off')
plt.show()


# In[29]:


import numpy as np
import matplotlib.pyplot as plt

# Assuming xgot_df is your DataFrame containing player statistics
# Get the top 15 players with the most goals (Gls)
top_players = xgot_df.nlargest(15, 'Gls')

# Extract player names for labeling the x-axis
labels = top_players['Player']

# Create an array of x-values for the bar positions
x = np.arange(len(labels))

# Set the width of the bars
width = 0.35

# Create a new figure and axis for the bar plot
fig, ax = plt.subplots()

# Create the first set of bars for xGOT values
rects1 = ax.bar(x - width/2, top_players['xGOT'], width, label='xGOT')

# Create the second set of bars for xGOTop values
rects2 = ax.bar(x + width/2, top_players['xGOTop'], width, label='xGOTop')

# Set labels and title for the plot
ax.set_ylabel('Scores')
ax.set_title('Comparison between xGOT and xGOTop for Top 15 Players with the most Goals')

# Set the tick positions and labels on the x-axis
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90)

# Add a legend to the plot
ax.legend()

# Display the plot
plt.show()


# In[30]:


# Import necessary libraries
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming xgot_df is your DataFrame containing player statistics
# Get the top 20 players with the most difference between xGOT and xGOTop
top_difference_players = xgot_df.nlargest(20, 'xGOT_difference')

# Set the theme and style for the plot using seaborn
sns.set_theme(style="whitegrid", color_codes=True)

# Create a bar plot using seaborn
# x-axis: Player names, y-axis: Difference between xGOT and xGOTop
# Use 'rocket' palette for color variation
ax = sns.barplot(x='Player', y='xGOT_difference', data=top_difference_players, palette='rocket')

# Set y-axis label
ax.set_ylabel("Difference (xGOT - xGOTop)", fontsize=20)

# Rotate x-axis labels for better readability
plt.xticks(rotation=75)

# Set the figure size
plt.rcParams["figure.figsize"] = (20, 8)

# Set the title for the plot
plt.title('Plot of Players vs Difference in xGOT and xGOTop', fontsize=20)

# Display the plot
plt.show()


# In[31]:


xgot_unfiltered_df['Shot_Quality'] = xgot_unfiltered_df['xGOTop'] / xgot_unfiltered_df['SoT']
xgot_df = xgot_unfiltered_df[xgot_unfiltered_df['Gls'] >= 15]
xgot_df


# In[32]:


import matplotlib.pyplot as plt
import numpy as np

# Set the figure size for the plot
plt.figure(figsize=(10, 6))

# Sort the DataFrame by the 'Shot_Quality' column in descending order
xgot_df_sortedbyShot_Quality = xgot_df.sort_values('Shot_Quality', ascending=False)

# Select the top 20 rows based on sorted 'Shot_Quality'
xgot_df_sortedbyShot_Quality_top20 = xgot_df_sortedbyShot_Quality[:20]

# Creating a horizontal bar plot
# Horizontal lines indicating player ranks, x-axis represents Shot Quality
# Color of lines: firebrick
plt.hlines(y=np.arange(1, 21), xmin=0, xmax=xgot_df_sortedbyShot_Quality_top20['Shot_Quality'][:20], color="firebrick")

# Plotting individual data points as circles
# x-axis: Shot Quality, y-axis: Player ranks
# Color of circles: darkred
plt.plot(xgot_df_sortedbyShot_Quality_top20['Shot_Quality'][:20], np.arange(1, 21), "o", color="darkred")

# Setting y-axis tick positions and labels
plt.yticks(np.arange(1, 21), xgot_df_sortedbyShot_Quality_top20["Player"][:20])

# Invert y-axis to have the player with the most goals at the top
plt.gca().invert_yaxis()

# Set x-axis label
plt.xlabel('Shot Quality')

plt.show()


# In[33]:


xgot_unfiltered_df['xGOTop/Gls'] = xgot_unfiltered_df['xGOTop'] / xgot_unfiltered_df['Gls']
xgot_df = xgot_unfiltered_df[xgot_unfiltered_df['Gls'] >= 15]
xgot_df


# In[34]:


import numpy as np
import matplotlib.pyplot as plt

# Assuming xgot_df is your DataFrame containing player statistics
# Get the top 15 players with the highest xGOTop values
top_players = xgot_df.nlargest(15, 'xGOTop')

# Extract player names for labeling the x-axis
labels = top_players['Player']

# Create an array of x-values for the bar positions
x = np.arange(len(labels))

# Set the width of the bars
width = 0.35

# Create a new figure and axis for the bar plot
fig, ax = plt.subplots()

# Create the first set of bars for xGOTop/Gls values, with color '#5F9EA0'
rects1 = ax.bar(x - width/2, top_players['xGOTop/Gls'], width, label='xGOTop/Gls', color='#5F9EA0')

# Create the second set of bars for Shot Quality values, with color '#DC143C'
rects2 = ax.bar(x + width/2, top_players['Shot_Quality'], width, label='Shot_Quality', color='#DC143C')

# Set labels and title for the plot
ax.set_ylabel('Scores')
ax.set_title('Comparison between Shot Quality and xGOTop/Gls for Top 15 Players with the most xGOT from open play')

# Set the tick positions and labels on the x-axis
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90)

# Add a legend to the plot
ax.legend()

plt.show()


# In[35]:


# Fit a linear regression line to the 'xG' and 'xGOT' data
slope, intercept = np.polyfit(xgot_df['Shot_Quality'], xgot_df['G/SoT'], 1)

# Generate the x values for the trendline
x_values = np.linspace(xgot_df['Shot_Quality'].min(), xgot_df['Shot_Quality'].max(), 100)

# Calculate the corresponding y values using the slope and intercept
y_values = slope * x_values + intercept

# Now you can create your scatterplot with this new DataFrame
fig, ax = plt.subplots()
fig.set_size_inches(7, 5)

# Add a horizontal line at the mean of 'G/SoT' using a red dashed line
plt.plot(xgot_df['Shot_Quality'], xgot_df['G/SoT'], ".", color = '#3D9140')
plt.axvline(xgot_df['Shot_Quality'].mean(), linestyle=':', color='r')  # Vertical line at the mean of 'Gls'
plt.axhline(y=xgot_df['G/SoT'].mean(), linestyle=':', color='r')  # Horizontal line at the mean of 'MP'

# Plot the linear trendline using blue color
plt.plot(x_values, y_values, "-", color="#00688B")  # Plot the trendline

# Set title and labels for axes
ax.set_title("Shot Quality (X) Vs. Goal Conversion Rate (Y)")
ax.set_xlabel("xGOTop/SoT")
ax.set_ylabel("Gls/SoT")

# List of highlighted player names for annotation
highlighted_players = ["Boulaye Dia", "Martin Ødegaard", "Lionel Messi", "Erling Haaland", "Vedat Muriqi"]  # Replace with actual names

# Add annotations for highlighted players
for index, row in xgot_df.iterrows():
    if row['Player'] in highlighted_players:
        plt.text(row['Shot_Quality'], row['G/SoT'], row['Player'], fontsize=9, ha='right')

plt.show()


# In[36]:


xgot_unfiltered_df['xGop'] = xgot_unfiltered_df['xG'] - xgot_unfiltered_df['PK'] * 0.76
xgot_unfiltered_df['adjSGA'] = xgot_unfiltered_df['xGOTop'] - xgot_unfiltered_df['xGop']


xgot_df = xgot_unfiltered_df[xgot_unfiltered_df['Gls'] >= 15]
print(xgot_df.columns)
xgot_df


# In[37]:


import seaborn as sns
import matplotlib.pyplot as plt

# Get the top 20 players with the highest 'adjSGA' values
top_adjSGA_players = xgot_df.nlargest(20, 'adjSGA')

# Sort the top_adjSGA_players DataFrame by 'adjSGA' column in descending order
top_adjSGA_players_sorted = top_adjSGA_players.sort_values('adjSGA', ascending=False)

# Set the theme and style for the plot using seaborn
sns.set_theme(style="whitegrid", color_codes=True)

# Create a bar plot using seaborn
# x-axis: Player names, y-axis: Adjusted Shooting Goals Added (adjSGA)
# Use 'viridis' palette for color variation
ax = sns.barplot(x='Player', y='adjSGA', data=top_adjSGA_players_sorted, palette='viridis')

# Set y-axis label
ax.set_ylabel("Adjusted Shooting Goals Added", fontsize=20)

# Rotate x-axis labels for better readability
plt.xticks(rotation=75)

# Set the figure size
plt.rcParams["figure.figsize"] = (20, 8)

# Set the title for the plot
plt.title('Plot of Players with highest adjSGA', fontsize=20)

plt.show()


# In[ ]:




