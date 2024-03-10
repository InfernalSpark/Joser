import os
import pandas as pd
import io

from pathlib import Path



def cleanup(df, name):


    for index, row in df.iterrows():
        try:
            int(row[3] if name.startswith("NIT") else row[2])
        except ValueError:
            df = df.drop(index)

    if name.startswith("NIT"):
        df = df.rename(columns={0:"Quota", 1:"Branch", 2:"Opening", 3:"Closing"}).assign(College=name).astype({"Quota":str, "Branch":str, "Opening":int, "Closing":int, "College":str})
    else:
        df.insert(0, "Quota", "")
        df = df.rename(columns={"Quota":"Quota", 0:"Branch", 1:"Opening", 2:"Closing"}).assign(College=name).astype({"Quota":str, "Branch":str, "Opening":int, "Closing":int, "College":str})

    return df

def apply_quota(df, home:bool):
    if home:
        for index, row in df.iterrows():
            if df["Quota"][index] == "OS":
                df = df.drop(index)
    else:
        for index, row in df.iterrows():
            if df["Quota"][index] == "HS":
                df=df.drop(index)
    
    return df

def cum_data(home):
    li = []
    for file in os.listdir("clg"):
        f = open(f"clg/{file}")
        c = pd.read_html(io.StringIO(f.read()))
        clg = apply_quota(cleanup(c[0], Path(file).stem), True if Path(file).stem==home else False)
        li.append(clg)


    master = pd.concat(li, axis=0, ignore_index=True)

    return master


def main(rank, home):
    pd.set_option('display.max_rows', None)

    # with open("clg/NITK.txt") as f:
    #     c = pd.read_html(io.StringIO(f.read()))
    #     clg = apply_quota(cleanup(c[0], "NITK"), True)
    #     allowed_branches = clg[clg["Closing"].astype(int) >= RANK]
    #     print(allowed_branches)

    # rank = int(input("What's your rank?: "))
    # home = input("What's your home state NIT Code?: ")
    # male = input("you have ding ding?(y/n): ")

    master = cum_data(home)

    allowed = master[master["Closing"].astype(int) >= rank]
    assist = master[(master["Closing"].astype(int) >= rank-2000) & (master["Closing"].astype(int) <= rank+5000)]
    # print(assist.sort_values(by=['Closing']))

    return assist
