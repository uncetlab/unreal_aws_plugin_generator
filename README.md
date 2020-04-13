# Unreal AWS Plugin Generator 
This repo was created to help with generating Unreal Plugins that link to the compiled aws c++ sdks. Creating Unreal Plugins that link to third party c++ libraries can be a pain to get right, so this code will take care of all the boilerplate files you need need to start building with the aws sdk. Currently only windows and android are supported. 

To understand the structure of the generated files you need to have some knowledge of how plugins work in Unreal. I recommend reading this page from Epic Games https://docs.unrealengine.com/en-US/Programming/Plugins/index.html. 

TLDR:
A plugin consists of atleast one module. A module can depend on other modules.


# What exactly is created?
The generator will generate a plugin with two kinds of modules: 
- ThirdPartyModules(TP):
    These are thin wrappers around the different aws sdks
    For example: S3TPModule would be a module that contains the compiled S3 sdk that other modules can depend on to use that sdk. 
- ClientModules
    These can depend on multiple different TPModules.
    This is where you should write you logic and expose things to Blueprints

TODO: Add more about this, a diagram, and talk about aws sdk dependencies on the basesdk 


## Get the compiled aws sdks
1. Download compiled sdks from public S3 bucket using ```download-sdks``` command 
2. Compile it yourself (TODO link to blog about how to do this)


## Environment Set Up
You Need Python 3.7 or greater cause I use string interpolation from python 3.7.
We are using Jinja2 to generate the files from templates. Even though it is a single dependency, I personally recommend using python virtual environments as it is a good habit. 

pip install Jinja2

## Generating a plugin
From the base directory run:

python Scripts/generate.py make-plugin --pluginfile <path-to-file>


## Settings
Todo talk about structure of json objects and what they can modify

client-module is json of the structure:
{
    "client-module-name": str,
    "sdk": str,
    "sh": str,
    "TPModules": [
        <TPModuleJsons>
    ]
}

TP-module is a json of the structure:
{
    "aws-sdk-name": str (must be valid aws sdk name), TODO write code to check this
    "TPModuleName": str
}

## Example of an actual implementation 
https://github.com/uncetlab/unreal_aws_example_project
TODO: link to blog about how I have implenented some of the clients


### Plugin Creation Steps 
1. Create tmp working directory
2. Create Skeleton folder structure in the working dir
3. Make the All the TP Modules from templates
4. Make the client Modules from templates
5. Make the Plugin from templates 
6. Make the Base Module from templates
7. Move files to Output directory and clean up 

TODO: rename files to be actually good names





