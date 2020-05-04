
# coding: utf-8

# In[64]:


import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


# In[5]:


df = pd.read_csv("Desktop\SalesAnalysis\Sales_Data\Sales_April_2019.csv")
df


# In[6]:


#list all files in a directory using os library
files = [file for file in os.listdir('Desktop\SalesAnalysis\Sales_Data')]
for file in files:
    print(file)


# In[8]:


#Merging Data

all_data = pd.DataFrame()
for file in files:
        df = pd.read_csv("Desktop/SalesAnalysis/Sales_Data/"+file)
        all_data = pd.concat([all_data, df])

all_data.head()


# In[9]:


#Clean Data

nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data = all_data.dropna(how='all')
all_data.head()


# In[12]:


#Find 'Or' and drop

#temp_df = all_data[all_data['Order Date'].str[0:2] =='Or']
#temp_df.head() #Shows the rows with errors

all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data.head() #Drops the rows with errors


# In[13]:


#Adding Additional columns

#Adding month column to the dataframe

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()



# In[14]:


#Converting columns in to necessary data types

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[15]:


# Adding a sales column

all_data['Sales'] = all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# In[16]:


#What was the best month for sales and how much was earned that month?

all_data.groupby('Month').sum()


# In[17]:


# Plot the above data
results = all_data.groupby('Month').sum()
months = range(1, 13)

plt.bar(months, results['Sales'])
plt.xticks(months)
plt.xlabel('Month Number')
plt.ylabel('Sales in USD ($)')
plt.show()


# In[40]:


#Which city has the higher number of sales

#Get City and State

def get_state(address):
    return address.split(',')[2].split(' ')[1]

def get_city(address):
    return address.split(',')[1]

#all_data['State'] = all_data['Purchase Address'].apply(lambda x: get_state(x))
#all_data.head()

all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x) + ' ' + get_state(x))
all_data.head()


#all_data.drop(columns = 'State', inplace = True)
#all_data.drop(columns = 'City', inplace = True)
#all_data.head()


# In[ ]:


#Which city has the higher number of sales


# In[41]:


# Plot the above data
results = all_data.groupby('City').sum()
results


# In[44]:


cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation = 'vertical', size = 8)
plt.xlabel('Cities')
plt.ylabel('Sales in USD ($)')
plt.show()


# In[51]:


#Best time to advertise a product

#convert into date time
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

#get hours, minutes
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[56]:


Hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(Hours, all_data.groupby(['Hour']).count())
plt.xticks(Hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.grid()
plt.show()


# In[58]:


#Which products are sold together

#See duplicated order ID

df = all_data[all_data['Order ID'].duplicated(keep=False)]
df.head()


# In[59]:


#Create a new column with products in sample tuple

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df.head()


# In[60]:


#Drop dupliate order id

df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head()


# In[66]:


count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
#print(count)
count.most_common(10)


# In[68]:


#Which product has been sold the most?

product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.xlabel('Product')
plt.ylabel('Quantity Ordered')
plt.xticks(products, rotation= 'vertical', size = 8 )
plt.show()


# In[70]:


#Get product prices

prices = all_data.groupby('Product').mean()['Price Each']
print(prices)


# In[71]:


fig , ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color = 'g')
ax2.plot(products,prices, 'b-')

ax1.set_xlabel('Product Name')
ax2.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price $', color = 'b')
ax1.set_xticklabels(products, rotation='vertical', size= 8)
plt.show()


