import random
import leereglas as r
#import cartas as c
print('{0:^40}'.format("UNO :)"))

class jugador:
    def __init__(self,msjs):
        self.cartas = 0
        self.nums = []
        self.colrs = []
        self.pts = 0
        self.puntaje = []
        self.empieza = msjs['empieza']
        self.turno = msjs['turno']
        self.nc = msjs['nuevacarta']
        self.puededesafiar = False

    def cartasenmano(self,modo = 'visibles'):    #imprimir cartas del jugador
        c_jug = ''
        for i in range(self.cartas):
            match modo:
                case 'visibles':
                    c_jug += f'{fcarta(self.nums[i],self.colrs[i])} '
                case 'ocultas':
                    c_jug += '[] '
        if self.cartas==1: c_jug += f'{uno}'
        print('{0:^40}'.format(c_jug))

    def posibs(self):     #jugadas posibles como lista de i posibles
        global poss
        poss = []
        for i in range(self.cartas):
            if self.nums[i]==cmesa[0] or self.colrs[i]==cmesa[1] or self.colrs[i]==0:
                poss.append(i)
                

ingame = True
opcinicial = 0
separ = '\n----------------------------------------\n'
uno = '¡UNO!'
erroropc = 'Error: escribe el número correspondiente.'
msjs_us = {
    'empieza':'Tú empiezas.',
    'turno':'Tu turno.',
    'nuevacarta':'Robaste una nueva carta'
}
msjs_op = {
    'empieza':'Empieza tu oponente.',
    'turno':'Turno de tu oponente.',
    'nuevacarta':'Tu oponente robó una nueva carta'
}
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
def nuevacarta(jug,cant = 1):      #robar carta(s) del mazo
    global mnums
    for i in range(cant):
        cdelmazo = random.randrange(0,len(mnums)-1)
        jug.nums.append(mnums.pop(cdelmazo))
        jug.colrs.append(mcors.pop(cdelmazo))   #0=sin 1=amarillo 2=verde 3=rojo 4=azul
    return jug.cartas + cant
def cartavieja(jug):    #devolver c. al mazo y definir nueva carta en mesa
    global colorpre_com4
    if cmesa[0] >= 13:  cmesa[1] = 0
    mnums.append(cmesa[0])
    mcors.append(cmesa[1])
    cmesa[0] = jug.nums.pop(poss[numjug])
    if cmesa[0]==14: colorpre_com4 = cmesa[1]
    cmesa[1] = jug.colrs.pop(poss[numjug])
    return jug.cartas - 1
def reparto():          #reparto de cartas
    us.cartas = nuevacarta(us,7)
    op.cartas = nuevacarta(op,7)
def pricartamesa():   #primera carta volteada del mazo en mesa
    global cmesa
    cmesa = []
    cdelmazo = random.randrange(0,len(mnums))
    if mnums[cdelmazo] == 14:
        pricartamesa()
    else:
        cmesa.append(mnums.pop(cdelmazo))
        cmesa.append(mcors.pop(cdelmazo))
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
    global comentario, poss, cmesa
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
            op.cartas = nuevacarta(op,2)
            comentario = f'Le sumaste 2 cartas a tu oponente. '
        case 14:
            op.cartas = nuevacarta(op,4)
            comentario = f'Le sumaste 4 cartas a tu oponente. '
            op.puededesafiar = True
    comentario += us.turno
    if us.cartas>0:
        print(separ+f'\nComo jugaste una carta {simb(cmesa[0])}, puedes jugar de nuevo.')
        mesa()
def oppjuegadn():
    global comentario
    comentario = ''
    match cmesa[0]:
        case 12:
            us.cartas = nuevacarta(us,2)
            comentario = f'Tu oponente te sumó 2 cartas. '
        case 14:
            us.cartas = nuevacarta(us,4)
            comentario = f'Tu oponente te sumó 4 cartas. '
            us.puededesafiar = True
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
def misposibs():   #mostrar posbs al jugador con la lista de index jugables
    us.posibs()
    print('Estas son tus cartas que puedes jugar:')
    for i in range(0,len(poss)):
        print(f'{i}.',fcarta(us.nums[poss[i]],us.colrs[poss[i]]),end=' ')
    print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta.')
    if us.puededesafiar:
        print(f'También puedes escribir "{len(poss)+1}" para desafiar a tu oponente si sospechas que descartó el Comodín +4 ilegalmente.')
def mesa():         #imprimir mesa actual
    print(separ,'{0:^40}'.format(comentario),sep='\n',end='\n\n') # comentario del turno
    op.cartasenmano('ocultas')      # cartas del oponente (ocultas para el usuario)
    print('\n','{0:^40}'.format(fcarta(cmesa[0],cmesa[1])),'\n')    # carta volteada en el centro de la mesa
    us.cartasenmano()       # cartas del usuario
    print(separ)
