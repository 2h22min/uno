import random
import leereglas as r
import cartas as c
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
                    c_jug += f'{c.fcarta(self.nums[i],self.colrs[i])} '
                case 'ocultas':
                    c_jug += '[] '
        if self.cartas==1: c_jug += f'{uno}'
        print('{0:^40}'.format(c_jug))

    def posibs(self):     #jugadas posibles como lista de i posibles
        global poss
        poss = []
        for i in range(self.cartas):
            if self.nums[i]==c.cmesa[0] or self.colrs[i]==c.cmesa[1] or self.colrs[i]==0:
                poss.append(i)
                
ingame = True
opcinicial = 0
opcfinal = 4
numjug = 100
poss = []
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

#funciones internas del juego 
def reparto():          #reparto de cartas
    us.cartas = c.nuevacarta(us,7)
    op.cartas = c.nuevacarta(op,7)
def validinput(opc = numjug, priopc = 0, ultopc = 0):
    global poss
    if ultopc == 0:
        ultopc = len(poss)
    while True:
        opc = input()
        try:
            opc = int(opc)
            if opc==len(poss)+1:
                try:
                    assert (us.puededesafiar)
                except:
                    pass
                else:
                    ultopc += 1
            assert (opc>=priopc and opc<=ultopc), 'Número inválido: inténtalo de nuevo.'
        except ValueError:
            print(erroropc,end='\t')
        except AssertionError as numerr:
            print(numerr,end='\t')
        else:
            break
    return opc
def jugada():          #actúa jugada del usuario y devuelve prox. carta en mesa
    global comentario, numjug
    if numjug<len(poss):
        us.cartas = c.cartavieja(us,poss[numjug])
        while c.cmesa[1]==0:
            print('Elige el nuevo color:\n1. amarillo; 2. verde; 3. rojo; 4. azul')
            nuevocolor = input()
            try:
               assert(1<=int(nuevocolor)<=4), 'Error al escoger, inténtalo de nuevo con un número válido.'
               c.cmesa[1] = int(nuevocolor)
            except AssertionError as error:
                print(error)
            except ValueError:
                match nuevocolor:
                    case 'amarillo':
                        c.cmesa[1] = 1
                    case 'AMARILLO':
                        c.cmesa[1] = 1
                    case 'verde':
                        c.cmesa[1] = 2
                    case 'VERDE':
                        c.cmesa[1] = 2
                    case 'rojo':
                        c.cmesa[1] = 3
                    case 'ROJO':
                        c.cmesa[1] = 3
                    case 'azul':
                        c.cmesa[1] = 4
                    case 'AZUL':
                        c.cmesa[1] = 4
                    case _:
                        print('Error al escoger, inténtalo de nuevo.')
        comentario = op.turno
    else:
        us.cartas = c.nuevacarta(us)
        comentario = f'{us.nc}. {op.turno}'
    return c.cmesa
def oppjuega():        #juega el oponente "
    global comentario, poss, c, numjug
    if len(poss)>0:
        op.cartas = c.cartavieja(op,poss[numjug])
        if c.cmesa[1]==0: c.cmesa[1] = random.randint(1,4)
    else:
        op.cartas = c.nuevacarta(op)
        comentario = op.nc
        if op.nums[-1]==c.cmesa[0] or op.colrs[-1]==c.cmesa[1] or op.colrs[-1]==0:
            poss = [len(op.nums)-1,1]
            numjug = random.randrange(0,len(poss))
            if numjug == 0:
                comentario += f' y la descartó. {us.turno}'
                n_c_jug = op.nums[poss[numjug]]
                c.cmesa = oppjuega()
                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                    oppjuegadn()
                    turnoop()
            else:
                comentario += f'. {us.turno}'
        else:
            comentario += f'. {us.turno}'
    return c.cmesa
def juegadenuevo():     #si juega c. tipo 10, 11, 12 o 14 porque cancelan el siguiente turno del oponente
    global comentario
    c.cmesa = jugada()
    comentario = ''
    match c.cmesa[0]:
        case 12:
            op.cartas = c.nuevacarta(op,2)
            comentario = f'Le sumaste 2 cartas a tu oponente. '
        case 14:
            op.cartas = c.nuevacarta(op,4)
            comentario = f'Le sumaste 4 cartas a tu oponente. '
            op.puededesafiar = True
    comentario += us.turno
    if us.cartas>0:
        print(separ+f'\nComo jugaste una carta {c.simb(c.cmesa[0])}, puedes jugar de nuevo.')
        mesa()
