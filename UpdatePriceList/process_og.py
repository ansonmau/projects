def findByDomain (domain:str, data:list[str]) -> list[str]:
	ans = []
	if len(data) > 0:
		for s in data:
			d = s.split(',')
			i = 3
			n = 0
			while (i < len(d)):
				if domain in d[i]:
					n+=1
				i+=1
			if n > 0:
				ans.append(d[0] + ":" + str(n))
	return ans


def emailsByAge(lower:int,upper:int,data:list[str]) -> list[float]:
	ans = [lower]
	if len(data) > 0:
		sorted = [[] for i in range(upper-lower+1)]
		for s in data:
			d = s.split(',')
			age = int(d[1])
			numEmails = len(d) - 3
			if (age <= upper and age >= lower):
				sorted[age - lower].append(numEmails)
		for i in sorted:
			if len(i) > 0:
				total = 0
				for j in i:
					total += j
				ans.append(total / len(i))
			else:
				ans.append(0)
	return ans 


data = ["cat,12,no meta, c@carleton.ca, c@gmail, c@cmail.carleton.ca, c@yahoo.ca\n", "anson, 19, no meta, a@email.ca, asd@cd.ca, gsa@gmail.ca",
"kafia, 12, meta, p@gmail.ca, asd@gmail.ca, asgas@hotmail.ca, adgf@carleton.ca, carleton@gmail.com"]
print(findByDomain("gmail", data))
print(emailsByAge(11,20,data))