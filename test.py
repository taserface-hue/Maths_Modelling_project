# coding=utf-8
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Script allowing to play the game by multiple players."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from absl import logging

from gfootball.env import config
from gfootball.env import football_env

FLAGS = flags.FLAGS

flags.DEFINE_string('players', 'keyboard:left_players=1',
                    'Semicolon separated list of players, single keyboard '
                    'player on the left by default')
flags.DEFINE_string('level', '11_vs_11_easy_stochastic', 'Level to play')
flags.DEFINE_enum('action_set', 'default', ['default', 'full'], 'Action set')
flags.DEFINE_bool('real_time', False,
                  'If true, environment will slow down so humans can play.')
flags.DEFINE_bool('render', False, 'Whether to do game rendering.')


def main(_):
    # players = FLAGS.players.split(';') if FLAGS.players else ''
    #    assert not (any(['agent' in player for player in players])
    #               ), 'Player type \'agent\' can not be used with play_game.'

    cfg_values = {'action_set': 'full', 'dump_full_episodes': True, 'players': '', 'real_time': False,
                  'level': '11_vs_11_easy_stochastic'}

    cfg = config.Config(cfg_values)
    env = football_env.FootballEnv(cfg)
    if FLAGS.render:
        env.render()
    steps = 0
    env.reset()
    try:
        while True:
            obs, rew, done, info, team1_score, team2_score = env.step([])
            steps += 1
            if steps % 100 == 0:
                print("Step %d Reward: %f" % (steps, rew))
            if done:
                print("The final score is %d : %d" % (team1_score, team2_score))
                return team1_score
    except KeyboardInterrupt:
        logging.warning('Game stopped, writing dump...')
        env.write_dump('shutdown')
        exit(1)

    return team1_score


if __name__ == '__main__':
    app.run(main)
