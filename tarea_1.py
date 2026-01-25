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

##############

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
        
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        
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
        estado = self.x[self.indice_cuarto(piso, robot)]
        return robot, piso, estado


def test():
    """
    Prueba del entorno y los agentes

    """
    x0=["A", "sucio", "sucio"]
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoNuevecuartos(), 
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         100)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(x0), 
                         AgenteReactivoModeloNueveCuartosCiego(), 
                         100)


if __name__ == "__main__":
    test()


###############

# 2)

class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 
                'ir_B')


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')
    
    
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)


###############

# 3)

class NueveCuartosCiego(NueveCuartos):
    """
    Igual que DosCuartos, pero no se puede ver nada

    """
    def percepcion(self):
        return []


class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['?', 'sucio', 'sucio']

    def programa(self, _):
        
        # Decide sobre el modelo interno
        robot, a, b = self.modelo
        accion = ('ir_A' if robot == '?' else
                  'nada' if a == b == 'limpio' else
                  'limpiar' if self.modelo[' AB'.find(robot)] == 'sucio' else
                  'ir_A' if robot == 'B' else 'ir_B' 
                  
                  )

        # Actualiza el modelo interno
        if accion == 'ir_A':
            self.modelo[0] = 'A'
        elif accion == 'ir_B':
            self.modelo[0] = 'B'
        elif accion == 'limpiar':
            self.modelo[' AB'.find(robot)] = 'limpio'
            
        return accion

###############

# 4)