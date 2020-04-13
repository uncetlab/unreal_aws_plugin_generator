# Unreal AWS Plugin Generator 
This repo was created to help with generating Unreal Plugins that link to the compiled aws c++ sdks. Creating Unreal Plugins that link to third party c++ libraries can be a pain to get right, so this code will take care of all the boilerplate files you need need to start building with the aws sdk. Currently only windows and android are supported. 

To understand the structure of the generated files you need to have some knowledge of how plugins work in Unreal. I recommend reading this page from Epic Games https://docs.unrealengine.com/en-US/Programming/Plugins/index.html. 

TLDR:
A plugin consists of atleast one module. A module can depend on other modules.


# What exactly is created?
The generator will generate a plugin with two kinds of modules: 
- ThirdPartyModules(TP):
    -- These are thin wrappers around the different aws sdks
    -- For example: S3TPModule would be a module that contains the compiled S3 sdk that other modules can depend on to use that sdk. 
- ClientModules
    -- These can depend on multiple different TPModules.
    -- This is where you should write you logic and expose things to Blueprints

TODO: Add more about this, a diagram, and talk about aws sdk dependencies on the basesdk 


## Environment Set Up
You need Python 3.7 or higher.
We are using Jinja2 to generate the files from templates and requests to download the files. Despite there not being many dependencies, I personally recommend using python virtual environments as it is a good habit. 

```pip install Jinja2```  
```pip install requests```


# What sdk are available? 
```python Scripts/generate.py list-aws-sdks```

## Get the compiled aws sdks
1. Download compiled sdks using ```download-sdks``` command 
2. Compile it yourself (TODO link to blog about how to do this)



## Generating a plugin
From the base directory run:

```python Scripts/generate.py make-plugin```


## Settings
Todo talk about structure of json objects and what they can modify

client-module is json of the structure:  
```json 
{  
  "client-module-name": "",  
  "sdk": "",  
  "sh": "",  
  "TPModules": [  
    "TPModuleJsons"  
  ]  
}
```

TP-module is a json of the structure:
```json
{
    "aws-sdk-name": "", 
    "TPModuleName": ""
}
```

## Example of an actual implementation 
https://github.com/uncetlab/unreal_aws_example_project
TODO: link to blog about how I have implenented some of the clients








