###Endpoints API

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

 
 
 ### List of forms
 
 
**-Form to register:**
 {
 "username": "your_username",
  "password": "your_password", 
  "password2": "your_password"
  "email": "your@email.com",
  "first_name": "your_first_name",
  "last_name": "your_last_name"
 }
 
 
 **-Form to login:** 
 {
 "username": "your_username",
  "password": "your_password"
 }
 
 
 **-Form to deposit in balance:** 
 {
 "deposit_amount": "<amount(can be decimals but not negative or 0)>"
 }
 
 
 **-Form to withdraw from balance:** 
 {
"withdraw_amount": "<amount(can be decimals but not negative or 0)>"
 }
 
 
  **-Form to open a trade:** 
 {
"amount": "<amount(can be decimals but not negative or 0)>",
 "symbol": "<write one of those: "BTC" OR "ETH">"
 }
 
 
  **-Form to close a trade:** 
 {
 "<let empty>"
 }
 
