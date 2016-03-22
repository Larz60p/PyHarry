#
#    PyHarry.py
#
#    This file is part of PyHarry.py.
#
#    Copyright (c) 2016 - Larry McCaig (A.K.A. Larz60+)
#
#    Licensed under GNU GENERAL PUBLIC LICENSE
#
import HarryGui

def main():
    gb = HarryGui.HarryGui()
    gb.create_widgets()
    gb.loadtree()
    gb.mainloop()

if __name__ == '__main__':
    main()
