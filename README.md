Endpoints API

 Route  | Method | Need authentication? | Usage 
 ------ | -------| -------------| -----
 /api/register/  | POST | None | Register a new user 
 /api/login/ | POST | None | Login as existing user 
 /api/login/refresh/ | GET | Yes | Refresh the login of the user
 /api/balance/ | GET | Yes | View current balance 
 /api/balance/deposit/ | POST | Yes | Deposit money from balance
 /api/balance/withdraw/ | POST | Yes | Withdraw money from balance
 /api/trade/index/ | GET | Yes | List of all the trades of the authenticated user with details
 /api/trade/<id>/ | GET | Yes | Details of one specific trade
 /api/trade/openPNL/ | GET | Yes | Show profit or loss of all open trades
 /api/trade/closePNL/ | GET | Yes | Shows profit or loss of all closed trades
 /api/trade/open/ | GET | Yes | List opened trades details of authenticated user
 /api/trade/close/ | GET | Yes | List closed trades details of authenticated user
 /api/trade/open/ | POST | Yes | Open a new trade 
 /api/trade/close/<id>/ | POST | Yes | Close an existing trade
