def factorial(n):
  resultado = 1
  for i in range(2,n+1):
    resultado *= i
  return resultado

def conbinaciones(n,m):
  return (factorial(n)/(factorial(n-m) * factorial(m)))# cuantas conbinacione se pueden hacer de m con n

print conbinaciones(10,2)

