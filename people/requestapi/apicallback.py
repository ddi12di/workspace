import requests



def get_all():
	response = requests.get("https://jsonplaceholder.typicode.com/posts")
	return response.json()

def get_only(id):
	response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}").json()
	return response


