# -*- coding: utf-8 -*-

'''
    Game
'''

db.define_table("tbGame",
    Field("mName", "string", requires=IS_NOT_EMPTY(), label=T('Name')),
    Field("mIsActive", "boolean", default=True, label=T('Is active')),
    Field("mIsJoinAble", "boolean", default=True, label=T('Is join able')),
    auth.signature, format='%(mName)s'
)


'''
    Auth game
'''

db.define_table("tbAuthGame",
    Field("mAuth", "reference auth_user", label=T('User')),
    Field("mGame", "reference tbGame", label=T('Game')),
    Field("mPoints", "integer", default=0, label=T('Points')),
    Field("mVictories", "integer", default=0, label=T('Victories')),
    Field("mDraws", "integer", default=0, label=T('Draws')),
    Field("mMatches", "integer", default=0, label=T('Matches')),
    Field("mLosses", "integer", default=0, label=T('Losses')),
    Field("mProGoals", "integer", default=0, label=T('ProGoals')),
    Field("mGoalsAgainst", "integer", default=0, label=T('GoalsAgainst')),
    auth.signature # The auth signature will register the auth history for this table.
)
