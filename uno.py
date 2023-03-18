import random
import leereglas as r
print('{0:^40}'.format("UNO :)"))

class jugador:
    def __init__(self,msjempieza,msjturno,comnuevac):
        self.cartas = 0
        self.nums = []
        self.colrs = []
        self.pts = 0
        self.puntaje = []
        self.empieza = msjempieza
        self.turno = msjturno
        self.nc = comnuevac
us = jugador('Tú empiezas.','Tu turno.\n','Robaste una nueva carta')                      #usuario
op = jugador('Empieza tu oponente.','Turno de tu oponente.\n','Tu oponente robó una nueva carta')  #oponente

ingame = True
rondas = 0
opcinicial = 0
mano = 2
separ = '\n----------------------------------------\n'
uno = '¡UNO!'
erroropc = 'Error: escribe el número correspondiente.'
pc_accion = 'Como la primera carta volteada de la ronda es un'
opciones = {
    0:'Nueva ronda (continuar)',
    1:'Ver puntaje',
    2:'Terminar',
    3:'Revisar reglas',
    4:'Comenzar juego'
}

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

#funciones internas del juego 
def nuevacarta(jug):      #robar carta del mazo
    global mnums
    cdelmazo = random.randrange(0,len(mnums))
    jug.nums.append(mnums.pop(cdelmazo))
    jug.colrs.append(mcors.pop(cdelmazo))   #0=sin 1=amarillo 2=verde 3=rojo 4=azul
    return jug.cartas + 1
def cartavieja(jug):    #devolver c. al mazo y definir nueva carta en mesa
    if cmesa[0] >= 13:  cmesa[1] = 0
    mnums.append(cmesa[0])
    mcors.append(cmesa[1])
    cmesa[0], cmesa[1] = jug.nums.pop(poss[numjug]), jug.colrs.pop(poss[numjug])
    return jug.cartas - 1
def reparto():          #reparto de cartas
    for i in range(7):
        us.cartas = nuevacarta(us)
        op.cartas = nuevacarta(op)
def pricartamesa():   #primera carta volteada del mazo en mesa
    global cmesa
    cmesa = []
    cdelmazo = random.randrange(0,len(mnums))
    if mnums[cdelmazo] == 14:
        pricartamesa()
    else:
        cmesa.append(mnums.pop(cdelmazo))
        cmesa.append(mcors.pop(cdelmazo))
def posibs(jug):     #jugadas posibles como lista de i posibles
    global poss
    poss = []
    for i in range(0,len(jug.nums)):
        if jug.nums[i]==cmesa[0] or jug.colrs[i]==cmesa[1] or jug.colrs[i]==0:
            poss.append(i)
def jugada():          #actúa jugada del usuario y devuelve prox. carta en mesa
    global comentario
    if numjug<len(poss):
        us.cartas = cartavieja(us)
        while cmesa[1]==0:
            print('Elige el nuevo color:\n1. amarillo; 2. verde; 3. rojo; 4. azul')
            nuevocolor = input('')
            try:
               assert(1<=int(nuevocolor)<=4), 'Error al escoger, inténtalo de nuevo con un número válido.'
               cmesa[1] = int(nuevocolor)
            except AssertionError as error:
                print(error)
            except ValueError:
                match nuevocolor:
                    case 'amarillo':
                        cmesa[1] = 1
                    case 'AMARILLO':
                        cmesa[1] = 1
                    case 'verde':
                        cmesa[1] = 2
                    case 'VERDE':
                        cmesa[1] = 2
                    case 'rojo':
                        cmesa[1] = 3
                    case 'ROJO':
                        cmesa[1] = 3
                    case 'azul':
                        cmesa[1] = 4
                    case 'AZUL':
                        cmesa[1] = 4
                    case _:
                        print('Error al escoger, inténtalo de nuevo.')
        comentario = op.turno
    else:
        us.cartas = nuevacarta(us)
        comentario = f'{us.nc}. {op.turno}'
    return cmesa
def oppjuega():        #juega el oponente "
    global comentario
    global poss
    global cmesa
    if len(poss)>0:
        op.cartas = cartavieja(op)
        if cmesa[1]==0: cmesa[1] = random.randint(1,4)
    else:
        op.cartas = nuevacarta(op)
        comentario = op.nc
        if op.nums[-1]==cmesa[0] or op.colrs[-1]==cmesa[1] or op.colrs[-1]==0:
            poss = [len(op.nums)-1,1]
            numjug = random.randrange(0,len(poss))
            if numjug == 0:
                comentario += f' y la descartó. {us.turno}'
                n_c_jug = op.nums[poss[numjug]]
                cmesa = oppjuega()
                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                    oppjuegadn()
                    turnoop()
            else:
                comentario += f'. {us.turno}'
        else:
            comentario += f'. {us.turno}'
    return cmesa
