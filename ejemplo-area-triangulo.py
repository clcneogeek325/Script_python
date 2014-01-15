def area_triangulo(base,altura):
  area = base * altura / 2.0
  return area

base = float(raw_input("Ingresa la base :"))
altura = float(raw_input("Ingresa la altura : "))

area_final = area_triangulo(base,altura)

print area_final
