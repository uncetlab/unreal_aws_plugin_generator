#pragma once

#include "CoreMinimal.h"
#include "Credentials.h"
#include "ClientConfiguration.h"

#include "aws/core/client/AWSClient.h"
#include "aws/core/auth/AWSCredentials.h"
#include "aws/core/client/ClientConfiguration.h"



class AWSBASE_API AWSSerializer{

public:

	//Returns the same pointer 
	static void* NoChange(void* in);

	//FString to Aws String
	static Aws::String FStoAS(FString s);

	//Aws String to FString
	static FString AStoFS(Aws::String s);

	static const Aws::Client::ClientConfiguration ClientConfiguration(FClientConfiguration config);
	static const Aws::Auth::AWSCredentials Credentials(FCredentials credentials);

	//FString Pointer to Aws String Pointer
	static Aws::String* PFStoPAS(FString* s);

	//Aws String Pointer to FString Pointer
	static FString* PAStoPFS(Aws::String* s);

	//TMap to Aws::Map where key and value are of the same type
	template <typename T>
	static Aws::Map<T,T> TMaptoAwsMap(TMap<T,T> in_map);

	//TMap to Aws::Map where values remain the same
	template <typename K, typename V>
	static Aws::Map<K, V> TMaptoAwsMap(TMap<K, V> in_map);

	//TMap to Aws::Map where you need to convert between types <typename AwsKey, typename AwsValue, typename UnrealKey, typename UnrealValue >
	template <typename AK, typename AV, typename UK, typename UV >
	static Aws::Map<AK, AV> TMaptoAwsMap(TMap<UK, UV> in_map, AK* (*keyConverter)(UK*), AV* (*valueConverter)(UV*));

	//Aws::Map to TMap where key and value are of the same type
	template <typename T>
	static TMap<T,T> AwsMaptoTMap(Aws::Map<T, T> in_map);

	//Aws::Map to TMap where values remain the same
	template <typename K, typename V>
	static TMap<K, V> AwsMaptoTMap(Aws::Map<K, V> in_map);

	//Aws::Map to TMap where you need to convert between types <typename AwsKey, typename AwsValue, typename UnrealKey, typename UnrealValue >
	template <typename AK, typename AV, typename UK, typename UV>
	static TMap<UK, UV> AwsMaptoTMap(Aws::Map<AK, AV> in_map, UK* (*keyConverter)(AK*), UV* (*valueConverter)(AV*));

	//TArray to Aws::Vector of same class
	template <typename T>
	static Aws::Vector<T> TArraytoAwsVector(TArray<T> in_array);

	//TArray to Aws::Vector with class conversion
	template <typename AT, typename UT>
	static Aws::Vector<AT> TArraytoAwsVector(TArray<UT> in_array, AT* (*valueConverter)(UT*));

	//Aws::Vector to TArray of same class
	template <typename T>
	static TArray<T> AwsVectortoTArray(Aws::Vector<T> in_array);

	//Aws::Vector to TArray with class conversion
	template <typename AT, typename UT>
	static TArray<UT>  AwsVectortoTArray(Aws::Vector<AT> in_array, UT* (*valueConverter)(AT*) );

	//TSet to Aws::Vector of same class
	template <typename T>
	static Aws::Vector<T> TSettoAwsVector(TSet<T> in_set);

	//TSet to Aws::Vector with class conversion
	template <typename AT, typename UT>
	static Aws::Vector<AT> TSettoAwsVector(TSet<UT> in_set, AT* (*valueConverter)(UT*));

	//Aws::Vector to TSet of same class
	template <typename T>
	static TSet<T> AwsVectortoTSet(Aws::Vector<T> in_array);

	//Aws::Vector to TSet with class conversion
	template <typename AT, typename UT>
	static TSet<UT> AwsVectortoTSet(Aws::Vector<AT> in_array, UT* (*valueConverter)(AT*));


};


#include "SerializerTemplatesImplementations.h"