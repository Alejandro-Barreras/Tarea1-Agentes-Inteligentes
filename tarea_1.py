#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'alejandro_barreras'

import entornos_f
import entornos_o

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python



######################################################################################



# 1) Nueve Cuartos


from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de 9 cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, piso, A1, B1, C1, A2, B2, C2, A3, B3, C3)
    donde robot puede tener los valores "A", "B", "C"
    piso puede tener los valores 1, 2, 3
    A1, B1, C1, A2, B2, C2, A3, B3, C3 pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Izquierda", 
    "ir_Derecha", "subir", "bajar", "limpiar", "nada").
    No todas las acciones son válidas en todos los estados.

    La acción "subir" solo es legal en los primeros dos pisos y cuando el
    robot está en el cuarto C. La acción "bajar" solo es legal en los
    segundos y terceros pisos y cuando el robot está en el cuarto A.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", 1, 
                           "sucio", "sucio", "sucio",
                           "sucio", "sucio", "sucio",
                           "sucio", "sucio", "sucio"]):
        
        """

        Por default inicialmente el robot está en el cuarto A, en el primer piso
        y todos los cuartos están sucios

        """
        self.x = x0[:]
        self.costo = 0
    
    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)

    def accion_legal(self, accion):
        robot = self.x[0] 
        piso = self.x[1]

        if accion in ("limpiar", "nada"):
            return True
        if accion == "ir_Izquierda":
            return robot != "A"
        if accion == "ir_Derecha":
            return robot != "C"
        if accion == "subir":
            return piso < 3 and robot == "C"
        if accion == "bajar":
            return piso > 1 and robot == "A"
        
        return False

    def transicion(self, accion):
        robot = self.x[0]
        piso = self.x[1]
        
        if not self.accion_legal(accion):
            self.costo += 5
            return
        
        if accion == "limpiar":
            self.costo += 1
        elif accion == "ir_Izquierda":
            self.costo += 2
        elif accion == "ir_Derecha":
            self.costo += 2
        elif accion == "subir":
            self.costo += 3
        elif accion == "bajar":
            self.costo += 3

        if accion == "limpiar":
            i = self.indice_cuarto(piso, robot)
            self.x[i] = "limpio"
        elif accion == "ir_Izquierda":
            self.x[0] = "ABC"[ "ABC".find(robot) - 1 ]
        elif accion == "ir_Derecha":
            self.x[0] = "ABC"[ "ABC".find(robot) + 1 ]
        elif accion == "subir":
            self.x[1] += 1
        elif accion == "bajar":
            self.x[1] -= 1

    def percepcion(self):
        robot = self.x[0]
        piso = self.x[1]
        situacion = self.x[self.indice_cuarto(piso, robot)]
        return robot, piso, situacion



######################################################################################



# 2) Agentes reactivos y agente aleatorio


class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepcion):
        robot, piso, situacion = percepcion
        if situacion == 'sucio':
            return 'limpiar'
        elif robot == 'A' and piso > 1:
            return 'bajar'
        elif robot == 'C' and piso < 3:
            return 'subir'
        elif robot != 'C':
            return 'ir_Derecha'
        else:
            return 'ir_Izquierda'


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 1,
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']
    
    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)

    def programa(self, percepcion):
        robot, piso, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[1] = piso
        self.modelo[self.indice_cuarto(piso, robot)] = situacion

        # Decide sobre el modelo interno
        return (
            'nada' if 'sucio' not in self.modelo[2:] else
            'limpiar' if situacion == 'sucio' else
            'ir_Izquierda' if robot != 'A' and 'sucio' in self.modelo[self.indice_cuarto(piso, 'A'):
                                                                      self.indice_cuarto(piso, robot)] else
            'ir_Derecha' if robot != 'C' else
            'subir' if piso < 3 else 
            'nada'
            )
    
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)



######################################################################################



# 3)


class NueveCuartosCiego(NueveCuartos):
    """
    Igual que DosCuartos, pero no se puede ver nada

    """
    def percepcion(self):
        robot = self.x[0]
        piso = self.x[1]

        return robot, piso, '?'


class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Agente reactivo basado en modelo (ciego)
    """

    def __init__(self):
        self.modelo = ['A', 1,
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']

    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)

    def programa(self, percepcion):
        robot, piso, _ = percepcion

        # Decide sobre el modelo interno
        accion = (
            'nada'
            if 'sucio' not in self.modelo[2:] else
            'ir_Derecha'
            if robot == '?' else
            'limpiar'
            if self.modelo[self.indice_cuarto(piso, robot)] == 'sucio' else
            'subir'
            if robot == 'C' and piso < 3 else
            'bajar'
            if robot == 'A' and piso > 1 else
            'ir_Derecha'
            if robot != 'C' else
            'ir_Izquierda'
        )

        # Actualiza el modelo interno
        if robot == '?':
            self.modelo[0] = 'A'
            self.modelo[1] = 1

        elif accion == 'ir_Derecha':
            self.modelo[0] = "ABC"["ABC".find(robot) + 1]

        elif accion == 'ir_Izquierda':
            self.modelo[0] = "ABC"["ABC".find(robot) - 1]

        elif accion == 'subir':
            self.modelo[1] += 1

        elif accion == 'bajar':
            self.modelo[1] -= 1

        elif accion == 'limpiar':
            i = self.indice_cuarto(piso, robot)
            self.modelo[i] = 'limpio'

        return accion





######################################################################################



# 4)




######################################################################################



# Pruebas:

def test():
    """
    Prueba del entorno y los agentes

    """
    x0=["A", 1,
         "sucio", "sucio", "sucio",
         "sucio", "sucio", "sucio",
         "sucio", "sucio", "sucio"]
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir',
                                          'bajar', 'limpiar', 'nada']),
                         200)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(NueveCuartos(x0), 
    #                    AgenteReactivoNuevecuartos(), 
    #                     200)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(x0), 
                         AgenteReactivoModeloNueveCuartosCiego(), 
                         200)


if __name__ == "__main__":
    test()
