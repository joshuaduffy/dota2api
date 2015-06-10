#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PlayerSummaries(list):
    def __init__(self, **kwargs):
        map(self.append, [PlayerSummary(**summary_kwargs) for summary_kwargs in kwargs['players']])


class PlayerSummary(object):
    def __init__(self, **kwargs):
        self.steam_id = kwargs.get('steamid')
        self.community_visibility_state = kwargs.get('communityvisibilitystate')
        self.profile_state = kwargs.get('profilestate')
        self.persona_name = kwargs.get('personaname')
        self.last_logoff = kwargs.get('lastlogoff')
        self.profile_url = kwargs.get('profileurl')
        self.url_avatar = kwargs.get('avatar')
        self.url_avatar_medium = kwargs.get('avatarmedium')
        self.url_avatar_full = kwargs.get('avatarfull')
        self.persona_state = kwargs.get('personastate')
        self.primary_clan_id = kwargs.get('primaryclanid')
        self.time_created = kwargs.get('timecreated')
        self.persona_state_flags = kwargs.get('personastateflags')

    def __repr__(self):
        return 'Player steam_id: {} name: {}'.format(self.steam_id, self.persona_name)
