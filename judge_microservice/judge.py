from typing import final
import mysql.connector
from pprint import pprint
import requests
import subprocess
import os
from decouple import config

USER = config('DB_USER')
PASS = config('DB_PASS')


MEDIA_URL = "http://127.0.0.1:8000/media/"

mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  password=PASS,
  database="seeroj1"
)

mycursor = mydb.cursor()

SUBMISSION_FETCH_QUERY = '''SELECT * from seer_submission WHERE status = "In Queue" LIMIT 1'''

mycursor.execute(SUBMISSION_FETCH_QUERY)

myresult = mycursor.fetchall()
print("Myresult: ")
print(myresult)

for x in myresult:
	sub_id = x[0]
	RUNNING_QUERY = f'UPDATE seer_submission SET status = "RUNNING" WHERE id = "{sub_id}"'
	mycursor.execute(RUNNING_QUERY)
	mydb.commit()
	code = x[1]
	language = x[2]
	problem_id = x[4]
	# print(language, problem_id, code)
	PROBLEM_IO_QUERY = f"SELECT * from seer_problem WHERE id = {problem_id}"
	mycursor.execute(PROBLEM_IO_QUERY)
	problem_details = mycursor.fetchall()[0]
	print(PROBLEM_IO_QUERY)
	print(problem_details)
	inp_path = problem_details[8]
	op_path = problem_details[9]
	inp_url = MEDIA_URL+inp_path
	op_url = MEDIA_URL+op_path
	r = requests.get(inp_url, allow_redirects=True)
	open("inp.txt", "wb").write(r.content)
	r = requests.get(op_url, allow_redirects=True)
	open("op.txt", "wb").write(r.content)
	open("code.py", "w").write(code)
	print("Starting execution...")
	rv1 = os.system("python code.py < inp.txt > our_op.txt")
	rv2 = os.system("fc /a /w op.txt our_op.txt > our_verdict.txt")

	final_verdict = "Wrong Answer"

	if(rv1==0 and rv2==0):
		final_verdict = "Accepted"

	if(rv1!=0):
		final_verdict = "Runtime Error"
	
	UPDATE_QUERY = f'UPDATE seer_submission SET status = "{final_verdict}" WHERE id = {sub_id}'
	print(UPDATE_QUERY)

	mycursor.execute(UPDATE_QUERY)
	mydb.commit()