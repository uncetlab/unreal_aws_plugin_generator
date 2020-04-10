using UnrealBuildTool;
using System.IO;

public class {{client_context['client-module-name']}} : ModuleRules
{
    public {{client_context['client-module-name']}}(ReadOnlyTargetRules Target) : base(Target)
    {
        PrivatePCHHeaderFile = "Private/{{client_context['client-module-name']}}PrivatePCH.h";

        bEnableExceptions = true;

        PublicDependencyModuleNames.AddRange(new string[] { "Engine", "Core", "CoreUObject", "InputCore", "Projects", "AWSBase", "BaseTPLibrary", {% for tp in client_context['TPModules']%} "{{tp['TPModuleName']}}",{%endfor%} });
        PrivateDependencyModuleNames.AddRange(new string[] { });

        PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public"));
        PrivateIncludePaths.Add(Path.Combine(ModuleDirectory, "Private"));


        if (Target.Type != TargetRules.TargetType.Server)
        {
            if (Target.Platform == UnrealTargetPlatform.Android || Target.Platform == UnrealTargetPlatform.Win64)
            {
                PublicDefinitions.Add("WITH_{{client_context['sh']}}=1");
            }
            else
            {
                PublicDefinitions.Add("WITH_{{client_context['sh']}}=0");
            }
        }
        else
        {
           PublicDefinitions.Add("WITH_{{client_context['sh']}}=0");
        }
    }
}
