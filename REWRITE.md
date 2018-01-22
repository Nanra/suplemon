# Rewriting Suplemon

## Rationale
The Suplemon project began as a POC. It proved to be a feasible idea and
worked well. However as the project progressed it became harder to add new
features since the core was too limiting. Supporting Python 2 and 3 at the same
time added unnecessary complexity. To fix this I'm rewriting the app from
scratch to be more flexible to work with. This will make it easier to implement
better and more advanced features.

## Major Architectural Changes
- [X] Base all UI components on a shared base class with a good interface (widget)
- [X] Allow arbitrary ordering of UI layout/widgets
- [X] Separate the terminal handling from the core with abstraction


## Features that should be added (or at least made possible)
- [ ] Render tab character as n spaces
- [/] Support selecting text (regions)
- [ ] Per file settings (e.g. different tab width for different file types, support editorconfig)
- [X] Split screen view (multiple files visible at the same time)
- [ ] Sidebar with directory tree (or anything else that's useful in a sidebar)
- [ ] Add a dropdown for autocomplete matches
- [ ] Proper plugin architecture (there's a lot that plugins can't do at the moment). Ultimately sublime plugins should be supported.
- [ ] Proper event system


## Whishlist
- [ ] Wrapping long lines
- [ ] Code folding
- [ ] Multi line prompts
- [ ] A menu for different commands at the top the screen (with mouse support)


## Tech
- General
> Use assert in (API) methods to make sure args are correct
> Use new-style classes: `class Buffer(object):`
> Setters return true or false depending on wether value changed
> Try to be more Pythonic

## Architecture

This is just a guideline and it's still very abstract and incomplete.

     __________________________
    |                          |
    |  COMMAND LINE INTERFACE  |
    |       Invokes App        |
    |__________________________|
        |
        |
    [Initialization parameters: files, debug, etc. Defaults used otherwise.]
        |
      \ | /
     __\|/_________________________________________________________
    |                          |                                   
    | APP                      | > Current files
    |                          | > Views of files
    |__________________________| >
        |                /|\     >
        |               / | \    >
        |                 |                                        
        |                 |                                        
        |                 |__________________________              
     __\|/____                                       |             
    |         |                                      |             
    | LAYOUT  |<---------[ Focused Widget ]----------|             
    | Widgets |                                      |             
    |_________|                                      |             
         |                                           |             
         |        ___________________________________|____________ 
         |       |                                   |            |
         |       |           EVENT LOOP              |            |
         |       |                                   |            |
         |       |___________________________________+____________|
         |       ¦                                  /|\            
         |       ¦                                 / | \           
    [Defered Rendering]                              |             
                 ¦                                   |             
     ____________¦______________                     |             
    |                           |                    |             
    |         RENDERER          |                    |             
    | (Render Layout to Screen) |                    |             
    |   See: ui.py, widgets.py  |                    |             
    |                           |                    |             
    |___________________________|       [      Buffered Input     ]
                 |                      [    If backend support   ]
     ____________|______________        [ Default backend: curses ]
    |                           |                    |             
    |         SCREEN            |                    |             
    |   (Character Cell Grid)   |                    |             
    |      See: screen.py       |                    |             
    |                           |                    |             
    |___________________________|                    |             
                 |                                   |             
     ____________|___________________________________|____________ 
    |            |                                   |            |
    |            |     INPUT / OUTPUT (BACKEND)      |            |
    |            |                                   |            |
    |            |                   [Abstracted to InputEvent's] |
    |          \ | /                                 |            |
    |     ______\|/___________          _____________|_______     |
    |    |                    |        |                     |    |
    |    |   Generic Output   |        |    Generic Input    |    |
    |    |                    |        |                     |    |
    |    |____________________|        |_____________________|    |
    |             |                                  |            |
    |    [ Character Cell Grid ]                     |            |
    |             |                                  |            |
    |           \ | /                               /|\           |
    |            \|/                               / | \          |
    |             |_______________ __________________|            |
    |     ________|____      _____|________      ____|_______     |
    |    |             |    |              |    |            |    |
    |    |   Curses    |    |    Urwid?    |    |    PTPY?   |    |
    |    |  (Default)  |    |              |    |            |    |
    |    |_____________|    |______________|    |____________|    |
    |    _________|___________________________________________    |
    |                            /|\                              |
    |                             |                               |
    |     _______________________\|/_________________________     |
    |    |                                                   |    |
    |    |                     TERMINAL                      |    |
    |    |___________________________________________________|    |
    |                                                             |
    |_____________________________________________________________|



## Useful Unicode Symbols

    ⏎    23CE carriage return symbol
    ⌫    232B erase to the left (backspace)
    ␣    2423 space symbol

    ✓    2713 check mark
    ✗    2717 cross mark
    ×    00D7 multiplication sign
    ☠    2620 skull and crossbones

    ♻    267B black universal recycling symbol

    ⚙    2699 gear
    ⚠    26A0 warning sign
    ⚬    26AC medium small white circle
    ⛶    26F6 square four corners


