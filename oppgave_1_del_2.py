import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def multi_remove(string, to_remove: list[str]|str) -> str:
	string = string.lower()
	if type(string) != str:
		return string
	for symbol in to_remove:
		string = string.replace(symbol, "")
	return string

fiske_arter: list[str] = []
with open('hi_arter.txt', 'r', encoding="UTF-8") as file:
	for line in file:
		fiske_arter.append(line.strip())
fiske_arter.sort(key=len)
fiske_arter = fiske_arter[::-1]

ukjente_arter: dict[str:int] = {}

def normalize(string: str) -> str:
	if "(" in string:
		#print(string)
		string = string[:string.index("(")]
		#print("( removed", string)
	string = re.sub("[^ÆØÅæøåa-zA-Z]", "", string).lower()
	string = multi_remove(string, ["vanlig", "usikker", "ukjent", "ikkebilde"])
	global fiske_arter
	for art in fiske_arter:
		if art in string:
			print(f"{art} | {string}")
			return art
	global ukjente_arter
	if string in ukjente_arter:
		ukjente_arter[string] = ukjente_arter[string]+1
	else:
		ukjente_arter[string] = 1
	return "annet"
			

#print(multi_remove("Hell o", [" "]))

READFILE = "havforsk.csv"
ENCODE = "Windows-1252"

raw_df = pd.read_csv(READFILE, delimiter=";", encoding=ENCODE, engine="python")
df = raw_df[['date', 'isValidated', 'validSpecie']].dropna(axis="index", inplace=False)

#Format the names of the valid species to remove as much misspelling as possible
#df['validSpecie'] = df['validSpecie'].map(lambda name : multi_remove(name, [" ", "(", ")", ",", "\"", ".", "«", "?", "vanlig", ":", "usikker", "ukjent", "-", "ikkebilde", "0"]))
df['validSpecie'] = df['validSpecie'].map(lambda name : normalize(name))
print(df)



df.dropna(axis="columns", inplace=True)
#df['validSpecie'] = df['validSpecie'].map(lambda name : name[0:6])



#Change date to only include the year
df['year'] = df['date'].map(lambda date: int(date[1:5]))
df.sort_values(by=['year'], inplace=True)
#print(df)



#df.head(10).plot(kind="bar", ylim=[2000, 2021])
#plt.show()



#Group and format data
grouped = df.groupby(["validSpecie", "year"]).count()
grouped.sort_values(by=['validSpecie'], inplace=True)
grouped.reset_index(inplace=True)
grouped.rename(columns={"date":"amount"}, inplace=True)
grouped.drop(columns=['isValidated'], inplace=True)
#print(grouped)
grouped.drop(grouped[grouped.amount < 5].index, inplace=True)
grouped.drop(grouped[grouped.year < 2017].index, inplace=True)
#print(grouped)

grouped.sort_values(by=['amount'], inplace=True, ascending=False)

print(grouped.describe().round(2))

#grouped.to_csv("test.csv")

#print((grouped.index))

#grouped.plot(kind="barh", x='validSpecie', y='amount')

fig, ax = plt.subplots()
grouped.pivot_table("amount", index="year", columns=["validSpecie"]).plot(kind="line" ,ax=ax)
plt.show()



#print(ukjente_arter)
#val_based_rev = {k: v for k, v in sorted(ukjente_arter.items(), key=lambda item: item[1], reverse=True)}
#print(val_based_rev)