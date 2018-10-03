import base64,time,requests,hashlib,json,hmac

class KredsUserAPI():
	def __init__(self,KREDS_API,KREDS_SECRET):
		self.url = "https://kredswallet.com/api"
		self.userURL = self.url+"/user"
		self.adminURL = self.url+"/admin"
		self.KREDS_API = KREDS_API
		self.KREDS_SECRET = KREDS_SECRET

	def genHeaders(self,params={}):
		params["nonce"] = str(round(time.time()*1000))
		payload = base64.b64encode(json.dumps(params).encode())
		SIGNATURE = hmac.new(payload,self.KREDS_SECRET.encode(),hashlib.sha512).hexdigest()
		return {
			"context-type":"application/json",
			"X-WWT-APIKEY":self.KREDS_API,
			"X-WWT-PAYLOAD":payload.decode("utf-8"),
			"X-WWT-SIGNATURE":SIGNATURE
		}

	"""
	USER FUNCTIONS
	"""
	
	def status(self): # Returns status of the API
		return requests.get("{}/status".format(self.userURL)).json()

	def info(self): # Returns information on the kreds wallet
		return requests.get("{}/info".format(self.userURL)).json()

	def validate(self,address):
		return requests.get("{}/validateAddress/{}".format(self.userURL,address))
	
	def address(self): # Generates a fresh address for your users
		headers = self.genHeaders()
		return requests.post("{}/address".format(self.userURL),headers=headers).json()

	def addresses(self,page=None,pagesize=None): # Gathers user's available addresses
		headers = self.genHeaders()
		if page and pagesize:
			return requests.get("{}/addresses/{}/{}".format(self.userURL,page,pagesize),headers=headers).json()
		elif page and not pagesize:
			return requests.get("{}/addresses/{}".format(self.userURL,page),headers=headers).json()
		elif pagesize and not page:
			return requests.get("{}/addresses/{}".format(self.userURL,pagesize),headers=headers).json()
		else:
			return requests.get("{}/addresses/".format(self.userURL),headers=headers).json()
		
	def balance(self,fromWallet=0): # Retrieves user's balance
		headers = self.genHeaders()
		return requests.get("{}/balance/{}".format(self.userURL,fromWallet),headers=headers).json()

	def deposits(self,page=None,pagesize=None): # Fetches account deposits
		headers = self.genHeaders()
		if page and pagesize:
			return requests.get("{}/deposits/{}/{}".format(self.userURL,page,pagesize),headers=headers).json()
		elif page and not pagesize:
			return requests.get("{}/deposits/{}".format(self.userURL,page),headers=headers).json()
		elif pagesize and not page:
			return requests.get("{}/deposits/{}".format(self.userURL,pagesize),headers=headers).json()
		else:
			return requests.get("{}/deposits/".format(self.userURL),headers=headers).json()
	
	def summary(self): # Gathers summary of the user's account
		headers = self.genHeaders()
		return requests.get("{}/summary".format(self.userURL),headers=headers).json()
	
	def transaction(self,TXID): # Gather details of provided TXID
		headers = self.genHeaders()
		return requests.get("{}/transactions/{}".format(self.userURL,TXID),headers=headers).json()
	
	def transactions(self,page=None,pagesize=None): # Gather information on all transactions for a user's account
		headers = self.genHeaders()
		if page and pagesize:
			return requests.get("{}/transactions/{}/{}".format(self.userURL,page,pagesize),headers=headers).json()
		elif page and not pagesize:
			return requests.get("{}/transactions/{}".format(self.userURL,page),headers=headers).json()
		elif pagesize and not page:
			return requests.get("{}/transactions/{}".format(self.userURL,pagesize),headers=headers).json()
		else:
			return requests.get("{}/transactions".format(self.userURL),headers=headers).json()

	def withdraw(self,ADDRESS,AMT,FEE): # Generate a new withdrawal
		headers = self.genHeaders()
		return requests.post("{}/withdraws/{}/{}/{}".format(self.userURL,ADDRESS,AMT,FEE),heades=headers).json()		
		
	def withdraws(self,page=None,pagesize=None): # Retrieve user's withdrawals
		headers = self.genHeaders()
		if page and pagesize:
			return requests.get("{}/withdraws/{}/{}".format(self.userURL,page,pagesize),headers=headers).json()
		elif page and not pagesize:
			return requests.get("{}/withdraws/{}".format(self.userURL,page),headers=headers).json()
		elif pagesize and not page:
			return requests.get("{}/withdraws/{}".format(self.userURL,pagesize),headers=headers).json()
		else:
			return requests.get("{}/withdraws".format(self.userURL),headers=headers).json()

class KredsAdminAPI():
	def __init__(self,KREDS_API,KREDS_SECRET):
		self.url = "https://kredswallet.com/api"
		self.userURL = self.url+"/user"
		self.adminURL = self.url+"/admin"
		self.KREDS_API = KREDS_API
		self.KREDS_SECRET = KREDS_SECRET

	def genHeaders(self,params={}):
		params["nonce"] = str(round(time.time()*1000))
		payload = base64.b64encode(json.dumps(params).encode())
		SIGNATURE = hmac.new(payload,self.KREDS_SECRET.encode(),hashlib.sha512).hexdigest()
		return {
			"context-type":"application/json",
			"X-WWT-APIKEY":self.KREDS_API,
			"X-WWT-PAYLOAD":payload.decode("utf-8"),
			"X-WWT-SIGNATURE":SIGNATURE
		}	

	"""
	ADMIN FUNCTIONS
	"""

	def account(self,withBalance=False,initialBalance=None) # Generates a fresh account
		headers = self.genHeaders()
		if withBalance:
			if initialBalance:
				return requests.post("{}/account/withBalance/{}".format(self.adminURL),headers=headers).json()
		else:
			return requests.post("{}/account".format(self.adminURL),headers=headers).json()
		
	def balance(self,account,fromWallet=0): # Retrieves user's balance
		headers = self.genHeaders()
		return requests.get("{}/balance/{}/{}".format(self.adminURL,account,fromWallet),headers=headers).json()

	def credit(self,ACCOUNT,AMT): # Credits an account
		headers = self.genHeaders()
		return requests.post("{}/account/credit/{}/{}".format(self.adminURL,ACCOUNT,AMT),headers=headers).json()
	
	def debit(self,ACCOUNT,AMT): # Debits an account
		headers = self.genHeaders()
		return requests.post("{}/account/debit/{}/{}".format(self.adminURL,ACCOUNT,AMT),headers=headers).json()
	
	def depositsSum(self,account,hours=24): # Retrieves deposits sum over X hours (default 24)
		headers = self.genHeaders()
		return requests.get("{}/deposits/sum/{}/{}".format(self.adminURL,account,hours),headers=headers).json()
	
	def reset(self,account): # Resets specified account
		headers = self.genHeaders()
		return requests.post("{}/reset/{}".format(self.adminURL,account),headers=headers).json()
	
	def withdrawsAvailable(self,account,hours=24,maxAmount=1000): # Retrieves withdraws available for specified user
		headers = self.genHeaders()
		return requests.get("{}/withdraws/available/{}/{}/{}".format(self.adminURL,account,hours,maxAmount),headers=headers).json()
	
	def withdrawsSum(self,account,hours=24): # Retrieves withdraw sum for user over specified time (default 24h)
		headers = self.genHeaders()
		return requests.get("{}/withdraws/sum/{}/{}".format(self.adminURL,account,hours),headers=headers).json()
