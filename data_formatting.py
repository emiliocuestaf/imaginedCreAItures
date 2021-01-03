import pandas as pd
import json

# Reading and filtering
df = pd.read_csv('original_data.csv', header=None, sep='\t').iloc[:, 1:]
df.index = df[1]
labels = df.index 
df = df.iloc[:, 1:].T


sources = []
dest = []
d = {}
k = 0
# iteration over rows
for index, row in df.iterrows():
    
    # i indicates first field
    for i in range(row.shape[0]):
        # Adding tag
        if row.iloc[i] != '0' and '{}_{}'.format(row.index[i],row.iloc[i]) not in d.keys(): 
            d['{}_{}'.format(row.index[i],row.iloc[i])] = k
            k += 1
        
        # j indicates 2nd field
        j = i + 1
        
        # Adding target tag and link
        if j < row.shape[0]:
        

            # Target is missing (skip)
            if row.iloc[j] == '0':
                continue
            # Origin is missing (backward search)
            elif row.iloc[i] == '0':            	
                # Adding target tag if necessary
                if '{}_{}'.format(row.index[j],row.iloc[j]) not in d.keys(): 
            	     d['{}_{}'.format(row.index[j],row.iloc[j])] = k
            	     k += 1
                # Backward search	 
                l = i - 1
                while l > 0 and row.iloc[l] == '0':

                    l -= 1
                if l > 0:
                    sources.append(d['{}_{}'.format(row.index[l],row.iloc[l])])
                    dest.append(d['{}_{}'.format(row.index[j],row.iloc[j])])
            elif '{}_{}'.format(row.index[j],row.iloc[j]) not in d.keys(): 
                d['{}_{}'.format(row.index[j],row.iloc[j])] = k
                k += 1
                sources.append(d['{}_{}'.format(row.index[i],row.iloc[i])])
                dest.append(d['{}_{}'.format(row.index[j],row.iloc[j])])
            else:
                sources.append(d['{}_{}'.format(row.index[i],row.iloc[i])])
                dest.append(d['{}_{}'.format(row.index[j],row.iloc[j])])
        else:
            # i is in the last field and j is out of bounds
            pass


# Dictionary formating
out_data = {}
out_data['data'] = []
out_data['data'].append({'node': {}, 'link': {}})

out_data['data'][0]['node']['label'] = [name.split('_')[1] for name in list(d.keys())]
out_data['data'][0]['node']['color'] = ['black'] * len(list(d.keys()))

out_data['data'][0]['link']['source'] = sources
out_data['data'][0]['link']['target'] = dest
out_data['data'][0]['link']['color'] = ['black'] * len(sources)
out_data['data'][0]['link']['value'] = [1] * len(sources)
out_data['data'][0]['link']['label'] = [] 


# Exporting to JSON
with open('formatted_data.json', 'w') as outfile:
    json.dump(out_data, outfile)
    
    
    
# Dictionary formating
out_data = {}
out_data['data'] = []
out_data['data'].append({'node': {}, 'link': {}})

out_data['data'][0]['node']['label'] = ['' for name in list(d.keys())]
out_data['data'][0]['node']['color'] = ['black'] * len(list(d.keys()))

out_data['data'][0]['link']['source'] = sources
out_data['data'][0]['link']['target'] = dest
out_data['data'][0]['link']['color'] = ['black'] * len(sources)
out_data['data'][0]['link']['value'] = [1] * len(sources)
out_data['data'][0]['link']['label'] = [] 


# Exporting to JSON
with open('formatted_data_nolabels.json', 'w') as outfile:
    json.dump(out_data, outfile)

