from jinja2 import Environment, FileSystemLoader
import os
import shutil 
import argparse, sys, json
import requests
from utils import printProgressBar

tmp_dir = '.tmp'



def deletetempdirectory():
    shutil.rmtree(os.path.join(".", tmp_dir))

def createtempdirectory():
    if os.path.isdir(os.path.join(".", tmp_dir)):
        print("Deleting old temp working directory")
        deletetempdirectory()
    
    os.mkdir(os.path.join(".", tmp_dir))

def makeSkeletonFolderStruct(context):
    plugin_name = context['plugin-name']
   

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)
    plugin_source_path = os.path.join(plugin_path, "Source")
    
    #Plugin Folders
    os.mkdir(plugin_path)
    os.mkdir(plugin_source_path)
    os.mkdir(os.path.join(plugin_path, "Resources"))

    #Make ThirdParty Folder
    os.mkdir(os.path.join(plugin_source_path, "ThirdParty"))

    for mod in context['client-modules']:
        #Client Module Folders
        os.mkdir(os.path.join(plugin_source_path, f"{mod['client-module-name']}"))
        os.mkdir(os.path.join(plugin_source_path, f"{mod['client-module-name']}", "Private"))
        os.mkdir(os.path.join(plugin_source_path, f"{mod['client-module-name']}", "Public"))

        for tp in mod['TPModules']:
            #Third Party Module Folder
            tp_module_name = tp['TPModuleName']
            tp_path = os.path.join(plugin_source_path, "ThirdParty", tp_module_name )
           
            if os.path.isdir(tp_path):
                continue

            os.mkdir(tp_path)
            
            for platform in context['supported_platforms']:
                os.mkdir(os.path.join(tp_path, platform['Platform']))
    
                for SubPlatform in platform['Sub-Platforms']:
                    os.mkdir(os.path.join(tp_path, platform['Platform'], SubPlatform))
    
def copyFilesFromBuild(context):
    #We need to copy the binary and header files of the actual aws sdk into the TP module folders
    plugin_name = context['plugin-name']

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)
    plugin_source_path = os.path.join(plugin_path, "Source")

    #for each client module look at the needed tp dependencies
    for clientmodule in context['client-modules']:
        for tpmodule in clientmodule['TPModules']:
            tp_path = os.path.join(plugin_source_path, "ThirdParty", tpmodule['TPModuleName'])
            isdirEmpty = True
            for dirpath, dirnames, files in os.walk(tp_path):
                if files:
                    #if we walk this folder we should not find any files unless we have already made this TP Module already 
                    isdirEmpty = False
                    break

            if not isdirEmpty:
                print(f"You have already made a {tpmodule['TPModuleName']} so you do not need two copies") 
                continue

            #Header files from source code
            header_src = os.path.join( context['binaries-path'], tpmodule['aws-sdk-name'], "aws")
            header_dst = os.path.join(tp_path, "aws")
            print(f"copying folder {header_src} to {header_dst}")
            shutil.copytree(header_src, header_dst)

            #Platform binaries
            #For each platform type copy the binaries
            for platform in context['supported_platforms']:
                platform_dir = os.path.join(tp_path, platform['Platform'])

                if len(platform['Sub-Platforms']) != 0:
                    for SubPlatform in platform['Sub-Platforms']:
                        sub_plat_dir = os.path.join(platform_dir, SubPlatform)
                        for filetype in platform['File-Types']:
                            filename = filetype['file-name'](tpmodule['aws-sdk-name'])

                            #make src file location
                            src = os.path.join(context['binaries-path'], tpmodule['aws-sdk-name'], filename)
                            dst = os.path.join(sub_plat_dir, filename )

                            print(f"Copying {src} to {dst}")
                            shutil.copyfile(src, dst)
                else:
                    for filetype in platform['File-Types']:
                        filename = filetype['file-name'](tpmodule['aws-sdk-name'])

                        #make src file location
                        src = os.path.join(context['binaries-path'], tpmodule['aws-sdk-name'], filename)
                        dst = os.path.join(platform_dir, filename)

                        print(f"Copying {src} to {dst}")
                        shutil.copyfile(src, dst)

