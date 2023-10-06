import decimal as d

def vat_faktura(lista):
    return round(0.23 * sum(lista), 2)

def vat_paragon(lista):
    return round(sum(0.23 * val for val in lista), 2)


def vat_faktura_d(lista):
    return round(d.Decimal('0.23') * sum(lista), 2)

def vat_paragon_d(lista):
    return round(sum(d.Decimal('0.23') * val for val in lista), 2)

print(vat_faktura([1,1.5,10]) == vat_paragon([1,1.5,10,3]))
print(vat_faktura_d([d.Decimal('1'), d.Decimal('1.5'),d.Decimal('10')]) == vat_paragon_d([d.Decimal('1'), d.Decimal('1.5'),d.Decimal('10')]))