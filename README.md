# Unreal AWS Plugin Generator 
This repo was created to help with generating Unreal Plugins that link to the compiled aws c++ sdks. Creating Unreal Plugins that link to third party c++ libraries can be a pain to get right, so this code will take care of all the boilerplate files you need need to start building with the aws sdk. Currently only windows and android are supported. 

To understand the structure of the generated files you need to have some knowledge of how plugins work in Unreal. I recommend reading this page from Epic Games https://docs.unrealengine.com/en-US/Programming/Plugins/index.html. 


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


## Settings
Before you can complete your first commands, you will be required to initialize some settings  
- **Binaries_Directory**: This will be the directory the scripts use to look for the compiled sdks  

You can change these settings anytime by running  
```python Scripts/generate.py settings```


# What sdk are available?
There are currently 220 available sdks so I can not include them all here. To check them look in Settings/sdks.json or run the following command  
```python Scripts/generate.py list-aws-sdks```

## Get the compiled aws sdks
1. Download compiled sdks using ```download-sdks``` command 
2. Compile it yourself (TODO link to blog about how to do this)


## Generating a plugin
From the base directory run:

```python Scripts/generate.py make-plugin```

## Plugin From a file
You can pass a file representing your plugin with the ```--pluginfile``` flag. Below is a description of how that file should look.  

Plugin is a json of the structure:
```json
{
    "plugin-name": "",
    "description": "",
    "plugin-prefix": "",
    "sdk-prefix": "",
    "tp-module-suffix": "",
    "client-modules": [
        "ClientModuleJsons"
    ]
}
```

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