def genetateTPTemplates(context):
    #We need to generate the template files for the third party modules
    plugin_name = context['plugin-name']

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)
    plugin_source_path = os.path.join(plugin_path, "Source")

    #jinja env
    env = Environment(loader=FileSystemLoader('templates'))

    #for each client module look at the needed tp dependencies
    for clientmodule in context['client-modules']:
        for tpmodule in clientmodule['TPModules']:
            tp_path = os.path.join(plugin_source_path, "ThirdParty", tpmodule['TPModuleName'])

            for template in context['tp-templates']:
                template_dst = template['path'](tp_path, tpmodule)
                
                if os.path.isfile(template_dst):
                    print(f"We have already made the generate files for the {tpmodule['TPModuleName']}")
                    break
                
                jinja_temp = env.get_template(template['name'])
                output = jinja_temp.render(context=tpmodule)
                print(template['msg'](tpmodule))

                with open(template_dst, 'w') as fh:
                    fh.write(output)
                
def makeTPModules(context):
    copyFilesFromBuild(context)

    genetateTPTemplates(context)

def generateClientTemplates(context):
    #We need to generate the template files for the third party modules
    plugin_name = context['plugin-name']

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)
    plugin_source_path = os.path.join(plugin_path, "Source")

    #jinja env
    env = Environment(loader=FileSystemLoader('templates'))
    
    for client_mod in context['client-modules']:
        client_path = os.path.join(plugin_source_path, client_mod['client-module-name'])

        #the module needs to know this to do some file finding 
        client_mod['plugin-name'] = context['plugin-name']
        
        for template in context['client-templates']:
            temp_dst = os.path.join(client_path, template['path'](client_mod['client-module-name']))

            jinja_temp = env.get_template(template['name'])
            output = jinja_temp.render(client_context=client_mod)

            print(template['msg'](client_mod['client-module-name']))
            with open(temp_dst,'w') as fh:
                fh.write(output)

def generatePlugingTemplates(context):
    #We need to generate the template files for the third party modules
    plugin_name = context['plugin-name']

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)

    #jinja env
    env = Environment(loader=FileSystemLoader('templates'))

    for plugin_temp in context['plugin-templates']:
        plugin_dst = os.path.join(plugin_path, plugin_temp['path'](context['plugin-name']))

        jinja_temp = env.get_template(plugin_temp['name'])
        output = jinja_temp.render(context=context)

        print(plugin_temp['msg'](context['plugin-name']) )
        with open(plugin_dst, "w") as fh:
            fh.write(output)

def moveBaseFiles(context):
    plugin_name = context['plugin-name']

    #Plugin paths
    plugin_path = os.path.join(".", tmp_dir, plugin_name)

    baseTPModule_src = os.path.join('./BaseModules', 'BaseTPLibrary')
    baseTPModule_dst = os.path.join(plugin_path, 'Source', 'ThirdParty', 'BaseTPLibrary')
    print(f"copying the BaseTPModule from {baseTPModule_src} to {baseTPModule_dst}" )
    shutil.copytree(baseTPModule_src, baseTPModule_dst)

    baseClientModule_src = os.path.join('./BaseModules', 'AWSBase')
    baseClientModule_dst = os.path.join(plugin_path, 'Source',  'AWSBase')
    print(f"copying the AWSBase Module from {baseClientModule_src} to {baseClientModule_dst}")
    shutil.copytree(baseClientModule_src, baseClientModule_dst)

    #Need to generate the base build file to have the correct plugin name in it 
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("BaseModules/AWSBaseModule.cpp")
    output = template.render(context=context)

    with open(os.path.join(baseClientModule_dst,"Private","AWSBaseModule.cpp"),'w') as fh:
        fh.write(output)
    print(f"Copying the Generated AWSBaseModule file to {os.path.join(baseClientModule_dst,'Private','AWSBaseModule.cpp')}")

    icon_src = os.path.join('./Templates', 'Resources', "Icon128.png")
    icon_dst = os.path.join(plugin_path, 'Resources', "Icon128.png")
    print(f"copying the icon from {icon_src} to {icon_dst}")
    shutil.copyfile(icon_src, icon_dst)

