import json

data = "[{\"imagen\":\"C:\\fakepath\\ranger-verde.jpeg\",\"nombre\":\"Agustin\",\"email\":\"agu.quiroz@tipddy.cl\",\"linkedin\":\"https://www.linkedin.com/AgustinQuiroz98\",\"cargo\":\"Full-Stack Web Developer\",\"empresa\":\"Coding Dojo\"}]"

new_data = json.loads(data)
print(new_data)

[
  {
    'imagen': 'C:\x0cakepath\ranger-verde.jpeg', 
    'nombre': 'Agustin', 'email': 'agu.quiroz@tipddy.cl', 
    'linkedin': 'https://www.linkedin.com/AgustinQuiroz98', 
    'cargo': 'Full-Stack Web Developer', 
    'empresa': 'Coding Dojo'
  }
]