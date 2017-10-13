
from ..base_output import OutputBackend


class CursesOutput(OutputBackend):
    def _init(self, curses):
        self.curses = curses
        self._max_pairs = None
        self._colors = False

    def _start(self):
        assert self._backend._root is not None
        self.size = self._update_size()
        self.logger.debug(self.size)
        self._start_colors()
        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            self.curses.curs_set(0)
        except:
            self.logger.warning("Hiding default cursor failed!")

    def _update_size(self):
        y, x = self._backend._root.getmaxyx()
        self.size = x, y
        return x, y

    def _start_colors(self):
        if self.curses.can_change_color():
            self.logger.debug("Term supports changing colors.")
            self._max_pairs = self.curses.COLOR_PAIRS
            self.logger.debug("Max color pairs:{}".format(self.curses.COLOR_PAIRS))
            self.curses.start_color()
            self.curses.use_default_colors()
            self._setup_colors()
        else:
            self.curses.use_default_colors()
            self.logger.debug("Term doesn't support changing colors.")

    def _setup_colors(self):
        pass
        #                       id,  fg,  bg
        # self.curses.init_pair(10,  -1, -1) # -1 = default
        # self.curses.init_pair(10,  200, -1)

    def _has_colors(self):
        return self.curses.has_colors()

    def _test_color_pairs_overflow(self):
        """Try to initialize more than the maximum amount of colors cures supports (256)"""
        # Test COLOR_PAIRS overflow
        # Only id's 1-256 work
        # TODO: What should happen if more colorpairs are specified by the app?
        #       Maybe we'll just ignore new colors if 256 would be exceded?
        #       Or normalize the colors to always be one of the default 256 colors
        #       That way we get the closest approximation and avoid overflowing
        #       However that would only work for foreground colors
        #       When all fg and bg combinations are combined we get 256*256

        i = 0
        while i < 300:
            self.logger.debug("Initing color #{}".format(i))
            try:
                self.curses.init_pair(i, 6, 100)
            except:
                self.logger.debug("Failed for #{}".format(i))
                break
            i += 1

    def _stop(self):
        pass

    def _convert_scr_attr(self, attr):
        attrs = self.curses.A_NORMAL
        if attr.is_bold():
            attrs = attrs | self.curses.A_BOLD
        if attr.is_underline():
            attrs = attrs | self.curses.A_UNDERLINE
        if attr.is_blink():
            attrs = attrs | self.curses.A_BLINK
        return attrs

    def _erase(self):
        self._backend._root.erase()
        # self._backend._root.clear()

    def _render(self, screen):
        # TODO: Warn if screen is bigger than terminal
        if not screen.lines:
            return False
        self._erase()  # TODO: clear or erase?
        self._backend._root.move(0, 0)
        x = 0
        y = 0
        for line in screen.lines:
            for part in line:
                attrs = self._convert_scr_attr(part.attributes)
                self.__addstr(y, x, str(part), attrs)
                x += len(part)
            y += 1
            x = 0
        self._backend._root.refresh()

    def __addstr(self, y, x, s, attrs):
        # Curses addstr needs to be wrapped since it stupidly
        # freaks out whenever writing to bottom right corner.
        # Verified on Python 3.5.2
        # Ref: https://stackoverflow.com/questions/7063128/last-character-of-a-window-in-python-curses

        try:
            self._backend._root.addstr(y, x, str(s), attrs)
        except self.curses.error:
            pass  # Just meh
            # self.logger.exception("__addstr failed!")
            # self.logger.error("string:{}".format(s))
            # self.logger.error("size:{}, x,y = {}, len:{}".format(self.size, (x, y), len(s)))
