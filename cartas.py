import random
mnums, mcors = [], []      #listas del mazo principal                   
for i in range(1,5):    #mazo: cartas 0 y cambios color (4 cada)
    mnums.append(13) #13 = cartas cambio de color
    mcors.append(0)
    mnums.append(14) #14 = cartas " " " +4
    mcors.append(0)  #0 = color negro/todos
    mnums.append(0)
    mcors.append(i)  #i: color de las cartas
for j in range(1,13):   #cartas con color aparte de los 0 (8 cada)
    for i in range(1,5):
        for l in range(2):
            mnums.append(j)  #10 = saltear jugador, 11 = invierte sentido, 12 = +2
            mcors.append(i)

#funciones de formatación
def simb(n):        #convertir símbolo de carta int->str
    match n:
        case 10:
            s = 'Skip'
        case 11:
            s = 'Reversa'
        case 12:
            s = '+2'
        case 13:
            s = 'Comodín'
        case 14:
            s = 'Comodín +4'
        case _:
            s = str(n)
    return s
def color(C):           #convertir color de carta int->str
    match C:
        case 1:
            color = ' amarillo'
        case 2:
            color = ' verde'
        case 3:
            color = ' rojo'
        case 4:
            color = ' azul'
        case 0:
            color = ''
    return color
fcarta = lambda nu,co:'[{}{}]'.format(simb(nu),color(co))

def pricartamesa():   #primera carta volteada del mazo en mesa
    global cmesa
    cmesa = []
    cdelmazo = random.randrange(0,len(mnums))
    if mnums[cdelmazo] == 14:
        pricartamesa()
    else:
        cmesa.append(mnums.pop(cdelmazo))
        cmesa.append(mcors.pop(cdelmazo))
def nuevacarta(jug,cant = 1):      #robar carta(s) del mazo
    global mnums
    for i in range(cant):
        cdelmazo = random.randrange(0,len(mnums)-1)
        jug.nums.append(mnums.pop(cdelmazo))
        jug.colrs.append(mcors.pop(cdelmazo))   #0=sin 1=amarillo 2=verde 3=rojo 4=azul
    return jug.cartas + cant
def cartavieja(jug,carta):    #devolver c. al mazo y definir nueva carta en mesa
    global colorpre_com4
    if cmesa[0] >= 13:  cmesa[1] = 0
    mnums.append(cmesa[0])
    mcors.append(cmesa[1])
    cmesa[0] = jug.nums.pop(carta)
    if cmesa[0]==14: colorpre_com4 = cmesa[1]
    cmesa[1] = jug.colrs.pop(carta)
    return jug.cartas - 1
