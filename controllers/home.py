# -*- coding: utf-8 -*-


def index():
    mQuery = db.tbGame.mIsActive==True
    mGames = db(mQuery).select(orderby=db.tbGame.mName)
    return dict(mGames=mGames)