def copyWorktoOutput(context):
    if not os.path.isdir(os.path.join(context['output-dir'])):
        os.mkdir(os.path.join(context['output-dir']))

    dst = os.path.join(context['output-dir'], context['plugin-name'])
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    src = os.path.join(".", tmp_dir, context['plugin-name'])

    shutil.copytree(src, dst)

def CreatePlugin(context):
    template_dir = './Templates'
    loader = FileSystemLoader(template_dir)
    environment = Environment(loader=loader)

    #Step 1 
    createtempdirectory()

    #Step 2 
    makeSkeletonFolderStruct(context)

    #Step 3 
    makeTPModules(context)

    #Step 4
    generateClientTemplates(context)

    #Step 5
    generatePlugingTemplates(context)

    #Step 6
    moveBaseFiles(context)

    #Step 7
    copyWorktoOutput(context)

    #Step 8
    deletetempdirectory()

def printAwsSdks(settings):
    #Hard coded to work for directories called aws-cpp-sdk-<sdkname>
    #validate the binaries path is correct
    for sub_dir in os.listdir(os.path.join(settings['binaries-path'])):        
        if sub_dir[0:12] == "aws-cpp-sdk-":
            print(sub_dir[12:])

def downloadTPModule(sdks):
    rv = checkSettings()

    if not rv:
        print("You have some invliad settings please set them correctly")
        setSettings()

    with open(os.path.join('./Settings', 'localsettings.json')) as fh:
        loaded_settings = json.load(fh)

    binariesPath = loaded_settings['binaries-path']

    with open(os.path.join('./Settings', 'compiledsdkkeys.json')) as fh:
        potiential_sdks = json.load(fh)
    
    for aws_sdk in sdks:
        if aws_sdk in potiential_sdks:
            #Check if they already have this sdk in the binaries path
            if os.path.isdir(os.path.join(binariesPath, f"aws-cpp-sdk-{aws_sdk}")):
                replace_sdk = input(f"There is already a {aws_sdk} in your binaries folder. Would you like to replace it? (Yes/No)  ")
                if replace_sdk == "No":
                    print(f"Skipping {aws_sdk}")
                    continue                

            print(f"downloading {aws_sdk} from S3... It will take a minute")
            baseurl = f"https://unreal-aws-compiled-sdks.s3.amazonaws.com/aws-cpp-sdk-{aws_sdk}"

            total_keys = len(potiential_sdks[aws_sdk])
            indx=0
            printProgressBar(indx, total_keys, prefix=f"{aws_sdk} Progress", length=50)
            for key in potiential_sdks[aws_sdk]:
                s3_url = f"{baseurl}/{key}"
                results = requests.get(s3_url)

                if not results:
                    #Need better error handling when a download attempt fails
                    print(f"Failed to download {s3_url}")
                    continue

                #destination of downloaded file
                top_folder = f"aws-cpp-sdk-{aws_sdk}"
                if not os.path.isdir(os.path.join(binariesPath, top_folder)):
                    os.mkdir(os.path.join(binariesPath, top_folder))

                sub_folders = key.split('/')
                file_name = sub_folders.pop()

                #If the subfolders still has items then we need to make sure those path exisit on the file system in the build dir
                checked_path = os.path.join(binariesPath, top_folder)
                while not len(sub_folders) == 0:
                    checked_path = os.path.join(checked_path, sub_folders.pop(0))
                    if not os.path.isdir(checked_path):
                        os.mkdir(checked_path)
                       
                with open(os.path.join(binariesPath, top_folder, key), "wb") as fh:
                    fh.write(results.content)

                printProgressBar(indx, total_keys, prefix=f"{aws_sdk} Progress", length=50)
                indx = indx+1

            printProgressBar(total_keys, total_keys, prefix=f"{aws_sdk} Progress", length=50)
            print("")
            print(f"Finished downloading {aws_sdk}")
        else:
            print(f"{aws_sdk} is not a valid Third Party Module")
    
