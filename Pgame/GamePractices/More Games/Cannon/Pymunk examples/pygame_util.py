# ----------------------------------------------------------------------------
# pymunk
# Copyright (c) 2007-2012 Victor Blomqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------

"""This submodule contains helper functions to help with quick prototyping 
using pymunk together with pygame.

Intended to help with debugging and prototyping, not for actual production use
in a full application. The methods contained in this module is opinionated 
about your coordinate system and not in any way optimized. 
"""

__version__ = "$Id$"
__docformat__ = "reStructuredText"

__all__ = ["draw", "get_mouse_pos", "to_pygame", "from_pygame"]

import pygame

import pymunk
from pymunk.vec2d import Vec2d

flip_y = True
"""Flip the y cooridnate to make y point upwards"""

def draw(screen, *objs):
    """Draw one or many pymunk objects on a pygame.Surface object.
        
    This method currently supports drawing of
        * pymunk.Space
        * pymunk.Segment
        * pymunk.Circle
        * pymunk.Poly
        * pymunk.Constraint objects 

    If a Space is passed in all shapes in that space will be drawn. 
    Unrecognized objects will be ignored (for example if you pass in a 
    constraint).
    
    Typical usage::
    
    >>> pymunk.pygame_util.draw(screen, my_space)
        
    You can control the color of a shape by setting shape.color to the color 
    you want it drawn in.
    
    >>> my_shape.color = pygame.color.THECOLORS["pink"]
    
    If you do not want a shape to be drawn, set shape.ignore_draw to True.
    
    >>> my_shape.ignore_draw = True
        
    Not all constraints are currently drawn in a very clear way, but all the 
    different shapes should look fine both as static and dynamic objects.
    
    See pygame_util.demo.py for a full example
    
    :Parameters:
            screen : pygame.Surface
                Surface that the objects will be drawn on
            objs : One or many objects to draw
                Can be either a single object or a list like container with 
                objects.
    """
    
    for o in objs:
        if isinstance(o, pymunk.Space):
            _draw_space(screen, o)
        elif isinstance(o, pymunk.Shape):
            _draw_shape(screen, o)
        elif isinstance(o, pymunk.Constraint):
            _draw_constraint(screen, o)
        elif hasattr(o, '__iter__'):
            for oo in o:
                draw(screen, oo)
                
def _draw_space(screen, space):
    
    (width, height) = screen.get_size()
    
    for s in space.shapes:
        if not (hasattr(s, "ignore_draw") and s.ignore_draw):
            _draw_shape(screen, s)
            
    for c in space.constraints:
        if not (hasattr(c, "ignore_draw") and c.ignore_draw):
            _draw_constraint(screen, c)

def _draw_shape(screen, shape):
    
    if isinstance(shape, pymunk.Circle):
        _draw_circle(screen, shape)
    elif isinstance(shape, pymunk.Segment):
        _draw_segment(screen, shape)
    elif  isinstance(shape, pymunk.Poly):
        _draw_poly(screen, shape)
        
def _draw_circle(screen, circle):
    
    circle_center = circle.body.position + circle.offset.rotated(circle.body.angle)
    p = to_pygame(circle_center, screen)
   
    r = 0
    color = pygame.color.THECOLORS["red"]
    if circle.body.is_static:
        color = pygame.color.THECOLORS["lightgrey"]
        r = 1
    if hasattr(circle, "color"):
        color = circle.color  
        
    pygame.draw.circle(screen, color, p, int(circle.radius), r)
    
    circle_edge = circle_center + Vec2d(circle.radius, 0).rotated(circle.body.angle)
    p2 = to_pygame(circle_edge, screen)
    line_r = 3 if circle.radius > 20 else 1
    pygame.draw.lines(screen, pygame.color.THECOLORS["blue"], False, [p,p2], line_r)

def _draw_poly(screen, poly):
    
    ps = poly.get_vertices()
    ps = [to_pygame(p, screen) for p in ps]
    ps += [ps[0]]
    if hasattr(poly, "color"):
        color = poly.color  
    elif poly.body.is_static:
        color = pygame.color.THECOLORS["lightgrey"]
    else:
        color = pygame.color.THECOLORS["green"]
    print(poly.radius)
    pygame.draw.lines(screen, color, False, ps, max(int(poly.radius*2),1))

def _draw_segment(screen, segment):
    
    body = segment.body
    pv1 = body.position + segment.a.rotated(body.angle)
    pv2 = body.position + segment.b.rotated(body.angle)

    p1 = to_pygame(pv1, screen)
    p2 = to_pygame(pv2, screen)
    
    if hasattr(segment, "color"):
        color = segment.color  
    elif segment.body.is_static:
        color = pygame.color.THECOLORS["lightgrey"]
    else:
        color = pygame.color.THECOLORS["blue"]
    pygame.draw.lines(screen, color, False, [p1,p2], max(int(segment.radius*2),1))
    
def _draw_constraint(screen, constraint):
    
    if isinstance(constraint, pymunk.GrooveJoint) and hasattr(constraint, "groove_a"):
        pv1 = constraint.a.position + constraint.groove_a
        pv2 = constraint.a.position + constraint.groove_b
        p1 = to_pygame(pv1, screen)
        p2 = to_pygame(pv2, screen)
        pygame.draw.aalines(screen, pygame.color.THECOLORS["darkgray"], False, [p1,p2])
    elif isinstance(constraint, pymunk.PinJoint):
        pv1 = constraint.a.position + constraint.anchr1.rotated(constraint.a.angle)
        pv2 = constraint.b.position + constraint.anchr2.rotated(constraint.b.angle)
        p1 = to_pygame(pv1, screen)
        p2 = to_pygame(pv2, screen)
        pygame.draw.aalines(screen, pygame.color.THECOLORS["darkgray"], False, [p1,p2])    
    elif isinstance(constraint, pymunk.GearJoint):
        pv1 = constraint.a.position
        pv2 = constraint.a.position
        p1 = to_pygame(pv1, screen)
        p2 = to_pygame(pv2, screen)
        pygame.draw.circle(screen, pygame.color.THECOLORS["darkgray"], p1, 3)
        pygame.draw.circle(screen, pygame.color.THECOLORS["darkgray"], p2, 3)
    elif hasattr(constraint, "anchr1"):
        pv1 = constraint.a.position + constraint.anchr1.rotated(constraint.a.angle)
        pv2 = constraint.b.position + constraint.anchr2.rotated(constraint.b.angle)
        p1 = to_pygame(pv1, screen)
        p2 = to_pygame(pv2, screen)
        pygame.draw.aalines(screen, pygame.color.THECOLORS["darkgray"], False, [p1,p2])
    else:
        pv1 = constraint.a.position
        pv2 = constraint.b.position
        p1 = to_pygame(pv1, screen)
        p2 = to_pygame(pv2, screen)
        pygame.draw.aalines(screen, pygame.color.THECOLORS["darkgray"], False, [p1,p2])    

def get_mouse_pos(screen):
    """Get position of the mouse pointer in pymunk coordinates."""
    p = pygame.mouse.get_pos()
    return from_pygame(p, screen)

def to_pygame(p, screen):
    """Convenience method to convert pymunk coordinates to pygame screen 
    local coordinates
    """
    if flip_y:
        return int(p[0]), screen.get_height()-int(p[1])
    else:
        return int(p[0]), int(p[1])
    
def from_pygame(p, screen):
    """Convenience method to convert pygame screen local coordinates to 
    pymunk coordinates    
    """
    return to_pygame(p,screen)

            
