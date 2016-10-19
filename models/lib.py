# -*- coding: utf-8 -*-


class MessageBox:

	def __init__ (self, mMessage):
		session.flash = mMessage
		pass

	def showWarning(self):
		session.mMessageBox_Theme = "warning"
		session.mMessageBox_Icon  = "glyphicon glyphicon-warning-sign"
		session.mShowed = False
		pass

	def showSuccess(self):
		session.mMessageBox_Theme = "success"
		session.mMessageBox_Icon  = "glyphicon glyphicon-ok-circle"
		pass

	def showError(self):
		session.mMessageBox_Theme = "danger"
		session.mMessageBox_Icon  = "glyphicon glyphicon-remove-circle"
		pass

	def showInfo(self):
		session.mMessageBox_Theme = "info"
		session.mMessageBox_Icon  = "glyphicon glyphicon-info-sign"
		pass

	def setTimer(mTimer):
		try:
			session.mMessageBox_Timer = int(mTimer)
		except:
			session.mMessageBox_Timer = 4000
		pass

	def resetTimer():
		session.mMessageBox_Timer = 4000
		pass



class DateTime:

	def __init__():
		pass
	#Get date to make a query in the future.
	@staticmethod
	def getParcialDate(mYearIndex=0, mMonthIndex=1):

	    mYear  = request.now.year
	    mMonth = request.now.month

	    try:
	        if(len(request.args) >= 2):
		        #Check if the year is valid.
		        if request.args[mYearIndex]>0:
		            #Check if the month is correct.
		            if (int(request.args[mMonthIndex]) > 0) and (int(request.args[mMonthIndex]) < 13) :
		                return request.args[mYearIndex], request.args[mMonthIndex]

	    except Exception as mError:
	        print "getDate", mError

	    return mYear, mMonth


    #Get a beautiful date.
	@staticmethod
	def adjustDate(mValue=request.now):
		if not mValue:
			mValue = request.now
		return mValue.strftime("%d/%m/%Y")


	#Get a beautiful datetime.
	@staticmethod
	def adjustDateTime(mValue=request.now):
		if not mValue:
			mValue = request.now
		return mValue.strftime("%d/%m/%Y - %H:%Mh")


	#Get a beautiful datetime.
	@staticmethod
	def getSimpleDateTime(mValue=request.now):
		if not mValue:
			mValue = request.now
		return mValue.strftime("%d-%m-%Y_%Hh-%Mm")



	#Get a beautiful time.
	@staticmethod
	def adjustTime(mValue=request.now):
		if not mValue:
			mValue = request.now
		return mValue.strftime("%H:%Mh")


	#Get a beautiful time.
	@staticmethod
	def getBeautifulDate(mValue=request.now):
		if not mValue:
			mValue = request.now
		return mValue.strftime("%d") +' '+ T('of') +' '+ DateTime.getMonthName(mValue.strftime("%m")) +' '+ T('of') +' '+ mValue.strftime("%Y")


	#Get month name by a number.
	@staticmethod
	def getMonthName(mMonth):

		    mMonth = int(mMonth)
		    if mMonth == 1:
		        return T('January')
		    if mMonth == 2:
		        return T('February')
		    if mMonth == 3:
		        return T('March')
		    if mMonth == 4:
		        return T('April')
		    if mMonth == 5:
		        return T('May')
		    if mMonth == 6:
		        return T('June')
		    if mMonth == 7:
		        return T('July')
		    if mMonth == 8:
		        return T('August')
		    if mMonth == 9:
		        return T('September')
		    if mMonth == 10:
		        return T('October')
		    if mMonth == 11:
		        return T('November')
		    if mMonth == 12:
		        return T('December')

		    return T("No valid month.")






class Validation:

	@staticmethod
	def isMaster(mPage = URL('default', 'index')):
		if not Utilities.is_master():
			redirect(mPage)

	@staticmethod
	def isAdmin(mPage = URL('default', 'index')):
		if not Utilities.is_admin():
			redirect(mPage)

	@staticmethod
	def isInteger( mString):

		try:
			mNumber = int(mString)
			return True
		except Exception as mError:
			print "is_integer", mError
			return False


	@staticmethod
	def hasArgs( mLength):

		if len(request.args)==mLength:
			return True
		else:
			return False


	@staticmethod
	def hasVars( mLength):

		if len(request.vars)==mLength:
			return True
		else:
			return False


	@staticmethod
	def valideArgs( mLength, mUrl = URL('default', 'index')):
		#print mLength
		if not len(request.args)==mLength:
			#print mUrl
			redirect(mUrl)
		pass



	@staticmethod
	def valideMinimumArgs( mLength, mUrl = URL('default', 'index')):
		#print mLength
		if not len(request.args)>=mLength:
			#print mUrl
			redirect(mUrl)
		pass



	@staticmethod
	def valideMinimumVars( mLength, mUrl = URL('default', 'index')):
		#print mLength
		if not len(request.vars)>=mLength:
			#print mUrl
			redirect(mUrl)
		pass


	@staticmethod
	def hasMinimumVars( mLength, mUrl = URL('default', 'index')):

		if not len(request.vars)>=mLength:
			return False

		return True



	@staticmethod
	def formProcess( mForm, mUrl = URL('default', 'index'), mSuccessMessage=T('Added successfully!'),
						mErrorMessage=T('Erros in form, please check it out.'), mValidation=None, mOnAccepted=None, mOnErrors=None):

		processed = None

		if mValidation == None:
			processed = mForm.process()
		else:
			processed = mForm.process(onvalidation=mValidation)

		if processed.accepted:
			if not mOnAccepted == None:
				mOnAccepted(mForm)
			MessageBox(T(mSuccessMessage)).showSuccess()
			if not mUrl == None:
				redirect(mUrl)
		elif mForm.errors:
			if not mOnErrors == None:
				mOnErrors(mForm)
			MessageBox(T(mErrorMessage)).showError()

		pass




	@staticmethod
	def checkIsGroupOwner( mId, mTable, mUrl=URL('default', 'index')):

		try:
			mGroup = db.auth_group(id=db(auth.user_id == db.auth_membership.user_id).select()[0].group_id)
			mItem = mTable(mId)

			if mGroup == None:
				redirect(mUrl)

			if not mGroup.id == mItem.mUserGroup:
				redirect(mUrl)

		except mError:
			print 'check_is_group_owner except', mError
			print  mId, mTable, mUrl
			redirect(mUrl)




	@staticmethod
	def getDate():

		mYear = request.now.year
		mMonth = request.now.month

		try:
			int(mYear)
			if has_args(2):
				if (int(request.args[1]) > 0) and (int(request.args[1]) < 13) :
					return request.args[0], request.args[1]

			return mYear, mMonth
		except Exception as mError:
			print mError
			return mYear, mMonth

	pass



class MyAuth:

	@staticmethod
	def isLogged():
		try:
			if auth.is_logged_in():
				return True
			else:
				return False
		except:
			return False


	@staticmethod
	def isMaster():
		try:
			mAuth = db.auth_user(auth.user_id)
			if mAuth.is_master:
				return True
			else:
				return False
			pass
		except:
			return False
