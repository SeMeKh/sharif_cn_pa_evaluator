from .basics import basic_print, join
from .completeness import mixed_scenario
from .conformance import type1x, type2x_30
from .leave import explicit_exit, change_parent
from .messaging import simple_sendmsg
from .broadcast import propagate
from .tricky import self_message, setparent_cycle, sudden_leave, msg_to_nowhere
from .violation import m20_from_parent, m21_from_child, m30_from_child, invalid_message

all = [
          basic_print,
          join,
      ] + [
          explicit_exit,
          change_parent,
      ] + [
          simple_sendmsg,
          propagate,
      ] + [
          self_message,
          setparent_cycle,
          sudden_leave,
          msg_to_nowhere,
      ] + [
          type1x,
          type2x_30,
      ] + [
          m20_from_parent,
          m21_from_child,
          m30_from_child,
          invalid_message,
      ] + [
          mixed_scenario,
      ]