def juegadenuevo():     #si juega c. tipo 10, 11, 12 o 14 porque cancelan el siguiente turno del oponente
    global comentario
    cmesa = jugada()
    comentario = ''
    match cmesa[0]:
        case 12:
            for i in range(2):
                op.cartas = nuevacarta(op)
            comentario = f'Le sumaste 2 cartas a tu oponente. '
        case 14:
            for i in range(4):
                op.cartas = nuevacarta(op)
            comentario = f'Le sumaste 4 cartas a tu oponente. '
    comentario += us.turno
    if us.cartas>0:
        print(separ+f'\nComo jugaste una carta {simb(cmesa[0])}, puedes jugar de nuevo.')
        mesa()
def oppjuegadn():
    global comentario
    comentario = ''
    match cmesa[0]:
        case 12:
            for i in range(2):
                us.cartas = nuevacarta(us)
            comentario = f'Tu oponente te sumó 2 cartas. '
        case 14:
            for i in range(4):
                us.cartas = nuevacarta(us)
            comentario = f'Tu oponente te sumó 4 cartas. '
    comentario += op.turno
    if op.cartas>0:
        print(f'\nComo tu oponente jugó una carta {simb(cmesa[0])}, puede jugar de nuevo.')
        mesa()    
def sumarpuntos():
    if us.cartas<op.cartas:
        for i in op.nums:
            if i<10:
                us.pts += i
            elif i<13:
                us.pts += 20
            else:
                us.pts += 50
    else:
        for i in us.nums:
            if i<10:
                op.pts += i
            elif i<13:
                op.pts += 20
            else:
                op.pts += 50
    us.puntaje.append(us.pts)
    op.puntaje.append(op.pts)

#funciones con imp en pantalla
def reglas():
    leer = True
    print('Escoge sección de las reglas para leer: ')
    r.printr()
    while leer:
        leer_reg = input()
        leer = r.leer(leer_reg)
def tirar():       #tirar (imprimir en el centro) carta en la mesa
    print()
    print('{0:^40}'.format(fcarta(cmesa[0],cmesa[1])))
    print()
def cartasopp():      #imprimir cartas del oponente
    c_op = ''
    for i in range(op.cartas):
        c_op += '[] '
    if op.cartas==1: c_op += f'{uno}'
    print('\n','{0:^40}'.format(c_op))
def miscartas():          #imprimir cartas del jugador
    c_us = ''
    for i in range(us.cartas):
        c_us += f'{fcarta(us.nums[i],us.colrs[i])} '
    if us.cartas==1: c_us += f'{uno}'
    print('{0:^40}'.format(c_us),separ,sep='\n')
def misposibs():   #mostrar posbs al jugador con la lista de index jugables
    posibs(us)
    print('Estas son tus cartas que puedes jugar:')
    for i in range(0,len(poss)):
        print(f'{i}.',fcarta(us.nums[poss[i]],us.colrs[poss[i]]),end=' ')
    print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta.')
def mesa():
    print(separ,'{0:^40}'.format(comentario),sep='\n')
    cartasopp()
    tirar()
    miscartas()            
def puntaje():
    print('\nPuntaje:  ','{0:^6}'.format('Tú'),'{0:^15}'.format('Tu oponente'))
    for i in range(rondas):
        print(f'Ronda {i+1}:  ','{0:^6}'.format(us.puntaje[i]),'{0:^15}'.format(op.puntaje[i]))
    
#turnos
def turnoop():                  #turno oponente
    global cmesa
    global comentario
    global numjug
    if op.cartas>0:
        posibs(op)
        if len(poss)>0:
            numjug = random.randrange(0,len(poss))
            n_c_jug = op.nums[poss[numjug]]
            cmesa = oppjuega()
            if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                oppjuegadn()
                turnoop()
            else: comentario = us.turno
        else:
            cmesa = oppjuega()
def turnous():                  #turno jugador
    global cmesa
    global comentario
    global numjug
    global poss
    try:
        n_c_jug = us.nums[poss[numjug]]
    except IndexError:
        cmesa = jugada()
        if us.nums[-1]==cmesa[0] or us.colrs[-1]==cmesa[1] or us.colrs[-1]==0:
            comentario = op.turno
            poss = [len(us.nums)-1,1]
            print(f'Tu nueva carta es un {fcarta(us.nums[-1],us.colrs[-1])}, puedes jugarla escribiendo "0", o "1" para quedártela y pasar tu turno.')
            numjug = int(input())
            if numjug == 0:
                n_c_jug = us.nums[poss[numjug]]
                comentario = f'{us.nc} y la descartaste. {op.turno}'
                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                    juegadenuevo()
                    if us.cartas>0:
                        misposibs()
                        numjug = int(input())
                        turnous()
                else: cmesa = jugada()
            else:
                comentario = f'{us.nc} y decidiste pasar tu turno. {op.turno}'
    else:
        if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
            juegadenuevo()
            if us.cartas>0:
                misposibs()
                numjug = int(input())
                turnous()
        else:   cmesa = jugada()