def oppjuegadn():
    global comentario
    comentario = ''
    match c.cmesa[0]:
        case 12:
            us.cartas = c.nuevacarta(us,2)
            comentario = f'Tu oponente te sumó 2 cartas. '
        case 14:
            us.cartas = c.nuevacarta(us,4)
            comentario = f'Tu oponente te sumó 4 cartas. '
            us.puededesafiar = True
    comentario += op.turno
    if op.cartas>0:
        print(f'\nComo tu oponente jugó una carta {c.simb(c.cmesa[0])}, puede jugar de nuevo.')
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
        print(f'{i}.',c.fcarta(us.nums[poss[i]],us.colrs[poss[i]]),end=' ')
    print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta.')
    if us.puededesafiar:
        print(f'También puedes escribir "{len(poss)+1}" para desafiar a tu oponente si sospechas que descartó el Comodín +4 ilegalmente.')
def mesa():         #imprimir mesa actual
    print(separ,'{0:^40}'.format(comentario),sep='\n',end='\n\n') # comentario del turno
    op.cartasenmano('ocultas')      # cartas del oponente (ocultas para el usuario)
    print('\n','{0:^40}'.format(c.fcarta(c.cmesa[0],c.cmesa[1])),'\n')    # carta volteada en el centro de la mesa
    us.cartasenmano()       # cartas del usuario
    print(separ)
def puntaje():
    print('\nPuntaje:    ','{0:^6}'.format('Tú'),'{0:^15}'.format('Tu oponente'))
    for i in range(rondas):
        print('{0:<12}'.format(f'Ronda {i+1}:  '),'{0:^6}'.format(us.puntaje[i]),'{0:^15}'.format(op.puntaje[i]))
def desafia(desafiante,desafiado):
    global comentario, c
    ilegal = False
    print('\nCartas del desafiado: \n')
    desafiado.cartasenmano()
    for i in range(desafiado.cartas):
        if desafiado.colrs[i]==c.colorpre_com4:
            ilegal = True
            break
    if ilegal:
        print('\nComo el desafiado tenía cartas que coincidían en color con la anterior carta en mesa, se confirma culpable.','{0:^40}'.format('El desafiante devuelve sus nuevas 4 cartas al mazo y el desafiado roba otras 4 en su lugar.'),sep='\n')
        for i in range(4):
            if desafiado == us:
                us.cartas = c.nuevacarta(us)
            else:
                op.cartas = c.nuevacarta(op)
            c.mnums.append(desafiante.nums.pop())
            c.mcors.append(desafiante.colrs.pop())
            desafiante.cartas -= 1
    else:
        print('\nComo el desafiado no tenía cartas que coincidieran en color con la anterior carta en mesa, se verifica inocente.','{0:^40}'.format('El desafiante roba 2 cartas adicionales.'),sep='\n')
        if desafiante == us:
            us.cartas = c.nuevacarta(us,2)
        else:
            op.cartas = c.nuevacarta(op,2)
    print()
    comentario = desafiante.turno
    desafiante.puededesafiar = False

#turnos
def turnoop():                  #turno oponente
    global c, comentario, numjug
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
            c.cmesa = oppjuega()
            if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                oppjuegadn()
                turnoop()
            else: comentario = us.turno
        else:
            c.cmesa = oppjuega()
