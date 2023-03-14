import random
print('{0:^40}'.format("UNO :)"))

ingame = True
selec = 0
ptsj, ptso = 0, 0
empieza = 2
separ = '\n----------------------------------------\n'
uno = '¡UNO!'
turop = "Turno de tu oponente.\n"
turus = 'Tu turno.\n'
ncop = f'Tu oponente tomó una nueva carta y pasó su turno. Tu turno.\n'
ncus = f'Tomaste una nueva carta y pasaste tu turno. Turno de tu oponente.\n'
empop = 'Empieza tu oponente.'
empus = 'Tú empiezas.'
pc_accion = 'Como la primera carta volteada de la ronda es un'
opciones = {
    0:'Nueva ronda (continuar)',
    1:'Ver puntuación',
    2:'Salir',
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
def nuevacarta(nums,colors,intc):      #robar carta del mazo
    global mnums
    cdelmazo = random.randrange(0,len(mnums))
    nums.append(mnums.pop(cdelmazo))
    colors.append(mcors.pop(cdelmazo))   #0=sin 1=amarillo 2=verde 3=rojo 4=azul
    return intc + 1
def cartavieja(nums,colors,intc):    #devolver c. al mazo y definir nueva carta en mesa
    if cmesa[0] >= 13:  cmesa[1] = 0
    mnums.append(cmesa[0])
    mcors.append(cmesa[1])
    cmesa[0], cmesa[1] = nums.pop(poss[numjug]), colors.pop(poss[numjug])
    return intc - 1
def pricartamesa():   #primera carta volteada del mazo en mesa
    global cmesa
    cmesa = []
    cdelmazo = random.randrange(0,len(mnums))
    if mnums[cdelmazo] == 14:
        pricartamesa()
    else:
        cmesa.append(mnums.pop(cdelmazo))
        cmesa.append(mcors.pop(cdelmazo))
def posibs(nums,colors):     #jugadas posibles como lista de i posibles
    global poss
    poss = []
    for i in range(0,len(nums)):
        if nums[i]==cmesa[0] or colors[i]==cmesa[1] or colors[i]==0:
            poss.append(i)
def jugada():          #actúa jugada del usuario y devuelve prox. carta en mesa
    global cartas
    global comentario
    if numjug<len(poss):
        cartas = cartavieja(mazoN,mazoC,cartas)
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
        comentario = turop
    else:
        cartas = nuevacarta(mazoN,mazoC,cartas)
        comentario = ncus
    return cmesa
def oppjuega():        #juega el oponente "
    global cartas_opp
    global comentario
    if len(poss)>0:
        cartas_opp = cartavieja(oppN,oppC,cartas_opp)
        if cmesa[1]==0: cmesa[1] = random.randint(1,4)
    else:
        cartas_opp = nuevacarta(oppN,oppC,cartas_opp)
        comentario = ncop
    return cmesa
def juegadenuevo():     #si juega c. tipo 10, 11, 12 o 14 porque cancelan el siguiente turno del oponente
    global comentario
    global cartas_opp
    cmesa = jugada()
    match cmesa[0]:
        case 12:
            for i in range(2):
                cartas_opp = nuevacarta(oppN,oppC,cartas_opp)
            comentario = f'Le sumaste 2 cartas a tu oponente. {turus}'
        case 14:
            for i in range(4):
                cartas_opp = nuevacarta(oppN,oppC,cartas_opp)
            comentario = f'Le sumaste 4 cartas a tu oponente. {turus}'
        case _:
            comentario = turus
    if cartas>0:
        print(separ+f'\nComo jugaste una carta {simb(cmesa[0])}, puedes jugar de nuevo.')
        mesa()    
def oppjuegadn():
    global comentario
    global cartas
    match cmesa[0]:
        case 12:
            for i in range(2):
                cartas = nuevacarta(mazoN,mazoC,cartas)
            comentario = f'Tu oponente te sumó 2 cartas. {turop}'
        case 14:
            for i in range(4):
                cartas = nuevacarta(mazoN,mazoC,cartas)
            comentario = f'Tu oponente te sumó 4 cartas. {turop}'
        case _:
            comentario = turop
    if cartas_opp>0:
        print(f'\nComo tu oponente jugó una carta {simb(cmesa[0])}, puede jugar de nuevo.')
        mesa()    

#funciones con imp en pantalla
def tirar():       #tirar (imprimir en el centro) carta en la mesa
    print()
    print('{0:^40}'.format(fcarta(cmesa[0],cmesa[1])))
    print()
def cartasopp():      #imprimir cartas del oponente
    c_op = ''
    for i in range(cartas_opp):
        c_op += '[] '
    if cartas_opp==1: c_op += f'{uno}'
    print('\n','{0:^40}'.format(c_op))
def miscartas():          #imprimir cartas del jugador
    c_us = ''
    for i in range(cartas):
        c_us += f'{fcarta(mazoN[i],mazoC[i])} '
    if cartas==1: c_us += f'{uno}'
    print('{0:^40}'.format(c_us),separ,sep='\n')
def misposibs():   #mostrar posbs al jugador con la lista de index jugables
    posibs(mazoN,mazoC)
    print('Estas son tus cartas que puedes jugar:')
    for i in range(0,len(poss)):
        print(f'{i}.',fcarta(mazoN[poss[i]],mazoC[poss[i]]),end=' ')
    print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta y pasar esta ronda.')
def mesa():
    print(separ,'{0:^40}'.format(comentario),sep='\n')
    cartasopp()
    tirar()
    miscartas()            

#turnos
def turnoop():                  #turno oponente+imprime mesa
    global cmesa
    global comentario
    global numjug
    if cartas_opp>0:
            posibs(oppN,oppC)
            if len(poss)>0:
                numjug = random.randrange(0,len(poss))
                n_c_jug = oppN[poss[numjug]]
                cmesa = oppjuega()
                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                    oppjuegadn()
                    turnoop()
                else: comentario = turus
            else:
                cmesa = oppjuega()
def turnous():                  #turno jugador sin mesa
    global cmesa
    global numjug
    if cartas>0:
        try:
            n_c_jug = mazoN[poss[numjug]]
        except IndexError:
            cmesa = jugada()
        else:
            if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                juegadenuevo()
                if cartas>0:
                    misposibs()
                    numjug = int(input())
                    turnous()
            else:   cmesa = jugada()


while ingame:
    print('Selecciona: ')
    for i in range(3):
        print('{0:^40}'.format(f'{i+1}. {opciones[4-i]}'))
    while selec!=1 or selec!=2 or selec!=3:
        selec = int(input())
        match selec:
            case 1:
                while ptsj<500 and ptso<500:
                    mnums, mcors = [], []      #listas del mazo principal
                    cartas, cartas_opp = 0, 0      #cantidad de cartas del jugador y del oponente
                    mazoN, mazoC = [], []      #listas de nums y de colores de las cartas del jugador
                    oppN, oppC = [], []       #lista de nums y de colores de las cartas del oponente
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
                    for i in range(7):              #reparto de cartas
                        cartas = nuevacarta(mazoN,mazoC,cartas)
                        cartas_opp = nuevacarta(oppN,oppC,cartas_opp)
                    pricartamesa()
                    if empieza%2==0:
                        comentario = empus
                        if cmesa[0]==13:
                            comentario += f' {pc_accion} Comodín, juegas el primer color que quieras.'
                            mesa()
                            for i in range(cartas):
                                poss.append(i)
                            print('Estas son tus cartas que puedes jugar:')
                            for i in range(len(poss)):
                                print(f'{i}.',fcarta(mazoN[poss[i]],mazoC[poss[i]]),end=' ')
                            print(f'\nEscógela escribiendo el número correspondiente, o "{len(poss)}" para tomar una nueva carta y pasar esta ronda.')
                        elif cmesa[0]>9:
                            comentario = f'{pc_accion} {simb(cmesa[0])}, '
                            match cmesa[0]:
                                case 12:
                                    comentario += f'robas 2 cartas y pierdes el turno. '
                                    for i in range(2):
                                        cartas = nuevacarta(mazoN,mazoC,cartas)
                                case 11:
                                    comentario += f'empieza el repartidor de cartas. '
                                case 10:
                                    comentario += f'pierdes el turno. '
                            comentario += empop
                            mesa()
                            turnoop()
                            mesa()
                            misposibs()
                        else:
                            mesa()
                            misposibs()
                    else:
                        comentario = empop
                        if cmesa[0]==13:
                            comentario += f' {pc_accion} Comodín, juega el primer color que quiera.'
                            mesa()
                            for i in range(cartas_opp):
                                poss.append(i)
                            while cartas_opp>0:
                                numjug = random.randrange(0,len(poss))
                                n_c_jug = oppN[poss[numjug]]
                                cmesa = oppjuega()
                                if n_c_jug==10 or n_c_jug==11 or n_c_jug==12 or n_c_jug==14:
                                    oppjuegadn()
                                    continue
                                comentario = turus
                                mesa()
                                break
                        elif cmesa[0]>9:
                            comentario = f'{pc_accion} {simb(cmesa[0])}, '
                            match cmesa[0]:
                                case 12:
                                    comentario += f'tu oponente roba 2 cartas y pierde el turno. '
                                    for i in range(2):
                                        cartas_opp = nuevacarta(oppN,oppC,cartas_opp)
                                case 11:
                                    comentario += f'empieza el repartidor de cartas. '
                                case 10:
                                    comentario += f'tu oponente pierde el turno. '
                            comentario += empus
                            mesa()
                        else:
                            mesa()
                            turnoop()
                            mesa()
                        misposibs()
                    
                    while cartas>0 and cartas_opp>0:
                        numjug = int(input())
                        turnous()
                        if cartas==0: break
                        mesa()
                        turnoop()                       #turno oponente
                        if cartas_opp!=0:
                            mesa()
                            misposibs()
                    if cmesa[0]==12 or cmesa[0]==14:
                        if cartas<cartas_opp:
                            comentario = f'Le sumaste {cmesa[0]-10} cartas a tu oponente.'
                        else:
                            comentario = f'Tu oponente te sumó {cmesa[0]-10} cartas.'
                    mesa()
                    if cartas<cartas_opp:
                        print('Felicidades, ganaste.')
                    else:
                        print('aprendé a jugar')
                    empieza += 1
            case 2:
                #print('Escoge sección de las reglas para leer: ')
                #for i in sec_reglas:
                    #print('{0:^40}'.format(sec_reglas[i]))
                print('En esta versión todavía nop')
                break
            case 3:
                ingame = False
                break
            case _:
                print('Error: escribe el número correspondiente.')
                break
            
