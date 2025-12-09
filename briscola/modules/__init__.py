from .briscola import *

from gymnasium.envs.registration import register

register(
    id = 'Briscola-v2',
    entry_point = 'modules.briscola:BriscolaEnv'
)