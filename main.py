import math
import random
import copy


def mutatie(cromozom, pozitii):
    mutatie = ""
    for i in range(len(cromozom)):
        if cromozom[i] == "0" and i in pozitii and pozitii.count(i) % 2 == 1:
            mutatie += "1"
        elif cromozom[i] == "1" and i in pozitii and pozitii.count(i) % 2 == 1:
            mutatie += "0"
        else:
            mutatie += cromozom[i]
    return mutatie


def incrucisare(biti1, biti2, i): #pt3 incrucisare intre 1,2 si 1,3
    bit1nou = biti1[:i] + biti2[i:]
    bit2nou = biti2[:i] + biti1[i:]
    return bit1nou, bit2nou


def codificare(numar, a, b, p):
    l = int(math.log((b-a)*(10**p), 2)) + 1
    interval_size = (b - a) / (2 ** l)
    index = int((float(numar) - a) // interval_size)
    binar = format(index, f'0{l}b')
    return binar


def decodificare(binar, a, b):
    p = len(binar)
    interval_size = (b - a) / (2 ** p)
    index = int(binar, 2)
    numar = a + index * interval_size
    return "{:.4f}".format(numar)


def f(x, a, b, c):
    return a*x*x + b*x + c


def find_interval(number, intervals):
    for i in range(len(intervals) - 1):
        if intervals[i] <= number < intervals[i + 1]:
            return i

nrcromozomi = 20#int(input())
a = -1#int(input())
b = 2#int(input())
c1 = -2#int(input())
c2 = 3#int(input())
c3 = 4#int(input())
p = 6#int(input())
probabilitate_recomb = 0.25#float(input())
probabilitate_mutatie = 0.01#float(input())
nr_etape = 50#int(input())




populatie = [codificare(random.uniform(a,b), a, b, p) for _ in range(nrcromozomi)]


populatiedecod = [decodificare(x, a, b) for x in populatie]


fx = [f(float(x),c1,c2,c3) for x in populatiedecod]

file = open("evolutie.txt", "w")
file.write("Populatie Initiala:\n")
for i in range(len(populatie)):
    file.write(str(i+1) + ": " + populatie[i] + "      x = " + populatiedecod[i] + "      f(x) = " + str(fx[i]) + "\n")

file.write("\n\n\n\n\n")

sumfx = sum(fx)

probabilitate_selectie = [fx[i]/sumfx for i in range(len(fx))]

file.write("Probabilitati Selectie:\n")
for i in range(len(probabilitate_selectie)):
    file.write("cromozom " + str(i+1) + ": " + str(probabilitate_selectie[i]) + "\n")

intervale_selectie = [0]
sumsl = 0

for i in range(len(probabilitate_selectie)):
    sumsl += probabilitate_selectie[i]
    intervale_selectie.append(sumsl)

file.write("\n\n\n\n\n")
file.write("Intervale de selectie:\n")
for i in range(len(intervale_selectie)):
    file.write(str(intervale_selectie[i]) + "\n")

selectie = []
for i in range(len(probabilitate_selectie)):
    selectat = random.uniform(0,1)
    file.write("u = " + str(selectat))
    cromozom_selectat = find_interval(selectat, intervale_selectie)
    file.write("    selectam cromozomul " + str(cromozom_selectat+1) + "\n")
    selectie.append(populatie[cromozom_selectat])

file.write("\n\n\n\n\n")

recombinari = []
for i in range(len(selectie)):
    recombinat = random.uniform(0,1)
    file.write(str(i+1) + ": " + str(selectie[i]) + "   u = " + str(recombinat))
    if recombinat <= probabilitate_recomb:
        recombinari.append(selectie[i])
        file.write(" < " + str(probabilitate_recomb) + "  =>Este ales")
    file.write("\n")

#print(selectie)
recombinaricopie = recombinari.copy()
descos = []
#print(recombinaricopie)
for i in range(len(selectie)):
    if selectie[i] in recombinaricopie:
        recombinaricopie.remove(selectie[i])
        descos.append(selectie[i])
for i in descos:
    selectie.remove(i)
#print(selectie)
#print(recombinaricopie)
#print(recombinari)

recombinari1 = []

if len(recombinari)%2==0:
    for i in range(0,len(recombinari),2):
        cr1,cr2 = incrucisare(recombinari[i],recombinari[i+1],1)
        recombinari1.append(cr1)
        recombinari1.append(cr2)
else:
    for i in range(0,len(recombinari)-3,2):
        cr1,cr2 = incrucisare(recombinari[i],recombinari[i+1],1)
        recombinari1.append(cr1)
        recombinari1.append(cr2)
    i1 = len(recombinari)-1
    i2 = len(recombinari)-2
    i3 = len(recombinari)-3
    cr1,cr2 = incrucisare(recombinari[i3],recombinari[i2],1)
    cr1,cr3 = incrucisare(cr1,recombinari[i1],1)
    recombinari1.append(cr1)
    recombinari1.append(cr2)
    recombinari1.append(cr3)

#print(recombinari1)
selectie += recombinari1
#print(selectie)

file.write("\n\n\n\n\n")
file.write("Populatia dupa incrucisari:\n")
for i in range(len(selectie)):
    file.write(str(i+1) + ": " + selectie[i] + "\n")


file.write("\n\n\n\n\n")
file.write("Populatia care muteaza:\n")
for i in range(len(selectie)):
    mut = random.uniform(0,1)
    file.write(str(i + 1) + ": " + str(selectie[i]) + "   u = " + str(mut))
    if mut <= probabilitate_mutatie:
        poz_mut = [int(random.uniform(0,22)) for i in range(3)]
        selectie[i] = mutatie(selectie[i], poz_mut)
        file.write(" < " + str(probabilitate_mutatie) + "  =>Este ales")
    file.write("\n")


rezultat = [decodificare(x, a, b) for x in selectie]
#print(rezultat)
fx = [f(float(x),c1,c2,c3) for x in rezultat]
#print(fx)

file.write("\n\n\n\n\n")
file.write("Populatie noua:\n")
for i in range(len(selectie)):
    file.write(str(i+1) + ": " + selectie[i] + "      x = " + rezultat[i] + "      f(x) = " + str(fx[i]) + "\n")


file.write("Maxim = " + str(max(fx)) + "        Medie = " + str(sum(fx)/len(fx)) + "\n")

populatie = selectie

for _ in range(nr_etape*4):
    populatiedecod = [decodificare(x, a, b) for x in populatie]

    fx = [f(float(x), c1, c2, c3) for x in populatiedecod]

    maxim = 0
    for x in populatiedecod:
        if f(float(x), c1, c2, c3) == max(fx):
            maxim = x
    maxim = codificare(maxim, a, b, p)

    sumfx = sum(fx)

    probabilitate_selectie = [fx[i] / sumfx for i in range(len(fx))]

    intervale_selectie = [0]
    sumsl = 0

    for i in range(len(probabilitate_selectie)):
        sumsl += probabilitate_selectie[i]
        intervale_selectie.append(sumsl)

    selectie = []
    for i in range(len(probabilitate_selectie)-1):
        selectat = random.uniform(0, 1)
        cromozom_selectat = find_interval(selectat, intervale_selectie)
        selectie.append(populatie[cromozom_selectat])

    recombinari = []
    for i in range(len(selectie)):
        recombinat = random.uniform(0, 1)
        if recombinat <= probabilitate_recomb:
            recombinari.append(selectie[i])

    # print(selectie)
    recombinaricopie = recombinari.copy()
    descos = []
    # print(recombinaricopie)
    for i in range(len(selectie)):
        if selectie[i] in recombinaricopie:
            recombinaricopie.remove(selectie[i])
            descos.append(selectie[i])
    for i in descos:
        selectie.remove(i)
    # print(selectie)
    # print(recombinaricopie)
    # print(recombinari)

    recombinari1 = []
    pctrupere = int(random.uniform(0,len(selectie[0])))
    if len(recombinari) % 2 == 0:
        for i in range(0, len(recombinari), 2):
            cr1, cr2 = incrucisare(recombinari[i], recombinari[i + 1], pctrupere)
            recombinari1.append(cr1)
            recombinari1.append(cr2)
    elif len(recombinari) % 2 == 1 and len(recombinari) > 1:
        for i in range(0, len(recombinari) - 3, 2):
            cr1, cr2 = incrucisare(recombinari[i], recombinari[i + 1], pctrupere)
            recombinari1.append(cr1)
            recombinari1.append(cr2)
        i1 = len(recombinari) - 1
        i2 = len(recombinari) - 2
        i3 = len(recombinari) - 3
        #print(i3,i2)
        cr1, cr2 = incrucisare(recombinari[i3], recombinari[i2], pctrupere)
        cr1, cr3 = incrucisare(cr1, recombinari[i1], pctrupere)
        recombinari1.append(cr1)
        recombinari1.append(cr2)
        recombinari1.append(cr3)
    else:
        recombinari1.append(recombinari[0])
    # print(recombinari1)
    selectie += recombinari1
    # print(selectie)

    for i in range(len(selectie)):
        mut = random.uniform(0, 1)
        if mut <= probabilitate_mutatie:
            poz_mut = [int(random.uniform(0, 22)) for i in range(3)]
            selectie[i] = mutatie(selectie[i], poz_mut)

    rezultat = [decodificare(x, a, b) for x in selectie]
    #print(rezultat)
    fx = [f(float(x), c1, c2, c3) for x in rezultat]
    #print(fx)
    #print(max(fx), "       ", sum(fx)/len(fx))
    file.write("Maxim = "+ str(max(fx)) + "        Medie = " + str(sum(fx) / len(fx)) + "\n")
    selectie.append(maxim)
    populatie = selectie