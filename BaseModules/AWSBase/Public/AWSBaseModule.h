#pragma once

#include "Modules/ModuleManager.h"
#include "aws/core/Aws.h"

class FAWSBaseModule : public IModuleInterface{
public:
	void StartupModule();
	void ShutdownModule();

private:
	static TSet<void*> ValidDllHandles;
	static void* CEventDll;
	static void* CCommonDll;
	static void* ChecksumDll;
	static void* CoreDll;

	Aws::SDKOptions initialOptions;


	bool LoadDll(const FString path, void*& dll_ptr, const FString name);

	void FreeDll(void*& dll_ptr);

	void FreeAllDll();

};