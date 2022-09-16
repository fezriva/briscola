from .briscola import *

from gym.envs.registration import register

register(
    id = 'Briscola-v2',
    entry_point = 'modules.briscola:BriscolaEnv'
)