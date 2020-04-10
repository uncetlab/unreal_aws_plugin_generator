#include "AWSBaseModule.h"
#include "AWSBaseModulePrivatePCH.h"
#include "HAL/PlatformProcess.h"
#include "Interfaces/IPluginManager.h"
#include "Misc/Paths.h"

void* FAWSBaseModule::CEventDll = nullptr;
void* FAWSBaseModule::CCommonDll = nullptr;
void* FAWSBaseModule::ChecksumDll = nullptr;
void* FAWSBaseModule::CoreDll = nullptr;

TSet<void*> FAWSBaseModule::ValidDllHandles = TSet<void*>();

void FAWSBaseModule::StartupModule(){
#if PLATFORM_WINDOWS && PLATFORM_64BITS
    //If we are on a windows platform we need to Load the DLL's
    UE_LOG(LogTemp, Display, TEXT("Start Loading AWS Base DLL's"));
    const FString PluginDir = IPluginManager::Get().FindPlugin("{{context['plugin-name']}}")->GetBaseDir();
    const FString DllDir = FPaths::Combine(*PluginDir, TEXT("Source"), TEXT("ThirdParty"), TEXT("BaseTPLibrary"), TEXT("Win64"));


    const FString CCommonName = "aws-c-common";
    const FString CCommonPath = FPaths::Combine(DllDir, CCommonName) + TEXT(".") + FPlatformProcess::GetModuleExtension();
    if (!FAWSBaseModule::LoadDll(CCommonPath, FAWSBaseModule::CCommonDll, CCommonName)) {
        FAWSBaseModule::FreeAllDll();
    }

    const FString ChecksumName = "aws-checksums";
    const FString ChecksumPath = FPaths::Combine(DllDir, ChecksumName) + TEXT(".") + FPlatformProcess::GetModuleExtension();
    if (!FAWSBaseModule::LoadDll(ChecksumPath, FAWSBaseModule::ChecksumDll, ChecksumName)) {
        FAWSBaseModule::FreeAllDll();
    }

    const FString CEventName = "aws-c-event-stream";
    const FString CEventPath = FPaths::Combine(DllDir, CEventName) + TEXT(".") + FPlatformProcess::GetModuleExtension();
    if (!FAWSBaseModule::LoadDll(CEventPath, FAWSBaseModule::CEventDll, CEventName)) {
        FAWSBaseModule::FreeAllDll();
    }

    const FString CoreName = "aws-cpp-sdk-core";
    const FString CorePath = FPaths::Combine(DllDir, CoreName) + TEXT(".") + FPlatformProcess::GetModuleExtension();
    if (!FAWSBaseModule::LoadDll(CorePath, FAWSBaseModule::CEventDll, CoreName)) {
        FAWSBaseModule::FreeAllDll();
    }
#endif
    //this call is important as the aws sdk will not work without it being called before any other call to the aws sdk
    Aws::InitAPI(initialOptions);
}

void FAWSBaseModule::ShutdownModule(){
    //this call is important to shutting down the actual aws sdk... the actual aws sdk performs clean up for you.
    Aws::ShutdownAPI(initialOptions);
    
#if PLATFORM_WINDOWS && PLATFORM_64BITS
    FAWSBaseModule::FreeAllDll();
#endif
}

bool FAWSBaseModule::LoadDll(const FString path, void*& dll_ptr, const FString name) {
    //load the passed in dll and if it successeds then add it to the valid set
    UE_LOG(LogTemp, Error, TEXT("Attempting to load DLL %s from %s"), *name, *path);
    dll_ptr = FPlatformProcess::GetDllHandle(*path);

    if (dll_ptr == nullptr) {
        UE_LOG(LogTemp, Error, TEXT("Could not load %s from %s"), *name, *path);
        return false;
    }

    UE_LOG(LogTemp, Display, TEXT("Loaded %s from %s"), *name, *path);
    FAWSBaseModule::ValidDllHandles.Add(dll_ptr);
    return true;
}

void FAWSBaseModule::FreeDll(void*& dll_ptr) {
    //free the dll handle
    if (dll_ptr != nullptr) {
        FPlatformProcess::FreeDllHandle(dll_ptr);
        dll_ptr = nullptr;
    }
}

void FAWSBaseModule::FreeAllDll() {
    //Free all the current valid dll's
    for (auto dll : FAWSBaseModule::ValidDllHandles) {
        FAWSBaseModule::ValidDllHandles.Remove(dll);
        FAWSBaseModule::FreeDll(dll);
    }
}


IMPLEMENT_MODULE(FAWSBaseModule, AWSBase);