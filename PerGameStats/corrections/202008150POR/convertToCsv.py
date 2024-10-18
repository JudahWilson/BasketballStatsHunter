import pandas as pd
##### USER VARIABLES #####
inp='tgq.jsonl'
#########################

def convertToCsv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

x=pd.read_csv(inp)
convertToCsv(x, inp.replace('.jsonl', '.csv'))