#include "{{client_context['client-module-name']}}Module.h"
#include "{{client_context['client-module-name']}}PrivatePCH.h"
#include "HAL/PlatformProcess.h"
#include "Interfaces/IPluginManager.h"
#include "Misc/Paths.h"

{% for module in client_context['TPModules']%}
void* F{{client_context['client-module-name']}}Module::{{module["TPModuleName"]}}Dll = nullptr;
{% endfor %}

TSet<void*> F{{client_context['client-module-name']}}Module::ValidDllHandles = TSet<void*>();

void F{{client_context['client-module-name']}}Module::StartupModule(){
#if PLATFORM_WINDOWS && PLATFORM_64BITS
    //If we are on a windows platform we need to Load the DLL's
    UE_LOG(LogTemp, Display, TEXT("Start Loading DLL's"));
    const FString PluginDir = IPluginManager::Get().FindPlugin("{{client_context['plugin-name']}}")->GetBaseDir();
    

    {% for module in client_context['TPModules']%}
    const FString {{module["TPModuleName"]}}Name = "{{module["aws-sdk-name"]}}";
    FString {{module["TPModuleName"]}}DllDir = FPaths::Combine(*PluginDir, TEXT("Source"), TEXT("ThirdParty"), TEXT("{{module['TPModuleName']}}"), TEXT("Win64"));
    const FString {{module["TPModuleName"]}}Path = FPaths::Combine({{module["TPModuleName"]}}DllDir, {{module["TPModuleName"]}}Name) + TEXT(".") + FPlatformProcess::GetModuleExtension();
    if (!F{{client_context['client-module-name']}}Module::LoadDll({{module["TPModuleName"]}}Path, F{{client_context['client-module-name']}}Module::{{module["TPModuleName"]}}Dll, {{module["TPModuleName"]}}Name)) {
        F{{client_context['client-module-name']}}Module::FreeAllDll();
    }
    {% endfor %}
#endif
}

void F{{client_context['client-module-name']}}Module::ShutdownModule(){   
#if PLATFORM_WINDOWS && PLATFORM_64BITS
    F{{client_context['client-module-name']}}Module::FreeAllDll();
#endif
}

bool F{{client_context['client-module-name']}}Module::LoadDll(const FString path, void*& dll_ptr, const FString name) {
    //load the passed in dll and if it successeds then add it to the valid set
    UE_LOG(LogTemp, Error, TEXT("Attempting to load DLL %s from %s"), *name, *path);
    dll_ptr = FPlatformProcess::GetDllHandle(*path);

    if (dll_ptr == nullptr) {
        UE_LOG(LogTemp, Error, TEXT("Could not load %s from %s"), *name, *path);
        return false;
    }

    UE_LOG(LogTemp, Display, TEXT("Loaded %s from %s"), *name, *path);
    F{{client_context['client-module-name']}}Module::ValidDllHandles.Add(dll_ptr);
    return true;
}

void F{{client_context['client-module-name']}}Module::FreeDll(void*& dll_ptr) {
    //free the dll handle
    if (dll_ptr != nullptr) {
        FPlatformProcess::FreeDllHandle(dll_ptr);
        dll_ptr = nullptr;
    }
}

void F{{client_context['client-module-name']}}Module::FreeAllDll() {
    //Free all the current valid dll's
    for (auto dll : F{{client_context['client-module-name']}}Module::ValidDllHandles) {
        F{{client_context['client-module-name']}}Module::ValidDllHandles.Remove(dll);
        F{{client_context['client-module-name']}}Module::FreeDll(dll);
    }
}


IMPLEMENT_MODULE(F{{client_context['client-module-name']}}Module, {{client_context['client-module-name']}});