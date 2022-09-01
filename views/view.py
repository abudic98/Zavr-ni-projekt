from asyncio import format_helpers
from arcade import View as ArcadeView

class View(ArcadeView):
    def __init__(self):
        super().__init__()
        
        #pratimo je li neki view pokrenuo svoj setup ili ne
        self.started = False
        
        #views UI manager, opcionalno za koristenje
        self.ui_manager = None
    
    def setup(self):
        self.started = True
        
    def on_show(self):
        if not self.started:
            self.setup()
            
        if self.ui_manager:
            self.ui_manager.enable()
            
    def on_hide_view(self):
        if self.ui_manager:
            self.ui_manager.disable()