def setSettings():
    binaries_message = ""
    output_message = ""
    was_there_previous_build_setting = False
    was_there_previous_output_setting = False

    #First make sure they have a binaries folder saved
    if not os.path.isfile(os.path.join('./Settings', 'localsettings.json')):
        #We need to make a local settings file
        #ask them for directory to put modules in
        binaries_message = "Binaries Directory []: "
        output_message = "Output Directory []: "
        
    else:
        loaded_settings = {}
        with open(os.path.join('./Settings', 'localsettings.json')) as fh:
            try:
                loaded_settings = json.load(fh)
            except:
                #probably empty file somehow
                loaded_settings = {}

        if not 'binaries-path' in loaded_settings:
            #need to set the binaries path
            binaries_message = "Binaries Directory []: "

        else: 
            binaries_message = f"Binaries Directory [{loaded_settings['binaries-path']}]: "
            was_there_previous_build_setting = True

        if not 'output-dir' in loaded_settings:
            #need to set the output dir
            output_message = "Output Directory []: "

        else:
            output_message = f"Output Directory [{loaded_settings['output-dir']}]: "
            was_there_previous_output_setting = True
    
    new_binaries_path = input(binaries_message)
    has_build_path_been_confirmed = False

    if was_there_previous_build_setting and new_binaries_path == "":
        #they want to keep this setting
        new_binaries_path = loaded_settings['binaries-path']
        print(f"Keeping the previous binaries dir of {loaded_settings['binaries-path']}")

    else:
        while not has_build_path_been_confirmed:
            if not os.path.isdir(new_binaries_path):
                try:
                    os.mkdir(os.path.join(new_binaries_path))
                    print(f"Made your Binaries Directory: {new_binaries_path}")
                    has_build_path_been_confirmed = True
                except:
                    print(f"{new_binaries_path} was not already a directory and we could not make it a directory.")
                    new_binaries_path = input(binaries_message)

            else:
                #breaks loop
                has_build_path_been_confirmed = True

    new_output_dir = input(output_message)
    has_output_dir_been_confirmed = False

    if was_there_previous_output_setting and new_output_dir == "":
        new_output_dir = loaded_settings['output-dir']
        print(f"keeping the previous output dir of {loaded_settings['output-dir']}")

    else:
        while not has_output_dir_been_confirmed:
            if not os.path.isdir(new_output_dir):
                try:
                    os.mkdir(os.path.join(new_output_dir))
                    print(f"Made your Output directory: {new_output_dir}")
                    has_output_dir_been_confirmed = True
                except:
                    print(f"{new_output_dir} was not already a directory and we could not make it a directory.")
                    new_output_dir = input(output_message)
            else:
                has_output_dir_been_confirmed = True 



    new_settings = {}
    new_settings['binaries-path'] = new_binaries_path
    new_settings['output-dir'] = new_output_dir

    with open(os.path.join('./Settings', "localsettings.json"), 'w') as fh2:
        json.dump(new_settings, fh2)
        print("Saved your new local settings")

def checkSettings():
    #First make sure they have a binaries folder saved
    if not os.path.isfile(os.path.join('./Settings', 'localsettings.json')):
        #We need to make a local settings file
        #ask them for directory to put modules in
        return False
        
    else:
        with open(os.path.join('./Settings', 'localsettings.json')) as fh:
            try:
                loaded_settings = json.load(fh)
            except:
                #probably empty file or non-valid json 
                return False

        if not 'binaries-path' in loaded_settings:
            #need to set the binaries path
            return False

        elif not os.path.isdir(os.path.join(loaded_settings['binaries-path'])): 
            #binaries path variable is not a valid directory
            return False
        
        elif not 'output-dir' in loaded_settings:
            return False

        elif not os.path.isdir(os.path.join(loaded_settings['output-dir'])): 
            #binaries path variable is not a valid directory
            return False

        else:
            return True

def interactiveTPDownload(settings, aws_sdk):
    ## Download the compiled aws sdk if it is missing 
    if not os.path.isdir(os.path.join(settings["binaries-path"],f"aws-cpp-sdk-{aws_sdk}")):
        download_sdk = input(f"Looks like your binaries folder is missing the {aws_sdk} sdk. Would you like to download it? (Yes/No): ")
        is_valid_answer = False

        while not is_valid_answer:
            if download_sdk.lower() == "no":
                print("Without the correct compiled binaries you can not create this TP Modules")
                return False

            elif download_sdk.lower() == "yes":
                #Download the module
                downloadTPModule([aws_sdk])
                is_valid_answer = True

            else:
                print("please answer either Yes or No")
                download_sdk = input("Looks like your binaries folder is missing this sdk. Would you like to download it? (Yes/No): ")

