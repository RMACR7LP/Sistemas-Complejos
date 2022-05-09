import math
import random
import agentpy as ap
import matplotlib.pyplot as plt
import numpy as np


def limpieza_datos(datos):
    datos_completos = []
    for line in datos: 
        datos_jugador = []
        for number in line.split(", "):
            number = number.replace("\n", "")
            datos_jugador.append(float(number))
        datos_completos.append(datos_jugador)
    return datos_completos

with open('datos_gol_messi.txt', 'r') as f:
    datos = f.readlines()
datos = limpieza_datos(datos)

datos_2 = np.zeros([6, len(datos[0])])

for i in range(0, 6):
    datos_2[i:] = np.array(datos[i])

datos = 10*datos_2

#print(datos)
f.close()

# ----------------------------------Simulación Original----------------------------------------------

def normalizacion(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

class Jugador(ap.Agent):
    
    def setup_pos(self, espacio):
        self.espacio = espacio
        self.neighbors = espacio.neighbors   # .neighbors es un metodo de la clase Space que captura todo los vecinos dentro de una cierta distancia.
        self.pos = espacio.positions[self]   # .positions es una variable de la clase Space, es un diccionario que vincula a cada agente con sus coordenadas en el espacio.


    def cambio_posicion(self):
        id = self.id #el id comienza a contar desde 2

        # id == 2, Messi
        # id == 3, Lass
        # id == 4, Alonso
        # id == 5, Ramos
        # id == 6, Albiol
        # id == 7, Marcelo
        #print(datos[1])

        if id in range(2,8):
            #print(self.pos)
            tramo_AB = datos[id-2][-4]/10
            tramo_AC = (datos[id-2][-3]+datos[id-2][-4])/10
            tramo_AD = (datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/10
            tramo_AE = (datos[id-2][-1]+datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/10

            if self.model.t<=tramo_AB:
                self.velocidad = np.array([datos[id-2][2], datos[id-2][3]]) - np.array([datos[id-2][0], datos[id-2][1]])
                if id ==5 and self.model.t%2 == 0:
                    self.espacio.move_by(self, 13*self.velocidad/datos[id-2][-4])
                
                elif id == 7 and self.model.t%5 == 0:
                    self.espacio.move_by(self, 2*normalizacion(self.velocidad))

                else: 
                    self.espacio.move_by(self, 10*self.velocidad/datos[id-2][-4])

            if tramo_AB<self.model.t<=tramo_AC:    
                self.velocidad = np.array([datos[id-2][4], datos[id-2][5]]) - np.array([datos[id-2][2], datos[id-2][3]])
                if id == 5: 
                    self.espacio.move_by(self, 2*10*self.velocidad/datos[id-2][-3])
                elif id == 7:
                    self.espacio.move_by(self, 4.1*normalizacion(self.velocidad))
                else:
                    self.espacio.move_by(self, 10*self.velocidad/datos[id-2][-3])
                
            if tramo_AC <self.model.t<=tramo_AD:    
                self.velocidad = np.array([datos[id-2][6], datos[id-2][7]]) - np.array([datos[id-2][4], datos[id-2][5]])
                if datos[id-2][-2] != 0: 
                    if id == 7:
                        self.espacio.move_by(self, 4.2*normalizacion(self.velocidad))
                    else:
                        self.espacio.move_by(self, 10*self.velocidad / datos[id-2][-2])

            if tramo_AD <self.model.t<=tramo_AE:    
                self.velocidad = np.array([datos[id-2][8], datos[id-2][9]]) - np.array([datos[id-2][6], datos[id-2][7]])
                if datos[id-2][-1] != 0:
                    self.espacio.move_by(self, 10*self.velocidad / datos[id-2][-1])

    def probabilidad_de_gol(self):
        id = self.id
        h = 440+10
        w = 680 +10+10
        b = 73.2
        if id == 2:
            x = self.pos[0]
            y = self.pos[1]
            numerador = b*(h-y)
            denominador = (((w-b-2*x)**2/4 + (h-y)**2)*((w+b-2*x)**2/4 + (h-y)**2))**0.5
            angulo = np.arcsin(numerador/denominador)
            probabilidad = 1/(1+np.exp(4.03 - 2.53*angulo - 0.12*(h-y)/10 - 0.11*(h-y)/10*angulo + 0.0069*(h-y)**2/100))
            if self.model.t<=120:
                return probabilidad


class Poblacion_modelo(ap.Model):

    def setup(self):
        self.espacio = ap.Space(self, shape=[self.p.size]*self.p.dimension)
        self.agents = ap.AgentList(self, 10, Jugador) #creamos una cantidad |population| de agentes.
        self.espacio.add_agents(self.agents, [[406.6, 65], [420, 60] , [350, 65], [322, 169 ], [416.6, 169], [510, 180], [10,10], [690, 10], [690, 535], [10, 535]]) #metemos a los agentes creados en el espacio.
        self.agents.setup_pos(self.espacio)

    def step(self): 
        self.agents.cambio_posicion()    
        self.agents.probabilidad_de_gol()    
    

def animacion_individual(m, ax):
    ax.set_title(f"______{m.t}")
    
    pos = m.espacio.positions.values()
    #estados = []
    
    
    # for i in range(0,m.p.population-1):
    #     temporal = m.agents.log[i]
    #     if len(temporal)!=0:
    #         estados.append(temporal['estado']) #Esta es una lista con todos los estados que ha pasado el agente i
    pos = np.array(list(pos)).T 

    ax.scatter(pos[0][0],pos[1][0], s=50, c='blue', marker = "o")
    for j in range(1, 10):
        ax.scatter(pos[0][j],pos[1][j], s=50, c='black', marker = "o")

             
    ax.set_xlim(0, 700) #0.4*m.p.size)
    ax.set_ylim(0, 545) #0.5*m.p.size)
    ax.set_axis_off()
              


def animacion_completa(m, p):
    fig = plt.figure(figsize=(10,7))
    fig.patch.set_facecolor("green")
    ax = fig.add_subplot()
    animation = ap.animate(m(p), fig, ax, animacion_individual, **{"interval": 100} )
    plt.show()
    animation.save("Gol Messi.gif", "GIF")
    #return animation


# def grafico():
#     graf = plt.plot(np.arange(0,145), np.arange(0,145) , color = "blue", label = "Susceptibles")
#     plt.legend()
#     plt.show()


parameters = {
    'dimension': 2,
    'size': 700,
    'seed': 123,
    'steps': 120,
    'population': 81,
    'R': 1.5,
    'p_c': 0.033,
    'p_u': 0.2,
    'p_m': 0.15,
    'p_quedados' : 0.1,
    'distancia_al_borde': 3,
}


animacion_completa(Poblacion_modelo, parameters)
#grafico()


#--------------------------------------Simulación Alterada-----------------------------------



class Jugador_Simulado(ap.Agent):   

    def setup_pos_s(self, espacio):
        self.espacio = espacio
        self.neighbors = espacio.neighbors   # .neighbors es un metodo de la clase Space que captura todo los vecinos dentro de una cierta distancia.
        self.pos = espacio.positions[self]   # .positions es una variable de la clase Space, es un diccionario que vincula a cada agente con sus coordenadas en el espacio.


    def cambio_posicion_s(self):
        id = self.id #el id comienza a contar desde 2

        # id == 2, Messi
        # id == 3, Lass
        # id == 4, Alonso
        # id == 5, Ramos
        # id == 6, Albiol
        # id == 7, Marcelo
        #print(datos[1])

        if id in range(2,8) and id not in [5,6]:
            tramo_AB = datos[id-2][-4]/10
            tramo_AC = (datos[id-2][-3]+datos[id-2][-4])/10
            tramo_AD = (datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/10
            tramo_AE = (datos[id-2][-1]+datos[id-2][-2]+datos[id-2][-3]+datos[id-2][-4])/10

            if self.model.t<=tramo_AB:
                self.velocidad = np.array([datos[id-2][2], datos[id-2][3]]) - np.array([datos[id-2][0], datos[id-2][1]])
                if id == 7 and self.model.t%5 == 0:
                    self.espacio.move_by(self, 2*normalizacion(self.velocidad))

                else: 
                    self.espacio.move_by(self, 10*self.velocidad/datos[id-2][-4])

            if tramo_AB<self.model.t<=tramo_AC:    
                self.velocidad = np.array([datos[id-2][4], datos[id-2][5]]) - np.array([datos[id-2][2], datos[id-2][3]])
                if id == 7:
                    self.espacio.move_by(self, 4.1*normalizacion(self.velocidad))
                else:
                    self.espacio.move_by(self, 10*self.velocidad/datos[id-2][-3])
                
            if tramo_AC <self.model.t<=tramo_AD:    
                self.velocidad = np.array([datos[id-2][6], datos[id-2][7]]) - np.array([datos[id-2][4], datos[id-2][5]])
                if datos[id-2][-2] != 0: 
                    if id == 7:
                        self.espacio.move_by(self, 4.2*normalizacion(self.velocidad))
                    else:
                        self.espacio.move_by(self, 10*self.velocidad / datos[id-2][-2])

            if tramo_AD <self.model.t<=tramo_AE:    
                self.velocidad = np.array([datos[id-2][8], datos[id-2][9]]) - np.array([datos[id-2][6], datos[id-2][7]])
                if datos[id-2][-1] != 0:
                    self.espacio.move_by(self, 10*self.velocidad / datos[id-2][-1])

        if id in [5,6]:
            # Messi es zurdo 
            for i in range(3, 8):
                if abs(self.pos[0][1]-self.pos[0][i])>10: 
                    self.espacio.move_by(self, )



class Poblacion_modelo(ap.Model):

    def setup(self):
        self.espacio = ap.Space(self, shape=[self.p.size]*self.p.dimension)
        self.agents = ap.AgentList(self, 10, Jugador) #creamos una cantidad |population| de agentes.
        self.espacio.add_agents(self.agents, [[406.6, 65], [420, 60] , [350, 65], [322, 169 ], [416.6, 169], [510, 180], [10,10], [690, 10], [690, 535], [10, 535]]) #metemos a los agentes creados en el espacio.
        self.agents.setup_pos(self.espacio)

    def step(self): 
        self.agents.cambio_posicion()    
        self.agents.probabilidad_de_gol()    
    

def animacion_individual(m, ax):
    ax.set_title(f"______{m.t}")
    
    pos = m.espacio.positions.values()
    #estados = []
    
    
    # for i in range(0,m.p.population-1):
    #     temporal = m.agents.log[i]
    #     if len(temporal)!=0:
    #         estados.append(temporal['estado']) #Esta es una lista con todos los estados que ha pasado el agente i
    pos = np.array(list(pos)).T 

    ax.scatter(pos[0][0],pos[1][0], s=50, c='blue', marker = "o")
    for j in range(1, 10):
        ax.scatter(pos[0][j],pos[1][j], s=50, c='black', marker = "o")

             
    ax.set_xlim(0, 700) #0.4*m.p.size)
    ax.set_ylim(0, 545) #0.5*m.p.size)
    ax.set_axis_off()
              


def animacion_completa(m, p):
    fig = plt.figure(figsize=(10,7))
    fig.patch.set_facecolor("green")
    ax = fig.add_subplot()
    animation = ap.animate(m(p), fig, ax, animacion_individual, **{"interval": 100} )
    plt.show()
    animation.save("Gol Messi.gif", "GIF")
    #return animation


# def grafico():
#     graf = plt.plot(np.arange(0,145), np.arange(0,145) , color = "blue", label = "Susceptibles")
#     plt.legend()
#     plt.show()


parameters = {
    'dimension': 2,
    'size': 700,
    'seed': 123,
    'steps': 120,
    'population': 81,
    'R': 1.5,
    'p_c': 0.033,
    'p_u': 0.2,
    'p_m': 0.15,
    'p_quedados' : 0.1,
    'distancia_al_borde': 3,
}


animacion_completa(Poblacion_modelo, parameters)
#grafico()