def turnous():                  #turno jugador
    global c, comentario, numjug, poss
    try:
        n_c_jug = us.nums[poss[numjug]]
    except IndexError:
        if numjug==len(poss):
            c.cmesa = jugada()
            if us.nums[-1]==c.cmesa[0] or us.colrs[-1]==c.cmesa[1] or us.colrs[-1]==0:
                comentario = op.turno
                poss = [len(us.nums)-1,1]
                print(f'Tu nueva carta es un {c.fcarta(us.nums[-1],us.colrs[-1])}, puedes jugarla escribiendo "0", o "1" para quedártela y pasar tu turno.')
                numjug = validinput(ultopc=1)
                if numjug == 0:
                    n_c_jug = us.nums[poss[numjug]]
                    comentario = f'{us.nc} y la descartaste. {op.turno}'
                    if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                        juegadenuevo()
                        if us.cartas>0:
                            misposibs()
                            numjug = validinput()
                            turnous()
                    else: c.cmesa = jugada()
                else:
                    comentario = f'{us.nc} y decidiste pasar tu turno. {op.turno}'
        elif numjug==len(poss)+1:
            print(separ)
            print('¡Desafiaste a tu oponente!')
            desafia(us,op)
            mesa()
            misposibs()
            numjug = validinput()
            turnous()
    else:
        if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
            juegadenuevo()
            if us.cartas>0:
                misposibs()
                numjug = validinput()
                turnous()
        else:   c.cmesa = jugada()
    us.puededesafiar = False
def primerturno():              #primer turno
    global c, comentario
    c.pricartamesa()
    if mano%2==0:
        comentario = us.empieza
        if c.cmesa[0]==13:
            comentario += f' {pc_accion} Comodín, juegas el primer color que quieras.'
            mesa()
            for i in range(us.cartas):
                poss.append(i)
            print('Estas son tus cartas que puedes jugar:')
            for i in range(len(poss)):
                print(f'{i}.',c.fcarta(us.nums[poss[i]],us.colrs[poss[i]]),end=' ')
            print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta.')
        elif c.cmesa[0]>9:
            comentario = f'{pc_accion} {c.simb(c.cmesa[0])}, '
            match c.cmesa[0]:
                case 12:
                    comentario += f'robas 2 cartas y pierdes el turno. '
                    us.cartas = c.nuevacarta(us,2)
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
        if c.cmesa[0]==13:
            comentario += f' {pc_accion} Comodín, juega el primer color que quiera.'
            mesa()
            for i in range(op.cartas):
                poss.append(i)
            while op.cartas>0:
                numjug = random.randrange(0,len(poss))
                n_c_jug = op.nums[poss[numjug]]
                c.cmesa = oppjuega()
                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                    oppjuegadn()
                    continue
                comentario = us.turno
                mesa()
                break
        elif c.cmesa[0]>9:
            comentario = f'{pc_accion} {c.simb(c.cmesa[0])}, '
            match c.cmesa[0]:
                case 12:
                    comentario += f'tu oponente roba 2 cartas y pierde el turno. '
                    op.cartas = c.nuevacarta(op,2)
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
        opcinicial = validinput(opcinicial,1,3)
        match opcinicial:
            case 1:
                rondas = 0
                us = jugador(msjs_us)           #usuario
                op = jugador(msjs_op)           #oponente
                mano = 2
                finforzado = False
                while us.pts<500 and op.pts<500:    # inicio del juego y rondas
                    us.cartas, op.cartas = 0, 0      #cantidad de cartas del jugador y del oponente
                    us.nums, us.colrs = [], []      #listas de nums y de colores de las cartas del jugador
                    op.nums, op.colrs = [], []      #listas de nums y de colores de las cartas del oponente
                    poss = []
                    reparto()
                    
                    primerturno()
                    while us.cartas>0 and op.cartas>0:
                        numjug = validinput()
                        turnous()
                        if us.cartas==0: break
                        mesa()
                        turnoop()
                        if op.cartas!=0:
                            mesa()
                            misposibs()

                    if c.cmesa[0]==12 or c.cmesa[0]==14:
                        if us.cartas<op.cartas:
                            comentario = f'Le sumaste {c.cmesa[0]-10} cartas a tu oponente.'
                        else:
                            comentario = f'Tu oponente te sumó {c.cmesa[0]-10} cartas.'
                    mesa()
                    print('Felicidades, ganaste.') if us.cartas<op.cartas else print('aprendé a jugar')
                    mano += 1
                    rondas += 1
                    sumarpuntos()

                    while us.pts<500 and op.pts<500:
                        print('\nSelecciona: ')
                        for i in range(4):
                            print('{0:^40}'.format(f'{i}. {opciones[i]}'))
                        opcfinal = validinput(opcfinal,0,3)
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
