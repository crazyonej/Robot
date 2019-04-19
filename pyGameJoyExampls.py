
# Examples from : https://www.programcreek.com/python/example/1012/pygame.init

def telemetry(sid, data):
    # The current steering angle of the car
    steering_angle = data["steering_angle"]
    # The current throttle of the car
    throttle = data["throttle"]
    # The current speed of the car
    speed = data["speed"]
    # The current image from the center camera of the car
    imgString = data["image"]
    image = Image.open(BytesIO(base64.b64decode(imgString)))
    image_prep = np.asarray(image)
    image_array = preprocess(image_prep)

    ### Maybe use recording flag to start image data collection?
    recording = False
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            print("Joystick moved")
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")

    ### Get joystick and initialize
    ### Modify/Add here for keyboard interface
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # We are using PS3 left joystick: so axis (0,1) run in pairs, left/right for 2, up/down for 3
    # Change this if you want to switch to another axis on your joystick!
    # Normally they are centered on (0,0)
    leftright = joystick.get_axis(0)/2.0
    updown = joystick.get_axis(1)

    ### Again - may want to try using "recording" flag here to gather images and steering angles for training.
    if leftright < -0.01 or leftright > 0.01:
        if joystick.get_button(0) == 0:
            recording = True
    if recording:
        print("Recording: ")
        print("Right Stick Left|Right Axis value {:>6.3f}".format(leftright) )
        print("Right Stick Up|Down Axis value {:>6.3f}".format(updown) )

    transformed_image_array = image_array[None, :, :, :]
    # This model currently assumes that the features of the model are just the images. Feel free to change this.
    steering_angle = float(model.predict(transformed_image_array, batch_size=1)) + leftright
    # The driving model currently just outputs a constant throttle. Feel free to edit this.

    ### we can force the car to slow down using the up joystick movement.
    throttle = 0.5 + updown
    print(steering_angle, throttle)
    send_control(steering_angle, throttle) 



def update(self, screen, event_queue, dt,clock,joystick, netmodel, vizmodel):
        # Logos/titles
        screen.blit(self.logo,(screen.get_width() / 4 - 265,screen.get_height() * 3 / 4-500))
        screen.blit(self.intel,(screen.get_width() / 4 - 300,screen.get_height()-130))
        screen.blit(self.activestate,(screen.get_width() - 980,screen.get_height() - 130))

        nextState = self
        displaytext('Play', 32, screen.get_width() / 4 - 20, screen.get_height() * 3 / 4
                    - 80, WHITE, screen)
        displaytext('Train', 32, screen.get_width() / 4 - 20, screen.get_height() * 3 / 4
                    - 40, WHITE, screen)
        displaytext('Exit', 32, screen.get_width() / 4 - 20, screen.get_height() * 3 / 4,
                    WHITE, screen)
        displaytext(u'\u00bb', 32, screen.get_width() / 4 - 60, screen.get_height() * 3 / 4
                    - 40*self.menu_selection, WHITE, screen)

        # Each game state processes its own input queue in its own way to avoid messy input logic
        for event in event_queue:
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN)) or (event.type == pygame.JOYBUTTONDOWN and (event.button == 1)) or (event.type == pygame.JOYAXISMOTION and (event.axis == 1 or event.value >= DEADZONE)):
                    self.menu_selection -= 1
                    if self.menu_selection == -1:
                        self.menu_selection = 2
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_UP)) or (event.type == pygame.JOYBUTTONDOWN and (event.button == 0)) or (event.type == pygame.JOYAXISMOTION and (event.axis == 1 or event.value <= -DEADZONE)):
                    self.menu_selection += 1
                    if self.menu_selection == 3:
                        self.menu_selection = 0
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.JOYBUTTONDOWN and event.button == 11):
                    if self.menu_selection == 2:
                        nextState = Play(False)
                    elif self.menu_selection == 1:
                        nextState = Play(True)
                    else:
                        nextState = None
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                    self.ExportModel()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_d):
                    self.DumpData()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    self.DumpWeights()
        return nextState 
		
def events(self):
        self.updated = False
        action = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game(self)
            # keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game(self)
                if event.key == pg.K_DOWN:
                    action = 'down'
                if event.key == pg.K_UP:
                    action = 'up'
                if event.key == pg.K_RETURN:
                    action = 'enter'
            # mouse
            if event.type == pg.MOUSEMOTION:
                self.mousex, self.mousey = pg.mouse.get_pos()
                for i in range(len(self.menu_rects.items())):
                    if self.menu_rects[i].collidepoint(self.mousex, self.mousey):
                        self.menu['selected_option'] = i
                        self.updated = True
                        break
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(len(self.menu_rects.items())):
                    if self.menu_rects[i].collidepoint(self.mousex, self.mousey):
                        action = 'enter'
                        break
            # joystick
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == J_BUTTONS['A']:
                    action = 'enter'
            if event.type == pg.JOYAXISMOTION:
                if event.dict['axis'] == 1:
                    if time.time() >= self.last_axis_motion + 0.3:
                        if event.dict['value'] < -JOYSTICK_THRESHOLD:
                            action = 'up'
                            self.last_axis_motion = time.time()
                        elif event.dict['value'] > JOYSTICK_THRESHOLD:
                            action = 'down'
                            self.last_axis_motion = time.time()

        if action == 'down':
            self.menu["selected_option"] += 1
            self.menu["selected_option"] %= len(self.menu["options"])
            self.updated = True
        elif action == 'up':
            self.menu["selected_option"] -= 1
            self.menu["selected_option"] %= len(self.menu["options"])
            self.updated = True
        elif action == 'enter':
            self.menu["options"][self.menu["selected_option"]]["func"](self) 