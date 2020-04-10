//For more information about this file check out https://wiki.unrealengine.com/An_Introduction_to_UE4_Plugins
using System.IO;
using UnrealBuildTool;

public class {{context["TPModuleName"]}} : ModuleRules{
    public {{context["TPModuleName"]}}(ReadOnlyTargetRules Target) : base(Target){
        Type = ModuleType.External;

        PublicIncludePaths.Add(ModuleDirectory);

        string ThirdPartyPath = System.IO.Path.Combine(ModuleDirectory, Target.Platform.ToString());

        if (Target.Platform == UnrealTargetPlatform.Android){
            AdditionalPropertiesForReceipt.Add("AndroidPlugin", System.IO.Path.Combine(ModuleDirectory, "{{context["TPModuleName"]}}_APL.xml"));
            {
                PublicLibraryPaths.Add(System.IO.Path.Combine(ThirdPartyPath, "armeabi-v7a"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(ThirdPartyPath, "armeabi-v7a", "lib{{context["aws-sdk-name"]}}.so"));
                RuntimeDependencies.Add(System.IO.Path.Combine(ThirdPartyPath, "armeabi-v7a", "lib{{context["aws-sdk-name"]}}.so"));
            }
            {
                PublicLibraryPaths.Add(System.IO.Path.Combine(ThirdPartyPath, "arm64-v8a"));
                PublicAdditionalLibraries.Add(System.IO.Path.Combine(ThirdPartyPath, "arm64-v8a", "lib{{context["aws-sdk-name"]}}.so"));
                RuntimeDependencies.Add(System.IO.Path.Combine(ThirdPartyPath, "arm64-v8a", "lib{{context["aws-sdk-name"]}}.so"));
            }
        }
       
        else if (Target.Platform == UnrealTargetPlatform.Win64){
            PublicLibraryPaths.Add(ThirdPartyPath);
            PublicAdditionalLibraries.Add(System.IO.Path.Combine(ThirdPartyPath, "{{context["aws-sdk-name"]}}.lib"));
            PublicDelayLoadDLLs.Add("{{context["aws-sdk-name"]}}.dll");
            RuntimeDependencies.Add(System.IO.Path.Combine(ThirdPartyPath, "{{context["aws-sdk-name"]}}.dll"));
        }
    }
}