# -*- coding: utf-8 -*-



def index():
    try:
        if request.args[0]!=session.current_game:
            session.current_game = request.args[0]

        mGame = db.tbGame(session.current_game)
        mAuthGame = db(db.tbAuthGame.mGame==mGame.id).select(orderby=db.tbAuthGame.mAuth)

        mCanShowsJoinButton = canAuthJoin(mGame.id)
                
        return dict(mGame=mGame, mAuthGame=mAuthGame, mCanShowsJoinButton=mCanShowsJoinButton)
    except Exception as mError:
        print mError
        redirect(URL('home','index'))


@auth.requires(lambda: MyAuth.isMaster())
def management():
    mGrid = SQLFORM.grid(db.tbGame, csv=False)
    return dict(mGrid=mGrid)




#===============================================================================


def canAuthJoin(mGameId):
    mGame = db.tbGame(mGameId)
    print mGame
    if MyAuth.isLogged():
        print db((db.tbAuthGame.mAuth==auth.user_id)&(db.tbAuthGame.mGame==mGameId)).count()
        if db((db.tbAuthGame.mAuth==auth.user_id)&(db.tbAuthGame.mGame==mGameId)).count()>0:
            return False

    return mGame.mIsJoinAble



@auth.requires_login()
def join():
    try:
        if not canAuthJoin(request.args[0]): redirect(URL('default','index'))
        db.tbAuthGame.insert(mAuth=auth.user_id, mGame=request.args[0])
        session.flash = T('Joined')
        redirect(URL('touga', 'game','index'))

    except Exception as mError:
        print mError
        #session.flash = T('Some erros were found, try again!')
        redirect(URL('home','index'))
