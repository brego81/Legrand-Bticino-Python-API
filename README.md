# Legrand Bticino Smarther API - An easy Python interface
Nowadays (2021) we see on the market a variety of Wi-Fi Chronothermostat equipped with an API suitable for domotic integration. When comparing functionalities and price, BTicino X8000 emerges as a competitive solution since it is easy to install and use, offers a stable and fully functioning smartphone app, and indeed presents a well documented and performing API. Further info on this API is available here: https://developer.legrand.com

![Alt text](img/BTicino_X8000.png?raw=true "BTicino_X8000" )

## Account setup
Before starting using this API tool, you need to create an account from https://developer.legrand.com/login/ and subscribe to "Starter Kit" in order to receive both Primary and Secondary keys. Importantly, the Primary Key represents the **Ocp-Apim-Subscription-Key** parameter used in the header of the HTML requests.

After subscribing to "Starter Kit", you then need to register a web application from https://mysettings.developer.legrand.com/Application/Index and define the application scope as **comfort.read** and **comfort.write**. Once you are done, within 24 hours you will receive an email containing the **client_id** and **client_secret** needed for API authentication.

If you are unsure how to set the web application parameters, you could use the following:
- Name: MyApp_PythonTest
- Description: MyApp_PythonTest
- Vendor: Test
- Type of the application: Web application
- Url: https://www.google.com
- First Reply Url: https://www.google.com

## How to use this Python API
Please note that in the very first run you will be asked to provide the following parameters which are going to be saved in the config.yaml file.
- client_id
- client_secret
- redirect_uri
- Ocp-Apim-Subscription-Key (Primary Key)

Later you will be asked to generate the **Authentication Code** by copy and paste an URL in your browser, follow the Sign-in and Accept steps, and finally paste back the redirect URL in the terminal. Crucially, the redirect URL contains the Authentication Code.

### Run the example code
Once you cloned or download the code, from you terminal you can just do the following

```
cd Legrand-Bticino-Python-API 
python -m pip install pprintpp pyyaml
python example.py
```
