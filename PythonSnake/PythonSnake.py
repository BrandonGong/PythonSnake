from random import randrange

# Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock


class Food(Widget):
    def __init__(self):
        super().__init__()
        self.size = (30,30)
        with self.canvas:
            Color(1,0,0)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        
        self.bind(pos=self.update,size=self.update)

    def update(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def reset_location(self):
        self.pos = (randrange(self.size[0] / 2, Window.size[0] - self.size[0]/2 ),randrange(self.size[1] / 2, Window.size[1] - self.size[1] / 2))
            
class SnakeBody(Widget):
    def __init__(self,pos):
        super().__init__()
        self.size = (30,30)
        self.pos = pos
        with self.canvas:
            Color(0,1,0)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        
        self.bind(pos=self.update,size=self.update)

    def update(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size



class GameBoard(Widget):
    def __init__(self):
        super().__init__()
        self.size = Window.size

        # Properties
        self.snake = [SnakeBody((self.size[0]/2,self.size[1]/2))]

        self.food = Food()
        self.food.reset_location()

        self.vel_x = 0
        self.vel_y = 1

        self.game_over = False


        # Events
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')

        # If it exists, this widget is a VKeyboard object which you can use to change the keyboard layout.
        if self._keyboard.widget:
            pass

        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        #Drawing
        self.draw()

    # Keyboard Events
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers) -> bool:

        key = keycode[1]
        if key == 'escape':
            App.get_running_app().stop()
            Window.close()

        vel_x = self.vel_x
        vel_y = self.vel_y
        if key == 'up' or key == 'w':
            vel_y = 1
            vel_x = 0
        if key == 'down' or key == 's':
            vel_y = -1
            vel_x = 0
        if key == 'left' or key == 'a':
            vel_x = -1
            vel_y = 0
        if key == 'right' or key == 'd':
            vel_x = 1
            vel_y = 0

        if self.vel_x + vel_x != 0:
            self.vel_x = vel_x

        if self.vel_y + vel_y != 0:
            self.vel_y = vel_y
             
        return True

    def update(self,dt):
        if self.game_over:
            return

        new_head = self.snake[0]
        if len(self.snake) > 1:
            new_head = self.snake.pop()
            new_head.pos = self.snake[0].pos


        x = new_head.pos[0] + self.vel_x * new_head.size[0]
        if x > Window.width:
            x = 0
        elif x < 0:
            x = Window.width

        y = new_head.pos[1] + self.vel_y * new_head.size[1]
        if y > Window.height:
            y = 0
        elif y < 0:
            y = Window.height

        new_head.pos = (x,y)

        if len(self.snake) > 1:
            # Check head has collided with body
            for w in self.snake[1:]:
                if new_head.collide_point(w.center_x,w.center_y):
                    self.game_over = True
        if new_head != self.snake[0]:
            # Add head back to body
            self.snake.insert(0,new_head)
        # Head has left the edge of the Window

        if new_head.collide_widget(self.food):
            self.snake.insert(0,SnakeBody((new_head.pos[0] + self.vel_x * new_head.size[0], new_head.pos[1] + self.vel_y * new_head.size[1])))
            self.food.reset_location()

        self.draw()

    def draw(self):
        self.clear_widgets()

        self.add_widget(self.food)
        for w in self.snake:
            self.add_widget(w)
        
        self.add_widget(Label(text="Score: " + str(len(self.snake))))
        if self.game_over:
            self.add_widget(Label(text="Game Over",
                                  font_size=70,
                                  center_y = self.height / 2,
                                  center_x = self.width / 2
                                  ))
            
'''
    Snake Application
'''
class snakeApp(App):

    def build(self):
        game = GameBoard()
        # Set Game clock
        Clock.schedule_interval(game.update,.1)
        return game
    

if __name__ == "__main__":
    snakeApp().run()
