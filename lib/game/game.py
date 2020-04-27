class Game:

    def __init__(self):
        self._isStart = False
        self._isOver = False
        self._isHasWinner = False
        self._lstPlayer = []


    @property
    def isStart(self):
        return self._isStart

    @property
    def isOver(self):
        return self._isOver

    @property
    def isHasWinner(self):
        return self._isHasWinner

    @property
    def lstPlayer(self):
        return self._lstPlayer

    # Defining the play state_value, player and the cell number
    def play(self, sv, each_player, cell):
        if sv[int((cell - 1) / 3)][(cell - 1) % 3] is ' ':
            sv[int((cell - 1) / 3)][(cell - 1) % 3] = each_player
        else:
            cell = int(input(" Choose again, Cell is not empty: "))
            self.play(sv, each_player, cell)

    def check_winner(self):
        raise NotImplementedError("Please implement this method.")

 
    def add_player(self, lstPlayer):
        
        for player in lstPlayer:
            self._lstPlayer.append(player)


    def has_winner(self):
        self._isHasWinner = True


    def start(self):
        self._isStart = True


    def over(self):
        self._isOver = True