def puntaje():
    print('\nPuntaje:    ','{0:^6}'.format('Tú'),'{0:^15}'.format('Tu oponente'))
    for i in range(rondas):
        print('{0:<12}'.format(f'Ronda {i+1}:  '),'{0:^6}'.format(us.puntaje[i]),'{0:^15}'.format(op.puntaje[i]))
def desafia(desafiante,desafiado):
    global comentario, colorpre_com4
    ilegal = False
    print('\nCartas del desafiado: \n')
    desafiado.cartasenmano()
    for i in range(desafiado.cartas):
        if desafiado.colrs[i]==colorpre_com4:
            ilegal = True
            break
    if ilegal:
        print('\nComo el desafiado tenía cartas que coincidían en color con la anterior carta en mesa, se confirma culpable.','{0:^40}'.format('El desafiante devuelve sus nuevas 4 cartas al mazo y el desafiado roba otras 4 en su lugar.'),sep='\n')
        for i in range(4):
            if desafiado == us:
                us.cartas = nuevacarta(us)
            else:
                op.cartas = nuevacarta(op)
            mnums.append(desafiante.nums.pop())
            mcors.append(desafiante.colrs.pop())
            desafiante.cartas -= 1
    else:
        print('\nComo el desafiado no tenía cartas que coincidieran en color con la anterior carta en mesa, se verifica inocente.','{0:^40}'.format('El desafiante roba 2 cartas adicionales.'),sep='\n')
        if desafiante == us:
            us.cartas = nuevacarta(us,2)
        else:
            op.cartas = nuevacarta(op,2)
    print()
    comentario = desafiante.turno
    desafiante.puededesafiar = False

#turnos
def turnoop():                  #turno oponente
    global cmesa, comentario, numjug
    if op.cartas>0:
        op.posibs()
        if op.puededesafiar:
            opdesafia = random.randint(1,4)
            if opdesafia==1:
                print('¡Tu oponente te desafió a mostrarle tus cartas para confirmar que descartaste tu Comodín +4 legalmente!')
                desafia(op,us)
                mesa()
            else: op.puededesafiar = False
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
    global cmesa, comentario, numjug, poss
    try:
        n_c_jug = us.nums[poss[numjug]]
    except IndexError:
        if numjug==len(poss):
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
        elif numjug==len(poss)+1:
            print(separ)
            print('¡Desafiaste a tu oponente!')
            desafia(us,op)
            mesa()
            misposibs()
            numjug = int(input())
            turnous()
    else:
        if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
            juegadenuevo()
            if us.cartas>0:
                misposibs()
                numjug = int(input())
                turnous()
        else:   cmesa = jugada()
    us.puededesafiar = False
def primerturno():              #primer turno
    global cmesa
    global comentario
    pricartamesa()
    if mano%2==0:
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
                    us.cartas = nuevacarta(us,2)
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
                    op.cartas = nuevacarta(op,2)
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
    

while ingame:
    while opcinicial!=1 or opcinicial!=2 or opcinicial!=3:
        print('\nSelecciona: ')
        for i in range(3):
            print('{0:^40}'.format(f'{i+1}. {opciones[4-i]}'))
        opcinicial = int(input())
        match opcinicial:
            case 1:
                rondas = 0
                us = jugador(msjs_us)           #usuario
                op = jugador(msjs_op)           #oponente
                mano = 2
                finforzado = False
                while us.pts<500 and op.pts<500:    # inicio del juego y rondas
                    mnums, mcors = [], []      #listas del mazo principal
                    us.cartas, op.cartas = 0, 0      #cantidad de cartas del jugador y del oponente
                    us.nums, us.colrs = [], []      #listas de nums y de colores de las cartas del jugador
                    op.nums, op.colrs = [], []      #listas de nums y de colores de las cartas del oponente
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
                    
                    primerturno()
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

                    while us.pts<500 and op.pts<500:
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
                                finforzado = True                                
                                break
                            case 3:
                                reglas()
                            case _:
                                print(erroropc)
                    if finforzado:
                        del us, op
                        break
                if not finforzado:
                    if us.pts>op.pts:
                        print(f'\n¡Felicidades! Ganaste el juego con {us.pts-op.pts} puntos de diferencia.')
                    else:
                        print(f'\nHas perdido por {op.pts-us.pts} puntos de diferencia.')
                    print('Así fueron los puntos durante la partida:\n')
                    puntaje()
                    print()
                    del us, op
                break
            case 2:
                reglas()
            case 3:
                ingame = False
                break
            case _:
                print(erroropc)