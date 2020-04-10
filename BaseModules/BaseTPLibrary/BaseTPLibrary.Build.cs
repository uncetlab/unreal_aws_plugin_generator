//For more information about this file check out https://wiki.unrealengine.com/An_Introduction_to_UE4_Plugins
using UnrealBuildTool;
using System.IO;

public class BaseTPLibrary : ModuleRules{
    public BaseTPLibrary(ReadOnlyTargetRules Target) : base(Target){
        Type = ModuleType.External;

        PublicIncludePaths.Add(ModuleDirectory);

        PublicDefinitions.Add("USE_IMPORT_EXPORT");

        if (Target.Platform == UnrealTargetPlatform.Android){
            string AndroidPath = System.IO.Path.Combine(ModuleDirectory, UnrealTargetPlatform.Android.ToString());

            //Link to the APL (AndroidPluginLanguage) XML file
            AdditionalPropertiesForReceipt.Add("AndroidPlugin", System.IO.Path.Combine(ModuleDirectory, "BaseAPL.xml"));
            
            //armeabi-v7a
            PublicLibraryPaths.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-c-common.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-c-common.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-checksums.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-checksums.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-c-event-stream.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-c-event-stream.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-cpp-sdk-core.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "armeabi-v7a", "libaws-cpp-sdk-core.so"));
            
            //arm64-v8a
            PublicLibraryPaths.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-c-common.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-c-common.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-checksums.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-checksums.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-c-event-stream.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-c-event-stream.so"));

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-cpp-sdk-core.so"));
            RuntimeDependencies.Add(System.IO.Path.Combine(AndroidPath, "arm64-v8a", "libaws-cpp-sdk-core.so"));
        }
        else if (Target.Platform == UnrealTargetPlatform.Win64){
            string WindowPath = System.IO.Path.Combine(ModuleDirectory, UnrealTargetPlatform.Win64.ToString());

            PublicLibraryPaths.Add(WindowPath);

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(WindowPath, "aws-c-common.lib"));
            RuntimeDependencies.Add(System.IO.Path.Combine(WindowPath, "aws-c-common.dll"));
            PublicDelayLoadDLLs.Add("aws-c-common.dll");

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(WindowPath, "aws-checksums.lib"));
            RuntimeDependencies.Add(System.IO.Path.Combine(WindowPath, "aws-checksums.dll"));
            PublicDelayLoadDLLs.Add("aws-checksums.dll");

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(WindowPath, "aws-c-event-stream.lib"));
            RuntimeDependencies.Add(System.IO.Path.Combine(WindowPath, "aws-c-event-stream.dll"));
            PublicDelayLoadDLLs.Add("aws-c-event-stream.dll");

            PublicAdditionalLibraries.Add(System.IO.Path.Combine(WindowPath, "aws-cpp-sdk-core.lib"));
            PublicDelayLoadDLLs.Add("aws-cpp-sdk-core.dll");
            RuntimeDependencies.Add(System.IO.Path.Combine(WindowPath, "aws-cpp-sdk-core.dll"));                                                            
        }
    }
}