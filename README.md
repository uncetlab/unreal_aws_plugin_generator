# Unreal AWS Plugin Generator 
This repo was created to help with generating the tedious parts of unreal plugins. After compiling the aws c++ sdk, it is still a lot of repatitive work to correctly make the plugin structure for each of the modules. By automating this step, we can quickly make different types of plugins that use aws. Also, the sdk is huge so you should not just make one big plugin that links to all the compiled sdks as that would probably slow down the startup time of your game.  

To understand the structure of the generated files you need to have some knowledge of how plugins work in Unreal. I recommend reading this page from Epic Games https://docs.unrealengine.com/en-US/Programming/Plugins/index.html. 

TLDR:
An Unreal code plugin consists of modules. These modules can depend on other modules.

The generator will generate two kinds of modules: 
- ThirdPartyModules(TP):
    These are thin wrappers around the different aws sdks 
- ClientModules
    These can depend on multiple different TPModules.
    This is where you should write you logic and expose things to Blueprints

TODO: Add more about this, a diagram, and talk about aws sdk dependencies on the basesdk 


## Get compiled aws sdks
1. Download compiled sdks from public S3 bucket: s3://unreal-aws-compiled-sdks (TODO add instructions/probably a script to do this but basically tou can curl or use aws cli)
2. Compile it yourself (TODO link to blog about how to do this)


## Environment Set Up
You Need Python 3.7 or greater cause I use string interpolation from this version.
We are using Jinja2 to generate the files from templates. Even though it is a single dependency, I personally recommend using python virtual environments as it is a good habit. 

pip install Jinja2



## Plugin Creation Steps 
1. Create tmp working directory
2. Create Skeleton folder structure in the working dir
3. Make the All the TP Modules from templates
4. Make the client Modules from templates
5. Make the Plugin from templates 
6. Make the Base Module from templates
7. Move files to Output directory and clean up 

TODO: rename files to be an actually good names
From the base module run:

python Scripts/render.py make-plugin --pluginfile <path-to-file>


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


## How to actually use this sdk 
https://sdk.amazonaws.com/cpp/api/0.14.3/index.html 
https://github.com/uncetlab/unreal_aws_example_project

TODO: link to blog about how I have implenented some of the clients
