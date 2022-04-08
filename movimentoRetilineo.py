'''
  __  __  _____     _____ __  __ _____ _   _ _____ ___    ____  _____ _____ ___ _      __ _   _ _____ ___  
 |  \/  |/ _ \ \   / /_ _|  \/  | ____| \ | |_   _/ _ \  |  _ \| ____|_   _|_ _| |    /_/| \ | | ____/ _ \ 
 | |\/| | | | \ \ / / | || |\/| |  _| |  \| | | || | | | | |_) |  _|   | |  | || |   |_ _|  \| |  _|| | | |
 | |  | | |_| |\ V /  | || |  | | |___| |\  | | || |_| | |  _ <| |___  | |  | || |___ | || |\  | |__| |_| |
 |_|  |_|\___/  \_/  |___|_|  |_|_____|_| \_| |_| \___/  |_| \_\_____| |_| |___|_____|___|_| \_|_____\___/  0.3.3

'''                                                                                                        
from vpython import *
from threading import Thread
import random, time

class RectilinearMovement:
    def __init__(self) -> None:
        self.WIDTH = 1200
        self.setInitialValues()
        self.createObjects()
        self.setupScene()
        self.createWidgets()
        self.createGraph()
        self.updateGraphs()
        self.run_thread = Thread(target = self.run)
        self.object_ace_variation_thread = Thread(target = self.sortAceVariationValue)
        self.graph_thread = Thread(target = self.updateGraphsThread)
        self.screen_thread = Thread(target = self.updateScreen)
    '''
        ┌─┐┬ ┬┌┐┌┌─┐┌─┐┌─┐┌─┐  ┌┬┐┌─┐  ┌─┐┬─┐┬┌─┐┌─┐┌─┐┌─┐
        ├┤ │ │││││  │ │├┤ └─┐   ││├┤   │  ├┬┘│├─┤│  ├─┤│ │
        └  └─┘┘└┘└─┘└─┘└─┘└─┘  ─┴┘└─┘  └─┘┴└─┴┴ ┴└─┘┴ ┴└─┘
    '''
    def setInitialValues(self):
        # definição dos valores iniciais
        self.t  = 0
        self.dt = .01
        self.object_ace = vector(0,0,0)
        self.object_vel = vector(0,0,0)
        self.object_initial_vel = vector(0,0,0)
        self.object_initial_pos = vector(0,1,0)
        self.object_ace_variation = vector(0,0,0)
        self.object_avarage_speed = vector(0,0,0)
        self.running = False
        self.isInitial = True 

    def createObjects(self):
        # esfera
        self.object = sphere(pos = vector(0,1,0), radius = 1, color = color.red)
        
        # criação e configuração da seta de aceleração
        self.ace_right_arrow = arrow(pos = vector(self.object.pos.x - (self.object.radius / 2 ), self.object.pos.y + 1.5, self.object.pos.z))
        self.ace_right_arrow.visible = False
        self.ace_left_arrow = arrow(pos = vector(self.object.pos.x + (self.object.radius / 2), self.object.pos.y + 1.5, self.object.pos.z))
        self.ace_left_arrow.rotate(1*pi, vector(0,1,0))
        self.ace_left_arrow.visible = False

        # criação e configuração da seta da velocidade
        self.vel_right_arrow = arrow(pos = vector(self.object.pos.x + (self.object.radius * 1.5) , self.object.pos.y, self.object.pos.z), length = 2)
        self.vel_left_arrow = arrow(pos = vector(self.object.pos.x - (self.object.radius * 1.5) , self.object.pos.y, self.object.pos.z), length = 2)
        self.vel_left_arrow.rotate(pi, vector(0,1,0))
        self.vel_right_arrow.visible = False
        self.vel_left_arrow.visible = False

        # criação e configuração do texto sobre as setas velocidade e aceleração   
        self.vel_text = label(text = str(self.t), height = 20, box = False, line = False, opacity = 0)
        self.ace_text = label(text = str(self.t), height = 20, box = False, line = False, opacity = 0)
        self.ace_text.align = 'center'
        self.ace_text.visible = False
        self.vel_text.visible = False

        # chão abaixo da esfera
        self.ground = box(pos = vector(0,-2.5, 0), size = vector(70, 5,2), color = color.white, texture={
            'file':textures.wood,
            'bumpmap':bumpmaps.stucco,
            'place':['right', 'sides'],
            'flipx':True,
            'flipy':True,
            'turn':-3})
        
    def setupScene(self):
        # largura da cena
        scene.width = self.WIDTH
        
        # configurar camera para seguir esfera
        scene.follow(self.object)

    def createWidgets(self):
        # vSpace() -> espaço na vertical
        # hSpace() -> espaço na horizontal
        self.vSpace(1)
       
        # texto velocidade
        self.velocity_label = wtext(text = "Velocidade Inicial:")
        self.hSpace(2)
       
        # caixa de texto para a inserção da velocidade
        self.object_velocity_input = winput(bind = self.nothing, type = "numeric", width = 50, _height = 20)
        self.hSpace(3)
       
        # texto acereleração
        self.object_ace_label = wtext(text = "Aceleração Inicial:")
        self.hSpace(2)
       
        # caixa de texto para a inserção da aceleração
        self.object_ace_input = winput(bind = self.nothing, type = "numeric", width = 50, _height = 20)
        self.hSpace(3)

        # botão de iniciar a animação junto com os graficos
        self.run_button = button(bind = self.start, text = "Executar")
        self.hSpace(3)

        # botão de iniciar a animação junto com os graficos
        self.pause_button = button(bind = self.pause, text = "Pausar")
        self.hSpace(3)

        # botão para reiniciar todos os valores
        self.reset_button = button(bind = self.reset, text = "Resetar")
        self.hSpace(5)
        self.vSpace(2)

        # texto acereleração
        self.object_ace_variation_label = wtext(text = "Variação da aceleração:", width = 500)
        self.vSpace(2)
    
        # slider variação da aceleração
        self.object_ace_variation_slider = slider(bind = self.updateAceVariationSliderInfo , step = 1, min = -10, max = 10, length = 1100)
        self.object_ace_variation_slider.value = 0

        self.vSpace(2)
        self.current_object_ace_variation_info = wtext(text = f"{str(self.object_ace_variation_slider.value)}m/s²")

        self.vSpace(3)
        # texto "Posição X = "
        self.object_pos_x_label = wtext(text = "Posição X = ")
        self.hSpace(1)
        
        # texto informando a posição X em tempo real
        self.object_pos_x_info = wtext(text = f"{self.object.pos.x}m")
        self.hSpace(3)
        
        # texto "Tempo = "
        self.time_label = wtext(text = "Tempo = ")
        self.hSpace(1)
        
        # texto informando a o tempo em tempo real
        self.time_info = wtext(text = f"{self.t}s")
        self.hSpace(3)

        # texto "Tempo = "
        self.object_avarage_speed_label = wtext(text = "Velocidade média = ")
        self.hSpace(1)

        self.object_avarage_speed_info = wtext(text = f"{self.object_avarage_speed.x}m/s")
        self.hSpace(1)

        self.vSpace(1)
        wtext(text = " ")
        self.vSpace(1)
    '''
        ┌─┐┬ ┬┌┐┌┌─┐┌─┐┌─┐┌─┐  ┌┬┐┌─┐  ┌─┐┌─┐┬  ┌─┐┬ ┬┬  ┌─┐┌─┐
        ├┤ │ │││││  │ │├┤ └─┐   ││├┤   │  ├─┤│  │  │ ││  │ │└─┐
        └  └─┘┘└┘└─┘└─┘└─┘└─┘  ─┴┘└─┘  └─┘┴ ┴┴─┘└─┘└─┘┴─┘└─┘└─┘
    '''
    def start(self):
        # captura a velocidade informada pelo usuario
        if self.isInitial: 
            if self.object_velocity_input.text != '':
                self.object_vel.x = float((self.object_velocity_input.text))
            else:
                self.object_vel.x = 0
            self.isInitial = False
            self.object_velocity_input.disabled = True         

        # captura a aceleração informada pelo usuario
        if self.object_ace_input.text != '':
            self.object_ace.x = float((self.object_ace_input.text))
        else:
            self.object_ace.x = 0
        
        # aumenta o valor x do grafico 2 | 5 posições a mais do valor maximo informado
        if self.object_vel.x > self.graph2_config.xmax:
            self.graph2_config.xmax = self.object_vel.x + 5

        # aumenta o valor x do grafico 3 | 5 posições a mais do valor maximo informado
        if self.object_ace.x > self.graph3_config.xmax:
            self.graph3_config.xmax = self.object_ace.x + 5

        self.reset_button.disabled = False
        self.running = True

        if not self.run_thread.is_alive():
            # realiza todo o calculo do códio
            self.run_thread.start()
            # atualiza os graficos
            self.graph_thread.start()
            # sorteia a variação de aceleração
            self.object_ace_variation_thread.start()

    def run(self):
        while True:
            while self.running:
                # fps
                rate(300)

                # calculo do tempo
                self.t = self.t + self.dt
                
                # calculo da velocidade
                self.object_vel.x   = self.object_vel.x + (self.object_ace.x * self.dt) + (self.object_ace_variation.x * self.dt)

                # calculo da posição da esfera
                self.object.pos.x   = self.object.pos.x + (self.object_vel.x * self.dt)
                
                # aumenta o tamanho do chão quando a esfere está proxima do fim
                if self.object.pos.x   > self.ground.pos.x + (self.ground.size.x // 3):
                    self.ground.pos.x  = self.ground.pos.x + (self.ground.size.x * 0.65)
                elif self.object.pos.x < self.ground.pos.x - (self.ground.size.x // 3):
                    self.ground.pos.x  = self.ground.pos.x - (self.ground.size.x * 0.65)

                # calculo da velocidade média
                self.object_avarage_speed.x = self.object.pos.x / self.t
                
                # atualiza todos os items da tela (não os gráficos)
                self.updateScreen()
   
    '''
        ┌─┐┬ ┬┌┐┌┌─┐┌─┐┌─┐┌─┐  ┌┬┐┌─┐  ┌─┐┬─┐┌─┐┌─┐┬┌─┐┌─┐┌─┐
        ├┤ │ │││││  │ │├┤ └─┐   ││├┤   │ ┬├┬┘├─┤├┤ ││  │ │└─┐
        └  └─┘┘└┘└─┘└─┘└─┘└─┘  ─┴┘└─┘  └─┘┴└─┴ ┴└  ┴└─┘└─┘└─┘
    '''

    def createGraph(self):
        # grafico 1 posição / tempo
        self.graph1_config = graph(width = self.WIDTH, _height = 400, title = 'Posição(m) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Posição(m)', foreground = color.black, background = color.white, fast = False)
        self.graph1 = gcurve(graph = self.graph1_config, color = color.blue, width = 5)
    
        # grafico 2 velocidade / tempo
        self.graph2_config = graph(width = self.WIDTH, _height = 400, title = 'Velocidade(m/s) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Velocidade(m/s)', foreground = color.black, background = color.white, fast = False, scroll = True, xmin = 0, xmax = 10)
        self.graph2 = gcurve(graph = self.graph2_config, color = color.red, width = 5)

        # grafico 3 aceleração / tempo
        self.graph3_config = graph(width = self.WIDTH, _height = 400, title = 'Aceleração(m/s²) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Aceleração(m/s²)', foreground = color.black, background = color.white, fast = False, scroll = True, xmin = 0, xmax = 5)
        self.graph3 = gcurve(graph = self.graph3_config, color = color.green, width = 5)
 
    def updateGraphs(self):
        self.graph1.plot(self.t, self.object.pos.x)
        self.graph2.plot(self.t, self.object_vel.x)
        self.graph3.plot(self.t, self.object_ace.x + self.object_ace_variation.x)
        
    def updateGraphsThread(self):
        while True:
            while self.running:
                self.graph1.plot(self.t, self.object.pos.x)
                self.graph2.plot(self.t, self.object_vel.x)
                self.graph3.plot(self.t, self.object_ace.x + self.object_ace_variation.x)   

    def resetGraphs(self):
        self.graph1.delete()
        self.graph2.delete()
        self.graph3.delete()

    '''
        ┬ ┬┬ ┌┬┐┬┬  ┬┌┬┐┌─┐┬─┐┬┌─┐┌─┐
        │ ││  │ ││  │ │ ├─┤├┬┘││ │└─┐
        └─┘┴─┘┴ ┴┴─┘┴ ┴ ┴ ┴┴└─┴└─┘└─┘
    '''

    def vSpace(self, times):
        # espaço na vertical
        scene.append_to_caption(f'\n' * times)

    def hSpace(self, times):
        # espaço na horizontal
        scene.append_to_caption(f' ' * times)

    def reset(self):
        # reseta todos os valores
        self.setInitialValues()
        self.resetGraphs()
        self.object_velocity_input.disabled = False
        self.reset_button.disabled = True
        self.object.pos = self.object_initial_pos
        self.updateScreen()
        self.run_thread = Thread(target = self.run)
        self.screen_thread = Thread(target = self.updateScreen)
        self.graph_thread = Thread(target = self.updateGraphs)
        self.object_ace_variation_thread = Thread(target = self.sortAceVariationValue)
        
    def updateScreen(self):
    
        # atualiza as posições das setas de aceleração
        self.ace_right_arrow.pos.x = (self.object.pos.x - (self.object.radius / 2))
        self.ace_left_arrow.pos.x  = (self.object.pos.x + (self.object.radius / 2))

        # atualiza as posições das setas de velocidade
        self.vel_right_arrow.pos.x = self.object.pos.x + (self.object.radius * 1.5)
        self.vel_left_arrow.pos.x = self.object.pos.x - (self.object.radius * 1.5)

        # atualiza a posição do texto referente velocidade e aceleração
        self.vel_text_right_pos = vector(self.vel_right_arrow.pos.x, self.vel_right_arrow.pos.y + .5, self.vel_right_arrow.pos.z)
        self.vel_text_left_pos  = vector(self.vel_left_arrow.pos.x, self.vel_left_arrow.pos.y + .5, self.vel_right_arrow.pos.z)
        self.ace_text_pos = vector(self.ace_right_arrow.pos.x + (self.ace_right_arrow.size.x / 2), self.ace_right_arrow.pos.y + .5, self.ace_right_arrow.pos.z)

        # atualiza o valor da velocidade e aceleração na tela
        self.ace_text.visible = True
        self.vel_text.visible = True
        self.vel_text.text = f"V: {self.object_vel.x:.2f} m/s"
        self.ace_text.text = f"A: {self.object_ace.x + self.object_ace_variation.x:.2f} m/s²"

        if (self.object_vel.x > 0):
            self.vel_text.pos = self.vel_text_right_pos
            self.vel_text.align = 'left'
        elif (self.object_vel.x < 0):
            self.vel_text.pos = self.vel_text_left_pos
            self.vel_text.align = 'right'
            
        self.ace_text.pos = self.ace_text_pos
        self.object_pos_x_info.text = f'{self.object.pos.x:.2f} m'
        self.time_info.text  = f'{self.t:.2f} s'
        self.object_avarage_speed_info.text = f'{self.object_avarage_speed.x:.2f} m/s'        
        
        # atualização gráfica das setas em relação a aceleração
        if self.object_ace.x  + self.object_ace_variation.x == 0:
            self.ace_right_arrow.visible = False
            self.ace_left_arrow.visible  = False
        elif self.object_ace.x + self.object_ace_variation.x > 0:
            self.ace_right_arrow.visible = True
            self.ace_left_arrow.visible  = False
        else:
            self.ace_right_arrow.visible = False
            self.ace_left_arrow.visible  = True

        # atualização gráfica das setas em relação a velocidade
        if self.object_vel.x == 0:
            self.vel_right_arrow.visible = False
            self.vel_left_arrow.visible  = False
        elif self.object_vel.x > 0:
            self.vel_right_arrow.visible = True
            self.vel_left_arrow.visible  = False
        else:
            self.vel_right_arrow.visible = False
            self.vel_left_arrow.visible  = True

    # atualiza o texto ao lado do slider
    def updateAceVariationSliderInfo(self):
        self.current_object_ace_variation_info.text = f"{str(self.object_ace_variation_slider.value)}m/s²"

    # sorteia a variação da aceleração
    def sortAceVariationValue(self):
        while True:
            while self.running:
                time.sleep(2)
                
                v = self.object_ace_variation_slider.value

                if v < 0:
                    sorted_v = random.uniform(v, 0)
                else:
                    sorted_v = random.uniform(0, v)
            
                if v!= 0:
                    if self.object_ace_variation.x > v:
                        while self.object_ace_variation.x > sorted_v:
                            self.object_ace_variation.x = self.object_ace_variation.x - self.dt
                            time.sleep(self.dt)
                    elif self.object_ace_variation.x < v:
                        while self.object_ace_variation.x < sorted_v:
                            self.object_ace_variation.x = self.object_ace_variation.x + self.dt
                            time.sleep(self.dt)
    
    def pause(self):
        if self.running:
            self.running = False
            self.pause_button.text = "Retomar"
        else:
            self.running = True
            self.pause_button.text = "Pausar"
                 
    def nothing(self):
        # literalmente nada
        pass

RectilinearMovement()