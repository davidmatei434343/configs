

################################################## IMPORTS ####################################################################################################################



from typing import List  # noqa: F401
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile import bar, layout, widget
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from powerline.bindings.qtile.widget import PowerlineTextBox
from libqtile.config import Screen
from libqtile.widget.base import _TextBox

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration






mod = "mod1"
terminal = "terminator"
myBrowser = "firefox"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),

    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),

    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),

    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),

    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),

    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),

    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),

    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),

    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),

    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),

    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], "n",
            lazy.layout.normalize(),
            desc="Reset all window sizes"),

    Key([mod], "w",
             lazy.spawn(myBrowser),
             desc='Firefox'
             ),
             
     Key([mod], "e",
             lazy.spawn("emacs"),
             desc='Launch Emacs'
             ),

     Key([mod], "d",
             lazy.spawn("pcmanfm"),
             desc='Launch File Manager'
             ),

    Key([mod], "b",
             lazy.spawn("brave"),
             desc='brave'
             ),

    Key([mod], "x",
             lazy.spawn("arcolinux-logout"),
             desc='logout'
             ),

    Key([mod, "shift"], "v",
             lazy.spawn("virtualbox"),
             desc='Virtualbox'
             ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod, "shift"], "d", lazy.spawn("dmenu_run -i -nb '#2b303b' -nf '#FFFFFF' -sb '#a3be8c' -sf '#191919' -fn NotoMonoRegular:pixelsize=17.5 -p 'Run: '"),
    #Key([mod, "shift"], "d", lazy.spawn("rofi -show run 'Run: '"),
    Key([mod, "shift"], "d", lazy.spawn("launcher_text 'Run: '"),
     ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
        desc="Spawn a command using a prompt widget"),
]

group_names = [("DEV", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'}),
               ("DOC", {'layout': 'monadtall'}),
               ("VBX", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'treetab'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group
    
    layout_theme = {"border_width": 2,
                "margin": 15,
                "border_focus": "#C9CBFF",
                "border_normal": "#575268"
                }


layouts = [
    layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Stack(stacks=3, **layout_theme),
    layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["Apps"],
         section_fontsize = 10,
         border_width =0,
         bg_color = "#282a36",
         active_bg = "#50fa7b",
         active_fg = "#000000",
         inactive_bg = "#a9a1e1",
         inactive_fg = "#1c1f24",
         padding_left = 0,
         margin = 15,
         padding_x = 5,
         padding_y = 5,
         section_top = 20,
         section_bottom = 20,
         level_shift = 20,
         vspace = 10,
         panel_width = 40
         ),
    layout.Floating(**layout_theme)
]

colors = [["#161320", "#161320"], # 0 panel background
          ["#3d3f4b", "#434758"], # 1 background for current screen tab
          ["#D9E0EE", "#D9E0EE"], # 2 font color for group names
          ["#6272a4", "#6272a4"], # 3 border line color for current tab
          ["#6272a4", "#6272a4"], # 4 border line color for 'other tabs' and color for 'odd widgets'
          ["#DDB6F2", "#DDB6F2"], # 5 color for the 'even widgets'
          ["#62B9E000", "#62B9E000"], # 6 window name
          ["#F8BD96", "#F8BD96"], # 7 backbround for inactive screen
          ["#F28FAD", "#F28FAD"], # culoare widget 8
          ["#F2CDCD", "#F2CDCD"], # culoare widget 9
          ["#ABE9B3", "#ABE9B3"], # culoare widget 10
          ["#89DCEB", "#89DCEB"], # culoare widget 11
          ["#FAE3B0", "#FAE3B0"]] # culoare widget 12


          
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())


##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 10,
    padding = 2,
   # opacity = 0.5,
    foreground=colors[2]
)

decor = {
    "decorations": [
        RectDecoration(use_widget_background=True, radius=13, filled=True, padding_y=0,)
    ],
    "padding": 15,
}
decor2 = {
    "decorations": [
        RectDecoration(use_widget_background=True, radius=11, filled=True, padding_y=0)
    ],
    "padding": 10,
}
decor3 = {
    "decorations": [
        RectDecoration(use_widget_background=True, radius=12, filled=True, padding_y=0)
    ],
    "padding": 2,
}
decor4 = {
    "decorations": [
        RectDecoration(use_widget_background=True, radius=13, filled=True, padding_y=0)
    ],
    "padding": 4,
}





#extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [

widget.Sep(
                       linewidth = 2,
                       padding = 6,
                       foreground = colors[6],
                       background = colors[6]
                       ),



              widget.GroupBox(
                       font = "Ubuntu Semibold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 3,
                       padding_y = 0,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[9],
                       rounded = False,
                       highlight_color = colors[6],
                       highlight_method = "line",
                       this_current_screen_border = colors[9],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0],
                       **decor,
                       ),



              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),



              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[0],
                       scale = 0.65,
                       **decor3,
                       ),




              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 46
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("firefox")},
                       #fontsize = 17
                       #),

              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 16
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("whatsapp-nativefier")},
                       #fontsize = 19
                       #),

              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 16
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("brave -e https://meet.google.com/lookup/deeh53snj7?authuser=0&hs=179")},
                       #fontsize = 16
                       #),


              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 46
                       #),

                       
widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[6]
                       ),
                            



            widget.Sep(
                       linewidth = 7,
                       padding = 6,
                       foreground = colors[6],
                       background = colors[6]
                       ),



                       
widget.WindowName(
                       foreground = colors[2],
                       background = colors[0],
                       padding_x = 6,
                       padding_y = 0,
                       **decor,
                       ),



            widget.Sep(
                       linewidth = 440,
                       padding = 6,
                       foreground = colors[6],
                       background = colors[6]
                       ),

              #widget.TextBox(
               #        text = '',
                #       background = colors[0],
                 #      foreground = colors[5],
                  #     padding = -4.5,
                   #    fontsize = 46
                    #   ),





              widget.Memory(
                       foreground = colors[5],
                       background = colors[0],
                       format = 'Mem: {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bpytop')},
                       **decor,
                       ),


                       
              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),



             widget.Net(
                       interface = "enp2s0",
                       format = '{down} ↓↑ {up}',
                       foreground = colors[10],
                       background = colors[0],
                       **decor,
                       ),
                       


                widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Upd: {updates}",
                       foreground = colors[12],
                       colour_have_updates = colors[12],
                       colour_no_updates = colors[12],
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('terminator -x sudo pacman -Syu')},
                       background = colors[0],
                       **decor,
                       ),


              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),




               widget.ThermalSensor(
                        foreground = colors[9],
                        background = colors[0],
                        threshold = 90,
                        fmt = "🌡  {}",
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bpytop')},
                        **decor,
                        ),


               # widget.CapsNumLockIndicator(),






            #    widget.KeyboardLayout(
            #           foreground = colors[0],
            #           background = colors[9],
            #           fmt = 'Keyboard: {}',
            #           padding = 5
            #           ),

            #    widget.TextBox(
            #           text = '',
            #           background = colors[9],
            #           foreground = colors[8],
            #           padding = -4.5,
            #           fontsize = 46
            #           ),






              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),



              widget.Volume(
                       foreground = colors[8],
                       background = colors[0],
                       fmt = "Vol: {}",
                       **decor,
                       ),



             # widget.TextBox(
                      # text = '',
                      # background = colors[11],
                      # foreground = colors[5],
                      # padding = -4.5,
                      # fontsize = 46
                      # ),


               # widget.CheckUpdates(
                      # update_interval = 1800,
                      # distro = "Arch_checkupdates",
                      # display_format = "Updates: {updates} ",
                      # foreground = colors[1],
                      # colour_have_updates = colors[1],
                      # colour_no_updates = colors[0],
                      # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                      # padding = 5,
                      # background = colors[5]
                      # ),

               
               # widget.CapsNumLockIndicator(),




              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),


              widget.Clock(
                       foreground = colors[11],
                       background = colors[0],
                       mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn("emacs -e calendar")},
                       format = "%A, %B %d",
                       **decor,
                       ),


widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

              widget.Clock(
                       foreground = colors[7],
                       background = colors[0],
                       mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn("emacs -e calendar")},
                       format = "%H:%M ",
                       **decor,
                       ),


              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),

                       widget.Systray(
                       background = colors[0],
                       foreground = colors[2],
                       padding = 0
                       ),

            widget.Notify(padding = 0,
                       foreground = colors[2],
                       background = colors[0]
                       ),

        #    widget.Sep(
        #               linewidth = 0,
        #               padding = 6,
        #               foreground = colors[6],
        #               background = colors[0]
        #               ),

                       widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[2],
                       padding = 5,
                       fontsize = 15,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("/home/david/.config/rofi/applets/android/powermenu.sh")},
                       ),


widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),
                
               # widget.QuickExit(padding_y=5, padding_x=5),
                
               # widget.Sep(linewidth = 0, padding = 6),
        
                        widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[6],
                       background = colors[6]
                       ),

            ],
            26,
            background="#2b303b00",
            padding = 5,
            #opacity = 0.4,
            margin = 6
        ),
    ),
    Screen(
        top=bar.Bar(
            [


widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),


              widget.Image(
                       filename = "~/.config/qtile/icons/python-white.png",
                       scale = "False",
                       padding_y = 6,
                      # margin = 1,
                      # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
                      # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("dmenu_run -i -nb '#2b303b' -nf '#FFFFFF' -sb '#a3be8c' -sf '#191919' -fn NotoMonoRegular:pixelsize=17.5 -p 'Run: '")}
                      # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show run 'Run: '")}
                      mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("launcher_text 'Run: '")}
                       
                       ),

            	 widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),

              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[10],
                       rounded = False,
                       highlight_color = colors[0],
                       highlight_method = "line",
                       this_current_screen_border = colors[10],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -4.5,
                       fontsize = 46
                       ),

            widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = -0.0,
                       fontsize = 25
                       ),

              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[0],
                       padding = -4,
                       scale = 0.7
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),

              #widget.CurrentLayout(
                      # foreground = colors[2],
                      # background = colors[4],
                      # padding = 5
                      # ),

              widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -4.5,
                       fontsize = 46
                       ),


              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 46
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("firefox")},
                       #fontsize = 17
                       #),

              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 16
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("whatsapp-nativefier")},
                       #fontsize = 19
                       #),

              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 16
                       #),

#widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[2],
                       #padding = 0,
                       #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("brave -e https://meet.google.com/lookup/deeh53snj7?authuser=0&hs=179")},
                       #fontsize = 16
                       #),


              #widget.TextBox(
                       #text = '',
                       #background = colors[0],
                       #foreground = colors[0],
                       #padding = 0,
                       #fontsize = 46
                       #),

                       
widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[6]
                       ),
                            
widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[6]
                       ),
                       
            widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),


                       
widget.WindowName(
                       foreground = colors[2],
                       background = colors[0],
                       padding_x = 6,
                       padding_y = 0
                       ),


            widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[0],
                       padding = 0.0,
                       fontsize = 25
                       ),


            widget.Sep(
                       linewidth = 450,
                       padding = 6,
                       foreground = colors[6],
                       background = colors[6]
                       ),

              #widget.TextBox(
               #        text = '',
                #       background = colors[0],
                 #      foreground = colors[5],
                  #     padding = -4.5,
                   #    fontsize = 46
                    #   ),

            widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[5],
                       padding = -0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                       text = " 🖬",
                       foreground = colors[0],
                       background = colors[5],
                       padding = 0,
                       fontsize = 14
                       ),

            widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors[0],
                       colour_have_updates = colors[0],
                       colour_no_updates = colors[0],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[5]
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[5],
                       padding = 0.0,
                       fontsize = 25
                       ),
                       
              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[10],
                       padding = 0.0,
                       fontsize = 25
                       ),

             widget.Net(
                       interface = "enp2s0",
                       format = '{down} ↓↑ {up}',
                       foreground = colors[0],
                       background = colors[10],
                       padding = 0
                       ),
                       
widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[10],
                       padding = 0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

                widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[12],
                       padding = 0.0,
                       fontsize = 25
                       ),

                widget.TextBox(
                       text = " ",
                       padding = 2,
                       foreground = colors[0],
                       background = colors[12],
                       fontsize = 11
                       ),


                widget.CPU(
                        foreground = colors[0],
                        background = colors[12],
                        threshold = 90,
                        format = 'CPU {freq_current}  |  GHz {load_percent}%',
                        update_interval = 0.3,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bpytop')},
                        padding = 5
                        ),

                widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[12],
                       padding = 0.0,
                       fontsize = 25
                       ),
               
               # widget.CapsNumLockIndicator(),



                widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),


            #    widget.KeyboardLayout(
            #           foreground = colors[0],
            #           background = colors[9],
            #           fmt = 'Keyboard: {}',
            #           padding = 5
            #           ),

            #    widget.TextBox(
            #           text = '',
            #           background = colors[9],
            #           foreground = colors[8],
            #           padding = -4.5,
            #           fontsize = 46
            #           ),


widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[8],
                       padding = 0.0,
                       fontsize = 25
                       ),


widget.WindowCount(
                       background = colors[8],
                       foreground = colors[0],
                       padding = 2,
                       fontsize = 14
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[8],
                       padding = 0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[11],
                       padding = 0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                        text = " Vol:",
                        foreground = colors[0],
                        background = colors[11],
                        padding = 5
                        ),

              widget.Volume(
                       foreground = colors[0],
                       background = colors[11],
                       padding = 0
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[11],
                       padding = 0.0,
                       fontsize = 25
                       ),

             # widget.TextBox(
                      # text = '',
                      # background = colors[11],
                      # foreground = colors[5],
                      # padding = -4.5,
                      # fontsize = 46
                      # ),


               # widget.CheckUpdates(
                      # update_interval = 1800,
                      # distro = "Arch_checkupdates",
                      # display_format = "Updates: {updates} ",
                      # foreground = colors[1],
                      # colour_have_updates = colors[1],
                      # colour_no_updates = colors[0],
                      # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                      # padding = 5,
                      # background = colors[5]
                      # ),

               
               # widget.CapsNumLockIndicator(),



                widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -2.5,
                       fontsize = 46
                       ),


widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[7],
                       padding = 0.0,
                       fontsize = 25
                       ),


              widget.Clock(
                       foreground = colors[0],
                       background = colors[7],
                       mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn("emacs -e calendar")},
                       format = "%A, %B %d - %H:%M "
                       ),

widget.TextBox(
                       text = '',
                       background = colors[6],
                       foreground = colors[7],
                       padding = 0.0,
                       fontsize = 25
                       ),

              widget.TextBox(
                       text = ' ',
                       background = colors[6],
                       foreground = colors[6],
                       padding = -4.5,
                       fontsize = 46
                       ),


                
               # widget.QuickExit(padding_y=5, padding_x=5),
                
               # widget.Sep(linewidth = 0, padding = 6),
        


            ],
            26,
            background="#2b303b00",
            padding = 5,
            #opacity = 0.4,
            margin = 6
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
