# FuzzyProject
Script made for analyzing network parameters to give optimal result using fuzzy logic apparatus

Script takes client network speed and response time from host server as parameters and returns a number representing amount of blocks or content elements that should be created

# Installation
Script requires python 3 installed to run it

In Ubuntu, Mint and Debian you can install Python 3 like this:

```sh
$ sudo apt-get install python3 python3-pip
```

For other Linux flavors, macOS and Windows, packages are available at

https://www.python.org/getit/

# Usage
Script creates a single instance of tipping controller on object initialisation

Tipping controller initialises client speed(0 to 1000 mb), server response time(0 to 100 ms) and TrafficControl(0 to 100) therms and then creates membership for these ranges

Amount of blocks / content elements to be displayed is chosen using fuzzy rules:

```sh
rule1 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
rule2 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
rule3 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['average'], self.TrafficControl['Low'])
rule4 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['average'], self.TrafficControl['medium'])
rule6 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['good'], self.TrafficControl['medium'])
rule5 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['average'], self.TrafficControl['high'])
rule7 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
rule8 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['good'], self.TrafficControl['Low'])
rule9 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['good'], self.TrafficControl['high'])
```

Least amount of blocks / elements to be displayed is 17, while the highest is 83

After object is initialised you can use calculate method to get a result


### Here is a small example:

This code creates an instance of tipping controller. You cannot have multiple controllers at the same time.

```sh
calc = fuzzyCalculator()
```
Now you can use `calculate` method to get the result of the script.

```sh
print(calc.calculate(1000, 0))

83.0
```
Each calculation will also provide you with a plot

Plot for parameters used in previous example look like this:

![Plot](https://i.imgur.com/DR5CXsMl.png)
