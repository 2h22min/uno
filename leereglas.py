def printr():
    print()
    for i in sec_reglas:
        print('{0:^40}'.format(f'{i}. {sec_reglas[i]}'))
    
def leer(selec):
    try:
        selec = int(selec)
    except ValueError:
        selec = False
    else:
        if selec>=0 and selec<=5:
            match selec:
                case 0:
                    p, f = 0, 4
                case 1:
                    p, f = 5, 13
                case 2:
                    p, f = 14, 18
                case 3:
                    p, f = 19, 43
                case 4:
                    p, f = 44, 54
                case 5:
                    p, f = 55, 58
            with open(r'reglas.txt','r') as r:
                texto = r.readlines()
                for i in range(p,f):
                    print(texto[i].strip())
            printr()
            selec = True
        else:
            selec = False
    return selec

sec_reglas = {
    0:'Objetivo del juego',
    1:'Cómo se juega',
    2:'Inicio de ronda',
    3:'Cartas de acción',
    4:'Puntos',
    5:'Fuentes',
    '-':'Volver'
}