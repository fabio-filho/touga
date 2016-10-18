# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    mGames = db((db.tbGame.id>0)&(db.tbGame.mIsActive==True)).select(orderby=db.tbGame.mName)
    return dict(mGames=mGames)