while ingame:
    while opcinicial!=1 or opcinicial!=2 or opcinicial!=3:
        print('Selecciona: ')
        for i in range(3):
            print('{0:^40}'.format(f'{i+1}. {opciones[4-i]}'))
        opcinicial = int(input())
        match opcinicial:
            case 1:
                while us.pts<500 and op.pts<500:
                    mnums, mcors = [], []      #listas del mazo principal
                    us.cartas, op.cartas = 0, 0      #cantidad de cartas del jugador y del oponente
                    us.nums, us.colrs = [], []      #listas de nums y de colores de las cartas del jugador
                    op.nums, op.colrs = [], []       #lista de nums y de colores de las cartas del oponente
                    poss = []
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
                    reparto()
                    pricartamesa()
                    if mano%2==0:                           #1er turno
                        comentario = us.empieza
                        if cmesa[0]==13:
                            comentario += f' {pc_accion} Comodín, juegas el primer color que quieras.'
                            mesa()
                            for i in range(us.cartas):
                                poss.append(i)
                            print('Estas son tus cartas que puedes jugar:')
                            for i in range(len(poss)):
                                print(f'{i}.',fcarta(us.nums[poss[i]],us.colrs[poss[i]]),end=' ')
                            print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta.')
                        elif cmesa[0]>9:
                            comentario = f'{pc_accion} {simb(cmesa[0])}, '
                            match cmesa[0]:
                                case 12:
                                    comentario += f'robas 2 cartas y pierdes el turno. '
                                    for i in range(2):
                                        us.cartas = nuevacarta(us)
                                case 11:
                                    comentario += f'empieza el repartidor de cartas. '
                                case 10:
                                    comentario += f'pierdes el turno. '
                            comentario += op.empieza
                            mesa()
                            turnoop()
                            mesa()
                            misposibs()
                        else:
                            mesa()
                            misposibs()
                    else:
                        comentario = op.empieza
                        if cmesa[0]==13:
                            comentario += f' {pc_accion} Comodín, juega el primer color que quiera.'
                            mesa()
                            for i in range(op.cartas):
                                poss.append(i)
                            while op.cartas>0:
                                numjug = random.randrange(0,len(poss))
                                n_c_jug = op.nums[poss[numjug]]
                                cmesa = oppjuega()
                                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                                    oppjuegadn()
                                    continue
                                comentario = us.turno
                                mesa()
                                break
                        elif cmesa[0]>9:
                            comentario = f'{pc_accion} {simb(cmesa[0])}, '
                            match cmesa[0]:
                                case 12:
                                    comentario += f'tu oponente roba 2 cartas y pierde el turno. '
                                    for i in range(2):
                                        op.cartas = nuevacarta(op)
                                case 11:
                                    comentario += f'empieza el repartidor de cartas. '
                                case 10:
                                    comentario += f'tu oponente pierde el turno. '
                            comentario += us.empieza
                            mesa()
                        else:
                            mesa()
                            turnoop()
                            mesa()
                        misposibs()
                    
                    while us.cartas>0 and op.cartas>0:
                        numjug = int(input())
                        turnous()
                        if us.cartas==0: break
                        mesa()
                        turnoop()
                        if op.cartas!=0:
                            mesa()
                            misposibs()

                    if cmesa[0]==12 or cmesa[0]==14:
                        if us.cartas<op.cartas:
                            comentario = f'Le sumaste {cmesa[0]-10} cartas a tu oponente.'
                        else:
                            comentario = f'Tu oponente te sumó {cmesa[0]-10} cartas.'
                    mesa()
                    print('Felicidades, ganaste.') if us.cartas<op.cartas else print('aprendé a jugar')
                    mano += 1
                    rondas += 1
                    sumarpuntos()

                    while True:
                        print('\nSelecciona: ')
                        for i in range(4):
                            print('{0:^40}'.format(f'{i}. {opciones[i]}'))
                        opcfinal = int(input())
                        match opcfinal:
                            case 0:
                                break
                            case 1:
                                puntaje()
                            case 2:
                                print(f'Juego terminado después de {rondas} rondas.')
                                puntaje()
                                if us.pts>op.pts:
                                    print(f'Ganaste con {us.pts-op.pts} puntos de diferencia. Felicidades:)')
                                elif op.pts>us.pts:
                                    print(f'Ganó tu oponente con {op.pts-us.pts} puntos de diferencia.')
                                else:
                                    print('El juego acabó en un empate.')
                                us.pts, op.pts = 500, 500
                                ingame = False
                                break
                            case 3:
                                reglas()
                            case _:
                                print(erroropc)
            case 2:
                reglas()
            case 3:
                ingame = False
                break
            case _:
                print(erroropc)