def interactiveTPModule():
    aws_sdk = input("What aws sdk would you like to use? ")
    while not type(aws_sdk) is str:
        print("Name needs to be a string. try again.")
        aws_sdk = input("What aws sdk would you like to use? ")

    with open(os.path.join("./Settings", "sdks.json")) as fh:
        valid_sdks = json.load(fh)

    has_confirmed_sdk = False

    while not has_confirmed_sdk:
        if not aws_sdk in valid_sdks['names']:
            print(f"{aws_sdk} is not a valid sdk. try again.")
            aws_sdk = input("What aws sdk would you like to use? ")
        else:
            has_confirmed_sdk = True
    
    ##Assume setting was checked in previous calls
    with open(os.path.join('./Settings', 'localsettings.json')) as fh:
        try:
            loaded_settings = json.load(fh)
        except:
            #probably empty file somehow BAD
            loaded_settings = {}
    
    interactiveTPDownload(loaded_settings, aws_sdk)

    rv = {}

    rv['aws-sdk-name'] = f"aws-cpp-sdk-{aws_sdk}"
    rv['TPModuleName'] = valid_sdks['TPModuleNames'][aws_sdk]

    return rv
    
def interactiveClientModule():
    client_mod_name = input("What is the name of this client module: ")
    while not type(client_mod_name) is str:
        print("Name needs to be a string. try again.")
        client_mod_name = input("What is the name of this client module: ")

    finished_linking_TPModules = False
    tp_modules = []
    #first time the grammer is a little different
    tp_message = f"Would you like to link a TP Module to {client_mod_name}? (Yes/No) "

    while not finished_linking_TPModules:
        is_valid_response = False
        while not is_valid_response:
            another_TP = input(tp_message)

            if another_TP.lower() == "no":
                finished_linking_TPModules = True
                is_valid_response = True

            elif another_TP.lower() == "yes":
                tp_module = interactiveTPModule()
                if not tp_module:
                    #rv was false so it was not a valid TP module
                    print("")
                else:
                    tp_modules.append(tp_module)
                is_valid_response = True

            else:
                print("Please respond with either Yes or No.")
            #Change the grammer slightly for not first tp module
            tp_message = f"Would you like to link another TP Module to {client_mod_name}? (Yes/No) "

    if len(tp_modules) == 0:
        #Did not link any aws sdks so not a valid client module
        return False

    rv = {}
    rv['client-module-name'] = client_mod_name
    rv['TPModules'] = tp_modules

    return rv

def interactivePlugin():
    rv = checkSettings()

    if not rv:
        print("Before you can make a plugin please set your settings:")
        setSettings()

    plugin_name = input("What would you like the name of your plugin to be? ")
    
    while not type(plugin_name) is str:
        print("Name needs to be a string. try again.")
        plugin_name = input("What would you like the name of your plugin to be? ")

    plugin_description = input("Description of plugin: ")

    while not type(plugin_description) is str:
        print("Description needs to be a string. try again.")
        plugin_description = input("Description of plugin: ")

    finished_making_ClientModules = False
    client_modules = []
    #Grammer is a little different for the first message
    client_message = f"Would you like to make a client module for {plugin_name}? (Yes/No) "

    while not finished_making_ClientModules:
        is_valid_response = False
        while not is_valid_response:
            another_module = input(client_message)

            if another_module.lower() == "no":
                finished_making_ClientModules = True
                is_valid_response = True

            elif another_module.lower() == "yes":
                client_module = interactiveClientModule()
                if not client_module:
                    #rv was false so it was not a valid TP module
                    print("")
                else:
                    client_modules.append(client_module)
                is_valid_response = True

            else:
                print("Please respond with either Yes or No.")

        client_message = f"Would you like to make another client module for {plugin_name}? (Yes/No) "
    
    rv = {}
    rv['plugin-name'] = plugin_name
    rv['description'] = plugin_description
    rv['client-modules'] = client_modules

    return rv

