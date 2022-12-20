import pandas as pd
from chembl_webresource_client.new_client import new_client

# Target search for coronavirus
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)
targets

# proteins only inhibit or activate
selected_target = targets.target_chembl_id[4]

# Select bioactivities for specfic target
activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
df = pd.DataFrame.from_dict(res)

# for standard value, the lower the number, the higher the potency
# probably also means the volatility and accuracy of the drug
print(df.standard_type.unique())
df.to_csv('coronavirus_bioactivity_data_raw.csv', index=False)

df2 = df[df.standard_value.notna()]
bioactivity_class = []
# for ml model: categorize bioactivity as active, intermediate, or inactive
for i in df2.standard_value:
    if float(i) >= 10000: # > 10,000 nM- means its too diluted to be effective
        bioactivity_class.append("inactive")
    elif float(i) <= 1000: # < 1000 nM
        bioactivity_class.append("active")
    else:
        bioactivity_class.append("intermediate")

selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection]
print(df3)

df3.to_csv('coronavirus_bioactivity_data_preprocessed.csv', index=False)

# add bioactivity class to dataframe
bioactivity_class = pd.Series(bioactivity_class, name='bioactivity_class')
df4 = pd.concat([df3, bioactivity_class], axis=1)
print(df4)

df4.to_csv('bioactivity_data_preprocessed.csv', index=False)

# compute molecular descriptors for each compound
