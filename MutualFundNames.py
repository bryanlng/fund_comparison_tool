"""
Purpose: Grab names of EVERY mutual fund out there
Should return a sorted list of every mutual fund out there, in their ticket symbols
Ex: ["ABNYX", "AMTRX", ...]

Use https://www.marketwatch.com/tools/mutual-fund/list?firstLetter=A, except do it for every letter

Process:
1. For every letter:
	1. Make a call to https://www.marketwatch.com/tools/mutual-fund/list?firstLetter=<letter_in_caps>
	2. Scrape symbol names, and add them to our list
2. Sort the list, then return
3. Export to a file..?
"""

import requests
from bs4 import BeautifulSoup


class MutualFundNames:
	def get_all_fund_names(self):
		#Generate list of all alphabetical letters in letter_in_caps
		# letters = self.generate_alphabet()
		letters = ["A"]

		#For every letter, 1) make a call to the url, 2) Scrape symbol names, 3) Add to list only if they are a mutual fund (symbol name == 5 lettesr)
		names = []
		base_url = "https://www.marketwatch.com/tools/mutual-fund/list?firstLetter="
		for letter in letters:
			try:
				raw = requests.get(base_url + letter)

				if raw != None:
					soup = BeautifulSoup(raw.text, 'html.parser')

					#Scrape symbol names. Find the table, then get all td tags that have class name "quotelist-symb" only if they are a mutual fund
					table = soup.find("table")
					rows = table.findAll("td", class_="quotelist-symb")
					for row in rows:
						symbol = str(row.text)
						if len(symbol) == 5:
							names.append(symbol)

			except Exception as e: # Not good to have a catch-all exception, but I'll create custom exceptions later
				print(e)

		#Sort in ascending
		names = sorted(names)

		#Print to external file
		with open("mutual_fund_names.txt", "w") as text_file:
			for name in names:
				text_file.write(name + "\n")

	def generate_alphabet(self):
		"""
		A-Z is in ascii ranges 65-90
		Instead of manually typing out an array, use a list comprehension to generate it
		http://www.asciitable.com/
		https://stackoverflow.com/questions/227459/ascii-value-of-a-character-in-python
		"""
		return [str(chr(num)) for num in range(65,90)]

m = MutualFundNames()
m.get_all_fund_names()