def loadPluginFromFile(path):
    if not os.path.isfile(os.path.join(path)) or not path.endswith(".json"):
        print(f"{path} is not a valid json")
        return False

    with open(os.path.join(path)) as fh:
        try:
            loaded_plugin = json.load(fh)
        except:
            print("Plugin file was not a valid json")
            return False

    rv = validatePlugin(loaded_plugin)

    if type(rv) is str:
        print(rv)
        return False

    with open(os.path.join("./Settings", "sdks.json")) as fh:
        valid_sdks = json.load(fh)
    

    for client in loaded_plugin['client-modules']:
        new_tp_list = []
        for tp in client['TPModules']:
            with open(os.path.join('./Settings', 'localsettings.json')) as fh:
                loaded_settings = json.load(fh)

            interactiveTPDownload(loaded_settings, tp['aws-sdk-name'] )

            new_tp = {}
            new_tp['aws-sdk-name'] = f"aws-cpp-sdk-{tp['aws-sdk-name']}"
            new_tp['TPModuleName'] = valid_sdks['TPModuleNames'][tp['aws-sdk-name']]
            new_tp_list.append(new_tp)

            #check that they have the TP Modules in build folder
           

        
        client['TPModules'] = new_tp_list
        


    return loaded_plugin

def validateTPModule(tp_module):
    if not type(tp_module) is dict:
        return False

    if not "aws-sdk-name" in tp_module:
        return False
    if not type(tp_module['aws-sdk-name']) is str:
        return " name was not a string"
   
    with open(os.path.join("./Settings", "sdks.json")) as fh:
        valid_sdks = json.load(fh)

    if not tp_module['aws-sdk-name'] in valid_sdks['names']:
        return " is not a valid aws sdk"

    return True

def validateClientModule(client_module):
    if not type(client_module) is dict:
        return False

    if not "client-module-name" in client_module or not type(client_module['client-module-name']) is str:
        return False

    if not 'TPModules' in client_module or not type(client_module['TPModules']) is list:
        return f"{client_module['client-module-name']} did not have valid list of TP Modules"

    if len(client_module['TPModules']) == 0:
        return f"{client_module['client-module-name']} did not contain any TP Modules"

    for tp_mod in client_module['TPModules']:
        rv = validateTPModule(tp_mod)
        if type(rv) is str:
            return f"In {client_module['client-module-name']}: {tp_mod['aws-sdk-name']}{rv}" 

        if not rv:
            return f"One of the TP Modules in {client_module['client-module-name']} was not a valid TPModule json"

    return True

def validatePlugin(plugin):
    if not type(plugin) is dict:
       return "Context Object was not a dictionary"

    if not 'plugin-name' in plugin or not type(plugin['plugin-name']) is str:
        return "Invalid plugin name"

    if not 'description' in plugin or not type(plugin['description']) is str:
        return "Invalid description"

    if not 'client-modules' in plugin or not type(plugin['client-modules']) is list:
        return "Invalid list of client modules"

    if len(plugin['client-modules']) == 0:
        return "Did not provide any client modules"

    for client in plugin['client-modules']:
        rv = validateClientModule(client)

        if type(rv) is str:
            return rv
        elif not rv:
            return "Invalid client module name"
    
    return True

