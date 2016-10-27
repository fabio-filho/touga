# -*- coding: utf-8 -*-



def index():
    try:
        if request.args[0]!=session.current_game:
            session.current_game = request.args[0]

        mGame = db.tbGame(session.current_game)		
        mAuthGame = db(db.tbAuthGame.mGame==mGame.id).select(orderby=~db.tbAuthGame.mPoints|~db.tbAuthGame.mVictories|~(db.tbAuthGame.mProGoals-db.tbAuthGame.mGoalsAgainst)|~db.tbAuthGame.mProGoals)

        mCanShowsJoinButton = canAuthJoin(mGame.id)
        mMatchForm = getInputMatchForm(mGame)
        return dict(mGame=mGame, mAuthGame=mAuthGame, mCanShowsJoinButton=mCanShowsJoinButton, mMatchForm=mMatchForm)
    except Exception as mError:
        print mError
        redirect(URL('home','index'))


@auth.requires(lambda: MyAuth.isMaster())
def management():
    mGrid = SQLFORM.grid(db.tbGame, csv=False, searchable=False)
    return dict(mGrid=mGrid)




#===============================================================================


def canAuthJoin(mGameId):
    mGame = db.tbGame(mGameId)
    if MyAuth.isLogged():
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



def getInputMatchForm(mGame):
    if not MyAuth.isMaster(): return None

    mGoalsRange = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    mForm = SQLFORM.factory(
        Field('mPlayerOne', 'reference auth_user',label=T('Player 1'), default=0,requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s') ),
        Field('mPlayerOneGoals', 'integer', label=T('Player 1 goals'), default=0, requires=IS_IN_SET(mGoalsRange) ),
        Field('mPlayerTwo', 'reference auth_user', label=T('Player 2'), default=0, requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s') ),
        Field('mPlayerTwoGoals', 'integer', label=T('Player 2 goals'), default=0, requires=IS_IN_SET(mGoalsRange) ),
    )

    if mForm.process(onvalidation=onMatchFormValidation).accepted:
        addMatch(mGame,mForm)
        session.flash = T('Match added!')
        redirect(URL('game','index', args=mGame))
    elif mForm.errors:
        session.flash = T('Erros in form, please check it out!')

    return mForm

def onMatchFormValidation(mForm):

    if mForm.vars.mPlayerOne==mForm.vars.mPlayerTwo:
        mForm.errors.mPlayerTwo = T('The second player cannot be the same as the one above!')
    pass


def updateAuthGameRecord(mGame, mPlayerOne, mPlayerTwo):
    db(
        (db.tbAuthGame.mAuth==mPlayerOne[0])
        & (db.tbAuthGame.mGame==mGame)
    ).update(
        mPoints       = db.tbAuthGame.mPoints       + getPointsByGols(mPlayerOne[1], mPlayerTwo[1]),
        mVictories    = db.tbAuthGame.mVictories    + 1 if getPointsByGols(mPlayerOne[1], mPlayerTwo[1]) == 3 else 0,
        mDraws        = db.tbAuthGame.mDraws        + 1 if getPointsByGols(mPlayerOne[1], mPlayerTwo[1]) == 1 else 0,
        mLosses       = db.tbAuthGame.mLosses       + 1 if getPointsByGols(mPlayerOne[1], mPlayerTwo[1]) == 0 else 0,
        mMatches      = db.tbAuthGame.mMatches      + 1 ,
        mProGoals     = db.tbAuthGame.mProGoals     + mPlayerOne[1],
        mGoalsAgainst = db.tbAuthGame.mGoalsAgainst + mPlayerTwo[1]
    )

def addMatch(mGame, mForm):
    # Update player one
    updateAuthGameRecord(mGame,
        [mForm.vars.mPlayerOne, mForm.vars.mPlayerOneGoals],
        [mForm.vars.mPlayerTwo, mForm.vars.mPlayerTwoGoals]
    )
    # Update player two
    updateAuthGameRecord(mGame,
        [mForm.vars.mPlayerTwo, mForm.vars.mPlayerTwoGoals],
        [mForm.vars.mPlayerOne, mForm.vars.mPlayerOneGoals]
    )
    pass


def getPointsByGols(mPlayerOne, mPlayerTwo):

    if mPlayerOne > mPlayerTwo:
        return 3
    elif mPlayerOne == mPlayerTwo:
        return 1
    else:
        return 0
