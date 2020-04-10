#pragma once 

#include "Modules/ModuleManager.h"
#include "GenericPlatform/GenericPlatformProcess.h"

class F{{client_context['client-module-name']}}Module : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

private:

	static TSet<void*> ValidDllHandles;
	{% for module in client_context['TPModules']%}
    static void* {{module["TPModuleName"]+"Dll"}};
    {% endfor %}

	bool LoadDll(const FString path, void*& dll_ptr, const FString name);

	void FreeDll(void*& dll_ptr);

	void FreeAllDll();

};