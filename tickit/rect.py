
import ctypes

from collections.abc import Container

from tickit.ctickit import *

class Rect(Container):
    @property
    def top(self):
        return self._rect.top.value

    @top.setter
    def top(self, value):
        if not isinstance(value, int):
            raise TypeError('not an integer')
        self._rect.top = ctypes.c_int(value)

    @property
    def left(self):
        return self._rect.left.value

    @left.setter
    def left(self, value):
        if not isinstance(value, int):
            raise TypeError('not an integer')
        self._rect.left = ctypes.c_int(value)

    @property
    def lines(self):
        return self._rect.lines.value

    @lines.setter
    def lines(self, value):
        if not isinstance(value, int):
            raise TypeError('not an integer')
        self._rect.lines = ctypes.c_int(value)

    @property
    def cols(self):
        return self._rect.cols.value

    @cols.setter
    def cols(self, value):
        if not isinstance(value, int):
            raise TypeError('not an integer')
        self._rect.cols = ctypes.c_int(value)

    @property
    def right(self):
        return self.left + self.cols

    @property
    def bottom(self):
        return self.top + self.lines

    def __init__(self, obj=None, **kwargs):
        if obj is not None:
            if isinstance(obj, tickit.TickitRect):
                self._rect = obj
            elif isinstance(obj, basestring):
                self._rect = self.parse(obj)
            else:
                raise TypeError('object input invalid')
        else:
            self._rect = tickit.TickitRect()

            if 'lines' in kwargs:
                ctickit.tickit_rect_init_sized(
                    self._rect, kwargs['top'], kwargs['left'],
                    kwargs['lines'], kwargs['cols']
                )
            else:
                ctickit.tickit_rect_init_bounded(
                    self._rect, kwargs['top'], kwargs['left'],
                    kwargs['right'], kwargs['bottom']
                )

    def parse(self, string):
        string = string[1:-1]
        strings = string.split('..')

        left, top = strings[0][:-1].split(',')
        right, bottom = strings[1][1:].split(',')

        rect = tickit.TickitRect()

        ctickit.tickit_rect_init_bounded(rect, top, left, right, bottom)

        return rect

    def add(self, other):
        rect_arr = tickit.TickitRect * 3
        rects = rect_arr()
        count = ctickit.tickit_rect_add(rects, self._rect, other._rect)

        return (Rect(obj=rects[x]) for x in range(count))

    def subtract(self, a, b):
        rect_arr = tickit.TickitRect * 4
        rects = rect_arr()
        count = ctickit.tickit_rect_subtract(rects, self._rect, other._rect)

        return (Rect(obj=rects[x]) for x in range(count))

    def intersect(self, other):
        rect = tickit.TickitRect()

        intersects = ctickit.tickit_rect_intersect(rect, self._rect, other._rect)

        if intersects:
            return Rect(obj=rect)

        return None

    def intersects(self, other):
        if self.intersect(other) is not None:
            return True
        return False

    def contains(self, other):
        return ctickit.tickit_rect_contains(self._rect, other._rect)

    def __contains__(self, other):
        return self.contains(other)