def main(): 
    #Global information for all genreated plugins
    context = {
        'plugin-prefix': 'AWS',
        'sdk-prefix': 'aws-cpp-sdk-',
        'tp-module-suffix': 'TPModule',
        'supported_platforms': [
            {
                'Platform':'Android',  
                'Sub-Platforms':['arm64-v8a', 'armeabi-v7a'],
                'File-Types': [
                    {
                        "file-name": (lambda name: f"lib{name}.so"),
                    }
                ]
            },  
            {
                'Platform':'Win64', 
                'Sub-Platforms':[],
                'File-Types': [
                    {
                        "file-name": (lambda name: f"{name}.dll"),
                    }, 
                    {
                        "file-name": (lambda name: f"{name}.lib"),
                    }
                ]

            }
        ],
        'tp-templates':[
            {
                'name': 'ThirdParty/Library/TemplateLibrary.Build.cs',
                'path': (lambda tp_path, tp_module: os.path.join(tp_path, f"{tp_module['TPModuleName']}.Build.cs")),
                'msg': (lambda tp_module: f"Writing the generated {tp_module['TPModuleName']}.Build.cs file")
            },
            {
                'name': 'ThirdParty/Library/Template_APL.xml',
                'path': (lambda tp_path, tp_module: os.path.join(tp_path, f"{tp_module['TPModuleName']}_APL.xml")),
                'msg': (lambda tp_module: f"Writing the generated {tp_module['TPModuleName']}_APL.xml file")
            },
        ],
        'client-templates':[
            {
                'name': 'Library/AWSName.build.cs',
                'path': (lambda name: os.path.join(f"{name}.build.cs")),
                'msg': (lambda name: f"Writing the generated {name}.build.cs file")
            },
            {
                'name': 'Library/Private/AWSNameModule.cpp',
                'path': (lambda name: os.path.join("Private", f"{name}Module.cpp")),
                'msg': (lambda name: f"Writing the generated {name}Module.cpp file")
            },
            {
                'name': 'Library/Private/AWSNamePrivatePCH.h',
                'path': (lambda name: os.path.join("Private", f"{name}PrivatePCH.h")),
                'msg': (lambda name: f"Writing the generated {name}PrivatePCH.h file")
            },
            {
                'name': 'Library/Public/AWSNameModule.h',
                'path': (lambda name: os.path.join("Public", f"{name}Module.h")),
                'msg': (lambda name: f"Writing the generated {name}Module.h file")
            },
            {
                'name': 'Library/Private/AWSNameClientObject.cpp',
                'path': (lambda name: os.path.join("Private", f"{name}ClientObject.cpp")),
                'msg': (lambda name: f"Writing the generated {name}ClientObject.cpp file")
            },
            {
                'name': 'Library/Public/AWSNameClientObject.h',
                'path': (lambda name: os.path.join("Public", f"{name}ClientObject.h")),
                'msg': (lambda name: f"Writing the generated {name}ClientObject.h file")
            },         
        ],
        'plugin-templates': [
             {
                'name': "Plugin/AwsDemo.uplugin",
                'path': (lambda name: os.path.join(f"{context['plugin-name']}.uplugin")),
                'msg': (lambda name: f"Writing the generated {context['plugin-name']}.uplugin file")
            } 
        ],
    }

    #command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs=1, help='Command to run', choices=["make-plugin",  "list-aws-sdks", "download-sdks", "set-settings"])
    parser.add_argument("--pluginfile", nargs=1, help='location of JSON file that describes the plugin you want to create')
    parser.add_argument("--sdks", nargs=1, help='comma seperated list of aws sdk names to download')

    arg = parser.parse_args(sys.argv[1:])
    

    if arg.command[0] == "list-aws-sdks":
        printAwsSdks(context)

    elif arg.command[0] == "download-sdks":
        if arg.sdks is None:
            print("You need to provide a comma seperated list of aws sdks to download as the --sdks flag. To see potiental names use list-aws-sdks command")

        else:
            sdks = arg.sdks[0].split(",")
            downloadTPModule(sdks)

    elif arg.command[0] == "set-settings":
        setSettings()

    elif arg.command[0] == "make-plugin":
        if not arg.pluginfile == None:
            plugin = loadPluginFromFile(arg.pluginfile[0])

            if not plugin:
                return

            context['plugin-name'] = plugin['plugin-name']
            context['description'] = plugin['description']
            context['client-modules'] = plugin['client-modules']
            
        else:
            info = interactivePlugin()

            context['plugin-name'] = info['plugin-name']
            context['description'] = info['description']
            context['client-modules'] = info['client-modules']


        with open(os.path.join("./Settings", "localsettings.json")) as fh:
            settings = json.load(fh)

        context['binaries-path'] = settings['binaries-path']
        context['output-dir'] = settings['output-dir']

        
        CreatePlugin(context)


if __name__ == "__main__":
    main()