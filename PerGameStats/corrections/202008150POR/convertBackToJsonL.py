import pandas as pd
##### USER VARIABLES #####
inp='tgq.csv'
#########################

def convertBackToJsonL(filename):
    df = pd.read_csv(filename)
    df.to_json(filename.replace('.csv', '.jsonl'), orient='records', lines=True, index=False)
    print(f"Data saved to {filename.replace('.csv', '.jsonl')}")
    

with open(inp, 'r') as f:
    x=pd.read_json(f, lines=True)
    convertBackToJsonL(x, inp)