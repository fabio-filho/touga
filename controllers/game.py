# -*- coding: utf-8 -*-



def index():
    try:
        mGame = db.tbGame(request.args[0])
        mAuthGame = db(db.tbAuthGame.mGame==mGame.id).select(orderby=db.tbAuthGame.created_by)

        mCanShowsJoinButton = canAuthJoin(mGame.id)

        return dict(mGame=mGame, mAuthGame=mAuthGame, mCanShowsJoinButton=mCanShowsJoinButton)
    except Exception as mError:
        print mError
        redirect(URL('default','index'))


@auth.requires(lambda: MyAuth.isMaster())
def management():
    mGrid = SQLFORM.grid(db.tbGame, csv=False)
    return dict(mGrid=mGrid)




#===============================================================================


def canAuthJoin(mGameId):
    mGame = db.tbGame(mGameId)
    mCanShowsJoinButton = False
    if MyAuth.isLogged():
        if mGame.mIsJoinAble:
            if len(db((db.tbAuthGame.mGame==db.tbAuthGame.created_by)&(db.tbAuthGame.mGame==mGameId)).select())==0:
                mCanShowsJoinButton = True

    return mCanShowsJoinButton



@auth.requires_login()
def join():
    try:
        if not canAuthJoin(request.args[0]): redirect(URL('default','index'))

        db.tbAuthGame.insert(mAuth=auth.user_id, mGame=request.args[0])

        session.flash = T('Joined')
        redirect(URL('game','index', args=request.args[0]))

    except Exception as mError:
        print mError
        session.flash = T('Some erros were found, try again!')
        redirect(URL('default','index'))
