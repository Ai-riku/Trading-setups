# Welcome to this setup to trade algorithmically.

This folder will contain a working trading setup you can use to learn how to trade in the financial markets algorithmically. The setup can be used to trade any forex asset using the Interactive Brokers API. 

## Disclaimer
**This trading setup and its strategy are just a template and should not be used for live trading without appropriate backtesting and tweaking of the strategy parameters.**

1. Cautionary Note
    - Trading is not appropriate for all investors and carries a significant risk.
    - Markets are very unpredictable and unstable, and past performance does not guarantee future outcomes.
    - The trading setup and the strategy that are provided here are merely meant to be educational; they are not meant to be regarded as specific investing advice.
2. Limitations and Assumptions
    - Trading Experience: The trading setup and the strategy provided here are predicated on the supposition that traders possess the necessary expertise to comprehend the risks involved and modify both according to their unique risk tolerance and preferences.
    - Risk Capital: Trading should only be done with risk capital, and only people who have enough of it should think about trading. It is not advisable to trade with capital that can affect your way of life or your financial commitments.
    - Market Volatility: The trading setup and the strategy provided here are contingent upon the state of the market and may not yield anticipated results during periods of high market volatility or atypical occurrences.
    - No Promises: Trading losses are a possibility, and neither success nor profit are certain.
3. Accountability: By utilizing this trading setup and the strategy detailed in this repository, you agree that:
    - You have read and understood the disclaimer and risk warning.
    - You assume full accountability for the decisions you make about trading and investing.
    - You alone will bear responsibility for any losses you incur if you employ this trading setup and approach.
4. Additional Notes
    - Before putting any trading technique into practice, you must perform your own independent research and due diligence.
    - Trading involves emotions, and it is crucial to manage your emotions and risk tolerance effectively.
5. By continuing to use this trading setup and/or the strategy
    - You attest that you have read, comprehended, and accepted the risk warning and disclaimer.
    - You understand that trading carries a significant risk and that your trading and investment decisions are entirely your responsibility.

## Table of contents
1. [Author](#author)
2. [Setup properties](#properties)
3. [Read the documentation](#documentation)
4. [Ask for help](#help)
5. [Quick start](#start)

<a id='author'></a>
## Author
- [José Carlos Gonzáles Tanaka](https://www.linkedin.com/in/jose-carlos-gonzales-tanaka/)
- QuantInsti's EPAT content team is responsible for maintaining and contributing to this project.

<a id='properties'></a>
## Setup properties
- The trading setup allows you to trade any forex asset available in Interactive Brokers.
- You can only trade forex assets with this trading setup.
- It uses the Interactive Brokers API (IB API). It uses the stable version.
- It can be used with the TWS platform or the IB Gateway as long as the trader installs the stable versions of any of them.
- The setup is packaged as a Python library and is installable with one single code line.
- The trading setup package can be used in any Operating system, country, or timezone.
- There are 2 separate files apart from the trading setup package: The main file and the strategy_file file. The former is used to run the whole trading setup. The latter is to be changed per your discretion and contains all the relevant functions that can be tweaked to use your own strategy.
- The trading setup configuration consists only of the main and the strategy file. In case you want to test the setup only, you can modify the main file only and then run the file. If you want to incorporate your own strategy, modify both files and run the main file.
- The setup is ready to be tested or modified as per your needs.

<a id='documentation'></a>
## Read the documentation
This setup can be used only for forex assets with an Interactive Brokers API. 
- In case you want to test the trading setup quickly, please read: “Start_here_documentation”.
- In case you want to use a customized strategy, please read: “Strategy_documentation”.
- In case you want to learn more about the trading setup, please read: “The_trading_setup_references”.

<a id='help'></a>
## Ask for help
In case of questions, please write to:
- Your support manager (if you’re a present EPAT student)
- The alumni team (if you’re a past EPAT student and an alumnus)
- QuantInsti coordinates you see on our “Contact Us” page: [https://www.quantinsti.com/contact-us](https://www.quantinsti.com/contact-us)

<a id='start'></a>
## Quick start
1. Download the "trading_setup_folder" zip file, unzip it, and move the unzipped folder into the “..path_to/Jts" folder.
2. Open an Anaconda terminal (or a terminal in Linux or Mac), then type (wait until each command is completely run):

    - conda create --name setup_env python=3.12
   
      ![image01](res/image01.png)
      
    - conda activate setup_env
      
      ![image02](res/image02.png)
      
    - cd 'path_to/Jts/trading_setup_folder/installation_file'
      ![image03](res/image03.png)
    - pip install epat_trading_setup-1.0.0-py3-none-any.whl
      ![image04](res/image04.png)
    - cd ..
      ![image05](res/image05.png)
    - conda install spyder
      ![image06](res/image06.png)

4. Since you have already installed the IB API in 'path_to/Jts/tws_api'. Let's install it in our 'setup_env" environment. Type:
    - cd 'path_to/Jts/tws_api/source/pythonclient'
      ![image07](res/image07.png)
    - python setup.py install
      ![image08](res/image08.png)
    - cd C:\Jts
      ![image09](res/image09.png)
    - spyder
      ![image10](res/image10.png)
5. Once Spyder is opened, select as main folder the "trading_setup_folder" folder and open the "main.py" 
6. Modify the inputs as per your trading requirements.
7. Run the file, and

# Go live algo trading!
