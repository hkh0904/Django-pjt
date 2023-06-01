import requests
import json

end = []

for i in range(10):
    url = f"https://api.themoviedb.org/3/movie/popular?include_adult=false&language=ko-KR&page={i+1}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NWFkNmQ4NTE3YmUxZDAxZjEwYWNiZGE5MzczY2E2YiIsInN1YiI6IjYzZDMxYmQ2Y2I3MWI4MDBkNDNhNzA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XzbupQeJ7SvUZiiIj8pih7HIC8i1R2Il2VEsqcqn2_Q"
    }
    requestData = requests.get(url, headers=headers)    

    # print(requestData.text)
        
    jsonData = requestData.json()
    for result in jsonData['results']:
        tot = {}
        
        tot['fields'] = result
        tot["model"] = "movies.movie" 
        end.append(tot)

    with open('./algorithm.json','w', encoding='utf-8') as f:
        json.dump(end, f, ensure_ascii=False, indent=4)